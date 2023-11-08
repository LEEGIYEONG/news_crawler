from django.shortcuts import render
from django.conf import settings
import requests
import json

def main_page(request):
    return render(request, 'mainapp/main_page.html')

def my_view(request):
    # JSON 파일의 경로 가져오기
    json_file_path = settings.JSON_FILE_PATH

    # JSON 파일 읽어오기
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

def space(request):
    # 'space' 서브페이지 뷰 로직을 작성
    return render(request, 'mainapp/space.html')

def semiconductor(request):

    return render(request, 'mainapp/semiconductor.html', )

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