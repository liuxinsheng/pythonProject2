"""
日期：2022年02月11日
"""
import asyncio
import time

import aiohttp
from fake_useragent import UserAgent

urls = [
    'https://www.okx.com/v3/c2c/tradingOrders/books?quoteCurrency=CNY&baseCurrency=BTC&side=sell&paymentMethod=all&userType=all&showTrade=false&receivingAds=false&showFollow=false&showAlreadyTraded=false&isAbleFilter=false',
    'https://www.okx.com/api/v5/market/ticker?instId=BTC-USDT'
]

ua = UserAgent()
headers = {'User-Agent': ua.random}
# headers = {"user-agent": header}


def get_local_proxy():
    from urllib.request import getproxies
    proxy = getproxies()['http']
    return proxy


async def get_page(url):
    async with aiohttp.ClientSession() as session:
        async with await session.get(url=url, headers=headers, proxy=get_local_proxy()) as responsse:
            page_json = await responsse.json()
            # print(page_json)
    return page_json


def updata():
    stat = time.time()
    tasks = []
    for url in urls:
        c = get_page(url)
        task = asyncio.ensure_future(c)
        tasks.append(task)

    loop = asyncio.get_event_loop()
    # 异步协程固定写法 创建事件循环
    loop.run_until_complete(asyncio.wait(tasks))

    end = time.time()
    print('总耗时：', end - stat)


if __name__ == '__main__':
    while 1:
        try:
            updata()
            print(page_json)
        except:
            print('错误00123456')
            time.sleep(1)
        time.sleep(5)