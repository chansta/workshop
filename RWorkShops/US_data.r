setwd("C:\\Users\\16715044\\Documents\\PhD Thesis\\Database\\WRDS")
m <- read.csv("Execucomp.csv")
layout(matrix(seq(1,20),5,4))
frac_salary <- m[["SALARY"]]/m[["TDC1"]]
#Value of negative salary
neg_salary <- m[["SALARY"]][m[["SALARY"]]<0]
#Ticker for negative salary
neg_ticker <- m[["TICKER"]][m[["SALARY"]]<0]
#Year for negative salary
neg_year <- m[["YEAR"]][m[["SALARY"]]<0]
for (i in unique(m[["YEAR"]])[1:20]) { 
  temp <- frac_salary[m[["YEAR"]]==i]
  hist(temp,50, xlab=i, main="Salary Fraction")
  print(summary(temp))
}