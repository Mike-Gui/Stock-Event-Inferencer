import requests
import json
import pandas as pd
import datetime
#import matplotlib.pyplot  as plt


#User Entry Conditions
# ticker = input("Enter ticker of a company in the S&P500 you'd like to review: ")  
# ticker = ticker.upper()
d0 = datetime.date(2021, 1, 1)
d1 = datetime.date.today()
days = d1 - d0
days = days.days
YourAPI_Token = "tb_930718fabb2a4750a1c00b38a1552097" #Your https://thebaite.com/ token goes here

def attention(ticker):
    #ticker = ticker.get()
    ticker = ticker.upper()
    try:
        URL = f'http://thebaite.com:81/api/v1/stocks/metric?m=attention&d={days}&s={ticker}&token={YourAPI_Token}' ##Modify for your specific API Token
        r = requests.get(URL)
        rJson =  r.json() 
    except Exception as e:
        print(e)
    r = json.dumps(rJson)
    s = json.loads(r)
    global df_attention
    df_attention = pd.DataFrame(s)
    df_attention['t'] = pd.to_datetime(df_attention['t'],unit ='s').apply(lambda x: x.strftime('%m/%d/%Y'))
    df_attention['t'] = pd.strftime(format ="%Y-%m-%d")
    df_attention.rename(columns={'t': 'Date','d': 'Attention Score'}, inplace=True)
    df_attention= df_attention.reindex(columns = ['Date', "Attention Score"])
    df_attention = df_attention.iloc[::-1]
    #df_sentiment.plot(y = 'Attention Score', x = 'Date', kind = 'line')
    #df_sentiment.to_csv('C:/Users/mcgui/Desktop/Secondary/attention_output.csv', encoding = 'utf-8', index =False)
    #plt.title(f'{ticker} Attention Index Chart')
    #plt.show()
    df1 = df_attention 
    df1['MA7'] = df1.rolling(window = 7).mean()  ##7-day Moving Average
    df1.dropna()
    MA7 = df1['MA7'].tolist()
    deriv = list()
    index_num = list()
    dflength = len(MA7)
    x = dflength
    for i in range(dflength):
        if i == dflength-2:
            break
        n = 2 + i
        m = i
        x = (dflength-2) - i
        derIndex = ((MA7[n])-(MA7[m]))/2   
        deriv.append(derIndex)
        index_num.append(x)
    #global max_dates
    df1.drop(df1.head(1).index,inplace=True) # drop first row
    df1.drop(df1.tail(1).index,inplace=True) # drop last row
    df1['∆^2'] = deriv
    df1['index'] = index_num
    df_maxdates = df1[(df1['∆^2']<0.15) & (df1['∆^2']>-0.15)] #Sensitivity scale of 0.15
    max_dates = df_maxdates.sort_values(by=['MA7']).tail(5) #Select top 5 days for attention within range
    markerDates = max_dates['index'].tolist()
    markerDates.sort()
    print(max_dates)
    return markerDates


# def sentiment():
#     try:
#         URL = f'http://thebaite.com:81/api/v1/stocks/metric?m=sentiment&d={days}&s={ticker}&token={YourAPI_Token}' ##Modify for your specific API Token
#         r = requests.get(URL)
#         rJson =  r.json()
#     except Exception as e:
#         print(e)
#     r = json.dumps(rJson)
#     s = json.loads(r)
#     df_sentiment = pd.DataFrame(s)
#     df_sentiment['t'] = pd.to_datetime(df_sentiment['t'],unit='s')
#     df_sentiment.rename(columns={'d': 'Sentiment Score', 't': 'Date'}, inplace=True)
#     df_sentiment.plot(y = 'Sentiment Score', x= 'Date', kind = 'line')
#     plt.title(f'{ticker} Sentiment Index Chart')
#     plt.show()
# sentiment()