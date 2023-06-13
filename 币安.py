import pyautogui
import pyperclip
import requests
import json
import pyttsx3
import time
import cv2
import numpy as np
from PIL import ImageGrab

engine = pyttsx3.init()


def search(side, symbol, transAmount):
    # url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    url = "https://p2p.suitechsui.biz/bapi/c2c/v2/friendly/c2c/adv/search"
    data = {
        "fiat": "CNY",
        "page": 1,
        "rows": 10,
        "tradeType": side,
        "asset": symbol,
        "countries": [],
        "proMerchantAds": False,
        "publisherType": None,
        "payTypes": [],
        "transAmount": transAmount
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        i = np.array(response_json["data"])
        # print(i[0]['adv']['price'], i[0]["advertiser"]["nickName"])
        return i

    else:
        print(f"请求失败，状态码：{response.status_code}")
        return False


def tick(symbol):
    # 定义请求地址
    # url = "https://www.binance.com/api/v3/ticker/price?symbol=" + symbol + "USDT"
    url = "https://www.suitechsui.biz/api/v3/ticker/price?symbol=" + symbol + "USDT"
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    # print(response.status_code)
    if response.status_code == 200:
        return float(response.json()['price'])
    else:
        return False


def check_sell(sell_limit, symbols, transAmount):
    for symbol in symbols:
        res = search("BUY", symbol, transAmount)
        arr = []
        ask = tick(symbol)
        if symbol == "ETH":
            text = '以太坊'
        if symbol == 'BTC':
            text = '比特币'
        if ask or res.all():
            for index, ii in enumerate(res):
                if float(ii['adv']['price']) / ask >= sell_limit or ii["advertiser"]["nickName"] == '老白-专业-安全-长期稳定':
                    arr.append([float(ii['adv']['price']), ii["advertiser"]["nickName"]])
            for index, i in enumerate(arr):
                if float(i[0]) / ask >= sell_limit or i[1] == '老白-专业-安全-长期稳定':
                    # print(i['adv']['price'], i["advertiser"]["nickName"], round(float(i['adv']['price']) / ask, 3))
                    if i[1] == '老白-专业-安全-长期稳定':
                        print('SELL', symbol, i[0], i[1], round(float(i[0]) / ask, 3), index)
                        if index == 0:
                            Proportion = arr[1][0] / i[0]
                            if Proportion > 1.0003:
                                print("UP", round((Proportion - 1) * 100 - 0.01, 2))
                                pending('S' + symbol, round((Proportion - 1) * 100 - 0.01, 2))
                                engine.say(text + "卖单上调" + str(round((Proportion - 1) * 100 - 0.01, 2)))
                                engine.runAndWait()
                        else:
                            Proportion = i[0] / arr[0][0]
                            # if Proportion > 1.0002:
                            print("Down", round((Proportion - 1) * 100 + 0.01, 2))
                            pending('S' + symbol, round(((Proportion - 1) * 100 + 0.01), 2) * -1)
                            engine.say(text + "卖单下调" + str(round((Proportion - 1) * 100 + 0.01, 2)))
                            engine.runAndWait()
                        break
                    else:
                        print(i[0], i[1], round(i[0] / ask, 3), index)

            time.sleep(5)
        else:
            print('网络连接错误')
            time.sleep(5)


def check_buy(buy_limit, symbols, transAmount):
    for symbol in symbols:
        res = search("SELL", symbol, transAmount)
        arr = []
        ask = tick(symbol)
        if symbol == "ETH":
            text = '以太坊'
        if symbol == 'BTC':
            text = '比特币'
        if ask or res.all():
            for index, ii in enumerate(res):
                if float(ii['adv']['price']) / ask <= buy_limit or ii["advertiser"][
                    "nickName"] == '老白-专业-安全-长期稳定':
                    arr.append([float(ii['adv']['price']), ii["advertiser"]["nickName"]])
            for index, i in enumerate(arr):
                if float(i[0]) / ask <= buy_limit or i[1] == '老白-专业-安全-长期稳定':
                    # print(i['adv']['price'], i["advertiser"]["nickName"], round(float(i['adv']['price']) / ask, 3))
                    if i[1] == '老白-专业-安全-长期稳定':
                        print('BUY', symbol, i[0], i[1], round(float(i[0]) / ask, 3), index)
                        if index == 0:
                            Proportion = i[0] / arr[1][0]
                            if Proportion > 1.0003:
                                print("Down", round((Proportion - 1) * 100 - 0.01, 2))
                                pending('B' + symbol, round((Proportion - 1) * 100 - 0.01, 2) * -1)
                                engine.say(text + "收单下调" + str(round((Proportion - 1) * 100 - 0.01, 2)))
                                engine.runAndWait()
                        else:
                            Proportion = arr[0][0] / i[0]
                            # if Proportion > 1.0002:
                            print("UP", round((Proportion - 1) * 100 + 0.01, 2))
                            pending('B' + symbol, round(((Proportion - 1) * 100 + 0.01), 2))
                            engine.say(text + "收单上调" + str(round((Proportion - 1) * 100 + 0.01, 2)))
                            engine.runAndWait()
                        break
                    else:
                        print(i[0], i[1], round(i[0] / ask, 3), index)

            time.sleep(5)
        else:
            print('网络连接错误')
            time.sleep(5)


def pending(symbol, a):
    max_attempts = 10
    current_attempt = 0

    location = pyautogui.locateOnScreen('imgs/' + symbol + '.png', confidence=0.9)
    if location:
        x, y = pyautogui.center(location)
        pyautogui.moveTo(x + 1410, y + 1)
        pyautogui.click()
        time.sleep(1)
        while current_attempt < max_attempts:
            location = pyautogui.locateOnScreen('imgs/100.png', confidence=0.8)
            if location:
                pyautogui.moveTo(x + 121, y + 169)
                time.sleep(1)
                pyautogui.doubleClick()
                pyautogui.hotkey('ctrl', 'c')
                text = float(pyperclip.paste())
                ii = round(text + a, 2)
                i = str(ii)
                time.sleep(0.5)
                pyautogui.typewrite(i, 0.1)
                time.sleep(0.5)
                while current_attempt < 4:
                    location = pyautogui.locateOnScreen('imgs/bc.png', confidence=0.9)
                    if location:
                        pyautogui.click(location)
                        break
                    pyautogui.click(1050, 707)
                    time.sleep(1)
                    pyautogui.scroll(-300)
                    time.sleep(1)
                    current_attempt += 1
                break
            else:
                time.sleep(1)
                current_attempt += 1
        pyautogui.moveTo(56,642)
        time.sleep(1)

    else:
        engine.say("没有找到交易对")
        engine.runAndWait()
        print("没有找到交易对")


if __name__ == '__main__':
    sell_limit = 7.15
    buy_limit = 7.075
    symbols = ["BTC", "ETH"]
    sell_transAmount = 10000
    buy_transAmount = 10000
    while 1:
        try:
            check_sell(sell_limit, symbols, sell_transAmount)
            time.sleep(5)
            check_buy(buy_limit, symbols, buy_transAmount)
            time.sleep(5)
        except:
            print('出错')
