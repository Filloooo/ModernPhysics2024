from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)


def PPlot(fig, x, y, Er_y=None, x_label="", y_label="", legName="", setLogY=False): #setting a default value of the input noFIt to False
    
    myPlot = fig.add_subplot()
    ## first we do a the basic plot
    if  Er_y is None: 
        myPlot.plot(x, y, linestyle=None, label=legName) ##makes plot without errorbars

    elif Er_y is not None: ## errorsbars on Y but not on X
        myPlot.errorbar(x, y, yerr=Er_y, fmt="o", label=legName, markersize=1, capsize=2., markerfacecolor="black", markeredgecolor="black") ##makes errorbar point plot

    myPlot.set_xlabel(x_label, fontsize=16)
    myPlot.set_ylabel(y_label, fontsize=16, labelpad = 10)
    myPlot.grid(True)
    
    if setLogY:
        myPlot.set_yscale('log') #### Logarithmic

    myPlot.legend(fontsize=13)
    myPlot.xaxis.set_major_locator(MultipleLocator(100))
    myPlot.xaxis.set_minor_locator(AutoMinorLocator(2))
    
    return myPlot
