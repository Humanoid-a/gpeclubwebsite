import scrapy


class PslSpider(scrapy.Spider):
    name = "psl"
    allowed_domains = ["power.this.edu.cn"]
    start_urls = ["https://power.this.edu.cn/public/"]

    def parse(self, response):
        QUOTE_SELECTOR = '.quote'
        TEXT_SELECTOR = '.center'
        AUTHOR_SELECTOR = '.author::text'

        for tag in response.css(TEXT_SELECTOR):
            print('-'*50)
            print(tag)

