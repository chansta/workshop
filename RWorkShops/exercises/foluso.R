x <- c(5,4,3,2,1,23,4,3,4,11)
sx <- 0 
#using for loop with index as the iterator
for (i in 1:10) {
  sx <- sx + x[i]
}

#using for loop with the element in the list as iterator
sx <- 0
for (i in x) {
  sx <- sx + i
}

#transforming the data (log-difference) and save it into a new varibale "ld_"+variable name. 
for (i in n[2:5]) {
  assign(paste("ld", i, sep="_"), log(m[[i]][2:3394])/m[[i]][1:3393])
}

#variance 
#solution 1
v1 <- function(x) {
  n <- length(x)
  sx <- 0 
  for (i in x) {
    sx <- sx + i^2  
  }
  v <- sx/(n-1)
  return(v)
}

#solution 2
v2 <- function(x) {
  sx <- 0 
  x2 <- x^2
  for (i in x2) {
    sx = sx + i
  }
  v <- sx/(n-1)
  return(v)
}

#solution 3
s1 <- function(x) {
  sx <- 0
  for (i in x) {
    sx <- sx + i  
  }
  return(sx)  
}

v3 <- function(x) {
  n <- length(x)
  x2 <- x^2
  sx <- s1(x2)
  v <- sx/(n-1)
  return(v)
}