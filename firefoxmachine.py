from time import sleep
from machine import Machine
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from fake_useragent import UserAgent
from config import Timeout
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException, WebDriverException


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
        sleep(self.timeout.getrandom())

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

        sleep(self.timeout.getrandom())

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

        sleep(self.timeout.getrandom())
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

            sleep(self.timeout.getrandom())

            self.driver.back()

            self.waituntil(
                expected_conditions.url_changes(url=oldurl)
            )

            self.waituntil(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
