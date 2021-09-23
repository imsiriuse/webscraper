class Scraper:  
    #constructor
    def __init__(self, config):
        self.proxies = config["proxies"]
        self.threads = config["threads"]
        self.timeout = config["timeout"]
        self.parsetree = config["parsetree"]
        
        self.urlpool = []
        for i in range(0,len(self.parsetree)+1):
            self.urlpool.append([])
        
        self.urlpool[0] = config["starts"]

        self.contentselectors = config["contentselectors"]
        self.results = []
        for i in range(0, len(self.contentselectors)):
            self.results.append([])
    #-----------------------------------
    def getlinks(self, selector, html):
        from bs4 import BeautifulSoup
        import html5lib
        
        soup = BeautifulSoup(html, "html5lib")
        
        links = []
        #use selector
        divs = soup.select(selector)
        
        #find all links from div
        for div in divs:
            aas = div.findAll('a')
            if len(div)==1:
                href = div['href']
                if href not in links:
                    links.append(href)

            for a in aas:
                href = a['href']
                if href not in links:
                    links.append(href)
        return links
    #-----------------------------------
    def nextstrategy(self, selector, driver, level):
        from random import randint

        for url in self.urlpool[level]:
            #set delay to slow down downloading
            driver.implicitly_wait(randint(self.timeout[0], self.timeout[1])/1000)

            #download url through http not https
            driver.get(url.replace("https://", "http://"))
            print("downloaded url: ", url)
            
            #parse to get next level links and add it to pool
            self.urlpool[level+1] += self.getlinks(selector,driver.page_source.encode('utf8'))
    #-----------------------------------
    def downloadcontent(self, selectors, driver, level):
        from random import randint
        from bs4 import BeautifulSoup

        for url in self.urlpool[level]:
            #set delay to slow down downloading
            driver.implicitly_wait(randint(self.timeout[0], self.timeout[1])/1000)
            
            #try to download actual URL
            #download url through http not https
            driver.get(url.replace("https://", "http://"))
            print("downloaded url: ", url)
            
            soup = BeautifulSoup(driver.page_source.encode('utf8'), "html5lib")
            for i in range(0, len(selectors)):
                divs = soup.select(selectors[i])
                for div in divs:
                    self.results[i].append(div.getText())
    #-----------------------------------
    def paggingstrategy(self, selector, driver, level):
        from random import randint

        for nextlink in self.urlpool[level]:
            while nextlink:
                #add found link to next level bucket for next processing
                self.urlpool[level+1].append(nextlink)
                
                #set delay to slow down downloading
                driver.implicitly_wait(randint(self.timeout[0], self.timeout[1])/1000)

                #try to download actual URL
                #download url through http not https
                driver.get(nextlink.replace("https://", "http://"))
                print("downloaded url: ", nextlink)
                
                #parse next page
                temp = self.getlinks(selector,driver.page_source.encode('utf8'))
                if temp:
                    nextlink = temp[0]
                else:
                    break
                
    #-------------------------------------
    def createThread(self, mode, selectors, level):
        import virtualbrowser
        
        proxy = self.proxies.pop()
        try: 
            driver = virtualbrowser.createChromeMachine(proxy)
            if mode=='p':
                self.paggingstrategy(selectors, driver, level)
            if mode=='n':
                self.nextstrategy(selectors, driver, level)
            if mode=='c':
                self.downloadcontent(selectors, driver, level)
        except Exception as e:
                print(e)
                print("blocked: " + proxy)
                
                driver.quit()
                
                proxy = self.proxies.pop()
                if not proxy:
                    print("we ran out of proxies")
    #-----------------------------------
    def createThreadExp(self, mode, selectors, level):
        import virtualbrowser
        
        driver = virtualbrowser.createChromeMachine("127.0.0.1")
        if mode=='p':
            self.paggingstrategy(selectors, driver, level)
        if mode=='n':
            self.nextstrategy(selectors, driver, level)
        if mode=='c':
            self.downloadcontent(selectors, driver, level)
        driver.quit()
    #-----------------------------------
    #start the scraping process
    #TODO
    #pagination with ajax
    #nextstrategy with popups
    #pagination with loadmore
    #loading more while scrolling

    def start(self):
        #harvest links to be scraped with config json logic
        for i in range(0,len(self.parsetree)):
            self.createThreadExp(self.parsetree[i][0], self.parsetree[i][1], i)

        #download content with
        self.createThreadExp('c', self.contentselectors, len(self.parsetree))

        return self.results
#-------------------------------------------------
