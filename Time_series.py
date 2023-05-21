import mpmath
import numpy as np



np.seterr(over='raise')

def density(x, y, lam1, lam2, lam3):
    """ 
    Density of the Bivariate Poisson distribution

    x,y= Values or Goals of the Home/Away
    lam1,lam2,lam3= parametres of the distribution

    """
    s = lam1 + lam2 + lam3
    ifac = mpmath.factorial(x)
    jfac = mpmath.factorial(y)
    
    log_pow1 = x * mpmath.log(lam1) - mpmath.log(ifac)
    log_pow2 = y * mpmath.log(lam2) - mpmath.log(jfac)
    t = 0
    
    for k in range(min(x, y) + 1):
        denom = lam1 * lam2
        if denom == 0 or np.abs(denom) < 1e-12:
            denom = 1e-12  # Set small positive value for denominator
        t += mpmath.binomial(x, k) * mpmath.binomial(y, k) * mpmath.factorial(k) * mpmath.exp(k * (mpmath.log(lam3) - mpmath.log(denom)))
        
    return mpmath.exp(-np.float128(s) + log_pow1 + log_pow2) * np.float128(t)


def U(i,j,lam1,lam2,lam3,q):
    """
    Used for Log gradient

    """
    t=0
    for k in range(min(i,j)+1):
        denom=lam1*lam2
        if denom < 1e-10 or denom == 0:
            denom=1e-10
            
        t+=mpmath.binomial(i,k)*mpmath.binomial(j,k)*mpmath.factorial(k)*( ( lam3 / (denom) ) **k) * (k**q)
    return t


def S(i,j,lam1,lam2,lam3):
    """
    Used for Log gradient

    """
    return U(i,j,lam1,lam2,lam3,1)/U(i,j,lam1,lam2,lam3,0)


def grad_log(x,y,lam1,lam2,lam3):
    """
    Gradient of the log-density for updating one single game, see (.Koopman 2016)

    """
    g=S(x,y,lam1,lam2,lam3)

    a=x-lam1-g
    b=y-lam2-g
    c=lam2-y+g
    d=lam1-x+g

    return np.array([a,b,c,d])

def density2(i,j,sig,alpha_i,alpha_j,beta_i,beta_j,lam3):
    """
    Density for one game 

    i,j= Index of teams
    sig= Parameter of impact of home games
    alpha_i,alpha_j = Home,Away Attacking strength Parameters Respectively
    beta_i,beta_j = Home,Away Defending strength Parameters Respectively

    """
    lam1=mpmath.exp(sig+alpha_i-beta_j)
    lam2=mpmath.exp(alpha_j-beta_i)
    return density(i,j,lam1,lam2,lam3)

def Mat_M(i,j):

    M=np.zeros((4,40))
    M[0][i],M[1][j],M[2][i],M[3][j]=1,1,1,1
    return M

def Mat_A(a1,a2):
    N=20
    Z = np.zeros((N,N))
    I1,I2=np.eye(N)*a1,np.eye(N)*a2 
    out = np.asarray(np.bmat([[I1, Z], [Z, I2]]))
    return out

def update_score(i,j,x,y,f,phi,omega):

    """
    Updating parameter of the Parameter of game opposing home team i and away team j

    i,j: Index of Home/away teams
    x,y : Goals scored by Home/Away Teams
    f: Current Parameters of all teams in the shape (alpha0,.........., alpha19,beta0,.......,beta19)
    omega: Decay Parameter

    """
    ## phi=[a1,a2,b1,b2,lam3,homeadvantage]
    #### f= (alpha0,.........., alpha19,beta0,.......,beta19)
    M=Mat_M(i,j)
    sigma=phi[4]
    alpha_i=f[i]
    alpha_j=f[j]
    beta_i=f[i+20]
    beta_j=f[j+20]
    lam3=phi[5]
    f_ij=np.array([alpha_i,alpha_j,beta_i,beta_j])
    a1,a2,b1,b2=phi[:4]
    

    A_ij=np.eye(4)
    B_ij=np.eye(4)
    A_ij[0,0],A_ij[1,1],A_ij[2,2],A_ij[3,3]=a1,a1,a2,a2
    B_ij[0,0],B_ij[1,1],B_ij[2,2],B_ij[3,3]=b1,b1,b2,b2
    
    lam1_ij=mpmath.exp(sigma+alpha_i-beta_j)
    lam2_ij=mpmath.exp(alpha_j-beta_i)
    
    f_ij_up = omega + (B_ij @ f_ij) + (A_ij @ grad_log(x,y,lam1_ij,lam2_ij,lam3))
    
    return f_ij_up