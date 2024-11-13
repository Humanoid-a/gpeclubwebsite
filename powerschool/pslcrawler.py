from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from powerschool.spiders import psl # Replace with your spider


def crawl_account(username, pwd):
    process = CrawlerProcess(get_project_settings())
    psl.USERNAME = username
    psl.PWD = pwd
    process.crawl(psl.PslSpider)
    process.start()