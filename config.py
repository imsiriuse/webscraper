from machine import ChromeMachine
from machine import FirefoxMachine

class Config:
    def __init__(self, starturl):
        # url of first page
        self.starturl = starturl

        self.proxies = []
        self.threads = 1
        self.timeout = [3000, 5000]
        self.windowsizes = ["1280,720", "1920,1080", "2560,1440", "2048,1080", "3840,2160"]
        self.driver = FirefoxMachine

        self.actions = None

        self.actions = {}

        self.actions = [
            {
                "selector": ".browse-category-wrap",
                "strategy": "click"
            },{
                "selector": ".categorylist",
                "strategy": "nextpage"
            },{
                "selector": ".page-numbers",
                "strategy": "paging"
            },{
                "selector": ".woocommerce-loop-product__link",
                "strategy": "nextpage"
            },{
                "selector": ".page-title",
                "strategy": "content"
            },{
                "selector": ".woocommerce-Tabs-panel--description p",
                "strategy": "content"
            },{
                "selector": ".summary .woocommerce-Price-amount bdi",
                "strategy": "content"
            }
    ]

