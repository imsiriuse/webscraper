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
        return self.root.printtree(level=0)

    def loadnextlinks(self, nextlinks):
        for link in nextlinks:
            if link not in self.data:
                newpage = page.Page(link, self.current, self.current.parser.nextnode)
                self.current.addchild(newpage)
                self.data[link] = newpage

    def loadpagelinks(self, pagelinks):
        for link in pagelinks:
            if link not in self.data:
                newpage = page.Page(link, self.current, self.current.parser)
                self.current.addchild(newpage)
                self.data[link] = newpage

    def gorandomback(self, machine):
        if len(self.pagestack) == 1:
            return 0
        steps = randint(1, randint(1, len(self.pagestack) - 1))

        for i in range(steps):
            self.pagestack.pop()
            self.current = self.current.parent

        machine.goback(steps=steps)

    def gonext(self):
        self.current = random.choice(self.current.childs)
        self.pagestack.append(self.current)

    def alltraversed(self):
        if self.root.opened and len(self.root.childs) == 0:
            return True
        return False
