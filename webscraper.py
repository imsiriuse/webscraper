import virtualbrowser
import config
import tree
import page

class Scraper:
    def __init__(self):
        #table with results
        self.results    = []
        #tree of scraped web pages
        self.tree = None
    #-------------------------------------
    def runThread(self, driver, page):
        if not page.opened:
            self.results.append(self.tree.opennode(page))
        if page.opened:
            #todo
            nextpage = page.getNext()
            if nextpage:
                self.runThread(driver, page.getNext())
    #-------------------------------------
    def createThread(self):
        #create headless browser
        driver = virtualbrowser.createChromeMachine("127.0.0.1")
        
        #start tree
        self.runThread(driver, self.root)
        
        driver.quit()
    #-----------------------------------
    #start the scraping process
    def start(self):
        #erase previous values of results
        self.results = []
        self.data    = {}

        #set first set of urls from config file as starts
        self.tree = tree.Tree(config.CONFIG["starturl"])
        
        self.createThread()
    #-------------------------------------------------
    def removeSeparators(self, output):
        # replacing every ";"" with ","" because of unexpected delimiters in csv file
        for i in range(0, len(output)):
            for j in range(0, len(output[i])):
                output[i][j] = output[i][j].replace(";", ",")
        return output
    # -------------------------------------------------
    #convert sparse table to csv table
    def getResults(self):
        output = []
        for row in self.results:
            output.append([""] * len(config.CONFIG["contents"]))
            for cell in row:
                output[len(output) - 1][cell[0]] = cell[1]

        output = self.removeSeparators(output)
        return output
    #-------------------------------------------------
