# 第二种方法：解析器方式，利用Python特性创建list
# 基础list



quoteMaxAmountPerOrder = 31000
limit = 7.23
# name = '资金安全审流水'
name = '九州安全商行'


def otcbook(coin):
    url = 'https://www.okx.com/v3/c2c/tradingOrders/books?quoteCurrency=CNY&baseCurrency=' + coin + '&side=sell&paymentMethod=all&userType=all&showTrade=false&receivingAds=false&showFollow=false&showAlreadyTraded=false&isAbleFilter=false'

    headers = {"User-Agent": ua.random}
    response = requests.get(url=url, headers=headers)
    res = response.json()['data']['sell']
    # print(res)
    return res



def judge(ask):
    i = 0
    ask = otcbook()
    print(ask)
    for i in range(10):
        if float(ask[i]['quoteMaxAmountPerOrder']) < quoteMaxAmountPerOrder and ask[i]['nickName'] != name:
            # if float(ask[i]['price']) / float(tiker(coin)) <= limit:
            i = i + 1
            # print('订单量太低，不抢', ask[i]['nickName'], ask[i]['quoteMaxAmountPerOrder'], i)
        else:
            # print(ask[i]['nickName'], ask[i]['quoteMaxAmountPerOrder'], i)
            break
    # print(i)
    return i


# 过滤list
blockList = [640, 588]
filteredList = [ele for ele in baseList if ele not in blockList]
print(filteredList)