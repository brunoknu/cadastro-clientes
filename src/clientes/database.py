import sqlite3

# Nome do arquivo de banco de dados.
# Ele deve estar na raiz do projeto (mesmo nível de src/).
DB_NAME = "clientes.db"


def criar_conexao():
    """
    Cria e retorna uma conexão com o banco SQLite.
    """
    conn = sqlite3.connect(DB_NAME)
    # Permite acessar colunas pelo nome (row["nome"])
    conn.row_factory = sqlite3.Row
    return conn


def criar_tabela():
    """
    Cria a tabela 'clientes' caso ainda não exista.
    """
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT,
            telefone TEXT,
            cpf TEXT,
            data_nascimento TEXT
        )
        """
    )
    conn.commit()
    conn.close()
