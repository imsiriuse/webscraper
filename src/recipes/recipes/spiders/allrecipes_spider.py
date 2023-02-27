import scrapy
from scrapy import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class RecipeSpider(CrawlSpider):
    name = "allrecipes.com"
    allowed_domains = ['allrecipes.com']
    start_urls = [
        'https://www.allrecipes.com/recipes-a-z-6735880',
    ]
    rules = [
        Rule(LinkExtractor(restrict_xpaths=('//a[@class="link-list__link type--dog-bold type--dog-link"]'))),
        Rule(LinkExtractor(restrict_xpaths=('//a[contains(@id,"mntl-card-list-items_")]')), callback="parse_recipes", process_links="process_links")
       # Rule(LinkExtractor(restrict_xpaths=('//a[contains(.,"Air Fryer Recipes")]'))),
       # Rule(LinkExtractor(restrict_xpaths=('//a[@data-doc-id=6665737]')), callback="parse_recipes", process_links="process_links")

    ]
    
    def process_links(self, links):
        return links[0:1]
    
    def clean(self, text):
        return ''.join(ch for ch in text if ch.isprintable())
    
    def parse_recipes(self, response):
        item = {}
        
        item['name'] = self.clean(response.xpath('//h1[@id="article-heading_2-0"]/text()').get())
        
        ingredients = response.xpath('//div[@id="mntl-structured-ingredients_1-0"]//p').getall()
        item['ingredients'] = list(map(lambda s: ' '.join(s.xpath('//span/text()').getall()), (Selector(text=x) for x in ingredients)))
        
        item['steps'] = list(map(self.clean, response.xpath('//div[@id="recipe__steps_1-0"]//p/text()').getall()))
                
        content_labels = response.xpath('//div[@id="recipe-details_1-0"]//div[@class="mntl-recipe-details__label"]/text()').getall()
        content_values = response.xpath('//div[@id="recipe-details_1-0"]//div[@class="mntl-recipe-details__value"]/text()').getall()
        item['content'] = list(map(lambda x: ' '.join(x) ,zip(content_labels, content_values)))
        
        nutrition = response.xpath('//div[@id="mntl-nutrition-facts-summary_1-0"]//td/text()').getall()
        def get_pairs(l):
            return list(zip(l[::2], l[1::2]))
        item['nutrition'] = ', '.join( map(lambda x: ' = '.join(x), get_pairs(nutrition)))

        
        return item
