from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_usuario_atual
from app.domain.models.usuario import Usuario
from app.schemas.pedido import PedidoCriacao, PedidoResposta
from app.application.services.pedido_service import criar_pedido


router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.post("/", response_model=PedidoResposta, status_code=201)
def criar_pedido_endpoint(
    dados: PedidoCriacao,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(get_usuario_atual)
):
    try:
        pedido = criar_pedido(db, usuario_atual, dados)

        db.commit()
        db.refresh(pedido)

        return pedido

    except ValueError as erro:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao criar pedido."
        )