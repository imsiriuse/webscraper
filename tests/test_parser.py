from webscraper.parser import DbParser
from webscraper.entry import Entry
from tmu.links import readfiles
import pytest


@pytest.fixture
def config():
    recipe = [
        Entry(
            name="category",
            selector=".bredcrumbs-section"
        ),
        Entry(
            name="title",
            selector=".recipe-hed"
        ),
        Entry(
            name="description",
            selector=".recipe-introduction"
        ),
        Entry(
            name="calories",
            selector=".cal-per-serv-amount",
            maxlength="10"
        ),
        Entry(
            name="yields",
            selector=".yields-amount",
            maxlength="10"
        ),
        Entry(
            name="cooktime",
            selector=".cook-time-amount",
            maxlength="10"
        ),
        Entry(
            name="totaltime",
            selector=".total-time-amount",
            maxlength="10"
        ),
        Entry(
            name="ingredients",
            selector=".ingredients-body"
        ),
        Entry(
            name="directions",
            selector=".direction-lists"
        ),
        Entry(
            name="diresjkhdsfkj",
            selector=".directioasidhadn-lists"
        ),
        Entry(
            name="diresjkhdsfkj",
            selector=".directioasidhadn-lists",
            maxlength="50"
        )
    ]
    pytest.parser = DbParser(entries=recipe, name="recipe")


def test_dbconnect(config):
    try:
        pytest.parser.dbconnect(
            host="46.36.41.120",
            user="parser",
            dbname="parser",
            password="maxim23.error"
        )
    except Exception as e:
        print(e)
        assert False
    finally:
        pytest.parser.dbdisconnect()
    assert True


def test_inittable(config):
    try:
        pytest.parser.dbconnect(
            host="46.36.41.120",
            user="parser",
            dbname="parser",
            password="maxim23.error"
        )
        pytest.parser.inittable()

        cursor = pytest.parser.dbconnection.cursor()
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name=\'recipe\';")
        columns = cursor.fetchall()
        for entry in pytest.parser.entries:
            if (entry.name,) not in columns:
                assert False
        cursor.close()

    except Exception as e:
        print(e)
        assert False
    finally:
        pytest.parser.dbdisconnect()
    assert True


def test_parsehtml():
    try:
        contents = readfiles("data/html-rawdata")

        result = parser.parsehtml(contents[0])

        print(result)

    except Exception as e:
        print(e)
        assert False
    assert True
