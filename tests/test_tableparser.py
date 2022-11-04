from tmu.tableparser import Tableparser


def test_loadcsv():
    try:
        parser = Tableparser()
        parser.loadcsv(filename="data/ingredients.csv")
        print(parser.table)
    except Exception as e:
        print(e)
        assert False
    assert True


def test_loadfromdb():
    try:
        parser = Tableparser()
        parser.loadfromdb(
            tablename="ingredients",
            host="46.36.41.120",
            user="parser",
            dbname="recipes",
            pwd="maxim23.error"
        )
        print(parser.table)
    except Exception as e:
        print(e)
        assert False
    assert True

