#NewsAPI
import requests
import datetime
import pandas as pd
import json


##Uses ContextualWeb API
def dateRange(day, company, api_key):
    day= pd.to_datetime(day)
    days = datetime.timedelta(4)
    begin = day-days
    begin = begin.strftime('%m/%d/%Y')
    end = day+days 
    end  = end.strftime('%m/%d/%Y')
    url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/search/NewsSearchAPI"
    headers = {
        'x-rapidapi-host': "contextualwebsearch-websearch-v1.p.rapidapi.com",
        'x-rapidapi-key': f"{api_key}"
        }
    query = f"{company}"
    page_number = 1
    page_size = 10
    auto_correct = False
    safe_search = False
    with_thumbnails = False
    from_published_date = f"{begin}"
    to_published_date = f"{end}"

    querystring = {"q": query,
                "pageNumber": page_number,
                "pageSize": page_size,
                "autoCorrect": auto_correct,
                "safeSearch": safe_search,
                "withThumbnails": with_thumbnails,
                "fromPublishedDate": from_published_date,
                "toPublishedDate": to_published_date}
    response = requests.request("GET", url, headers=headers, params=querystring).json()
    article_list = list()
    for web_page in response["value"]:
        url = web_page["url"]
        title = web_page["title"]
        description = web_page["description"]
        body = web_page["body"]
        date_published = web_page["datePublished"]
        provider = web_page["provider"]["name"]
        web_page = ("Title: {}. Provider: {}. Published Date: {}. Url: {}. ".format(title, provider, date_published, url))
        article_list.append(web_page)
        #print(web_page)
    
    return article_list

    
        
