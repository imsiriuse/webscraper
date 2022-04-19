import virtualbrowser
import config
import tree


class Scraper:
    def __init__(self):
        # table with results
        self.results = []
        # tree of scraped web pages
        self.tree = None

    def runthread(self, driver):
        while not self.tree.alltraversed():
            print(self.tree.getcurrent())
            if not self.tree.iscurrentopen():

                results = self.tree.opencurrent(driver)
                if results:
                    self.results.append(results)

            if self.tree.iscurrentopen():
                if self.tree.iscurrentleaf():
                    self.tree.deletecurrent()
                    self.tree.gorandomback(driver)
                else:
                    self.tree.gonext()

    def createthread(self):
        # create headless browser
        driver = virtualbrowser.createChromeMachine("127.0.0.1")
        # set tree to root
        self.tree.current = self.tree.root
        # start thread
        self.runthread(driver)
        # closing headless browser
        driver.quit()

    def start(self):
        # erase previous values of results
        self.results = []

        # set first set of urls from config file as starts
        self.tree = tree.Tree(config.CONFIG["start"])

        # start thread
        self.createthread()

    @staticmethod
    def removeseparators(output):
        # replacing every ";"" with ","" because of unexpected delimiters in csv file
        for i in range(0, len(output)):
            for j in range(0, len(output[i])):
                output[i][j] = output[i][j].replace(";", ",")
        return output

    def getresults(self):
        # convert sparse table to csv table
        output = []
        for row in self.results:
            output.append([""] * len(config.CONFIG["contents"]))
            for cell in row:
                output[len(output) - 1][cell[0]] = cell[1]

        output = self.removeseparators(output)
        return output
