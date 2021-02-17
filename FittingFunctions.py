from scipy.optimize import curve_fit
import numpy as np
from scipy.stats.distributions import chi2 ## p value calculator, given chi^2 and ndf as input

""" function to be fitted, annoyingly scipy.curvefit requires a explicit list of parameters as input, (x, p0, p1 , p2),
whereas scipy.odr requires input in the form of a vector, (P, x) with P = [p0, p1, p2] """

def pol1(x, p0, p1):
    return p0 + p1*x


def Gauss(x, p0, p1, p2):
    return p0*np.exp( -(x-p1)**2/(2*p2**2) )


def pol1_Gauss(x, p0, p1, p2, p3, p4):
    return p0*np.exp( -(x-p1)**2/(2*p2**2) ) + p3 + p4*x 
"""fits data with pol2, makes a nice plot, and returns the following:
value list of fit paramaters
their covariance matrix
a list of the GoF quantities [chi^2, ndf, p_val]"""

def curveFit(myPlot, x, y, Er_y=None, legName="", Fit=None, fitRange=None, parEst=None, parBounds=None, returnGOF=False): 
    """ Fit is the name of the used defined function to call
        parESt is a 1D list of initial estimates for the fit parameters
        parbounds is 2D array containing limits/bounds on the fit parameters [[p0_min, p1_min], [p0_max, p1_max]]"""

    if fitRange is not None: ## if you didnt supply a specific fit range, the entire range will be used.
        y_fit = y[(fitRange[0]<x) & (x<fitRange[1]) ] # have to create a set of new array's only containing data within the fit range
        x_fit = x[(fitRange[0]<x) & (x<fitRange[1]) ]
        if Er_y is not None: ## if we have supplied an array of y errors cut out the desired range
            Er_y_fit = Er_y[(fitRange[0]<x) & (x<fitRange[1]) ]
        else:
            Er_y_fit = np.zeros(len(y_fit))
    else:
        fitRange = [min(x), max(x)]
        x_fit, y_fit = x, y
        Er_y_fit = np.zeros(len(y_fit)) ## create a list of zeroes to be used in the chi^2 calculation, will cause divide by 0 warning

    if   Er_y is None and parBounds is None: ## the 4 different fitting options, depending on if Y errors and/or parameter bounds are given
        fitPars, pCov = curve_fit(Fit, x_fit, y_fit, p0=parEst) ### THIS is the fit
    elif Er_y is None and parBounds is not None:
        fitPars, pCov = curve_fit(Fit, x_fit, y_fit, p0=parEst, bounds=parBounds) ### THIS is the fit
    elif Er_y is not None and parBounds is None:
        fitPars, pCov = curve_fit(Fit, x_fit, y_fit, sigma=Er_y_fit, absolute_sigma=True, p0=parEst) ### THIS is the fit
    else:
        fitPars, pCov = curve_fit(Fit, x_fit, y_fit, sigma=Er_y_fit, absolute_sigma=True, p0=parEst, bounds=parBounds) ### THIS is the fit

    ## manually calculating chi^2 and P_val
    Yexp = Fit(x_fit, *fitPars) ##expected value from fit'
    chisq = np.sum(( (y_fit - Yexp)/Er_y_fit)**2)
    ndf = len(x) - 2  ## number degrees of freedom
    p_val = chi2.sf(chisq, ndf)
    GoFs = [chisq, ndf, p_val]

    ## creates nice legend containing values of GoF, fit parameters and their errors, play around with the string formatting so 
    ## the number of significant digits shown looks nice, eg not too many and not too few - lagom!
    varnames = [] ## names of the fit paramters to be displayed in the legend
    for i in range(len(fitPars)): ## 
        varnames.append( r"$p_{}$".format(i) ) # creating a list of parameter names p_i

    # legtext = ""
    legtext = r"$\bf{%s:}$"%(legName) # string var used to created the legend of the plot
    legtext += "\n"
    # First adding the Goodness of Fit values to the legend
    legtext += r"$\chi^2 \ / \ ndf$ = " +"{:.2f}/{}\n".format(chisq, ndf) 
    if p_val > 0.01:
        legtext += "Prob = {:.2f}\n".format(p_val)
    else:
        legtext += "Prob = {:.2e}\n".format(p_val)

    # now adding the fit parameters and their uncertainty, consider doing a custom IF block, to display values with or without scientific notation, etc. 
    for i in range(len(fitPars)):
        legtext += "%s = %1.3f, +/- %1.2f\n"%(varnames[i], fitPars[i],pCov[i,i]**0.5) ##Error on fit par is found along diagonal of the covariance matrix



    if len(x) < 420:
        xpoints = np.linspace(fitRange[0], fitRange[1], 420) ## points to plot fit line over, 420 is arb number for smoothly plotted line
    else:
        xpoints = np.linspace(fitRange[0], fitRange[1], len(x)) ## points to plot fit line over

    myPlot.plot(xpoints, Fit(xpoints, *fitPars), '-', label=legtext, linewidth=4) ## makes fitted line plot

  
    myPlot.legend(fontsize=13)

    myPlot.set_xlim(min(x)*0.99, max(x)*1.01) ## setting the range of the x axis
    myPlot.set_ylim(min(y)*0.99, max(y)*1.05) ## setting the range of the y axis

    # plt.show()
    if returnGOF:
        return fitPars, pCov, GoFs 
    else:
        return fitPars, pCov
