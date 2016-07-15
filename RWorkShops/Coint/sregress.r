ar_sim <- function(p, period, y0) { 
     y <- c(y0)
     e <- rnorm(period, mean=0, sd=p[3])
     for (t in 2:period) {
          y[t] <- p[1] + p[2]*y[t-1]+e[t]
     }
     list(data=y, resid=e)
}

p1 <- c(0.1,1,0.1)
p2 <- c(0.2,1,0.1)
period <- 1000
sim1 <- ar_sim(p1,period,0.5)
sim2 <- ar_sim(p2,period,0)
x1 <- sim1$data
x2 <- sim2$data
reg <- lm(x2~1+x1)
summary(reg)
e1 <- sim1$resid
e2 <- sim2$resid
cor(e1,e2)
cor(x1,x2)
plot(x1, type="l")
lines(seq(1,period),x2, col="red")
plot(x1,x2)
