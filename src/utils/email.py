import sqlite3
import re
from datetime import datetime

# ==============================
# CONFIGURAÇÃO DO BANCO
# ==============================

DB_NAME = "clientes.db"

def criar_conexao():
    conn = sqlite3.connect(DB_NAME)
    return conn

def criar_tabela():
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT,
            telefone TEXT,
            cpf TEXT,
            data_nascimento TEXT
        )
    """)
    conn.commit()
    conn.close()

# ==============================
# FUNÇÕES DE VALIDAÇÃO
# ==============================

def validar_email(email: str) -> bool:
    if not email:
        return True  # email opcional
    padrao = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(padrao, email) is not None

def validar_cpf(cpf: str) -> bool:
    if not cpf:
        return True  # cpf opcional
    cpf_limpo = re.sub(r"\D", "", cpf)
    return len(cpf_limpo) == 11

def validar_data(data_str: str) -> bool:
    if not data_str:
        return True  # data opcional
    try:
        datetime.strptime(data_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False

# ==============================
# OPERAÇÕES DE BANCO (CRUD)
# ==============================

def inserir_cliente(nome, email, telefone, cpf, data_nascimento):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clientes (nome, email, telefone, cpf, data_nascimento)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, email, telefone, cpf, data_nascimento))
    conn.commit()
    conn.close()

def listar_clientes():
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email, telefone, cpf, data_nascimento FROM clientes")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def buscar_cliente_por_id(id_cliente):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nome, email, telefone, cpf, data_nascimento
        FROM clientes
        WHERE id = ?
    """, (id_cliente,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def buscar_clientes_por_nome(nome_parcial):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nome, email, telefone, cpf, data_nascimento
        FROM clientes
        WHERE nome LIKE ?
    """, (f"%{nome_parcial}%",))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def atualizar_cliente(id_cliente, nome, email, telefone, cpf, data_nascimento):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE clientes
        SET nome = ?, email = ?, telefone = ?, cpf = ?, data_nascimento = ?
        WHERE id = ?
    """, (nome, email, telefone, cpf, data_nascimento, id_cliente))
    conn.commit()
    conn.close()

def excluir_cliente(id_cliente):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))
    conn.commit()
    conn.close()

# ==============================
# INTERFACE DE LINHA DE COMANDO
# ==============================

def exibir_menu():
    print("\n========== CADASTRO DE CLIENTES ==========")
    print("1 - Cadastrar novo cliente")
    print("2 - Listar todos os clientes")
    print("3 - Buscar cliente por ID")
    print("4 - Buscar clientes por nome")
    print("5 - Atualizar cliente")
    print("6 - Excluir cliente")
    print("0 - Sair")
    print("==========================================")

def input_cliente(dados_existentes=None):
    """
    Se 'dados_existentes' for passado, permite ENTER para manter valor antigo.
    dados_existentes: tupla (id, nome, email, telefone, cpf, data_nascimento)
    """
    if dados_existentes:
        _, nome_ant, email_ant, tel_ant, cpf_ant, data_ant = dados_existentes
        print("Pressione ENTER para manter o valor atual.")
    else:
        nome_ant = email_ant = tel_ant = cpf_ant = data_ant = ""

    while True:
        nome = input(f"Nome [{nome_ant}]: ").strip()
        if not nome and not dados_existentes:
            print("Nome é obrigatório.")
            continue
        if not nome:
            nome = nome_ant
        break

    while True:
        email = input(f"Email [{email_ant}]: ").strip()
        if not email:
            email = email_ant
        if not validar_email(email):
            print("Email inválido. Tente novamente.")
            continue
        break

    telefone = input(f"Telefone [{tel_ant}]: ").strip()
    if not telefone:
        telefone = tel_ant

    while True:
        cpf = input(f"CPF [{cpf_ant}] (somente números ou com máscara): ").strip()
        if not cpf:
            cpf = cpf_ant
        if not validar_cpf(cpf):
            print("CPF inválido (precisa ter 11 dígitos).")
            continue
        break

    while True:
        data_nascimento = input(
            f"Data de nascimento [{data_ant}] (dd/mm/aaaa, opcional): "
        ).strip()
        if not data_nascimento:
            data_nascimento = data_ant
        if not validar_data(data_nascimento):
            print("Data inválida. Use o formato dd/mm/aaaa.")
            continue
        break

    return nome, email, telefone, cpf, data_nascimento

