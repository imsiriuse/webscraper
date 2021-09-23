import json
import webscraper
import proxdownload
import importlib
import csv

importlib.reload(webscraper)

with open('config-data.json') as json_file:
    config = json.load(json_file)
    json_file.close()

#config["proxies"] = proxdownload.getList()

scraper = webscraper.Scraper(config)
results = scraper.start()

for i in range(0,len(results)):
    for j in range(0,len(results[i])):
        results[i][j] = results[i][j].replace(";", ",")

results = [*zip(*results)]

with open("results.csv","w",newline='', encoding='utf-8') as results_file:
    csvWriter = csv.writer(results_file, delimiter=';')
    csvWriter.writerows(results)
