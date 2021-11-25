import twint
import pandas as pd
import time as time
import datetime as datetime
from bs4 import BeautifulSoup
import requests

#pip3 install --upgrade -e git+https://github.com/twintproject/twint.git@origin/master#egg=twint

today_date = datetime.datetime.today() - datetime.timedelta(days=2)
today_date = today_date.strftime('%Y-%m-%d')
year_ago = datetime.datetime.today() - datetime.timedelta(days=365)
year_ago = year_ago.strftime('%Y-%m-%d')




# if the length of the chart df is shorter than 180 days (or 365 days), 
#  increase the limits on likes and retweets. 
#  Recently IPO'd companies will likely have more discussion
def locateRank(): #This def locates the appropriate search parameters for twint using popularity metrics from https://apewisdom.io/ from the last 24hrs
    headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    rankurl = "https://apewisdom.io/"
    r1 = requests.get(rankurl, headers=headers)
    soup = BeautifulSoup(r1.text, 'html.parser') ###converts the html to a temporary text file and parses the content
    symbol_list = list()
    mentions_list = list()
    upvotes_list = list()
    for i in range(0,50):
        if i == 15:
            continue
        symbol = soup.find('table', {'class': 'table marketcap-table dataTable default-table'}).find('tbody').find_all('tr')[i].find_all('td')[3].text
        symbol_list.append(symbol)
        mentions = soup.find('table', {'class': 'table marketcap-table dataTable default-table'}).find('tbody').find_all('tr')[i].find_all('td')[4].text
        mentions = int(mentions.replace(',',''))
        mentions_list.append(mentions)
        upvotes = str(soup.find('table', {'class': 'table marketcap-table dataTable default-table'}).find('tbody').find_all('tr')[i].find_all('td')[7].text)
        upvotes = int(upvotes.replace(',',''))
        upvotes_list.append(upvotes)
    rank_df = pd.DataFrame({'Symbol':symbol_list, 'Mentions':mentions_list, 'Upvotes':upvotes_list})
    #rank_df = rank_df.drop_duplicates()
    print(rank_df)
    global min_RetweetVal
    global min_LikeVal
    global verified_bool
    global popular_bool
    global current_sentiment
    global indexed_mention
    global upvotes_index
    inList_count = rank_df['Symbol'].str.contains(x_upper).sum()
    if inList_count>0:        
        rank_list_index = rank_df.loc[rank_df['Symbol'] == x_upper]
        indexed_mention = rank_list_index.iat[0,1]
        upvotes_index = rank_list_index.iat[0,2]
        min_RetweetVal = indexed_mention*0.15
        min_LikeVal = (indexed_mention**0.4)
        popular_bool = True
        verified_bool = False
        if indexed_mention > 50:
            verified_bool = False
        else:
            verified_bool = False
        current_sentiment = int(upvotes_index) / int(indexed_mention)
    else:
        print("not in list, setting default settings")
        min_RetweetVal = 5
        min_LikeVal = 10
        verified_bool = False
        popular_bool = False
        upvotes_index = "unknown"
        indexed_mention = "unknown"
        current_sentiment = 'unknown'

def scrape():
    c = twint.Config()
    c.Search = x
    c.Limit = 2000
    c.Since= str(year_ago)
    c.Until= str(today_date)
    c.Images= False
    c.Pandas = True
    c.Lang = "en"
    c.Email = False
    c.Phone = False
    c.Replies = False
    #c.Verified = verified_bool
    #c.Popular_tweets = #popular_bool
    c.Min_retweets = min_RetweetVal
    c.Min_likes = min_LikeVal
    twint.run.Search(c)
    Tweets_df = twint.storage.panda.Tweets_df
    df2=pd.DataFrame(Tweets_df)
    df2.drop(["place","photos",
    "nreplies","place", "link","quote_url",
    "video","thumbnail","near","geo","source",
    "user_rt_id","user_rt","place", "retweet_id",
    "reply_to","retweet_date", "urls", "translate", 
    "trans_src", "trans_dest","retweet", "day", "hour",
    "created_at","name", "username","conversation_id", "user_id", "user_id_str", "id"], axis=1, inplace=True)
    #####Remove items containing urls
    #print(list(df2.columns.values))
    df2 = df2[df2.language == "en"]
    #df2 = df2[df2['tweet'].str.contains("OPTIONS|Options|options|Calls|Puts|C>|P<|Gain|Alerted|ALERT|Alert")==False]  #Rewrite as multiple inclusion drop function
    df2 = df2[df2['tweet'].str.contains("Options")==False]
    df2 = df2[df2['tweet'].str.contains("options")==False]  
    df2 = df2[df2['tweet'].str.contains("Calls")==False]
    df2 = df2[df2['tweet'].str.contains("Puts")==False]
    df2 = df2[df2['tweet'].str.contains("C>")==False]
    df2 = df2[df2['tweet'].str.contains("P<")==False]
    df2 = df2[df2['tweet'].str.contains("GAIN")==False]
    df2 = df2[df2['tweet'].str.contains("Alerted")==False]
    df2 = df2[df2['tweet'].str.contains("ALERT")==False]
    df2 = df2[df2['tweet'].str.contains("Alert")==False]
    #df2=df2[df2['cashtags'].str.contains("[rblx]")==True]
    df2.drop(["language"], axis=1, inplace=True)
    df2['tweet'] = df2['tweet'].str.replace('http\S+|www.\S+', '', case=False)
    df2['tweet'] = df2['tweet'].str.replace('&lt;/?[a-z]+&gt;', '', case=False)
    df2['tweet'] = df2['tweet'].str.replace('&amp;amp;', '&', case=False)
    df2['tweet'] = df2['tweet'].str.replace('&lt;', '<', case=False)
    df2['tweet'] = df2['tweet'].str.replace('&gt;', '>', case=False)
    df2.to_csv(f'C:/Users/mcgui/Desktop/Secondary/{x}.csv', encoding='utf-8-sig')



x=input('Enter a Ticker:')
x = x.upper()
x_upper = x
x = "$"+ x
x=str(x)
print("searching twitter for " + x)

locateRank()
try:
    scrape()
    print('current sentiment index is ' , current_sentiment ,' based on ' , indexed_mention ,' mentions and ' , upvotes_index , ' upvotes')
except Exception as e: 
    print(e)