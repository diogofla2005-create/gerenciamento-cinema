from filmes import validar_dados_filme


print("\n===== TESTES DE VALIDAÇÃO DE FILMES =====")

print("\nTESTE 1 - Dados válidos")
print(validar_dados_filme("Interestelar", "Ficção científica", 169, "12"))

print("\nTESTE 2 - Título vazio")
print(validar_dados_filme("", "Ação", 120, "14"))

print("\nTESTE 3 - Gênero vazio")
print(validar_dados_filme("Batman", "", 120, "14"))

print("\nTESTE 4 - Duração negativa")
print(validar_dados_filme("Batman", "Ação", -120, "14"))

print("\nTESTE 5 - Duração igual a zero")
print(validar_dados_filme("Batman", "Ação", 0, "14"))

print("\nTESTE 6 - Duração em texto")
print(validar_dados_filme("Batman", "Ação", "abc", "14"))

print("\nTESTE 7 - Classificação inválida")
print(validar_dados_filme("Batman", "Ação", 120, "25"))

print("\nTESTE 8 - Classificação livre minúscula")
print(validar_dados_filme("Toy Story", "Animação", 81, "l"))

from filmes import (
    cadastrar_filme,
    atualizar_filme,
    excluir_filme,
    buscar_filme_por_id,
    buscar_filme_por_titulo
)


print("\n===== TESTES DE VALIDAÇÃO DO CRUD =====")

print("\nTESTE 9 - Cadastro com título vazio")
cadastrar_filme("", "Ação", 120, "14")

print("\nTESTE 10 - Cadastro com duração inválida")
cadastrar_filme("Batman", "Ação", -120, "14")

print("\nTESTE 11 - Atualização com ID inválido")
atualizar_filme(-1, "Batman", "Ação", 120, "14")

print("\nTESTE 12 - Atualização com classificação inválida")
atualizar_filme(1, "Batman", "Ação", 120, "25")

print("\nTESTE 13 - Exclusão com ID inválido")
excluir_filme(0)

print("\nTESTE 14 - Busca por ID inválido")
print(buscar_filme_por_id(-1))

print("\nTESTE 15 - Busca por título vazio")
print(buscar_filme_por_titulo(""))