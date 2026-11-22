
from pydantic import BaseModel, ConfigDict, Field


class EstoqueAtualizacao(BaseModel):
    quantidade_disponivel: int = Field(ge=0)


class EstoqueResposta(BaseModel):
    id: int
    produto_unidade_id: int
    quantidade_disponivel: int

    model_config = ConfigDict(from_attributes=True)
