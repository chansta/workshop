############################################################################################################################
"""
Name: lm.py (class)
Author: Felix Chan
Email: fmfchan@gmail.com
Date Created: 2012.10.10
Last Updated:	2013.12.28 - Replacing print statement with print() function 
History:	2013.01.13

"""
##########################################################################################################################
import numpy as np
import scipy as sp
import scipy.stats as sps
import matplotlib.pyplot as plt
import dataobj as dob

class lm:
	"""
	A collection of routines for estimating linear regression models. 
	Note: This is not finished yet. Only OLS under the classical assumption has been implemented. 
	Input:
		formula: In a format similar to R. It takes advantage of variable names if data is a data object as defined in dataobj (see data below). Otherwise, if data is numpy.ndarray, then the variable names should be the column index of the data matrix. For example, "1~c+2+3" means regressing the first column data against an intercept "c", the second and third column data. Alternatively, "Y~c+X+Z" means regressing the variable "Y" on an intercept, the variable X and the variable Z. These variable names must be in dataobj.header in the latter case. The absence of "c" means there is no intercept in the model.  
		data: Either a dataobj or TXN numpy.ndarray, where T is the number of observations and N is the number of variates. 
		header: If data is a numpy.ndarray then header can contain a list of variable names corresponds to the formula. 
		cov_method: "ols", calculated under the classical assumption; "residuals", calculated by taking the average of residuals. 
	Members:
		self.coef: the parameter estimates following the specificaion of the formula.
		self.cov: the variance-covariance matrix of self.coef
		self.sterr: the standard errors of self.coef
		self.tstats: the t-statistics of self.coef
		self.p: the p-values associated with the t-statistics
		self.sigma: the variance of the estimated errors
		self.omega: the variance-covariance matrix of residuals. Users must provide self.omega in the case of gls
		self.invOmega: the inverse of self.omega
		self.RSS: Residuals sum of squares
		self.MSS: Model sum of squares
		self.TSS: Total sum of squares
		self.fitted: fitted values of the dependent variable
		self.residuals: residuals from the fitted model 
		self.R2: R squared
		self.adjR2: Adjusted R squared
		self.F: F test statistics for regression
		self.pF: The p-value associated with the F test statistics 
		self.k: the number of parameters estiamted 	
		self.N: the number of variates in the data
		self.T: the number of observations
	"""

	def __init__(self, formula, data, header="default"):

		dformula = formula.split("~")
		self.formula = formula
		self.depvar = dformula[0] 
		self.explvar = dformula[1].split("+") #Deconstructing the formula: assigning dependent and explanatory variables. 
		if 'c' in self.explvar: #determine if there is an intercept in the model.
			self.explvar.remove('c') 
			self.intercept = True
		else:
			self.intercept = False
		if type(data)==np.ndarray: #Constructing the Y and X matricies based on the nature of "data"
			self.T, self.N = data.shape
			self.data = data.transpose()
			if header == "default":
				getindex = [int(i) for i in self.explvar]
				self.Y = self.data[int(self.depvar)]
				self.explvar = ["v"+str(i) for i in range(1,self.N+1)]
				self.depvar = "Y"
			else:
				self.header = header
				getindex = [self.header.index(i) for i in self.explvar]
				self.Y = self.data[self.header.index(self.depvar)]

		else:
			self.data = data.data
			self.N, self.T = self.data.shape
			self.header = data.header
			getindex = [self.header.index(i) for i in self.explvar]
			self.Y = self.data[self.header.index(self.depvar)]
		self.X = np.array([self.data[i] for i in getindex])
		if self.intercept == True:
			self.X = np.r_[np.ones((1,self.T)), self.X] 
			self.explvar.insert(0,"Intercept")
		self.estchoice = "ols" #setting the default estimator to ols. 
		self.X = self.X.transpose()
		self.Y = self.Y.reshape((self.T,1))
		self.k = self.X.shape[1]
		self.omega = np.eye(self.k) #setting the default covariance matrix for GLS as identity matrix.
		self.invOmega = np.linalg.inv(self.omega)
		self.residuals = 0
		self.fitted = 0
		self.coef = 0
		self.cov = 0
		self.sigma = 0
		self.sterr = 0
		self.tstats = 0
		self.p = 0
		self.RSS = 0 #Residuals sum of squares
		self.MSS = 0 #Model (Estiamted) sum of squares
		self.TSS = 0 #Totla sum of squares
		self.got_residuals = False

	def __ols__(self):
		"""
			Get the OLS estimator
		"""
		if self.estchoice == "ols" or self.estchoice == "ols_g":
			self.coef=np.dot(np.linalg.inv(np.dot(self.X.transpose(), self.X)), np.dot(self.X.transpose(), self.Y))
		elif self.estchoice == "gls": 
			wX = np.dot(self.invOmega, self.X) 
			wY = np.dot(self.invOmega, self.Y)
			self.coef=np.dot(np.linalg.inv(np.dot(self.X.transpose(), wX)), np.dot(self.X.transpose(), wY))
		else:
			print("The estimator has not been implemented yet.")

	def __residuals__(self):
		"""
			Calculate residuals and fitted values
		"""
		self.fitted = np.dot(self.X, self.coef)
		self.residuals = self.Y - self.fitted 
		self.got_residuals = True

	def __anova__(self):
		"""
			Partially finished anova table. Though it does provide R^2 and the variance-covariance matrix.
		"""
		if self.got_residuals == False:
			self.__residuals__()
		dy = self.Y - sp.stats.tmean(self.Y)
		dfy = self.fitted - sp.stats.tmean(self.Y)
		RSS = float(np.dot(self.residuals.transpose(), self.residuals).reshape(1))
		MSS = float(np.dot(dfy.transpose(),dfy).reshape(1))
		TSS = float(np.dot(dy.transpose(),dy).reshape(1))
		self.sigma = RSS/float(self.T-self.k)
		if self.estchoice == "ols":
			self.cov = self.sigma*np.linalg.inv(np.dot(self.X.transpose(), self.X))
		elif self.estchoice == "ols_g":
			invXX = np.dot(self.X.transpose(), self.X)
			XOX = np.dot(self.X.transpose(), np.dot(self.omega, self.X))
			self.cov = np.dot(invXX, np.dot(XOX, invXX)) 
		elif self.estchoice == "gls":
			temp = np.dot(self.X.transpose(), np.dot(self.invOmega, self.X))
			self.cov = np.linalg.inv(temp)
		else: 
			print("The variance estimator has not been implemented yet.")
		self.R2 = 1-RSS/TSS
		self.adjR2 = 1- (1-self.R2)*((self.T-1)/float(self.T-self.k))
		self.F = MSS/RSS*((self.T-self.k)/float(self.k-1))
		self.pF = 1-sps.f.cdf(self.F,self.k-1, self.T-self.k)
		self.RSS = RSS
		self.TSS = TSS
		self.MSS = MSS 

	def __sterr__(self):
		"""
			Calculate the standard errors, t statistics and p-values
		"""
		self.sterr = np.power(np.diag(self.cov),0.5)
		self.tstats = self.coef.reshape(self.k)/self.sterr
		self.p = 1-sp.stats.t.cdf(abs(self.tstats),self.T-self.k)
	
	def estimate(self, estimator="ols", cov=1):
		"""
			Users interface to estimate the specified model
			estimtor options: ols, ols_g, gls
		"""
		if estimator == "ols" or estimator =="ols_g":
			self.estchoice = estimator 
		elif estimator == "gls":
			if type(cov)==int:
				print("Please enter the covariance matrix to be used with GLS.")
			else:
				self.omega = cov
				self.invOmega = np.linalg.inv(cov)
				self.estchoice = estimator
		self.__ols__()
		self.__residuals__()
		if estimator == "ols_g":
			e = self.residuals
		self.__anova__()
		self.__sterr__()
		self.got_estimates = True
	
	def summary(self, showgraph=False):
		"""
			Present output
		"""
		col_label = ["Variables", "Coefficients", "Std. Errors", "t-statistics", "p-values"] 
		stats = np.c_[self.coef.reshape(self.k), self.sterr.reshape(self.k), self.tstats.reshape(self.k), self.p.reshape(self.k)]
		allm= [["{0:8.4g}".format(i) for i in l] for l in stats]
		[allm[i].insert(0, "{0:12}".format(self.explvar[i])) for i in range(0,self.k)]
		allm.insert(0,col_label)
		s = "\n".join(["\t".join([i for i in l]) for l in allm])
		print("The regression output for the model {0}".format(self.formula))
		print("The number of observation is {0}".format(self.T))
		print("The number of estimates is {0}".format(self.k))
		print("The dependent variable is {0}".format(self.depvar))
		print(s)
		print("The R^2 is {0}".format(self.R2))
		print("The adjusted R^2 is {0}.".format(self.adjR2))
		print("The F test statistics is {0} with p value {1}.".format(self.F, self.pF))
		if showgraph==True:
			plt.subplot(2,1,1)
			plt.plot(self.Y)
			plt.plot(self.fitted, "r-")
			plt.title("Data and Fitted Values")
			plt.legend(("{0}".format(self.depvar), "Fitted Values"))
			plt.subplot(2,1,2)
			plt.plot(self.residuals)
			plt.title("Residuals of {0}".format(self.depvar))
			plt.show()
