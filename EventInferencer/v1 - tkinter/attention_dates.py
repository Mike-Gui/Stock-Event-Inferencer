import requests
import json
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot  as plt
from scipy.signal import find_peaks

#User Entry Conditions for debugging
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
    df2 = df_attention 
    indexer = list()
    dflength = len(df2)
    x = 0
    for i in range(dflength):
        x = x+1
        indexer.append(x)
    df2['Index'] = indexer
    data_y = (df2['Attention Score'])
    peaks, _ = find_peaks(data_y, height=0, distance = 7)#Find_peaks, each peak must be at least 7 units away from the next 
    peak_days = peaks.tolist()
    peaks_list = list()
    for i in peak_days:
        peaks_list.append(df2.iloc[i]) 
    df_peakscores = pd.DataFrame(peaks_list)
    markers = df_peakscores.sort_values(by=['Attention Score']).tail(5)
    print(markers)
    return markers


def sentiment(ticker, api_token):
    ticker = ticker.upper()
    try:
        URL2 = f'http://thebaite.com:81/api/v1/stocks/metric?m=sentiment&d={days}&s={ticker}&token={api_token}' 
        r2 = requests.get(URL2)
        rJson2 =  r2.json() 
    except Exception as e:
        print(e)
    a = json.dumps(rJson2)
    b = json.loads(a)
    df_sentiment = pd.DataFrame(b)
    df_sentiment['t'] = pd.to_datetime(df_sentiment['t'],unit ='s').apply(lambda x: x.strftime('%m/%d/%Y'))
    df_sentiment.rename(columns={'t': 'Date','d': 'Sentiment Score'}, inplace=True)
    df_sentiment= df_sentiment.reindex(columns = ['Date', "Sentiment Score"])
    df_sentiment = df_sentiment.iloc[::-1]
    df_sentiment['Sentiment Score'] = 100*((df_sentiment['Sentiment Score'] - min(df_sentiment['Sentiment Score'])) / (max(df_sentiment['Sentiment Score']) - min(df_sentiment['Sentiment Score']))) #Rescale (0-100)
    return df_sentiment
