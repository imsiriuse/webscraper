from actions import *
from actionsnode import ActionsNode
from firefoxmachine import FirefoxMachine
from timeout import Timeout


class Config:
    def __init__(self, starturl):
        # url of first page
        self.starturl = starturl

        # settings
        self.proxies = []
        self.threads = 1
        self.timeout = Timeout(max=5, min=1, step=1)
        self.windowsizes = ["1280,720", "1920,1080", "2560,1440", "2048,1080", "3840,2160"]
        self.driver = FirefoxMachine
        self.encoding = "utf8"
        self.honeypots = False

        # parsetree
        mainpage = ActionsNode([
            ActionClick(
                selector=".browse-category-wrap"
            ),
            ActionNextpage(
                selector=".categorylist"
            )
        ])
        paging = ActionsNode([
            ActionPaging(
                selector=".page-numbers"
            ),
            ActionNextpage(
                selector=".woocommerce-loop-product__link"
            )
        ])
        product = ActionsNode([
            ActionGetcontent(
                selectors=[
                    ".page-title",
                    ".woocommerce-Tabs-panel--description p",
                    ".summary .woocommerce-Price-amount bdi"
                ],
                alias="product")
        ])

        paging.nextnode = product
        mainpage.nextnode = paging
        self.parser = mainpage

        # what kinds of random actions scraper should do
        # click on random links
        self.randomactions = []

        # what kind of actions scraper should do during waiting
        # scrolling, mouse moves etc
        self.waitingactions = []
