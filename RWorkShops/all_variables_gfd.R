setwd("~/research/nargess/")
m <- read.csv("all_variables_gfp.csv", header=TRUE)
for (i in 1:27403) {m$id[i] <- paste(m$gvkey1[i], m$execid[i], sep=".")}
library(plm)
pm.ijt <- plm.data(m,indexes=c("id","fyear"))
f1 <- tobinq~stocks_adj+options_adj+salary_adj+bonus_adj+ceo_tenure+age
f2 <- roe~stocks_adj+options_adj+salary_adj+bonus_adj+ceo_tenure+age
explvar <- "stocks_adj+options_adj+salary_adj+bonus_adj+ltip_adj+ceo_tenure+age+firm_size+market_to_book"
for (m in c("tobinq", "roe", "TRS1YR", "roa")) {
  for (model in c("within")) {
    f <- paste(m,explvar, sep="~")  
    assign(paste("pm.ijt",m,model,"2ways",sep="."), plm(as.formula(f), data=pm.ijt, model=model,effect="twoways")) 
  }
}
  
