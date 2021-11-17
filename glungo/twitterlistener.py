import twint
import pandas as pd
import time as time
import datetime as dt
from bs4 import BeautifulSoup
import requests

#pip3 install --upgrade -e git+https://github.com/twintproject/twint.git@origin/master#egg=twint

x=input('Enter a Ticker:')
x = x.upper()
xUpper = x
x = "$"+ x
x=str(x)
print("searching twitter for " + x)
def locateRank():
    headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    rankurl = "https://apewisdom.io/"
    r1 = requests.get(rankurl, headers=headers)
    soup = BeautifulSoup(r1.text, 'html.parser') ###converts the html to a temporary text file and parses the content
    symbol_list = list()
    mentions_list = list()
    for i in range(0,50):
        if i == 15:
            continue
        symbol = soup.find('table', {'class': 'table marketcap-table dataTable default-table'}).find('tbody').find_all('tr')[i].find_all('td')[3].text
        symbol_list.append(symbol)
        mentions = int(soup.find('table', {'class': 'table marketcap-table dataTable default-table'}).find('tbody').find_all('tr')[i].find_all('td')[4].text)
        mentions_list.append(mentions)
    rank_list = pd.DataFrame({'Symbol':symbol_list, 'Mentions':mentions_list})
    rank_list = rank_list.drop_duplicates()
    print(rank_list)
    global min_retweetval
    global min_LikeVal
    if rank_list.eq(xUpper).any(axis=1):
        #for col in rank_list:
        print("benis")

    

    #mentions_specific = 
    #min_retweetval = mentions_specific

locateRank()





# https://stonks.news/top-100/robinhood use this for determining c.Min_likes & c.Min_retweets. All other stocks, i.e., those not on this list, receive a standard requirement.
# if the length of the chart df is shorter than 180 days (or 365 days), 
#           increase the limits on likes and retweets. 
#           Recently IPO'd companies will likely have more discussion


# def scrape():
#     c = twint.Config()
#     c.Search = x
#     c.Limit = 1000
#     c.Since="2021-01-02" ### Convert to 1yr ago dynamically
#     c.Until="2021-10-27" ###Convert to present day -1
#     c.Images= False
#     c.Pandas = True
#     c.Lang = "en"
#     c.Email = False
#     c.Phone = False
#     c.Replies = False
#     #c.Verified = True
#     #c.Popular_tweets = True
#     #c.Min_retweets = 5
#     c.Min_likes = 35
    
#     twint.run.Search(c)
#     Tweets_df = twint.storage.panda.Tweets_df
#     df2=pd.DataFrame(Tweets_df)
#     df2.drop(["place","photos",
#     "nreplies","place", "link","quote_url",
#     "video","thumbnail","near","geo","source",
#     "user_rt_id","user_rt","place", "retweet_id",
#     "reply_to","retweet_date", "urls", "translate", 
#     "trans_src", "trans_dest","retweet", "day", "hour",
#     "created_at","name", "username","conversation_id", "user_id", "user_id_str", "id"], axis=1, inplace=True)
#     # Remove items containing urls
#     #print(list(df2.columns.values))
#     df2 = df2[df2.language == "en"]
#     df2 = df2[df2['tweet'].str.contains("OPTIONS|Options|options|Calls|Puts|C>|P<|Gain|Alerted|ALERT|Alert")==False]  #Rewrite as multiple inclusion drop function
#     # df2 = df2[df2['tweet'].str.contains("Options")==False]
#     # df2 = df2[df2['tweet'].str.contains("options")==False]  
#     # df2 = df2[df2['tweet'].str.contains("Calls")==False]
#     # df2 = df2[df2['tweet'].str.contains("Puts")==False]
#     # df2 = df2[df2['tweet'].str.contains("C>")==False]
#     # df2 = df2[df2['tweet'].str.contains("P<")==False]
#     # df2 = df2[df2['tweet'].str.contains("GAIN")==False]
#     # df2 = df2[df2['tweet'].str.contains("Alerted")==False]
#     # df2 = df2[df2['tweet'].str.contains("ALERT")==False]
#     # df2 = df2[df2['tweet'].str.contains("Alert")==False]
#     #df2=df2[df2['cashtags'].str.contains("[rblx]")==True]
#     df2.drop(["language"], axis=1, inplace=True)
#     df2['tweet'] = df2['tweet'].str.replace('http\S+|www.\S+', '', case=False)
#     df2['tweet'] = df2['tweet'].str.replace('&lt;/?[a-z]+&gt;', '', case=False)
#     df2['tweet'] = df2['tweet'].str.replace('&amp;amp;', '&', case=False)
#     df2['tweet'] = df2['tweet'].str.replace('&lt;', '<', case=False)
#     df2['tweet'] = df2['tweet'].str.replace('&gt;', '>', case=False)

#     df2.to_csv(f'C:/Users/mcgui/Desktop/glungo/{x}.csv', encoding='utf-8-sig')
# scrape()
