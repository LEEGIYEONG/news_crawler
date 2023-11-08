# import requests
import time
import json
import pymysql

db = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="비밀번호 입력", ## 로컬 사용시 개인 DB 비밀번호 입력.
    database="test_db3",
    charset='utf8'
)
cursor = db.cursor()
cursor.execute("CREATE TABLE newsTable (id int primary key not null auto_increment, Topic varchar(100), Period char(100), Title varchar(200))")
db.commit()

file_path = "C:/Users/sjhj8/Desktop/Projects/news_crawler/titles.json"

with open(file_path, "r", encoding="utf-8") as file:
    topics = json.load(file)
    # print(titles["반도체"][0][0])
    
    for topic in topics:
        save_topic = topic
        for period in range(len(topics[topic])):
            if period == 0:
                save_period = "2021 상반기"
            elif period == 1:
                save_period = "2021 하반기"
            elif period == 2:
                save_period = "2022 상반기"
            elif period == 3:
                save_period = "2022 하반기"
            elif period == 4:
                save_period = "2023 상반기" 
            for i in range(100):
                print(save_topic, save_period, topics[topic][period][i])
                
                sql = "INSERT INTO newsTable(Topic, Period, Title) VALUES (%s, %s, %s)"
                val = (save_topic, save_period, topics[topic][period][i])
                cursor.execute(sql, val)
                db.commit()
    
print(cursor.rowcount, "record inserted")