import asyncio
import logging
import async_timeout
from typing import Optional, List

import aiohttp

logger = logging.getLogger('bitfinex.rest')


class APIPath:
    """Path definitions for the Bitfinex REST API"""

    API_ROOT = 'https://api.bitfinex.com/v1/{}'

    # -- Public endpoints

    SYMBOLS = API_ROOT.format('symbols')
    SYMBOLS_DETAILS = API_ROOT.format('symbols_details')

    # - Uses symbol (btcusd, etc)
    TICKER = API_ROOT.format('pubticker/{}')
    STATS = API_ROOT.format('stats/{}')
    TRADES = API_ROOT.format('trades/{}')

    # - Uses currency ('USD, etc)
    FUNDING_BOOK = API_ROOT.format('lendbook/{}')
    ORDER_BOOK = API_ROOT.format('orderbook/{}')
    LENDS = API_ROOT.format('lends/{}')


class RESTClient:
    """
    Async client for the bitfinex HTTP REST API.
    """

    def __init__(self,
                 loop: Optional[asyncio.BaseEventLoop]=None,
                 session: aiohttp.ClientSession=None):
        self._loop = loop or asyncio.get_event_loop()
        self._session = session or aiohttp.ClientSession(loop=self._loop)

    def __del__(self):
        if not self._session.closed:
            self._session.close()

    async def _fetch(self, url: str) -> any:
        """
        Performs a GET request, checking the response code to see if it's between 200 - 300.
        If it's, it parses the JSON to a python object. If not it raises an HTTP error

        :return: Bitfinex API response
        """
        logger.debug('Fetching', url)
        with async_timeout.timeout(10):
            async with self._session.get(url) as response:
                if 200 <= response.status < 300:
                    return await response.json()
                else:
                    raise aiohttp.errors.HttpProcessingError(
                        message=f'There was a problem processing {url}', code=response.status)

    async def ticker(self, symbol: str) -> dict:
        """
        Gets the high level overview of the state of the market (ticker) for the given symbol
        API URL: http://docs.bitfinex.com/v1/reference#rest-public-ticker

        :param symbol: the currency pair that you want information. (btcusd, etc). Yo can look at
        the available symbols with the symbol method.
        :return:
        """
        return await self._fetch(APIPath.TICKER.format(symbol))

    async def stats(self, symbol: str) -> dict:
        """
        Gets various statistics about the requested pair (symbol)
        API URL: http://docs.bitfinex.com/v1/reference#rest-public-stats

        :param symbol: the currency pair that you want information. (btcusd, etc). Yo can look
        at the available symbols with the symbol method.
        :return: stats about the requested pair
        """
        return await self._fetch((APIPath.STATS.format(symbol)))

    async def trades(self, symbol: str) -> List[dict]:
        """
        Gets the most recent trades for the given symbol
        API URL: http://docs.bitfinex.com/v1/reference#rest-public-trades

        :param symbol: the currency pair that you want information. (btcusd, etc). Yo can look
        at the available symbols with the symbol method.
        :return: a list with the most recent trades
        """
        return await self._fetch(APIPath.TRADES.format(symbol))

    async def funding_book(self, currency: str) -> dict:
        """
        Gets the full margin funding book
        API URL: http://docs.bitfinex.com/v1/reference#rest-public-fundingbook

        :param currency: the currency in what you want the information
        :return:
        """
        return await self._fetch((APIPath.FUNDING_BOOK.format(currency)))

    async def order_book(self, currency: str) -> dict:
        """
        Gets the full order book
        API URL: http://docs.bitfinex.com/v1/reference#rest-public-orderbook

        :param currency: the currency in what you want the information
        :return:
        """
        return await self._fetch(APIPath.ORDER_BOOK.format(currency))

    async def lends(self, currency: str) -> List[dict]:
        """
        Gets a list of the most recent funding data for the given currency

        :param currency:
        :return:
        """
        return await self._fetch(APIPath.LENDS.format(currency))

    async def symbols(self) -> List[dict]:
        """Gets a list with the available symbol names in the exchange"""
        return await self._fetch(APIPath.SYMBOLS)

    async def symbols_details(self) -> List[dict]:
        """Gets a detailed list with the available symbols on the exchange"""
        return await self._fetch(APIPath.SYMBOLS)



