import subprocess
import sys


def crawl_account(username, pwd):
    subprocess.run([sys.executable,'powerschool/pslcrawler.py','--username',username,'--pwd',pwd])

