import sqlite3

conn = sqlite3.connect("raizes.db")
cursor = conn.cursor()

tabelas = ["usuarios", "unidades", "produtos"]

for tabela in tabelas:
    print(f"\nEstrutura da tabela: {tabela}")

    cursor.execute(f"PRAGMA table_info({tabela})")

    for coluna in cursor.fetchall():
        print(coluna)

conn.close()