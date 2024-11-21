#import powerschool.pslcrawler as pslcrawler
import subprocess
import sys
import pslCrawlAPI

#pslcrawler.crawl_account('190621DLA', 'EsJ77577@')
#pslcrawler.crawl_account('190621DLA', 'EsJ77577@')
pslCrawlAPI.crawl_account('190621DLA', 'EsJ77577@')


#pslcrawler.crawl_account('190621DLA', 'EsJ77577@')
#test_n = '190621DLA'
#test_p = 'EsJ77577@'
#subprocess.run([sys.executable,'powerschool/pslcrawler.py','--username','190621DLA','--pwd','EsJ77577@'])
#subprocess.run([sys.executable,'powerschool/pslcrawler.py','--username','190621DLA','--pwd','EsJ77577@'])


#import sys

#if __name__ == "__main__":
#    username = sys.argv[1]
#    password = sys.argv[2]

#    try:
#        pslcrawler.crawl_account(username, password)
#    except Exception as e:
#        print(f"Error: {e}")
#        sys.exit(1)