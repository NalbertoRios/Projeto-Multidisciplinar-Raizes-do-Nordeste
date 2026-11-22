
from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    String,
    Boolean,
    DateTime
)

from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.database import Base


class Consentimento(Base):
    __tablename__ = "consentimentos"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=False
    )

    finalidade: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    autorizado: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    data_consentimento: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False
    )

    data_revogacao: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )
