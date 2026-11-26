
from mysql.connector import Error
from conexao import conectar
from validacoes import ler_inteiro, ler_texto_nao_vazio

# Validar dados do filme
def validar_dados_filme(titulo, genero, duracao_min, classificacao):

    if not isinstance(titulo, str) or not titulo.strip():
        return False, "O título não pode estar vazio."

    if len(titulo.strip()) > 150:
        return False, "O título deve ter até 150 caracteres."

    if not isinstance(genero, str) or not genero.strip():
        return False, "O gênero não pode estar vazio."

    if len(genero.strip()) > 50:
        return False, "O gênero deve ter até 50 caracteres."

    if type(duracao_min) is not int or duracao_min <= 0:
        return False, "A duração deve ser um número inteiro positivo."

    if not isinstance(classificacao, str):
        return False, "Classificação inválida."

    classificacoes_validas = ("L", "10", "12", "14", "16", "18")

    if classificacao.strip().upper() not in classificacoes_validas:
        return False, "Classificação inválida. Utilize L, 10, 12, 14, 16 ou 18."

    return True, "Dados válidos."

# CREATE - Cadastrar filme
def cadastrar_filme(titulo, genero, duracao_min, classificacao):
    valido, mensagem = validar_dados_filme(
        titulo, genero, duracao_min, classificacao
    )

    if not valido:
        print(mensagem)
        return

    titulo = titulo.strip()
    genero = genero.strip()
    classificacao = classificacao.strip().upper()

    conn = None
    cursor = None

    try:
        conn = conectar()

        if conn is None:
            print("Não foi possível conectar ao banco.")
            return

        cursor = conn.cursor()

        sql = """
            INSERT INTO filmes
            (titulo, genero, duracao_min, classificacao)
            VALUES (%s, %s, %s, %s)
        """

        valores = (titulo, genero, duracao_min, classificacao)

        cursor.execute(sql, valores)
        conn.commit()

        print("Filme cadastrado com sucesso!")
        print(f"ID do filme: {cursor.lastrowid}")

    except Error as e:
        print(f"Erro ao cadastrar filme: {e}")

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()


# READ - Listar filmes
def listar_filmes():
    conn = None
    cursor = None
    filmes = []

    try:
        conn = conectar()

        if conn is None:
            return filmes

        cursor = conn.cursor()

        sql = """
            SELECT id_filme, titulo, genero,
                   duracao_min, classificacao
            FROM filmes
            ORDER BY titulo
        """

        cursor.execute(sql)

        for linha in cursor.fetchall():
            filme = {
                "id": linha[0],
                "titulo": linha[1],
                "genero": linha[2],
                "duracao": linha[3],
                "classificacao": linha[4]
            }

            filmes.append(filme)

    except Error as e:
        print(f"Erro ao listar filmes: {e}")

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()

    return filmes


# READ - Buscar filme pelo ID
def buscar_filme_por_id(id_filme):
    if type(id_filme) is not int or id_filme <= 0:
        print("O ID do filme deve ser um número inteiro positivo.")
        return None

    conn = None
    cursor = None

    try:
        conn = conectar()

        if conn is None:
            return None

        cursor = conn.cursor()

        sql = """
            SELECT id_filme, titulo, genero,
                   duracao_min, classificacao
            FROM filmes
            WHERE id_filme = %s
        """

        cursor.execute(sql, (id_filme,))
        linha = cursor.fetchone()

        if linha:
            return {
                "id": linha[0],
                "titulo": linha[1],
                "genero": linha[2],
                "duracao": linha[3],
                "classificacao": linha[4]
            }

        return None

    except Error as e:
        print(f"Erro ao buscar filme: {e}")
        return None

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()


# READ - Buscar filme pelo título
def buscar_filme_por_titulo(titulo):
    if not isinstance(titulo, str) or not titulo.strip():
        print("O título da busca não pode estar vazio.")
        return []

    titulo = titulo.strip()

    conn = None
    cursor = None
    filmes = []

    try:
        conn = conectar()

        if conn is None:
            return filmes

        cursor = conn.cursor()

        sql = """
            SELECT id_filme, titulo, genero,
                   duracao_min, classificacao
            FROM filmes
            WHERE titulo LIKE %s
            ORDER BY titulo
        """

        cursor.execute(sql, (f"%{titulo}%",))

        for linha in cursor.fetchall():
            filme = {
                "id": linha[0],
                "titulo": linha[1],
                "genero": linha[2],
                "duracao": linha[3],
                "classificacao": linha[4]
            }

            filmes.append(filme)

    except Error as e:
        print(f"Erro ao buscar filme por título: {e}")

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()

    return filmes


