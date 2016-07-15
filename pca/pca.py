#############################################################################################################################################################################################
"""
Author:                 Felix Chan
Email:                  fmfchan@gmail.com
Created:                2016.07.15
Required:               pandas
Description:            Generate Principal Component base on a set of data in Pandas DataFrame. 

"""
#############################################################################################################################################################################################
import numpy as np
import scipy as sp
import pandas as pd

class pca(object):
    """
    Calculate Principal Components for a given data set X using either SVD or eigenvalue decomposition. 
    """

    def __init__(self, X, var='all',  method='svd'):
        """
        Input: 
            X: a pandas dataframe containing the data matrix.  
            var: a list of variables to be analysed. 
            method: 
                    'svd': singular value decomposition. 
                    'eigen': eigenvalue decomposition. 
        Output:
            pca.variance: the percentage of variance explained by each PCA. 
            pca.combination: the combination (eigenvectors) for constructing each PCA. 
            pca.pca: The generated PCA
        """
        self.method = method
        self.m = X
        self.var = var
        if self.var == 'all':
            self.data = self.m
        else:
            self.data = self.m[self.var]
        self.k = len(self.data.columns)
        self.pclabel = ['PC{0}'.format(i) for i in range(1,self.k+1)]
        if self.method == 'svd':
            self.svd()
        elif self.method == 'eigen':
            self.eigen()
        else:
            print('This method is not available in this class.') 

    def svd(self):
        U,s,V = np.linalg.svd(self.data-self.data.mean()) 
        self.variance = np.power(s,2)/sum(np.power(s,2))
        self.combination = V.transpose() 
        self.pca = np.dot(self.combination, self.data.values.transpose())
        self.pca = self.pca.transpose()
        self.pca = pd.DataFrame(self.pca, columns=self.pclabel, index=self.data.index)
        
    def eigen(self):
        w,V = np.linalg.eig(self.data.cov())
        self.variance = w/sum(w)
        self.combination = V
        self.pca = np.dot(V,self.data.values.transpose())
        self.pca = self.pca.transpose()
        self.pca = pd.DataFrame(self.pca, columns=self.pclabel, index=self.data.index)
            
