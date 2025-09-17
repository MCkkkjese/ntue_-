"""
搜尋結果的情感分析
說明
對搜尋結果的描述進行情感分析，判斷正面、負面或中性情緒。
"""
# 導入所需的庫
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote
from pprint import pprint
from textblob import TextBlob  # 導入 TextBlob 用於情感分析

class GoogleSpider(object):
    def __init__(self):
        # 初始化 GoogleSpider 類別
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:79.0) Gecko/20100101 Firefox/79.0',
            'Host': 'www.google.com',
            'Referer': 'https://www.google.com/'
        }

    def __get_source(self, url: str) -> requests.Response:
        # 私有方法：獲取指定 URL 的網頁源碼
        return requests.get(url, headers=self.headers)

    def analyze_sentiment(self, text: str) -> str:
        # 使用 TextBlob 進行情感分析
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity

        if polarity > 0.1:
            return "正面"
        elif polarity < -0.1:
            return "負面"
        else:
            return "中性"

    def search(self, query: str) -> list:
        # 執行 Google 搜尋並解析結果
        response = self.__get_source(f'https://www.google.com/search?q={quote(query)}')
        soup = BeautifulSoup(response.text, 'html.parser')
        result_containers = soup.find_all('div', class_='g')
        results = []

        for container in result_containers:
            title_element = container.find('h3')
            url_element = container.find('a')
            des_element = container.find('div', class_='VwiC3b')

            if title_element and url_element:
                title = title_element.text.strip()
                url = url_element['href']
                des = des_element.text.strip() if des_element else "沒有可用的描述"

                # 進行情感分析
                sentiment = self.analyze_sentiment(des)

                print(f"標題: {title}")
                print(f"網址: {url}")
                print(f"描述: {des}")
                print(f"情感: {sentiment}")
                print("---")

                results.append({
                    'title': title,
                    'url': url,
                    'des': des,
                    'sentiment': sentiment
                })

        return results

if __name__ == '__main__':
    query = input('想搜尋什麼？ ')
    results = GoogleSpider().search(query)
    if results:
        print("\n搜尋結果:")
        pprint(results)
    else:
        print("沒有找到結果或處理搜尋結果時出現錯誤。")