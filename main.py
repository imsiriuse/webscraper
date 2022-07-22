import webscraper
import config as CFG


if __name__ == '__main__':
    config = CFG.Config("https://localhost:4321/test1/")
    scraper = webscraper.Scraper(config)
    scraper.start()

