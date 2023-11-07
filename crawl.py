from bs4 import BeautifulSoup
import requests
import time

# 키워드 리스트
keyword_list = ["반도체", "디스플레이", "이차전지", "차세대원전", "수소",
                "5G", "6G", "바이오", "우주", "항공", "양자", "인공지능", "로봇", "사이버보안"]

# 각 키워드에 대해 월별 뉴스 타이틀 리스트를 저장할 데이터 구조
titles = {keyword: [[] for _ in range(12)] for keyword in keyword_list}

for keyword_index, keyword in enumerate(keyword_list):
    for i in range(1, 12):  # 1월부터 11월
        month = "{:02d}".format(i)
        for j in range(1, 51):  # 1페이지부터 50페이지까지
            start = (j - 1) * 10 + 1
            url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query={}&sort=0&photo=0&field=0&pd=3&ds=2023.{}.01&de=2023.{}.31&cluster_rank=749&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:from2023{}01to2023{}31,a:all&start={}".format(
                keyword, month, month, month, month, start)
            res = requests.get(url)
            soup = BeautifulSoup(res.text, "html.parser")
            # print(res.status_code)  # HTTP 상태 코드 확인
            # print(res.text)  # 반환된 HTML 확인
            for link in soup.find_all('a', class_='news_tit'):
                title = link.get('title')
                titles[keyword][i-1].append(title)

            time.sleep(1)

# 차단 안당하게 User-Agent를 추가하든가 스크래핑을 좀 나누든가 해야할 것 같습니다. 저대로 돌렸더니 차단당하네요ㅜㅜ
# 돌리실때는 i, j 범위를 줄여서 돌려보시는게 좋을 것 같습니다!
