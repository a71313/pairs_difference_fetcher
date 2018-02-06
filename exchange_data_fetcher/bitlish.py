from exchange_data_fetcher import ExchangePairFetcher


class BitlishPairFetcher(ExchangePairFetcher):
    url = 'https://bitlish.com/api/v1/tickers'
    exchange_name = 'bitlish'

    def convert_name(self, name):
        return f'{name[:3].upper()}/{name[3:].upper()}'

    def canonize(self, pairs):
        return {self.convert_name(p_name): float(p_data['last']) for p_name, p_data in pairs.items()}

    async def get_pairs(self):
        try:
            pairs = await self.fetcher.fetch(self.url)
            return {'data': self.canonize(pairs), 'exchange_name': self.exchange_name}
        except Exception as e:
            print(f'Something went wrong {e}. Skip {self.exchange_name}')
            return {'data': {}, 'exchange_name': self.exchange_name}
