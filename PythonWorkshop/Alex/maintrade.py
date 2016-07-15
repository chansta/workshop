import numpy as np
import scipy as sp
import scipy.stats as sps
import matplotlib.pyplot as plt
import sys
#sys.path.insert(0,"/Users/229922I/research/python/econometrics")
import dataobj as dob

from scipy.stats import uniform
import copy 
from trade7 import * 
import time
N=20
alpha=0.05
input_type = "cp"
if input_type is "cp":
	m_cp = dob.dataobj("ClosePrice.csv")
	m_op = dob.dataobj("OpenPrice.csv") 
else:
     m_OBV = dob.dataobj("OBV.csv")
     m_cp = dob.dataobj("ClosePrice.csv") 
     m_op = dob.dataobj("OpenPrice.csv") 
K = m_cp.N
mv_cp = moving_average(m_cp.data, N=N)
mv_cp = np.c_[np.zeros((m_op.data.shape[0],N-1)), mv_cp]
r_cp = np.log(m_cp.data.transpose()[1:m_cp.T]/m_cp.data.transpose()[0:m_cp.T-1])
r_cp = r_cp.transpose()
#varloss,vargain = bootstrap(r_cp[choice])
total_profit = np.zeros(K)
no_total_trade = np.zeros(K)
no_profit_trade = np.zeros(K)
no_loss_trade = np.zeros(K)
no_long_trade = np.zeros(K)
no_short_trade = np.zeros(K)
no_long_profit = np.zeros(K)
no_short_profit = np.zeros(K)
no_long_loss = np.zeros(K)
no_short_loss = np.zeros(K)
test_stats = np.zeros(K)
start = time.time()
for rules in range(1,5):
	filename = input_type+str(0)+str(rules)+".csv"
	for choice in range(0,K):
		varloss,vargain = bootstrap_extreme(r_cp[choice], alpha=alpha)
		if rules is 1:
			profit_list,profit,status_list,entry_list,exit_list,entry_price_list,exit_price_list= trade_stock_1(mv_cp[choice], m_op.data[choice], m_cp.data[choice], varloss, vargain, N=N, alpha=alpha)
		elif rules is 2:
			profit_list,profit,status_list,entry_list,exit_list,entry_price_list,exit_price_list= trade_stock_2(mv_cp[choice], m_op.data[choice], m_cp.data[choice], vargain, N=N, alpha=alpha)
		elif rules is 3:
			profit_list,profit,status_list,entry_list,exit_list,entry_price_list,exit_price_list= trade_stock_3(mv_cp[choice], m_op.data[choice], m_cp.data[choice], varloss, N=N, alpha=alpha)
		elif rules is 4:
			profit_list,profit,status_list,entry_list,exit_list,entry_price_list,exit_price_list= trade_stock_4(mv_cp[choice], m_op.data[choice], m_cp.data[choice], N=N, alpha=alpha)
		total_profit[choice] = profit
		temp = [i for i in status_list if i is not "none"]
		if len(temp) != len(profit_list):
			temp = temp[0:len(temp)-1]
		no_profit_trade[choice] = len([i for i in profit_list if i>0]) 
		no_loss_trade[choice] = len(profit_list)-no_profit_trade[choice]
		no_long_trade[choice] = len([i for i in temp if i is "long"])
		no_short_trade[choice] = len([i for i in temp if i is "short"])
		no_long_profit[choice] = len([i for i in range(0,len(temp)) if (temp[i] is "long")&(profit_list[i]>0)])
		no_short_profit[choice] = len([i for i in range(0,len(temp)) if (temp[i] is "short")&(profit_list[i]>0)])
		no_long_loss[choice] = no_long_trade[choice] - no_long_profit[choice] 
		no_short_loss[choice] = no_short_trade[choice] - no_short_profit[choice] 
		test_stats[choice] = sps.tmean(profit_list)*len(profit_list)/np.power(sps.tvar(profit_list), 0.5)
	end = time.time()
	duration = end-start
	print("The total time is {0} minutes".format(duration/60))
	allresult = np.c_[total_profit, no_profit_trade, no_loss_trade, no_long_trade, no_short_trade, no_long_profit, no_short_profit, no_long_loss, no_short_loss, test_stats]
	s = "\n".join([m_cp.header[j]+","+",".join(["{0}".format(i) for i in allresult[j]]) for j in range(0,K)])
	s = ",total_profit,no_profit_trade,no_loss_trade,no_long_trade, no_short_trade,no_long_profit, no_short_profit, no_long_loss, no_short_loss, test_stats\n"+s
	f = open(filename, "w")
	f.write(s)
	f.close()
