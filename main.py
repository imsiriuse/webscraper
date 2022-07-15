# import webscraper
# import config as CFG
from machine import FirefoxMachine

if __name__ == '__main__':

    # config = CFG.Config("https://localhost:4321/test1/")
    # scraper = webscraper.Scraper(config)
    # scraper.start()
    #
    # CLICKING TEST
    #
    # machine = FirefoxMachine(windowsize="1024,768")
    # try:
    #     machine.loadurl("http://localhost:4321/test1/")
    #     machine.clickon(".browse-category-wrap")
    #     print(machine.driver.current_url)
    #     machine.clicklink("http://localhost:4321/test1/product-category/core-neo/", ".categorylist a")
    #     print(machine.driver.current_url)
    #     machine.clicklink("http://localhost:4321/test1/product-category/core-neo/page/2/", "a.page-numbers")
    #     print(machine.driver.current_url)
    #     machine.clicklink("http://localhost:4321/test1/product/mens-adidas-running-asweerun-shoes-2/",
    #         "a.woocommerce-loop-product__link")
    #     print(machine.driver.current_url)
    #     machine.goback(3)
    #     print(machine.driver.current_url)
    # finally:
    #     machine.driver.quit()
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
