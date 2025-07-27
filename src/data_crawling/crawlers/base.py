from abc import ABC, abstractmethod

class BaseCrawler(ABC):
    # model: type[BaseDocument]

    @abstractmethod
    def extract(self, link: str, **kwargs) -> None: ...