import psycopg2
from bs4 import BeautifulSoup


class Parser:
    def __init__(self, entries, name):
        self.entries = entries
        self.name = name
        self.results = []
        for entry in self.entries:
            self.results.append([])

    def parsehtmlcont(self, html):
        soup = BeautifulSoup(html)

        result = {}
        for entry in self.entries:
            result[entry.name] = soup.select(entry.selector)

        return result

    def parsehtml(self, html):
        return self.parsehtmlcont(html)


class DbParser(Parser):
    def __init__(self, entries, name):
        super().__init__(entries, name)
        self.dbconnection = None
        self.cursor = None

    def dbconnect(self, dbname, user="postgres", password="postgres", host="localhost", port="5432"):
        self.dbconnection = psycopg2.connect(
            host=host,
            database=dbname,
            user=user,
            password=password,
            port=port
        )
        self.cursor = self.dbconnection.cursor()

    def dbdisconnect(self):
        self.cursor.close()
        self.dbconnection.close()
        self.cursor = None
        self.dbconnection = None

    def inittable(self):
        command = "CREATE TABLE " + self.name + " ( id BIGSERIAL NOT NULL PRIMARY KEY "
        for entry in self.entries:
            command = command + entry.name
            if not entry.maxlength:
                command = ", " + command + "TEXT "
            else:
                command = ", " + command + "VARCHAR(" + entry.maxlength + ") "
        command = command + ");"
        return command

    def parsehtml(self, html):
        result = self.parsehtmlcont(html)
        return result
