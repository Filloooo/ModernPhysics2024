
""" function to be fitted, annoyingly scipy.curvefit requires a explicit list of parameters as input, (x, p0, p1 , p2),
whereas scipy.odr requires input in the form of a vector, (P, x) with P = [p0, p1, p2] """

def pol1(x, p0, p1):
    return p0 + p1*x


def Gauss(x, p0, p1, p2):
    return p0*np.exp( -(x-p1)**2/(2*p2**2) )


def pol1_Gauss(x, p0, p1, p2, p3, p4):
    return p0*np.exp( -(x-p1)**2/(2*p2**2) ) + p3 + p4*x 
