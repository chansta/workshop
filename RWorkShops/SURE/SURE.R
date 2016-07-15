library(systemfit)
setwd("~/Dropbox/RWorkShops/SURE")
m <- read.table("mur.csv", sep=",", header=TRUE)
#Create the Variable PXa - Probability fo Execution and Conviction. PXa = PX*PC
PXa <- m$PX*m$PC
m <- cbind(m,PXa) #putting PXa into the dataframe

#Runing SURE
mf <- M~1+T+U+URB+W+X+XPOS+LF #defining the first equation
PXaf <- PXa~1+SOUTH+NW+XPOS #definiting the second equation
f <- list(mf, PXaf) #putting the equations into a list for systemfit
m.sure <- systemfit(f, method="SUR", data=m) #run the estiamtion 
summary(m.sure)

#Runing equation separately. 
mf.ls <- lm(mf, data=m)
PXaf.ls <- lm(PXaf, data=m)
summary(mf.ls)
summary(PXaf.ls)