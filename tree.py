import page
import math
import config
import webparsing
from random import randint, random


class Tree:
    def __init__(self, starturl):
        self.root = page.Page(url=starturl, parent=None, parserid=0)
        self.data = {self.root.url: self.root}
        self.current = self.root
        self.sliz = [self.current]

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

        nextlinks = []
        if "nextselector" in parser:
            nextlinks = webparsing.getlinks(html, parser["nextselector"])

        for link in nextlinks:
            if link not in self.data:
                newpage = page.Page(link, self.current, self.current.parserid + 1)
                self.current.addchild(newpage)
                self.data[link] = newpage

        pagelinks = []
        if "pageselector" in parser:
            pagelinks = webparsing.getlinks(html, parser["pagelinks"])

        for link in pagelinks:
            if link not in self.data:
                newpage = page.Page(link, self.current, self.current.parserid)
                self.current.parent.addchild(newpage)
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
        if len(self.sliz) == 1:
            return 0
        return randint(1,randint(1,len(self.sliz)-1))

    def deletecurrent(self):
        if not self.current.parent:
            return None
        self.current.parent.childs.remove(self.current)

    def iscurrentopen(self):
        return self.current.opened

    def gorandomback(self, driver):
        numberofbacks = self.getnumberofbacks()

        for i in range(numberofbacks):
            print(self.sliz)
            driver.back()
            self.sliz.pop()
            self.current = self.current.parent

    def iscurrentleaf(self):
        return self.current.isleaf()

    def gonext(self):
        self.current = self.current.childs[randint(0, len(self.current.childs)-1)]

        self.sliz.append(self.current)
