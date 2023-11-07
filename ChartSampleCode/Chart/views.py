from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import numpy as np

def generate_pie_chart(request):
    #한글 폰트 설정
    font_path = "templates/Fonts/gulim.ttc"  # 한글 폰트 파일 경로
    font_prop = font_manager.FontProperties(fname=font_path)
    rc('font', family=font_prop.get_name())

    colors = ['mistyrose','salmon','lightsalmon', 'tomato','lemonchiffon', 'khaki', 'gold', 'goldenrod', 'lightgreen','mediumseagreen', 'teal','paleturquoise','deepskyblue','dodgerblue']
            #   ['lightcoral','tomato','coral','orange','lemonchiffon','yellowgreen', 'darkseagreen','lightgreen','mediumseagreen','paleturquoise','teal','deepskyblue','lightsteelblue','cornflowerblue'] 
    labels = ['반도체', '디스플레이', '이차전지', '차세대원전', '수소', '5G', '6G', '바이오', '우주', '항공', '양자', '인공지능', '로봇', '사이버보안']
    frequency = [2000, 1500, 800, 560, 750, 400, 500, 512, 620, 800, 720, 1540, 2400, 1300]

    labels_frequency = zip(labels,frequency,colors) 
    labels_frequency = sorted(labels_frequency,key=lambda x: x[1],reverse=True) 
    sorted_labels = [x[0] for x in labels_frequency] 
    sorted_frequency = [x[1] for x in labels_frequency] 
    sorted_colors = [x[2] for x in labels_frequency] 

    fig = plt.figure(figsize=(8,8))
    fig.set_facecolor('white') 
    ax = fig.add_subplot() 

    # def customPct(pct):
    #     return ('%.1f%%' % pct) if pct >= 10 else ''

    pie = ax.pie(sorted_frequency, 
                # labels=sorted_labels,
                 startangle=90,
                #  autopct = customPct,
                 counterclock=False, 
                 textprops={'size':25},
                 colors = colors)
    
    total = np.sum(frequency) 
    
    threshold = 5
    sum_pct = 0 
    count_less_5pct = 0 ## 5%보다 작은 라벨의 개수
    spacing = 0.1
    for i,l in enumerate(sorted_labels):    
        ang1, ang2 = ax.patches[i].theta1, ax.patches[i].theta2 ## 파이의 시작 각도와 끝 각도    
        center, r = ax.patches[i].center, ax.patches[i].r ## 파이의 중심 좌표        
        
        ## 비율 상한선보다 작은 것들은 계단형태로 만든다.    
        if sorted_frequency[i]/total*100 < threshold:        
            x = (r/2+spacing*count_less_5pct)*np.cos(np.pi/180*((ang1+ang2)/2)) + center[0] ## 텍스트 x좌표        
            y = (r/2+spacing*count_less_5pct)*np.sin(np.pi/180*((ang1+ang2)/2)) + center[1] ## 텍스트 y좌표        
            count_less_5pct += 1    
        else:        
            x = (r/2)*np.cos(np.pi/180*((ang1+ang2)/2)) + center[0] ## 텍스트 x좌표        
            y = (r/2)*np.sin(np.pi/180*((ang1+ang2)/2)) + center[1] ## 텍스트 y좌표        
            
        ## 퍼센티지 출력    
        if i < len(labels) - 1:        
            sum_pct += float(f'{sorted_frequency[i]/total*100:.2f}')        
            ax.text(x,y,f'{sorted_frequency[i]/total*100:.2f}%',ha='center',va='center',fontsize=12)    
        else: ## 마지막 파이 조각은 퍼센티지의 합이 100이 되도록 비율을 조절        
            ax.text(x,y,f'{100-sum_pct:.2f}%',ha='center',va='center',fontsize=12) 
    
    title_font = {
        'fontsize': 25,
        'fontweight': 'bold'
    }

    plt.title("14가지 키워드 과학기술 뉴스를 이용한 시장 동향 시각화", loc='left', fontdict=title_font, pad=20)
    plt.legend(pie[0],sorted_labels, loc='lower right', fontsize=10) 
    plt.savefig('static/pie_chart.png')

    return render(request, 'Chart/chart.html')