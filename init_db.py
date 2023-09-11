import sqlite3
import pickle
import numpy as np

from numpy import array

def create_word2vec_table():
    con = sqlite3.connect("data.db")
    con.execute("PRAGMA journal_mode=WAL")
    cur = con.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS embedding (word TEXT PRIMARY KEY, vector BLOB)"""
    )
    cur.execute(
        """CREATE TABLE IF NOT EXISTS tests (id INTEGER NOT NULL,
                                            date DATETIME NOT NULL,
                                            time TIME NOT NULL, 
                                            palavra_sonda TEXT NOT NULL,
                                            palavra_respondida TEXT,
                                            similaridade FLOAT NOT NULL)"""
    )
    con.commit()
    con.close()

def upload_embedding():
    con = sqlite3.connect("data.db")
    con.execute("PRAGMA journal_mode=WAL")
    cur = con.cursor()
    con.execute("DELETE FROM embedding")
    with open("glove_s100.txt", "r", encoding="utf-8") as w2v_file:
        _ = w2v_file.readline()
        n = 0
        for line in w2v_file:
            words = line.rstrip().split(" ")
            word = words[0]
            vector = array([float(w) for w in words[1:]])
            cur.execute(
                """INSERT INTO embedding VALUES (?, ?)""", (word, pickle.dumps(vector))
            )
            n += 1
            if n % 100000 == 0:
                print(f"processed {n} (+1) lines")
                con.commit()
    con.commit()
    con.close()

def main():
    create_word2vec_table()
    # upload_embedding()

if __name__ == "__main__":
    main()
