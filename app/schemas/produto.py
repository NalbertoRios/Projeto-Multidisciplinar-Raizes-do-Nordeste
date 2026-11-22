from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProdutoCriacao(BaseModel):
    nome: str = Field(min_length=3, max_length=100)
    descricao: str | None = Field(default=None, max_length=1000)
    preco_padrao: Decimal = Field(
        gt=0,
        max_digits=10,
        decimal_places=2
    )


class ProdutoAtualizacao(BaseModel):
    nome: str | None = Field(default=None, min_length=3, max_length=100)
    descricao: str | None = Field(default=None, max_length=1000)
    preco_padrao: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=10,
        decimal_places=2
    )
    ativo: bool | None = None


class ProdutoResposta(BaseModel):
    id: int
    nome: str
    descricao: str | None
    preco_padrao: Decimal
    ativo: bool

    model_config = ConfigDict(from_attributes=True)
    