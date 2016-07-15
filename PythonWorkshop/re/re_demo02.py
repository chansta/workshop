import urllib as ul
import re as re

m = ul.URLopener()
tempfile = "temp.html"
m.retrieve("http://business.curtin.edu.au/schools-and-departments/economics-and-finance/our-people/", tempfile)
f = open(tempfile, "r") 
re_name = re.compile("profile/view/[A-Za-z]+\.[A-Za-z]+")
staffname = []
for i,line in enumerate(f):
    temp = re_name.findall(line)
    if len(temp) > 0:
        temp1 = temp[0].split('/')
        staffname.append(temp1[-1])
f.close()
firstname = [i.split(".")[0] for i in staffname]
surename = [i.split(".")[1] for i in staffname]
back = zip(firstname,surename)
