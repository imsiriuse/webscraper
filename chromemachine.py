from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from machine import Machine


class ChromeMachine(Machine):

    def __init__(self, proxy="127.0.0.1", windowsize="2048,1080"):
        self.proxy = proxy
        self.windowsize = windowsize

        chrome_options = Options()

        # setting proxy server for chrome
        # chrome_options.add_argument("--proxy-server=" + proxy)

        # optimization settings
        prefs = {
            'profile.default_content_setting_values': {
                'cookies': 2,
                'images': 2,
                'plugins': 2,
                'popups': 2,
                'geolocation': 2,
                'notifications': 2,
                'auto_select_certificate': 2,
                'fullscreen': 2,
                'mouselock': 2,
                'mixed_script': 2,
                'media_stream': 2,
                'media_stream_mic': 2,
                'media_stream_camera': 2,
                'protocol_handlers': 2,
                'ppapi_broker': 2,
                'automatic_downloads': 2,
                'midi_sysex': 2,
                'push_messaging': 2,
                'ssl_cert_decisions': 2,
                'metro_switch_to_desktop': 2,
                'protected_media_identifier': 2,
                'app_banner': 2,
                'site_engagement': 2,
                'durable_storage': 2
            }
        }

        chrome_options.add_experimental_option('prefs', prefs)

        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # disable console
        chrome_options.add_argument("--log-level=3")

        # to be run as headless (do not open window)
        # chrome_options.add_argument("--headless")

        # set size of browser window
        chrome_options.add_argument("--window-size=" + windowsize)

        # define random user agent from pool
        chrome_options.add_argument("--user-agent=" + UserAgent().random)

        # creating instance of chrome browser
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def disablecss(self):
        pass

    def showelement(self, firstelement):
        action = ActionChains(self.driver)

        element = firstelement
        while element:
            element = element.find_element(by=By.XPATH, value="..")
            if element.is_displayed():
                action.move_to_element(element).click().perform()

                if firstelement.is_displayed():
                    return True
        return False

    def clicklink(self, url):
        # physically click on the link in browser
        actions = ActionChains(self.driver)

        # wait max 5 second for element to be loaded
        try:
            WebDriverWait(self.driver, 5).until(
                expected_conditions.presence_of_element_located((By.CSS_SELECTOR, 'a[href="' + url + '"]')))
        except TimeoutException:
            print("Element can't be located")
            return None

        elements = self.driver.find_elements(By.CSS_SELECTOR, 'a[href="' + url + '"]')

        # pick up that element which is visible
        for element in elements:
            if not element.is_displayed():
                # try to make element visible
                if self.showelement(element):
                    actions.move_to_element(element).click().perform()
                    return True
            else:
                actions.move_to_element(element).click().perform()
                return True

        return None


