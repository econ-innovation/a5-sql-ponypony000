import json
import sqlite3
import requests

#定义获取企业位置信息的函数
def get_location(x):
    # 构建请求 指定返回的数据格式为JSON
    key = "5ea71aaec2f483badb692869abe47bb9"
    url = f'https://restapi.amap.com/v3/geocode/geo?address={x}&output=JSON&key={key}'
    # 发送请求
    response = requests.get(url)
    # 打印响应结果
    print(response.text)
    # 解析数据
    json_data = json.loads(response.text)
    # 获取地理信息
    geo = json_data["geocodes"][0]["location"]
    # geo_d = json_data["geocodes"][0]["formatted_address"]
    return geo

# 连接到名为address.db的SQLite数据库
conn = sqlite3.connect('address.db')
# 创建游标对象
cur = conn.cursor()
# 创建表格address sql
cur.execute("CREATE TABLE address(line_location TEXT,location TEXT);")

#获取位置并写入数据库
with open("address.txt","r",encoding='utf-8') as f:
    for line in f.readlines():
        line_location = line.strip() # 去除可能的空格和换行符
        location = get_location(line)
        #创建list
        data = [line_location,location]
        # 写入数据
        cur.execute("INSERT INTO address VALUES (?,?)",data)

#提交改动
conn.commit() #对数据库做改动后（比如建表、插数等），都需要手动提交改动，否则无法将数据保存到数据库。
# 关闭游标
cur.close()
# 关闭连接
conn.close()

#参考python循环往sqlite3数据库中写数据
#https://wenku.csdn.net/answer/ad935de31c7845fda795d33d1b4ddecc