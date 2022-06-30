import webscraper
import config as CFG
from machine import FirefoxMachine

if __name__ == '__main__':

    # config = CFG.Config("https://localhost:4321/test1/")
    # scraper = webscraper.Scraper(config)
    # scraper.start()

    for i in range(1):
        machine = FirefoxMachine(windowsize="1024,768")
        machine.loadurl("http://localhost:4321/test1/", timeout=1000)
        machine.clickon(".browse-category-wrap")
        machine.clicklink("http://localhost:4321/test1/product-category/core-neo/")
        machine.clicklink("http://localhost:4321/test1/product-category/core-neo/page/2/")
        machine.clicklink("http://localhost:4321/test1/product/mens-adidas-running-asweerun-shoes-2/")
        print(machine.driver.current_url)
        machine.goback(3)
        print(machine.driver.current_url)
        machine.driver.quit()


