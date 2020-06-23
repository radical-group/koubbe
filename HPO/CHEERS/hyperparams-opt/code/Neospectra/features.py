import numpy as np
import scipy
from scipy import newaxis as nA

def mlr(x,y,order):
    """Multiple linear regression fit of the columns of matrix x
    (dependent variables) to constituent vector y (independent variables)

    order -     order of a smoothing polynomial, which can be included
                in the set of independent variables. If order is
                not specified, no background will be included.
    b -         fit coeffs
    f -         fit result (m x 1 column vector)
    r -         residual   (m x 1 column vector)
    """
    if order > 0:
        s=np.ones((len(y),1))
        for j in range(order):
            s=np.concatenate((s,(np.arange(0,1+(1.0/(len(y)-1)),1.0/(len(y)-1))**j)[:,nA]),1)
        X=np.concatenate((x, s),1)
    else:
        X = x
    a = np.dot(np.transpose(X),X)
    a = np.linalg.pinv(a)
    b = np.dot(np.dot(a,scipy.transpose(X)),y)
    f = np.dot(X,b)
    r = y - f

    return b,f,r

def emsc(myarray, order, fit=None):
    """Extended multiplicative scatter correction (Ref H. Martens)
    myarray -   spectral data for background correction
    order -     order of polynomial
    fit -       if None then use average spectrum, otherwise provide a spectrum
                as a column vector to which all others fitted
    corr -      EMSC corrected data
    mx -        fitting spectrum
    """
    #choose fitting vector
    if fit:
        mx = fit
    else:
        mx = np.mean(myarray,axis=0)[:,nA]

    #do fitting
    corr = np.zeros(myarray.shape)
    for i in range(len(myarray)):
        b,f,r = mlr(mx, myarray[i,:][:,nA], order)
        corr[i,:] = np.reshape((r/b[0,0]) + mx, (corr.shape[1],))

    return corr

def getGradients(data, order=1):
    gradData = np.gradient(data, order)[0]
    return gradData
