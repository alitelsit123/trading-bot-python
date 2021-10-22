import asyncio
from binance import AsyncClient, BinanceSocketManager


async def main():
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client, user_timeout=30)
    # start any sockets here, i.e a trade socket
    ts = bm.trade_socket('BTCUSDT')
    # then start receiving messages
    async with ts as tscm:
        while True:
            res = await tscm.recv()
            print(res)

    await client.close_connection()

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())