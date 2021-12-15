import requests
from bs4 import BeautifulSoup
import datetime as datetime
ticker = input("Enter ticker of a company in the S&P500 you'd like to review: ")  
ticker = ticker.upper()
currentday = datetime.datetime.today()
firstdate = datetime.datetime(2021, 1, 1)
try:
    #ticker = "amzn"
    headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    #ticker = ticker.get() ### retrieves the ticker from the main.py user entry request
    yahoourl = f'https://finance.yahoo.com/calendar/earnings?symbol={ticker}' 
    r1 = requests.get(yahoourl, headers=headers)
    yahoosoup = BeautifulSoup(r1.text, 'html.parser')

    earnings_list = list()
    e_list = list()
    for i in range(0,12):
        er_1 = yahoosoup.find('table', {'class': 'W(100%)'}).find('tbody').find_all('tr')[i].find_all('td')[2].text
        er_1 = str(er_1[:-9])
        er_1 = er_1.replace(",","")
        er_1 = datetime.datetime.strptime(er_1, '%b %d %Y')
        earnings_list.append(er_1)
    e_list.sort()
    for i in range(0,9):
        if earnings_list[i] < currentday and earnings_list[i] > firstdate:
            e_list.append(earnings_list[i])
    e_list = list(set(e_list))
    e_list.sort()
    e_list.reverse()

    #earnings_list = [earnings_list[0], earnings_list[1],earnings_list[2], earnings_list[3],earnings_list[4]]
    
    print(e_list)

except Exception as e:
    print(e)
    print("not enough earnings previous dates")


