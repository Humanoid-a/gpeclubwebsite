#import sys,os

#sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from powerschool.powerschool.spiders import psl


def crawl_account(username, pwd):
    process = CrawlerProcess(get_project_settings())
    psl.USERNAME = username
    psl.PWD = pwd
    process.crawl(psl.PslSpider)
    process.start()