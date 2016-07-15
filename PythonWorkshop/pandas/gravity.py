import pandas as pd
import numpy as np

m = pd.read_csv("project02_pdata_nokorea.csv", header=0, index_col=[24,25]) #import data using year and import_export id as indexes. 
m = m.sort_index() #sort index (important for slicing purpoeses). 

sm = pd.read_csv("project02_pdata_nokorea.csv", header=0, index_col=[24,26,27]) #import data again but using time, import and export indexes (3-dimensional index). 
sm = sm.sort_index()


