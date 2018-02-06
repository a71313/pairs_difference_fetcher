from abc import ABCMeta, abstractmethod

import inject

from fetcher import Fetcher


class ExchangePairFetcher(metaclass=ABCMeta):
    @inject.params(fetcher=Fetcher)
    def __init__(self, fetcher):
        self.fetcher = fetcher

    @abstractmethod
    def canonize(self, pairs):
        pass

    @abstractmethod
    def get_pairs(self) -> dict:
        pass
