stateGP <- function(Xloc, yloc, floor){
  # xloc and yloc contain relative paths from the
  #finite_horizon_control folder
  library('gptk')
  print(Xloc)
  print(yloc)
  X = read.csv(file=Xloc)
  X = as.matrix(X)
  y = read.csv(file=yloc)
  y = as.matrix(y)
  print("matrices read from file")
  opt = gpOptions()
  opt$kern$comp = list('rbf', 'white')

  
  myGP = gpCreate(q=dim(X)[2], d=1,X=X,y=y,options=opt)
  print("GP initialized")
  optVarName= paste('myGP_opt', as.character(floor), sep = "")
  print(paste("GP Name is: ", optVarName))
  assign(optVarName, gpOptimise(model=myGP))
  print("GP optimization complete")
  gp = get(optVarName)
  save(gp, file=paste('state/gps/gp', as.character(floor), ".gpr", sep=''))
  return(gp)
}


