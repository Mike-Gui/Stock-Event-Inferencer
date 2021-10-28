import twint
import pandas as pd
import time as time
import datetime as dt


#pip3 install --upgrade -e git+https://github.com/twintproject/twint.git@origin/master#egg=twint

x=input('Enter a Ticker:')
x = x.upper()
x = "$"+ x
x=str(x)
print("searching twitter for " + x)

# https://stonks.news/top-100/robinhood use this for determining c.Min_likes & c.Min_retweets. All other stocks, i.e., those not on this list, receive a standard requirement.

def scrape():
    c = twint.Config()
    c.Search = x
    c.Limit = 500
    c.Since="2020-10-25" ### Convert to 1yr ago dynamically
    c.Until="2021-10-27" ###Convert to present day -1
    c.Images= False
    c.Pandas = True
    c.Lang = "en"
    c.Email = False
    c.Phone = False
    c.Replies = False
    #c.Verified = True
    #c.Popular_tweets = True
    #c.Min_retweets = 10
    c.Min_likes = 50
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
    # Remove items containing urls
    #print(list(df2.columns.values))
    df2 = df2[df2.language == "en"]
    #df2 = df2.drop([(df2['tweet']=='Options') & (df2['tweet']=='OPTIONS') & (df2['tweet']=="Call") & (df2['tweet']=="Put")].index)
    df2.drop(["language"], axis=1, inplace=True)
    df2['tweet'] = df2['tweet'].str.replace('http\S+|www.\S+', '', case=False)
    df2['tweet'] = df2['tweet'].str.replace('&lt;/?[a-z]+&gt;', '', case=False)
    df2['tweet'] = df2['tweet'].str.replace('&amp;amp;', '&', case=False)
    df2['tweet'] = df2['tweet'].str.replace('&lt;', '<', case=False)
    df2['tweet'] = df2['tweet'].str.replace('&gt;', '>', case=False)

    df2.to_csv(f'C:/Users/mcgui/Desktop/glungo/{x}.csv', encoding='utf-8-sig')
scrape()
