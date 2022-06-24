import htmlparsing


class ActionClick:
    def __init__(self, selector):
        self.selector = selector

    def __call__(self, driver, tree):
        pass


class ActionPaging:
    def __init__(self, selector):
        self.selector = selector

    def __call__(self, driver, tree):
        html = tree.gethtml(driver)

        pagelinks = htmlparsing.getlinks(html, self.selector)

        tree.loadpagelinks(pagelinks)


class ActionNextpage:
    def __init__(self, selector):
        self.selector = selector

    def __call__(self, driver, tree):
        nextlinks = htmlparsing.getlinks(tree.gethtml(driver), self.selector)
        tree.loadnextlinks(nextlinks)


class ActionGetcontent:
    def __init__(self, selectors, alias, parentselector = None ):
        self.selectors = selectors
        self.parentselector = parentselector
        self.alias = alias

    def __call__(self, driver, tree):
        html = tree.gethtml(driver)

        if self.parentselector:
            tags = htmlparsing.getcontent(html, self.parentselector)
        else:
            tags = [html]

        for tag in tags:
            for selector in self.selectors:
                result = htmlparsing.getcontent(tag, selector)
                result = htmlparsing.concattags(result)

                results = {}
                results[self.alias] = {selector: result}

            tree.results.append(results)
        print(results)
        print("------------------------")