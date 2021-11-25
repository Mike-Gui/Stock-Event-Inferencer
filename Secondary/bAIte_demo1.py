import requests
import json
import pandas as pd
from datetime import datetime as dt
import matplotlib.pyplot  as plt




##User Entry Conditions
ticker = input("Enter ticker of a company in the S&P500 you'd like to review: ")  #Ticker
ticker = ticker.upper()
days = input('Enter Lookback period in days: ')


##Sentiment Request
# def sentiment():
#     try:
#         URL = f'http://thebaite.com:81/api/v1/stocks/metric?m=sentiment&d={days}&s={ticker}&token=' ##Modify for your specific API Token
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
#     plt.title('Sentiment Index Chart')
#     plt.show()
    

# sentiment()

# ##Attention Request:
def attention():
    try:
        URL = f'http://thebaite.com:81/api/v1/stocks/metric?m=attention&d={days}&s={ticker}&token=' ##Modify for your specific API Token
        r = requests.get(URL)
        rJson =  r.json()
    except Exception as e:
        print(e)
    r = json.dumps(rJson)
    s = json.loads(r)
    df_sentiment = pd.DataFrame(s)
    df_sentiment['t'] = pd.to_datetime(df_sentiment['t'],unit='s')
    df_sentiment.rename(columns={'d': 'Attention Score', 't': 'Date'}, inplace=True)
    df_sentiment.plot(y = 'Attention Score', x = 'Date', kind = 'line')
    plt.title('Attention Index Chart')
    plt.show()
attention()


# ##Index Sentiment Request