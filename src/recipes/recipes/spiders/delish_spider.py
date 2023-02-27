import scrapy
from scrapy import Selector
from scrapy.spiders import SitemapSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from bs4 import BeautifulSoup

class RecipeSpider(SitemapSpider):
    name = "delish"
    allowed_domains = ['www.delish.com']
    sitemap_urls = [
        'https://www.delish.com/sitemap_index.xml/',
    ]
    sitemap_rules = [('/recipes/', 'parse_recipes')]
    sitemap_follow = [
        '/content'
    ]
    limit = 10
    current = 0
    def clean(self, text):
        return ''.join(ch for ch in text if ch.isprintable())
    
    def remove_control_characters(self, text):
        return ''.join(self.impl_remove_control_characters(text))
    
    def impl_remove_control_characters(self, text):
        for ch in text:
            if ch.isprintable():
                yield ch
            else:
                yield ' '
    
    def parse_recipes(self, response):
        item = {}
        
        item['name'] = self.clean(response.xpath('//header//h1//text()').get())
        item['ingredients'] = []
        ingredients  = response.xpath('//div[contains(@class,"ingredients-body")]//li').getall()
        for ingredient in ingredients:
            soup = BeautifulSoup(markup=ingredient, features='html.parser')
            item['ingredients'].append(soup.get_text())
        
        item['steps'] = list(map(self.remove_control_characters, response.xpath('//ul[contains(@class,"directions")]//li/text()').getall()))
        
        names = response.xpath('//div[contains(@class,"recipe-body")]//dt//text()').getall()
        values = list(filter(lambda s: not s.isspace() and s != '' ,response.xpath('//div[contains(@class,"recipe-body")]//dd').getall()))
        clean_values = []
        for val in values:
            soup = BeautifulSoup(markup=val, features='html.parser')
            clean_values.append(soup.get_text())
            
        item['content'] = [' '.join(x) for x in zip(names, clean_values)]

        self.current +=1
        if self.current >= self.limit:
            raise CloseSpider('limit reached')

        return item