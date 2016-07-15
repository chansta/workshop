library(plm)
setwd("~/research/nargess")
m <- read.csv("EXECUCOMP_COMPUSTAT_MERGED.csv")

#defining some performance variables
roa <- m[["ebit"]]/m[["at"]]
roa_ni <- m$ni/m$at
roe <- m$ebit/m$uceq
roe_ni <- m$ni/m$uceq

#defining panel dataframe. 
pm <- plm.data(m, c("gvkey", "year"))
pm <- cbind(pm,roa,roa_ni, roe, roe_ni)
f <- total_alt1~1+roa+roe+emp+revt+mkvalt+age
plm.f <- plm(f, data=pm, model="within")
