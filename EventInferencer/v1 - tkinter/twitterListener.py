#import requests
#import os 
#import json
#import twint
import random
import pandas as pd
import twint as tw
# marco = random.sample(range(1, 250), 5)

# print (marco)


def markerDates(df1): ###Demo function for assigning random values to days of importance
    #print(df1)
    dfLen = len(df1)
    # allDates = df1['Date']
    # print(allDates)
    marco = random.sample(range(0, dfLen), 5)
    marco = sorted(marco)
    return marco

# def markerDates(df1): ###Demo function for assigning random values to days of importance
#     marco = 1
#     return marco



#Class Twittersniffing: ###Contains primary comprehensive twitter analysis and relevant outputs
