import csv
import json

# Função para ler um vetor de um arquivo CSV
def read_vector(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        csv_reader = csv.reader(file, delimiter=",")
        vector = next(csv_reader)  # Lê a próxima linha do CSV
    return vector

# Função para escrever dados em um arquivo JSON
def write_json(file_name, data):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=6, ensure_ascii=False)  # Escreve os dados em formato JSON

# Função para escrever dados em um arquivo
def write_file(file_name, data):
    with open(file_name, "w", encoding="utf-8") as file:
        file.writelines([l + ",\n" for l in data])  # Escreve as linhas de dados no arquivo

# Lê os vetores de palavras e frequências de arquivos CSV
words = read_vector("words.csv")
freq = read_vector("freq.csv")

# Convertendo as frequências para uma lista de inteiros
freq = list(map(int, freq))

# Imprime o valor máximo de frequência (para verificar)
print(max(freq))

# words_freq = dict(zip(words, freq))
# write_json("wordsFreq.json", words_freq)
# write_json("words.js", words)
# write_json("freq.js", freq)
