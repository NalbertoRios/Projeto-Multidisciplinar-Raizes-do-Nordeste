from pydantic import BaseModel, ConfigDict, Field


class UnidadeCriacao(BaseModel):
    nome: str = Field(min_length=3, max_length=100)
    cidade: str = Field(min_length=2, max_length=100)
    regiao: str = Field(min_length=2, max_length=100)


class UnidadeAtualizacao(BaseModel):
    nome: str | None = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    cidade: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    regiao: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    ativa: bool | None = None


class UnidadeResposta(BaseModel):
    id: int
    nome: str
    cidade: str
    regiao: str
    ativa: bool

    model_config = ConfigDict(from_attributes=True)