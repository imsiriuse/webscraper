
class TreeIter:
    def __init__(self, startNode, filter):
        self.start = startNode
        
    def __iter__(self):
        if filter(self.start):
            yield self.start
        
        for child in self.start.children:
            for node in TreeIter(child):
                yield node