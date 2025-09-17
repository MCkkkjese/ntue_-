# 匯入 requests 套件
import requests
# 匯入 BeautifulSoup 套件
from bs4 import BeautifulSoup, NavigableString
# 匯入 json 套件
import json
# 匯入 pandas 套件
import pandas as pd
# 匯入 re 套件
import re

# 使用 requests.get 方法下載文章頁面
url = "https://www.ptt.cc/bbs/Gossiping/M.1720632619.A.6B0.html"

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
# print(soup.prettify())

# 以網址最後的頁面名稱當作檔名，在此範例中檔名為 M.1720620433.A.E04
filename = url.split('/')[-1][:-5]

# 輸出檔名
print(filename)

# 作法一
# 爬取文章，作者 id、文章標題、發佈時間、文章內容、發文 ip
# 作者 id
author_id = soup.select('span.article-meta-value')[0].text
# 文章標題
title = soup.select('span.article-meta-value')[2].text
# 發佈時間
time = soup.select('span.article-meta-value')[3].text
# 文章內容
content = soup.select('#main-content')[0].text.split('※ 發信站')[0].split(time)[1]
# 發文 ip
ip = soup.select('span.f2')[0].text.split(': ')[1]

# 輸出文章，作者 id、文章標題、發佈時間、文章內容、發文 ip
print('作者 id:', author_id)
print('文章標題:', title)
print('發佈時間:', time)
print('文章內容:', content)
print('發文 ip:', ip)

# 儲存文章，作者 id、文章標題、發佈時間、文章內容、發文 ip
data = {
    '作者 id': author_id,
    '文章標題': title,
    '發佈時間': time,
    '文章內容': content,
    '發文 ip': ip
}

# 輸出文章，作者 id、作者暱稱、文章標題、發佈時間、文章內容、發文 ip
print(data)

# 將文章，作者 id、作者暱稱、文章標題、發佈時間、文章內容、發文 ip 輸出成 JSON 檔案
with open(f'{filename}.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)

# 爬取留言，推噓、推文 id、推文內容、推文 ip、推文時間
# 留言列表
comments = []
# 找出所有留言
pushes = soup.find_all('div', class_='push')
# 逐一檢視每個留言
for push in pushes:
    # 推噓
    push_tag = push.find('span', class_='push-tag').text
    # 推文 id
    push_userid = push.find('span', class_='push-userid').text
    # 推文內容
    push_content = push.find('span', class_='push-content').text
    # 推文 ip
    push_ipdatetime = push.find('span', class_='push-ipdatetime').text
    # 推文時間
    push_time = push_ipdatetime.split(' ')[-1]
    # 推文 ip
    push_ip = push_ipdatetime.split(' ')[0]
    # 將推噓、推文 id、推文內容、推文 ip、推文時間輸出成列表
    comments.append([push_tag, push_userid, push_content, push_ip, push_time])

# 輸出留言，推噓、推文 id、推文內容、推文 ip、推文時間
for comment in comments:
    print(comment)

# 將結果儲存為EXCEL
df = pd.DataFrame(comments, columns=['推噓', '推文 id', '推文內容', '推文 ip', '推文時間'])
df.to_excel("comments.xlsx", index=False, engine="openpyxl")

# 作法二
# 找出文章主要內容
# article_body = soup.find(id='main-content')

# article = {
#     'author_id': '',
#     'author_nickname': '',
#     'title': '',
#     'timestamp': '',
#     'contents': '',
#     'ip': ''
# }

# # article header
# article_head = article_body.findAll('div', class_='article-metaline')
# for metaline in article_head:
#     meta_tag = metaline.find(class_='article-meta-tag').text
#     meta_value = metaline.find(class_='article-meta-value').text
#     if meta_tag == '作者':
#         compile_nickname = re.compile('\((.*)\)').search(meta_value)
#         article['author_id'] = meta_value.split('(')[0].strip(' ')
#         article['author_nickname'] = compile_nickname.group(1) if compile_nickname else ''
#     elif meta_tag == '標題':
#         article['title'] = meta_value
#     elif meta_tag == '時間':
#         article['timestamp'] = meta_value

# # article content
# contents = [expr for expr in article_body.contents if isinstance(expr, NavigableString)]
# contents = [re.sub('\n', '', expr) for expr in contents]
# contents = [i for i in contents if i]
# contents = '\n'.join(contents)
# article['contents'] = contents

# # article publish ip
# article_ip = article_body.find(class_='f2').text
# compile_ip = re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}').search(article_ip)
# article['ip'] = compile_ip.group(0) if compile_ip else ''

# # 輸出文章，作者 id、作者暱稱、文章標題、發佈時間、文章內容、發文 ip
# print('作者 id:', article['author_id'])
# print('作者暱稱:', article['author_nickname'])
# print('文章標題:', article['title'])
# print('發佈時間:', article['timestamp'])
# print('文章內容:', article['contents'])
# print('發文 ip:', article['ip'])