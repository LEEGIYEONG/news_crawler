from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import sys
[sys.path.append(i) for i in ['.', '..']]
from datetime import date, timedelta
import datetime
import json
import time


def news_attrs_crawler(articles, attrs):
    attrs_content = []
    for i in articles:
        attrs_content.append(i.attrs[attrs])
    return attrs_content

# ConnectionError방지
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}

# html생성해서 기사크롤링하는 함수 만들기(url): 링크를 반환
def articles_crawler(url):
    # html 불러오기
    original_html = requests.get(url, headers=headers)
    html = BeautifulSoup(original_html.text, "html.parser")

    url_naver = html.select(
        "div.group_news > ul.list_news > li div.news_area > div.news_info > div.info_group > a.info")
    url = news_attrs_crawler(url_naver, 'href')
    return url

# 제목, 링크, 내용 1차원 리스트로 꺼내는 함수 생성
def makeList(newlist, content):
    for i in content:
        for j in i:
            newlist.append(j)
    return newlist

def naver_news_crawler_last_month(query, s_date, e_date):
    s_from = s_date.replace('.', '')
    e_to = e_date.replace(".", "")
    sort = '1'
    page_nm = 1
    last = False

    collect_df = pd.DataFrame()
    while last == False:
        news_titles = []
        news_url = []
        news_dates = []

        url = "https://search.naver.com/search.naver?where=news&query=" + query + "&sort=" + sort + "&ds=" + s_date + "&de=" + e_date + "&nso=so%3Ar%2Cp%3Afrom" + s_from + "to" + e_to + "%2Ca%3A&start=" + str(
            page_nm)

        news_url = articles_crawler(url)

        # NAVER 뉴스만 남기기
        final_urls = []
        for i in range(len(news_url)):
            if "news.naver.com" in news_url[i]:
                final_urls.append(news_url[i])
            else:
                pass

        for i in final_urls:
            # 각 기사 html get하기
            news = requests.get(i, headers=headers, verify=True)
            news_html = BeautifulSoup(news.text, "html.parser")

            # 뉴스 제목 가져오기
            title = news_html.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_title > h2")
            if title == None:
                title = news_html.select_one("#content > div.end_ct > div > h2")

            # html태그제거 및 텍스트 다듬기
            pattern1 = '<[^>]*>'
            title = re.sub(pattern=pattern1, repl='', string=str(title))

            news_titles.append(title)

            try:
                html_date = news_html.select_one(
                    "div#ct> div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span")
                news_date = html_date.attrs['data-date-time']
            except AttributeError:
                news_date = news_html.select_one("#content > div.end_ct > div > div.article_info > span > em")
                news_date = re.sub(pattern=pattern1, repl='', string=str(news_date))

            # 날짜 형식 맞추고 가져오기
            news_date = news_date.replace('.', '')
            news_date = news_date.replace('-', '')
            news_date = news_date[:8]

            news_dates.append(news_date)

        news_df = pd.DataFrame({'date': news_dates, 'keyword' : query, 'title': news_titles})
        collect_df = pd.concat((collect_df, news_df), ignore_index=True, axis=0)

        # 마지막 페이지를 가져오기
        response = requests.get(url)
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')

        last_page = soup.find('div', {'class': 'group_news'})

        if last_page is None:
            last == True
            print(page_nm)
            break
        else:
            page_nm += 10
            print(page_nm)

    return collect_df

def naver_news_crawler_today(query, s_date, e_date):
    s_from = s_date.replace('.', '')
    e_to = e_date.replace(".", "")
    sort = '1'
    page_nm = 1
    last = False

    collect_df = pd.DataFrame()
    while last == False:
        news_titles = []
        news_url = []
        news_dates = []

        url = "https://search.naver.com/search.naver?where=news&query=" + query + "&sort=" + sort + "&ds=" + s_date + "&de=" + e_date + "&nso=so%3Ar%2Cp%3Afrom" + s_from + "to" + e_to + "%2Ca%3A&start=" + str(
            page_nm)

        news_url = articles_crawler(url)

        # NAVER 뉴스만 남기기
        final_urls = []
        for i in range(len(news_url)):
            if "news.naver.com" in news_url[i]:
                final_urls.append(news_url[i])
            else:
                pass

        for i in final_urls:
            # 각 기사 html get하기
            news = requests.get(i, headers=headers, verify=True)
            news_html = BeautifulSoup(news.text, "html.parser")

            # 뉴스 제목 가져오기
            title = news_html.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_title > h2")
            if title == None:
                title = news_html.select_one("#content > div.end_ct > div > h2")

            # html태그제거 및 텍스트 다듬기
            pattern1 = '<[^>]*>'
            title = re.sub(pattern=pattern1, repl='', string=str(title))

            news_titles.append(title)

            try:
                html_date = news_html.select_one(
                    "div#ct> div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span")
                news_date = html_date.attrs['data-date-time']
            except AttributeError:
                news_date = news_html.select_one("#content > div.end_ct > div > div.article_info > span > em")
                news_date = re.sub(pattern=pattern1, repl='', string=str(news_date))

            # 날짜 형식 맞추고 가져오기
            news_date = news_date.replace('.', '')
            news_date = news_date.replace('-', '')
            news_date = news_date[:8]

            news_dates.append(news_date)

        news_df = pd.DataFrame({'date': news_dates, 'keyword' : query, 'title': news_titles, 'link': final_urls})
        collect_df = pd.concat((collect_df, news_df), ignore_index=True, axis=0)

        # 마지막 페이지를 가져오기
        response = requests.get(url)
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')

        last_page = soup.find('div', {'class': 'group_news'})

        if last_page is None:
            last == True
            print(page_nm)
            break
        else:
            page_nm += 10
            print(page_nm)

    return collect_df

