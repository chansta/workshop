import os as os
import shutil as shutil
import sys as sys
import re as re

src = "/Users/229922I/unit/203/lectures/" #source directory path
dest = "/Users/229922I/Dropbox/unit/DBAStats/" #destination directory path
srcfolder = ["0"+str(i) for i in range(8,10)] #generating a list of directory name in the source path
srcfolder.append("10") #adding to the list so that we have ["08", "09", "10"]
destfolder = ["0"+str(i) for i in range(3,6)] #generating the list of directory name in destination.
re_findgraph = re.compile("\\includegraphics") #regular expression for finding the graphic files
for k,i in enumerate(srcfolder): #loop through all the potential directory
    temp_src = src+"lecture"+i #constructing the source directory name
    tempsub = os.listdir(temp_src) #list all the files under the directory
    srcfilelist = [j for j in tempsub if re.match("lecture"+i+"[^_]", j) is not None] #using regular expression to find the tex files for lecture notes
    destfilelist = [j.replace(i,destfolder[k]) for j in srcfilelist] #construct the list of new file names
    desti = "lecture"+destfolder[k] #construct the correspond directory name
    os.mkdir(dest+desti)
    [shutil.copyfile(temp_src+"/"+srcfilelist[m], dest+desti+"/"+destfilelist[m]) for m in range(0,len(srcfilelist))] #copy all the files from source to destination
    texfile = [tex for tex in srcfilelist if re.search("\.tex$", tex) is not None] #locate the tex source 
    if len(texfile)>0: 
        f = open(temp_src+"/"+texfile[0]) #open the tex source
        for ln,line in enumerate(f): #loop through the tex source
            tempg = re_findgraph.findall(line) #find the line with \includegraphics. 
            if len(tempg) > 0:
                gfilename = line.split("{")[1].split("}")[0] #extract the filename 
                shutil.copyfile(temp_src+"/"+gfilename, dest+desti+"/"+gfilename) #copy the graphical files to the destination
        f.close()



    

