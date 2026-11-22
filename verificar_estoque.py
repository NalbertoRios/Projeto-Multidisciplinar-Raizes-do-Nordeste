
import sqlite3

conexao = sqlite3.connect("raizes.db")
cursor = conexao.cursor()

cursor.execute("""
    SELECT
        id,
        produto_unidade_id,
        quantidade_disponivel
    FROM estoques
""")

resultados = cursor.fetchall()

print("Registros de estoque encontrados:")

for registro in resultados:
    print(registro)

conexao.close()
