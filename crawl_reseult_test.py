import json

with open('titles.json', 'r', encoding='utf-8') as file:
    titles = json.load(file)
# titles["반도체"][0]는 반도체 2021년 상반기 기사제목 100개가 있는 리스트
# titles["로봇"][3]는 로봇 2022년 하반기 기사제목 100개가 있는 리스트
# 리스트는 주제별, 2021년 상반기부터 2023년 상반기까지 5개 기간, 기사제목 100개로 구성

print(titles["반도체"][0])
