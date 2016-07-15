#Code created for demonstration puposes only. 
#Create by: Felix Chan
#Created on: 2012.07.10
#Required data: edata.csv

# import data from file edata.csv
m <- read.table("edata.csv", sep=",", skip=4, header=TRUE);

#2 ways to calculate returns

T <- dim(m)[1]; #get the time series length. 

#Method 1 - manipulate dataframe m as a whole. This will give a new dataframe, rm, which share the same varaible names as m but containing the return data. 
rm <- 100*log(m[2:T,]/m[1:(T-1),]);

#Method 2 - do it variable by variable.  
namelist <- names(m);
j=1
for (i in m) {
	assign( paste("r",namelist[j], sep=""), 100*log(i[2:T]/i[1:(T-1)]));
	j=j+1;	
}

#plot a few graphs
attach(m); #put the variable names of the dataframe onto the workspace. 
plot(Apple, type="l"); #plot Apple as a line graph.
lines(MS, col="red"); #add MS in red.
lines(Intel, col="blue"); #add Intel in blue. 
detach(m)

#Get some basic statsitics
sm <- summary(m)
rsm <- summary(rm) 

#Run a simple regression
attach(rm)
Apple.reg <- lm(Apple~Intel+MS)
anova(Apple.reg)

