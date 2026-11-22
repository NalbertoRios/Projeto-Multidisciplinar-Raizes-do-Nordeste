
from app.infrastructure.database.database import SessionLocal
from app.domain.models.usuario import Usuario
from app.core.security import gerar_hash_senha


db = SessionLocal()

try:
    email = "atendente.teste@raizes.com"

    existente = db.query(Usuario).filter(
        Usuario.email == email
    ).first()

    if existente:
        print("Usuário de teste já cadastrado.")
    else:
        atendente = Usuario(
            nome="Atendente Teste",
            email=email,
            senha_hash=gerar_hash_senha("Atendente@123"),
            perfil="ATENDENTE",
            ativo=True
        )

        db.add(atendente)
        db.commit()
        db.refresh(atendente)

        print("Atendente criado com sucesso!")
        print("ID:", atendente.id)
        print("Perfil:", atendente.perfil)

finally:
    db.close()
