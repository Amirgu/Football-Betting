

import mpmath
from Time_series import *



def gradcheck():
    
    """
    Testing the gradient formula of the log-density

    """

    sig=1.
    lam3=1.
    i,j=1,4
    eps=0.000000001
    for k in range(100):
        a,b,c,d=np.random.rand(),np.random.rand(),np.random.rand(),np.random.rand()

        lam1=mpmath.exp(sig+a-d)
        lam2=mpmath.exp(b-c)

        
        G=grad_log(i,j,lam1,lam2,lam3)
        

        ah,bh,ch,dh=a+eps,b+eps,c+eps,d+eps
        f=mpmath.log(density2(i,j,sig,a,b,c,d,lam3))
        
        g1,g2,g3,g4=density2(i,j,sig,ah,b,c,d,lam3),density2(i,j,sig,a,bh,c,d,lam3),density2(i,j,sig,a,b,ch,d,lam3),density2(i,j,sig,a,b,c,dh,lam3)
        f1,f2,f3,f4=mpmath.log(g1),mpmath.log(g2),mpmath.log(g3),mpmath.log(g4)

        G1,G2,G3,G4=((f1-f)/eps),((f2-f)/eps),((f3-f)/eps),((f4-f)/eps)

        
        Gn=np.array([G1,G2,G3,G4])

        if np.linalg.norm(G-Gn) > 1e-4:
            print(k)
            print(G,Gn)
            print(np.linalg.norm(G-Gn))
            print('Failed')
            break
    print('Success')