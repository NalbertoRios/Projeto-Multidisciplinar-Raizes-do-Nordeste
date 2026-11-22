
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UsuarioCriacao(BaseModel):
    nome: str = Field(min_length=3, max_length=100)
    email: EmailStr
    senha: str = Field(min_length=8, max_length=128)
    perfil: str = "CLIENTE"


class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str


class UsuarioResposta(BaseModel):
    id: int
    nome: str
    email: EmailStr
    perfil: str
    ativo: bool

    model_config = ConfigDict(from_attributes=True)
