from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from config import Timeout
from selenium.webdriver.support.ui import WebDriverWait


class Machine:
    def __init__(self):
        self.proxy = None
        self.windowsize = None
        self.driver = None
        self.timeout = None
        self.wait = None
        self.honeypots = None

    def waituntil(self, expression):
        try:
            self.wait.until(expression)
        except TimeoutException:
            print("Element can't be loaded, waited: " + str(self.timeout.max) + "sec, skipping...")
            return False
        except WebDriverException as e:
            print(e)
            return False

        return True

    def loadurl(self, url, https=False):
        time.sleep(self.timeout.getrandom())

        if not https:
            url = url.replace("https://", "http://")
        else:
            url = url.replace("http://", "https://")

        self.driver.get(url)

        self.waituntil(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

    def gethtml(self, encoding="utf8"):
        return self.driver.page_source.encode(encoding)

    def getcss(self, element):
        styles = self.driver.execute_script(
            'var items = {};' +
            'var compsty = getComputedStyle(arguments[0]);' +
            'var len = compsty.length;' +
            'for (index = 0; index < len; index++)' +
            '{items [compsty[index]] = compsty.getPropertyValue(compsty[index])};' +
            'return items;', element)

        return styles

    def ishoneypot(self, element):
        if self.honeypots:
            styles = self.getcss(element)
            if styles["display"] == "none":
                return True
            if styles["opacity"] == "0":
                return True
        else:
            return element.is_displayed()

        return False

    def clickon(self, selector):
        self.waituntil(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, selector))
        )

        action = ActionChains(self.driver)
        element = self.driver.find_element(By.CSS_SELECTOR, selector)

        if self.ishoneypot(element):
            print("Element is honeypot")
            return False

        time.sleep(self.timeout.getrandom())

        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        action.move_to_element(element).click().perform()

    def clicklink(self, url, selector):
        selector = selector + '[href*="' + url + '"]'
        oldurl = self.driver.current_url

        self.waituntil(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, selector))
        )

        action = ActionChains(self.driver)
        element = self.driver.find_element(By.CSS_SELECTOR, selector)

        if self.ishoneypot(element):
            print("Element is honeypot")
            return False

        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(self.timeout.getrandom())
        action.move_to_element(element).click().perform()

        self.waituntil(
            expected_conditions.url_changes(url=oldurl)
        )

        self.waituntil(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

    def goback(self, steps=1):
        for i in range(steps):
            oldurl = self.driver.current_url

            time.sleep(self.timeout.getrandom())

            self.driver.back()

            self.waituntil(
                expected_conditions.url_changes(url=oldurl)
            )

            self.waituntil(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )


class ChromeMachine(Machine):
    def __init__(self, proxy="127.0.0.1", windowsize="2048,1080"):
        super().__init__(proxy, windowsize)

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
        chrome_options.add_argument("--headless")

        # set size of browser window
        chrome_options.add_argument("--window-size=" + windowsize)

        # define random user agent from pool
        chrome_options.add_argument("--user-agent=" + UserAgent().random)

        # creating instance of Chrome browser
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )


class FirefoxMachine(Machine):
    def __init__(self, proxy="127.0.0.1", windowsize="2048,1080", timeout=Timeout(), honeypots=False):
        super().__init__()

        self.proxy = proxy
        self.windowsize = windowsize
        self.timeout = timeout
        self.honeypots = honeypots

        options = FirefoxOptions()
        profile = webdriver.FirefoxProfile()

        # options.add_argument("--headless")
        options.add_argument("--width=" + self.windowsize.split(",")[0])
        options.add_argument("--height=" + self.windowsize.split(",")[1])

        profile.set_preference("general.useragent.override", UserAgent().random)  # usage of rotating user agents

        profile.set_preference("network.http.pipelining", True)  # enable proxies
        profile.set_preference("network.http.proxy.pipelining", True)   # enable proxies

        profile.set_preference("browser.cache.memory.capacity", 65536)  # Increase the cache capacity.
        profile.set_preference("browser.display.use_document_fonts", 0)  # Don't load document fonts.
        profile.set_preference("browser.shell.checkDefaultBrowser", False)

        self.driver = webdriver.Firefox(
            service=Service(GeckoDriverManager().install()),
            options=options,
            firefox_profile=profile
        )

        self.wait = WebDriverWait(driver=self.driver, timeout=self.timeout.max)
