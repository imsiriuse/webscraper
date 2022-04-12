from random import randint
from bs4 import BeautifulSoup
import math
import config

class Page:
    def __init__(self, url, childs, parent, parserid):
        self.url       = url
        self.childs    = childs
        self.parent    = parent
        self.parserid    = parserid
        self.opened    = False
    # -----------------------------------
    def __str__(self):
        result  = self.url + '\n'
        result += "parent: "    + str(self.parent)    + "\n"
        result += "childs: "    + str(self.childs)    + "\n"
        result += "node: "      + str(self.parserid)     + "\n"
        result += "opened: "    + str(self.opened)    + "\n"
        result += "-----------" + "\n"
        return result
    # -----------------------------------
    def isleaf(self):
        if not self.childs:
            return True
        if len(self.childs) == 0:
            return True
        return False
    # -----------------------------------
    def gethtml(self, driver):
        # set delay to slow down downloading
        driver.implicitly_wait(randint(config.CONFIG["timeout"][0], config.CONFIG["timeout"][1]) / 1000)

        # download url through http not https
        driver.get(self.url.replace("https://", "http://"))

        #return html code of webpage in utf8
        return driver.page_source.encode('utf8')
    # -----------------------------------
    def concattags(self, tags):
        result = ""
        for tag in tags:
            result += tag.get_text() + " "
        return result
    # -----------------------------------
    def getlinks(self, html, selector):
        #parse html by beatuiful soup $
        soup = BeautifulSoup(html, "html5lib")
        # use selector
        divs = soup.select(selector)
        # find all links from div
        links = []
        for div in divs:
            aas = div.findAll('a')
            for a in aas:
                href = a['href']
                if href not in links:
                    links.append(href)
        return links
    # -----------------------------------
    def parsecontent(self, html):
        # parse html with BS
        soup = BeautifulSoup(html, "html5lib")

        selectorids = config.CONFIG["parsetree"][self.parserid]

        result = []
        for selectorid in selectorids:
            tags = soup.select(config.CONFIG["contentselectors"][selectorid])

            # add to results file in form of pair col number and string
            result.append((selectorid, self.concattags(tags)))
        return result
    # -----------------------------------
    def getnumberofbacks(self):
        maxlvl = config.CONFIG["c"]**self.depth
        temp = randint(1, maxlvl)

        temp = math.log(temp, config.CONFIG["c"])
        temp = round(maxlvl - temp)
        return temp
    # -----------------------------------
    def addchild(self, child, dict):
        if not child in dict:
            self.childs.append(child)
    # -----------------------------------
    def process(self, driver, dict):
        html = self.gethtml(driver)
        parser = config.CONFIG["parsetree"][self.parserid]

        result = None
        if "contents" in parser:
            result = self.parsecontent(html, parser["contents"])

        links = None
        if parser["strategy"] != "c":
            links = self.getlinks(html, parser["selector"])

            for link in links:
                if not link in dict:
                    if parser["strategy"] == "n":
                        self.addchild(Page(link, [], self, self.parserid + 1))
                    if parser["strategy"] == "p":
                        self.addchild(Page(link, [], self, self.parserid))

        self.opened = True

        return result
