from mysql.connector import Error
from conexao import conectar
from datetime import datetime
from decimal import Decimal, InvalidOperation
from validacoes import ler_inteiro, ler_texto_nao_vazio


# CREATE - Cadastrar ingresso
def cadastrar_ingresso(id_cliente, id_filme, assento, valor, data_sessao):

    valido, mensagem = validar_dados_ingresso(
        id_cliente, id_filme, assento, valor, data_sessao
    )

    if not valido:
        print(mensagem)
        return

    valido, mensagem = validar_cliente_filme(
        id_cliente, id_filme
    )

    if not valido:
        print(mensagem)
        return

    assento = assento.strip().upper()

    disponivel, mensagem = verificar_assento_disponivel(
        id_filme, assento, data_sessao
    )

    if not disponivel:
        print(mensagem)
        return

    conn = None
    cursor = None

    try:
        conn = conectar()

        if conn is None:
            print("Não foi possível conectar ao banco.")
            return

        cursor = conn.cursor()

        sql = """
            INSERT INTO ingressos
            (id_cliente, id_filme, assento, valor, data_sessao)
            VALUES (%s, %s, %s, %s, %s)
        """

        valores = (
            id_cliente,
            id_filme,
            assento,
            Decimal(str(valor)),
            data_sessao
        )

        cursor.execute(sql, valores)
        conn.commit()

        print("Ingresso cadastrado com sucesso!")
        print(f"ID do ingresso: {cursor.lastrowid}")

    except Error as e:
        print(f"Erro ao cadastrar ingresso: {e}")

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()


            # READ - Listar ingressos
def listar_ingressos():
    conn = None
    cursor = None
    ingressos = []

    try:
        conn = conectar()

        if conn is None:
            return ingressos

        cursor = conn.cursor()

        sql = """
            SELECT i.id_ingresso,
                   c.nome,
                   f.titulo,
                   i.assento,
                   i.valor,
                   i.data_sessao
            FROM ingressos i
            INNER JOIN clientes c
                ON i.id_cliente = c.id_cliente
            INNER JOIN filmes f
                ON i.id_filme = f.id_filme
            ORDER BY i.data_sessao
        """

        cursor.execute(sql)

        for linha in cursor.fetchall():
            ingresso = {
                "id": linha[0],
                "cliente": linha[1],
                "filme": linha[2],
                "assento": linha[3],
                "valor": linha[4],
                "data_sessao": linha[5]
            }

            ingressos.append(ingresso)

    except Error as e:
        print(f"Erro ao listar ingressos: {e}")

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()

    return ingressos


# READ - Buscar ingresso por ID
def buscar_ingresso_por_id(id_ingresso):
    conn = None
    cursor = None

    try:
        conn = conectar()

        if conn is None:
            return None

        cursor = conn.cursor()

        sql = """
            SELECT i.id_ingresso,
                   c.nome,
                   f.titulo,
                   i.assento,
                   i.valor,
                   i.data_sessao
            FROM ingressos i
            INNER JOIN clientes c
                ON i.id_cliente = c.id_cliente
            INNER JOIN filmes f
                ON i.id_filme = f.id_filme
            WHERE i.id_ingresso = %s
        """

        cursor.execute(sql, (id_ingresso,))

        linha = cursor.fetchone()

        if linha:
            return {
                "id": linha[0],
                "cliente": linha[1],
                "filme": linha[2],
                "assento": linha[3],
                "valor": linha[4],
                "data_sessao": linha[5]
            }

        return None

    except Error as e:
        print(f"Erro ao buscar ingresso: {e}")
        return None

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()

            # READ - Buscar ingressos por cliente
def buscar_ingressos_por_cliente(id_cliente):
    conn = None
    cursor = None
    ingressos = []

    try:
        conn = conectar()

        if conn is None:
            return ingressos

        cursor = conn.cursor()

        sql = """
            SELECT i.id_ingresso,
                   c.nome,
                   f.titulo,
                   i.assento,
                   i.valor,
                   i.data_sessao
            FROM ingressos i
            INNER JOIN clientes c
                ON i.id_cliente = c.id_cliente
            INNER JOIN filmes f
                ON i.id_filme = f.id_filme
            WHERE i.id_cliente = %s
            ORDER BY i.data_sessao
        """

        cursor.execute(sql, (id_cliente,))

        for linha in cursor.fetchall():
            ingresso = {
                "id": linha[0],
                "cliente": linha[1],
                "filme": linha[2],
                "assento": linha[3],
                "valor": linha[4],
                "data_sessao": linha[5]
            }

            ingressos.append(ingresso)

    except Error as e:
        print(f"Erro ao buscar ingressos por cliente: {e}")

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()

    return ingressos

    # READ - Buscar ingressos por filme
