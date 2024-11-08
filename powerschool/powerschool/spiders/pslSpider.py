import scrapy


class PowerSchool(scrapy.Spider):
    name = 'powerschool'
    allowed_domains = ['power.this.edu.cn']
    start_urls = ['https://power.this.edu.cn/public/']

    def parse(self, response):
        print(response)