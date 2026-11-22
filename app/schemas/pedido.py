from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.domain.enums.canal_pedido import CanalPedido
from app.domain.enums.status_pedido import StatusPedido


class ItemPedidoCriacao(BaseModel):
    produto_unidade_id: int = Field(gt=0)
    quantidade: int = Field(gt=0)


class PedidoCriacao(BaseModel):
    unidade_id: int = Field(gt=0)
    cliente_id: int | None = Field(default=None, gt=0)
    canal_pedido: CanalPedido
    itens: list[ItemPedidoCriacao] = Field(min_length=1)


class ItemPedidoResposta(BaseModel):
    id: int
    produto_unidade_id: int
    quantidade: int
    preco_unitario: Decimal

    model_config = {"from_attributes": True}


class PedidoResposta(BaseModel):
    id: int
    cliente_id: int
    atendente_id: int | None
    unidade_id: int
    canal_pedido: CanalPedido
    status: StatusPedido
    valor_total: Decimal
    data_criacao: datetime
    itens: list[ItemPedidoResposta]

    model_config = {"from_attributes": True}