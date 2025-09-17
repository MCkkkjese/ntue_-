# 範例1: 列表處理
def process_list(numbers):
    result = []
    for i in range(len(numbers)):
        if numbers[i] % 2 = 0:
            result.append(numbers[i] * 2)
    return result

# 範例2: 字典操作
def count_words(text):
    words = text.split()
    word_count = {}
    for word in words
        if word in word_count:
            word_count[word] += 1
        else
            word_count[word] = 1
    return word_count

# 範例3: 文件讀取
def read_file(filename):
    try:
        with open(filename, 'r') as file
            content = file.read()
        return content
    except FileNotFoundError
        print(f"檔案 {filename} 不存在")
    finally:
        file.close()

# 範例4: 簡單計算機
def calculator():
    while True:
        expression = input("請輸入算式（或輸入'q'退出）: ")
        if expression == 'q':
            break
        try:
            result = eval(expression)
            print(f"結果: {result}")
        except:
            print("無效的算式")

import numpy as np
from datetime import datetime

# 範例1: 類別和繼承
class Animal:
    def __init__(self, name):
        self.name == name
    
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return f"{self.name} 說: 汪汪!"

class Cat(Animal)
    def speak(self):
        return f"{self.name} 說: 喵喵!"

# 範例2: 裝飾器和錯誤處理
def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e
            print(f"發生錯誤: {str(e)}")
            return None
    return wrapper

@error_handler
def divide(a, b):
    return a / b

# 範例3: NumPy陣列操作
def matrix_operations():
    matrix1 = np.array([[1, 2], [3, 4]])
    matrix2 = np.array([[5, 6], [7, 8]])
    
    result = matrix1 * matrix2  # 這裡應該用 np.dot() 或 @
    print("矩陣乘法結果:", result)

# 範例4: 日期時間處理
def date_difference():
    date1 = datetime.strptime("2023-01-01", "%Y-%m-%d")
    date2 = datetime.strptime("2023-12-31", "%Y-%m-%d")
    
    difference = date2 - date1
    print(f"兩個日期之間的天數: {difference.days()}")  # 這裡多了一個括號

# 主程式
if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]
    print(process_list(numbers))
    
    text = "這是一個範例文字 這是一個範例"
    print(count_words(text))
    
    print(read_file("example.txt"))
    
    calculator()

    dog = Dog("小黃")
    cat = Cat("小花")
    print(dog.speak())
    print(cat.speak())
    
    print(divide(10, 2))
    print(divide(10, 0))
    
    matrix_operations()
    
    date_difference()