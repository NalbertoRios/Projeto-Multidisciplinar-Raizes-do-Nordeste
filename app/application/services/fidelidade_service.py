from decimal import Decimal, ROUND_DOWN
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.domain.models.consentimento import Consentimento
from app.domain.models.ponto_fidelidade import PontoFidelidade


FINALIDADE_FIDELIDADE = "PROGRAMA_FIDELIDADE"


def cliente_aderiu_fidelidade(
    db: Session,
    cliente_id: int
) -> bool:

    consentimento = db.query(Consentimento).filter(
        Consentimento.usuario_id == cliente_id,
        Consentimento.finalidade == FINALIDADE_FIDELIDADE,
        Consentimento.autorizado == True,
        Consentimento.data_revogacao.is_(None)
    ).first()

    return consentimento is not None


def calcular_pontos(valor: Decimal) -> int:
    """
    Regra MVP:
    1 ponto por R$ 1,00 pago.
    Frações de reais são arredondadas para baixo.
    """

    return int(
        valor.quantize(
            Decimal("1"),
            rounding=ROUND_DOWN
        )
    )


def creditar_pontos(
    db: Session,
    pedido,
    pagamento
):
    # 1. Somente pagamentos aprovados geram pontos.
    if pagamento.status_pagamento.value != "APROVADO":
        return None

    # 2. Verificar se o cliente aderiu ao programa.
    if not cliente_aderiu_fidelidade(
        db,
        pedido.cliente_id
    ):
        return None

    # 3. Prevenir crédito duplicado.
    credito_existente = db.query(PontoFidelidade).filter(
        PontoFidelidade.pedido_id == pedido.id
    ).first()

    if credito_existente:
        return credito_existente

    # 4. Calcular pontos com base no pagamento.
    pontos = calcular_pontos(pagamento.valor)

    if pontos <= 0:
        return None

    # 5. Registrar crédito no histórico.
    credito = PontoFidelidade(
        cliente_id=pedido.cliente_id,
        pedido_id=pedido.id,
        pagamento_id=pagamento.id,
        pontos=pontos
    )

    db.add(credito)

    # Não faz commit aqui.
    # O commit será realizado pelo endpoint de pagamento.

    return credito

def consultar_saldo(db: Session, cliente_id: int) -> int:
    saldo = db.query(
        func.coalesce(func.sum(PontoFidelidade.pontos), 0)
    ).filter(
        PontoFidelidade.cliente_id == cliente_id
    ).scalar()

    return saldo


def listar_historico(db: Session, cliente_id: int):
    return db.query(PontoFidelidade).filter(
        PontoFidelidade.cliente_id == cliente_id
    ).order_by(
        PontoFidelidade.data_credito.desc()
    ).all()