from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SaldoFidelidadeResponse(BaseModel):
    saldo_pontos: int


class HistoricoFidelidadeResponse(BaseModel):
    id: int
    cliente_id: int
    pedido_id: int
    pagamento_id: int
    pontos: int
    data_credito: datetime

    model_config = ConfigDict(from_attributes=True)