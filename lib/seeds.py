"""
PyPlant 1.0
LIBRARY: Seed File I/O

Copyright(c) 2010 Chris Ponticello
s4234549@student.uq.edu.au

DESCRIPTION:
Performs reading, writing and file validation for seed data files (.sdf).

LICENSE:
I, Chris Ponticello, hereby grant the rights to copy, redistribute, modify and
otherwise edit any source code file included within PyPlant 1.0, provided that
this license agreement and my ownership of the code is maintained and
acknowledged.

I also grant the right to non-commercial use of the source code without my
express permission. Commercial users must seek the permission of the author.
"""

import os.path

# -------------------------------------------------------------------------------------
"""
File Structure for the seed files
(n var - type):
/
0  PlantName       :   string
1  Color1 R        :   float (0<x<1)
2  Color1 G        :   float (0<x<1)
3  Color1 B        :   float (0<x<1)
4  Color2 R        :   float (0<x<1)
5  Color2 G        :   float (0<x<1)
6  Color2 B        :   float (0<x<1)
7  Color3 R        :   float (0<x<1)
8  Color3 G        :   float (0<x<1)
9  Color3 B        :   float (0<x<1)
10 GrowCycleYears  :   float (0<x<300)
11 MutatorFactor   :   float (0<x<0.75)
12 InitStemLength  :   float (0.5<x<50)
13 InitStemWidth   :   float (0.01<x<5)
14 InitStemAngle   :   float (5<x<75)
15 RoC%BranchLength:   float (-0.75<x<0)
16 RoC%BranchWidth :   float (-0.75<x<0)
17 RoC%BranchAngle :   float (-0.5<x<0)
18 MaxSteps        :   int   (2<x<15)
19 Divisions       :   int   (1<x<30)
20 DivisionIncrease:   int   (0<x<15)
/
"""

#list of tuples describing numeric data in the file: (is_int,minVal,maxVal)
dataTypes=[None,(False,0,1),(False,0,1),(False,0,1),(False,0,1),(False,0,1),
           (False,0,1),(False,0,1),(False,0,1),(False,0,1),
           (False,0,60*60*24*365*300),(False,0,0.75),(False,0.5,50),
           (False,0.01,5),(False,5,75),(False,-0.75,0),(False,-0.75,0),
           (False,-0.5,0),(True,2,15),(True,1,30),(True,0,15)]
    
# -------------------------------------------------------------------------------------


class seed:
    """A container class to hold seed data in a meaningful format.

    Constructor: seed(list<string>,string)
    Class invariant: filedata has been validated by seedFile_check(filedata)
    """
    def __init__(self,filedata,filename):
        """Fill the data structure with values from the file contents."""
        self._data = filedata
        self.name = filedata[0]
        self.color=[]
        for x in range(3):
            self.color.append((filedata[x+1],filedata[x+2],filedata[x+3]))
        #Growth Cycle Period
        self.cycleT = filedata[10]
        #Growth Mutation Factor
        self.mutator = filedata[11]
        #First stem - Length      
        self.iniLen = filedata[12]
        #First stem - Diameter 
        self.iniWidth = filedata[13]
        #First stem - branch's Splitting Angle 
        self.iniAngle = filedata[14]
        #% Decrease in Branch Length/iteration      
        self.rocLen = filedata[15]
        #% Decrease in Branch Diameter/iteration 
        self.rocWidth = filedata[16]
        #% Decrease in Branch Splitting Angle/iteration
        self.rocAngle = filedata[17]
        #Number of iterations (branch divisions)
        self.steps = filedata[18]
        #Number of Splits (new branches)/iteration        
        self.divs = filedata[19]
        #Number of Extra Splits (new branches)/iteration
        self.divInc = filedata[20]
        self.filename = filename

    def saveToFile(self):
        """Write seed file into the saves folder. Return wether successful.

        saveToFile() -> boolean"""
        #check folder exists
        if os.path.isdir("dat"):
            #write data to new lines
            f = open(self.filename,"w")
            for line in self._data:
                f.write(line+'\n')
            f.close()
            return True
        return False


def fileExists(fileName):
    """Check if the given seed file name exists

    fileExists(string) -> boolean"""
    return (os.path.exists(fileName) and os.path.isfile(fileName))


def seedFile_check(fileData):
    """Check seed file's contents against valid file length and data ranges.
    Checks are run indivudually, as each relies on the previous check to prevent
    the checking code drawing exceptions.

    seedFile_check(list<string>,list<tuple<boolean,float,float>>) -> boolean
    """
    #check file size
    
    if len(fileData)<>21:
        return False#'File Length'
    #iterate over numeric data
    for i in range(1,len(fileData)):
        #check blank data
        if fileData[i]=='':
            return False#'Blank'
        else:
            #check number type
            try:
                val=float(fileData[i])
            except:
                return False#'Not a number'
            #check data range
            if not dataTypes[i][1]<=val<=dataTypes[i][2]:
                return False#'Out of range'
            #check for integers
            if dataTypes[i][0] and val%1<>0:
                return False#'Not an integer'
    return True


def seedFile_load(fileName):
    """Check file exists and has valid content; return a seed data structure.

    seed_load(string) -> seed or False or None
    """
    fname="dat"+chr(92)+fileName+'.sdf'
    if fileExists(fname):
        #read file
        data=open(fname,'U').read().split('\n')
        #check content
        if seedFile_check(data):
            #file data validated and returned
            return seed(data,fname)
        else:
            #file found, invalid data
            return False
    #no file
    return None


# ----------------------------------------------------------------------------
