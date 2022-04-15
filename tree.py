import page
import math
import config
import webparsing
from random import randint


class Tree:
    def __init__(self, starturl):
        self.root = page.Page(url=starturl, parent=None, parserid=0)
        self.data = {self.root.url: self.root}
        self.current = self.root

    def getcurrent(self):
        return self.current

    def setcurrent(self, node):
        if not node:
            return None
        self.current = node

    def opencurrent(self, driver):
        html = webparsing.gethtml(driver, self.current.url, config.CONFIG["timeout"][0], config.CONFIG["timeout"][1])
        parser = config.CONFIG["parsetree"][self.current.parserid]

        result = None
        if "contents" in parser:
            result = webparsing.getcontent(html, parser["contents"], config.CONFIG["contentselectors"])

        links = None
        if parser["strategy"] != "c":
            links = webparsing.getlinks(html, parser["selector"])

            for link in links:
                if not link in self.data:
                    newpage = None
                    if parser["strategy"] == "n":
                        newpage = page.Page(link, page, self.current.parserid + 1)
                    if parser["strategy"] == "p":
                        newpage = page.Page(link, page, self.current.parserid)
                    self.current.addchild(newpage)
                    self.data[link] = newpage
        self.current.opened = True

        return result

    @staticmethod
    def getdepth(node):
        # get depth of node in tree
        depth = 0
        parent = node.parent
        while parent:
            depth += 1
            parent = parent.parent
        return depth

    def getnumberofbacks(self):
        # generate random number of back clicks
        depth = self.getdepth(self.current)
        maxlvl = config.CONFIG["c"] ** depth
        val = randint(1, maxlvl)
        val = math.log(val, config.CONFIG["c"])
        val = round(maxlvl - val)
        return val

    def deletecurrent(self):
        if not self.current.parent:
            return None
        parent = self.data[self.current.url].parent
        parent.childs.remove(self.current)
        self.current = parent

    def iscurrentopen(self):
        return self.current.opened

    def gorandomback(self, driver):
        numberofbacks = self.getnumberofbacks()
        for i in range(numberofbacks):
            driver.back()
            self.current = self.current.parent

    def iscurrentleaf(self):
        return self.current.isleaf()

    def gonext(self):
        self.current = self.current.childs[randint(0, len(self.current.childs) - 1)]
