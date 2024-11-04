# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PowerschoolItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class PowerSchool(scrapy.Spider):
    name = 'powerschool'
    allowed_domains = ['power.this.edu.cn']
    start_urls = ['hhtps://power.this.edu.cn/public/']

    def parse(self, response):
        print(response)