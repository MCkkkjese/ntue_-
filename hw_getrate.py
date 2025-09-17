# 匯入 requests 套件
import requests
# 匯入 BeautifulSoup 套件
from bs4 import BeautifulSoup
# 匯入 json 套件
import json
# 匯入 pandas 套件
import pandas as pd

url = "https://rate.bot.com.tw/xrt?Lang=zh-TW"

resp = requests.get(url)
resp.encoding = 'utf-8'
soup = BeautifulSoup(resp.text, 'html.parser')

# find the table
table = soup.find('table', {'class': 'table table-striped table-bordered table-condensed table-hover'})

# find the table head
thead = table.find('thead')
colname = table.find_all('th', {'class': 'display_none_print_show print_width'})
# 抓取欄位名稱
colname = [i.text for i in colname]
# 修改欄位名稱
col1 = "現金匯率"
col2 = "即期匯率"
for i in range(2, 4):
    colname[i] = col1 + colname[i]
for i in range(4, 6):
    colname[i] = col2 + colname[i]
colname.pop(0)
colname.pop(0)
colname.insert(0, "幣別")
print(colname)

# find the table body
tbody = table.find('tbody')

# find all the rows
rows = tbody.find_all('tr')
rows = [list(row.stripped_strings) for row in rows]

data = []
for row in rows:
    data.append(row[1:6])

df = pd.DataFrame(data, columns=colname)
df.to_excel('rate.xlsx', index=False, engine='openpyxl')

# create a list to store the data
# data = []

# loop through the rows
# for row in rows:
#     # find all the columns
#     cols = row.find_all('td')
#     # get the currency name
#     currency = cols[0].text.strip()
#     # get the currency rate
#     rate = cols[2].text.strip()
#     # append the data to the list
#     data.append([currency, rate])