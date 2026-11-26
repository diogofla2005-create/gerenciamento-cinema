from filmes import (
    cadastrar_filme,
    listar_filmes,
    buscar_filme_por_id,
    buscar_filme_por_titulo,
    atualizar_filme,
    excluir_filme
)

from clientes import menu_clientes

from ingressos import menu_ingressos


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
            titulo = input("Título: ")
            genero = input("Gênero: ")
            duracao = int(input("Duração em minutos: "))
            classificacao = input("Classificação: ")

            cadastrar_filme(titulo, genero, duracao, classificacao)

        elif opcao == "2":
            filmes = listar_filmes()

            if not filmes:
                print("Nenhum filme cadastrado.")

            for filme in filmes:
                print(filme)

        elif opcao == "3":
            id_filme = int(input("ID do filme: "))
            print(buscar_filme_por_id(id_filme))

        elif opcao == "4":
            titulo = input("Digite o título: ")
            resultados = buscar_filme_por_titulo(titulo)

            for filme in resultados:
                print(filme)

            if not resultados:
                print("Nenhum filme encontrado.")

        elif opcao == "5":
            id_filme = int(input("ID do filme: "))
            titulo = input("Novo título: ")
            genero = input("Novo gênero: ")
            duracao = int(input("Nova duração: "))
            classificacao = input("Nova classificação: ")

            atualizar_filme(
                id_filme,
                titulo,
                genero,
                duracao,
                classificacao
            )

        elif opcao == "6":
            id_filme = int(input("ID do filme para excluir: "))
            excluir_filme(id_filme)

        elif opcao == "0":
            break

        else:
            print("Opção inválida!")


# MENU PRINCIPAL
def menu_principal():
    while True:
        print("\n================================")
        print("   SISTEMA DE GERENCIAMENTO")
        print("          DE CINEMA")
        print("================================")
        print("1. Gerenciar filmes")
        print("2. Gerenciar clientes")
        print("3. Gerenciar ingressos")
        print("0. Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            menu_filmes()

        elif opcao == "2":
            menu_clientes()

        elif opcao == "3":
            menu_ingressos()

        elif opcao == "0":
            print("Encerrando o sistema...")
            break

        else:
            print("Opção inválida!")


if __name__ == "__main__":
    menu_principal()