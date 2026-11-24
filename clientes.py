from mysql.connector import Error, errorcode
from conexao import conectar
from validacoes import (
    validar_cpf, validar_email, validar_telefone,
    formatar_cpf, formatar_telefone,
    ler_inteiro, ler_texto_nao_vazio
)

# ==================== 1. CREATE (CADASTRAR) ====================
def cadastrar_cliente(nome, cpf, email, telefone):
    conn = None
    cursor = None
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "INSERT INTO clientes (nome, cpf, email, telefone) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (nome, cpf, email, telefone))
        conn.commit()
        print(f"Cliente '{nome}' cadastrado com sucesso! ID: {cursor.lastrowid}")
    except Error as e:
        if e.errno == errorcode.ER_DUP_ENTRY:
            print("Erro: CPF ou E-mail já cadastrado no sistema.")
        else:
            print(f"Erro ao cadastrar: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

# ==================== 2. READ (CONSULTAR TODOS) ====================
def listar_clientes():
    conn = None
    cursor = None
    lista_clientes = []
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "SELECT id_cliente, nome, cpf, email, telefone FROM clientes ORDER BY nome"
        cursor.execute(sql)
        
        for linha in cursor.fetchall():
            cliente_dict = {
                "id": linha[0],
                "nome": linha[1],
                "cpf": linha[2],
                "email": linha[3],
                "telefone": linha[4]
            }
            lista_clientes.append(cliente_dict)
    except Error as e:
        print(f"Erro ao listar clientes: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
    return lista_clientes

# ==================== CONSULTAS SQL RELACIONADAS ====================
def buscar_por_cpf(cpf):
    conn = None
    cursor = None
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "SELECT id_cliente, nome, cpf, email, telefone FROM clientes WHERE cpf = %s"
        cursor.execute(sql, (cpf,))
        linha = cursor.fetchone()
        if linha:
            return {"id": linha[0], "nome": linha[1], "cpf": linha[2], "email": linha[3], "telefone": linha[4]}
        return None
    except Error as e:
        print(f"Erro na busca por CPF: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def buscar_por_nome(termo):
    conn = None
    cursor = None
    resultados = []
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "SELECT id_cliente, nome, cpf, email, telefone FROM clientes WHERE nome LIKE %s ORDER BY nome"
        cursor.execute(sql, (f"%{termo}%",))
        for linha in cursor.fetchall():
            resultados.append({
                "id": linha[0],
                "nome": linha[1],
                "cpf": linha[2],
                "email": linha[3],
                "telefone": linha[4]
            })
    except Error as e:
        print(f"Erro na busca por nome: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
    return resultados

def consultar_ingressos_do_cliente(id_cliente):
    """Consulta relacional (INNER JOIN) cruzando Clientes, Ingressos e Filmes."""
    conn = None
    cursor = None
    historico = []
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
            SELECT c.nome, f.titulo, i.assento, i.valor, i.data_sessao
            FROM clientes c
            INNER JOIN ingressos i ON c.id_cliente = i.id_cliente
            INNER JOIN filmes f ON i.id_filme = f.id_filme
            WHERE c.id_cliente = %s
            ORDER BY i.data_sessao DESC
        """
        cursor.execute(sql, (id_cliente,))
        for linha in cursor.fetchall():
            historico.append({
                "cliente": linha[0],
                "filme": linha[1],
                "assento": linha[2],
                "valor": float(linha[3]),
                "data_sessao": linha[4]
            })
    except Error as e:
        print(f"Erro ao consultar ingressos do cliente: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
    return historico

def relatorio_gastos_clientes():
    """Consulta analítica (LEFT JOIN + GROUP BY + SUM + COUNT) por cliente."""
    conn = None
    cursor = None
    relatorio = []
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """
            SELECT c.id_cliente, c.nome,
                   COUNT(i.id_ingresso) AS total_ingressos,
                   COALESCE(SUM(i.valor), 0.00) AS valor_total
            FROM clientes c
            LEFT JOIN ingressos i ON c.id_cliente = i.id_cliente
            GROUP BY c.id_cliente, c.nome
            ORDER BY valor_total DESC
        """
        cursor.execute(sql)
        for linha in cursor.fetchall():
            relatorio.append({
                "id": linha[0],
                "nome": linha[1],
                "total_ingressos": linha[2],
                "valor_total": float(linha[3])
            })
    except Error as e:
        print(f"Erro ao gerar relatório: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
    return relatorio

# ==================== 3. UPDATE (ATUALIZAR) ====================
def atualizar_cliente(id_cliente, novo_nome, novo_email, novo_telefone):
    conn = None
    cursor = None
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "UPDATE clientes SET nome = %s, email = %s, telefone = %s WHERE id_cliente = %s"
        cursor.execute(sql, (novo_nome, novo_email, novo_telefone, id_cliente))
        conn.commit()
        if cursor.rowcount > 0:
            print("Cliente atualizado com sucesso!")
        else:
            print("Nenhum cliente encontrado com esse ID.")
    except Error as e:
        if e.errno == errorcode.ER_DUP_ENTRY:
            print("Erro: Esse e-mail já está em uso por outro cliente.")
        else:
            print(f"Erro ao atualizar: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

# ==================== 4. DELETE (EXCLUIR) ====================
def excluir_cliente(id_cliente):
    conn = None
    cursor = None
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "DELETE FROM clientes WHERE id_cliente = %s"
        cursor.execute(sql, (id_cliente,))
        conn.commit()
        if cursor.rowcount > 0:
            print("Cliente excluído com sucesso!")
        else:
            print("Nenhum cliente encontrado com esse ID.")
    except Error as e:
        if e.errno == errorcode.ER_ROW_IS_REFERENCED_2:
            print("Bloqueado: Este cliente possui ingressos comprados e não pode ser apagado.")
        else:
            print(f"Erro ao excluir: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

# ==================== MENU INTERATIVO ====================
def menu_clientes():
    while True:
        print("\n=== GERENCIAR CLIENTES ===")
        print("1. Cadastrar Cliente")
        print("2. Listar Todos os Clientes")
        print("3. Buscar Cliente por CPF")
        print("4. Buscar Cliente por Nome")
        print("5. Ver Ingressos Comprados por Cliente (JOIN)")
        print("6. Relatório de Gastos por Cliente")
        print("7. Atualizar Cliente")
        print("8. Excluir Cliente")
        print("0. Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome = ler_texto_nao_vazio("Nome completo: ")
            while True:
                ok, cpf = validar_cpf(input("CPF: "))
                if ok: break
                print(cpf)
            while True:
                ok, email = validar_email(input("E-mail: "))
                if ok: break
                print(email)
            while True:
                ok, tel = validar_telefone(input("Telefone (com DDD): "))
                if ok: break
                print(tel)
            cadastrar_cliente(nome, cpf, email, tel)

        elif opcao == "2":
            clientes = listar_clientes()
            if not clientes:
                print("Nenhum cliente cadastrado.")
            for c in clientes:
                print(
                    f"ID: {c['id']} | Nome: {c['nome']} | CPF: {formatar_cpf(c['cpf'])} | "
                    f"E-mail: {c['email']} | Tel: {formatar_telefone(c['telefone'])}"
                )

        elif opcao == "3":
            ok, cpf = validar_cpf(input("Digite o CPF para busca: "))
            if not ok:
                print(cpf)
            else:
                cli = buscar_por_cpf(cpf)
                if cli:
                    print(
                        f"Encontrado -> ID: {cli['id']} | Nome: {cli['nome']} | "
                        f"E-mail: {cli['email']} | Tel: {formatar_telefone(cli['telefone'])}"
                    )
                else:
                    print("Cliente não encontrado.")

        elif opcao == "4":
            termo = ler_texto_nao_vazio("Digite parte do nome: ")
            resultados = buscar_por_nome(termo)
            if not resultados:
                print("Nenhum cliente encontrado.")
            for c in resultados:
                print(f"ID: {c['id']} | Nome: {c['nome']} | CPF: {formatar_cpf(c['cpf'])}")

        elif opcao == "5":
            id_cli = ler_inteiro("Digite o ID do cliente: ")
            ingressos = consultar_ingressos_do_cliente(id_cli)
            if not ingressos:
                print("Este cliente ainda não comprou ingressos.")
            for ing in ingressos:
                print(f"Filme: {ing['filme']} | Assento: {ing['assento']} | Valor: R$ {ing['valor']:.2f} | Data: {ing['data_sessao']}")

        elif opcao == "6":
            relatorio = relatorio_gastos_clientes()
            for r in relatorio:
                print(f"ID: {r['id']} | Cliente: {r['nome']} | Ingressos: {r['total_ingressos']} | Total: R$ {r['valor_total']:.2f}")

        elif opcao == "7":
            id_cli = ler_inteiro("ID do cliente para atualizar: ")
            nome = ler_texto_nao_vazio("Novo nome: ")
            while True:
                ok, email = validar_email(input("Novo e-mail: "))
                if ok: break
                print(email)
            while True:
                ok, tel = validar_telefone(input("Novo telefone: "))
                if ok: break
                print(tel)
            atualizar_cliente(id_cli, nome, email, tel)

        elif opcao == "8":
            id_cli = ler_inteiro("ID do cliente para excluir: ")
            excluir_cliente(id_cli)

        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu_clientes()