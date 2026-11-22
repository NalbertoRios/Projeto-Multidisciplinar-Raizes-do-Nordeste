
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.infrastructure.database.database import SessionLocal
from app.domain.models.usuario import Usuario
from app.core.token import verificar_token


oauth2_scheme = HTTPBearer()

def get_db():
    """Fornece uma sessão do banco de dados."""

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_usuario_atual(
    credenciais: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Identifica o usuário por meio do token JWT."""

    credenciais_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado.",
        headers={"WWW-Authenticate": "Bearer"}
    )
    token = credenciais.credentials
    dados_token = verificar_token(token)

    if dados_token is None:
        raise credenciais_invalidas

    usuario_id = dados_token.get("sub")

    if usuario_id is None:
        raise credenciais_invalidas

    try:
        usuario_id = int(usuario_id)
    except (ValueError, TypeError):
        raise credenciais_invalidas

    usuario = db.get(Usuario, usuario_id)

    if usuario is None or not usuario.ativo:
        raise credenciais_invalidas

    return usuario


def exigir_perfil(*perfis_permitidos: str):
    """
    Verifica se o usuário autenticado possui
    um dos perfis autorizados.
    """

    def verificar_permissao(
        usuario: Usuario = Depends(get_usuario_atual)
    ):
        if usuario.perfil not in perfis_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não possui permissão para realizar esta operação."
            )

        return usuario

    return verificar_permissao

