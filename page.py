class Page:
    def __init__(self, url, parent, parserid):
        self.url       = url
        self.childs    = []
        self.parent    = parent
        self.parserid  = parserid
        self.opened    = False

    def __str__(self):
        result  = self.url + '\n'
        result += "parent: "    + str(self.parent)    + "\n"
        result += "childs: "    + str(self.childs)    + "\n"
        result += "parserid: "  + str(self.parserid)  + "\n"
        result += "opened: "    + str(self.opened)    + "\n"
        result += "-----------" + "\n"
        return result

    def isleaf(self):
        if len(self.childs) == 0:
            return True
        return False

    def addchild(self, child):
        if child:
            self.childs.append(child)
