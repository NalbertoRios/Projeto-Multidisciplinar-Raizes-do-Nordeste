from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    ForeignKey,
    DateTime,
    Numeric,
    Integer,
    String,
    Enum,
    UniqueConstraint,
    CheckConstraint
)

from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.database import Base

from app.domain.enums.status_pagamento import StatusPagamento


class Pagamento(Base):

    __tablename__ = "pagamentos"

    __table_args__ = (
        UniqueConstraint(
            "pedido_id",
            "numero_tentativa",
            name="uq_pagamento_pedido_tentativa"
        ),
        CheckConstraint(
            "valor > 0",
            name="ck_pagamento_valor_positivo"
        ),
        CheckConstraint(
            "numero_tentativa > 0",
            name="ck_pagamento_tentativa_positiva"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    pedido_id: Mapped[int] = mapped_column(
        ForeignKey("pedidos.id"),
        nullable=False
    )

    status_pagamento: Mapped[StatusPagamento] = mapped_column(
        Enum(StatusPagamento, name="status_pagamento"),
        default=StatusPagamento.PENDENTE,
        nullable=False
    )

    valor: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    data_pagamento: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False
    )

    numero_tentativa: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    referencia_transacao: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )