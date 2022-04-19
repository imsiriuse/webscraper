class Page:
    def __init__(self, url, parent, parserid):
        self.url       = url
        self.childs    = []
        self.parent    = parent
        self.parserid  = parserid
        self.opened    = False
    def __repr__(self):
        return self.url
    #def __str__(self):
    #    result  = self.url + '\n'
    #    result += "parent: "    + str( "None" if not self.parent else self.parent.url)    + "\n"
    #    result += "childs: "    + str([child.url for child in self.childs])    + "\n"
    #    result += "parserid: "  + str(self.parserid)  + "\n"
    #    result += "opened: "    + str(self.opened)    + "\n"
    #    result += "-----------" + "\n"
    #    return result

    def __str__(self):
        result = self.url + '\n'
        for child in self.childs:
            result += " - " + child.url + "\n"
        return result

    def isleaf(self):
        if len(self.childs) == 0:
            return True
        return False

    def addchild(self, child):
        if child:
            self.childs.append(child)
