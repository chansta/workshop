m <- read.table("macrodata.csv", sep=",", skip=5, header=TRUE)
attach(m) 
layout(matrix(c(1,2),2,1))
acf(rUnemploy, main="ACF of rUnemploy Rates")
pacf(rUnemploy, main="PACF of rUnemploy Rates") 
rUnemploy.aic <- matrix(rep(0,49), 7, 7)
for (i in 0:6) {
	for (j in 0:6) {
		rUnemploy.aic[i+1,j+1] <- arima(rUnemploy, order=c(i,0,j))$aic
	}
}
detach(m)
