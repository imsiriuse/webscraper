class Entry:
    def __init__(self, name, selector, maxlength=None):
        self.name = name
        self.selector = selector
        self.maxlength = maxlength

    def parse(self):
        pass


class ArrayEntry(Entry):
    def parse(self):
        pass


class TableEntry(Entry):
    def parse(self):
        pass
