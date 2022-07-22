class Machine:
    def __init__(self):
        self.proxy = None
        self.windowsize = None
        self.driver = None
        self.timeout = None
        self.wait = None
        self.honeypots = None

    def waituntil(self, expression):
        pass

    def loadurl(self, url, https=False):
        pass

    def gethtml(self, encoding="utf8"):
        pass

    def getcss(self, element):
        pass

    def ishoneypot(self, element):
        pass

    def clickon(self, selector):
        pass

    def clicklink(self, url, selector):
        pass

    def goback(self, steps=1):
        pass
