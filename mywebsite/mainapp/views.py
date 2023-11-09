from django.shortcuts import render
from django.conf import settings
import requests
import json
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
from collections import Counter
import numpy as np

KEYWORDS = ["반도체", "이차전지", "수소", "우주", "로봇", "인공지능"]
COLORS = ['orange', 'darkturquoise', '#ffc000', '#8fd9b6', '#ff9999', '#d395d0'] 

# 원형 차트 그리기
def makeCirCularGraph(contents):
    #부채꼴 모양 설정
    wedgeprops={'width': 0.7, 'edgecolor': 'w', 'linewidth': 5}

    labels = KEYWORDS
    frequency = []
    for keyword in KEYWORDS:
        frequency.append(sum(contents[keyword]))
    labels_frequency = zip(KEYWORDS,frequency,COLORS) 

    fig = plt.figure(figsize=(8,8))
    fig.set_facecolor('white') 
    ax = fig.add_subplot() 

    pie = ax.pie(frequency, 
                 startangle=90,
                 counterclock=False, 
                 labels = labels,
                 textprops={'size':15},
                 wedgeprops=wedgeprops,
                 colors = COLORS)

    total = np.sum(frequency) 

    threshold = 5
    sum_pct = 0 
    count_less_5pct = 0 ## 5%보다 작은 라벨의 개수
    spacing = 0.1
    for i,l in enumerate(labels):    
        ang1, ang2 = ax.patches[i].theta1, ax.patches[i].theta2 ## 파이의 시작 각도와 끝 각도    
        center, r = ax.patches[i].center, ax.patches[i].r ## 파이의 중심 좌표        

        ## 비율 상한선보다 작은 것들은 계단형태로 만든다.    
        if frequency[i]/total*100 < threshold:        
            x = (r/2+spacing*count_less_5pct)*np.cos(np.pi/180*((ang1+ang2)/2)) + center[0] ## 텍스트 x좌표        
            y = (r/2+spacing*count_less_5pct)*np.sin(np.pi/180*((ang1+ang2)/2)) + center[1] ## 텍스트 y좌표        
            count_less_5pct += 1    
        else:        
            x = (r/2)*np.cos(np.pi/180*((ang1+ang2)/2)) + center[0] ## 텍스트 x좌표        
            y = (r/2)*np.sin(np.pi/180*((ang1+ang2)/2)) + center[1] ## 텍스트 y좌표        

        ## 퍼센티지 출력    
        if i < len(labels) - 1:        
            sum_pct += float(f'{frequency[i]/total*100:.2f}')        
            ax.text(x,y,f'{frequency[i]/total*100:.2f}%',ha='center',va='center',fontsize=12)    
        else: ## 마지막 파이 조각은 퍼센티지의 합이 100이 되도록 비율을 조절        
            ax.text(x,y,f'{100-sum_pct:.2f}%',ha='center',va='center',fontsize=12) 

    ax.tick_params(colors='white')

    plt.legend(bbox_to_anchor=(1.1,0.2), loc='center right', fontsize=10) 
    plt.savefig('static/chart/pie_chart.png')

# 꺽은선 그래프 파일 만들기 
def makeLineGraph(contents):

    x = []
    for i in range(1, 32):
        x.append("{}일".format(i))

    fig = plt.figure(figsize=(20,10),facecolor='white')
    for i in range(len(KEYWORDS)):
        plt.plot(x, contents[KEYWORDS[i]], color=COLORS[i], linewidth=1.5, linestyle='-',marker='o',markersize=8, markerfacecolor="white", markeredgewidth=1.5,label= contents[KEYWORDS[i]])

    plt.legend(KEYWORDS, loc='center right', fontsize=10) 
    plt.savefig('static/chart/line_chart.png')

def main_page(request):

    #한글 폰트 설정
    font_path = "static/fonts/gulim.ttc"  # 한글 폰트 파일 경로
    font_prop = font_manager.FontProperties(fname=font_path)
    rc('font', family=font_prop.get_name())

    with open('static/crawling/keyword_news_counting_by_day_for_202310.json', 'r') as file:
        contents = json.load(file)

    makeCirCularGraph(contents)
    makeLineGraph(contents)

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
