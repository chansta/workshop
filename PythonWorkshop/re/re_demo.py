#############################################################################
"""
Name:               re_demo.py
Author:             Felix Chan
Email:              fmfchan@gmail.com
Date Created:       2016.02.05
Description:        Demo on regular expression with Pandas
"""
#############################################################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re as re

m = pd.read_csv("../class/datastream_equities_201405.csv", header=0, index_col=0)
T = m.count()[0]
re105 = re.compile("^1/05/[0-9]{4}")
date = m.index
dlist = [i for i in range(0,T) if re105.search(date[i]) is not None]
sm = m.iloc[dlist,:]

