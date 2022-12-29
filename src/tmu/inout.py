import pandas as pd
import psycopg2
import pandas.io.sql as sqlio
import pickle


def loadfromdb(tablename, host="localhost", user="postgres", pwd="postgres", dbname="postgres", port="5432"):
    # table = loadfromdb("ingredients", host="inrightplace.com", user="parser", pwd="maxim23.error", dbname="recipes")
    conn = psycopg2.connect("host='{}' port={} dbname='{}' user={} password={}".format(host, port, dbname, user, pwd))
    sql = "select * from " + tablename + ";"
    table = sqlio.read_sql_query(sql, conn)
    conn.close()
    return table


def loadcsv(filename="input.csv", delimiter=";"):
    if filename is None or not filename.endswith(".csv"):
        raise NotImplementedError
    return pd.read_csv(filename, delimiter=delimiter)


def savecsv(table, filename="output.csv", delimiter=";"):
    with open(filename, 'w', encoding="utf8") as csv_file:
        table.to_csv(path_or_buf=csv_file, sep=delimiter, encoding="utf8")


def loadbinary(filename="test.parser"):
    with open(filename, 'rb') as read_file:
        return pickle.load(read_file)


def savebinary(obj, filename="test.parser"):
    with open(filename, 'wb') as file_object:
        pickle.dump(obj, file_object)
