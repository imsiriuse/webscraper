from models.ingredients.model import IngredientsTagger
from tmu.inout import *
import pytest


@pytest.fixture
def config():
    pytest.parser = IngredientsTagger(table=loadcsv(filename="data/input.csv")["content"][0:10])


def test_printdict(config):
    print("")
    try:
        parser = pytest.parser

        print(str(parser))

    except Exception as e:
        print(e)
        assert False
    assert True
