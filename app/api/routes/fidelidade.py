
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, exigir_perfil
from app.application.services.fidelidade_service import (
    consultar_saldo,
    listar_historico
)
from app.schemas.fidelidade import (
    SaldoFidelidadeResponse,
    HistoricoFidelidadeResponse
)


router = APIRouter(
    prefix="/fidelidade",
    tags=["Fidelidade"]
)


@router.get(
    "/meus-pontos",
    response_model=SaldoFidelidadeResponse
)
def obter_meu_saldo(
    db: Session = Depends(get_db),
    usuario=Depends(exigir_perfil("CLIENTE"))
):
    saldo = consultar_saldo(db, usuario.id)

    return {
        "saldo_pontos": saldo
    }


@router.get(
    "/meu-historico",
    response_model=list[HistoricoFidelidadeResponse]
)
def obter_meu_historico(
    db: Session = Depends(get_db),
    usuario=Depends(exigir_perfil("CLIENTE"))
):
    historico = listar_historico(db, usuario.id)

    return historico
