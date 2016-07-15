library(plm)

get_princomp <- function(year, dm, cutoff, option) { 
     #getting a sequence of principle components based on different year. 
     temp <- dm[(dm$year==year)&(abs(dm$r)<cutoff),]
     if (option=="new"){
          temp_pc <- princomp(~salary+bonus+option_awards+stock_awards, data=temp)
     } else { 
          if (option == "old") {
          temp_pc <- princomp(~salary+bonus+option_awards_blk_value+rstkgrnt, data=temp)
          } else {
               temp_pc <- princomp(~salary+bonus+option_awards_fv+stock_awards_fv, data=temp)
          }
     }
     summary(temp_pc)
}

print_result <- function(a) {
     print(a)
     print(a$loadings)
}

setwd("~/research/nargess")
m <- read.csv("CEOCOMP_COMPUSTAT_RETURN_VER4.csv")

dm <- m[(!is.na(m$stock_awards))&(!is.na(m$option_awards)),]
yearspan <- seq(2006,2013)
z <- lapply(yearspan, get_princomp,dm,1,"new")
lapply(z, print_result)

dm1 <- m[(!is.na(m$option_awards_blk_value)&(!is.na(m$rstkgrnt))),]
yearspan1 <- seq(1993,2005)
z.option1 <- lapply(yearspan1, get_princomp,dm1,1, "old")
lapply(z.option1, print_result)

dm2 <- m[(!is.na(m$option_awards_fv)&(!is.na(m$stock_awards_fv))),]
z.option2 <- lapply(yearspan, get_princomp,dm2,1, "sp")
lapply(z.option2, print_result)

dm.plm <- plm.data(dm, c("gvkey1", "year"))
dm01.plm <- dm.plm[abs(dm.plm$r)<1,]
dm.plm.result <- plm(r~1+lag(option_awards)+lag(stock_awards), data=dm01.plm, effect="individual")
summary(dm.plm.result)

dm1 <- cbind(dm1, dm1$r^2)
colnames(dm1)[198] <- "r2"
dm1.plm <- plm.data(dm1, c("gvkey", "year"))
dm.plm.old.result <- plm(r2~1+option_awards_blk_value+rstkgrnt, data=dm1.plm, effect="individual")
summary(dm.plm.old.result)

dm2 <- cbind(dm2, dm2$r^2)
colnames(dm2)[198] <- "r2"
dm2.plm <- plm.data(dm2, c("gvkey", "year"))
dm.plm.sp.result <- plm(r2~1+option_awards_fv+stock_awards_fv, data=dm2.plm, effect="individual")
summary(dm.plm.sp.result)