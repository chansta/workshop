setwd("C:\\Users\\16715044\\Documents\\PhD Thesis\\Database\\R_data")
m<-read.csv("STRATEGY_VARIABLES_VER7.csv")
identify_listing <- function(asxc, no, m) {
  mm <- m
  old <- paste(asxc,as.character(no),sep="")
  temp <- m[m$asx_code==old,]
  ind <- FALSE
  current_year <- 2013
  while ((ind==FALSE)&(current_year != 1999)) {
    if (sum(is.na(temp[temp$year==as.character(current_year),c(4:8,10,12,15:20)])) < 13) {
      ind <- TRUE
      terminate <- current_year
    } else {
      current_year <- current_year - 1
    }     
  }
  delete_old <- seq(current_year+1,2013)
  delete_new <- seq(1999,current_year)
  delete_index <- ((m$asx_code==asxc)&(is.element(m$year,delete_new)))|((m$asx_code==old)&(is.element(m$year,delete_old)))
  mm <- m[!delete_index,]
  mm
}
m1 <- m
ln <- unique(m$asx_code)
for (j in 1:2) {
  selected <- ln[grep(paste(j,"$",sep=""), ln)]
  selected <- gsub(paste(j,"$",sep=""),"",selected)
  for (i in selected) {
    m1 <- identify_listing(i,j,m1)
  }
}

output <- 'C:\\R_Excel\\strategy.csv'
write.csv(m1, output)
