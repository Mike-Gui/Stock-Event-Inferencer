# -*- coding: utf-8 -*-
"""
Created on 9/8/2021 6:38pm
"""
from tkinter import *
import tkinter as tk
import pandas as pd
import numpy as np
from matplotlib import *
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import datetime as datetime
import time
from time import sleep
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.dates as mdates
###API Configs-----------------------------------------------------------------------------

###Defaults--------------------------------------------------------------------------------
onStart = 0
clear = 0
click = 0
#-------------------------------------------------------------
def tickerAsk(): ##when the user presses "Find" after entering a stock ticker, this function is called, sending the user's input to a webscraper function in utilities.py
        listbox.insert(END,'"'+ t.get()+'"' + ' Selected')
        try:
            tickerGetFirst(t)
            x.configure(text = intradayChange) #sets the intraday change label to what is returned by the data from yahoo finance.
            x2.configure(text = "$"+ price) #sets the price label to what is returned by the data from yahoo finance.
            x3.configure(text = companyName)
            global onStart
            global clear
            global click
            onStart = 1
            clear = 0 
            historicalData(t)
            onStartCheck()
            if click == 0:
                windowRefresh()
                click = click + 1
            else:
                windowRefresh2()
                click = 0
            lb3.configure(text = companyName)

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
    global onStart
    clear = 1
    onStart = 1
    onStartCheck()
    windowClear()
 
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
    period1 = int(time.mktime((datetime.datetime.now() - datetime.timedelta(days = 365)).timetuple()))
    period2 = int(time.mktime(datetime.datetime.now().timetuple()))
    interval = "1d" #1wk or 1m
    ticker = ticker.get()
    yahooQuery = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
    global df1
    df1 = pd.read_csv(yahooQuery, parse_dates=["Date"], index_col ="Date")
    df1.drop('Open', axis=1, inplace=True)
    df1.drop('High', axis=1, inplace=True)
    df1.drop('Low', axis=1, inplace=True)
    df1.drop('Adj Close', axis=1, inplace=True)
    df1.drop('Volume', axis=1, inplace=True)
    global priceChange1yr
    global posneg #identifier for YoY status
    priceChange1yr = (df1['Close'].values[251])-(df1['Close'].values[0]) ##determines if the change over the last year was positive or negative
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

# ##Chart clearing  -------------------------------------------------------------------------------------------------
fig = Figure(figsize= (12,5), dpi = 100)
canvas = FigureCanvasTkAgg(fig, master = frame)
fig.canvas.draw_idle
canvas.get_tk_widget().pack()
def onStartCheck():
    if onStart == 1:
        if clear == 0:
            fig.clear()
            #df2 = dfRetrieve(df)
            graph1 = fig.add_subplot(111)
            if posneg == 1:
                graph1.plot(df1.index, df1['Close'], color = "#08c959", linewidth=0.9)
            else:
                graph1.plot(df1.index, df1['Close'], color = "#ed000c", linewidth=0.9)
            graph1.xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
            graph1.grid(True)
            #graph1.plot.xlabel("Date")
            #graph1.plot.ylabel("Price")
            canvas = FigureCanvasTkAgg(fig, master = frame)
            fig.canvas.draw_idle 
            canvas.get_tk_widget().pack()
        else:
            fig.clear()
            canvas = FigureCanvasTkAgg(fig, master = frame)
            fig.canvas.draw_idle #canvas.draw()
            canvas.get_tk_widget().pack()
    elif onStart ==0:   
        print("start successful")
    else:
        print(0.0)

def windowRefresh():
    root.geometry("1201x710")
def windowRefresh2():
    root.geometry("1201x709")
def windowClear():
    root.geometry("1200x705")


##GUI Initiate-----------------------------------------------------------------------------------------------------
root.configure(background="white")
root.geometry("1200x705")
root.title('Stock Event Inferencer')
root.pack_propagate(1)
#root.after(1000, windowRefresh)
root.mainloop()

