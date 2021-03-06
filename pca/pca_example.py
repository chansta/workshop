i#############################################################################################################################################################################################
"""
Author:                 Felix Chan
Email:                  fmfchan@gmail.com
Created:                2016.07.15
Description:            An example file for pca.py using the sentiment.csv data.  

"""
#############################################################################################################################################################################################
mport pandas as pd
import pca as pca
import matplotlib.pyplot as plt

m = pd.read_csv('sentiment.csv', header=0, index_col=0)
var = [i for i in m.columns if i != 'ripo']
svd = pca.pca(m,var=var, method='svd')
eig = pca.pca(m,var=var,method='eigen')
print('The variance explained by using svd')
print(svd.variance)
print('The variance explained by using eigenvalue')
print(eig.variance)
plt.figure(0)
svd.pca.plot()
plt.figure(1)
eig.pca.plot()
plt.show()

