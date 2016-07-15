#################################################################################
"""
Name:                   An Introduction to Python
Author:                 Felix Chan
Email:                  fmfchan@gmail.com
Date Created:           2014.05.22
Updated:                2016.02.05 - added dictionary
Descriptions:           A demonstration file introducing some elemenatary characteristics of Python. 
                        Topics to cover:
                        Basic Input/Output
                        List 
                        List Comprehension
                        User defined function 
"""
#################################################################################

# The hash tag comment out the line. To comment out an entire block, use 

"""
    the three double quotation. Anything between the two sets of three double quotes will be treated as comments, or docstring. Python uses docstring as help file. This is handy because it means you do not have to write separate help file if you comment your codes well. 
"""

#Basic Input/Ouput:

print("Hello, welcome to Python and I don't bite. \n") #The \n indicate a new line (similar to pressing return). 
print("It would be great if we can be friends. \n") 
name = raw_input("Please tell me your name.\n") #Asking for input from keyboard and store answer into a variable name. Python is mostly dynamic typing but it is a little more complicated than that
#so we won't go into for now. 
print("It is nice to see you {0}. \n".format(name)) #The print function will replace {0} with the first argument in format. Similarly it will replace {1} in the string with the second argument in format.
# Everything in Python is an object and it starts counting from 0 (not 1). 
#This can be confusing if you are used to R but it conforms with most programming languages such as C. 

try:
    lastname = input("What's your last name? The answer needs to be in a string format.\n")
except:
    print("It would appear that you have forgotten the string quotes. \n")
    lastname = raw_input("Please try again. \n") 

"""
    The fundamental difference between input and raw_input is that Python takes input from raw_input() as string (without the quotes) but will treat input from input() as standard input to python.
    Warning: In Python 3, they remove the input() function in Python 2 and changed the name of raw_input() to input(). Ie input() in Python 3 is the same as raw_input in Python 2. In order to achieve something like input() in Python 2 in Python 3, we need to use eval(). Confuse yet? 
"""

print("So your full name is {0} {1}?\n".format(name, lastname))

#Fun with list

lname = list(name) #We can turn word into a list of letters
print(lname)
llastname = list(lastname) 
print(llastname)
#We can join two list
lfullname = lname + llastname
print(lfullname)

#Python works on the principle of pointers
temp = lfullname
a = temp.pop(1) #This is useful. pop is a method in the class list. It removes an element from the list and saves it to the variable a. 
print("The element being removed is {0}\n".format(a))
print("The remaining list is {0}.\n".format(temp))
print("BUT surprisingly, it also affects the original list. lfullname is now {0}.\n".format(lfullname))
#This is because the statement temp=lfullname does not create a new variable, but rather creating a link. Thus anything being operated on temp is the same as being operated on the source, ie lfullname.
#To create a new variable which contains the same value as an old variable. We can use copy() from the module copy
import copy as cp #import the module copy and assign it a name cp. Calling a method/function from the object can be done via cp.function(). The "as" part of the statement is not necessary. The object name will simply be copy if the "as" part is missing. 
temp = cp.copy(lfullname) # Calling the copy function from the object cp. 
a = temp.pop(2)
print("The element being removed is {0}.\n".format(a))
print("The new list is {0}.\n".format(temp))
print("But the old list didn't change which stays as {0}.\n".format(lfullname))

#Basic List Comprehension. 
#List comprehension is one of the most powerful feature in Python. It simplifies manipulation of list in an almost magical way.
#Example: I want to change all the elements lfullname to lowercase. 
#I can use a "for" loop:

newlist = [] #initiate a new list
for i in lfullname:             #beginning of a for loop
    newlist.append(i.lower())   #there is no beginning or end command in Python. It uses indentation to indicate if a block of codes should belong to the for loop. 

#Or you can use list comprehension:

newlistcomp = [i.lower() for i in lfullname] 

print("The list using loop is {0}. \n".format(newlist))
print("The list using list comprehension is {0}. \n".format(newlistcomp))

#set operation. list and set are similar but diferent objects. Superficially, list are just collection of elements where set is a colection of UNIQUE elements. 

set01 = set(list("Ranjodh"))
set02 = set(list("joyce"))

set03 = set01.union(set02)
set04 = set01.intersection(set02)
set05 = set01.difference(set02)
set06 = set02.difference(set01) #difference is not a symmetric operator. 

print("Set01 is {0}.\n".format(set01))
print("Set02 is {0}.\n".format(set02))
print("Set03 is {0}.\n".format(set03))
print("Set04 is {0}.\n".format(set04))
print("Set05 is {0}.\n".format(set05))
print("Set06 is {0}.\n".format(set06))

#string. Some useful string function. 

s = "Python is fun." #This is a string with white space between werds.
ls = s.split(" ") #separate s based on white space.
ss = "Python is fun.\n C is powerful." #string with a new line character \n. 
lss = ss.split("\n") #separate string based on new line character
print(s)
print(ls)
print(ss)
print(lss)

nss = "\n".join(lss) #join all elemens in the list lss by \n. 
print(nss)

#User Defined Function
#Essentially, list comprehension allows us to do something like sapply() in R. To fully appreciate that we need to learn about user defined function. 

#To define a function 
def convertUpper(a): #The command def tells Python you would like to create a function called covertUpper.
    """
    Description: It coverts an input string a to upper case.
    Input: 
        a: a string
    Ouput:
        upper case of a
    """
    if type(a) is str:
        return a.upper()
    else:
        print("{0} is not a string".format(a))

converttemp = [convertUpper(i) for i in lfullname]
print("The upperconversion of lfullname is {0}.\n".format(converttemp))

#Of course if you are more experienced, you don't really need to define the funciton. You can simply do the following:
converttemp_smart = [i.upper() for i in lfullname]
print("The upperconversion of lfullname is {0}.\n".format(converttemp_smart))

#Another important data structure in Python is dictionary. Basically a disctionary is a list with non-numeric index. An example:
record01 = {"Name": "Felix Chan", "Phone":92667760, "office": "402.612"}
print("The name is {0}".format(record01["Name"])) 

#Another way to initiate a dictionary is to use the dict function. It takes a list of tuples as input. 
record02 = dict([("Name", "Ranjodh Singh"), ("Phone", 92264409), ("office", "Unknown")]) 

#Dictionary can itself be an element in a dictionary. 

record = { "record01":record01, "record02":record02 }

#The keys method lists all the keys in the a dictionary
print(record.keys())
print(record["record01"].keys())
print(record["record01"]["Name"])




