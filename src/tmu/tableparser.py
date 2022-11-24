import pandas as pd
import psycopg2
import pandas.io.sql as sqlio
from nltk.tokenize import word_tokenize
import json
import pickle


def loadcsv(filename="input.csv", delimiter=";"):
    if filename is None or not filename.endswith(".csv"):
        raise NotImplementedError

    return pd.read_csv(filename, delimiter=delimiter)


def loadfromdb(tablename, host="localhost", user="postgres", pwd="postgres", dbname="postgres", port="5432"):
    # table = loadfromdb("ingredients", host="inrightplace.com", user="parser", pwd="maxim23.error", dbname="recipes")
    conn = psycopg2.connect("host='{}' port={} dbname='{}' user={} password={}".format(host, port, dbname, user, pwd))
    sql = "select * from " + tablename + ";"
    table = sqlio.read_sql_query(sql, conn)
    conn.close()
    return table


def savecsv(table, filename="output.csv", delimiter=";"):
    with open(filename, 'w', encoding="utf8") as csv_file:
        table.to_csv(path_or_buf=csv_file, sep=delimiter, encoding="utf8")


def loadparser(filename):
    j = json.loads(filename)
    return Tableparser(**j)


class Token:
    def __init__(self, string, tag=None):
        self.string = string
        self.tag = tag


class Tableparser:
    def __init__(self):
        self.table = None
        self.dict = set()
        self.paragraphs = []

    def loadtable(self, table, column):
        self.table = table
        for row in table[column]:
            tokens = []
            for elem in word_tokenize(row):
                tokens.append(Token(string=elem))
                self.dict.add(elem)
            self.paragraphs.append(tokens)

    def save(self, filename):
        with open(filename, 'w', encoding="utf8") as f:
            pickle.dump(self, f)
            f.close()

    def printdict(self):
        for row in sorted(list(self.dict)):
            print(row)

    def tolowercase(self):
        for paragraph in self.paragraphs:
            for elem in paragraph:
                elem.string = elem.string.lower()
        self.dict = set(map(lambda x: x.lower(), self.dict))