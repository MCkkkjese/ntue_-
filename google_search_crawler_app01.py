# 導入所需的模組
import requests  # 用於發送 HTTP 請求
from bs4 import BeautifulSoup  # 用於解析 HTML
from urllib.parse import urljoin, quote  # 用於處理 URL
from pprint import pprint  # 用於美化輸出
import sqlite3  # 用於操作 SQLite 資料庫

class DatabaseManager:
    def __init__(self, db_name):
        # 初始化資料庫管理器
        self.conn = sqlite3.connect(db_name)  # 建立資料庫連線
        self.cursor = self.conn.cursor()  # 建立游標物件
        self.create_table()  # 呼叫方法建立資料表

    def create_table(self):
        # 建立搜尋結果資料表（如果不存在）
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  # 自動遞增的主鍵
            query TEXT,  # 搜尋關鍵字
            title TEXT,  # 搜尋結果標題
            url TEXT,    # 搜尋結果網址
            description TEXT  # 搜尋結果描述
        )
        ''')
        self.conn.commit()  # 提交變更

    def insert_result(self, query, title, url, description):
        # 插入搜尋結果到資料表
        self.cursor.execute('''
        INSERT INTO search_results (query, title, url, description)
        VALUES (?, ?, ?, ?)
        ''', (query, title, url, description))
        self.conn.commit()  # 提交變更

    def close(self):
        # 關閉資料庫連線
        self.conn.close()

class GoogleSpider(object):
    def __init__(self, db_manager):
        # 初始化 Google 爬蟲
        self.headers = {
            # 設定 HTTP 請求標頭，模擬瀏覽器行為
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:79.0) Gecko/20100101 Firefox/79.0',
            'Host': 'www.google.com',
            'Referer': 'https://www.google.com/'
        }
        self.db_manager = db_manager  # 儲存資料庫管理器實例

    def __get_source(self, url: str) -> requests.Response:
        # 私有方法：獲取指定 URL 的網頁原始碼
        return requests.get(url, headers=self.headers)

    def search(self, query: str) -> list:
        # 執行 Google 搜尋並解析結果
        response = self.__get_source(f'https://www.google.com/search?q={quote(query)}')  # 發送搜尋請求
        soup = BeautifulSoup(response.text, 'html.parser')  # 解析 HTML
        result_containers = soup.find_all('div', class_='g')  # 找出所有搜尋結果容器
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
                des = des_element.text.strip() if des_element else "沒有可用的描述"

                # 輸出除錯資訊
                print(f"標題: {title}")
                print(f"網址: {url}")
                print(f"描述: {des}")
                print("---")

                # 將結果加入列表
                results.append({
                    'title': title,
                    'url': url,
                    'des': des
                })

                # 將結果儲存到資料庫
                self.db_manager.insert_result(query, title, url, des)

        return results  # 回傳搜尋結果列表

if __name__ == '__main__':
    # 主程式進入點
    db_manager = DatabaseManager('search_results.db')  # 建立資料庫管理器實例
    spider = GoogleSpider(db_manager)  # 建立 Google 爬蟲實例

    while True:
        query = input('想搜尋什麼？（輸入 q 退出） ')  # 取得使用者輸入
        if query.lower() == 'q':
            break  # 如果輸入 'q'，則退出迴圈

        results = spider.search(query)  # 執行搜尋
        if results:
            print("\n搜尋結果:")
            pprint(results)  # 美化輸出搜尋結果
        else:
            print("沒有找到結果或處理搜尋結果時出現錯誤。")

    db_manager.close()  # 關閉資料庫連線
    print("搜尋結果已儲存到 search_results.db 資料庫中。")