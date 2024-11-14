import powerschool.pslcrawler as pslcrawler

#pslcrawler.crawl_account('ENTER YOUR USERNAME', 'ENTER YOUR PWD')
#pslcrawler.crawl_account('190621DLA', 'EsJ77577@')
#test_n = '190621DLA'
#test_p = 'EsJ77577@'


import sys

if __name__ == "__main__":
    username = sys.argv[1]
    password = sys.argv[2]

    pslcrawler.crawl_account(username, password)

