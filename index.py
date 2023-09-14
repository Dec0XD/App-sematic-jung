from flask import Flask, request, jsonify, send_file, send_from_directory
import pandas as pd
import pickle

app = Flask(__name__)

# Lê o arquivo CSV de palavras com vírgula como separador
with open("words.csv", "r") as file:
    words_list = file.readline().strip().split(',')

# Criando um dicionário onde as palavras são as chaves e as posições são os valores
words_dict = {word: position for position, word in enumerate(words_list)}

# Lê o arquivo CSV de vetores
vectors_df = pd.read_csv("vetores.csv")

@app.route("/")
def home():
    return send_file("static/index.html")

@app.route("/assets/<path:path>")
def send_static(path):
    return send_from_directory("static/assets", path)

@app.route("/model/<string:word>")
def get_word(word):
    try:
        # Verificando se a palavra está no DataFrame
        row = words_df.loc[words_df['word'] == word]
        
        if not row.empty:
            # Se a palavra for encontrada, ele retorna a posição e o vetor correspondente
            position = row.iloc[0]['position']
            vector = row.iloc[0]['vector']

            # Criando uma lista do vetor
            vector = pickle.loads(vector)
            
            return jsonify(list(vector))
        else:
            # A palavra não foi encontrada
            return ""
    except Exception as e:
        print(e)
        return jsonify("Erro")

@app.route("/model2/<string:word_1>/<string:word_2>")
def get_word_pair(word_1, word_2):
    try:
        # Obtém a posição das palavras no arquivo words.csv
        position_1 = words_dict.get(word_1)
        position_2 = words_dict.get(word_2)
        
        if position_1 is None or position_2 is None:
            return jsonify("")
        
        # Obtém os vetores correspondentes as palavras sonda e input 
        vector_1 = vectors_df.iloc[position_1]['vector']
        vector_2 = vectors_df.iloc[position_2]['vector']
        
        if pd.isna(vector_1) or pd.isna(vector_2):
            return jsonify("")
        
        result = {
            "vec_1": list(pickle.loads(vector_1)),
            "vec_2": list(pickle.loads(vector_2)),
        }
        return jsonify(result)
    except Exception as e:
        print(e)
        return jsonify("")



@app.route("/save_test/", methods=["POST"])
def save_test():
    try:
        json_data = request.get_json()
        id = json_data["id"]
        data = json_data["data"]
        tempo = json_data["tempo"]
        palavra_sonda = json_data["palavra_sonda"]
        palavra_respondida = json_data["palavra_respondida"]
        similaridade = json_data["similaridade"]
        msg = "200"
    except:
        msg = "500"

    return jsonify(msg)

@app.errorhandler(404)
def not_found(error):
    return "Page not found", 404

@app.errorhandler(500)
def error_handler(error):
    return str(error), 500

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store"
    return response

if __name__ == "__main__":
    app.run(debug=True)
