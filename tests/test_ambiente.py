from sqlalchemy import inspect


def test_banco_de_testes_criado(db):
    inspetor = inspect(db.bind)

    tabelas = inspetor.get_table_names()

    assert "usuarios" in tabelas
    assert "produtos" in tabelas
    assert "pedidos" in tabelas
    assert "pagamentos" in tabelas
    assert "consentimentos" in tabelas
    assert "pontos_fidelidade" in tabelas