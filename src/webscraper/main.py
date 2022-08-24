from webscraper.webscraper import Scraper
import webscraper.config as CFG
from webscraper.timeout import Timeout


if __name__ == '__main__':
    config = CFG.Config("https://inrightplace.com/testing/")
    config.windowsizes = ["1024,768"]
    config.timeout = Timeout(max=5, min=1, step=1)
    config.headless = False

    scraper = Scraper(config)
    scraper.start()
