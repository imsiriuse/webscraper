from tmu.links import *


def test_readfiles():
    try:
        contents = readfiles("data/html-rawdata")

        if len(contents) != 100:
            assert False
    except Exception as e:
        print(e)
        assert False
    assert True


def test_getsitemaplinks():

    url = "https://www.allrecipes.com/"

    try:
        getsitemaplinks(url)
    except Exception as e:
        print(e)
        assert False

    assert True


def test_batchdownload():
    try:
        links = ["https://www.allrecipes.com/article/moms-simple-trick-ooey-gooey-brownies/",
                 "https://www.allrecipes.com/article/cavemen-eat-cupcakes-paleo-breakfast-muffins/",
                 "https://www.allrecipes.com/article/popular-cookies-in-us-cities/"]
        batchdownload(lines=links, resdir="D:/data-mining/todo/allrecipes.com/rawdata", timeout=5)

        if links:
            assert False

    except Exception as e:
        print(e)
        assert False
    assert True
