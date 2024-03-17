import os 
import numpy as np
def get_data( filename,filetype, ignoreLines=0): # I separate filename and filetype, so you can reuse filename list for eg writing legends, without .txt appearing  
    XX = []
    YY = []
    n = 0.
    getBinsNext = False
    Nbins = 0
    filepath = os.path.join(os.getcwd(), "data2", filename + filetype)
    startN = 9999999 
    """# Allows data to be put in separate subfolder from the script,
    # os.getcwd makes it works across different operating systems"""
    with open(filepath, "r") as file: #open the file in read mode
        for ievent, line in enumerate(file):  # Loop over lines in file
            line = line.strip()  # This removes all "codes" that may be put into the file like linebreaks \n.
            line = line.split() # splits the line, by default using spaces as separator 
            if ievent < ignoreLines: ## to ignore the header lines of the data files
                continue
            else:
                # if ievent < 170:
                # print(ievent, line)

                if getBinsNext: ## this is the line to extract Nbins, which is used to stop collecting data when end of file strings comes along
                    Nbins = int(line[1])
                    getBinsNext = False
                    # print("Got Nbins = ",Nbins)

                elif line[0] == "$DATA:": ## next line contains Nbins
                    getBinsNext = True
                    startN = ievent +2

                elif len(line) != 0 and ievent >= startN: # to avoid errors from trying to convert nothing/stuff after data into a float
                    if ievent <= Nbins +ignoreLines +2: ## we start proccessing line[] at "$DATA:", 2 lines before data listing starts
                        XX.append(n)
                        YY.append(float(line[0]))
                        n += 1

    return np.array(XX), np.array(YY)
