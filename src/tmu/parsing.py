import glob
from bs4 import BeautifulSoup


class Entry:
    def __init__(self, name, selector):
        self.name = name
        self.selector = selector

    def parse(self):
        pass


class ArrayEntry(Entry):
    def parse(self):
        pass


class TableEntry(Entry):
    def parse(self):
        pass


def readfiles(folderpath, n=None, ext=""):
    filenames = glob.glob(folderpath + "/*" + ext)

    if not n:
        n = len(filenames)

    results = []
    for i in range(n):
        f = open(filenames[i], "r")
        results.append(f.read())
        f.close()

    return results


def parsehtml(entries, html):
    soup = BeautifulSoup(html)

    result = {}
    for entry in entries:

        result[entry.name] = soup.select(entry.selector)

    return result
