import asyncio

from aiohttp import web

from application import Application
from application.routing import router
from exchange_data_fetcher.bitlish import BitlishPairFetcher
from exchange_data_fetcher.exmo import ExmoPairFetcher
from pool import Pool


class ApplicationImpl(Application):
    loop = asyncio.get_event_loop()
    difference = 0.01

    def __init__(self, usable_exchange_fetchers=None):
        super().__init__()
        self._usable_exchange_fetchers = usable_exchange_fetchers

    @property
    def usable_exchange_fetchers(self):
        if not self._usable_exchange_fetchers:
            self._usable_exchange_fetchers = (BitlishPairFetcher(), ExmoPairFetcher())
        return self._usable_exchange_fetchers

    async def get_currency_difference(self):
        futures = []
        for fetcher in self.usable_exchange_fetchers:
            futures.append(fetcher.get_pairs)

        pool = Pool(futures)
        exchanges_to_compare_data = await pool.run()

        return self.compare(exchanges_to_compare_data)

    def compare(self, data: list):
        exch_1_name = data[0]['exchange_name']
        exch_2_name = data[1]['exchange_name']
        exch_data_1 = data[0]['data']
        exch_data_2 = data[1]['data']

        comparation = {}
        for pair_name in exch_data_1:
            try:
                v1, v2 = exch_data_1[pair_name], exch_data_2[pair_name]
                diff = round(abs(v1 - v2), 4)
                diff_perc = round(max(v1, v2) * self.difference, 4)

                if diff > diff_perc:
                    comparation[pair_name] = {
                        exch_1_name: v1,
                        exch_2_name: v2,
                        'diff': diff
                    }

            except KeyError:
                pass
        return comparation

    def run(self):
        self._init_api()
        self.loop.run_until_complete(future=self._serv_generator)
        self.loop.run_forever()

    def _init_api(self):
        self.web_app = web.Application(loop=self.loop, router=router)
        handler = self.web_app.make_handler()
        self._serv_generator = self.loop.create_server(
            handler,
            "0.0.0.0",
            8080,
        )
