simulate.arma <- function(theta=c(0.5,0.1), order=c(1,1), period=100, initial.value=c(0,0)) {
	p <- order[1];
	q <- order[2];
	s <- max(p,q);
	e <- rnorm(period+s);
	y <- rep(0,period+s); 
	if (p!=0) {
		y[1:p] <- initial.value[1:p]; 
	} 
	if (q != 0 ) {
		e[1:q] <- initial.value[(p+1):(p+q)];
	}
 	for (t in (s+1):(period+s)) {
		if ((p!=0)&(q!=0)) {
		y[t] <- t(as.matrix(theta[1:p] ))%*%as.matrix(y[(t-p):(t-1)]) + t(as.matrix(theta[(p+1):(q+p)]))%*%as.matrix(e[(t-q):(t-1)]) + e[t]; } else { 
		if (p!=0) { 
			y[t] <- t(as.matrix(theta[1:p] ))%*%as.matrix(y[(t-p):(t-1)]) + e[t]
		} else {
			y[t] <-  t(as.matrix(theta[(1):(q)]))%*%as.matrix(e[(t-q):(t-1)]) + e[t]; 
		} 
		}
	}
	y; 
}
	 
	
