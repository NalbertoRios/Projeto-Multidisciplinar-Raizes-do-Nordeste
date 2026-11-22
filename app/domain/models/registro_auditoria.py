
from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    String,
    Integer,
    DateTime
)

from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.database import Base


class RegistroAuditoria(Base):
    __tablename__ = "registros_auditoria"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    usuario_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=True
    )

    acao: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    entidade: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    entidade_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    data_hora: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False
    )
