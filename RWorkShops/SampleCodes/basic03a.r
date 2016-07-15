source("basic03.r") # import the function from the file basic03.r
z <- simulate.arma(theta=c(0.4), order=c(0,1), period=500); #simulate an MA(1) process
layout(matrix(c(1,2),2,1))
acf(z, main="Autocorrelation for z")
pacf(z, main="Partial Autocorrelation for z") 

