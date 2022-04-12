import webscraper
import config

if __name__ == '__main__':

    # get list of ip adresses of proxy servers
    # config["proxies"] = proxdownload.getList()

    # start of scraping process
    scraper = webscraper.Scraper(config.CONFIG)
    scraper.start()
    #results = scraper.getResults()

    # saving results table as csv
    #with open("results.csv", "w", newline='', encoding='utf-8') as results_file:
    #    csvWriter = csv.writer(results_file, delimiter=';')
    #    csvWriter.writerows(results)

