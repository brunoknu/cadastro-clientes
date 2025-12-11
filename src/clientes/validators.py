import re
from datetime import datetime


def validar_email(email: str) -> bool:
    """
    Valida o formato básico de um email.
    Email é opcional: se vier vazio, retorna True.
    """
    if not email:
        return True

    padrao = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(padrao, email) is not None


def validar_cpf(cpf: str) -> bool:
    """
    Valida se o CPF tem 11 dígitos numéricos.
    Não faz validação de dígitos verificadores (é uma validação simples).
    CPF é opcional: se vier vazio, retorna True.
    """
    if not cpf:
        return True

    cpf_limpo = re.sub(r"\D", "", cpf)
    return len(cpf_limpo) == 11


def validar_data(data_str: str) -> bool:
    """
    Valida se a data está no formato dd/mm/aaaa.
    Campo é opcional: se vier vazio, retorna True.
    """
    if not data_str:
        return True

    try:
        datetime.strptime(data_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False
