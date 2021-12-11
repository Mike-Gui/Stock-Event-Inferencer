import requests
import json
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot  as plt
from scipy.signal import find_peaks

#User Entry Conditions
#ticker = input("Enter ticker of a company in the S&P500 you'd like to review: ")  
# ticker = ticker.upper()
d0 = datetime.date(2021, 1, 1)
d1 = datetime.date.today()
days = d1 - d0
days = days.days

def attention(ticker,api_token):

    ticker = ticker.upper()
    try:
        URL = f'http://thebaite.com:81/api/v1/stocks/metric?m=attention&d={days}&s={ticker}&token={api_token}' 
        r = requests.get(URL)
        rJson =  r.json() 
    except Exception as e:
        print(e)
    r = json.dumps(rJson)
    s = json.loads(r)
    df_attention = pd.DataFrame(s)
    df_attention['t'] = pd.to_datetime(df_attention['t'],unit ='s').apply(lambda x: x.strftime('%m/%d/%Y'))
    df_attention.rename(columns={'t': 'Date','d': 'Attention Score'}, inplace=True)
    df_attention= df_attention.reindex(columns = ['Date', "Attention Score"])
    df_attention = df_attention.iloc[::-1]
    df1 = df_attention 
    df1['MA7'] = df1.rolling(window = 7).mean()  ##7-day Moving Average
    df1.dropna()
    MA7 = df1['MA7'].tolist()
    deriv = list()
    index_num = list()
    dflength = len(MA7)
    x = 0
    for i in range(dflength):
        if i == dflength-2:
            break
        n = 2 + i
        m = i
        x = x+1
        derIndex = ((MA7[n])-(MA7[m]))/2   
        deriv.append(derIndex)
        index_num.append(x)
    df1.drop(df1.head(1).index,inplace=True) # drop first row
    df1.drop(df1.tail(1).index,inplace=True) # drop last row
    df1['∆^2'] = deriv
    df1['index'] = index_num
    df_maxdates = df1[(df1['∆^2']<0.15) & (df1['∆^2']>-0.15)] #Sensitivity scale of 0.15
    markers = df_maxdates.sort_values(by=['MA7']).tail(5) #Select top 5 days for attention within range
    print(markers)
    return markers

# def attention(ticker,api_token):
# ticker = ticker.upper()
# try:
#     URL = f'http://thebaite.com:81/api/v1/stocks/metric?m=attention&d={days}&s={ticker}&token=tb_930718fabb2a4750a1c00b38a1552097' 
#     r = requests.get(URL)
#     rJson =  r.json() 
# except Exception as e:
#     print(e)
# r = json.dumps(rJson)
# s = json.loads(r)
# df_attention = pd.DataFrame(s)
# df_attention['t'] = pd.to_datetime(df_attention['t'],unit ='s').apply(lambda x: x.strftime('%m/%d/%Y'))
# df_attention.rename(columns={'t': 'Date','d': 'Attention Score'}, inplace=True)
# df_attention= df_attention.reindex(columns = ['Date', "Attention Score"])
# df_attention = df_attention.iloc[::-1]
# df2 = df_attention 

# indexer = list()
# dflength = len(df2)
# x = 0
# for i in range(dflength):
#     x = x+1
#     indexer.append(x)

# df2['Index'] = indexer

# data_y = (df2['Attention Score'])#.iloc[::-1]
# data_x = (df2['Index'])

# df2 = pd.DataFrame({'Index': data_x, 'Attention Score':data_y}, columns = ['Index','Attention Score'])
# print(df2)
# #Find_peaks------------------------
# peaks, _ = find_peaks(data_y, height=0, distance = 7)
# peak_days = pd.DataFrame(peaks, columns = ['peak dates'])
# print(peak_days)
# ##Match back into df2 to iloc serach for indexed dates
# #markers = np.where(peak_days['peak dates'] == df2['Index'], 1, 0) 
# #markers = np.where(peak_days.loc[peak_days['peak dates']] == df2.loc[df2['Index']], 1, 0) 

# markers = df2.sort_values(by=['AttentionScore']).tail(5)
# print(markers)


# # peak_list = list()

# # for i in peak_days:
# #     if peak_days[i] == df2["Index"][i]:
# #         print(df2[i])
# #     print(peak_days[i])
# #     #markers = 
# #return markers
    
