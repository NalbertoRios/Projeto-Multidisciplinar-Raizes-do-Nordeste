
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, exigir_perfil
from app.domain.models.estoque import Estoque
from app.schemas.estoque import EstoqueResposta, EstoqueAtualizacao


router = APIRouter(
    prefix="/estoques",
    tags=["Gestão de Estoque"]
)


@router.get(
    "/",
    response_model=list[EstoqueResposta]
)
def listar_estoques(
    db: Session = Depends(get_db),
    usuario=Depends(exigir_perfil(
        "ATENDENTE",
        "COZINHA",
        "GERENTE",
        "MATRIZ"
    ))
):
    estoques = db.query(Estoque).all()

    return estoques


@router.get(
    "/{estoque_id}",
    response_model=EstoqueResposta
)
def obter_estoque(
    estoque_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(exigir_perfil(
        "ATENDENTE",
        "COZINHA",
        "GERENTE",
        "MATRIZ"
    ))
):
    estoque = db.get(Estoque, estoque_id)

    if not estoque:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de estoque não encontrado."
        )

    return estoque


@router.patch(
    "/{estoque_id}",
    response_model=EstoqueResposta
)
def atualizar_estoque(
    estoque_id: int,
    dados: EstoqueAtualizacao,
    db: Session = Depends(get_db),
    usuario=Depends(exigir_perfil("GERENTE", "MATRIZ"))
):
    estoque = db.get(Estoque, estoque_id)

    if not estoque:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de estoque não encontrado."
        )

    estoque.quantidade_disponivel = dados.quantidade_disponivel

    db.commit()
    db.refresh(estoque)

    return estoque

