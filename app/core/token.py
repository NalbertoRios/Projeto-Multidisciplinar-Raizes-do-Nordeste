
from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import settings


def criar_token_acesso(dados: dict) -> str:
    """Gera um token JWT com prazo de validade."""

    dados_token = dados.copy()

    expiracao = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    dados_token.update({"exp": expiracao})

    token = jwt.encode(
        dados_token,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return token


def verificar_token(token: str) -> dict | None:
    """Valida o token e retorna seus dados."""

    try:
        dados = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        return dados

    except jwt.InvalidTokenError:
        return None
