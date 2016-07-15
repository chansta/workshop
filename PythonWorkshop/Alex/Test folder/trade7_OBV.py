import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import sys
sys.path.insert(0,"/Users/229922I/research/python/econometrics")
import dataobj as dob

from scipy.stats import uniform
import copy 

def accumulation(x):
    """
    Give x, calcualte the accumulated sum
    """
    T = len(x)
    return [sum(x[0:i]) for i in range(1,T)]

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
	mv = np.zeros((K,T-N+1)) #initiate the output variables with size K X (T-N)
	for i,s in enumerate(m): 
		temp = [sp.stats.tmean(s[t-N:t]) for t in range(N,T+1)]	
		mv[i] = temp
	return mv

def entry_buy(OBV, mv): 
	"""
	Determine the entry for buying 
	Input:
		OBV: a 2 X 1 array containing OBV for two consecutive days 
		mv: a 2 X 1 array containing moving averages for two consecutive days
	Ouput:
		Boolean: True if entry happens otherwise False
	"""
	if OBV[1] > mv[1] and OBV[0] <= mv[0]: 
		return True 
	else: 
		return False

def entry_sell(OBV, mv):
	"""
	Determine the entry for selling 
	Input:
		OBV: a 2 X 1 array containing OBV for two consecutive days 
		mv: a 2 X 1 array containing moving averages for two consecutive days
	Ouput:
		Boolean: True if entry happens otherwise False
	"""
	if OBV[1] < mv [1] and OBV[0] >= mv[0]:
		return True 
	else: 
		return False

def exit_trendreverse_buy(mv, OBV):
	"""
	Determine exit status due to trend reversal. 
	Input:
		mv: a scalar denoting the moving average of the last N days
		OBV: a scalar denoting the OBV of the same day. 
	Output:
		Boolean: True if exit happens and False otherwise.
	"""
	if OBV < mv:
		return True
	else:
		return False

def exit_trendreverse_sell(mv, OBV):
	"""
	Determine exit status due to trend reversal. 
	Input:
		mv: a scalar denoting the moving average of the last N days
		OBV: a scalar denoting the OBV of the same day. 
	Output:
		Boolean: True if exit happens and False otherwise.
	"""
	if OBV > mv:
		return True
	else:
		return False

def exit_varloss(entryprice, cp, varloss, status):
	"""
	Determine exit status due to accumulative returns less than worse case VaR
	Input: 
		entryprice: a scailar indicating the price at the time of entry. 
		cp: a scalar denoting the closing price of the current day. 
	Output:
		Boolean: True if exit happens and False otherwise.
	"""
	ar =np.log(cp/entryprice)
        if status is "short":
            ar = -ar
	if ar <= varloss: 
		return True
	else: 
		return False

def exit_vargain(entryprice, cp, vargain, status): 
	"""
	Determine exit status due to accumulative returns greater than best case VaR
	Input:
		entryproce: a scalar indicating the price at the time of entry
		cp: a scalar denoting the closing price of the current day
	Output:
		Boolean: True if exit happens and False otherwise.
	"""
	ar = np.log(cp/entryprice)
        if status is "short":
            ar = -ar
	if ar > vargain:
		return True
	else:
		return False
def bootstrap_extreme(rm, alpha=0.05, replication=1000):
	"""
	Bootstrap the Vargain and Varloss based on the return data. 
	Input:
		rm: a T numpy.array containing return data. 
		alpha: a scalar representing the significant level
		replication: a scailar representing the number of replicaiton in the bootstrap
	"""
	T = len(rm)
	vargain_m = np.zeros(replication)
        varloss_m = np.zeros(replication)
	for i in range(0,replication):
	    boots_index = [int(np.floor(j)) for j in uniform.rvs(size=T, loc=0, scale=T-1)]
            tempboots = rm[boots_index]
            tempboots.sort()
	    vargain_m[i] = tempboots[int(np.floor((1-alpha)*T))]
            varloss_m[i] = tempboots[int(np.floor((alpha)*T))] 
	varloss,vargain = sp.stats.tmean(varloss_m), sp.stats.tmean(vargain_m) 
	return varloss,vargain

def trade_stock_1(OBV, mv, op, cp, varloss, vargain, N=20, alpha=0.05, replication=1000):
	"""
	Trade stock based on opening, closing and moving average price by executing various entry and exit rules. 
	Input:
		OBV: a T numpy array of OBV
            mv: a T numpy array of moving average of OBV. 
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
        ################################################
        #variables for debugging purposes
        status_list = ["none"]
        entry_list = []
        exit_list = []
        entry_price_list = []
        exit_price_list = []
        ################################################
	T = len(op)
        status = "none"
	profit_list = []
        profit = 0
	for t in range(N+1,T):
            temp_mv = np.array([mv[t-2], mv[t-1]])
            temp_OBV = np.array([OBV[t-2], OBV[t-1]])
            if status is "none": 
                if entry_buy(temp_OBV, temp_mv) and op[t] >= op[t-1]: 
                    status = "long"
                    entryprice = op[t]
                    entrytime = t
                    ####-----debugging variables ------#####
                    status_list.append(status)
                    entry_list.append(t)
                    entry_price_list.append(op[t])
                    ####-----End debugging variables ------#####
                elif entry_sell(temp_OBV, temp_mv) and op[t] <= op[t-1]: 
                    status = "short"
                    entryprice = op[t]
                    entrytime = t
                    ####-----debugging variables ------#####
                    status_list.append(status)
                    entry_list.append(t)
                    entry_price_list.append(op[t])
                    ####-----End debugging variables ------#####
            else:
                if status is "long" and (exit_trendreverse_buy(mv[t],OBV[t]) or exit_varloss(op[entrytime],cp[t],varloss, status) or exit_vargain(op[entrytime], cp[t], vargain, status)):  
                    profit_list.append(np.log(cp[t]/op[entrytime]))
                    if exit_trendreverse_buy(mv[t],OBV[t]):
                        status = "short"
                    else:
                        status = "none"
                    ####-----debugging variables ------#####
                    status_list.append(status)
                    exit_price_list.append(cp[t])
                    exit_list.append(t)
                    ####-----End debugging variables ------#####
                elif status is "short" and (exit_trendreverse_sell(mv[t],OBV[t]) or exit_varloss(op[entrytime],cp[t],varloss, status) or exit_vargain(op[entrytime], cp[t], vargain, status)):   
                    profit_list.append(-np.log(cp[t]/op[entrytime]))
                    if exit_trendreverse_sell(mv[t], OBV[t]):
                        status = "long"
                    else:
                        status = "none"
                    ####-----debugging variables ------#####
                    status_list.append(status)
                    exit_price_list.append(cp[t])
                    exit_list.append(t)
                    ####-----End debugging variables ------#####
        profit = sum(profit_list)
        return profit_list,profit,status_list,entry_list,exit_list,entry_price_list,exit_price_list

