from firefoxmachine import FirefoxMachine
from selenium.webdriver.common.by import By

def test_loadurl():
    machine = FirefoxMachine(windowsize="1024,768")
    try:
        machine.loadurl("https://www.inrightplace.com/testing/")
        if machine.driver.current_url != "https://www.inrightplace.com/testing/":
            assert False
    except:
        assert False
    finally:
        machine.driver.quit()
    assert True

def test_ishoneypot():
    machine = FirefoxMachine(windowsize="1024,768")
    try:
        machine.loadurl("https://www.inrightplace.com/testing/index.php/test-page/")

        selector = "p#displaynone > a" + '[href*="' + "https://www.inrightplace.com/testing/index.php/product-category/core-neo/" + '"]'
        element = machine.driver.find_element(By.CSS_SELECTOR, selector)
        if machine.ishoneypot(element):
            assert False

        selector = "p#opacity0 > a" + '[href*="' + "https://www.inrightplace.com/testing/index.php/product-category/originals/" + '"]'
        element = machine.driver.find_element(By.CSS_SELECTOR, selector)
        if machine.ishoneypot(element):
            assert False
    except:
        assert False
    finally:
        machine.driver.quit()
    assert True


def test_clickon():
    machine = FirefoxMachine(windowsize="1024,768")
    try:
        machine.loadurl("https://www.inrightplace.com/testing/")
        selector = ".browse-category-wrap"
        machine.clickon(selector)
        element = machine.driver.find_element(By.CSS_SELECTOR, selector)
        if not element.is_displayed():
            assert False
    except:
        assert False
    finally:
        machine.driver.quit()
    assert True

def test_clicklink():
    machine = FirefoxMachine(windowsize="1024,768")
    try:
        machine.loadurl("https://www.inrightplace.com/testing/")
        machine.clickon(".browse-category-wrap")
        machine.clicklink( "https://www.inrightplace.com/testing/index.php/cart/", ".page_item a")
        if "https://www.inrightplace.com/testing/index.php/cart/" != machine.driver.current_url:
            assert False
    except:
        assert False
    finally:
        machine.driver.quit()


def test_goback():
    machine = FirefoxMachine(windowsize="1024,768")
    try:
        machine.loadurl("https://www.inrightplace.com/testing/")
        machine.clickon(".browse-category-wrap")
        machine.clicklink("https://www.inrightplace.com/testing/product-category/core-neo/", ".categorylist a")
        machine.clicklink("https://www.inrightplace.com/testing/product-category/core-neo/page/2/", "a.page-numbers")
        machine.clicklink("http://localhost:4321/test1/product/mens-adidas-running-asweerun-shoes-2/", "a.woocommerce-loop-product__link")
        machine.goback(3)
        if "https://www.inrightplace.com/testing/" != machine.driver.current_url:
            assert False
    except:
        assert False
    finally:
        machine.driver.quit()
    assert False
