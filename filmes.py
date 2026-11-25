
from mysql.connector import Error
from conexao import conectar


# CREATE - Cadastrar filme
def cadastrar_filme(titulo, genero, duracao_min, classificacao):
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