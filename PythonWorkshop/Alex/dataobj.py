############################################################################################################################
"""
name: dataobj.py (class)
created by: Felix chan
email: fmfchan@gmail.com
date created: 2012.10.10
last updated:	2013.12.18 - Replacing print statement with print() function. 	
History:	2013.12.12 - Updated function MergeRow, including colname and rowname. 
		2013.08.20

"""
###########################################################################################################################

import numpy as np
import scipy as sp 
import scipy.stats as sps
import matplotlib.pyplot as plt
import copy as copy
#from data import * 

class dataobj(object):
	"""
		Create a data object similar to dataframe in R. It uses data.py to import data. 
	Input:
		filename: Can either be a filename or a NXT numpy.array
		sep: column separator in the file
		skip: number of line to skip before start importing data
		index: True if the first column contains date in the case of importing data from file. In the case of numpy.array, index can equal a list of date corresponds to the data. 
		header: True if importing data with variable names in the first row. In the case of numpy.array, header can be a list of variable names.
	Members:
		self.data: a NXT numpy.array of data
		self.N: The number of variables
		self.T: The number of observations
		self.header: The list of variable names
		self.date: A list containing the date information of the data
		self.mean: Numpy.array of size self.N contaiing the mean of the data
		self.variance: Numpy.array of size self.N containing the variance of the data
		self.covariacne: Numpy.array of size self.N X self.N containing the variance-covariance matrix of the date
		self.correlation: Numpy.array of size self.N X self,.N containing the correlaton matrix of the data
		
	"""

	def __init__(self, filename, sep=",", skip=0, index=True, header=True): 
		if type(filename) == str:
			allm = gendata(filename, sep=sep, skip=skip, index=index, header=header)
			if index==True:
				self.date = allm[0] 
				self.data = allm[1]
				self.header = allm[2]
			else:
				self.data = allm[0]
				self.header = allm[1]
				self.date = "none"
			self.data = self.data.transpose()
		else:
			self.data = filename
			self.date = index
			self.header = header
		self.N,self.T = self.data.shape
		self.mean = [sps.tmean(i) for i in self.data]
		if self.N > 1:
			self.variance = [sps.tvar(i) for i in self.data]
		else:
			self.variance = [sps.tvar(self.data)]
		self.mean = np.array(self.mean)
		self.variance = np.array(self.variance)
		self.covariance = np.zeros((self.N, self.N))
		self.correlation = np.zeros((self.N, self.N))
		self.skewness = 0
		self.kurtosis = 0
		self.dmean = (self.data.transpose()-self.mean).transpose()
		self.did_covar = False
		self.JB = 0
		self.JBpvalue = 0 

	def covar(self, sample=True):
		"""
			Calculate the variance-covariance matrix of the given data. 
			Input:
				sample: If true then the sample version will be used. 
			Members Updated:
				dataobj.covariance
				dataobj.correlation
		"""
		self.covariance = np.dot(self.dmean, self.dmean.transpose())
		if sample == True:
			self.covariance = self.covariance/(self.T-1)
		else:
			self.covariance = self.covariance/self.T
		std = [1/pow(j,0.5) for j in np.diag(self.covariance)]
		std = np.diag(np.array(std))
		self.correlation = np.dot(np.dot(std,self.covariance), std) 
		self.did_covar = True

	def __HigherOrder__(self, order=3):
		"""
			Sum of data after it is being raised by a power specified in order. 
			Input:
				order: 
			Output:
				sho: 
				
		"""
		ho = [np.power(j,order) for j in self.dmean]
		sho = np.array([sum(j) for j in ho])
		return sho.reshape(self.N)

	def skew(self):
		"""
			Calculate sample skewness.
		"""
		if self.did_covar==False:
			self.covar() 
		self.skewness = self.__HigherOrder__()/((self.T-1)*np.power(np.diag(self.covariance),3/2))
		return self.skewness
	
	def kurt(self):
		"""
			Calculate sample kurtosis.
		"""
		if self.did_covar==False:
			self.covar()
		self.kurtosis = self.__HigherOrder__(order=4)/((self.T-1)*np.power(np.diag(self.covariance),2))
		return self.kurtosis

	def JBtest(self):
		"""
			Calculate the Jarque-Bera test of normality. 
		"""
		self.skew()
		self.kurt()
		self.JB = self.T*(pow(self.skewness,2)+0.25*pow((self.kurtosis-3),2))/6
		self.JBpvalue =1-sps.chi2.cdf(self.JB, 2)
		return self.JB, self.JBpvalue
	
	def summary(self, LaTeX=False):
		"""
			Print Descriptive Statistics for each variable in the object. 
		"""
		if (self.did_covar==False)&(self.N>1):
			self.covar()
		self.JBtest()
		allm = np.c_[self.mean, np.power(self.variance,0.5), self.skew(), self.kurt(), self.JB, self.JBpvalue]
		lall = [["{0:.8f}".format(i) for i in l] for l in allm]
		[lall[i].insert(0,"{0:9}".format(self.header[i])) for i in range(0,self.N)]
		label = ["{0:9}".format("Variables"), "{0:9}".format("Mean"), "Deviation", "Skewness", "Kurtosis", "{0:9}".format("JB Test"), "JB P-value"] 
		lall.insert(0, label)
		s = "\n".join(["\t".join([i for i in l]) for l in lall])
		print("The number of variable(s) is {0}".format(self.N))
		print("The number of observations is {0}\n".format(self.T))
		print(s)
		if self.N>1:
			print("\nThe Correlation Matrix is")
			print(self.correlation)
			print("\nThe variance-covariance matrix is ")
			print(self.covariance)
		if LaTeX!=False:
			lall = [["{0:.3f}".format(i) for i in l] for l in allm]
			[lall[i].insert(0,"{0:9}".format(self.header[i])) for i in range(0,self.N)]
			lall.insert(0, label)
			s = "\\\\ \n".join(["&".join([i for i in l]) for l in lall])
			beginning = "\\begin{tabular}{c|cccccc|} \n \\hline \n"
			end = "\\\\ \n \\hline \\end{tabular} \n"
			alls = beginning + s + end
			fout = open(LaTeX, "w")
			fout.write(alls)
			fout.close()
	
	def showgraph(self, s=[2,2]):
		plt.rcParams["font.size"]=10
		if self.data != "none":
			x = np.linspace(0,self.T-1, 5)
			xloc = [int(np.floor(i)) for i in x]
			xlabel = [self.date[i] for i in xloc]
		j = 1
		for i in self.data:
			plt.subplot(s[0], s[1], j)
			plt.plot(i)
			if len(self.header)>0:
				plt.title(self.header[j-1])
			if self.date != "none":
				plt.xticks(xloc, xlabel)
			j = j + 1
		plt.show()
	
	def extract_var(self, var):
		"""
			Extract the data for variables listed in var. 
			Input:
				var: a list containing names of variable to be extracted. 
			Output:
				newobj: a dataobj object containing the data for the variables as listed in var
		"""
		if all([i in self.header for i in var])==False:
			print("Not all the variables are in the dataset.")
			return 0
		else: 
			indexset = [self.header.index(i) for i in var]
			X = self.data[indexset]
			return dataobj(X, index=self.date, header=var)
				
