from getpass import getpass

from app.infrastructure.database.database import SessionLocal
from app.domain.models.usuario import Usuario
from app.core.security import gerar_hash_senha


db = SessionLocal()

try:
    email = "gerente.mvp@example.com"

    existente = db.query(Usuario).filter(
        Usuario.email == email
    ).first()

    if existente:
        print("Este usuário já está cadastrado.")
    else:
        senha = getpass("Digite a senha do gerente: ")

        if len(senha) < 8:
            print("A senha deve ter pelo menos 8 caracteres.")
        else:
            gerente = Usuario(
                nome="Gerente Teste",
                email=email,
                senha_hash=gerar_hash_senha(senha),
                perfil="GERENTE",
                ativo=True
            )

            db.add(gerente)
            db.commit()

            print("Usuário GERENTE criado com sucesso!")

finally:
    db.close()