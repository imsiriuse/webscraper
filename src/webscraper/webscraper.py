import random
import tree


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
            windowsize=random.choice(self.config.windowsizes),
            timeout=self.config.timeout,
            honeypots=self.config.honeypots,
            headless=self.config.headless
        )

    def runthread(self, machine):
        while not self.tree.end():
            current = self.tree.current

            if not current.opened:
                print("opening:" + str(current))
                self.tree.open(current, machine)
            else:
                if current.isleaf():
                    print("removing:" + str(current))
                    self.tree.remove(current)
                    self.tree.gorandomback(machine)
                else:
                    self.tree.gonext(machine)

    def createthread(self):
        # create headless browser
        machine = self.createMachine()
        # start thread
        try:
            machine.loadurl(url=self.tree.root.url)
            self.runthread(machine)
        finally:
            machine.driver.close()

    def start(self):
        # set first set of urls from config file as starts
        self.tree = tree.Tree(self.config)

        # start thread
        self.createthread()
