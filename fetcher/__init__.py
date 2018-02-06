from abc import ABCMeta, abstractmethod


class Fetcher(metaclass=ABCMeta):
    @abstractmethod
    def fetch(self, url, data=None, success_http_codes=(200,), ignore_http_codes=()):
        pass


