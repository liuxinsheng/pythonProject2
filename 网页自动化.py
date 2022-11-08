
from fake_useragent import UserAgent
import requests
import pyautogui
import time
import pyperclip
import winsound
import random
from requests.adapters import HTTPAdapter

ua = UserAgent()
# 请求的网址
# url = 'https://www.okx.com/v3/c2c/tradingOrders/books?quoteCurrency=CNY&baseCurrency=ETH&side=sell&paymentMethod=all&userType=all&showTrade=false&receivingAds=false&showFollow=false&showAlreadyTraded=false&isAbleFilter=false'
# TikerUrl = 'https://www.okx.com/api/v5/market/ticker?instId=ETH-USDT'
quoteMaxAmountPerOrder = 30000
limit = 7.28
name = '资金安全审流水'
name1 = '九州安全商行'
# name = '九州安全商行'
# name1 = '资金安全审流水'


def otcbook(coin):
    res = 0
    for i in range(5):
        try:
            url = 'https://www.okx.com/v3/c2c/tradingOrders/books?quoteCurrency=CNY&baseCurrency=' + coin + '&side=sell&paymentMethod=all&userType=all&showTrade=false&receivingAds=false&showFollow=false&showAlreadyTraded=false&isAbleFilter=false'

            headers = {"User-Agent": ua.random}
            response = requests.get(url=url, headers=headers)
            res = response.json()['data']['sell']
        except:
            print('otc_book网络错误，重新获取数据', i + 1)
            time.sleep(1)
        else:
            break
    new_book = []
    if res != None:
        for ele in res:
            if float(ele['quoteMaxAmountPerOrder']) > quoteMaxAmountPerOrder and ele['nickName'] != name1 or ele[
                'nickName'] == name:
                new_book.append(ele)
        # print(new_book)
    return new_book


def tiker(coin):
    TikerUrl = 'https://www.okx.com/api/v5/market/ticker?instId=' + coin + '-USDT'
    headers = {"User-Agent": ua.random}
    res = None
    for i in range(5):
        try:
            response = requests.get(url=TikerUrl, headers=headers)
            res = response.json()['data'][0]['askPx']
        except:
            print('tiker网络错误，重新获取数据', i + 1)
            time.sleep(1)
        else:
            break
    # print(res)
    return res


def judge(ask):
    i = 0
    # ask = otcbook()
    # print(ask)
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


def judge1(ask, coin, ask_price):
    i = 0
    ii = 0
    # ask_price = float(tiker(coin))
    # print(ask_price)
    for i in range(10):
        # if float(ask[i]['quoteMaxAmountPerOrder']) < quoteMaxAmountPerOrder and ask[i]['nickName'] != name:
        if float(ask[i]['price']) / ask_price < limit * 1.0003 and ask[i]['nickName'] != name:
            i = i + 1
            # print('订单量太低，不抢', ask[i]['nickName'], ask[i]['quoteMaxAmountPerOrder'], i)
        else:
            # print(ask[i]['nickName'], ask[i]['quoteMaxAmountPerOrder'], i)
            break
    for ii in range(10):
        # if float(ask[i]['quoteMaxAmountPerOrder']) < quoteMaxAmountPerOrder and ask[i]['nickName'] != name:
        if ask[ii]['nickName'] != name:
            ii = ii + 1
            # print('订单量太低，不抢', ask[i]['nickName'], ask[i]['quoteMaxAmountPerOrder'], i)
        else:
            # print(ask[i]['nickName'], ask[i]['quoteMaxAmountPerOrder'], i)
            break
    # print(float(ask[i]['price']) / ask_price)
    # print(ii)
    return i, ii


def pricing(a, coinLocation):
    fb = pyautogui.locateOnScreen('img/fb.png', confidence=0.9)
    if coinLocation is None:
        print('没有找到交易对')
        time.sleep(5)
    elif fb is not None:
        print('刷新页面')
        pyautogui.hotkey('F5')
        time.sleep(5)
    else:
        pyautogui.moveTo(coinLocation, duration=0.1)
        pyautogui.moveRel(865, 0, duration=0.1)
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
            # print(i)
            time.sleep(0.5)
            pyautogui.typewrite(i, 0.3)
            time.sleep(0.5)
            pyautogui.click(fdLocation.left + 776, fdLocation.top + 25)
            # pyautogui.moveTo(fdLocation.left+1088,fdLocation.top+35, duration=0.1)


def error():
    fb = pyautogui.locateOnScreen('img/fb.png', confidence=0.9)
    if fb is not None:
        pyautogui.hotkey('F5')


def rob(coin):
    ask = otcbook(coin)
    ask_price = float(tiker(coin))
    if ask_price != 0:
        index = judge1(ask, coin, ask_price)
        # print(float(ask[index]['price']))
        price = float(ask[index[0]]['price']) / ask_price
        print(coin, round(price, 3), ask[index[0]]['nickName'], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        difference_percentage = round(
            (float(ask[index[0]]['price']) - float(ask[index[1]]['price'])) / float(ask[index[1]]['price']) * 100, 2)

        # for i in range(2):
        coinLocation = pyautogui.locateOnScreen('img/' + coin + '.png', confidence=0.9)
        if price / 1.0003 > limit and ask[index[0]]['nickName'] != name:
            # num = random.choice([difference_percentage-0.01, difference_percentage])
            num = difference_percentage - 0.01
            pricing(num, coinLocation)
            print('抢单', num)
            time.sleep(5)
        elif price < limit and ask[index[0]]['nickName'] == name:
            num = random.choice([0.18, 0.28])
            pricing(num, coinLocation)
            print('低于极限，上调', num)
            time.sleep(5)
            winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
        elif float(ask[index[0] + 1]['price']) / float(ask[index[0]]['price']) >= 1.000190 and ask[index[0]][
            'nickName'] == name:
            num = random.choice([0.15, 0.23])
            pricing(num, coinLocation)
            print('上调', num)
            time.sleep(5)
        else:
            print('=' * 50)
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

