import pandas as pd

df1 = pd.read_csv("C:/Users/mcgui/Desktop/Secondary/demo.csv")
df1['MA7'] = df1.rolling(window = 7).mean()  ##7-day Moving Average
df1 = df1.dropna()
MA7 = df1['MA7'].tolist()
deriv = list()
dflength = len(MA7)

for i in range(dflength):
    if i == dflength-2:
        break
    n = 2+i
    m = i
    derIndex = ((MA7[n])-(MA7[m]))/2   
    deriv.append(derIndex)
df1.drop(df1.head(1).index,inplace=True) # drop first row
df1.drop(df1.tail(1).index,inplace=True) # drop last row
df1['∆^2'] = deriv
df_maxdates = df1[(df1['∆^2']<0.15) & (df1['∆^2']>-0.15)]
max_dates = df_maxdates.sort_values(by=['MA7']).tail(5)
max_dates = max_dates['Date']
print(max_dates)



