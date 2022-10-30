from webscraper.parser import DbParser
from webscraper.entry import Entry
import pytest
import glob
import codecs

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
            selector=".ingredient-item"
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


def test_getid(config):
    try:
        pytest.parser.dbconnect()
        pytest.parser.inittables()
        cursor = pytest.parser.dbconnection.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS sldkfj(id SERIAL PRIMARY KEY, content TEXT);
            INSERT INTO sldkfj(content) VALUES(\'pcxx\');
            INSERT INTO sldkfj(content) VALUES(\'pcxx\');
            INSERT INTO sldkfj(content) VALUES(\'pcxx\');
            """)

        result = pytest.parser.getid("sldkfj", "pcxx")
        if result != 1:
            assert False
        result = pytest.parser.getid("sldkfj", "xxcp")
        if result is not None:
            assert False
        cursor.execute("DROP TABLE IF EXISTS sldkfj;")
        cursor.close()
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

        for entry in pytest.parser.entries:
            cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name=\'" + entry.name + "\';")
            columns = cursor.fetchall()
            if ("id",) not in columns:
                assert False
            if ("content",) not in columns:
                assert False
            if (pytest.parser.name + "_id",) not in columns:
                assert False

        cursor.close()

    except Exception as e:
        print(e)
        assert False
    finally:
        pytest.parser.dbdisconnect()
    assert True


def test_insertrow(config):
    try:
        pytest.parser.dbconnect()
        pytest.parser.inittables()

        filenames = glob.glob("D:/data-mining/todo/goodhousekeeping.com/rawdata/*")

        for filename in filenames:
            with codecs.open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                print("parsing: " + filename)
                pytest.parser.insertrow(f.read(), filename)
                f.close()

    except Exception as e:
        print(e)
        assert False
    finally:
        pytest.parser.dbdisconnect()
    assert True
