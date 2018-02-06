from exchange_data_fetcher import ExchangePairFetcher


class ExmoPairFetcher(ExchangePairFetcher):
    url = 'https://api.exmo.com/v1/ticker'
    exchange_name = 'exmo'

    def convert_name(self, name):
        return '{}/{}'.format(*name.split('_'))

    def canonize(self, pairs):
        return {self.convert_name(p_name): float(p_data['buy_price']) for p_name, p_data in pairs.items()}

    async def get_pairs(self):
        pairs = await self.fetcher.fetch(self.url)
        return {'data': self.canonize(pairs), 'exchange_name': self.exchange_name}
