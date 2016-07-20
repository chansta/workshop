#!/usr/bin/python3
###########################################################################################################################################################################
"""
Author:                   Felix Chan
Email:                    fmfchan@gmail.com
Created:                  2016.07.14
Description:              Source code 1 on a course of bootstrapping. It demonstrates how to estimate mean and its standard error by bootstrapping. 

"""
###########################################################################################################################################################################
import numpy as np
import numpy.random as npr
import scipy.stats as sps
import scipy as sp
import matplotlib.pyplot as plt
import pandas as pd

N = 1000 #Initial sample size
B = 500 #number of bootstrap sample ie replication. 
m = 3 #True mean of the data
s = 2 #True standard deviation of the data. 
data = sps.norm.rvs(size=N, loc=m, scale=s) #generating the random sample from normality. 
mhat = sps.tmean(data) #calculate sample mean estimate. 
shat2 = sps.tvar(data) #calcualte sample variance estimate. 
bootsample = [npr.choice(data,size=N,replace=True) for i in range(0,B)] #generate B bootstrap samples. 
bootmean = [sps.tmean(j) for j in bootsample]
plt.hist(bootmean,bins=np.floor(B/10))
plt.show()
columns = ['True', 'Estimated', 'Bootstrap']
index = ['mean', 'variance']
result = [ [m,mhat,sps.tmean(bootmean)], [np.power(s,2)/N, shat2/N, sps.tvar(bootmean)]]
result = np.array(result)
resultpd = pd.DataFrame(result, columns=columns, index=index)
print(resultpd)


