
import numpy as np

def BivariatePoisson(lam1,lam2,lam3):
    a=np.random.poisson(lam1)
    b=np.random.poisson(lam2)
    c=np.random.poisson(lam3)
    X=a+c
    Y=b+c
    return X,Y