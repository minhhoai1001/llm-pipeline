import re

from data_crawling.crawlers.base import BaseCrawler
from data_crawling.crawlers.custom_article import NBCNewsCrawler


class CrawlerDispatcher:
    def __init__(self) -> None:
        self._crawlers = {}

    def register(self, domain: str, crawler: type[BaseCrawler]) -> None:
        self._crawlers[r"https://(www\.)?{}.com/*".format(re.escape(domain))] = crawler

    def get_crawler(self, url: str) -> BaseCrawler:
        for pattern, crawler in self._crawlers.items():
            if re.match(pattern, url):
                return crawler()
        else:
            print(
                f"No crawler found for {url}. Defaulting to CustomArticleCrawler."
            )

            return NBCNewsCrawler()