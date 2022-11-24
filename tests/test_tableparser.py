from tmu.tableparser import Tableparser
import pytest


@pytest.fixture
def config():
    pytest.tableparser = Tableparser(filename="data/ingredients.csv")


def test_loaddbtable(config):
    try:
        pytest.tableparser.loaddbtable(
            tablename="ingredients",
            host="46.36.41.120",
            user="parser",
            dbname="recipes",
            pwd="maxim23.error"
        )
        print(len(pytest.tableparser.table))
    except Exception as e:
        print(e)
        assert False
    assert True
