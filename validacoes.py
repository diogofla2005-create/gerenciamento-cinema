import re

def limpar_numeros(texto):
    """Remove pontos, traços e parênteses, deixando apenas números."""
    return re.sub(r'\D', '', texto)

def validar_cpf(cpf_str):
    """Valida os 11 dígitos e os dois dígitos verificadores do CPF."""
    cpf = limpar_numeros(cpf_str)

    if len(cpf) != 11:
        return False, "O CPF deve ter exatamente 11 dígitos."

    if cpf == cpf[0] * 11:
        return False, "CPF inválido (números repetidos)."

    # Cálculo do 1º dígito verificador
    soma_1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto_1 = (soma_1 * 10) % 11
    digito_1 = 0 if resto_1 == 10 else resto_1
    if digito_1 != int(cpf[9]):
        return False, "CPF inválido (1º dígito verificador incorreto)."

    # Cálculo do 2º dígito verificador
    soma_2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto_2 = (soma_2 * 10) % 11
    digito_2 = 0 if resto_2 == 10 else resto_2
    if digito_2 != int(cpf[10]):
        return False, "CPF inválido (2º dígito verificador incorreto)."

    return True, cpf

def validar_email(email_str):
    """Valida se o texto segue o formato nome@dominio.com."""
    email = email_str.strip().lower()
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(padrao, email):
        return True, email
    return False, "E-mail inválido! Use o formato exemplo@dominio.com"

def validar_telefone(telefone_str):
    """Valida telefone com DDD (10 dígitos fixo ou 11 dígitos celular)."""
    tel = limpar_numeros(telefone_str)
    if len(tel) not in (10, 11):
        return False, "Telefone inválido! Digite DDD + número (10 ou 11 dígitos)."
    if len(tel) == 11 and tel[2] != '9':
        return False, "Celular com 11 dígitos deve começar com 9 após o DDD."
    return True, tel

def formatar_cpf(cpf):
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

def formatar_telefone(tel):
    if len(tel) == 11:
        return f"({tel[:2]}) {tel[2:7]}-{tel[7:]}"
    return f"({tel[:2]}) {tel[2:6]}-{tel[6:]}"

def ler_inteiro(mensagem):
    """Evita que o programa quebre se o usuário digitar letras em vez de números."""
    while True:
        try:
            return int(input(mensagem).strip())
        except ValueError:
            print("Digite apenas números inteiros!")

def ler_texto_nao_vazio(mensagem):
    """Impede campos obrigatórios em branco."""
    while True:
        texto = input(mensagem).strip()
        if texto:
            return texto
        print("Este campo não pode ficar vazio!")