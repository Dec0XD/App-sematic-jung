import sqlite3
import mysql.connector
import pickle
import numpy as np

# Conectar ao banco de dados SQLite
sqlite_conn = sqlite3.connect("data.db")
sqlite_cursor = sqlite_conn.cursor()

# Conectar ao banco de dados MySQL
mysql_config = {
    'user': 'root',
    'password': 'admim',
    'host': 'localhost',
    'database': 'Semantic_data',
}
mysql_conn = mysql.connector.connect(**mysql_config)
mysql_cursor = mysql_conn.cursor()

# Transferir dados da tabela "embedding" de SQLite para MySQL
sqlite_cursor.execute("SELECT * FROM embedding")
rows = sqlite_cursor.fetchall()

for row in rows:
    word = row[0]
    vector = pickle.loads(row[1])

    # Converter o vetor numpy.ndarray em uma representação de string (por exemplo, JSON)
    vector_str = json.dumps(vector.tolist())  # Converter o vetor em lista e depois em JSON

    # Inserir a palavra e o vetor (representação de string) na tabela MySQL
    mysql_cursor.execute("INSERT INTO embedding (word, vector) VALUES (%s, %s)", (word, vector_str))

# Commit as alterações no MySQL e fechar conexões
mysql_conn.commit()
mysql_cursor.close()
mysql_conn.close()
sqlite_cursor.close()
sqlite_conn.close()
