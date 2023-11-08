from bs4 import BeautifulSoup
import requests
import time
import json

# 키워드 리스트
keyword_list = ["반도체", "이차전지", "수소", "우주", "인공지능", "로봇"]

# 각 키워드에 대해 월별 뉴스 타이틀 리스트를 저장할 데이터 구조
titles_2023_2 = {keyword: [] for keyword in keyword_list}

user_agent = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    "Referer": "https://www.google.com"
}


for keyword in keyword_list:
    for year in range(2023, 2024):  # 2021년부터 2022년까지
        for page in range(1, 11):  # 1페이지부터 30페이지까지
            start = (page - 1) * 10 + 1
            url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query={}&sort=0&photo=0&field=0&pd=3&ds=2023.07.01&de=2023.10.31&cluster_rank=749&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:from230701to231031,a:all&start={}".format(
                keyword, start)
            res = requests.get(url, headers=user_agent)
            soup = BeautifulSoup(res.text, "html.parser")
            print(res.status_code)  # HTTP 상태 코드 확인

            for link in soup.find_all('a', class_='news_tit'):
                title = link.get('title')
                titles_2023_2[keyword].append(title)
            print(year, titles_2023_2[keyword])

            time.sleep(4)

with open('titles_2023_2.json', 'w') as file:
    json.dump(titles_2023_2, file)

# import json

# with open('mywebsite/crawling/titles_2023_2.json', 'r', encoding='utf-8') as file:
#    titles_2023_2 = json.load(file)

# print(titles_2023_2["반도체"])
