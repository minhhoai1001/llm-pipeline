import schedule
import time
import subprocess

from data_crawling.crawlers import NBCNewsCrawler
from data_crawling.dispatcher import CrawlerDispatcher

_dispatcher = CrawlerDispatcher()
_dispatcher.register("nbcnews", NBCNewsCrawler)

def handler():
    crawler = NBCNewsCrawler()
    # Example link to crawl
    nbc_link = "https://www.nbcnews.com/politics"
    crawler = _dispatcher.get_crawler(nbc_link)
    
    print(f"Using crawler: {crawler.__class__.__name__}")
    crawler.extract(nbc_link)

if __name__ == "__main__":
    schedule.every(5).minutes.do(handler)
    
    # start the first run immediately
    handler()
    
    # start the scheduler
    while True:
        schedule.run_pending()
        time.sleep(60)