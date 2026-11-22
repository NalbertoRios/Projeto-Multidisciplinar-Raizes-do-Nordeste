from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    Integer,
    DateTime,
    CheckConstraint,
    UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.database import Base


class PontoFidelidade(Base):

    __tablename__ = "pontos_fidelidade"

    __table_args__ = (
        UniqueConstraint(
            "pedido_id",
            name="uq_pontos_pedido"
        ),
        UniqueConstraint(
            "pagamento_id",
            name="uq_pontos_pagamento"
        ),
        CheckConstraint(
            "pontos > 0",
            name="ck_pontos_positivos"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=False
    )

    pedido_id: Mapped[int] = mapped_column(
        ForeignKey("pedidos.id"),
        nullable=False
    )

    pagamento_id: Mapped[int] = mapped_column(
        ForeignKey("pagamentos.id"),
        nullable=False
    )

    pontos: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    data_credito: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False
    )