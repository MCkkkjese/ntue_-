# 匯入 requests 套件
import requests
# 匯入 BeautifulSoup 套件
from bs4 import BeautifulSoup
# 匯入 json 套件
import json
# 匯入 pandas 套件
import pandas as pd

# 使用 requests.get 方法下載文章頁面
url = "https://www.ptt.cc/bbs/Beauty/index.html"

# 設定 User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

# 加上 cookies
cookies = {
    'over18': '1'
}

# 帶入 headers 參數及 cookies 參數
response = requests.get(url, headers=headers, cookies=cookies)

# 使用 BeautifulSoup 解析 HTML 程式碼
soup = BeautifulSoup(response.text, 'html.parser')

# 印出 HTML 程式碼
print(soup.prettify())

