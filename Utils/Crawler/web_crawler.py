import scrapy

#Dont use this

class PowerSchool(scrapy.Spider):
    name = 'powerschool'
    allowed_domains = ['power.this.edu.cn']
    start_urls = ['hhtps://power.this.edu.cn/public/']

    def parse(self, response):
        print(response)

psl = PowerSchool()