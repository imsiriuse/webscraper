import webscraper
import json
#import proxdownload
#import csv
import validatejson

if __name__ == '__main__':
    # loading config file
    with open('config-data.json', 'r') as json_file:
        config = json.load(json_file)
        json_file.close()

    validatejson.configvalidation(config)

    # get list of ip adresses of proxy servers
    # config["proxies"] = proxdownload.getList()

    # start of scraping process
    scraper = webscraper.Scraper(config)
    scraper.start()
    #results = scraper.getResults()

    # saving results table as csv
    #with open("results.csv", "w", newline='', encoding='utf-8') as results_file:
    #    csvWriter = csv.writer(results_file, delimiter=';')
    #    csvWriter.writerows(results)

