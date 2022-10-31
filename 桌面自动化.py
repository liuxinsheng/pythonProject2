import pandas as pd
import pyautogui
import time
import pyperclip
import urllib.request
import winsound
import random
# print(1)
limit = 7.115
name = '资金安全审流水'
# name = '九州安全商行'

# url=['http://metaapps.pro/btc','http://metaapps.pro/eth']
img = ['img/eth.png', 'img/btc.png']
# img = ['img/btc.png']
# img = ['img/eth.png']
rnum =[0.01,0.03]


def info(a):
    url = ['http://metaapps.pro/eth', 'http://metaapps.pro/btc']
    req = urllib.request.Request(url[a])
    response = urllib.request.urlopen(req)
    res = pd.read_json(response)
    return res


# 改价格
def update(a):
    pyautogui.moveTo(coinLocation, duration=0.1)
    pyautogui.moveRel(1215, 0, duration=0.1)
    pyautogui.click()
    time.sleep(1)
    fdLocation = pyautogui.locateOnScreen('img/fd.png')
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


if __name__ == '__main__':

    while 1:
        try:
            for index in range(len(img)):
                coinLocation = pyautogui.locateOnScreen(img[index])
                INFO = info(index)['res']
                print(float(INFO[8]) / float(INFO[2]))
                if float(INFO[1]) > limit and INFO[3] != name:
                    if coinLocation is None:
                        print('没有找到交易对')
                        time.sleep(1)
                        # coinLocation = pyautogui.locateOnScreen(img[index])
                    else:
                        print('抢单')
                        update(-0.02)
                        time.sleep(2)
                elif float(INFO[1]) <= limit and INFO[3] == name:
                    print('低于极限，上调')
                    update(0.05)
                    time.sleep(2)
                    winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
                elif float(INFO[8]) / float(INFO[2]) >= 1.000200 and INFO[3] == name:
                    print('上调')
                    num = random.choice([0.01,0.03,0.05])
                    update(num)
                    time.sleep(2)
                else:
                    print(img[index],INFO[1])
                time.sleep(2)
        except:
            print('出现异常')
