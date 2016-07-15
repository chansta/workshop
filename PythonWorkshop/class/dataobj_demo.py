import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import sys #Do not need this line and the next line if you have the dataobj.py file in the same directory. 
sys.path.insert(0,"/Users/niteowl/research/python/econometrics")
import dataobj as dob

m = dob.dataobj("datastream_equities_201405.csv") #import data
tmp = m.data.transpose()
rtmp = np.log(tmp[1:m.T]/tmp[0:m.T-1])*100 # calculate returns
rm = dob.dataobj(rtmp.transpose(), index=m.date, header=m.header) #creating another dataobj based on the return data. 
