class Entry:
    def __init__(self, name, selector, maxlength=None):
        self.name = name
        self.selector = selector
        self.maxlength = maxlength

    def __str__(self):
        res = self.name + ": " + self.selector + " "
        return res


class ArrayEntry(Entry):
    def parse(self):
        pass


class TableEntry(Entry):
    def parse(self):
        pass
