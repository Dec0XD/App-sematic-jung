import sqlite3
import pickle
import numpy as np

from numpy import array

# Cria uma tabela chamada "embedding" e uma tabela "tests" no banco de dados "data.db"
def create_word2vec_table():
    con = sqlite3.connect("data.db")
    con.execute("PRAGMA journal_mode=WAL")  # Define o modo de jornal para WAL (Write-Ahead Logging)
    cur = con.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS embedding (word TEXT PRIMARY KEY, vector BLOB)"""
    )  # Cria a tabela "embedding" com colunas "word" (texto) e "vector" (BLOB)
    cur.execute(
        """CREATE TABLE IF NOT EXISTS tests (id INTEGER NOT NULL,
                                            date DATETIME NOT NULL,
                                            time TIME NOT NULL, 
                                            palavra_sonda TEXT NOT NULL,
                                            palavra_respondida TEXT,
                                            similaridade FLOAT NOT NULL)"""
    )  # Cria a tabela "tests" com colunas para armazenar informações de testes
    con.commit()  # Confirma as alterações no banco de dados
    con.close()  # Fecha a conexão com o banco de dados

# Faz upload dos vetores de palavras do arquivo "glove_s100.txt" para o banco de dados "data.db"
def upload_embedding():
    con = sqlite3.connect("data.db")
    con.execute("PRAGMA journal_mode=WAL")  # Define o modo de jornal para WAL
    cur = con.cursor()
    con.execute("DELETE FROM embedding")  # Remove os dados existentes da tabela "embedding"
    with open("glove_s100.txt", "r", encoding="utf-8") as w2v_file:
        _ = w2v_file.readline()  # Lê a primeira linha (cabeçalho) do arquivo
        n = 0
        for line in w2v_file:
            words = line.rstrip().split(" ")  # Divide a linha em palavras
            word = words[0]  # A primeira palavra é a palavra em si
            vector = array([float(w) for w in words[1:]])  # Vetor de floats após a primeira palavra
            cur.execute(
                """INSERT INTO embedding VALUES (?, ?)""", (word, pickle.dumps(vector))
            )  # Insere a palavra e seu vetor na tabela "embedding"
            n += 1
            if n % 100000 == 0:
                print(f"processed {n} (+1) lines")  # Mostra o progresso a cada 100.000 linhas
                con.commit()  # Confirma as alterações no banco de dados
    con.commit()  # Confirma as alterações finais no banco de dados
    con.close()  # Fecha a conexão com o banco de dados

def main():
    create_word2vec_table()  # Chama a função para criar a tabela no banco de dados
    # upload_embedding()  # Chama a função para fazer upload dos vetores das palavras

if __name__ == "__main__":
    main()  # Chama a função principal apenas se o arquivo for executado diretamente
    