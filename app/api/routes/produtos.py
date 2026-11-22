from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_usuario_atual, exigir_perfil
from app.domain.models.produto import Produto
from app.schemas.produto import (
    ProdutoCriacao,
    ProdutoAtualizacao,
    ProdutoResposta
)

router = APIRouter(
    prefix="/produtos",
    tags=["Produtos"]
)


@router.post(
    "/",
    response_model=ProdutoResposta,
    status_code=status.HTTP_201_CREATED
)
def cadastrar_produto(
    dados: ProdutoCriacao,
    db: Session = Depends(get_db),
    usuario = Depends(
        exigir_perfil("GERENTE", "MATRIZ")
    )
):
    produto = Produto(
        nome=dados.nome,
        descricao=dados.descricao,
        preco_padrao=dados.preco_padrao
    )

    db.add(produto)
    db.commit()
    db.refresh(produto)

    return produto


@router.get(
    "/",
    response_model=list[ProdutoResposta]
)
def listar_produtos(
    db: Session = Depends(get_db),
    usuario = Depends(get_usuario_atual)
):
    produtos = db.query(Produto).all()
    return produtos

@router.get("/{produto_id}", response_model=ProdutoResposta)
def buscar_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario = Depends(get_usuario_atual)
):
    produto = db.query(Produto).filter(
        Produto.id == produto_id
    ).first()

    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado."
        )

    return produto


@router.patch("/{produto_id}", response_model=ProdutoResposta)
def atualizar_produto(
    produto_id: int,
    dados: ProdutoAtualizacao,
    db: Session = Depends(get_db),
    usuario = Depends(exigir_perfil("GERENTE", "MATRIZ"))
):
    produto = db.query(Produto).filter(
        Produto.id == produto_id
    ).first()

    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado."
        )

    dados_atualizacao = dados.model_dump(exclude_unset=True)

    for campo, valor in dados_atualizacao.items():
        setattr(produto, campo, valor)

    db.commit()
    db.refresh(produto)

    return produto

@router.delete("/{produto_id}")
def desativar_produto(
    produto_id: int,
    db: Session = Depends(get_db),
    usuario = Depends(exigir_perfil("GERENTE", "MATRIZ"))
):
    produto = db.query(Produto).filter(
        Produto.id == produto_id
    ).first()

    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado."
        )

    if not produto.ativo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este produto já está desativado."
        )

    produto.ativo = False

    db.commit()
    db.refresh(produto)

    return {
        "mensagem": "Produto desativado com sucesso.",
        "produto": ProdutoResposta.model_validate(produto)
    }