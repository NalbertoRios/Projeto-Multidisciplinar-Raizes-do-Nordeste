from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProdutoUnidadeCriacao(BaseModel):
    unidade_id: int = Field(gt=0)
    produto_id: int = Field(gt=0)

    preco_especifico: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=10,
        decimal_places=2
    )

    data_inicio_disponibilidade: date | None = None
    data_fim_disponibilidade: date | None = None

    observacao_variacao: str | None = Field(
        default=None,
        max_length=255
    )


class ProdutoUnidadeAtualizacao(BaseModel):
    preco_especifico: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=10,
        decimal_places=2
    )

    habilitado: bool | None = None

    data_inicio_disponibilidade: date | None = None
    data_fim_disponibilidade: date | None = None

    observacao_variacao: str | None = Field(
        default=None,
        max_length=255
    )


class ProdutoUnidadeResposta(BaseModel):
    id: int
    unidade_id: int
    produto_id: int
    preco_especifico: Decimal | None
    habilitado: bool
    data_inicio_disponibilidade: date | None
    data_fim_disponibilidade: date | None
    observacao_variacao: str | None

    model_config = ConfigDict(from_attributes=True)