import webscraper

if __name__ == '__main__':

    # get list of ip addresses of proxy servers
    # config["proxies"] = proxdownload.getList()

    # start of scraping process
    scraper = webscraper.Scraper()
    scraper.start()
    # results = scraper.getResults()

    # saving result table as csv
    # with open("results.csv", "w", newline='', encoding='utf-8') as results_file:
    #    csvWriter = csv.writer(results_file, delimiter=';')
    #    csvWriter.writerows(results)
