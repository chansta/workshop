import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

import sys
sys.path.insert(0,"/Users/229922I/research/python/econometrics")
import dataobj as dob

from scipy.stats import uniform
import copy 

def moving_average(m, N=20): 
	"""
	Calculate N days moving average for stock, stock. 
	Input: 
		m: a KXT numpy array containing T time series observations for K stocks. 
		N: an integer. The windows of moving average
	Output:
		mv: a KX(T-N) numpy array containing the N moving averages for stock. 
	"""
	K,T = m.shape # The method shape returns the number of rows (K) and the number of columns (T)
	mv = np.zeros((K,T-N)) #initiate the output variables with size K X (T-N)
	for i,s in enumerate(m): 
		temp = [sp.stats.tmean(s[t-N:t]) for t in range(N,T)]	
		mv[i] = temp
	return mv

def entry_buy(op, cp, mv): 
	"""
	Determine the entry for buying 
	Input:
		op: a scalar denoting the open price the next time period 
		cp: a scalar denoting the closing price of the same day as the moving average
		mv: a scalar denoting the moving price of the last N days 
	Ouput:
		Boolean: True if entry happens otherwise False
	"""
	if mv < cp and mv < op:
		return True 
	else: 
		return False

def entry_sell(op, cp, mv):
	"""
	Determine the entry for selling 
	Input:
		op: a scalar denoting the open price the next time period 
		cp: a scalar denoting the closing price of the same day as the moving average
		mv: a scalar denoting the moving price of the last N days 
	Ouput:
		Boolean: True if entry happens otherwise False
	"""
	if mv > cp and mv > op:
		return True 
	else: 
		return False

def exit_trendreverse_buy(mv, cp):
	"""
	Determine exit status due to trend reversal. 
	Input:
		mv: a scalar denoting the moving average of the last N days
		cp: a scalar denoting the closing price of the same day. 
	Output:
		Boolean: True if exit happens and False otherwise.
	"""
	if cp < mv:
		return True
	else:
		return False

def exit_trendreverse_sell(mv, cp):
	"""
	Determine exit status due to trend reversal. 
	Input:
		mv: a scalar denoting the moving average of the last N days
		cp: a scalar denoting the closing price of the same day. 
	Output:
		Boolean: True if exit happens and False otherwise.
	"""
	if cp > mv:
		return True
	else:
		return False

def exit_varloss(entryprice, cp, varloss):
	"""
	Determine exit status due to accumulative returns less than worse case VaR
	Input: 
		entryprice: a scailar indicating the price at the time of entry. 
		cp: a scalar denoting the closing price of the current day. 
	Output:
		Boolean: True if exit happens and False otherwise.
	"""
	ar = 100*np.log(cp/entryprice)
	if ar <= var: 
		return True
	else: 
		return False

def exit_vargain(entryprice, cp, vargain): 
	"""
	Determine exit status due to accumulative returns greater than best case VaR
	Input:
		entryproce: a scalar indicating the price at the time of entry
		cp: a scalar denoting the closing price of the current day
	Output:
		Boolean: True if exit happens and False otherwise.
	"""
	ar = 100*np.log(cp/entryprice)
	if ar > vargain:
		return True
	else:
		return False

def bootstrap(rm, alpha=0.05, replication=1000):
	"""
	Bootstrap the Vargain and Varloss based on the return data. 
	Input:
		rm: a T numpy.array containing return data. 
		alpha: a scalar representing the significant level
		replication: a scailar representing the number of replicaiton in the bootstrap
	"""
	T = len(rm)
	ThreeMmeans = np.zeros(replication)
	for i in range(0,replication):
	    boots_index = [int(np.floor(j)) for j in uniform.rvs(size=T, loc=0, scale=T-1)]
	    ThreeMmeans[i] = sp.stats.tmean(rm[boots_index])
	sThreeMeans = copy.copy(ThreeMmeans)
	sThreeMeans.sort()
	varloss,vargain = sThreeMeans[int(np.floor(len(sThreeMeans)*alpha))], sThreeMeans[int(len(sThreeMeans)-np.floor(len(sThreeMeans)*alpha))]
	return varloss,vargain

def trade_stock(mv, op, cp, varloss, vargain, N=20, alpha=0.05, replication=1000):
	"""
	Trade stock based on opening, closing and moving average price by executing various entry and exit rules. 
	Input:
		mv: a T-N numpy array of moving average. 
		op: a T numpy array of openning prices. 
		cp: a T numpy array of closing prices. 
		N: a scalar representing the windows of moving averages. 
		alpha: a scalar denoting the significant level for the calculation of VaR. 
		replication: a scalar indicating the number of replication in bootstrapping. 
		varloss: var for worse case
		vargain: var for best case
	Output:
		profit: total gain/loss of trade. 
		no_entry_sell: total number of sell entries. 
		no_entry_buy: total number of buy entries. 
		no_profit_entry: total number of profit entry.
		ptofit_pertrade = profit/(no_entry_sell+no_entry_buy) 
	"""
	T = len(op)
	buy_status = False
	sell_status = False
	no_entry_buy = 0
	no_entry_sell = 0
	no_profit_entry = 0
	profit = 0
	for t in range(N+1,T):
		if entry_buy(op[t], cp[t-1], mv[t-N-1]) and buy_status is False and sell_status is False:
			buy_status = True
			time_of_entry = t
			no_entry_buy = no_entry_buy+1
		elif buy_status is True: 
			if exit_trendreverse_buy(mv[t], cp[t]) or exit_varloss(op[time_of_entry], cp[t], varloss) or exit_vargain(op[time_of_entry], cp[t], vargain):
				buy_status = False
				tempprof = 100*np.log(cp[t]/op[time_of_entry])
				profit = profit + tempprof 
				if tempprof > 0:
					no_profit_entry = no_profit_entry + 1
		elif entry_sell(op[t], cp[t-1], mv[t-N-1]) and buy_status is False and sell_status is False:	
			sell_status = True
			time_of_entry = t
			no_entry_sell = no_entry_sell+1
		elif sell_status is True: 
			if exit_trendreverse_sell(mv[t], cp[t]) or exit_varloss(op[time_of_entry], cp[t], varloss) or exit_vargain(op[time_of_entry], cp[t], vargain):
				sell_status = False
				tempprof = 100*np.log(cp[t]/op[time_of_entry])
				profit = profit + tempprof 
				if tempprof > 0:
					no_profit_entry = no_profit_entry + 1
	return profit,no_entry_sell,no_entry_buy,no_profit_entry,profit/(no_entry_sell+no_entry_buy) 



######################################################################################################################
#A block time wasting code to convince Alex
N=20
m = dob.dataobj("ClosePrice.csv")
mv = moving_average(m.data[0:4], N=N)
K,T = mv.shape
T = 500
for i,s in enumerate(mv):
	plt.subplot(K,1,i+1)
	plt.plot(range(0,T+N), m.data[i][0:T+N], "r", range(N,T+N), mv[i][0:T], "b")
plt.show()

######################################################################################################################
	
