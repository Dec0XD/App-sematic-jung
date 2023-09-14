import sqlite3
import csv
import pickle  # Usaremos o módulo pickle para desserializar os dados BLOB

# Conectar-se ao banco de dados (substitua 'seu_banco_de_dados.db' pelo nome do seu banco de dados SQLite)
conexao = sqlite3.connect('data.db')

# Criar um objeto cursor para executar consultas SQL
cursor = conexao.cursor()

# Executar uma consulta SQL para recuperar os vetores (substitua 'sua_tabela' e 'vetor_coluna' pelos nomes apropriados)
consulta = "SELECT vector FROM embedding"

# Execute a consulta SQL
cursor.execute(consulta)

# Processar os resultados
resultados = cursor.fetchall()

# Nome do arquivo CSV de saída
nome_arquivo_csv = "vetores.csv"

# Abrir o arquivo CSV para escrita
with open(nome_arquivo_csv, 'w', newline='') as arquivo_csv:
    # Crie um objeto escritor CSV
    escritor_csv = csv.writer(arquivo_csv)

    # Escreva os cabeçalhos (se necessário)
    # escritor_csv.writerow(["nome_da_coluna1", "nome_da_coluna2", ...])

    # Escreva os vetores no arquivo CSV
    for resultado in resultados:
        vetor_blob = resultado[0]  # Supondo que a coluna do vetor seja a primeira coluna na sua tabela
        # Desserialize o BLOB para obter o vetor em seu formato original
        vetor = pickle.loads(vetor_blob)
        escritor_csv.writerow(vetor)  # Escreve o vetor em uma linha

# Feche o cursor e a conexão com o banco de dados
cursor.close()
conexao.close()

print(f'Os vetores foram salvos em {nome_arquivo_csv}.')
