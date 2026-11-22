
from pwdlib import PasswordHash


# Configura o algoritmo Argon2
password_hash = PasswordHash.recommended()


def gerar_hash_senha(senha: str) -> str:
    """Gera um hash seguro para a senha."""
    return password_hash.hash(senha)


def verificar_senha(senha: str, senha_hash: str) -> bool:
    """Verifica se a senha corresponde ao hash armazenado."""
    return password_hash.verify(senha, senha_hash)