# UPDATE - Atualizar filme
def atualizar_filme(id_filme, titulo, genero, duracao_min, classificacao):
    if type(id_filme) is not int or id_filme <= 0:
        print("O ID do filme deve ser um número inteiro positivo.")
        return

    valido, mensagem = validar_dados_filme(
        titulo, genero, duracao_min, classificacao
    )

    if not valido:
        print(mensagem)
        return

    titulo = titulo.strip()
    genero = genero.strip()
    classificacao = classificacao.strip().upper()

    conn = None
    cursor = None

    try:
        conn = conectar()

        if conn is None:
            return

        cursor = conn.cursor()

        sql = """
            UPDATE filmes
            SET titulo = %s,
                genero = %s,
                duracao_min = %s,
                classificacao = %s
            WHERE id_filme = %s
        """

        valores = (titulo, genero, duracao_min, classificacao, id_filme)

        cursor.execute(sql, valores)
        conn.commit()

        if cursor.rowcount > 0:
            print("Filme atualizado com sucesso!")
        else:
            print("Filme não encontrado.")

    except Error as e:
        print(f"Erro ao atualizar filme: {e}")

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()


# DELETE - Excluir filme
def excluir_filme(id_filme):
    if type(id_filme) is not int or id_filme <= 0:
        print("O ID do filme deve ser um número inteiro positivo.")
        return

    conn = None
    cursor = None

    try:
        conn = conectar()

        if conn is None:
            return

        cursor = conn.cursor()

        sql = """
            DELETE FROM filmes
            WHERE id_filme = %s
        """

        cursor.execute(sql, (id_filme,))
        conn.commit()

        if cursor.rowcount > 0:
            print("Filme excluído com sucesso!")
        else:
            print("Filme não encontrado.")

    except Error as e:
        print(f"Erro ao excluir filme: {e}")

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()


# Exibir dados de um filme
def exibir_filme(filme):
    print("-" * 45)
    print(f"ID: {filme['id']}")
    print(f"Título: {filme['titulo']}")
    print(f"Gênero: {filme['genero']}")
    print(f"Duração: {filme['duracao']} minutos")
    print(f"Classificação: {filme['classificacao']}")
    print("-" * 45)    


    # MENU DE FILMES
def menu_filmes():
    while True:
        print("\n===== GERENCIAR FILMES =====")
        print("1. Cadastrar filme")
        print("2. Listar filmes")
        print("3. Buscar filme por ID")
        print("4. Buscar filme por título")
        print("5. Atualizar filme")
        print("6. Excluir filme")
        print("0. Voltar ao menu principal")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            titulo = ler_texto_nao_vazio("Título: ")
            genero = ler_texto_nao_vazio("Gênero: ")
            duracao = ler_inteiro("Duração em minutos: ")
            classificacao = ler_texto_nao_vazio(
                "Classificação (L, 10, 12, 14, 16 ou 18): "
            )

            cadastrar_filme(
                titulo,
                genero,
                duracao,
                classificacao
            )
        elif opcao == "2":
            filmes = listar_filmes()

            if not filmes:
                print("Nenhum filme cadastrado.")
            else:
                print("\n===== FILMES CADASTRADOS =====")

                for filme in filmes:
                    exibir_filme(filme)

                print(f"Total de filmes: {len(filmes)}")

        elif opcao == "3":
            id_filme = ler_inteiro("ID do filme: ")

            if id_filme <= 0:
                print("O ID deve ser um número positivo.")
                continue

            filme = buscar_filme_por_id(id_filme)

            if filme:
                print("\n===== FILME ENCONTRADO =====")
                exibir_filme(filme)
            else:
                print("Filme não encontrado.")

        elif opcao == "4":
            titulo = ler_texto_nao_vazio(
                "Digite o título do filme: "
            )

            resultados = buscar_filme_por_titulo(titulo)

            if not resultados:
                print("Nenhum filme encontrado.")
            else:
                print("\n===== RESULTADOS DA BUSCA =====")

                for filme in resultados:
                    exibir_filme(filme)

                print(f"Total encontrado: {len(resultados)}")

        elif opcao == "5":
            id_filme = ler_inteiro("ID do filme para atualizar: ")

            if id_filme <= 0:
                print("O ID deve ser um número positivo.")
                continue

            filme = buscar_filme_por_id(id_filme)

            if not filme:
                print("Filme não encontrado.")
                continue

            print("\n===== DADOS ATUAIS DO FILME =====")
            exibir_filme(filme)

            print("\n===== INFORME OS NOVOS DADOS =====")

            titulo = ler_texto_nao_vazio("Novo título: ")
            genero = ler_texto_nao_vazio("Novo gênero: ")
            duracao = ler_inteiro("Nova duração em minutos: ")
            classificacao = ler_texto_nao_vazio(
                "Nova classificação (L, 10, 12, 14, 16 ou 18): "
            )

            atualizar_filme(
                id_filme,
                titulo,
                genero,
                duracao,
                classificacao
            )

        elif opcao == "6":
            id_filme = ler_inteiro("ID do filme para excluir: ")

            if id_filme <= 0:
                print("O ID deve ser um número positivo.")
                continue

            filme = buscar_filme_por_id(id_filme)

            if not filme:
                print("Filme não encontrado.")
                continue

            print("\n===== FILME SELECIONADO =====")
            exibir_filme(filme)

            confirmacao = input(
                "Deseja realmente excluir este filme? (S/N): "
            ).strip().upper()

            if confirmacao == "S":
                excluir_filme(id_filme)
            else:
                print("Exclusão cancelada.")

        elif opcao == "0":
            break

        else:
            print("Opção inválida!")