#Basic02.r - Soem examples on defining functions in R! 

moment <- function(x,order=1,centralised=TRUE) {
	T <- length(x)
	if (centralised==TRUE) {
		xtransform <- x-mean(x);
		m <- xtransform^order
	} else {
		m <- x^order; 
}
	mean(m);
}

kurtosis <- function(x) {
	kurt <- moment(x,order=4)/(moment(x, order=2)^2);
	kurt;
}
		 