def buscar_ingressos_por_filme(id_filme):
    conn = None
    cursor = None
    ingressos = []

    try:
        conn = conectar()

        if conn is None:
            return ingressos

        cursor = conn.cursor()

        sql = """
            SELECT i.id_ingresso,
                   c.nome,
                   f.titulo,
                   i.assento,
                   i.valor,
                   i.data_sessao
            FROM ingressos i
            INNER JOIN clientes c
                ON i.id_cliente = c.id_cliente
            INNER JOIN filmes f
                ON i.id_filme = f.id_filme
            WHERE i.id_filme = %s
            ORDER BY i.data_sessao
        """

        cursor.execute(sql, (id_filme,))

        for linha in cursor.fetchall():
            ingresso = {
                "id": linha[0],
                "cliente": linha[1],
                "filme": linha[2],
                "assento": linha[3],
                "valor": linha[4],
                "data_sessao": linha[5]
            }

            ingressos.append(ingresso)

    except Error as e:
        print(f"Erro ao buscar ingressos por filme: {e}")

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()

    return ingressos

# UPDATE - Atualizar ingresso
def atualizar_ingresso(id_ingresso, id_cliente, id_filme,
                       assento, valor, data_sessao):

    if not isinstance(id_ingresso, int) or id_ingresso <= 0:
        print("ID do ingresso inválido.")
        return

    valido, mensagem = validar_dados_ingresso(
        id_cliente, id_filme, assento, valor, data_sessao
    )

    if not valido:
        print(mensagem)
        return

    valido, mensagem = validar_cliente_filme(
        id_cliente, id_filme
    )

    if not valido:
        print(mensagem)
        return

    assento = assento.strip().upper()

    disponivel, mensagem = verificar_assento_disponivel(
        id_filme, assento, data_sessao, id_ingresso
    )

    if not disponivel:
        print(mensagem)
        return

    conn = None
    cursor = None

    try:
        conn = conectar()

        if conn is None:
            print("Não foi possível conectar ao banco.")
            return

        cursor = conn.cursor()

        sql = """
            UPDATE ingressos
            SET id_cliente = %s,
                id_filme = %s,
                assento = %s,
                valor = %s,
                data_sessao = %s
            WHERE id_ingresso = %s
        """

        valores = (
            id_cliente,
            id_filme,
            assento,
            Decimal(str(valor)),
            data_sessao,
            id_ingresso
        )

        cursor.execute(sql, valores)
        conn.commit()

        if cursor.rowcount > 0:
            print("Ingresso atualizado com sucesso!")
        else:
            print("Ingresso não encontrado ou sem alterações.")

    except Error as e:
        print(f"Erro ao atualizar ingresso: {e}")

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()

            # DELETE - Excluir ingresso
def excluir_ingresso(id_ingresso):
    conn = None
    cursor = None

    try:
        conn = conectar()

        if conn is None:
            print("Não foi possível conectar ao banco.")
            return

        cursor = conn.cursor()

        sql = """
            DELETE FROM ingressos
            WHERE id_ingresso = %s
        """

        cursor.execute(sql, (id_ingresso,))
        conn.commit()

        if cursor.rowcount > 0:
            print("Ingresso excluído com sucesso!")
        else:
            print("Ingresso não encontrado.")

    except Error as e:
        print(f"Erro ao excluir ingresso: {e}")

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()  

            # Validar dados do ingresso
