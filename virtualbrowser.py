from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import traceback

def createChromeMachine(proxy="127.0.0.1", windowsize="1920,1080"):
    print("opening chrome proxy: " + proxy)
    chrome_options = Options()

    # setting proxy server for chrome
    # chrome_options.add_argument("--proxy-server=" + proxy)

    # optimization settings
    prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'javascript': 2, 'plugins': 2,
                                                        'popups': 2, 'geolocation': 2, 'notifications': 2,
                                                        'auto_select_certificate': 2, 'fullscreen': 2, 'mouselock': 2,
                                                        'mixed_script': 2, 'media_stream': 2, 'media_stream_mic': 2,
                                                        'media_stream_camera': 2, 'protocol_handlers': 2,
                                                        'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                                                        'push_messaging': 2, 'ssl_cert_decisions': 2,
                                                        'metro_switch_to_desktop': 2, 'protected_media_identifier': 2,
                                                        'app_banner': 2, 'site_engagement': 2, 'durable_storage': 2}}

    #chrome_options.add_experimental_option('prefs', prefs)

    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # disable console
    chrome_options.add_argument("--log-level=3")

    # to be run as headless (do not open window)
    chrome_options.add_argument("--headless")

    # set size of browser window
    chrome_options.add_argument("--window-size=" + windowsize)

    # define random user agent from pool
    chrome_options.add_argument("--user-agent=" + UserAgent().random)

    # creating instance of chrome browser
    driver = webdriver.Chrome(options=chrome_options)

    return driver

def test(driver):
    try:
        driver.get("http://localhost:4321/test1/")
        loadnewpage(driver, "http://localhost:4321/test1/product-category/core-neo/")

        print(driver.current_url)
    except:
        traceback.print_exc()
    finally:
        driver.quit()


def loadnewpage(driver, url):
    # physically click on the link in browser
    actions = ActionChains(driver)

    elements = WebDriverWait(driver, 10).until(lambda x: x.find_elements(By.CSS_SELECTOR, 'a[href="' + url + '"]'))

    for element in elements:
        #check if element is visible
        if element.is_displayed():
            actions.move_to_element(element)
            actions.click(element)
            actions.perform()
            break


