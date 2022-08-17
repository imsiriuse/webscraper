import htmlparsing


class ActionClick:
    def __init__(self, selector, routine=False):
        self.selector = selector
        self.routine = routine

    def __call__(self, machine, tree):
        machine.clickon(self.selector)


class ActionPaging:
    def __init__(self, selector, routine=False):
        self.selector = selector
        self.routine = routine

    def __call__(self, machine, tree):
        pagelinks = htmlparsing.getlinks(machine.gethtml(encoding=tree.config.encoding), self.selector)
        tree.loadpagelinks(pagelinks, self.selector)


class ActionNextpage:
    def __init__(self, selector, routine=False):
        self.selector = selector
        self.routine = routine

    def __call__(self, machine, tree):
        nextlinks = htmlparsing.getlinks(machine.gethtml(encoding=tree.config.encoding), self.selector)
        tree.loadnextlinks(nextlinks, self.selector)


class ActionGetcontent:
    def __init__(self, selectors, alias=None, parentselector=None, routine=False):
        self.selectors = selectors
        self.routine = routine
        self.parentselector = parentselector
        self.alias = alias

    def __call__(self, machine, tree):
        html = machine.gethtml(encoding=tree.config.encoding)

        if self.parentselector:
            tags = htmlparsing.getcontent(html, self.parentselector)
        else:
            tags = [html]

        for tag in tags:
            results = {}
            for selector in self.selectors:
                result = htmlparsing.getcontent(tag, selector)
                result = htmlparsing.concattags(result)
                results[selector] = result
            if self.alias:
                results["type"] = self.alias

            tree.results.append(results)
            print(results)
            print("------------------------")