def gendata(filename, sep=",", skip=0, index=True, header=True):
	"""
	Import data from a text file. If index is true then the first column will be treated as an identifier.
	Input:
		filename: The name of the file containing the data 
		sep: The separator used to separate columns
		skip: The number of line to skip before importing the first row of data
		index: True if the first column contains date information
		header: True if the first row contains the name of the variables. 
	Output:
		return datef, m, headerinfo if index is true. 
		return m, headerinfo if index is false. 
		In the case when header is false, headerinfo is an empty list. 
		
	"""
	f = open(filename)
	m = []
	headerinfo = []
	if index == True:
		datef = []
	for i,line in enumerate(f):
		if i >= skip:
			source = line.split(sep)
			n = len(source)
			source[n-1] = source[n-1].rstrip()
			if (i==skip)&(header==True):
				if index==True:
					headerinfo = source[1:n]
				else:
					headerinfo = source
			else:
				if index==True:
					temp = np.array([float(i) for i in source[1:n]])
					datef.append(source[0])
				else: 
					temp = np.array([float(i) for i in source[0:n]])
				m.append(temp)
	f.close()
	#m.pop()
	m = np.array(m)
	T,N = m.shape
	if len(headerinfo)==0:
		headerinfo = ["v"+str(i+1) for i in range(0,N)]
	if index==True:
	#	datef.pop()
		return datef,m, headerinfo
	else:
		return m, headerinfo

def vec_data(filename, sep=",", sortby="time", savefilename=False):
	"""
		Convert a rectangular matrix of data into column. Assuming the first row contains names and the first column contains date
	"""
	f = open(filename)
	dateinfo = []
	data = []
	for i,line in enumerate(f):
		if i==0:
			names = line.split(sep)
			names = names[1:len(names)]
			names[len(names)-1]=names[len(names)-1].rstrip()
			N = len(names)
		else:
			temp = line.split(sep)
			temp[len(temp)-1].rstrip()
			dateinfo.append(temp[0])
			data.append([float(j) for j in temp[1:len(temp)]])
	f.close()
	T = len(dateinfo)
	data = np.array(data).transpose().reshape(N*T)	
	if sortby == "time":
		dateinfocol = dateinfo*N
		namescol = []
		for i in range(0,N):
			namescol = namescol + [names[i]]*T
	else:
		namescol = names*T
		dateinfocol = []
		for i in range(0,T):
			dateinfocol = dateinfocol+[dateinfo[i]]*N
	if savefilename != False: 
		m = [[dateinfocol[i], namescol[i], str(data[i])] for i in range(0,T*N)]
		s = "\n".join([",".join([j for j in l]) for l in m])
		f = open(savefilename,"w")
		f.write(s)
		f.close()
	return dateinfocol, namescol, data

