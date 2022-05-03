from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from fake_useragent import UserAgent
from machine import Machine

class FirefoxMachine(Machine):

    def __init__(self, proxy="127.0.0.1", windowsize="2048,1080"):
        self.proxy = proxy

        # setting of geckodriver
        options = FirefoxOptions()
        profile = webdriver.FirefoxProfile()

        # options.add_argument("--headless")
        # options.add_argument("--width=" + windowsize.split(",")[0])
        # options.add_argument("--height=" + windowsize.split(",")[1])

        profile.set_preference("general.useragent.override", UserAgent().random) #usage of rotating user agents

        profile.set_preference('permissions.default.stylesheet', 2) # disable css
        profile.set_preference("permissions.default.image", 2)  # disable images

        profile.set_preference("network.http.pipelining", True) # enable proxies
        profile.set_preference("network.http.proxy.pipelining", True) # enable proxies

        profile.set_preference("browser.cache.memory.capacity", 65536)  # Increase the cache capacity.
        profile.set_preference("browser.display.use_document_fonts", 0)  # Don't load document fonts.
        profile.set_preference("browser.shell.checkDefaultBrowser", False)

        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options, firefox_profile=profile)

    def clicklink(self, url):
        print("clicking:" + url)
