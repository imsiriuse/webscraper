import psycopg2
from bs4 import BeautifulSoup


class Parser:
    def __init__(self, entries, name, selector=None):
        self.entries = entries
        self.name = name
        self.selector = selector

    def parsehtml(self, html):
        soup = BeautifulSoup(html, "html5lib")

        results = {}
        for entry in self.entries:
            tags = soup.select(entry.selector)
            if len(tags) != 0:
                results[entry.name] = tags

        if len(results) == 0:
            return None

        return results


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
        cursor = self.dbconnection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS " + self.name + " ( id SERIAL NOT NULL PRIMARY KEY, content TEXT NOT NULL);")
        for entry in self.entries:
            cursor.execute("CREATE TABLE IF NOT EXISTS " + entry.name + " ( id SERIAL NOT NULL PRIMARY KEY, content TEXT NOT NULL," + self.name + "_id INT REFERENCES " + self.name + "(id));")

        cursor.close()
        self.dbconnection.commit()

    def insertrow(self, html, filename):
        results = self.parsehtml(html)

        if not results:
            return None

        cursor = self.dbconnection.cursor()

        cursor.execute("INSERT INTO " + self.name + "(content) VALUES(%s) RETURNING id;", (filename,))
        mainid = cursor.fetchone()[0]

        for column in results:
            tags = results[column]

            for tag in tags:
                text = " ".join(tag.get_text().split())
                cmd = "INSERT INTO " + column + "(content, " + self.name + "_id) VALUES ( %s, %s);"
                cursor.execute(cmd, (text, mainid))

        cursor.close()
        self.dbconnection.commit()
