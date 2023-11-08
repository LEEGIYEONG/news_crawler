from bs4 import BeautifulSoup
import requests
import time
import json

# 키워드 리스트
keyword_list = ["반도체", "이차전지", "수소", "우주", "인공지능", "로봇"]

# 각 키워드에 대해 월별 뉴스 타이틀 리스트를 저장할 데이터 구조
titles = {keyword: [[] for _ in range(5)] for keyword in keyword_list}

user_agent = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    "Referer": "https://www.google.com"
}

# 상반기
for keyword_index, keyword in enumerate(keyword_list):
    for year in range(2021, 2024):  # 2021년부터 2023년까지
        for page in range(1, 11):  # 1페이지부터 10페이지까지
            start = (page - 1) * 10 + 1
            url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query={}&sort=0&photo=0&field=0&pd=3&ds={}.01.01&de={}.06.30&cluster_rank=749&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:from{}0101to{}0630,a:all&start={}".format(
                keyword, year, year, year, year, start)
            res = requests.get(url, headers=user_agent)
            soup = BeautifulSoup(res.text, "html.parser")
            print(res.status_code)  # HTTP 상태 코드 확인

            for link in soup.find_all('a', class_='news_tit'):
                title = link.get('title')
                index = (year - 2021) * 2
                titles[keyword][index].append(title)
            print(year, index, titles[keyword][index])

            time.sleep(3)

# 하반기
for keyword_index, keyword in enumerate(keyword_list):
    for year in range(2021, 2023):  # 2021년부터 2022년까지
        for page in range(1, 11):  # 1페이지부터 30페이지까지
            start = (page - 1) * 10 + 1
            url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query={}&sort=0&photo=0&field=0&pd=3&ds={}.07.01&de={}.12.31&cluster_rank=749&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:from{}0701to{}1231,a:all&start={}".format(
                keyword, year, year, year, year, start)
            res = requests.get(url, headers=user_agent)
            soup = BeautifulSoup(res.text, "html.parser")
            print(res.status_code)  # HTTP 상태 코드 확인

            for link in soup.find_all('a', class_='news_tit'):
                title = link.get('title')
                index = (year - 2021) * 2 + 1
                titles[keyword][index].append(title)
            print(year, index, titles[keyword][index])

            time.sleep(4)

with open('titles.json', 'w') as file:
    json.dump(titles, file)


# with open('titles.json', 'r', encoding='utf-8') as file:
#    titles = json.load(file)

# #titles["반도체"][0]는 반도체 2021년 상반기 기사제목 100개가 있는 리스트
# #titles["로봇"][3]는 로봇 2022년 하반기 기사제목 100개가 있는 리스트
# #리스트는 주제별, 2021년 상반기부터 2023년 상반기까지 5개 기간, 기사제목 100개로 구성

# print(titles["반도체"][0])
