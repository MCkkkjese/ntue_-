import requests
from bs4 import BeautifulSoup as bs

new_url = int(input("請輸入最新的網頁網址編號："))
url = f"https://www.ptt.cc/bbs/Baseball/index{new_url}.html"

for i in range(new_url):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
    }

    session = requests.Session()
    session.cookies.update({"over18": "1"})

    response = session.get(url, headers=headers)
    soup = bs(response.text, "html.parser")

    post_data = []
    url_data = []

    for div in soup.find_all("div", class_="r-ent"):
        title_tag = div.find("div", class_="title")
        a_tag = title_tag.find("a") if title_tag else None

        if a_tag:
            title = a_tag.text.strip()
            url = "https://www.ptt.cc" + a_tag["href"]
        else:
            title = "[已刪除]"
            url = ""

        author = div.find("div", class_="author").text.strip()
        date = div.find("div", class_="date").text.strip()
        nrec = div.find("div", class_="nrec").text.strip()

        if url:
            url_data.append(url)
        post_data.append((title, author, date, nrec, url))

    print("文章列表：")
    for p in post_data:
        print(p)

    content_data = []
    for url in url_data:
        response = session.get(url, headers=headers)
        soup = bs(response.text, "html.parser")

        content_div = soup.find("div", id="main-content")
        if content_div:
            content = content_div.text.strip()
            content_data.append(content)

    print("\n文章內文：")
    for i, content in enumerate(content_data):  
        print(f"--- 第 {i+1} 篇 ---")
        print(content)  

    new_url -= 1
    url = f"https://www.ptt.cc/bbs/Baseball/index{new_url}.html"