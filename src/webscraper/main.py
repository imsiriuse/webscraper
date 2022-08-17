import webscraper
import config as CFG
import timeout


if __name__ == '__main__':
    config = CFG.Config("https://inrightplace.com/testing/")
    config.windowsizes = ["1024,768"]
    config.timeout = timeout.Timeout(max=5, min=1, step=1)
    config.headless = False

    scraper = webscraper.Scraper(config)
    scraper.start()
