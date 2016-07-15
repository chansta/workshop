library("urca")
m <- read.table("macrodata.csv", sep=",", skip=5, header=TRUE)
m <- log(m)
attach(m)

#Engle and Granger Two-Step Approach
simple.reg <- lm(GDP~CPI+Unemploy+RBA+bank+bond+ASX+export+import)
co.test <- ur.df(simple.reg$residuals,type="trend", selectlags="BIC")

#Johansen Approach
rk.test <- ca.jo(m, type="trace", ecdet="const", K=4, spec="transitory")
m.vecm <- cajorls(rk.test, r=6)
#generate t-statistics
n <- dim(coef(m.vecm$rlm))
m.vecm.tstat <- coef(m.vecm$rlm)/matrix(sqrt(diag(vcov(m.vecm$rlm))), n[1], n[2])
