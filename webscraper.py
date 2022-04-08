class Page:
    def __init__(self, u, c, p, d):
        self.url       = u
        self.childs    = c
        self.parent    = p
        self.depth     = d
        self.opened    = False
    def __str__(self):
        result  = self.url + '\n'
        result += "parent: "    + str(self.parent)    + "\n"
        result += "childs: "    + str(self.childs)    + "\n"
        result += "node: "      + str(self.depth)     + "\n"
        result += "opened: "    + str(self.opened)    + "\n"
        result += "-----------" + "\n"
        return result
    def isLeaf(self):
        if not self.childs:
            return True
        if len(self.childs) == 0:
            return True
        return False
#-------------------------------------
class Scraper:  
    #constructor
    def __init__(self, config):
        # list of proxy servers ips
        self.proxies    = config["proxies"]
        #number of threads
        self.threads    = 1 
        #timeout interval min-max to wait
        self.timeout    = config["timeout"]
        #list of urls to start in first node
        self.starturl   = config["start"]
        #tree structure to store scraping logic
        self.parsetree  = config["parsetree"]
        #all selectors to be used during scraping
        self.contents   = config["contentselectors"]
        #table with results
        self.results    = []
        #number of rows in results csv table
        self.resultsnum = 0
        #table with links x node reference
        self.pages      = []
        #dictionary of added URLs
        self.opened     = {}
        #constant for generation number of previous levels
        self.c          = 2
    #-----------------------------------
    def getHtml(self, driver, url):
        from random import randint

        #set delay to slow down downloading
        driver.implicitly_wait(randint(self.timeout[0], self.timeout[1])/1000)
        
        #download url through http not https
        driver.get(url.replace("https://", "http://"))
        
        return driver.page_source.encode('utf8')
    #-----------------------------------
    def concattags(self, tags):
        result = ""
        for tag in tags:
            result += tag.get_text() + " "
        return result
    #-----------------------------------
    def getlinks(self, html, selector):
        from bs4 import BeautifulSoup
        import html5lib
        
        soup = BeautifulSoup(html, "html5lib")
        
        links = []
        
        #use selector
        divs = soup.select(selector)

        #find all links from div
        for div in divs:
            aas = div.findAll('a')
        
            for a in aas:
                href = a['href']
                if href not in links:
                    links.append(href)
        return links
    #-----------------------------------
    def parsecontent(self, html, selectors):
        from bs4 import BeautifulSoup
        
        #parse html with BS
        soup = BeautifulSoup(html, "html5lib")
        
        for selectorid in selectors[1:]:
            tags = soup.select(self.contents[selectorid])

            #add to results file in form of pair col number and string
            self.results.append((selectorid, self.resultsnum, self.concattags(tags)))
        self.resultsnum += 1
    #-------------------------------------
    def getnumberofbacks(self, page):
        from random import randint
        import math
        
        maxlvl = self.c**page.depth
        temp = randint(1,maxlvl)
        print(temp)
        temp = math.log(temp, self.c)
        temp = round(maxlvl - temp)
        return temp
    #-------------------------------------
    def runThread(self, driver, idx):            
        from random import randint

        page = self.pages[idx]
        node = self.parsetree[page.depth]
        html = self.getHtml(driver, page.url)
        
        print(page.url)
        
        #harvest data if not yet harvested
        if not self.opened[page.url]:
            print("otvaram url")
            if "contents" in node:
                self.parsecontent(html, node["contents"])
            
            if node["strategy"] != "c":
                links = self.getlinks(html, node["selector"])
                
                for link in links:
                    if not link in self.opened:
                        if node["strategy"] == "n":
                            self.pages.append(Page(link, [], idx, page.depth + 1))
                            self.pages[idx].childs.append(len(self.pages) - 1)
                        if node["strategy"] == "p":
                            self.pages.append(Page(link, [], idx, page.depth))
                            self.pages[page.parent].childs.append(len(self.pages) - 1)
                        
                        self.opened[link] = False
            self.opened[page.url] = True
        
        if self.opened[page.url]:
            if page.isLeaf():
                self.pages[page.parent].childs.remove(idx)
                numofbacks = self.getnumberofbacks(page)
                print("skacem o: " + str(numofbacks))
                if numofbacks == 0:
                    return None
                for i in range(numofbacks):
                    nextid = page.parent
                    if not nextid:
                        return None
                    page = self.pages[nextid]
                self.runThread(driver, nextid)
            else:
                self.runThread(driver, page.childs[randint(0, len(page.childs)-1)])
    #-------------------------------------
    def createThread(self):
        import virtualbrowser
        
        #create headless browser
        driver = virtualbrowser.createChromeMachine("127.0.0.1")
        
        #start tree
        self.runThread(driver, 0)
        
        driver.quit()
    #-----------------------------------
    #start the scraping process
    def start(self):
        #erase previous values of results
        self.results = []
        self.pages   = []
        
        #set first set of urls from config file as starts
        self.pages.append(Page(self.starturl, [], None, 0))
        self.opened[self.starturl] = False
        
        self.createThread()
    #-------------------------------------------------
    #convert sparse table to csv table
    def getResults(self):
        output = []
        for i in range(self.resultsnum):
            output.append([""] * len(self.contents))
        
        for elem in self.results:
            output[elem[1]][elem[0]] = elem[2]
        
        #replacing every ";"" with ","" because of unexpected delimiters in csv file
        for i in range(0,len(output)):
            for j in range(0,len(output[i])):
                output[i][j] = output[i][j].replace(";", ",")
        
        return output
    #-------------------------------------------------
