from datetime import date

from sqlalchemy.orm import Session

from decimal import Decimal


from app.domain.models.unidade import Unidade
from app.domain.models.usuario import Usuario
from app.domain.models.produto import Produto
from app.domain.models.produto_unidade import ProdutoUnidade
from app.domain.models.estoque import Estoque
from app.domain.models.pedido import Pedido
from app.domain.models.item_pedido import ItemPedido
from app.schemas.pedido import ItemPedidoCriacao
from app.schemas.pedido import PedidoCriacao


def validar_unidade(db: Session, unidade_id: int) -> Unidade:
    unidade = db.get(Unidade, unidade_id)

    if unidade is None:
        raise ValueError("Unidade não encontrada.")

    if not unidade.ativa:
        raise ValueError("Esta unidade está desativada.")

    return unidade


def validar_cliente(db: Session, cliente_id: int) -> Usuario:
    cliente = db.get(Usuario, cliente_id)

    if cliente is None:
        raise ValueError("Cliente não encontrado.")

    if not cliente.ativo:
        raise ValueError("Este cliente está desativado.")

    if cliente.perfil != "CLIENTE":
        raise ValueError("O usuário informado não possui perfil de cliente.")

    return cliente


def validar_atendente(db: Session,  atendente_id: int | None) -> Usuario | None:

    if atendente_id is None:
        return None

    atendente = db.get(Usuario, atendente_id)

    if atendente is None:
        raise ValueError("Atendente não encontrado.")

    if not atendente.ativo:
        raise ValueError("Este atendente está desativado.")

    if atendente.perfil != "ATENDENTE":
        raise ValueError("O usuário informado não possui perfil de atendente.")

    return atendente



def validar_produto_unidade(
    db: Session,
    unidade_id: int,
    produto_unidade_id: int
) -> tuple[ProdutoUnidade, Produto]:

    associacao = db.query(ProdutoUnidade).filter(
        ProdutoUnidade.id == produto_unidade_id,
        ProdutoUnidade.unidade_id == unidade_id
    ).first()

    if associacao is None:
        raise ValueError(
            "Produto não encontrado ou não associado a esta unidade."
        )

    if not associacao.habilitado:
        raise ValueError(
            "Este produto está desabilitado nesta unidade."
        )

    hoje = date.today()

    if (
        associacao.data_inicio_disponibilidade is not None
        and hoje < associacao.data_inicio_disponibilidade
    ):
        raise ValueError(
            "Este produto ainda não está disponível."
        )

    if (
        associacao.data_fim_disponibilidade is not None
        and hoje > associacao.data_fim_disponibilidade
    ):
        raise ValueError(
            "O período de disponibilidade deste produto terminou."
        )

    produto = db.get(Produto, associacao.produto_id)

    if produto is None or not produto.ativo:
        raise ValueError(
            "Este produto está inativo ou não foi encontrado."
        )

    return associacao, produto



def validar_estoque(
    db: Session,
    produto_unidade_id: int,
    quantidade_solicitada: int
) -> Estoque:

    estoque = db.query(Estoque).filter(
        Estoque.produto_unidade_id == produto_unidade_id
    ).first()

    if estoque is None:
        raise ValueError(
            "Registro de estoque não encontrado."
        )

    if estoque.quantidade_disponivel < quantidade_solicitada:
        raise ValueError(
            "Estoque insuficiente para atender ao pedido."
        )

    return estoque



def calcular_preco_item(
    associacao: ProdutoUnidade,
    produto: Produto,
    quantidade: int
) -> tuple[Decimal, Decimal]:

    if associacao.preco_especifico is not None:
        preco_unitario = associacao.preco_especifico
    else:
        preco_unitario = produto.preco_padrao

    subtotal = preco_unitario * quantidade

    return preco_unitario, subtotal


def preparar_itens_pedido(
    db: Session,
    unidade_id: int,
    itens: list[ItemPedidoCriacao]
) -> tuple[list[tuple[int, int, Decimal, Decimal]], Decimal]:

    produtos_processados = set()
    itens_preparados = []
    valor_total = Decimal("0.00")

    for item in itens:

        if item.produto_unidade_id in produtos_processados:
            raise ValueError(
                "O mesmo produto não pode ser repetido no pedido."
            )

        produtos_processados.add(item.produto_unidade_id)

        associacao, produto = validar_produto_unidade(
            db,
            unidade_id,
            item.produto_unidade_id
        )

        validar_estoque(
            db,
            item.produto_unidade_id,
            item.quantidade
        )

        preco_unitario, subtotal = calcular_preco_item(
            associacao,
            produto,
            item.quantidade
        )

        itens_preparados.append(
            (
                associacao.id,
                item.quantidade,
                preco_unitario,
                subtotal
            )
        )

        valor_total += subtotal

    return itens_preparados, valor_total

def identificar_compradores(
    db: Session,
    usuario_atual: Usuario,
    cliente_id: int | None
) -> tuple[int, int | None]:

    if usuario_atual.perfil == "CLIENTE":
        if cliente_id is not None:
            raise ValueError("Cliente não deve informar cliente_id.")

        validar_cliente(db, usuario_atual.id)
        return usuario_atual.id, None

    if usuario_atual.perfil == "ATENDENTE":
        if cliente_id is None:
            raise ValueError("Atendente deve informar cliente_id.")

        validar_cliente(db, cliente_id)
        validar_atendente(db, usuario_atual.id)

        return cliente_id, usuario_atual.id

    raise ValueError("Perfil não autorizado a criar pedidos.")


def validar_preparar_pedido(
    db: Session,
    usuario_atual: Usuario,
    dados: PedidoCriacao
):
    unidade = validar_unidade(db, dados.unidade_id)

    cliente_id, atendente_id = identificar_compradores(
        db,
        usuario_atual,
        dados.cliente_id
    )

    itens_preparados, valor_total = preparar_itens_pedido(
        db,
        unidade.id,
        dados.itens
    )

    return (
        unidade,
        cliente_id,
        atendente_id,
        itens_preparados,
        valor_total
    )



def criar_registro_pedido(
    db: Session,
    unidade_id: int,
    cliente_id: int,
    atendente_id: int | None,
    canal_pedido,
    valor_total: Decimal
) -> Pedido:

    pedido = Pedido(
        unidade_id=unidade_id,
        cliente_id=cliente_id,
        atendente_id=atendente_id,
        canal_pedido=canal_pedido,
        valor_total=valor_total
    )

    db.add(pedido)
    db.flush()

    return pedido


def criar_itens_pedido(
    db: Session,
    pedido_id: int,
    itens_preparados: list
) -> list[ItemPedido]:

    itens_criados = []

    for item in itens_preparados:
        produto_unidade_id, quantidade, preco_unitario, subtotal = item

        item_pedido = ItemPedido(
            pedido_id=pedido_id,
            produto_unidade_id=produto_unidade_id,
            quantidade=quantidade,
            preco_unitario=preco_unitario
        )

        db.add(item_pedido)
        itens_criados.append(item_pedido)

    return itens_criados


def criar_pedido(
    db: Session,
    usuario_atual: Usuario,
    dados: PedidoCriacao
) -> Pedido:

    (
        unidade,
        cliente_id,
        atendente_id,
        itens_preparados,
        valor_total
    ) = validar_preparar_pedido(
        db,
        usuario_atual,
        dados
    )

    pedido = criar_registro_pedido(
        db,
        unidade.id,
        cliente_id,
        atendente_id,
        dados.canal_pedido,
        valor_total
    )

    criar_itens_pedido(
        db,
        pedido.id,
        itens_preparados
    )

    return pedido