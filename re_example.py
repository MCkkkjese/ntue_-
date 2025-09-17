# 匯入 re 模組,用於處理正規表達式
import re

# 定義一個函式來測試正規表達式
def test_pattern(pattern, test_string):
    # 使用 re.search() 函式來尋找匹配項
    match = re.search(pattern, test_string)
    if match:
        print(f"匹配成功: '{match.group()}' 在位置 {match.start()}-{match.end() - 1}")
    else:
        print("沒有找到匹配項")

# 主程式
def main():
    # 1. 比對固定字串
    print("1. 比對固定字串")
    test_pattern(r"台灣", "我愛台灣")
    
    # 2. 比對數字
    print("\n2. 比對數字")
    test_pattern(r"\d+", "我的電話是 0912345678")
    
    # 3. 比對英文字母
    print("\n3. 比對英文字母")
    test_pattern(r"[a-zA-Z]+", "Hello 世界")
    
    # 4. 比對電子郵件地址
    print("\n4. 比對電子郵件地址")
    test_pattern(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "我的信箱是 example@email.com")
    
    # 5. 比對台灣手機號碼
    print("\n5. 比對台灣手機號碼")
    test_pattern(r"09\d{8}", "請撥打 0912345678 聯絡我")
    
    # 6. 比對台灣身分證字號
    print("\n6. 比對台灣身分證字號")
    test_pattern(r"[A-Z][12]\d{8}", "身分證字號是 A123456789")
    
    # 7. 比對日期格式(年/月/日)
    print("\n7. 比對日期格式(年/月/日)")
    test_pattern(r"\d{4}/\d{2}/\d{2}", "今天是 2023/10/08")
    
    # 8. 比對 IPv4 地址
    print("\n8. 比對 IPv4 地址")
    test_pattern(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b", "IP 地址是 192.168.0.1")
    
    # 9. 比對台灣郵遞區號
    print("\n9. 比對台灣郵遞區號")
    test_pattern(r"\d{3}(?:-\d{2})?", "郵遞區號是 106-09")
    
    # 10. 比對 HTML 標籤
    print("\n10. 比對 HTML 標籤")
    test_pattern(r"<([a-z]+)([^<]+)*(?:>(.*)<\/\1>|\s+\/>)", "<p>這是一個段落</p>")
    
    # 11. 比對台灣統一編號(公司行號)
    print("\n11. 比對台灣統一編號(公司行號)")
    test_pattern(r"\d{8}", "公司統一編號為 12345678")

# 如果這個腳本是直接執行的(而不是被匯入的),則執行 main() 函式
if __name__ == "__main__":
    main()