
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_usuario_atual
from app.domain.models.usuario import Usuario
from app.schemas.consentimento import (
    ConsentimentoCriacao,
    ConsentimentoResposta
)
from app.application.services.consentimento_service import (
    registrar_consentimento,
    listar_consentimentos,
    revogar_consentimento
)


router = APIRouter(
    prefix="/consentimentos",
    tags=["Consentimento LGPD"]
)


@router.post(
    "/",
    response_model=ConsentimentoResposta,
    status_code=status.HTTP_201_CREATED
)
def criar_consentimento(
    dados: ConsentimentoCriacao,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual)
):
    try:
        return registrar_consentimento(
            db=db,
            usuario_id=usuario.id,
            finalidade=dados.finalidade
        )
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(erro)
        )


@router.get(
    "/meus",
    response_model=list[ConsentimentoResposta]
)
def consultar_meus_consentimentos(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual)
):
    return listar_consentimentos(
        db=db,
        usuario_id=usuario.id
    )


@router.patch(
    "/{consentimento_id}/revogar",
    response_model=ConsentimentoResposta
)
def revogar_meu_consentimento(
    consentimento_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_atual)
):
    try:
        return revogar_consentimento(
            db=db,
            consentimento_id=consentimento_id,
            usuario_id=usuario.id
        )
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro)
        )
