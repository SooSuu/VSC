import time, sqlite3
from datetime import date, datetime, timedelta
from matplotlib import dates
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.font_manager
import matplotlib as mpl
from dateutil.relativedelta import relativedelta
import seaborn as sns

def graph():
    result=[]
    named=[]
    postshelf=[]
    postnamed=[]
    time = datetime.now()
    #time1 = time.strftime('%Y-%m-%d %H:%M:%S')
    #time2 = datetime.strptime(time,'%Y-%m-%d %H:%M:%S')
    ymax=time+relativedelta(days=30)
    con=sqlite3.connect('../sensorsData.db')
    curs=con.cursor()
    curs.execute("SELECT * from VACCINE")
    for row in curs.fetchall():
        date_time_str=row[3]
        date_time_obj=datetime.strptime(date_time_str,'%Y-%m-%d')
        if date_time_obj>time:
            result.append(date_time_obj)
            named.append(row[2])
        else:
            postnamed.append(date_time_obj)
            postshelf.append(row[2])
            
    colors=sns.color_palette('hls',len(named))
    mpl.rcParams['axes.unicode_minus'] = False
    plt.rcParams["font.family"]='NanumGothic'
    fig=plt.figure(figsize=(13,10))    
    plt.axis([-1,30,time,ymax])
    plt.title("백신")
    plt.xlabel('Vaccine name')
    plt.ylabel('days')
    plt.bar(named,result,label='유통기한', color=colors, 
         alpha=0.7, linewidth=4)

    print(named)
    print(result)
    plt.legend()
    plt.xticks(rotation=50)

    # 그래프 저장 경로
    plt.savefig('C:/Users/user/Desktop/flask23_A/dhtWebServer/static/vaccine.png')

    
graph()
