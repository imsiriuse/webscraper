import re
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


def loadparser(filename="test.parser"):
    with open(filename, 'rb') as read_file:
        return pickle.load(read_file)


class Token:
    def __init__(self, string, tag=None):
        self.string = string
        self.tag = tag

    def __str__(self):
        return self.string

    def __hash__(self):
        return hash(self.string)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.string == other.string

    def __lt__(self, other):
        return self.string < other.string

    def __gt__(self, other):
        return self.string > other.string


class Tableparser:
    def __init__(self, table):
        self.source = table

        self.dict = {}
        self.paragraphs = []
        for row in table:
            token = Token(string=row)
            self.paragraphs.append([token])
            if token in self.dict:
                self.dict[token] = self.dict[row] + 1
            else:
                self.dict[token] = 1

    def save(self, filename="test.parser"):
        with open(filename, 'wb') as file_object:
            pickle.dump(self, file_object)

    def tokenize(self, regex="\s+"):
        for token in self.dict:
            splits = re.split(regex, token.string)
            if len(splits) == 1:
                continue
            for split in splits:
                if split in self.dict:
                    self.dict[split] = self.dict[split] + 1
                else:
                    self.dict[split] = 1
            del self.dict[token]

    def printdict(self):
        for row in sorted(list(self.dict)):
            print(str(self.dict[row]) + ": " + row)

    #def tolowercase(self):
    #    self.dict = set(map(lambda x: str.lower(x.string), self.dict))

    # def grep(self, regex):
    #     for paragraph in self.paragraphs:
    #        for token in paragraph:
    #            if re.match(regex, token.string):
    #                print(paragraph)


parser = Tableparser(loadcsv()["content"])