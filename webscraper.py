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
        url = self.tree.root.url.replace("https://", "http://")
        print(url)
        driver.get(url)

        while not self.tree.alltraversed():
            print(self.tree.current.parser.actions[0].selector)

            if not self.tree.current.opened:
                self.tree.opencurrent(driver)
            else:
                if self.tree.current.isleaf():
                    self.tree.deletecurrent()
                    self.tree.gorandomback(driver)
                else:
                    self.tree.gonext(driver)

    def createthread(self):
        # create headless browser
        machine = self.createMachine()
        # start thread
        self.runthread(machine.driver)

    def start(self):
        # set first set of urls from config file as starts
        self.tree = tree.Tree(self.config)

        # start thread
        self.createthread()

