
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.api.dependencies import get_db, exigir_perfil
from app.domain.models.produto import Produto
from app.domain.models.unidade import Unidade
from app.domain.models.produto_unidade import ProdutoUnidade
from app.domain.models.estoque import Estoque
from app.schemas.produto_unidade import (
    ProdutoUnidadeCriacao,
    ProdutoUnidadeResposta
)
from app.schemas.produto_unidade import (
    ProdutoUnidadeCriacao,
    ProdutoUnidadeAtualizacao,
    ProdutoUnidadeResposta
)



router = APIRouter(
    prefix="/produto-unidades",
    tags=["Produtos por Unidade"]
)


@router.post(
    "/",
    response_model=ProdutoUnidadeResposta,
    status_code=status.HTTP_201_CREATED
)
def associar_produto_unidade(
    dados: ProdutoUnidadeCriacao,
    db: Session = Depends(get_db),
    usuario=Depends(exigir_perfil("GERENTE", "MATRIZ"))
):
    unidade = db.get(Unidade, dados.unidade_id)

    if not unidade or not unidade.ativa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidade não encontrada ou inativa."
        )

    produto = db.get(Produto, dados.produto_id)

    if not produto or not produto.ativo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado ou inativo."
        )

    associacao_existente = db.query(ProdutoUnidade).filter(
        ProdutoUnidade.unidade_id == dados.unidade_id,
        ProdutoUnidade.produto_id == dados.produto_id
    ).first()

    if associacao_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este produto já está associado a esta unidade."
        )

    if (
        dados.data_inicio_disponibilidade
        and dados.data_fim_disponibilidade
        and dados.data_fim_disponibilidade < dados.data_inicio_disponibilidade
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="A data final não pode ser anterior à data inicial."
        )

    associacao = ProdutoUnidade(
        unidade_id=dados.unidade_id,
        produto_id=dados.produto_id,
        preco_especifico=dados.preco_especifico,
        data_inicio_disponibilidade=dados.data_inicio_disponibilidade,
        data_fim_disponibilidade=dados.data_fim_disponibilidade,
        observacao_variacao=dados.observacao_variacao,
        habilitado=True
    )

    try:
        db.add(associacao)
        db.flush()

        estoque = Estoque(
            produto_unidade_id=associacao.id,
            quantidade_disponivel=0
        )

        db.add(estoque)
        db.commit()
        db.refresh(associacao)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não foi possível criar a associação. Verifique se ela já existe."
        )

    return associacao


@router.get(
    "/",
    response_model=list[ProdutoUnidadeResposta]
)
def listar_produtos_unidades(
    db: Session = Depends(get_db),
    usuario=Depends(exigir_perfil(
        "CLIENTE",
        "ATENDENTE",
        "COZINHA",
        "GERENTE",
        "MATRIZ"
    ))
):
    associacoes = db.query(ProdutoUnidade).all()

    return associacoes


@router.get(
    "/{produto_unidade_id}",
    response_model=ProdutoUnidadeResposta
)
def obter_produto_unidade(
    produto_unidade_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(exigir_perfil(
        "CLIENTE",
        "ATENDENTE",
        "COZINHA",
        "GERENTE",
        "MATRIZ"
    ))
):
    associacao = db.get(ProdutoUnidade, produto_unidade_id)

    if not associacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associação entre produto e unidade não encontrada."
        )

    return associacao


@router.patch(
    "/{produto_unidade_id}",
    response_model=ProdutoUnidadeResposta
)
def atualizar_produto_unidade(
    produto_unidade_id: int,
    dados: ProdutoUnidadeAtualizacao,
    db: Session = Depends(get_db),
    usuario=Depends(exigir_perfil("GERENTE", "MATRIZ"))
):
    associacao = db.get(ProdutoUnidade, produto_unidade_id)

    if not associacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associação entre produto e unidade não encontrada."
        )

    dados_atualizacao = dados.model_dump(exclude_unset=True)

    data_inicio = dados_atualizacao.get(
        "data_inicio_disponibilidade",
        associacao.data_inicio_disponibilidade
    )

    data_fim = dados_atualizacao.get(
        "data_fim_disponibilidade",
        associacao.data_fim_disponibilidade
    )

    if data_inicio and data_fim and data_fim < data_inicio:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="A data final não pode ser anterior à data inicial."
        )

    for campo, valor in dados_atualizacao.items():
        setattr(associacao, campo, valor)

    db.commit()
    db.refresh(associacao)

    return associacao


@router.delete("/{produto_unidade_id}")
def desativar_produto_unidade(
    produto_unidade_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(exigir_perfil("GERENTE", "MATRIZ"))
):
    associacao = db.get(ProdutoUnidade, produto_unidade_id)

    if not associacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Associação entre produto e unidade não encontrada."
        )

    if not associacao.habilitado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta associação já está desabilitada."
        )

    associacao.habilitado = False

    db.commit()
    db.refresh(associacao)

    return {
        "mensagem": "Associação desabilitada com sucesso.",
        "associacao": associacao
    }
