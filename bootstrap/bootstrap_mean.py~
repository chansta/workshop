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

N = 1000 #Initial sample size
B = 500 #number of bootstrap sample ie replication. 
m = 3 #True mean of the data
s = 2 #True standard deviation of the data. 
data = sps.norm.rvs(size=N, loc=m, scale=s) #generating the random sample from normality. 
mhat = sps.tmean(data) #calculate sample mean estimate. 
shat2 = sps.tvar(data) #calcualte sample variance estimate. 
bootsample = [npr.choice(data,size=N,replace=True) for i in range(0,B)] #generate B bootstrap samples. 
bootmean = [sps.tmean(s) for s in bootsample]
plt.hist(bootmean,bins=np.floor(B/10))
plt.show()
print('The population mean is {0}'.format(m))
print('The population variance is {0}'.format(np.power(s,2)))
print('The estimated mean is {0}'.format(mhat))
print('The estimated variance is {0}'.format(shat2))
print('The mean of the bootstrapped sample mean is {0}'.format(sps.tmean(bootmean)))
print('The variance of the bootstrapped sample mean is {0}'.format(sps.tvar(bootmean)))
print('The theoretical variance of the estiamted mean is {0}'.format(shat2/float(N)))

