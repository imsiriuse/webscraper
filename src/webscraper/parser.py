import psycopg2
from bs4 import BeautifulSoup


class Parser:
    def __init__(self, entries, name):
        self.entries = entries
        self.name = name
        self.results = []
        for entry in range(len(self.entries)):
            self.results.append([])

    def parsehtml(self, html):
        soup = BeautifulSoup(html)

        result = {}
        for entry in self.entries:
            result[entry.name] = soup.select(entry.selector)

        return result


class DbParser(Parser):
    def __init__(self, entries, name):
        super().__init__(entries, name)
        self.dbconnection = None

    def dbconnect(self, dbname, user="postgres", password="postgres", host="localhost", port="5432"):
        self.dbconnection = psycopg2.connect(
            host=host,
            database=dbname,
            user=user,
            password=password,
            port=port
        )

    def dbdisconnect(self):
        # if self.dbconnection:
        #     self.dbconnection.close()
        self.dbconnection.close()

    def inittable(self):
        cursor = self.dbconnection.cursor()
        cmd = "CREATE TABLE IF NOT EXISTS " + self.name + " ( id BIGSERIAL NOT NULL PRIMARY KEY"
        for entry in self.entries:
            cmd = cmd + ", " + entry.name
            if not entry.maxlength:
                cmd = cmd + " TEXT"
            else:
                cmd = cmd + " VARCHAR(" + entry.maxlength + ")"
        cmd = cmd + ");"
        for entry in self.entries:
            cmd = cmd + "ALTER TABLE " + self.name + " ADD COLUMN IF NOT EXISTS "
            if not entry.maxlength:
                cmd = cmd + entry.name + " TEXT; "
            else:
                cmd = cmd + entry.name + " VARCHAR(" + entry.maxlength + "); "
        cursor.execute(cmd)
        cursor.close()
        self.dbconnection.commit()
