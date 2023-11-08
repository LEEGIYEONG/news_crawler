from django.shortcuts import render
from wordcloud import WordCloud
import requests
from bs4 import BeautifulSoup

def main_page(request):
    return render(request, 'mainapp/main_page.html')

def space(request):
    # 뉴스 웹 사이트에서 뉴스 데이터 크롤링 (예시: 네이버 뉴스)
    news_url = "https://news.naver.com/"
    response = requests.get(news_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 뉴스 데이터 추출
    news_text = ""
    for headline in soup.find_all('strong', {'class': 'headline'}):
        news_text += headline.get_text() + " "

    # 워드 클라우드 생성
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(news_text)

    # 워드 클라우드 이미지를 저장
    wordcloud_image_path = 'mainapp/static/mainapp/wordcloud.png'
    wordcloud.to_file(wordcloud_image_path)

    # 워드 클라우드 이미지의 URL
    wordcloud_image_url = '/static/mainapp/wordcloud.png'

    return render(request, 'mainapp/space.html', {'wordcloud_image_url': wordcloud_image_url})

def semiconductor(request):
    # 'semiconductor' 서브페이지 뷰 로직을 작성
    return render(request, 'mainapp/semiconductor.html')

def hydrogen(request):
    # 'hydrogen' 서브페이지 뷰 로직을 작성
    return render(request, 'mainapp/hydrogen.html')

def ai(request):
    # 'ai' 서브페이지 뷰 로직을 작성
    return render(request, 'mainapp/ai.html')

def robot(request):
    # 'robot' 서브페이지 뷰 로직을 작성
    return render(request, 'mainapp/robot.html')

def battery(request):
    # 'battery' 서브페이지 뷰 로직을 작성
    return render(request, 'mainapp/battery.html')