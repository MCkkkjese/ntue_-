# 匯入 requests 套件
import requests
# 匯入 BeautifulSoup 套件
from bs4 import BeautifulSoup

# 使用 requests.get 方法下載 PTT 棒球版首頁
url = 'https://www.ptt.cc/bbs/Baseball/index.html'

# 設定 User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}
# 帶入 headers 參數
response = requests.get(url, headers=headers)

# 存成 HTML 檔案
with open('index1.html', 'w', encoding='utf-8') as f:
    f.write(response.text)

# 使用 BeautifulSoup 解析 HTML 程式碼
soup = BeautifulSoup(response.text, 'html.parser')

# 存成 HTML 檔案
with open('index2.html', 'w', encoding='utf-8') as f:
    f.write(soup.prettify())