from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_db,
    get_usuario_atual,
    exigir_perfil
)

from app.domain.models.unidade import Unidade

from app.schemas.unidade import (
    UnidadeCriacao,
    UnidadeAtualizacao,
    UnidadeResposta
)


router = APIRouter(
    prefix="/unidades",
    tags=["Unidades"]
)


@router.post(
    "/",
    response_model=UnidadeResposta,
    status_code=status.HTTP_201_CREATED
)
def cadastrar_unidade(
    dados: UnidadeCriacao,
    db: Session = Depends(get_db),
    usuario=Depends(exigir_perfil("GERENTE", "MATRIZ"))
):
    unidade = Unidade(
        nome=dados.nome,
        cidade=dados.cidade,
        regiao=dados.regiao
    )

    db.add(unidade)
    db.commit()
    db.refresh(unidade)

    return unidade


@router.get(
    "/",
    response_model=list[UnidadeResposta]
)
def listar_unidades(
    db: Session = Depends(get_db),
    usuario=Depends(get_usuario_atual)
):
    unidades = db.query(Unidade).all()

    return unidades

@router.get(
    "/{unidade_id}",
    response_model=UnidadeResposta
)
def buscar_unidade(
    unidade_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(get_usuario_atual)
):
    unidade = db.query(Unidade).filter(
        Unidade.id == unidade_id
    ).first()

    if unidade is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidade não encontrada."
        )

    return unidade

@router.patch(
    "/{unidade_id}",
    response_model=UnidadeResposta
)
def atualizar_unidade(
    unidade_id: int,
    dados: UnidadeAtualizacao,
    db: Session = Depends(get_db),
    usuario=Depends(exigir_perfil("GERENTE", "MATRIZ"))
):
    unidade = db.query(Unidade).filter(
        Unidade.id == unidade_id
    ).first()

    if unidade is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidade não encontrada."
        )

    dados_atualizacao = dados.model_dump(exclude_unset=True)

    for campo, valor in dados_atualizacao.items():
        setattr(unidade, campo, valor)

    db.commit()
    db.refresh(unidade)

    return unidade

@router.delete("/{unidade_id}")
def desativar_unidade(
    unidade_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(exigir_perfil("GERENTE", "MATRIZ"))
):
    unidade = db.query(Unidade).filter(
        Unidade.id == unidade_id
    ).first()

    if unidade is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidade não encontrada."
        )

    if not unidade.ativa:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta unidade já está desativada."
        )

    unidade.ativa = False

    db.commit()
    db.refresh(unidade)

    return {
        "mensagem": "Unidade desativada com sucesso.",
        "unidade": UnidadeResposta.model_validate(unidade)
    }