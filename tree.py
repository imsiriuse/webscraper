import page
import random
from random import randint


class Tree:
    def __init__(self, config):
        self.config = config
        self.root = page.Page(url=config.starturl, parent=None, parser=config.parser)
        self.data = {self.root.url: self.root}
        self.current = self.root
        self.pagestack = [self.current]
        self.results = []

    def __str__(self):
        return self.root.printtree(level = 0)

    def getcurrent(self):
        return self.current

    def setcurrent(self, node):
        if not node:
            return None
        self.current = node

    def gethtml(self, driver):
        # set delay, to slow down downloading
        timeout = randint(self.config.timeoutmin, self.config.timeoutmax) / 1000
        driver.implicitly_wait(timeout)

        # return html code of webpage in utf8
        return driver.page_source.encode('utf8')

    def loadnextlinks(self, nextlinks):
        for link in nextlinks:
            if link not in self.data:
                newpage = page.Page(link, self.current, self.config.parser.nextnode)
                self.current.addchild(newpage)
                self.data[link] = newpage

    def loadpagelinks(self, pagelinks):
        for link in pagelinks:
            if link not in self.data:
                newpage = page.Page(link, self.current, self.config.parser)
                self.current.addchild(newpage)
                self.data[link] = newpage

    def opencurrent(self, driver):
        # print("otvaram: " + self.current.url)

        self.current.parser.run(driver, self)
        self.current.opened = True

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
        #  print("skacem dozadu o :" + str(numberofbacks))

        # print("som v hlbke: "+ str(len(self.pagestack)))
        for i in range(numberofbacks):
            self.pagestack.pop()
            self.current = self.current.parent

    def iscurrentleaf(self):
        return self.current.isleaf()

    def gonext(self, driver):
        # print("skacem do: "  + self.current.url)

        #  choose link where to jump
        self.current = random.choice(self.current.childs)
        self.pagestack.append(self.current)

        driver.get(self.current.url)

    def alltraversed(self):
        if self.root.opened and len(self.root.childs) == 0:
            return True
        return False
