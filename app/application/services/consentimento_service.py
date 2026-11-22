
from datetime import datetime

from sqlalchemy.orm import Session

from app.domain.models.consentimento import Consentimento


def registrar_consentimento(
    db: Session,
    usuario_id: int,
    finalidade: str
):
    consentimento_existente = db.query(Consentimento).filter(
        Consentimento.usuario_id == usuario_id,
        Consentimento.finalidade == finalidade,
        Consentimento.autorizado == True
    ).first()

    if consentimento_existente:
        raise ValueError(
            "Já existe um consentimento ativo para esta finalidade."
        )

    consentimento = Consentimento(
        usuario_id=usuario_id,
        finalidade=finalidade,
        autorizado=True,
        data_consentimento=datetime.now()
    )

    db.add(consentimento)
    db.commit()
    db.refresh(consentimento)

    return consentimento


def listar_consentimentos(
    db: Session,
    usuario_id: int
):
    return db.query(Consentimento).filter(
        Consentimento.usuario_id == usuario_id
    ).order_by(Consentimento.data_consentimento.desc()).all()


def revogar_consentimento(
    db: Session,
    consentimento_id: int,
    usuario_id: int
):
    consentimento = db.query(Consentimento).filter(
        Consentimento.id == consentimento_id,
        Consentimento.usuario_id == usuario_id,
        Consentimento.autorizado == True
    ).first()

    if not consentimento:
        raise ValueError(
            "Consentimento ativo não encontrado."
        )

    consentimento.autorizado = False
    consentimento.data_revogacao = datetime.now()

    db.commit()
    db.refresh(consentimento)

    return consentimento
