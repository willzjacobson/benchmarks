costGP <- function(Xloc, yloc){
  # xloc and yloc contain relative paths from the
  #finite_horizon_control folder
  library('gptk')
  print(Xloc)
  print(yloc)
  X = read.csv(file=Xloc)
  X = as.matrix(X)
  y = read.csv(file=yloc)
  y = as.matrix(y)
  opt = gpOptions()
  opt$kern$comp = list('rbf', 'white')
  
  myGP = gpCreate(q=dim(X)[2], d=1,X=X,y=y,options=opt)
  myGP_opt =gpOptimise(model=myGP)
  save(myGP_opt, file='cost/gps/gp.gpr')
  return(myGP_opt)
}

