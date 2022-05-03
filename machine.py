class Machine:
    def __init__(self, proxy="127.0.0.1", windowsize="2048,1080"):
        self.proxy = proxy
        self.windowsize = windowsize
        self.driver = None

    def wait(self, time):
        self.driver.implicitly_wait(time)

    def loadurl(self, url):
        self.driver.get(url)

