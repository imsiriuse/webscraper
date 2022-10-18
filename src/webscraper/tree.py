from webscraper import page
import random
from random import randint


class Tree:
    def __init__(self, config):
        self.config = config

        self.root = page.Page(
            url=config.starturl,
            parent=None,
            parser=config.parser,
            selector=None
        )

        self.data = {self.root.url: self.root}
        self.current = self.root
        self.pagestack = [self.current]
        self.results = []

    def __str__(self):
        return self.root.printtree(level=0)

    def loadnextlinks(self, nextlinks, selector):
        for link in nextlinks:
            if link not in self.data:
                newpage = page.Page(
                    url=link,
                    parent=self.current,
                    parser=self.current.parser.nextnode,
                    selector=selector
                )

                self.current.addchild(newpage)
                self.data[link] = newpage

    def loadpagelinks(self, pagelinks, selector):
        for link in pagelinks:
            if link not in self.data:
                newpage = page.Page(
                    url=link,
                    parent=self.current,
                    parser=self.current.parser,
                    selector=selector
                )

                self.current.addchild(newpage)
                self.data[link] = newpage

    def gorandomback(self, machine):
        if len(self.pagestack) == 1:
            return 0
        steps = randint(1, randint(1, len(self.pagestack) - 1))

        for i in range(steps):
            self.pagestack.pop()
            self.current = self.current.parent
        print("goingback:" + str(steps))
        machine.goback(steps=steps)

    def gonext(self, machine):
        self.current = random.choice(self.current.childs)
        self.pagestack.append(self.current)

        self.current.parser.run(machine, self, routine=True)
        print("gonext:" + self.current.selector + " " + self.current.url)
        machine.clicklink(self.current.url, self.current.selector)

    def end(self):
        if self.root.opened and len(self.root.childs) == 0:
            return True
        return False

    def open(self, node, machine):
        node.opened = True
        node.parser.run(machine, self)

    def remove(self, node):
        if node.parent:
            node.parent.removechild(node)
        else:
            return None
