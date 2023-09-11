import csv
import json

def read_vector(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        csv_reader = csv.reader(file, delimiter=",")
        vector = next(csv_reader)
    return vector

def write_json(file_name, data):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=6, ensure_ascii=False)

def write_file(file_name, data):
    with open(file_name, "w", encoding="utf-8") as file:
        file.writelines([l + ",\n" for l in data])

words = read_vector("words.csv")
freq = read_vector("freq.csv")
freq = list(map(int, freq))
print(max(freq))
# words_freq = dict(zip(words, freq))
# write_json("wordsFreq.json", words_freq)
# write_json("words.js", words)
# write_json("freq.js", freq)
