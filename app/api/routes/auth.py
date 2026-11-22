
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import (get_db, get_usuario_atual)
from app.domain.models.usuario import Usuario
from app.schemas.usuario import (
    UsuarioCriacao,
    UsuarioLogin,
    UsuarioResposta
)
from app.core.security import gerar_hash_senha, verificar_senha
from app.core.token import criar_token_acesso


router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)


@router.post(
    "/cadastro",
    response_model=UsuarioResposta,
    status_code=status.HTTP_201_CREATED
)
def cadastrar_usuario(
    dados: UsuarioCriacao,
    db: Session = Depends(get_db)
):
    email_existente = db.query(Usuario).filter(
        Usuario.email == dados.email
    ).first()

    if email_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este email já está cadastrado."
        )

    usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=gerar_hash_senha(dados.senha),
        perfil="CLIENTE"
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    return usuario


@router.post("/login")
def realizar_login(
    dados: UsuarioLogin,
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(
        Usuario.email == dados.email
    ).first()

    if not usuario or not verificar_senha(
        dados.senha,
        usuario.senha_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos."
        )

    if not usuario.ativo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo."
        )

    token = criar_token_acesso({
        "sub": str(usuario.id),
        "perfil": usuario.perfil
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UsuarioResposta)
def obter_usuario_logado(
    usuario: Usuario = Depends(get_usuario_atual)
):
    return usuario