import matplotlib.pyplot as plt
from matplotlib import dates
import sqlite3,os,csv,datetime,matplotlib.font_manager
import pandas as pd
from pandas import DataFrame as df
from matplotlib.ticker import MultipleLocator, IndexLocator, FuncFormatter
from matplotlib.dates import MonthLocator, DateFormatter
import matplotlib.dates as mdates
from datetime import date
import matplotlib as mpl

def graph_tem():
    conn=sqlite3.connect('../sensorsData.db')
    curs=conn.cursor()
    xx=[]
    yy=[]

    for row in curs.execute("SELECT strftime('%H:%M',timestamp),temp FROM DHT_data order by timestamp desc limit 30"):
        xx.append(row[0])
        yy.append(row[1])
    xx.reverse()
    yy.reverse()

    mpl.rcParams['axes.unicode_minus']=False
    plt.rcParams["font.family"]='NanumGothic'
    fig=plt.figure(figsize=(15,12))
    ax=fig.add_subplot()
    plt.title("온도계")
    plt.xlabel('시간')
    plt.ylabel('온도')
    plt.plot(xx,yy,'r-',marker='o')
    plt.legend()
    plt.xticks(rotation=50)
    
    plt.savefig('C:/Users/user/Desktop/flask23_A/dhtWebServer/static/graph.png')


graph_tem()