def job_last_month_newsCrawling():

    # 하루씩 크롤링해오기
    query_list = ["반도체"]

    for query in query_list:
        result_df = pd.DataFrame()
        result = {}  # 결과를 누적할 딕셔너리

        start_date = datetime.datetime(2023, 10, 1)
        end_date = datetime.datetime(2023, 10, 11)

        while start_date <= end_date:
            s_date = start_date.strftime('%Y.%m.%d')
            e_date = (start_date + datetime.timedelta(days=9)).strftime('%Y.%m.%d')  # 10일 단위로 설정
            
            # 크롤링 함수 호출
            collect_df = naver_news_crawler_last_month(query, s_date, e_date)
            
            # 결과 데이터프레임에 추가
            result_df = pd.concat([result_df, collect_df], axis=0, ignore_index=True)
            
            start_date += datetime.timedelta(days=10)  # 10일씩 증가
            
            # 일부 날짜 초기화 (마지막 구간이 10일 이하인 경우)
            if start_date > end_date:
                start_date = end_date + datetime.timedelta(days=1)

            time.sleep(3)  # 3초간 대기

        result_df = result_df.drop_duplicates(keep='first', ignore_index=True)
        result_df = result_df[result_df.date != 'None']
        print("{} crawling done".format(query))

        # 일별 그룹화, 카운팅
        grouped = result_df.groupby(['date', 'keyword']).size().reset_index(name='count')
        
        query_filename = f'{query}_keyword_news_data_by_day_for_202310.json'
        
        for _, row in grouped.iterrows():
            date = row['date']
            keyword = row['keyword']
            count = row['count']

            if keyword not in result:
                result[keyword] = []

            result[keyword].append(count)   

        # json 형식으로 저장
        with open(query_filename, 'w') as json_file:
            json.dump(result, json_file, indent=4)
        
    return result_df

def job_today_newsCrawling():

    # 어제 날짜 구하기
    yesterday = (date.today() - timedelta(1)).strftime('%Y.%m.%d')

    # 하루씩 크롤링해오기
    query_list = ["반도체", "이차전지", "수소", "우주", "인공지능", "로봇"]

    result_df = pd.DataFrame()

    for query in query_list:

        query = query
        small_df = pd.DataFrame()

        s_date = yesterday
        e_date = yesterday

        collect_df = naver_news_crawler_today(query, s_date, e_date)

        small_df = pd.concat([small_df, collect_df], axis=0, ignore_index=True)

        # 중복 행 제거
        small_df = small_df.drop_duplicates(keep='first', ignore_index=True)
        small_df = small_df[small_df.date != 'None']
        print("{}_{} crawling done".format(query, e_date))

        result_df = pd.concat([result_df, small_df], axis=0, ignore_index=True)
        
        # 하루 동안 키워드 검색결과 json 파일 변환
        result_df.to_json('today_keyword_news_data.json', orient='records', lines=True)
        
        keyword_count = result_df['keyword'].value_counts().to_dict()

        # keyword 카운팅을 dict 형태로 변환
        estimate_dict = {keyword: keyword_count.get(keyword, 0)
                        for keyword in set(result_df['keyword'])}

        # 카운팅 결과 json 변환
        with open('today_keyword_news_counting.json', 'w') as json_file:
            json.dump(estimate_dict, json_file, indent=4)

    return result_df

