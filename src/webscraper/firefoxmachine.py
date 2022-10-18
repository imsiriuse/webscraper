from webscraper.machine import Machine
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from fake_useragent import UserAgent
from webscraper.timeout import Timeout
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions


class FirefoxMachine(Machine):
    def __init__(
            self,
            proxy="127.0.0.1",
            windowsize="1024,768",
            timeout=Timeout(),
            honeypots=False,
            headless=True
    ):
        super().__init__()

        self.proxy = proxy
        self.windowsize = windowsize
        self.timeout = timeout
        self.honeypots = honeypots

        options = FirefoxOptions()
        profile = webdriver.FirefoxProfile()

        if headless:
            options.add_argument("--headless")

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

    def loadurl(self, url, https=False):
        # self.timeout.run()

        # TODO https/http
        # if not https:
        #     url = url.replace("https://", "http://")
        # else:
        #     url = url.replace("http://", "https://")

        self.driver.get(url)

        self.wait.until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

    def gethtml(self, encoding="utf8"):
        return self.driver.page_source.encode(encoding)

    def getcss(self, selector, property):
        self.wait.until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        element = self.driver.find_element(By.CSS_SELECTOR, selector)
        styles = self.driver.execute_script(
            'var compsty = getComputedStyle(arguments[0]);' 
            'return compsty["' + property + '"];', element
        )
        return styles

    def ishoneypot(self, element):
        if self.honeypots:
            if self.getcss(element, "display") == "none":
                return True
            if self.getcss(element, "opacity") == "0":
                return True
            if self.getcss(element, "height") == "0px":
                return True
            if self.getcss(element, "width") == "0px":
                return True
        else:
            return not element.is_displayed()

        return False

    def clickon(self, selector):
        self.wait.until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, selector))
        )

        action = ActionChains(self.driver)
        element = self.driver.find_element(By.CSS_SELECTOR, selector)

        # self.timeout.run()

        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        action.move_to_element(element).click().perform()

    def openmenu(self, buttonselector, menuselector):
        self.wait.until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, buttonselector))
        )

        action = ActionChains(self.driver)
        element = self.driver.find_element(By.CSS_SELECTOR, buttonselector)

        # self.timeout.run()

        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        action.move_to_element(element).click().perform()

        width = self.getcss(menuselector, "width")
        height = self.getcss(menuselector, "height")
        timeout = 0
        while timeout < self.timeout.max:
            self.timeout.dostep()
            timeout = timeout + self.timeout.step
            newwidth = self.getcss(menuselector, "width")
            newheight = self.getcss(menuselector, "height")
            if width == newwidth and height == newheight:
                break
            width = newwidth
            height = newheight

    def clicklink(self, url, selector):
        selector = selector + '[href*="' + url + '"]'
        oldurl = self.driver.current_url

        self.wait.until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, selector))
        )

        action = ActionChains(self.driver)
        element = self.driver.find_element(By.CSS_SELECTOR, selector)

        if self.ishoneypot(element):
            print("Element is honeypot")
            return False

        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

        # self.timeout.run()

        action.move_to_element(element).click().perform()

        self.wait.until(
            expected_conditions.url_changes(url=oldurl)
        )

        self.wait.until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )

    def goback(self, steps=1):
        for i in range(steps):
            # self.timeout.run()

            oldurl = self.driver.current_url

            self.driver.back()

            self.wait.until(
                expected_conditions.url_changes(url=oldurl)
            )

            self.wait.until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
