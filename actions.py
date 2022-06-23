import htmlparsing


class Action:
    def __init__(self):
        pass

    def __call__(self, driver, tree):
        pass


class ActionClick(Action):
    def __init__(self, selector):
        super().__init__()
        self.selector = selector

    def __call__(self, driver, tree):
        pass


class ActionPaging  (Action):
    def __init__(self, selector):
        super().__init__()
        self.selector = selector

    def __call__(self, driver, tree):
        pagelinks = htmlparsing.getlinks(tree.gethtml(driver), self.selector)
        tree.loadpagelinks(pagelinks)


class ActionNextpage(Action):
    def __init__(self, selector):
        super().__init__()
        self.selector = selector

    def __call__(self, driver, tree):
        nextlinks = htmlparsing.getlinks(tree.gethtml(driver), self.selector)
        tree.loadnextlinks(nextlinks)


class ActionContent (Action):
    def __init__(self, selector):
        super().__init__()
        self.selector = selector

    def __call__(self, driver, tree):
        results = htmlparsing.getcontent(tree.gethtml(driver), self.selector)
        tree.addresults(results)
