from webscraper.parser import DbParser
from webscraper.entry import Entry
import pytest
import glob


@pytest.fixture
def config():
    recipe = [
        Entry(
            name="category",
            selector=".breadcrumb > li:not(.hide_content_breadcrumbs)"
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
            selector=".cal-per-serv-amount"
        ),
        Entry(
            name="yields",
            selector=".yields-amount"
        ),
        Entry(
            name="cooktime",
            selector=".cook-time-amount"
        ),
        Entry(
            name="totaltime",
            selector=".total-time-amount"
        ),
        Entry(
            name="ingredients",
            selector=".ingredients-body"
        ),
        Entry(
            name="directions",
            selector=".direction-lists"
        )
    ]
    pytest.parser = DbParser(
        entries=recipe,
        name="recipe",
        host="46.36.41.120",
        user="parser",
        dbname="parser",
        password="maxim23.error"
    )


def test_dbconnect(config):
    try:
        pytest.parser.dbconnect()
    except Exception as e:
        print(e)
        assert False
    finally:
        pytest.parser.dbdisconnect()
    assert True


def test_inittables(config):
    try:
        pytest.parser.dbconnect()
        pytest.parser.inittables()

        cursor = pytest.parser.dbconnection.cursor()

        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name=\'" + pytest.parser.name + "\';")
        columns = cursor.fetchall()
        for entry in pytest.parser.entries:
            if (entry.name,) not in columns:
                assert False

        for entry in pytest.parser.entries:
            cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name=\'" + entry.name + "\';")
            columns = cursor.fetchall()
            if ("id",) not in columns:
                assert False
            if ("content",) not in columns:
                assert False

        cursor.close()

    except Exception as e:
        print(e)
        assert False
    finally:
        pytest.parser.dbdisconnect()
    assert True


def test_parsehtml(config):
    try:
        pytest.parser.dbconnect()
        pytest.parser.inittable()

        filenames = glob.glob("data/html-rawdata/*")

        n = len(filenames)
        contents = []
        for i in range(n):
            f = open(filenames[i], "r")
            contents.append(f.read())
            f.close()

        print("\n")
        for content in contents:
            pytest.parser.parsehtml(content)

    except Exception as e:
        print(e)
        assert False
    finally:
        pytest.parser.dbdisconnect()
    assert True
