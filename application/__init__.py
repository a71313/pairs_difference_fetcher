from abc import ABCMeta, abstractmethod

import inject

from application.app_config import configurate


class Application(metaclass=ABCMeta):

    @abstractmethod
    def get_currency_difference(self):
        pass
    

    @abstractmethod
    def run(self):
        pass


def run_app():
    configurate()
    app = inject.instance(Application)
    app.run()
