from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.domain.enums.status_pagamento import StatusPagamento


class PagamentoSimulacao(BaseModel):
    aprovado: bool


class PagamentoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    pedido_id: int
    status_pagamento: StatusPagamento
    valor: Decimal
    data_pagamento: datetime
    numero_tentativa: int
    referencia_transacao: str | None