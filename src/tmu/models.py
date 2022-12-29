import spacy
from tmu.inout import *


def main():
    table = loadcsv(filename="data/input.csv")
    print(table)

