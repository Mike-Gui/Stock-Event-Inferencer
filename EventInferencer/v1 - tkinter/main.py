# -*- coding: utf-8 -*-
"""
Created on 9/8/2021 6:38pm
"""
from tkinter import *
import tkinter as tk
import pandas as pd
from matplotlib import *
#import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import datetime as datetime
import time
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.dates as mdates
from random import randrange
import attention_dates as Attention
import notice as notice
import APIKEYS as APIKEYS
#Defaults--------------------------------------------------------------------------------
clear = 0
day1 = ""
day2 = ""
day3 = ""
day4 = ""
day5 = ""
ticker = "Null"
#APIKeys---------------------------------------------------------------------------------
noticeAPI = APIKEYS.usearch() #Retrieves and stores your usearch API token, if you've entered it
attentionAPI = APIKEYS.bAIte() #Retrieves and stores your bAIte API token, if you've entered it
#-------------------------------------------------------------
def tickerAsk(): ##when the user presses "Find" after entering a stock ticker, this function is called, sending the user's input to a webscraper function in utilities.py
        listbox.insert(END,'"'+ t.get()+'"' + ' Selected')
        try:
            tickerGetFirst(t)
            x.configure(text = intradayChange) #sets the intraday change label to what is returned by the data from yahoo finance.
            x2.configure(text = "$"+ price) #sets the price label to what is returned by the data from yahoo finance.
            x3.configure(text = companyName)
            global clear
            clear = 0 
            historicalData(t)
            makeChart()
            lb3.configure(text = companyName)
            ####Conversion from day number to xx/xx/xxxx format should occur here
            global ticker
            ticker = t.get()
 
            markerDatesListbox = ', '.join(str(e) for e in marker_dates)
            listbox.insert(END, "Days " + markerDatesListbox + " were found to be important")
        except Exception as e: #if nothing is returned, the exception returns an error message
            print(e)
            listbox.insert(END, 'Error finding all ' +  t.get() + " data, make sure the ticker symbol is correct")

def clearButton(): ##update to remove all dynamic variables at the end
    listbox.delete(0, END) ## clears the listbox
    listbox.insert(END, 'Search Cleared')
    x.configure(text = "")
    x2.configure(text = "")
    x3.configure(text = "")
    lb3.configure(text = "") ###company name above chart reset to ""
    global clear
    global ticker
    clear = 1
    makeChart()
    d1b['text'] = ""
    d2b['text'] = ""
    d3b['text'] = ""
    d4b['text'] = ""
    d5b['text'] = ""
    ticker = "Null"

###Realtime price data from Yahoo Finance--------------------------------------------------------------------------------------------        
def tickerGetFirst(ticker):
    headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    ticker = ticker.get() ### retrieves the ticker from the main.py user entry request
    yahoourl = f'https://finance.yahoo.com/quote/{ticker}' ### f string allows for dynamic entry from user, thankfully Yahoo Finance has a simple url search syntax
    r1 = requests.get(yahoourl, headers=headers)
    yahoosoup = BeautifulSoup(r1.text, 'html.parser') ###converts the html to a temporary text file and parses the content
    global companyName ### sets the following variables as global variables so they can be retrieved outside of the def tickerGetFirst call from main.py
    global price  
    global intradayChange
    companyName = yahoosoup.find('h1', {'class': 'D(ib) Fz(18px)'}).text ###parses the url html under the h1 tag for the company name
    price = yahoosoup.find('fin-streamer', {'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)' }).text
    intradayChange = yahoosoup.find('div', {'class': "D(ib) Mend(20px)"}).find_all('fin-streamer')[2].find_all('span')[0].text
          
####Historical Data Retriever---------------------------------------------------------------------------------------------------------------------------------
def historicalData(ticker):
    d0 = datetime.date(2021, 1, 1)
    d1 = datetime.date.today()
    Days = d1 - d0
    Days = Days.days
    fulldate_df = pd.DataFrame({'Date':pd.date_range(start = d0, end = d1, periods = Days)})
    fulldate_df['Date'] = pd.to_datetime(fulldate_df['Date'],format='%Y-%m-%d')
    period1 = int(time.mktime((datetime.datetime.now() - datetime.timedelta(days = Days)).timetuple()))
    period2 = int(time.mktime(datetime.datetime.now().timetuple()))
    interval = "1d"
    ticker = ticker.get()
    yahooQuery = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history' #&includeAdjustedClose=true'
    global df1
    global df1Length
    df1 = pd.read_csv(yahooQuery, parse_dates=["Date"], index_col ="Date")
    df1.drop('Open', axis=1, inplace=True)
    df1.drop('High', axis=1, inplace=True)
    df1.drop('Low', axis=1, inplace=True)
    df1.drop('Adj Close', axis=1, inplace=True)
    df1.drop('Volume', axis=1, inplace=True)
    df1 = pd.merge_asof(fulldate_df, df1, on="Date") 
    df1['Date'] = pd.to_datetime(df1["Date"].dt.strftime('%Y-%m-%d'))
    df1Length = len(df1) - 1
    