# today_result=job_today_newsCrawling()
# print(today_result)
def crawl_and_save(query, cycle):
    result_df = pd.DataFrame()

    for day in range(1, 11):  # 각 사이클에서 10번의 크롤링 수행
        start_date = datetime.datetime(2023, 10, (cycle - 1) * 10 + day)
        end_date = datetime.datetime(2023, 10, (cycle - 1) * 10 + day)
        
        s_date = start_date.strftime('%Y.%m.%d')
        e_date = end_date.strftime('%Y.%m.%d')
        
        # 크롤링 함수 호출
        collect_df = naver_news_crawler_last_month(query, s_date, e_date)
        
        # 결과 데이터프레임에 추가
        result_df = pd.concat([result_df, collect_df], axis=0, ignore_index=True)
        
        time.sleep(5)  # 3초간 대기

    result_df = result_df.drop_duplicates(keep='first', ignore_index=True)
    result_df = result_df[result_df.date != 'None']

    # 일별 그룹화, 카운팅
    grouped = result_df.groupby(['date', 'keyword']).size().reset_index(name='count')
    
    # json 형식으로 저장
    json_filename = f'{query}_cycle{cycle}_keyword_news_counting_by_day_for_202310.json'
    with open(json_filename, 'w') as json_file:
        json.dump(grouped.to_dict(orient='records'), json_file, indent=4)
        
    return result_df

def job_last_month_newsCrawling():
    # 하루씩 크롤링해오기
    query_list = ["반도체", "이차전지", "수소", "우주", "인공지능", "로봇"]
    
    final_result_list = []

    for query in query_list:
        for cycle in range(1, 4):  # 3번의 사이클 수행
            result_df = crawl_and_save(query, cycle)
            final_result_list.append(result_df)

        # 각 쿼리에 대한 크롤링이 끝난 후에 휴식을 줄 수 있습니다.
        time.sleep(5)  # 5초간 대기

    # 최종 결과를 json 파일로 저장
    final_result_df = pd.concat(final_result_list, axis=0, ignore_index=True)
    final_grouped = final_result_df.groupby(['date', 'keyword']).size().reset_index(name='count')
    json_filename = f'{query_list}_combined_keyword_news_counting_by_day_for_202310.json'
    with open(json_filename, 'w') as json_file:
        json.dump(final_grouped.to_dict(orient='records'), json_file, indent=4)

    return final_result_df

# 키워드별 10월 일별 빈도스 카운트 함수 실행 
job_last_month_newsCrawling()

last_month_result = job_last_month_newsCrawling()
print(last_month_result)



# JSON 파일 합치는 함수
def merge_json_files(file_list, output_filename):
    merged_data = {}

    for file_name in file_list:
        with open(file_name, 'r') as file:
            data = json.load(file)
            keyword = data[0]['keyword']
            counts = [entry['count'] for entry in data]
            
            if keyword not in merged_data:
                merged_data[keyword] = counts
            else:
                merged_data[keyword] += counts

    with open(output_filename, 'w') as output_file:
        json.dump(merged_data, output_file, indent=4)

# JSON 파일리스트
json_files = [
    '수소_cycle1_keyword_news_counting_by_day_for_202310.json',
    '수소_cycle2_keyword_news_counting_by_day_for_202310.json',
    '수소_cycle3_keyword_news_counting_by_day_for_202310.json',
    '반도체_cycle1_keyword_news_counting_by_day_for_202310.json',
    '반도체_cycle2_keyword_news_counting_by_day_for_202310.json',
    '반도체_cycle3_keyword_news_counting_by_day_for_202310.json',
    '우주_cycle1_keyword_news_counting_by_day_for_202310.json',
    '우주_cycle2_keyword_news_counting_by_day_for_202310.json',
    '우주_cycle3_keyword_news_counting_by_day_for_202310.json',
    '이차전지_cycle1_keyword_news_counting_by_day_for_202310.json',
    '이차전지_cycle2_keyword_news_counting_by_day_for_202310.json',
    '이차전지_cycle3_keyword_news_counting_by_day_for_202310.json',
    '인공지능_cycle1_keyword_news_counting_by_day_for_202310.json',
    '인공지능_cycle2_keyword_news_counting_by_day_for_202310.json',
    '인공지능_cycle3_keyword_news_counting_by_day_for_202310.json',
    '로봇_cycle1_keyword_news_counting_by_day_for_202310.json',
    '로봇_cycle2_keyword_news_counting_by_day_for_202310.json',
    '로봇_cycle3_keyword_news_counting_by_day_for_202310.json'
    # Add the paths for the remaining JSON files
]

# 저장할 JSON 파일 이름 
output_json_filename = 'keyword_news_counting_by_day_for_202310.json'

# JSON 파일 합치기
merge_json_files(json_files, output_json_filename)

