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

#Defaults--------------------------------------------------------------------------------
clear = 0
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
    clear = 1
    makeChart()


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
    price = yahoosoup.find('span', {'class': 'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text ### parses the url html under the span class for the current company price
    intradayChange = yahoosoup.find('span', {'class': 'Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($positiveColor)'})### parses for the current intraday change value
        ### an if else state was required for intraday change, as the html string of the intradayChange changes depending on whether the stock is up or down for the day. This accounts for that.
    if intradayChange == (None):
        intradayChange = yahoosoup.find('span', {'class': 'Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($negativeColor)'})
    if intradayChange == (None):
        intradayChange = yahoosoup.find('span', {'class': 'Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px)'}).text
    elif intradayChange == yahoosoup.find('span', {'class': 'Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($negativeColor)'}):
        intradayChange = yahoosoup.find('span', {'class': 'Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($negativeColor)'}).text
    else:
        intradayChange = yahoosoup.find('span', {'class': 'Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px) C($positiveColor)'}).text  
          
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
    df1 = pd.read_csv(yahooQuery, parse_dates=["Date"], index_col ="Date")
    df1.drop('Open', axis=1, inplace=True)
    df1.drop('High', axis=1, inplace=True)
    df1.drop('Low', axis=1, inplace=True)
    df1.drop('Adj Close', axis=1, inplace=True)
    df1.drop('Volume', axis=1, inplace=True)

    df1 = pd.merge_asof(fulldate_df, df1, on="Date") 
    df1['Date'] = pd.to_datetime(df1["Date"].dt.strftime('%Y-%m-%d'))
    df1.to_csv("C:/Users/mcgui/Desktop/Secondary/df1_output.csv", encoding = 'utf-8')
    df1Length = len(df1) - 1
    #df1Length = df1Length - 1


# Retrieve data from API script------------------------------------------------------
    try:
        global markers
        global marker_index
        global marker_dates
        markers = Attention.attention(ticker)
        marker_index = markers['index'].tolist()
        marker_dates = markers['Date'].tolist()
        marker_dates.sort()
        print(markers)
    except Exception as e: 
        print(e)
    
#Determine if the 1yr price action is positive or negative----------------------------

    global priceChange1yr
    global posneg #identifier for YoY status
    priceChange1yr = float(df1['Close'].values[df1Length])-float(df1['Close'].values[4]) ##determines if the change over the last year was positive or negative
    #print(priceChange1yr)

    if priceChange1yr >= 0: #sets the posneg value to 1 if the price has increased or not moved in the last year
        posneg = 1
    else:
        posneg = 0

####GUI Config-----------------------------------------------------------------------------
root = tk.Tk()
frame = Frame(root, width=500, height=400)
frame.pack(expand = 1, fill = X, side = TOP, anchor = N)
#---------------------Criteria selection--------------------
bbar = Frame(frame, relief = 'sunken', width=600, bd = 4)
bbar.pack(expand = 1, fill = BOTH, side = BOTTOM, pady = 5)
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
           graph1.plot(df1.index, df1['Close'], color = "#08c959", linewidth=0.9, linestyle='-', marker = 'o',ms=7, markerfacecolor = "#000000", markevery=marker_index)
        else:
           graph1.plot(df1.index, df1['Close'], color = "#ed000c", linewidth=0.9, linestyle='-', marker= 'o',ms=7, markerfacecolor = "#000000", markevery=marker_index )
        graph1.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        #graph1.xaxis.set_ticks(12)
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