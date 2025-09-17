# 導入所需的庫
import requests  # 用於發送 HTTP 請求
from bs4 import BeautifulSoup  # 用於解析 HTML
from urllib.parse import urljoin, quote  # 用於 URL 處理
from pprint import pprint  # 用於美化輸出

class GoogleSpider(object):
    def __init__(self):
        # 初始化 GoogleSpider 類別
        self.headers = {
            # 設定 HTTP 請求標頭，模擬瀏覽器行為
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:79.0) Gecko/20100101 Firefox/79.0',
            'Host': 'www.google.com',
            'Referer': 'https://www.google.com/'
        }

    def __get_source(self, url: str) -> requests.Response:
        # 私有方法：獲取指定 URL 的網頁源碼
        return requests.get(url, headers=self.headers)

    def search(self, query: str) -> list:
        # 執行 Google 搜尋並解析結果
        # 構建搜尋 URL 並發送請求
        response = self.__get_source(f'https://www.google.com/search?q={quote(query)}')
        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        # 找出所有搜尋結果容器
        result_containers = soup.find_all('div', class_='g')
        results = []  # 儲存搜尋結果的列表

        for container in result_containers:
            # 在每個容器中尋找標題、URL 和描述元素
            title_element = container.find('h3')
            url_element = container.find('a')
            des_element = container.find('div', class_='VwiC3b')

            if title_element and url_element:
                # 如果找到標題和 URL，則提取資訊
                title = title_element.text.strip()
                url = url_element['href']
                # 如果找到描述則提取，否則使用預設文字
                des = des_element.text.strip() if des_element else "沒有可用的描述"

                # 輸出調試資訊
                print(f"標題: {title}")
                print(f"網址: {url}")
                print(f"描述: {des}")
                print("---")

                # 將結果添加到列表中
                results.append({
                    'title': title,
                    'url': url,
                    'des': des
                })

        return results  # 返回搜尋結果列表

if __name__ == '__main__':
    # 主程式入口點
    query = input('想搜尋什麼？ ')  # 獲取使用者輸入的搜尋詞
    results = GoogleSpider().search(query)  # 執行搜尋
    if results:
        print("\n搜尋結果:")
        pprint(results)  # 美化輸出搜尋結果
    else:
        print("沒有找到結果或處理搜尋結果時出現錯誤。")