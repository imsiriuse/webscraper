# unstructured data parser
# made for manual entity recognition tagging
# of text data not structured into sentences
# using only english trained pipeline

import re
import en_core_web_trf


class Token:
    def __init__(self, string, tag=None, paragraphs=[], num=1):
        self.string = string
        self.tag = tag
        self.paragraphs = paragraphs
        self.num = num

    def __str__(self):
        return self.string + " tag: " + str(self.tag) + " : " + str(self.paragraphs) + " : " + str(self.num) + "\n"


class Udparser:
    def __init__(self, table):
        self.dict = {}
        self.paragraphs = []
        nlp = en_core_web_trf.load()

        for row in table:
            self.paragraphs.append(nlp(row))

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
