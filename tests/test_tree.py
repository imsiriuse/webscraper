import pytest
from webscraper.tree import *
        
def test_children():
    class TTree(Tree):
        def __init__(self, name: str):
            self.name: str = name
       
    def __repr__(self) -> str:
        return name

    a = TTree("a")
    print(a.name)
    
