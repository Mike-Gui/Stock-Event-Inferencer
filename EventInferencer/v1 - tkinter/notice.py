#NewsAPI
import requests
import datetime
import pandas as pd
import json
#import re

##Uses ContextualWeb API



def dateRange(day, company, api_key):
    print(company)
    day= pd.to_datetime(day)
    days = datetime.timedelta(4)
    begin = day-days
    begin = begin.strftime('%m/%d/%Y')
    end = day+days 
    end  = end.strftime('%m/%d/%Y')
    url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/search/NewsSearchAPI"
    querystring = {"q":f"{company}","pageNumber":"1","pageSize":"10","autoCorrect":"false","fromPublishedDate":f"{begin}","toPublishedDate":f"{end}"}
    headers = {
        'x-rapidapi-host': "contextualwebsearch-websearch-v1.p.rapidapi.com",
        'x-rapidapi-key': f"{api_key}"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    #response.to_csv('C:/Users/mcgui/Desktop/Secondary/articles1.csv', encoding = 'utf-8')


    print(response.text)