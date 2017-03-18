import asyncio

from aiobitfinex import RESTClient

async def main(loop):
    bitfinex = RESTClient(loop)
    ticker = await bitfinex.ticker('btcusd')
    print(ticker)


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))

