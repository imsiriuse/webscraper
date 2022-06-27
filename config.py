from machine import *
from actions import *
from actionsnode import ActionsNode


class Config:
    def __init__(self, starturl):
        # url of first page
        self.starturl = starturl

        # settings
        self.proxies = []
        self.threads = 1
        self.timeoutmin = 3000
        self.timeoutmax = 5000
        self.windowsizes = ["1280,720", "1920,1080", "2560,1440", "2048,1080", "3840,2160"]
        self.driver = FirefoxMachine
        self.encoding = "utf8"

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
        self.randomactions = []
