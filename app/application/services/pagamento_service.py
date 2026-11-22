
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.domain.models.pedido import Pedido
from app.domain.models.pagamento import Pagamento
from app.domain.models.estoque import Estoque

from app.domain.enums.status_pedido import StatusPedido
from app.domain.enums.status_pagamento import StatusPagamento

from app.application.services.fidelidade_service import creditar_pontos


def buscar_pedido(db: Session, pedido_id: int) -> Pedido:
    pedido = db.query(Pedido).filter(
        Pedido.id == pedido_id
    ).first()

    if not pedido:
        raise ValueError("Pedido não encontrado.")

    return pedido


def validar_pedido_para_pagamento(pedido: Pedido):
    if pedido.status != StatusPedido.AGUARDANDO_PAGAMENTO:
        raise ValueError(
            "Pedido não está aguardando pagamento."
        )

    if not pedido.itens:
        raise ValueError("Pedido não possui itens.")

    if pedido.valor_total <= 0:
        raise ValueError("Valor do pedido inválido.")


def obter_numero_tentativa(
    db: Session,
    pedido_id: int
) -> int:
    ultima_tentativa = db.query(
        func.max(Pagamento.numero_tentativa)
    ).filter(
        Pagamento.pedido_id == pedido_id
    ).scalar()

    return (ultima_tentativa or 0) + 1


def validar_estoque_pedido(
    db: Session,
    pedido: Pedido
):
    for item in pedido.itens:
        estoque = db.query(Estoque).filter(
            Estoque.produto_unidade_id
            == item.produto_unidade_id
        ).first()

        if not estoque:
            raise ValueError(
                "Estoque não encontrado para um item do pedido."
            )

        if estoque.quantidade_disponivel < item.quantidade:
            raise ValueError(
                "Estoque insuficiente para pagamento."
            )


def baixar_estoque_pedido(
    db: Session,
    pedido: Pedido
):
    for item in pedido.itens:
        estoque = db.query(Estoque).filter(
            Estoque.produto_unidade_id
            == item.produto_unidade_id
        ).first()

        if not estoque:
            raise ValueError(
                "Estoque não encontrado para um item do pedido."
            )

        estoque.quantidade_disponivel -= item.quantidade


def processar_pagamento(
    db: Session,
    pedido_id: int,
    aprovado: bool
) -> Pagamento:

    # 1. Buscar o pedido
    pedido = buscar_pedido(db, pedido_id)

    # 2. Validar se o pedido pode receber pagamento
    validar_pedido_para_pagamento(pedido)

    # 3. Identificar o número da tentativa
    tentativa = obter_numero_tentativa(
        db,
        pedido_id
    )

    # 4. Definir o resultado da simulação
    if aprovado:

        # Verificar estoque antes da aprovação
        validar_estoque_pedido(db, pedido)

        status_pagamento = StatusPagamento.APROVADO

        # Baixar estoque após aprovação simulada
        baixar_estoque_pedido(db, pedido)

        # Atualizar o status do pedido
        pedido.status = StatusPedido.EM_PREPARO

    else:
        # Pagamento recusado: não baixa estoque
        status_pagamento = StatusPagamento.RECUSADO

    # 5. Registrar a tentativa de pagamento
    pagamento = Pagamento(
        pedido_id=pedido.id,
        status_pagamento=status_pagamento,
        valor=pedido.valor_total,
        numero_tentativa=tentativa,
        referencia_transacao=(
            f"SIM-{pedido.id}-{tentativa}"
        )
    )

    db.add(pagamento)

    # 6. Persistir dentro da transação atual
    # O flush disponibiliza o ID do pagamento
    db.flush()

    # 7. Creditar pontos somente se aprovado
    # O serviço verifica o consentimento do cliente
    if aprovado:
        creditar_pontos(
            db=db,
            pedido=pedido,
            pagamento=pagamento
        )

    # O commit será realizado pela rota de pagamentos
    return pagamento
