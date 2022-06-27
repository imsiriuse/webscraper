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
            if not self.tree.current.opened:
                self.tree.opencurrent(machine.driver)
            else:
                if self.tree.current.isleaf():
                    self.tree.deletecurrent()
                    self.tree.gorandomback()
                else:
                    self.tree.gonext()

            print(self.tree.current.url)
            machine.loadurl(
                url=self.tree.current.url,
                timeout=randint(self.config.timeoutmin, self.config.timeoutmax) / 1000
            )

    def createthread(self):
        # create headless browser
        machine = self.createMachine()
        # start thread
        try:
            self.runthread(machine)
        except:
            traceback.print_exc()
        finally:
            machine.driver.close()

    def start(self):
        # set first set of urls from config file as starts
        self.tree = tree.Tree(self.config)

        # start thread
        self.createthread()