def opcao_cadastrar():
    print("\n--- Cadastrar novo cliente ---")
    nome, email, telefone, cpf, data_nascimento = input_cliente()
    inserir_cliente(nome, email, telefone, cpf, data_nascimento)
    print("Cliente cadastrado com sucesso!")

def opcao_listar():
    print("\n--- Lista de clientes ---")
    clientes = listar_clientes()
    if not clientes:
        print("Nenhum cliente cadastrado.")
        return
    for c in clientes:
        print(f"ID: {c[0]} | Nome: {c[1]} | Email: {c[2]} | Telefone: {c[3]} | CPF: {c[4]} | Nasc.: {c[5]}")

def opcao_buscar_por_id():
    print("\n--- Buscar cliente por ID ---")
    try:
        id_cliente = int(input("Informe o ID do cliente: "))
    except ValueError:
        print("ID inválido.")
        return

    cliente = buscar_cliente_por_id(id_cliente)
    if cliente:
        print(f"ID: {cliente[0]}")
        print(f"Nome: {cliente[1]}")
        print(f"Email: {cliente[2]}")
        print(f"Telefone: {cliente[3]}")
        print(f"CPF: {cliente[4]}")
        print(f"Data de Nascimento: {cliente[5]}")
    else:
        print("Cliente não encontrado.")

def opcao_buscar_por_nome():
    print("\n--- Buscar clientes por nome ---")
    nome_parcial = input("Digite parte do nome: ").strip()
    resultados = buscar_clientes_por_nome(nome_parcial)
    if not resultados:
        print("Nenhum cliente encontrado.")
        return
    for c in resultados:
        print(f"ID: {c[0]} | Nome: {c[1]} | Email: {c[2]} | Telefone: {c[3]} | CPF: {c[4]} | Nasc.: {c[5]}")

def opcao_atualizar():
    print("\n--- Atualizar cliente ---")
    try:
        id_cliente = int(input("Informe o ID do cliente a atualizar: "))
    except ValueError:
        print("ID inválido.")
        return

    cliente = buscar_cliente_por_id(id_cliente)
    if not cliente:
        print("Cliente não encontrado.")
        return

    print("Dados atuais do cliente:")
    print(f"ID: {cliente[0]} | Nome: {cliente[1]} | Email: {cliente[2]} | Telefone: {cliente[3]} | CPF: {cliente[4]} | Nasc.: {cliente[5]}")

    print("\nInforme os novos dados (ou ENTER para manter):")
    nome, email, telefone, cpf, data_nascimento = input_cliente(dados_existentes=cliente)

    atualizar_cliente(id_cliente, nome, email, telefone, cpf, data_nascimento)
    print("Cliente atualizado com sucesso!")

def opcao_excluir():
    print("\n--- Excluir cliente ---")
    try:
        id_cliente = int(input("Informe o ID do cliente a excluir: "))
    except ValueError:
        print("ID inválido.")
        return

    cliente = buscar_cliente_por_id(id_cliente)
    if not cliente:
        print("Cliente não encontrado.")
        return

    print(f"Você está prestes a excluir o cliente: {cliente[1]} (ID: {cliente[0]})")
    confirma = input("Tem certeza? (s/n): ").strip().lower()
    if confirma == "s":
        excluir_cliente(id_cliente)
        print("Cliente excluído com sucesso!")
    else:
        print("Operação cancelada.")

# ==============================
# FUNÇÃO PRINCIPAL
# ==============================

def main():
    criar_tabela()
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            opcao_cadastrar()
        elif opcao == "2":
            opcao_listar()
        elif opcao == "3":
            opcao_buscar_por_id()
        elif opcao == "4":
            opcao_buscar_por_nome()
        elif opcao == "5":
            opcao_atualizar()
        elif opcao == "6":
            opcao_excluir()
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
