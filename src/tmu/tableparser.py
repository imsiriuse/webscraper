import pandas.io.sql as sqlio
import psycopg2
import pandas as pd


class Tableparser:
    def __init__(self):
        self.table = pd.DataFrame()

    def loadcsv(self, filename, delimiter=";"):
        self.table = pd.read_csv(filename, delimiter=delimiter)

    def loadfromdb(self, tablename, host="localhost", user="postgres", pwd="postgres", dbname="postgres", port="5432"):
        conn = psycopg2.connect("host='{}' port={} dbname='{}' user={} password={}".format(host, port, dbname, user, pwd))
        sql = "select * from " + tablename + ";"
        self.table = sqlio.read_sql_query(sql, conn)
        conn.close()
