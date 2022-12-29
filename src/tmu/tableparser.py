import re


class Token:
    def __init__(self, string, tag=None, paragraphs=[], num=1):
        self.string = string
        self.tag = tag
        self.paragraphs = paragraphs
        self.num = num

    def __str__(self):
        return self.string + " tag: " + str(self.tag) + " : " + str(self.paragraphs) + " : " + str(self.num) + "\n"


class Tableparser:
    def __init__(self, table):
        self.dict = {}
        self.paragraphs = []

        for row in table:
            if row in self.dict:
                token = self.dict[row]
            else:
                token = Token(row)
                self.dict[row] = token

            paragraph = [token]
            self.paragraphs.append(paragraph)
            token.paragraphs.append(paragraph)

    def printdict(self):
        for row in sorted(list(self.dict)):
            print("[" +row +"]=" + str(self.dict[row]))

    def arrayinsert(self, paragraph, what, where):
        paragraph[paragraph.index(where):paragraph.index(where)] = what
        paragraph.remove(where)

    def splittoken(self, regex, oldtoken):
        splits = regex.split(oldtoken.string)
        newtokens = []
        for split in splits:
            if split in self.dict:
                newtoken = self.dict[split]
            else:
                newtoken = Token(split, oldtoken.tag, oldtoken.paragraphs, oldtoken.num)
            newtokens.append(newtoken)
        return newtokens

    def tokenize(self, r='\s+'):
        regex = re.compile(r)

        newtokens = []
        oldtokens = []
        for key, oldtoken in self.dict.items():
            if not regex.search(key):
                continue
            splits = self.splittoken(regex, oldtoken)
            for oldparagraph in oldtoken.paragraphs:
                print(oldparagraph + ": " + splits + "; " + oldtoken.string)
                self.arrayinsert(oldparagraph, splits, oldtoken)
            newtokens = newtokens + splits
            oldtokens = oldtokens + oldtoken

        for newtoken in newtokens:
            self.dict[newtoken.string] = newtoken
        for oldtoken in oldtokens:
            del self.dict[oldtoken.string]

    def tolowercase(self):
        pass

    def grep(self, r):
        pass

    def strip(self, regex):
        pass


# parser = Tableparser(loadcsv()["content"])
parser = Tableparser(["one", "two three", "four"])
# parser.tokenize()
# parser.replacechars("!%")
# parser.printdict()
