##############################################################################################################################
"""
Name:               datastream.py
Author:             Felix Chan
Email:              fmfchan@gmail.com
Date Created:       2016.02.05
Description:        Data maangement with Pandas. 
"""
##############################################################################################################################

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

filename = "datastream_equities_201405.csv" #define filename
m = pd.read_csv(filename, header=0, index_col=0) #import file using read_csv function. 
print(m.keys()) # get columns name. 
print(m.describe()) #get basic summary statistics. 
applemax = m.sort_values(by='Apple', ascending=False) #sort vlaues from highest to lowest based on Apple's price. 
print(applemax.iloc[0:10,:]) 
ms = pd.Series(m['MS'], index=m.index) #extracting Microsfot price as a single series. 
ms.plot() #can use plt.plot but the pd.Series has its own interface to matplotlib.pytplot
plt.title("Stock Price of Microsoft")
plt.show()
T = len(m.index)
#####################################################################################################################
# The next few lines calculate the returns for every stock in the dataset and add the series to the dataset. 
for i in m.columns:
    keyname = "returns"+i
    rtemp = np.zeros(T)
    rtemp[1:T] = 100*np.log(m[i].values[1:T]/m[i].values[0:T-1])
    m[keyname] = rtemp
#Exercise: turns this into a function. Take a pandas dataframe as input and return the dataframe with return series. 
#####################################################################################################################
plt.subplot(2,1,1) #Creating subplot. In this case, in a 2 X 1 grid and the current position is the (1,1) subgrid. 
m['returnsApple'].plot()  #This goes to the top plot and plot the return time series for Apple. 
plt.title("The returns of Apple")
plt.subplot(2,1,2) #Move to the (2,1) subgrid. 
m['returnsApple'].hist(bins=50) #plot histogram of Apple's return in the (2,1) subgrid. 
plt.title("The histogram of Apple Returns")
plt.show()
filename = "exchangerate20120810.xlsx" #define filename
m1 = pd.read_excel(filename, sheet="sheet1", skiprows=0, header=1, index_col=0) #import file using read_excel function. 