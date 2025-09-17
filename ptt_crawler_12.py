# 匯入必要的套件
import requests  # 用來發送 HTTP 請求
from bs4 import BeautifulSoup, NavigableString  # 用來解析 HTML
import json  # 用來處理 JSON 資料
import pandas as pd  # 用來處理資料結構(這個程式碼中沒有使用到)
import re  # 用來處理正規表達式
from urllib.parse import urlencode, urljoin  # 用來處理 URL
import time  # 用來控制程式暫停

# 設定請求標頭,模擬瀏覽器行為
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

# 設定 cookies,繞過 PTT 的年齡限制
cookies = {
    'over18': '1'
}

# 設定欲搜尋的關鍵字
query_keyword = "大谷翔平"

# 將搜尋關鍵字轉換為 URL 編碼
encoding_title = urlencode({'q': query_keyword})
# 組合完整的搜尋 URL
query_url = 'https://www.ptt.cc/bbs/Gossiping/search?{}'.format(encoding_title)

# 發送 GET 請求到搜尋頁面
resp_article_list = requests.get(query_url, headers=headers, cookies=cookies)
# 使用 BeautifulSoup 解析回應的 HTML 內容
soup_article_list = BeautifulSoup(resp_article_list.text, 'html.parser')

# 印出美化後的 HTML,方便檢視
print(soup_article_list.prettify())

# 定義爬取單一文章的函式
def article_crawler(url):
    # 發送 GET 請求到文章頁面
    response = requests.get(url, headers=headers, cookies=cookies)
    # 如果回應狀態碼不是 200,則結束函式
    if response.status_code != 200:
        return
    
    # 解析文章頁面的 HTML 內容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 印出正在爬取的文章 URL
    print("=" * 30)
    print("爬取 " + url + " 文章內容，並暫停 1 秒")
    print("=" * 30)
    
    # 初始化儲存文章資訊的字典
    article = {
        'author_id': '',
        'author_nickname': '',
        'title': '',
        'timestamp': '',
        'contents': '',
        'ip': ''
    }
    
    # 找到文章主體
    article_body = soup.find(id='main-content')

    # 找到文章的中繼資訊(作者、標題、時間)
    article_head = article_body.findAll('div', class_='article-metaline')
    # 遍歷中繼資訊
    for metaline in article_head:
        # 取得中繼標籤(作者、標題、時間)
        meta_tag = metaline.find(class_='article-meta-tag').text
        # 取得對應的值
        meta_value = metaline.find(class_='article-meta-value').text
        # 根據標籤類型,將值存入 article 字典
        if meta_tag == '作者':
            # 使用正規表達式分離作者 ID 和暱稱
            compile_nickname = re.compile('\((.*)\)').search(meta_value)
            article['author_id'] = meta_value.split('(')[0].strip(' ')
            article['author_nickname'] = compile_nickname.group(1) if compile_nickname else ''
        elif meta_tag == '標題':
            article['title'] = meta_value
        elif meta_tag == '時間':
            article['timestamp'] = meta_value

    # 提取文章內容,去除標頭和推文
    contents = [expr for expr in article_body.contents if isinstance(expr, NavigableString)]
    contents = [re.sub('\n', '', expr) for expr in contents]  # 移除換行符
    contents = [i for i in contents if i]  # 移除空字串
    contents = '\n'.join(contents)  # 合併內容
    article['contents'] = contents

    # 提取文章發布 IP
    article_ip = article_body.find(class_='f2').text
    # 使用正規表達式找出 IP
    compile_ip = re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}').search(article_ip)
    article['ip'] = compile_ip.group(0) if compile_ip else ''

    # 暫停 1 秒,避免過於頻繁的請求
    time.sleep(1)

    # 印出正在爬取留言的提示
    print("=" * 30)
    print("爬取 " + url + " 留言內容，並暫停 1 秒")
    print("=" * 30)
    
    # 初始化儲存留言的列表
    comments = []
    # 遍歷所有留言
    for comment in article_body.findAll('div', class_='push'):
        # 提取留言的各項資訊
        tag = comment.find(class_='push-tag').text
        guest_id = comment.find(class_='push-userid').text
        guest_content = comment.find(class_='push-content').text
        guest_ipdatetime = comment.find(class_='push-ipdatetime').text
        # 使用正規表達式提取 IP
        compile_ip = re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}').search(guest_ipdatetime)
        guest_ip = compile_ip.group(0) if compile_ip else ''
        # 提取時間戳,去除 IP
        guest_timestamp = re.sub(guest_ip, '', guest_ipdatetime).strip()
        # 將留言資訊加入 comments 列表
        comments.append({
            'tag': tag,
            'id': guest_id,
            'content': guest_content,
            'ip': guest_ip,
            'timestamp': guest_timestamp
        })

    # 再次暫停 1 秒
    time.sleep(1)

    # 將留言列表和文章 URL 加入 article 字典
    article['comments'] = comments
    article['url'] = url
    return article

# 初始化儲存所有文章資料的列表
data = []
# 遍歷搜尋結果頁面中的每篇文章
for article_line in soup_article_list.findAll('div', class_='r-ent'):
    title_tag = article_line.find('div', class_='title')
    # 提取文章 URL
    article_url = title_tag.find('a')['href']
    # 組合完整的文章 URL
    article_url = urljoin(resp_article_list.url, article_url)
    # 爬取文章內容
    article_data = article_crawler(article_url)
    # 將文章資料加入 data 列表
    data.append(article_data)

# 將爬取的資料寫入 JSON 檔案
with open('search_results_by_keyword.json', 'w+', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)