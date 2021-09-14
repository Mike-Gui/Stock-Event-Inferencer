# -*- coding: utf-8 -*-
"""
Created on 9/8/2021 6:38pm
@mikegui


"""

from tkinter import *
import tkinter
import csv
import pandas as pd
#import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import datetime as datetime
import time


###API Configs-----------------------------------------------------------------------------


####GUI Config-----------------------------------------------------------------------------
class Menu:
    def __init__(self, master):
        frame = Frame(master, width=500, height=400)
        frame.pack(expand = 1, fill = X, side = TOP, anchor = N)
        #---------------------Criteria selection--------------------
        self.bbar = Frame(frame, relief = 'sunken', width=600, bd = 4)
        self.bbar.pack(expand = 1, fill = BOTH, side = BOTTOM, pady = 5)
        #--------------------Ticker Entry---------------------------
        self.t = StringVar()
        self.ef = Frame(frame, bd=2, relief='groove')
        self.lb2 = Label(self.ef, text='Company Ticker Symbol:', font=('bold'))
        self.lb2.pack(side= LEFT)
        self.entry = Entry(self.ef, textvariable = self.t, bg='white') 
        self.bt = Button(self.ef, text = 'Find', command = self.tickerAsk)
        self.entry.pack(side = LEFT, padx = 5)
        self.bt.pack(side = LEFT, padx= 5)
        self.bt2 = Button(self.ef, text = 'Clear', command = self.clearButton)
        self.bt2.pack(side = LEFT, padx= 5)
        self.ef.pack(expand=0, fill=X, pady=5, side = BOTTOM)
        self.x = Label(self.ef, text = "") ##Intraday Change value from tickerAsk.py
        self.x.pack(side= RIGHT, padx = 10)
        self.w = Label(self.ef, text = 'Intraday Change:')
        self.w.pack(side= RIGHT, padx = 4)
        self.x2 = Label(self.ef, text = "") ##Current price value from tickerAsk.py
        self.x2.pack(side= RIGHT, padx = 4)
        self.w2 = Label(self.ef, text = 'Current Price:')
        self.w2.pack(side= RIGHT, padx = 10)
        self.x3 = Label(self.ef, text = "") ##companyName value from tickerAsk.py
        self.x3.pack(side= RIGHT, padx = 4)
        self.w3 = Label(self.ef, text = 'Company Name:')
        self.w3.pack(side= RIGHT, padx = 10)
        

        #----Chart Display----------------------------------------------
        self.chart = Frame(frame, bd=5, relief='groove')
        self.chartlabel  = Label(self.chart, text = "1 Year Price action", font=('bold'))
        self.chartlabel.pack(side = BOTTOM)
        self.chart.pack(side=BOTTOM, pady = 5, padx=2.5, expand=0)
        
        #----Status log----------------------------------------------
        self.lf = Frame(frame, bd=2, relief='groove')
        self.lb = Label(self.lf, text='Status:')
        self.listbox = Listbox(self.lf, height=5)
        self.lb.pack(side=TOP, padx=5, fill=Y)
        self.listbox.pack(padx=5, fill = X)
        self.lf.pack(fill="both", expand=1, pady=5, before = self.bbar, side = BOTTOM)
        
        #-------------------------------------------------------------
    def tickerAsk(self): ##when the user presses "Find" after entering a stock ticker, this function is called, sending the user's input to a webscraper function in utilities.py
          self.listbox.insert(END,'"'+ self.t.get()+'"' + ' Selected')
          currentTicker = self.t.get()
          try:
              tickerGetFirst(self.t)
              self.x.configure(text = intradayChange) #sets the intraday change label to what is returned by the data from yahoo finance.
              self.x2.configure(text = "$"+ price) #sets the price label to what is returned by the data from yahoo finance.
              self.x3.configure(text = companyName)
               
          except Exception as e: #if nothing is returned, the exception returns an error message
               print(e)
               self.listbox.insert(END, 'Error finding all ' + self.t.get()+ " data")

    def clearButton(self): ##update to remove all dynamic variables at the end
        self.listbox.delete(0, END) ## clears the listbox
        self.listbox.insert(END, 'Search Cleared')
        currentTicker = ""
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
#def historicalData()

    
    period1 = int(time.mktime(datetime.datetime.now().timetuple()))
    
    period2 = int(time.mktime(datetime.datetime.(datetime.datetime.now() - datetime.timedelta(days = 365)).timetuple()))
    
    print(period1)
    interval = ("1d")

    yahooQuery = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'






def main():
    root = Tk()
    root.configure(background="white")
    root.geometry("1200x750")
    all = Menu(root)
    root.title('Stock Event Finder')
    root.pack_propagate(1)
    root.mainloop()

if __name__ == "__main__":
    main()