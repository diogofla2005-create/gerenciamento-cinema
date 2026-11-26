from ingressos import atualizar_ingresso
from ingressos import listar_ingressos

print("TESTE 1 - Atualizar para assento ocupado")
atualizar_ingresso(
    3, 1, 1, "A10", 30.00, "2026-12-10 19:30:00"
)

print("-" * 40)

print("TESTE 2 - Cliente inexistente")
atualizar_ingresso(
    3, 999, 1, "A11", 30.00, "2026-12-10 19:30:00"
)

print("-" * 40)

print("TESTE 3 - Filme inexistente")
atualizar_ingresso(
    3, 1, 999, "A11", 30.00, "2026-12-10 19:30:00"
)

print("-" * 40)

print("TESTE 4 - Valor negativo")
atualizar_ingresso(
    3, 1, 1, "A11", -30.00, "2026-12-10 19:30:00"
)

print("-" * 40)

print("TESTE 5 - Atualizacao valida mantendo o assento")
atualizar_ingresso(
    3, 1, 1, "A11", 30.00, "2026-12-10 19:30:00"
)

print("-" * 40)

print("DADOS APOS A ATUALIZACAO")

for ingresso in listar_ingressos():
    print(ingresso)
