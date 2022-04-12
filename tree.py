import page

class Tree:
    def __init__(self, starturl):
        self.root = page.Page(url = starturl, childs = [], parent = None, parserid = 0)
        self.data = {}
        self.data[self.root.url] = self.root
    #----------------------------
    def opennode(self, driver,  page):
        return page.getnewchilds(driver)
    #----------------------------
