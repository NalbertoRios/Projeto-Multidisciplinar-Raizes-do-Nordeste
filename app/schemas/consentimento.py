from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ConsentimentoCriacao(BaseModel):
    finalidade: str = Field(
        min_length=3,
        max_length=100,
        description="Finalidade do consentimento"
    )


class ConsentimentoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    usuario_id: int
    finalidade: str
    autorizado: bool
    data_consentimento: datetime
    data_revogacao: datetime | None