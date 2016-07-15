##############################################################################################################################
"""
Name:               sirca.py
Author:             Felix Chan
Email:              fmfchan@gmail.com
Date Created:       2016.02.05
Description:        Big Data maangement with Pandas.  
"""
##############################################################################################################################

import pandas as pd
import matplotlib.pyplot as plt

m = pd.read_csv("/Users/229922I/research/data/SIRCA/2005082.csv", index_col=[1,0], header=0) #Import data
print(m.keys()) #shows the keys of the data object - it is essentially a dictionary. 
ele = ('03-Jul-2003', 'WOW.AX') # define a key for the following examples. A particular stock on a particular date
print(m.loc[ele, 'Time':'L1-BPrc']) #extract a subset of data based on the index
t1 = pd.Series(m.loc[ele, 'L1-BPrc'].values, index = m.loc[ele,'Time']) #Create a time series for a particular stock on a particular date. 
t1.plot() #plot the series
plt.title("Plot of {0} on {1}".format(ele[1],ele[0])) #adding title to the plot
plt.ylabel("WoolWorth") #adding y label to the plot. 
plt.show()
