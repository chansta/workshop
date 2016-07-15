###################################################################
"""
A quick routine to fix a date format problem. 
Source file is dates.csv
Output file is newdates.csv
"""
###################################################################

f = open("dates.csv")  #open connection to the file "dates.csv"
allset = []    #initiate an empty set to store the content of dates.csv
for i in f:   #loop through each line in f
	allset.append(i.rstrip()) #treat each line as a new element in the list allset
f.close()   #close the file connection 
for i,e in enumerate(allset):
	sline = e.split("/")  #split the element by the separator "/"
	if i is 0:
		lastd = sline[0]      #Set the initial month and day 
		lastm = sline[1]
		lasty = sline[2]
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
			allset[i] = "/".join(sline)
		else:
			lastm = sline[1]
			lastd = sline[0]
s = "\n".join(allset)
f = open("newdates.csv", "w")
f.write(s)
f.close()
