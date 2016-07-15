layout(matrix(c(1,3,2,3),2,2,byrow=TRUE))
plot(m[["Apple"]], type="l", xlab="Time", ylab="Price", main="Apple Stock Price")
plot(rm[["Apple"]], type="l", xlab="Time", ylab="Return", main="Apple Stock Returns")
hist(rm[["Apple"]], main="Histogram of Apple Returns", xlab="Apple Returns")

#note m[["Apple"]] is the same as m[,"Apple"]. Can you explain that? 
