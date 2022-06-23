import page
import config as CFG
import htmlparsing
import random
from random import randint


class Tree:
    def __init__(self, config):
        self.config = config
        self.root = page.Page(url=config.starturl, parent=None, parserid=0)
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

    def gethtml(self, driver, timeout):
        # set delay, to slow down downloading
        driver.implicitly_wait(timeout)

        # return html code of webpage in utf8
        return driver.page_source.encode('utf8')

    def opencurrent(self, driver):
        print("otvaram: " + self.current.url, self.config.timeout)
        html = self.gethtml(driver, randint(self.config.timeout[0], self.config.timeout[1]) / 1000)

        parser = self.config.actions[self.current.parserid]

        result = None
        if "contselector" in parser:
            result = htmlparsing.getcontent(html, parser["contselector"]["link"])

        nextlinks = []
        if "nextselector" in parser:
            nextlinks = htmlparsing.getlinks(html, parser["nextselector"])

        for link in nextlinks:
            if link not in self.data:
                newpage = page.Page(link, self.current, self.current.parserid + 1)
                self.current.addchild(newpage)
                self.data[link] = newpage

        pagelinks = []
        if "pageselector" in parser:
            pagelinks = htmlparsing.getlinks(html, parser["pageselector"])

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
        print("skacem dozadu o :" + str(numberofbacks))
        print("som v hlbke: "+ str(len(self.pagestack)))
        for i in range(numberofbacks):
            self.pagestack.pop()
            self.current = self.current.parent

    def iscurrentleaf(self):
        return self.current.isleaf()

    def gonext(self, driver):
        print("skacem do: "  + self.current.url)
        #choose link where to jump
        self.current = random.choice(self.current.childs)
        self.pagestack.append(self.current)

        driver.get(self.current.url)

    def alltraversed(self):
        if self.root.opened and len(self.root.childs) == 0:
            return True
        return False