#Retrieve data from API script------------------------------------------------------
    try:
        global markers
        global marker_index
        global marker_dates
        markers = Attention.attention(ticker, attentionAPI)
        marker_index = markers['index'].tolist()
        marker_dates = markers['Date'].tolist()
        marker_dates.sort()
        #print(marker_dates)
        global day1
        global day2
        global day3
        global day4
        global day5
        day1 = marker_dates[0]
        day2 = marker_dates[1]
        day3 = marker_dates[2]
        day4 = marker_dates[3]
        day5 = marker_dates[4]
        d1b['text'] = day1
        d2b['text'] = day2
        d3b['text'] = day3
        d4b['text'] = day4
        d5b['text'] = day5
    except Exception as e: 
        print(e)
    
#Determine if the 1yr price action is positive or negative----------------------------
    global priceChange1yr
    global posneg #identifier for YoY status
    priceChange1yr = float(df1['Close'].values[df1Length])-float(df1['Close'].values[4]) ##determines if the change over the last year was positive or negative
    if priceChange1yr >= 0: #sets the posneg value to 1 if the price has increased or not moved in the last year
        posneg = 1
    else:
        posneg = 0
#Reports ---------------------------------------------------------------------------
def day1_report():
    if ticker == "Null":
        listbox.insert(END, 'Cannot generate a report yet')
    else:
        listbox.insert(END, 'Generating report for '+ day1+"...")
        #articles = notice.dateRange(day1)
        notice.dateRange(day1, companyName, noticeAPI)

        new_window = Toplevel()
        new_window.title(day1+ " Report")
        new_window.geometry("400x700")
        frame_new = Frame(new_window, width = 400, height=800)
        frame_new.pack(expand = 1, fill=BOTH, side = TOP, anchor = N)
        Font = ("Arial","20") 
        date_label = Label(frame_new, text = day1, font = Font)
        date_label.pack(side = TOP)
        listbox.insert(END, 'Done.')

def day2_report():
    if ticker == "Null":
        listbox.insert(END, 'Cannot generate a report yet')
    else:
        listbox.insert(END, 'Generating report for '+ day2+"...")
        #articles = notice.dateRange(day1)
        notice.dateRange(day2, companyName, noticeAPI)

        new_window = Toplevel()
        new_window.title(day2+ " Report")
        new_window.geometry("400x700")
        frame_new = Frame(new_window, width = 400, height=800)
        frame_new.pack(expand = 1, fill=BOTH, side = TOP, anchor = N)
        Font = ("Arial","20") 
        date_label = Label(frame_new, text = day2, font = Font)
        date_label.pack(side = TOP)
        listbox.insert(END, 'Done.')

def day3_report():
    if ticker == "Null":
        listbox.insert(END, 'Cannot generate a report yet')
    else:
        listbox.insert(END, 'Generating report for '+ day3+"...")
        #articles = notice.dateRange(day1)
        notice.dateRange(day3, companyName, noticeAPI)

        new_window = Toplevel()
        new_window.title(day3+ " Report")
        new_window.geometry("400x700")
        frame_new = Frame(new_window, width = 400, height=800)
        frame_new.pack(expand = 1, fill=BOTH, side = TOP, anchor = N)
        Font = ("Arial","20") 
        date_label = Label(frame_new, text = day3, font = Font)
        date_label.pack(side = TOP)
        listbox.insert(END, 'Done.')

def day4_report():

    if ticker == "Null":
        listbox.insert(END, 'Cannot generate a report yet')
    else:
        listbox.insert(END, 'Generating report for '+ day4+"...")
        #articles = notice.dateRange(day1)
        notice.dateRange(day4, companyName, noticeAPI)

        new_window = Toplevel()
        new_window.title(day4+ " Report")
        new_window.geometry("400x700")
        frame_new = Frame(new_window, width = 400, height=800)
        frame_new.pack(expand = 1, fill=BOTH, side = TOP, anchor = N)
        Font = ("Arial","20") 
        date_label = Label(frame_new, text = day4, font = Font)
        date_label.pack(side = TOP)
        listbox.insert(END, 'Done.')

def day5_report():
    if ticker == "Null":
        listbox.insert(END, 'Cannot generate a report yet')
    else:
        listbox.insert(END, 'Generating report for '+ day5+"...")
        #articles = notice.dateRange(day1)
        notice.dateRange(day5, companyName, noticeAPI)

        new_window = Toplevel()
        new_window.title(day5+ " Report")
        new_window.geometry("400x700")
        frame_new = Frame(new_window, width = 400, height=800)
        frame_new.pack(expand = 1, fill=BOTH, side = TOP, anchor = N)
        Font = ("Arial","20") 
        date_label = Label(frame_new, text = day5, font = Font)
        date_label.pack(side = TOP)
        listbox.insert(END, 'Done.')


