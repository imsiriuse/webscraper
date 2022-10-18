from webscraper.urlutils import Url


def test_url():
    urlmain = Url("http://flyandlure.org/articles/fly_fishing/fly_fishing_diary_july_2020?q=word&b=something#anchor")

    try:
        if urlmain != Url("http://flyandlure.org/articles/fly_fishing/fly_fishing_diary_july_2020?q=word&b=something#anchor"):
            assert False
        if urlmain != Url("https://flyandlure.org/articles/fly_fishing/fly_fishing_diary_july_2020?q=word&b=something#anchor"):
            assert False
        if urlmain == Url("https://blabla.org/articles/fly_fishing/fly_fishing_diary_july_2020?q=word&b=something#anchor"):
            assert False
        if urlmain == Url("https://flyandlure.org?q=word&b=something#anchor"):
            assert False
        if urlmain == Url("https://flyandlure.org/?q=word&b=something#anchor"):
            assert False
        if urlmain == Url("flyandlure.org?q=word&b=something#anchor"):
            assert False
        if urlmain == Url("flyandlure.org/?q=word&b=something#anchor"):
            assert False
        if urlmain == Url("https://flyandlure.org/artiy_fishing_diary_july_2020?q=word&b=something#anchor"):
            assert False
        if urlmain != Url("flyandlure.org/articles/fly_fishing/fly_fishing_diary_july_2020?q=word&b=something#anchor"):
            assert False
        if urlmain != Url("www.flyandlure.org/articles/fly_fishing/fly_fishing_diary_july_2020?q=word&b=something#anchor"):
            assert False
        if urlmain != Url("https://www.flyandlure.org/articles/fly_fishing/fly_fishing_diary_july_2020?q=word&b=something#anchor"):
            assert False
        if urlmain != Url("http://flyandlure.org/articles/fly_fishing/fly_fishing_diary_july_2020?q=word&b=something"):
            assert False
        if urlmain != Url("http://flyandlure.org/articles/fly_fishing/fly_fishing_diary_july_2020?q=word&c=something"):
            assert False
        if urlmain != Url("http://flyandlure.org/articles/fly_fishing/fly_fishing_diary_july_2020"):
            assert False
        if urlmain != Url("flyandlure.org/articles/fly_fishing/fly_fishing_diary_july_2020"):
            assert False
        if urlmain != "http://flyandlure.org/articles/fly_fishing/fly_fishing_diary_july_2020?q=word&b=something#anchor":
            assert False
        if urlmain != "https://flyandlure.org/articles/fly_fishing/fly_fishing_diary_july_2020?q=word&b=something#anchor":
            assert False
        if urlmain == "https://blabla.org/articles/fly_fishing/fly_fishing_diary_july_2020?q=word&b=something#anchor":
            assert False
        if urlmain == "https://flyandlure.org/artiy_fishing_diary_july_2020?q=word&b=something#anchor":
            assert False
        if urlmain != "flyandlure.org/articles/fly_fishing/fly_fishing_diary_july_2020?q=word&b=something#anchor":
            assert False
        if urlmain != "www.flyandlure.org/articles/fly_fishing/fly_fishing_diary_july_2020?q=word&b=something#anchor":
            assert False
        if urlmain != "http://flyandlure.org/articles/fly_fishing/fly_fishing_diary_july_2020?q=word&b=something":
            assert False
        if urlmain != "http://flyandlure.org/articles/fly_fishing/fly_fishing_diary_july_2020?q=word&c=something":
            assert False
        if urlmain != "http://flyandlure.org/articles/fly_fishing/fly_fishing_diary_july_2020":
            assert False
        if urlmain != "flyandlure.org/articles/fly_fishing/fly_fishing_diary_july_2020":
            assert False
    except NotImplementedError as e:
        print(e)
        assert False

    assert True
