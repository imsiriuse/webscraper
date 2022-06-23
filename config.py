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

        # parsetree
        mainpage = ActionsNode([
            ActionClick(".browse-category-wrap"),
            ActionNextpage(".categorylist")])

        productspage = ActionsNode([
            ActionPaging(".page-numbers"),
            ActionNextpage(".woocommerce-loop-product__link")])

        productpage = ActionsNode([
            ActionContent(".page-title"),
            ActionContent(".woocommerce-Tabs-panel--description p"),
            ActionContent(".summary .woocommerce-Price-amount bdi")])

        mainpage.nextnode = productspage
        productspage.nextnode = productpage

        self.parser = mainpage
