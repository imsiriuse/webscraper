from tmu.udparser import Udparser
from tmu.inout import *
import pytest


@pytest.fixture
def config():
    pytest.parser = Udparser(loadcsv(filename="data/input.csv")["content"][0:10])


def test_printdict(config):
    print("")
    try:
        parser = pytest.parser

        parser.printdict()

    except Exception as e:
        print(e)
        assert False
    assert True
