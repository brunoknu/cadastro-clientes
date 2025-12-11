from .database import criar_conexao


def inserir_cliente(nome, email, telefone, cpf, data_nascimento):
    """
    Insere um novo cliente na tabela.
    """
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO clientes (nome, email, telefone, cpf, data_nascimento)
        VALUES (?, ?, ?, ?, ?)
        """,
        (nome, email, telefone, cpf, data_nascimento),
    )
    conn.commit()
    conn.close()


def listar_clientes():
    """
    Retorna a lista de todos os clientes.
    """
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nome, email, telefone, cpf, data_nascimento FROM clientes"
    )
    resultados = cursor.fetchall()
    conn.close()
    return resultados


def buscar_cliente_por_id(id_cliente: int):
    """
    Busca um cliente específico pelo ID.
    """
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, nome, email, telefone, cpf, data_nascimento
        FROM clientes
        WHERE id = ?
        """,
        (id_cliente,),
    )
    resultado = cursor.fetchone()
    conn.close()
    return resultado


def buscar_clientes_por_nome(nome_parcial: str):
    """
    Busca clientes cujo nome contenha o texto informado.
    """
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, nome, email, telefone, cpf, data_nascimento
        FROM clientes
        WHERE nome LIKE ?
        """,
        (f"%{nome_parcial}%",),
    )
    resultados = cursor.fetchall()
    conn.close()
    return resultados


def atualizar_cliente(id_cliente, nome, email, telefone, cpf, data_nascimento):
    """
    Atualiza os dados de um cliente existente.
    """
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE clientes
        SET nome = ?, email = ?, telefone = ?, cpf = ?, data_nascimento = ?
        WHERE id = ?
        """,
        (nome, email, telefone, cpf, data_nascimento, id_cliente),
    )
    conn.commit()
    conn.close()


def excluir_cliente(id_cliente: int):
    """
    Exclui um cliente pelo ID.
    """
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))
    conn.commit()
    conn.close()
