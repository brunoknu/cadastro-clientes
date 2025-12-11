from typing import List, Dict, Any, Tuple
from .repository import inserir_cliente
from .validators import validar_email, validar_cpf, validar_data


def processar_lote_clientes(payload: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Função de serviço para processar um lote de clientes.
    Não é rota HTTP. Fica engatilhada para uso futuro em API ou importação.
    Retorna (criadas, falhas).
    """
    criadas: List[Dict[str, Any]] = []
    falhas: List[Dict[str, Any]] = []

    if not isinstance(payload, list):
        raise ValueError("Payload de lote deve ser uma lista de clientes.")

    for indice, cliente in enumerate(payload):
        nome = (cliente.get("nome") or "").strip()
        email = (cliente.get("email") or "").strip()
        telefone = (cliente.get("telefone") or "").strip()
        cpf = (cliente.get("cpf") or "").strip()
        data_nascimento = (cliente.get("data_nascimento") or "").strip()

        erros = []

        if not nome:
            erros.append("nome obrigatório")
        if not validar_email(email):
            erros.append("email inválido")
        if not validar_cpf(cpf):
            erros.append("cpf inválido (11 dígitos)")
        if not validar_data(data_nascimento):
            erros.append("data inválida (dd/mm/aaaa)")

        if erros:
            falhas.append({
                "indice": indice,
                "cliente": cliente,
                "erros": erros,
            })
            continue

        inserir_cliente(nome, email, telefone, cpf, data_nascimento)
        criadas.append(cliente)

    return criadas, falhas
