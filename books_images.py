import requests
from bs4 import BeautifulSoup
import csv
import os

# 設定目標 URL
url = "https://www.books.com.tw/web/sys_saletopb/books/"

# 發送 GET 請求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}
response = requests.get(url, headers=headers)

# 使用 BeautifulSoup 解析 HTML 內容
soup = BeautifulSoup(response.text, 'html.parser')

# 創建一個目錄來儲存圖片
if not os.path.exists('book_covers'):
    os.makedirs('book_covers')

# 準備 CSV 文件
with open('books_ranking.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['排名', '書名', '作者', '折扣','價格'])

# 找到包含所有書籍的 div 元素
book_list = soup.find('div', class_='grid_20 push_4 main_column alpha')

if book_list:
    # 找到所有的書籍項目
    books = book_list.find_all('li', class_='item')

    for book in books:

        # 提取排名
        rank_elem = book.find('strong', class_='no')
        rank = rank_elem.text if rank_elem else "排名未找到"

        # 提取書名
        title_elem = book.find('h4').find('a')
        title = title_elem.text if title_elem else "書名未找到"

        # 提取圖片
        image_elem = book.find('img', class_='cover')
        image_url = image_elem['src'] if image_elem else "圖片未找到"
        print(image_url)

        # 下載圖片
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            with open(f'book_covers/{title}.jpg', 'wb') as f:
                f.write(image_response.content)

        # 提取作者
        author_elem = book.find('ul', class_='msg').find('li').find('a')
        author = author_elem.text if author_elem else "作者未找到"

        # 提取金額
        price_elem = book.find('li', class_='price_a').find_all('b')
        if len(price_elem) == 2:
            discount = price_elem[0].text if price_elem else "折扣未找到"
            price = price_elem[1].text if price_elem else "金額未找到"
        else:
            discount = "折扣未找到"
            price = price_elem[0].text if price_elem else "金額未找到"

        # 將資料寫入 CSV 文件
        with open('books_ranking.csv', 'a', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([rank, title, author, discount, price])

print("爬取完成，資料已保存到 books_ranking.csv，圖片已下載到 book_covers 目錄")