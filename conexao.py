import mysql.connector
from mysql.connector import Error

def conectar():
    """Abre e retorna a conexão com o banco de dados MySQL."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",             # Usuário padrão do MySQL
            password="Petrus1309@",    # <-- COLOQUE AQUI A SENHA DO SEU MYSQL
            database="gerenciamento_cinema"
        )
        return conn
    except Error as e:
        print(f"[Erro de Conexão MySQL] Verifique se o MySQL está rodando: {e}")
        return None