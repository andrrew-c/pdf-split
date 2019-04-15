import os, sys
import csv
import pandas as pd
import pdb
from datetime import datetime

## Control file
fname = 'program_control.csv'

## Duplicates file
dupfile = 'duplicates.csv'

#f = open(fname, 'rt')


##params = []
##for row in control:
##    params.append(row)
#    print(row)

def CheckEnvironment():
    if sys.platform[:3] == 'win':
        print("Program not set to run on windows yet - please speak to Andrew Craik")
        return False


def SplitDocs(control, dupfile):

    """ This will split pages when given 'input, start, end, output, newfolder, foldername'
        Date: 2019-03-02
    """
    if sys.platform[:3] == 'win':
        print("Program not set to run on windows yet - please speak to Andrew Craik")
        return False

    
    dups = open(dupfile, 'at')
    
    ## For each input document
    for i in range(len(control.inputdoc)):#range(1)
        #pdb.set_trace()

        ## Get folder and path names
        if control.newfolder[i] == 'yes':

            pdb.set_trace()
            #if control.foldername
            foldername = control.foldername[i]
            folderpath = os.path.join(".", foldername)
        else:
            folderpath = os.curdir
        
        ## Does folder exist?
        if not os.path.exists(folderpath):
            os.mkdir(folderpath)

        ## If document exists - not sure what to do
        outfile = os.path.join(folderpath, control.name[i])
        if os.path.exists("{}.pdf".format(outfile)):
            dealWithDups(i, control, dups)
            continue
        
        ## Derive command
        cmd = "pdftk {0}.pdf cat {1}-{2} output {4}/{3}.pdf".format(control.inputdoc[i], control.pagestart[i], control.pageend[i], control.name[i], folderpath)
        
        print(cmd)
        os.system(cmd)

    # Close dup file
    dups.close()

def CheckForDupNames(control):
    """ Check that there is a 1-1 mapping for inputdoc->output name"""
    pass

def dealWithDups(i, control, dups):
    pass

    ## Get date/time
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time= now.strftime("%H:%M:%S")
    
    print("File '{}' already exists.".format(control.name[i]))
    dups.write("{},{},".format(date, time))
    control.iloc[:1,:].to_csv(dups, index=False, header=False)
    
    #dups.write(",{},{}".format(datetime.now().strftime("%Y-%m-%d"),datetime.now().strftime("%H-%m-%S")))
    #continue
                            
def reduceSize(fileIn, fileOut):
    """ 
        Purpose: Reduce size of PDF without losing quality
        
        Notes: 
            This progam uses ghostscript to reduce the size of the PDF.
            The aim is not to lose too much of the quality.
            
            Source code:
                
            fileIn: Name/path of file to read in
            fileOut: Name/path of file to read out
            gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/default \
                -dNOPAUSE -dQUIET -dBATCH -dDetectDuplicateImages \
                    -dCompressFonts=true -r150 -sOutputFile=output.pdf input.pdf
                
        Author: Andrew Craik
        Date: 2019-03-18
    """
    
    ## Create command to run on system
    cmd = "gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/default \
            -dNOPAUSE -dQUIET -dBATCH -dDetectDuplicateImages \
            -dCompressFonts=true -r300 -sOutputFile={} {}".format(fileOut, fileIn)
    
    
    ## Check input file exists
    if not os.path.exists(fileIn):
        a = input("Input file '{}' does not exist.  Program will stop.\nPress Enter... ".format(fileIn))
        return False
    if os.path.exists(fileOut):
        print("File '{}' already exists.  Process will stop.".format(fileout))
    else:
        print("File '{}' does not already exist".format(fileOut))
        print("This function will attempt to convert the PDF called {} to become {}.".format(os.path.abspath(fileIn), os.path.abspath(fileOut)))
        print("\nCommand will be {}".format(cmd))

        ## Check user wants to continue
        check = input("Do you want to continue? Y/N ")
        if check.upper() == "Y":
            os.system(cmd)
        
        ## User said no
        elif check.upper() == "N":
            print("User cancelled")
            return False
        
        ## User pressed another option - stop
        else:
            a = input("Choose Y or N.  Function terminating")
            return False

#testFileIn = os.path.join('/..', '..', 'pdf-split-test', '2016-03-16-mortgage-first-key-facts.pdf')
#testFileOut = os.path.join('..', '..', 'pdf-split-test', '2016-03-16-mortgage-first-key-facts_reduce1.pdf')
   
sdirect = os.path.abspath("/home/andrewc/scanning")         
ffront= os.path.join(sdirect, 'contract-20190320-front.pdf')
ffrev = os.path.join(sdirect, 'contract-20190320-reverse.pdf') 
if __name__ == "__main__":
    pass

    ## Check environment running in
    if CheckEnvironment():
        
        #with open(fname, 'rt') as f:
        control = pd.read_csv(fname)

        print("\n"*2)
        #SplitDocs(control, dupfile)
        
        reduceSize(ffront,  'contract-20190320-front-compressed.pdf')
        reduceSize(ffrev,  'contract-20190320-reverse-compressed.pdf')
        