####GUI Config-----------------------------------------------------------------------------
root = tk.Tk()
frame = Frame(root, width=500, height=400)
frame.pack(expand = 1, fill = X, side = TOP, anchor = N)
#---------------------Criteria selection--------------------
bbar = Frame(frame, relief = 'sunken', width=600, bd = 4)
bbar.pack(expand = 1, fill = BOTH, side = BOTTOM, pady = 5)
#Reports--------------------------------------------------
reports = Frame(frame, bd= 2, relief= 'groove')
reportlbl = Label(reports, text = "Reports:", font =('bold'))
reportlbl.pack(side=LEFT)
d5b = Button(reports, text = day5, command = day5_report)
d4b = Button(reports, text = day4, command = day4_report)
d3b = Button(reports, text = day3, command = day3_report)
d2b = Button(reports, text = day2, command = day2_report)
d1b = Button(reports, text = day1, command = day1_report)
d5b.pack(side = RIGHT)
d4b.pack(side = RIGHT)
d3b.pack(side = RIGHT)
d2b.pack(side = RIGHT)
d1b.pack(side = RIGHT)
reports.pack(side = BOTTOM, fill = X, expand = 0)
#--------------------Ticker Entry---------------------------
t = StringVar()
ef = Frame(frame, bd=2, relief='groove')
lb2 = Label(ef, text='Company Ticker Symbol:', font=('bold'))
lb2.pack(side= LEFT)
entry = Entry(ef, textvariable = t, bg='white') 
bt = Button(ef, text = 'Find', command = tickerAsk)
entry.pack(side = LEFT, padx = 5)
bt.pack(side = LEFT, padx = 5)
bt2 = Button(ef, text = 'Clear', command = clearButton)
bt2.pack(side = LEFT, padx = 5)
bt3 = Button(ef, text = "Omni")
ef.pack(expand=0, fill=X, pady=5, side = BOTTOM)
x = Label(ef, text = "") ##Intraday Change value from tickerAsk.py
x.pack(side= RIGHT, padx = 10)
w = Label(ef, text = 'Intraday Change:')
w.pack(side= RIGHT, padx = 4)
x2 = Label(ef, text = "") ##Current price value from tickerAsk.py
x2.pack(side= RIGHT, padx = 4)
w2 = Label(ef, text = 'Current Price:')
w2.pack(side= RIGHT, padx = 10)
x3 = Label(ef, text = "") ##companyName value from tickerAsk.py
x3.pack(side= RIGHT, padx = 4)
w3 = Label(ef, text = 'Company Name:')
w3.pack(side= RIGHT, padx = 10)
#----Chart Title Display----------------------------------------------
chart = Frame(frame, bd=5)
chartlabel = Label(chart, text = "1 Year Chart", font=('bold'))
chartlabel.pack(side = TOP)
lb3 = Label(chart, text ="")
lb3.pack(side = TOP)
chart.pack(side=TOP, fill=X, pady=5, expand=0 )
#----Status log----------------------------------------------------------------------------------------------------
lf = Frame(frame, bd=2, relief='groove')
b = Label(lf, text='Status:')
listbox = Listbox(lf, height=5)
b.pack(side=TOP, padx=5, fill=Y)
listbox.pack(padx=5, fill = X)
lf.pack(fill="both", expand=1, pady=5, before = bbar, side = BOTTOM)

###Chart Creator -------------------------------------------------------------------------------------------------
fig = Figure(figsize= (12,5), dpi = 100)
canvas = FigureCanvasTkAgg(fig, master = frame)
fig.canvas.draw_idle
canvas.get_tk_widget().pack()
def makeChart():
    if clear == 1:
        fig.clear()
        canvas = FigureCanvasTkAgg(fig, master = frame)
        fig.canvas.draw_idle
        canvas.get_tk_widget().pack()    
    else:
        fig.clear()
        graph1 = fig.add_subplot(111)
        #tw = [mpf.make_addplot(markerDates, scatter=True,markersize=7, marker="o", ax=graph1)]
        if posneg == 1:
           graph1.plot(df1.index, df1['Close'], color = "#08c959", linewidth=1.1, linestyle='-', marker = 'o',ms=7, markerfacecolor = "#000000", markevery=marker_index)
        else:
           graph1.plot(df1.index, df1['Close'], color = "#ed000c", linewidth=1.1, linestyle='-', marker= 'o',ms=7, markerfacecolor = "#000000", markevery=marker_index )
        graph1.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        a = list((range(1,(df1Length+30),30)))
        graph1.xaxis.set_ticks(a)
        graph1.grid(True)
        #graph1.set_xlabel("Date")
        graph1.set_ylabel("Price per Share")
        canvas = FigureCanvasTkAgg(fig, master = frame)
        fig.canvas.draw_idle 
        canvas.get_tk_widget().pack()
    windowRefresh()

def windowRefresh(): #Allows for user input to change the matplot lib display within the tkinter window
    xpar = randrange(7,10)
    ypar = randrange(7,10)
    root.geometry(f'120{xpar}x70{ypar}')
##Root GUI Initiate-----------------------------------------------------------------------------------------------------
root.configure(background="white")
root.geometry("1200x706")
root.title('Stock Event Inferencer')
root.pack_propagate(1)
root.mainloop()
