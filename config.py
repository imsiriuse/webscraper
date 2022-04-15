import validatejson
import json

# loading config file
with open('config-data.json', 'r') as json_file:
    CONFIG = json.load(json_file)
    json_file.close()

validatejson.configvalidation(CONFIG)
