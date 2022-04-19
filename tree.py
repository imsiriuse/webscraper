import page
import config
import webparsing
import random
from random import randint


class Tree:
    def __init__(self, starturl):
        self.root = page.Page(url=starturl, parent=None, parserid=0)
        self.data = {self.root.url: self.root}
        self.current = self.root
        self.pagestack = [self.current]

    def __str__(self):
        return self.root.printtree(level = 0)

    def getcurrent(self):
        return self.current

    def setcurrent(self, node):
        if not node:
            return None
        self.current = node

    def opencurrent(self, driver):
        # print("otvaram: " + self.current.url)
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
            pagelinks = webparsing.getlinks(html, parser["pageselector"])

        for link in pagelinks:
            if link not in self.data:
                newpage = page.Page(link, self.current, self.current.parserid)
                self.current.addchild(newpage)
                self.data[link] = newpage

        self.current.opened = True

        return result

    def getnumberofbacks(self):
        # generate random number of back clicks
        if len(self.pagestack) == 1:
            return 0
        return randint(1, randint(1, len(self.pagestack) - 1))

    def deletecurrent(self):
        self.current.removeself()

    def iscurrentopen(self):
        return self.current.opened

    def gorandomback(self, driver):
        numberofbacks = self.getnumberofbacks()
        #print("skacem dozadu o :" + str(numberofbacks))
        #print("som v hlbke: "+ str(len(self.pagestack)))
        for i in range(numberofbacks):
            self.pagestack.pop()
            self.current = self.current.parent

    def iscurrentleaf(self):
        return self.current.isleaf()

    def gonext(self):
        # print("skacem do: "  + self.current.url)
        self.current = random.choice(self.current.childs)
        self.pagestack.append(self.current)

    def alltraversed(self):
        if self.root.opened and len(self.root.childs) == 0:
            return True
        return False
