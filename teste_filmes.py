from conexao import conectar

from filmes import cadastrar_filme

from filmes import cadastrar_filme, listar_filmes, buscar_filme_por_id

from filmes import (
    cadastrar_filme,
    listar_filmes,
    buscar_filme_por_id,
    buscar_filme_por_titulo
)

from filmes import atualizar_filme

from filmes import excluir_filme


print("INICIANDO TESTE")

conn = conectar()

if conn:
    print("CONEXÃO REALIZADA!")

    cursor = conn.cursor()
    cursor.execute("SELECT DATABASE()")

    print("Banco:", cursor.fetchone()[0])

    cursor.execute("SHOW TABLES")

    for tabela in cursor.fetchall():
        print(tabela[0])

    cursor.close()
    conn.close()
else:
    print("FALHA NA CONEXÃO")

    from filmes import cadastrar_filme

cadastrar_filme(
    "Interestelar",
    "Ficção científica",
    169,
    "10 anos"
)

print("\nTESTANDO CADASTRO DE FILME")

cadastrar_filme(
    "Interestelar",
    "Ficção científica",
    169,
    "10 anos"
)

from filmes import listar_filmes

print("\n===== LISTANDO FILMES =====")

filmes = listar_filmes()

for filme in filmes:
    print(filme)

print("\n===== BUSCANDO FILME PELO ID =====")

filme = buscar_filme_por_id(1)

print(filme)

print("\n===== BUSCANDO FILME PELO TÍTULO =====")

resultados = buscar_filme_por_titulo("Interestelar")

for filme in resultados:
    print(filme)

    print("\n===== TESTANDO ATUALIZAÇÃO =====")

atualizar_filme(
    1,
    "Interestelar - Edição Atualizada",
    "Ficção científica",
    169,
    "12 anos"
)

print("\n===== CONFERINDO FILME ATUALIZADO =====")


print(buscar_filme_por_id(1))

print("\n===== TESTANDO EXCLUSÃO =====")

excluir_filme(1)
