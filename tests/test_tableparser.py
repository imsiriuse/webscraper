from tmu.tableparser import *
import pytest


@pytest.fixture
def config():
    pytest.table = loadfromdb(
        tablename="ingredients",
        host="46.36.41.120",
        user="parser",
        dbname="recipes",
        pwd="maxim23.error"
    )


def test_loadcsv():
    try:
        loadcsv(filename="data/ingredients.csv")
    except Exception as e:
        print(e)
        assert False
    assert True


def test_loadfromdb():
    try:
        loadfromdb(
            tablename="ingredients",
            host="46.36.41.120",
            user="parser",
            dbname="recipes",
            pwd="maxim23.error"
        )
    except Exception as e:
        print(e)
        assert False
    assert True
