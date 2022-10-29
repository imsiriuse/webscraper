import psycopg2
from bs4 import BeautifulSoup


class Parser:
    def __init__(self, entries, name, selector=None):
        self.entries = entries
        self.name = name
        self.selector = selector

    @staticmethod
    def tagstotext(tags):
        result = ""

        for tag in tags:
            result = result + " ".join(tag.get_text().split())
        return result

    def parsehtml(self, html):
        soup = BeautifulSoup(html, "html5lib")

        result = {}
        for entry in self.entries:
            result[entry.name] = soup.select(entry.selector)

        return result


class DbParser(Parser):
    def __init__(self, entries, name, host="localhost", user="postgres", dbname="postgres", password="postgres", port="5432"):
        super().__init__(entries, name)
        self.dbconnection = None
        self.host = host
        self.user = user
        self.dbname = dbname
        self.password = password
        self.port = port

    def dbconnect(self):
        self.dbconnection = psycopg2.connect(
            host=self.host,
            database=self.dbname,
            user=self.user,
            password=self.password,
            port=self.port
        )

    def dbdisconnect(self):
        if self.dbconnection:
            self.dbconnection.close()

    def inittables(self):
        # creating main table of parser
        cmd = "CREATE TABLE IF NOT EXISTS " + self.name + " ( id SERIAL NOT NULL PRIMARY KEY); "
        for entry in self.entries:
            cmd = cmd + "\nALTER TABLE " + self.name + " ADD COLUMN IF NOT EXISTS " + entry.name + " INT; "

        # creating tables for entries
        for entry in self.entries:
            cmd = cmd + "\nCREATE TABLE IF NOT EXISTS " + entry.name + " ( id SERIAL NOT NULL PRIMARY KEY, content TEXT NOT NULL);"

        cursor = self.dbconnection.cursor()
        cursor.execute(cmd)
        cursor.close()
        self.dbconnection.commit()

    def parsehtml(self, html):
        soup = BeautifulSoup(html, "html5lib")

        columns = []
        values = []
        for entry in self.entries:
            results = soup.select(entry.selector)
            if len(results) != 0:
                columns.append(entry)
                values.append(self.tagstotext(results))

        if len(values) == 0:
            return None

        cmd = ""

        print(cmd)

        # cursor = self.dbconnection.cursor()
        # cursor.execute(cmd, values)
        # cursor.close()
        # self.dbconnection.commit()
