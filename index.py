from flask import Flask, request, jsonify, send_file, send_from_directory
import sqlite3
import pickle

app = Flask(__name__)

@app.route("/")
def home():
    return send_file("static/index.html")

@app.route("/assets/<path:path>")
def send_static(path):
    return send_from_directory("static/assets", path)

@app.route("/model/<string:word>")
def get_word(word):
    try:
        con = sqlite3.connect("data.db")
        cur = con.cursor()
        cur.execute("SELECT vector FROM embedding WHERE word = ?", (word,))
        res = cur.fetchone()
        con.close()
        if res is None:
            return ""
        res = pickle.loads(res[0])
        return jsonify(list(res))
    except Exception as e:
        print(e)
        return jsonify("Erro")

@app.route("/model2/<string:word_1>/<string:word_2>")
def get_word_pair(word_1, word_2):
    try:
        con = sqlite3.connect("data.db")
        cur = con.cursor()
        cur.execute("SELECT vector FROM embedding WHERE word = ?", (word_1,))
        vec_1 = cur.fetchone()
        cur.execute("SELECT vector FROM embedding WHERE word = ?", (word_2,))
        vec_2 = cur.fetchone()
        con.close()
        if vec_1 is None or vec_2 is None:
            return jsonify("")
        result = {
            "vec_1": list(pickle.loads(vec_1[0])),
            "vec_2": list(pickle.loads(vec_2[0])),
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

        with sqlite3.connect("data.db") as con:
            cur = con.cursor()
            cur.execute(
                """INSERT INTO game values (?,?,?,?,?,?)""",
                (id, data, tempo, palavra_sonda, palavra_respondida, similaridade),
            )
            con.commit()
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
