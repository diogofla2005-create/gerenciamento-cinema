from filmes import menu_filmes
from clientes import menu_clientes
from ingressos import menu_ingressos


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