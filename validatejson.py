import json
from jsonschema import validate


def configvalidation(config):
    # loading validation scheme of config file
    with open('configuration-scheme.json', 'r') as json_file:
        schema = json.load(json_file)
        json_file.close()

    # validation of config file through scheme
    validate(config, schema)

