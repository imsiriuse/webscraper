import random
import tree


class Scraper:
    def __init__(self, config):
        # table with results
        self.results = []
        # tree of scraped web pages
        self.tree = None
        #configuration
        self.config = config

    def createMachine(self):
        return self.config.driver(windowsize=random.choice(self.config.windowsizes))

    def runthread(self, driver):
        # download url through http not https
        driver.get(self.tree.root.url.replace("https://", "http://"))

        while not self.tree.alltraversed():
            print("som v:" + str(self.tree.getcurrent()))

            if not self.tree.iscurrentopen():
                self.tree.opencurrent(driver)

            if self.tree.iscurrentopen():
                if self.tree.iscurrentleaf():
                    self.tree.deletecurrent()
                    self.tree.gorandomback(driver)
                else:
                    self.tree.gonext(driver)

    def createthread(self):
        # create headless browser
        machine = self.createMachine()
        # set tree to root
        self.tree.current = self.tree.root
        # start thread
        self.runthread(machine.driver)

    def start(self):
        # set first set of urls from config file as starts
        self.tree = tree.Tree(self.config)

        # start thread
        self.createthread()

