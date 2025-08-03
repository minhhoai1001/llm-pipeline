from data_crawling.crawlers import NBCNewsCrawler
from data_crawling.dispatcher import CrawlerDispatcher

_dispatcher = CrawlerDispatcher()
_dispatcher.register("nbcnews", NBCNewsCrawler)

if __name__ == "__main__":
    crawler = NBCNewsCrawler()
    # Example link to crawl
    example_link = "https://www.nbcnews.com/politics"
    # crawler.extract(example_link)
    crawler = _dispatcher.get_crawler(example_link)
    
    print(f"Using crawler: {crawler.__class__.__name__}")
    crawler.extract(example_link)