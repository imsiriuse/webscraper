from webscraper.firefoxmachine import FirefoxMachine
from selenium.webdriver.common.by import By
from webscraper.timeout import Timeout


# def test_loadurl():
#     machine = FirefoxMachine(headless=False, timeout=Timeout(max=5, min=1, step=1))
#     try:
#         oldurl = machine.driver.current_url
#         targeturl = "http://www.inrightplace.com/testing/"
#
#         machine.loadurl(targeturl)
#
#         if oldurl == machine.driver.current_url:
#             assert False
#         if machine.driver.current_url != targeturl:
#             assert False
#
#     except Exception as e:
#         print(e)
#         assert False
#     finally:
#         machine.driver.quit()
#     assert True
#
#
# def test_ishoneypot():
#     machine = FirefoxMachine(headless=False, timeout=Timeout(max=5, min=1, step=1))
#     try:
#         machine.loadurl("https://www.inrightplace.com/testing/index.php/test-page/")
#
#         selector = 'p#displaynone0 > a[href*="https://www.inrightplace.com/testing/index.php/product-category/core-neo/"]'
#         element = machine.driver.find_element(By.CSS_SELECTOR, selector)
#         if not machine.ishoneypot(element):
#             assert False
#
#         selector = 'p#opacity0 > a[href*="https://www.inrightplace.com/testing/index.php/product-category/originals/"]'
#         element = machine.driver.find_element(By.CSS_SELECTOR, selector)
#         if not machine.ishoneypot(element):
#             assert False
#
#     except Exception as e:
#         print(e)
#         assert False
#     finally:
#         machine.driver.quit()
#     assert True
#
#
# def test_openmenu():
#     machine = FirefoxMachine(headless=False, timeout=Timeout(max=5, min=1, step=1))
#     try:
#         machine.loadurl("https://www.inrightplace.com/testing/")
#
#         targetselector = '.categorylist a[href*="https://www.inrightplace.com/testing/index.php/product-category/core-neo/"'
#         menuselector = ".categorylist"
#
#         element = machine.driver.find_element(By.CSS_SELECTOR, targetselector)
#         if element.is_displayed():
#             assert False
#
#         machine.openmenu(".browse-category-wrap", menuselector)
#
#         element = machine.driver.find_element(By.CSS_SELECTOR, menuselector)
#
#         if not element.is_displayed():
#             assert False
#
#     except Exception as e:
#         print(e)
#         assert False
#     finally:
#         machine.driver.quit()
#
#
# def test_clicklink():
#     machine = FirefoxMachine(headless=False, timeout=Timeout(max=5, min=1, step=1))
#     try:
#         machine.loadurl("https://www.inrightplace.com/testing/")
#         machine.openmenu(".browse-category-wrap", ".categorylist")
#
#         targetselector = '.categorylist a[href*="https://www.inrightplace.com/testing/index.php/product-category/core-neo/"'
#         targetlink = "https://www.inrightplace.com/testing/index.php/product-category/core-neo/"
#
#         element = machine.driver.find_element(By.CSS_SELECTOR, targetselector)
#         if not element.is_displayed():
#             assert False
#
#         machine.clicklink(targetlink, ".categorylist a")
#         if targetlink != machine.driver.current_url:
#             assert False
#
#     except Exception as e:
#         print(e)
#         assert False
#     finally:
#         machine.driver.quit()
#
#
# def test_goback():
#     machine = FirefoxMachine(headless=False, timeout=Timeout(max=5, min=1, step=1))
#     try:
#         baseurl = "https://www.inrightplace.com/testing/"
#         machine.loadurl(baseurl)
#         machine.openmenu(".browse-category-wrap", ".categorylist")
#
#         machine.clicklink(
#             "https://www.inrightplace.com/testing/index.php/product-category/core-neo/",
#             ".categorylist a")
#         machine.clicklink(
#             "https://www.inrightplace.com/testing/index.php/product-category/core-neo/page/2/",
#             "a.page-numbers")
#         machine.clicklink(
#             "https://www.inrightplace.com/testing/index.php/product/mens-adidas-running-asweerun-shoes-3/",
#             ".woocommerce-loop-product__title a")
#
#         machine.goback(3)
#
#         if baseurl != machine.driver.current_url:
#             assert False
#     except Exception as e:
#         print(e)
#         assert False
#     finally:
#         machine.driver.quit()
#     assert True
#