def validar_dados_ingresso(id_cliente, id_filme,
                           assento, valor, data_sessao):

    if not isinstance(id_cliente, int) or id_cliente <= 0:
        return False, "ID do cliente inválido."

    if not isinstance(id_filme, int) or id_filme <= 0:
        return False, "ID do filme inválido."

    if not assento.strip():
        return False, "O assento não pode ficar vazio."

    if len(assento.strip()) > 10:
        return False, "O assento deve ter até 10 caracteres."

    try:
        valor = Decimal(str(valor))

        if not valor.is_finite():
            return False, "Valor inválido."

        if valor <= 0:
            return False, "O valor deve ser maior que zero."

        if valor > Decimal("9999.99"):
            return False, "Valor acima do limite permitido."

        if valor != valor.quantize(Decimal("0.01")):
            return False, "Use até duas casas decimais."

    except (InvalidOperation, ValueError):
        return False, "Valor inválido."

    try:
        datetime.strptime(data_sessao, "%Y-%m-%d %H:%M:%S")

    except (ValueError, TypeError):
        return False, "Data inválida. Use AAAA-MM-DD HH:MM:SS."

    return True, "Dados válidos."

    # Validar existencia do cliente e do filme
def validar_cliente_filme(id_cliente, id_filme):
    conn = None
    cursor = None

    try:
        conn = conectar()

        if conn is None:
            return False, "Falha na conexão com o banco."

        cursor = conn.cursor()

        cursor.execute(
            "SELECT id_cliente FROM clientes WHERE id_cliente = %s",
            (id_cliente,)
        )

        if cursor.fetchone() is None:
            return False, "Cliente não encontrado."

        cursor.execute(
            "SELECT id_filme FROM filmes WHERE id_filme = %s",
            (id_filme,)
        )

        if cursor.fetchone() is None:
            return False, "Filme não encontrado."

        return True, "Cliente e filme encontrados."

    except Error as e:
        return False, f"Erro na validação: {e}"

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()

       # Verificar disponibilidade do assento
def verificar_assento_disponivel(id_filme, assento,
                                 data_sessao, id_ingresso=None):
    conn = None
    cursor = None

    try:
        conn = conectar()

        if conn is None:
            return False, "Falha na conexão com o banco."

        cursor = conn.cursor()

        sql = """
            SELECT id_ingresso
            FROM ingressos
            WHERE id_filme = %s
            AND assento = %s
            AND data_sessao = %s
        """

        valores = [id_filme, assento.strip().upper(), data_sessao]

        if id_ingresso is not None:
            sql += " AND id_ingresso != %s"
            valores.append(id_ingresso)

        sql += " LIMIT 1"

        cursor.execute(sql, tuple(valores))

        if cursor.fetchone() is not None:
            return False, "Assento já ocupado nesta sessão."

        return True, "Assento disponível."

    except Error as e:
        return False, f"Erro ao verificar assento: {e}"

    finally:
        if cursor:
            cursor.close()

        if conn and conn.is_connected():
            conn.close()

            # MENU - Gerenciamento de ingressos
