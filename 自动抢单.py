from fake_useragent import UserAgent
import requests
import pyautogui
import time
import pyperclip
import winsound
import random

ua = UserAgent()
# 请求的网址
# url = 'https://www.okx.com/v3/c2c/tradingOrders/books?quoteCurrency=CNY&baseCurrency=ETH&side=sell&paymentMethod=all&userType=all&showTrade=false&receivingAds=false&showFollow=false&showAlreadyTraded=false&isAbleFilter=false'
# TikerUrl = 'https://www.okx.com/api/v5/market/ticker?instId=ETH-USDT'
quoteMaxAmountPerOrder = 30000
limit = 7.22
# name = '资金安全审流水'
name = '九州安全商行'
# img = ['img/eth.png', 'img/btc.png']
# img = ['img/eth.png']


def otcbook(coin):
    url = 'https://www.okx.com/v3/c2c/tradingOrders/books?quoteCurrency=CNY&baseCurrency='+coin+'&side=sell&paymentMethod=all&userType=all&showTrade=false&receivingAds=false&showFollow=false&showAlreadyTraded=false&isAbleFilter=false'

    headers = {"User-Agent": ua.random}
    response = requests.get(url=url, headers=headers)
    res = response.json()['data']['sell']
    # print(res)
    return res


def tiker(coin):
    TikerUrl = 'https://www.okx.com/api/v5/market/ticker?instId='+coin+'-USDT'
    headers = {"User-Agent": ua.random}
    response = requests.get(url=TikerUrl, headers=headers)
    res = response.json()['data'][0]['askPx']
    # print(res)
    return res


def judge(ask):
    i = 0
    # ask = otcbook()
    # print(ask)
    for i in range(10):
        if float(ask[i]['quoteMaxAmountPerOrder']) < quoteMaxAmountPerOrder:
        # if float(ask[i]['price']) / float(tiker(coin)) <= limit:
            i = i + 1
            # print('订单量太低，不抢', ask[i]['nickName'], ask[i]['quoteMaxAmountPerOrder'], i)
        else:
            # print(ask[i]['nickName'], ask[i]['quoteMaxAmountPerOrder'], i)
            break
    # print(i)
    return i


def pricing(a, coinLocation):
    if coinLocation is None:
        print('没有找到交易对')
        time.sleep(1)
    else:
        pyautogui.moveTo(coinLocation, duration=0.1)
        pyautogui.moveRel(1215, 0, duration=0.1)
        pyautogui.click()
        time.sleep(1)
        fdLocation = pyautogui.locateOnScreen('img/fd.png', confidence=0.9)
        if fdLocation is not None:
            pyautogui.moveTo(fdLocation, duration=0.1)
            pyautogui.moveRel(0, 30, duration=0.1)
            pyautogui.doubleClick()
            pyautogui.hotkey('ctrl', 'c')
            text = float(pyperclip.paste())
            ii = round(text + a, 2)
            i = str(ii)
            print(i)
            time.sleep(0.5)
            pyautogui.typewrite(i, 0.3)
            time.sleep(0.5)
            pyautogui.click(fdLocation.left + 1088, fdLocation.top + 35)
            # pyautogui.moveTo(fdLocation.left+1088,fdLocation.top+35, duration=0.1)


def rob(coin):
    ask = otcbook(coin)
    index = judge(ask)
    # print(float(ask[index]['price']))
    price = float(ask[index]['price']) / float(tiker(coin))
    print(coin,round(price,3), ask[index]['nickName'],time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # print(float(ask[index+1]['price'])/ float(ask[index]['price']))

    # for i in range(2):
    coinLocation = pyautogui.locateOnScreen('img/' + coin + '.png',confidence=0.9)
    if price > limit and ask[index]['nickName'] != name:
        num = random.choice([-0.01, -0.02])
        pricing(num, coinLocation)
        print('抢单',num)
        time.sleep(5)
    elif price < limit and ask[index]['nickName'] == name:
        pricing(0.05, coinLocation)
        print('低于极限，上调',0.05)
        time.sleep(5)
        winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
    elif float(ask[index + 1]['price']) / float(ask[index]['price']) >= 1.000300 and ask[index]['nickName'] == name:
        num = random.choice([0.01, 0.03, 0.05])
        pricing(num, coinLocation)
        print('上调',num)
        time.sleep(15)
    else:
        print('等待几秒')
        time.sleep(5)


if __name__ == '__main__':
    while 1:
        try:
            rob('BTC')
            time.sleep(5)
            rob('ETH')
            time.sleep(5)
        except:
            print('出现异常')
