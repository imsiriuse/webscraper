class Page:
    def __init__(self, url, parent, parser, selector):
        self.url = url
        self.selector = selector
        self.childs = []
        self.parent = parent
        self.parser = parser
        self.opened = False

    def __repr__(self):
        return self.url

    def __str__(self):
        result = self.url + '\n'
        return result

    def printtree(self, level=0):
        ret = " - "*level + self.url + " - id:" + str(self.parser) + "\n"
        for child in self.childs:
            ret += child.printtree(level+1)
        return ret

    def isleaf(self):
        if not self.childs:
            return True
        if len(self.childs) == 0:
            return True
        return False

    def addchild(self, child):
        if child:
            self.childs.append(child)
        else:
            return None

    def removechild(self, child):
        if child:
            self.childs.remove(child)
        else:
            return None