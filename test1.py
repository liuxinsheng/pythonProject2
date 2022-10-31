import requests

if __name__ == '__main__':
    url = 'https://www.okx.com/v3/c2c/tradingOrders/books?quoteCurrency=CNY&baseCurrency=BTC&side=all&paymentMethod=all&userType=all&showTrade=false&receivingAds=false&showFollow=false&showAlreadyTraded=false&isAbleFilter=false'
    url1 = 'https://www.google.com/?hl=zh_CN'
    headers = {
        # 'accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / avif, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3;q = 0.9',
        'user - agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        # 'accept-encoding': 'gzip, deflate, br',
        # 'accept - language': 'zh - CN, zh;q = 0.9',
        # 'cache - control': 'max - age = 0',
        # 'dnt': 1,
        # 'sec-ch-ua': '"Chromium";v = "106", "Google Chrome"; v = "106", "Not;A=Brand"; v = "99"',
        # 'sec-ch-ua-mobile': '?0',
        # 'sec-ch-ua-platform': '"Windows"',
        # 'sec-fetch-dest': 'document',
        # 'sec-fetch-mode': 'navigate',
        # 'sec-fetch-site': 'none',
        # 'sec-fetch-user': '?1',
        # 'upgrade-insecure-requests': 1
    }
    cookie={'cookie': 'defaultLocale=zh_CN; G_ENABLED_IDPS=google; limitRegion=1; first_ref=https%3A%2F%2Fwww.okx.com%2Fweb3; limitRegion1=0; locale=zh_CN; u_ip=MTAzLjE0Mi4xNDAuODM; isLogin=1; _ga=GA1.1.41270403.1664608134; amp_56bf9d=f7QcwToTRhXx7Im30U0Hwd.OUdGQmRjWmg0NmVZSExRUzRtczc4QT09..1gevknd9c.1gevkonc7.76.7.7d; amp_56bf9d_okx.com=f7QcwToTRhXx7Im30U0Hwd.OUdGQmRjWmg0NmVZSExRUzRtczc4QT09..1gevkonc7.1gevkonca.26.h.2n; _ga_G0EKWWQGTZ=GS1.1.1665361753.6.1.1665363014.0.0.0; __cf_bm=8kyaiuU7raxX2s5iIXngiVR8bo4jxzRQ0WHs6X9CEMI-1665625747-0-AQLL6SxYe0W84+0UZXhyM/dbv8jzTszVhme71JvEZb5NB3vuqmAHVseOgytJeYF6LOXDrp5F2bd5tYbyu2uAy3M=',

    }
    response = requests.get(url=url, headers=headers,cookies=cookie)
    print(response.status_code)
    # resJson = response.text
    # print(resJson)
