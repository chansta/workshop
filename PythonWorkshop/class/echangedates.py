###################################################################
"""
A quicker routine to fix a date format problem. 
Source file is dates.csv
Output file is newdates.csv
"""
###################################################################

f = open("dates.csv")  #open connection to the file "dates.csv"
allset = []    #initiate an empty set to store the content of dates.csv
for i,ei in enumerate(f):
	e = ei.rstrip()
	sline = e.split("/")  #split the element by the separator "/"
	if i is 0:
		lastd = sline[0]      #Set the initial month and day 
		lastm = sline[1]
		lasty = sline[2]
		allset.append(e)
	else:
		if sline[0] == lastd:     #If the format is wrong then the first entry will be month which will equal to the previous first entry.
			pline = allset[i-1]
			psline = pline.split("/")
			psline[0] = lastm
			psline[1] = lastd
			allset[i-1] = "/".join(psline)
			lastm = sline[0]
			lastd = sline[1]
			sline[0] = lastd
			sline[1] = lastm
			allset.append( "/".join(sline))
		else:
			lastm = sline[1]
			lastd = sline[0]
			allset.append(e)
s = "\n".join(allset)
f = open("newdates.csv", "w")
f.write(s)
f.close()
