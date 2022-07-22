# import webscraper
# import config as CFG
from firefoxmachine import FirefoxMachine

if __name__ == '__main__':

    # config = CFG.Config("https://localhost:4321/test1/")
    # scraper = webscraper.Scraper(config)
    # scraper.start()
    #

    #
    # HONEYPOT TEST
    #
    machine = FirefoxMachine(windowsize="1024,768", honeypots=True)
    try:
        machine.loadurl("http://localhost:4321/test1/testing-page/")
        print(machine.driver.current_url)
        machine.clicklink("http://localhost:4321/test1/product-category/originals/", "p#displaynone > a")
        print(machine.driver.current_url)
        machine.clicklink("http://localhost:4321/test1/product-category/core-neo/", "p#opacity0 > a")
        print(machine.driver.current_url)
    finally:
        machine.driver.quit()
