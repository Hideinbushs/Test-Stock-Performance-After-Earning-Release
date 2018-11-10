# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 19:56:08 2018

@author: siwei
"""

#Test the performance of stock after earning release, if this stock has 4 consectutive positive performance before
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from numpy import nan as Nan
# Pulling out stocks want to test
DF=pd.read_excel('C:/Users/siwei/Dropbox/Python/StockCharts Project/Earning Check/Earning Test.xlsx')

# Set up parameters

df3=pd.DataFrame.from_dict(dict(), orient='index')
df4=pd.Series([Nan,Nan,Nan], index=['index', 0,'Stock'])

# Loop through the stocks
# income: add up performance
# incomecount: how many stock has 4 consecutive positive performance
# Totalincome: add up performance of all the stock tested
# Totalcount: how many stock tested

row=0
income=0
incomecount=0
SA=0
Totalincome=0
Totalcount=0
for s in DF['Symbol']:
    SA=SA+1
    link1='https://stocksearning.com/stocks/'+ str(s).lower() + '/historical-earnings-date'
    row=row+1

    response = requests.get(link1)
    bf = BeautifulSoup(response.text, 'lxml')
    try:
        data=bf.find_all('div', class_='datablurbox')
        data2=data[0].find_all('li')
        earningmap=dict()
    except:
        print(s, 'earning.com dont have information for this stock')
        continue
    for i in range(len(data2)):
        date=data2[i].find_all('span')[0].string
        Date=datetime.strptime(date,'%m/%d/%Y').date()
        percentage=data2[i].find_all('span')[3].string
        try:
            Percentage=float(percentage.strip('%'))/100
        except:
            Percentage=0
        earningmap[Date]=list()
        earningmap[Date].append(Percentage)
    if len(earningmap.keys())<5:
        continue
    t=0
    count=0
    for i in earningmap.keys():
        if t==0 and pd.Timestamp(year=i.year, month=i.month, day=i.day, hour=0)==DF.iloc[row-1,1]:
            Totalincome=earningmap[i][0]+Totalincome
            Totalcount=Totalcount+1

        else:
            if t==0 and pd.Timestamp(year=i.year, month=i.month, day=i.day, hour=0)!=DF.iloc[row-1,1]:
                print(s, 'current earning day doesnt match')
                break
            else:            
                if t!=0 and earningmap[i][0]>0:
                    count=count+1
        t=t+1
        if t>=5:
            break
    
    if count>=4:
        incomecount=incomecount+1
        df2 = pd.DataFrame.from_dict(earningmap, orient='index')
        df2=df2.reset_index()
        df2=df2.fillna('0%')
        df2['Stock']=str(s)
        print(s)
        df3=df3.append(df4,ignore_index=True)
        df3=df3.append(df2,ignore_index=True)
        income=income+df2.iloc[0,1]
    
    
address='C:/Users/siwei/Dropbox/Python/StockCharts Project/Earning Check/Earning Test Result.xls'
writer = pd.ExcelWriter(address, engine='xlsxwriter')           
df3.to_excel(writer, sheet_name='Sheet1')
writer.save()               
                
            
            
        
        
    
    