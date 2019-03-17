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

#with open(fname, 'rt') as f:
control = pd.read_csv(fname)


##params = []
##for row in control:
##    params.append(row)
#    print(row)

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
                            

if __name__ == "__main__":
    SplitDocs(control, dupfile)


