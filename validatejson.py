import json
from jsonschema import validate

def configvalidation(config):
    #loading validation scheme of config file
    with open('configuration-scheme.json', 'r') as json_file:
        schema = json.load(json_file)
        json_file.close()
    
    #validation of config file through scheme
    validate(config, schema)
    
    if not "contentselectors" in config:
        raise Exception("There are no selectors to harvest content")

    #validation of sizes of arrays and pointers in parse tree
    for node in config["parsetree"]:
        if "contents" in node:
            for i in range(1, len(node["contents"])-1):
                if node["contents"][i] > len(config["contentselectors"])-1:
                    raise Exception("Node wants to use non exist content selector")
 
