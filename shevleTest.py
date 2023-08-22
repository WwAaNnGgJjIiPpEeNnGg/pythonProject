import shelve

# 创建一个 shelve 文件
with shelve.open('mydata') as db:
    db['name'] = 'John'
    db['age'] = 30
    db['city'] = 'New York'

# 从 shelve 文件中读取数据
with shelve.open('mydata') as db:
    name = db['name']
    age = db['age']
    city = db['city']

print(f"Name: {name}, Age: {age}, City: {city}")
