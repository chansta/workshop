#You will need to download these three modules:
import numpy as np
import scipy as sp 
import matplotlib.pyplot as plt 
#--------------------------------------------------
#Comment the next two lines out if you have dataobj.py in the same directory. If not, change path to the location of your dataobj.py file.
path = "/Users/229922I/research/python/econometrics"
import sys
sys.path.insert(0,path) 
import dataobj as dob
#--------------------------------------------------
from scipy.stats import uniform
import copy

#import data using dob.dataobj
m = dob.dataobj("ClosePrice.csv") 
#calculate returns
rmtemp = 100*np.log(m.data.transpose()[2:m.T]/m.data.transpose()[1:m.T-1])
#import returns to the dataobject
rm = dob.dataobj(rmtemp.transpose(), index=m.date[1:m.T], header=m.header) 

#Draw some histograms
plt.figure(0)
k=1
for i in rm.data:
    plt.subplot(2,4,k)
    plt.hist(i, bins=50, normed=True)
    plt.xlabel(rm.header[k-1])
    k=k+1
#plt.show()

replication = 1000
ThreeMmeans = np.zeros(replication)
for i in range(0,replication):
    #print("Hello, I am doing replication {0} out of {1}. Leave me alone, go and grab a coffee.\n".format(i+1, replication))
    boots_index = [int(np.floor(j)) for j in uniform.rvs(size=rm.T, loc=0, scale=rm.T-1)]
    ThreeMmeans[i] = sp.stats.tmean(rm.data[0][boots_index])

sThreeMeans = copy.copy(ThreeMmeans)
sThreeMeans.sort()
alpha = 0.05
cvlower,cvupper = sThreeMeans[int(np.floor(len(sThreeMeans)*alpha))], sThreeMeans[int(len(sThreeMeans)-np.floor(len(sThreeMeans)*alpha))]


