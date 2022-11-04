import nltk
import pandas.io.sql as sqlio
import psycopg2
import pandas as pd
from nltk.tokenize import word_tokenize


def loadcsv(filename, delimiter=";"):
    return pd.read_csv(filename, delimiter=delimiter)


def loadfromdb(tablename, host="localhost", user="postgres", pwd="postgres", dbname="postgres", port="5432"):
    conn = psycopg2.connect("host='{}' port={} dbname='{}' user={} password={}".format(host, port, dbname, user, pwd))
    sql = "select * from " + tablename + ";"
    table = sqlio.read_sql_query(sql, conn)
    conn.close()
    return table


def tokenize(table, column):
    nltk.download('punct')
    for row in table[column]:
        row = word_tokenize(row.str)


def uniq(table):
    pool = set()
    for row in table:
        for elem in row:
            pool.add(elem)
    return list(pool)


def loadingredients():
    return loadfromdb(
        tablename="ingredients",
        host="46.36.41.120",
        user="parser",
        dbname="recipes",
        pwd="maxim23.error"
    )
