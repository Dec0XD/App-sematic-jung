import mysql.connector

# Configurar informações de conexão com o banco de dados MySQL
mysql_config = {
    'user': 'root',
    'password': 'admim',
    'host': 'localhost',
    'database': 'Semantic_data',
}

# Conectar ao banco de dados MySQL
mysql_conn = mysql.connector.connect(**mysql_config)
mysql_cursor = mysql_conn.cursor()

# Executar uma consulta para verificar os dados
mysql_cursor.execute("SELECT * FROM embedding LIMIT 10")  # Exemplo: Seleciona os primeiros 10 registros da tabela "embedding"
rows = mysql_cursor.fetchall()

for row in rows:
    print(row)

# Fechar o cursor e a conexão
mysql_cursor.close()
mysql_conn.close()