def menu_ingressos():
    while True:
        print("\n" + "=" * 40)
        print("       MENU DE INGRESSOS")
        print("=" * 40)
        print("1 - Cadastrar ingresso")
        print("2 - Listar ingressos")
        print("3 - Buscar ingresso por ID")
        print("4 - Buscar ingressos por cliente")
        print("5 - Buscar ingressos por filme")
        print("6 - Atualizar ingresso")
        print("7 - Excluir ingresso")
        print("0 - Voltar ao menu principal")
        print("=" * 40)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "0":
            print("Voltando ao menu principal...")
            break

        elif opcao == "1":
            print("\n--- CADASTRAR INGRESSO ---")

            id_cliente = ler_inteiro("ID do cliente: ")
            id_filme = ler_inteiro("ID do filme: ")
            assento = ler_texto_nao_vazio("Assento: ").upper()
            valor = ler_texto_nao_vazio("Valor do ingresso: ")
            data_sessao = ler_texto_nao_vazio(
                "Data da sessão (AAAA-MM-DD HH:MM:SS): "
            )

            cadastrar_ingresso(
                id_cliente,
                id_filme,
                assento,
                valor,
                data_sessao
            )

        elif opcao == "2":
            print("\n--- LISTAR INGRESSOS ---")

            ingressos = listar_ingressos()

            if not ingressos:
                print("Nenhum ingresso encontrado.")
            else:
                for ingresso in ingressos:
                    print(f"ID: {ingresso['id']}")
                    print(f"Cliente: {ingresso['cliente']}")
                    print(f"Filme: {ingresso['filme']}")
                    print(f"Assento: {ingresso['assento']}")
                    print(f"Valor: R$ {ingresso['valor']:.2f}")
                    print(f"Sessão: {ingresso['data_sessao']}")
                    print("-" * 40)

        elif opcao == "3":
            print("\n--- BUSCAR INGRESSO POR ID ---")

            id_ingresso = ler_inteiro("ID do ingresso: ")

            ingresso = buscar_ingresso_por_id(id_ingresso)

            if not ingresso:
                print("Ingresso não encontrado.")
            else:
                print(f"ID: {ingresso['id']}")
                print(f"Cliente: {ingresso['cliente']}")
                print(f"Filme: {ingresso['filme']}")
                print(f"Assento: {ingresso['assento']}")
                print(f"Valor: R$ {ingresso['valor']:.2f}")
                print(f"Sessão: {ingresso['data_sessao']}")
                print("-" * 40)

        elif opcao == "4":
            print("\n--- BUSCAR INGRESSOS POR CLIENTE ---")

            id_cliente = ler_inteiro("ID do cliente: ")

            ingressos = buscar_ingressos_por_cliente(id_cliente)

            if not ingressos:
                print("Nenhum ingresso encontrado.")
            else:
                for ingresso in ingressos:
                    print(f"ID: {ingresso['id']}")
                    print(f"Cliente: {ingresso['cliente']}")
                    print(f"Filme: {ingresso['filme']}")
                    print(f"Assento: {ingresso['assento']}")
                    print(f"Valor: R$ {ingresso['valor']:.2f}")
                    print(f"Sessão: {ingresso['data_sessao']}")
                    print("-" * 40)

        elif opcao == "5":
            print("\n--- BUSCAR INGRESSOS POR FILME ---")

            id_filme = ler_inteiro("ID do filme: ")

            ingressos = buscar_ingressos_por_filme(id_filme)

            if not ingressos:
                print("Nenhum ingresso encontrado.")
            else:
                for ingresso in ingressos:
                    print(f"ID: {ingresso['id']}")
                    print(f"Cliente: {ingresso['cliente']}")
                    print(f"Filme: {ingresso['filme']}")
                    print(f"Assento: {ingresso['assento']}")
                    print(f"Valor: R$ {ingresso['valor']:.2f}")
                    print(f"Sessão: {ingresso['data_sessao']}")
                    print("-" * 40)

        elif opcao == "6":
            print("\n--- ATUALIZAR INGRESSO ---")

            id_ingresso = ler_inteiro("ID do ingresso: ")

            ingresso = buscar_ingresso_por_id(id_ingresso)

            if not ingresso:
                print("Ingresso não encontrado.")
            else:
                id_cliente = ler_inteiro("Novo ID do cliente: ")
                id_filme = ler_inteiro("Novo ID do filme: ")
                assento = ler_texto_nao_vazio("Novo assento: ").upper()
                valor = ler_texto_nao_vazio("Novo valor: ")
                data_sessao = ler_texto_nao_vazio(
                    "Nova data da sessão (AAAA-MM-DD HH:MM:SS): "
                )

                atualizar_ingresso(
                    id_ingresso,
                    id_cliente,
                    id_filme,
                    assento,
                    valor,
                    data_sessao
                )

        elif opcao == "7":
            print("\n--- EXCLUIR INGRESSO ---")

            id_ingresso = ler_inteiro("ID do ingresso: ")

            ingresso = buscar_ingresso_por_id(id_ingresso)

            if not ingresso:
                print("Ingresso não encontrado.")
            else:
                print(f"Cliente: {ingresso['cliente']}")
                print(f"Filme: {ingresso['filme']}")
                print(f"Assento: {ingresso['assento']}")
                print(f"Valor: R$ {ingresso['valor']:.2f}")
                print(f"Sessão: {ingresso['data_sessao']}")

                confirmacao = input(
                    "Confirma a exclusão? (S/N): "
                ).strip().upper()

                if confirmacao == "S":
                    excluir_ingresso(id_ingresso)
                else:
                    print("Exclusão cancelada.")

        else:
            print("Opção inválida! Tente novamente.")