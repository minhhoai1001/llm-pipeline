import re, sys, os, requests
from urllib.parse import urlparse
from newsplease import NewsPlease
from bs4 import BeautifulSoup

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

    def crawl_links(self, link):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        response = requests.get(link, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()
        for a in soup.find_all('a', href=True):
            href = a['href']
            # Normalize to full URL
            if '/politics/' in href:
                if href.startswith("/"):
                    href = "https://www.nbcnews.com" + href
                
                if href.startswith("https://www.nbcnews.com/politics/"):
                    # Parse path to count segments after "/politics/"
                    path = urlparse(href).path  # e.g. /politics/white-house
                    segments = path.strip("/").split("/")  # ['politics', 'white-house']

                    if len(segments) >= 3:
                        links.add(href)  # only add if looks like a real article
        return links
        
    def extract(self, link: str, **kwargs) -> None:
        links = self.crawl_links(link)
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
