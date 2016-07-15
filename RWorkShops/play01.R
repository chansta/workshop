m<- read.csv("REMUNERATION_VER10.csv")
plm.m <- plm.data(m,c("asx_code", "year"))
frac_base_salary <- plm.m[["base_salary"]]/plm.m[["total_compensation_including_lon"]]
layout(matrix(seq(1,12),4,3))
yearlist <- seq(2003,2012)
tempmean <- c()
i <- 1
for (y in yearlist) {
  temp <- plm.m[["frac_superannuation"]][(plm.m[["year"]]==y)]
  hist(temp,50,xlab=y, main="Superannuation")
  print(summary(temp))
  tempmean[i] <- summary(temp)[["Mean"]]
  i <- i+1
}
plot(te)

