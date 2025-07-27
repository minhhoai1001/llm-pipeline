import re, sys, os
import asyncio
from newsplease import NewsPlease
from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CrawlerRunConfig,
    DefaultMarkdownGenerator,
    PruningContentFilter,
    CrawlResult
)

from .base import BaseCrawler
from core.db.documents import ArticleDocument

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

class NBCNewsCrawler(BaseCrawler):
    """Crawler for NBC News articles."""
    model = ArticleDocument
    def __init__(self):
        super().__init__()
    
    def extract_urls(self, markdown_text):
        # Match markdown links: ## [Title](URL)
        pattern = re.findall(r"## \[(.*?)\]\((https://www\.nbcnews\.com/business/.*?)\)", markdown_text)
        links = []
        for title, url in pattern:
            if len(title) < 30:
                continue
            links.append(url)
        return links

    async def crawl_links(self, link):
        browser_config = BrowserConfig(
            headless=False,
            verbose=True,
        )
        async with AsyncWebCrawler(config=browser_config) as crawler:
            crawler_config = CrawlerRunConfig(
                markdown_generator=DefaultMarkdownGenerator(
                    content_filter=PruningContentFilter()
                ),
            )
            result: CrawlResult = await crawler.arun(
                url=link, config=crawler_config
            )
            
            links = self.extract_urls(result.markdown)
            return links
        
    def extract(self, link: str, **kwargs) -> None:
        links = asyncio.run(self.crawl_links(link))
        for url in links:
            try:
                article = NewsPlease.from_url(url)
                if article:
                    data = {
                        "link": url,
                        "title": article.title,
                        "authors": article.authors,
                        "content": article.maintext,
                        "date_publish": article.date_publish
                    }
                    print(f"data: {article.title}")
                    instance = self.model(**data)
                    instance.save()
            except Exception as e:
                print(f"Error processing link {url}: {e}")
