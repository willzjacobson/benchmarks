from rpy2 import robjects
from rpy2.robjects.packages import importr

gptk = importr("gptk")


agp = robjects.r("load('gp.gpr')")
