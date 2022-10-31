from selenium import webdriver
from selenium.webdriver.common.by import By
# 设置自动化打开的浏览器访问网址
url = 'https://www.tnldfg.com/p2p/dashboard'

# 设置谷歌浏览器driver的目录所在
path = 'D:/chromedriver/chromedriver'

wd = webdriver.Chrome(executable_path=path)

elements = wd.find_elements(By.CLASS_NAME, 'plant')

for element in elements:
    print(element.text)
