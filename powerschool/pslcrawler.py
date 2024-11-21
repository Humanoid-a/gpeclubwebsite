import scrapy.cmdline
#import sys,os

#sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from powerschool.spiders import psl
from scrapy.cmdline import execute

from gpeclub.models import psl as psl_model



def crawl_account(username, pwd):
    psl_model.objects.all().delete()
    #process = CrawlerProcess(get_project_settings())

    process = CrawlerProcess(get_project_settings())
    process.crawl(psl.PslSpider)
    psl.USERNAME = username
    psl.PWD = pwd
    #command = ['scrapy', 'crawl', 'psl']
    #execute(command)
    #result = subprocess.run(command, cwd=PROJECT_PATH, text=True, capture_output=True)
    process.start()
    #process.join()
    #process.stop()



import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--username", type=str)
parser.add_argument("--pwd", type=str)

args = parser.parse_args()

crawl_account(args.username, args.pwd)