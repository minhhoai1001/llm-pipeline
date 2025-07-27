from data_crawling.crawlers import NBCNewsCrawler
# from core.db.documents import ArticleDocument


if __name__ == "__main__":
    crawler = NBCNewsCrawler()
    # Example link to crawl
    example_link = "https://www.nbcnews.com/business"
    crawler.extract(example_link)
    