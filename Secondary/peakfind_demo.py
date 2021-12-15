import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from scipy.signal import find_peaks




#do some stuff

df = pd.read_csv("C:/Users/mcgui/Desktop/Secondary/whyamazon.csv")
df1 = df.iloc[::-1]
data_y = (df1['Attention Score']).iloc[::-1]
data_x = (df1['Index'])

df = pd.DataFrame({'Index': data_x, 'AttentionScore':data_y}, columns = ['index','AttentionScore'])
print(df)
#Find_peaks------------------------
peaks, _ = find_peaks(data_y, height=0, distance = 7)
peak_days = pd.DataFrame(peaks, columns = ['peak dates'])
peak_heights = pd.DataFrame(peaks, )
#peak_days = peak_days.sort_values(by=['peak dates']).head(5)
print(peak_days)
print(peak_heights)

# for peak_days in df['Index']:
#     print

plt.plot(data_y)
plt.plot(peaks, data_y[peaks], "x")
plt.plot(np.zeros_like(data_y), "--", color="gray")
plt.show()
