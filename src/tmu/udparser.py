# unstructured data parser
# made for manual entity recognition tagging
# of text data not structured into sentences
# using only english trained pipeline

import en_core_web_sm


class Token:
    def __init__(self, string, tag=None, paragraphs=None, num=1):
        if paragraphs is None:
            paragraphs = []
        self.string = string
        self.tag = tag
        self.paragraphs = paragraphs
        self.num = num

    def __str__(self):
        return self.string + " tag: " + str(self.tag) + " : " + str(self.paragraphs) + " : " + str(self.num) + "\n"


class Udparser:
    def __init__(self, table):
        self.dict = set()

        self.nlp = en_core_web_sm.load()
        self.nlp.select_pipes(disable=["tagger", "parser", "attribute_ruler", "ner"])
        self.docs = list(self.nlp.pipe(table))

    def __str__(self):
        res = "PARAGRAPHS\n"
        for doc in self.docs:
            for token in doc:
                res = res + str(token) + ", "
            res = res + "\n"
        res = res + "DICT\n"
        res = res + str(self.dict)
        return res

    def printdict(self):
        pass

    def splittoken(self, oldtoken, r="\\s+"):
        pass

    def tolowercase(self):
        pass

    def grep(self, r):
        pass

    def strip(self, regex):
        pass
