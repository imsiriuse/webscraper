from tmu.parsing import readfiles
from tmu.parsing import Entry
from tmu.parsing import ArrayEntry
from tmu.parsing import parsehtml


def test_readfiles():
    try:
        contents = readfiles("tests/data/html-rawdata")

        if len(contents) != 100:
            assert False
    except Exception as e:
        print(e)
        assert False
    assert True


def test_parsehtml():
    try:
        contents = readfiles("tests/data/html-rawdata")

        recipe = [
            Entry(
                name="category",
                selector=".bredcrumbs-section"
            ),
            Entry(
                name="name",
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
            ArrayEntry(
                name="ingredients",
                selector=".ingredients-body"
            ),
            ArrayEntry(
                name="directions",
                selector=".direction-lists"
            )
        ]

        result = parsehtml(recipe, contents[0])

        print(result)

    except Exception as e:
        print(e)
        assert False
    assert True
