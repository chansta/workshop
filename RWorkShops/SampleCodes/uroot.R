for (i in names(m)) {
	assign(paste("df", i, sep="."), ur.df(m[[i]], type= "drift", lags= 4));
}