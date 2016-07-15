simulate.ar1 <- function(p, period, y0) {
	e <- rnorm(period, 0, p[3])
	y <- c() 
	y[1] <- y0
	for (t in 2:period) {
		y[t] <- p[1] + p[2]*y[t-1] + e[t]
	}
	y
}

loglike.arma <- function(p, y) { 
	T <- length(y);
	fy <- y[2:T];
	ly <- y[1:(T-1)] 
	e <- fy-p[1]-p[2]*ly
	l <- 0.5*(log(2*pi)+log(p[3])+(e^2)/p[3]) 
	sum(l)
}

#With artifical data
p <- c(0.1,0.5,1)
T <- 1500
sy <- simulate.ar1(p, T, 0)
sy <- sy[501:T]
sloglikef <- optim(p,loglike.arma, y=sy, hessian=TRUE)
sarmaf <- arima(sy, order=c(1,0,0))


#With real data
m <- read.table("puzzle.csv", sep=",", header=TRUE)
p <- c(mean(m[[1]]),0.1,var(m)[1,1])
loglikef <- optim(p, loglike.arma, y=m[[1]], hessian=TRUE)
armaf <- arima(m[[1]], order=c(1,0,0))
