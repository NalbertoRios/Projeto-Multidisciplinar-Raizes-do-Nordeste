from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_usuario_atual
from app.domain.models.usuario import Usuario
from app.schemas.pagamento import (
    PagamentoSimulacao,
    PagamentoResposta
)
from app.application.services.pagamento_service import (
    buscar_pedido,
    processar_pagamento
)


router = APIRouter(
    prefix="/pagamentos",
    tags=["Pagamentos"]
)


@router.post(
    "/{pedido_id}/simular",
    response_model=PagamentoResposta,
    status_code=201
)
def simular_pagamento_endpoint(
    pedido_id: int,
    dados: PagamentoSimulacao,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(get_usuario_atual)
):

    try:
        # 1. Identificar o perfil do usuário
        perfil = usuario_atual.perfil

        if hasattr(perfil, "value"):
            perfil = perfil.value

        # 2. Buscar o pedido
        pedido = buscar_pedido(db, pedido_id)

        # 3. Verificar autorização
        if perfil == "CLIENTE":

            if pedido.cliente_id != usuario_atual.id:
                raise HTTPException(
                    status_code=403,
                    detail="Você não pode pagar este pedido."
                )

        elif perfil == "ATENDENTE":

            if pedido.atendente_id != usuario_atual.id:
                raise HTTPException(
                    status_code=403,
                    detail="Você não pode processar o pagamento deste pedido."
                )

        else:
            raise HTTPException(
                status_code=403,
                detail="Perfil não autorizado a processar pagamentos."
            )

        # 4. Processar o pagamento
        pagamento = processar_pagamento(
            db,
            pedido_id,
            dados.aprovado
        )

        # 5. Confirmar transação
        db.commit()
        db.refresh(pagamento)

        return pagamento

    except HTTPException:
        db.rollback()
        raise

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
            detail="Erro interno ao processar pagamento."
        )