def writeRdata(filename, m, sep=",", header=0, do_transpose=True):
	"""
	Export the numpy array m to a file, filename. Variable names can be included in header. 
	"""
	if do_transpose == True:
		s = "\n".join([sep.join([str(j) for j in i]) for i in m.transpose() ])
	else:
		s = "\n".join([sep.join([str(j) for j in i]) for i in m])
	if header!=0:
		head = sep.join([i for i in header])+"\n" 
		s = head+s
	f = open(filename, "w")
	f.write(s)
	f.close()

def MergeRow(savefilename, m1, m2, bracket=["(", ")"], colname=None, rowname=None):
	"""
	Merge two arrays m1 and m2. The first row in m2 will appear under the first rwo from m1 with a bracket added. Its output will be saved to savefilename. 
	"""
	
	N,T=m1.shape
	m = []
	if (T>=2):
		x = [["{0:.3f}".format(j) for j in l] for l in m1]
		y  = [[bracket[0]+"{0:.3f}".format(j)+bracket[1] for j in l] for l in m2]
		
	else:
		x = ["{0:.3f}".format(j) for j in m1]
		y  = [bracket[0]+"{0:.3f}".format(j)+bracket[1] for j in m2]
	for i in range(0,N):
		if rowname is None: 
			m.append(x[i])
			m.append(y[i])
		else:
			m.append([rowname[i]]+x[i])
			m.append(list(" ") + y[i])
	if (T>=2):
		s = "\n".join([",".join([i for i in l]) for l in m])
	else:
		s = "\n".join([i for i in m])
	if colname is not None: 
		header = ","+",".join([l for l in colname])+"\n"
		s = header + s
	f=open(savefilename,"w")
	f.write(s)
	f.close()

def format_table(filename, savefilename, model=False, bracket=["(", ")"], LaTeX=True):
	"""
		Filename contains even number columns N with the first N/2 columns containing coefficient estiamtes and the last N/2 columns contains the corresponding stnadard errors. The routine will put the standard errors under the associated coefficients with the bracket specified in the argument bracket.
	"""
	if type(filename) == str:
		m = dataobj(filename)
	elif type(filename).__name__ != "dataobj":
		print("File {0} is not being supported.".format(filename))
	N,nvar = m.data.shape
	nmodel = N/2 
	coef = m.data[0:nmodel]
	std = m.data[nmodel:N] 
	coefs = [["{0:.3f}".format(i) for i in l] for l in coef.transpose()]
	stds = [["{0:.3f}".format(i) for i in l] for l in std.transpose()]
	s = ""
	if LaTeX==False:
		if model != False:
			s = "&" + "&".join(model)+" \n"
		for i in range(0,nvar):
			s = s+m.date[i]+"&"+"&".join([j for j in coefs[i]]) + "\n" + "&"+"&".join([bracket[0]+k+bracket[1] for k in stds[i]])+"\n"
	else: 
		for i in range(0,nvar):
			s = s+m.date[i]+"&"+"&".join([j for j in coefs[i]]) + "\\\\\n" + "&"+"&".join([bracket[0]+k+bracket[1] for k in stds[i]])+"\\\\\n"
		header = "\\begin{tabular}{c|"
		for i in range(0,nmodel):
			header = header + "c"
		header= header + "|} \n \\hline"
		if model != False:
			header = header + "&" + "&".join(model)+"\\\\ \\hline \n"
		end = "\hline\\end{tabular}"
		s = header + s + end
	f = open(savefilename, "w")
	f.write(s)
	f.close()
"""
def add_lag(obj):
	Create a dataobject from obj with lag variables. 
	Input: 
		obj: a dataobj object
	Output:
		An dataobj with the same variables as obj as well as their lag values.
	data = copy.copy(obj.data)
	fdata = data.transpose()[1:obj.T].transpose()
	ldata = data.transpose()[0:obj.T-1].transpose()
	cdata = np.r_[fdata, ldata]
	header = obj.header + ["l1."+i for i in obj.header]
	newobj = dataobj(filename=cdata,header=header, index=obj.date[1:obj.T])
	return newobj
"""
def add_lag(obj, lag=1):
	"""
	Create a dataobject from obj with lag variables. 
	Input: 
		obj: a dataobj object
		lag: how many lag to add. Default is 1. 
	Output:
		An dataobj with the same variables as obj as well as their lag values.
	"""
	if lag > obj.T:
		s = "You don't have enough obervsations. The number of observations is {0} and the number of lag is {1}.".format(obj.T, lag)
		print(s)
	data = copy.copy(obj.data)
	cdata = data.transpose()[lag:obj.T].transpose()
	header = copy.copy(obj.header)
	for i in range(1,lag+1):
		temp = data.transpose()[lag-i:obj.T-i].transpose()
		cdata = np.r_[cdata,temp]
		header = header + ["l"+str(i)+"."+j for j in obj.header] 
	newobj = dataobj(filename=cdata, header = header, index=obj.date[lag:obj.T])
	return newobj



