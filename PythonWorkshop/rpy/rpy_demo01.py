#####################################################################################################################
"""
Name: 			rpy_demo01.py
author:			Felix Chan
email: 			fmfchan@gmail.com
date created:		2014.06.06
Description:		First demo to demonstrate rpy using the two different approach. 
"""
#####################################################################################################################

#loading necessary module
import sys
sys.path.insert(0, "/Users/229922I/research/python/econometrics")
import dataobj as dob
import numpy as np
import rpy2.robjects as r #core rpy module to call 
from rpy2.robjects.packages import importr #allow to load R package and call its function onto Python workspace. 
from rpy2.robjects.methods import RS4 #module to deal with S4 class in R

"""
Using Rpy with rpy2.robjects.globalenv[]
	rpy is an interface module allow one to interact between R and Python. It is not a R emulator but rather, it loads up R in the background and acts as a translator between the objects in R and objects in Python. 
	The command rpy2.robjects.r(command) (or simply r.r(command) in this example) executes the command as defined by the text string "command" (inside the brackets of the function) in the R space. Thus, this function gives you direct access to R. 
	As such, there are two ways to use rpy. One is to communicate between R and Python through a set of common variables by using the dictionay rpy2.robjects.globalenv[].

"""
N = 10
r.globalenv["n"] = N # pass N onto R and create a variable on R space called n which has the same value as N in python. 
r.r("y <- seq(n)") # execute the command "y <- seq(n)" in R. 
Y = r.globalenv["y"]  #pass the value of y in R onto the variable calls Y in python
print("Y is  a rpy objects {0}".format(Y))
type(Y) 
y = np.array(Y).reshape(N)
print("y is a numpy object {0}".format(y))

"""
	The second approach is to call the function from R directly onto the python workspace. 
"""
seq = r.r("seq") #load the function seq from R to python. 
X = seq(N) #call the function on python space (action is still happening in R though). 
print("X is {0}".format(x)) 

#It is also possible to create a dataframe in python and pass it onto R
def CreateDataFrame(m):
	"""
		This function create a dataframe object using dictionary. 
	Input:
		m: a dataobj 
	Output:
		df: a dictionary suitable to be passed onto R as dataframe
	"""
	N,T = m.N,m.T 
	ry = [(m.header[i], r.FloatVector(m.data[i])) for i in range(0,N)]
	dry = dict(ry)
	df = r.DataFrame(dry) 
	return df

m = dob.dataobj("cooley.csv") #loading data
dfm = CreateDataFrame(m) #creating dataframe 
r.globalenv["m"] = dfm  #passing the dictionary as dataframe onto R
importr("urca") #import the library urca. It has the same effects as library(urca) but this allows python to access function in urca as well. 
r.r("""
		m.adf = ur.df(m[["INF"]], type="trend")
		cv <- m.adf@cval
		teststat <- m.adf@teststat
		""") # a set of R command. This can be a string from a .r file. 
cv = r.globalenv["cv"] #grabbing the variable cv in R and save it to a variable cv in python
teststat = r.globalenv["teststat"] # grabbing the variable teststat in R and save it to a variable teststat in python
cv = np.array(cv).reshape((3,3)) #convert cv from a rpy object into a numpy object
teststat = np.array(teststat).reshape((3,1)) #convert teststat from a rpy vector object to a numpy object
print("The critical Values are \n {0}".format(cv))
print("The test statistics are \n {0}".format(teststat))

