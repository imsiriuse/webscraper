import random
import tree
from random import randint
import traceback


class Scraper:
    def __init__(self, config):
        # table with results
        self.results = []
        # tree of scraped web pages
        self.tree = None
        # configuration
        self.config = config

    def createMachine(self):
        return self.config.driver(
            windowsize=random.choice(self.config.windowsizes)
        )

    def runthread(self, machine):
        machine.loadurl(
            url=self.tree.root.url,
            timeout=randint(self.config.timeoutmin, self.config.timeoutmax) / 1000
        )

        while not self.tree.alltraversed():
            page = self.tree.current
            if not page.opened:
                page.open(machine)
            else:
                if page.isleaf():
                    page.removeself()
                    self.tree.gorandomback(machine)
                else:
                    self.tree.gonext()

    def createthread(self):
        # create headless browser
        machine = self.createMachine()
        # start thread
        try:
            self.runthread(machine)
        finally:
            machine.driver.close()

    def start(self):
        # set first set of urls from config file as starts
        self.tree = tree.Tree(self.config)

        # start thread
        self.createthread()
