from webscraper.parser import DbParser
from webscraper.entry import Entry
from tmu.links import readfiles

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

parser = DbParser(entries=recipe, name="recipe")


def test_dbconnect():
    try:
        parser.dbconnect(
            host="46.36.41.120",
            user="miso",
            dbname="recipes",
            password="Raci2.we"
        )

    except Exception as e:
        print(e)
        assert False
    finally:
        parser.dbdisconnect()
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
