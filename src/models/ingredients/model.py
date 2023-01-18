import en_core_web_sm
from tmu.inout import *


class IngredientsTagger:
    def __init__(self, table):
        self.nlp = en_core_web_sm.load()
        self.nlp.select_pipes(disable=["tagger", "parser", "attribute_ruler", "ner"])
        self.docs = list(self.nlp.pipe(table))

    def start(self):
        pass

    def __str__(self):
        result = str(self.nlp.pipe_names) + "\n"
        result += str(self.docs)
        return result


def run():
    tagger = IngredientsTagger(table=loadcsv(filename="data/input.csv")["content"][0:10])
    tagger.start()
