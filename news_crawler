from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta


def date_cleansing(test, date_text):
    try:
        pattern = '\\\\d+.(\\\\d+).(\\\\d+).'
        r = re.compile(pattern)
        match = r.search(test).group(0)
        date_text.append(match)
    except AttributeError:
        pattern = '\\\\w* (\\\\d\\\\w*)'
        r = re.search(test).group(1)
        date_text.append(match)


# 본문 내용 정제
def contents_cleansing(contents, contents_text):
    first_cleansing_contents = re.sub('<dl>.*?</a> </div> </dd> <dd>', '',
                                    str(contents)).strip()  #앞에 필요없는 부분 제거
    second_cleansing_contents = re.sub('<ul class="relation_lst">.*?</dd>', '',
                                    first_cleansing_contents).strip()#뒤에 필요없는 부분 제거 (새끼 기사)
    third_cleansing_contents = re.sub('<.+?>', '', second_cleansing_contents).strip()
    contents_text.append(third_cleansing_contents)
    return contents_text


# Crawler 함수를 만들기
def all_news_crawler(query, s_date, e_date):
    sort = '1'
    s_from = s_date.replace('.', '')
    e_to = e_date.replace(".", "")
    page_nm = 1
    last = False
    result_df = pd.DataFrame()

    while last == False:
        title_text = []
        link_text = []
        source_text = []
        date_text = []
        contents_text = []
        result = {}

        url = "https://search.naver.com/search.naver?where=news&query=" + query + "&sort=" + sort + "&ds=" + s_date + "&de=" + e_date + "&nso=so%3Ar%2Cp%3Afrom" + s_from + "to" + e_to + "%2Ca%3A&start=" + str(
            page_nm)

        response = requests.get(url)
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')
        # <a>태그에서 제목과 링크주소 추출
        atags = soup.select('.news_tit')
        for atag in atags:
            title_text.append(atag.text)  # 제목
            link_text.append(atag['href'])  # 링크주소

        # 신문사 추출
        source_lists = soup.select('.info_group > .press')
        for source_list in source_lists:
            source_text.append(source_list.text)  # 신문사

        # 날짜 추출
        date_lists = soup.select('.info_group > span.info')
        for date_list in date_lists:
            # 1면 3단 같은 위치 제거
            if date_list.text.find("면") == -1:
                date_text.append(date_list.text)
                # date_cleansing(date_text)

        # 본문 요약
        contents_lists = soup.select('.news_dsc')
        for contents_list in contents_lists:
            contents_cleansing(contents_list, contents_text)  # 본문요약 정제화

        # 모든 리스트 딕셔너리형태로 저장
        result = {"search": query, "newsDate": date_text, "title": title_text, "source": source_text, "contents": contents_text,"link": link_text}

        today = datetime.now().strftime('%Y-%m-%d-%H')
        date_cal = datetime.strptime(today, '%Y-%m-%d-%H')
        print(result['newsDate'])
        
        # 날짜 형식 통일 (~일 전, ~시간 전)
        for i in range(len(result['newsDate'])):
            if result['newsDate'][i][-3:] == '일 전':
                result['newsDate'][i] = (date_cal - relativedelta(days=int(result['newsDate'][i][0]))).strftime(
                    '%Y.%m.%d.')
            elif result['newsDate'][i][-4:] in '시간 전':
                result['newsDate'][i] = (date_cal - relativedelta(hours=int(result['newsDate'][i][:-4]))).strftime(
                    '%Y.%m.%d.')
            elif result['newsDate'][i][-2:] in '분':
                result['newsDate'][i] = (date_cal - relativedelta(minutes=int(result['newsDate'][i][:-2]))).strftime(
                    '%Y.%m.%d.')
            elif result['newsDate'][i][-3:] in '분 전':
                result['newsDate'][i] = (date_cal - relativedelta(minutes=int(result['newsDate'][i][:-3]))).strftime(
                    '%Y.%m.%d.')
            else:
                result['newsDate'][i] = result['newsDate'][i]

            result['newsDate'][i] = result['newsDate'][i][:-1]

        df = pd.DataFrame(result)

        result_df = pd.concat((result_df, df), ignore_index=True, axis=0)

        # 마지막 페이지 확인
        last_page = soup.find('div', {'class': 'group_news'})

        if last_page is None:
            last == True
            print(page_nm)
            break
        else:
            page_nm += 10
            print(page_nm)

    # 중복 행 지우기
    result_df = result_df.drop_duplicates(keep='first', ignore_index=True)
    print("중복 제거 후 행 개수: ", len(result_df))
    return result_df

test_result = all_news_crawler(query='6G',s_date='2023.11.07',e_date='2023.11.07')
test=test_result.to_excel('test.xlsx')
test
