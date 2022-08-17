import pytest
import webscraper

class TestTree(Tree):
    def __init__(self, name: str):
        self.name: str = name
       
    def __repr__(self) -> str:
        return name
        
def test_children():
    a = TestTree("a")
    print(a.name)
    
