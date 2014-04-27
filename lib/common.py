
"""
PyPlant 1.0
LIBRARY: Common Resources

Copyright(c) 2010 Chris Ponticello
s4234549@student.uq.edu.au

DESCRIPTION:
Miscellaneous, stand-alone functions performing calculations/checks either
common to both applications, or falling outside other modules.

LICENSE:
I, Chris Ponticello, hereby grant the rights to copy, redistribute, modify and
otherwise edit any source code file included within PyPlant 1.0, provided that
this license agreement and my ownership of the code is maintained and
acknowledged.

I also grant the right to non-commercial use of the source code without my
express permission. Commercial users must seek the permission of the author.
"""

from math import pi

# ------------------------------------------------------------------------------


def filterFileChars(filename):
    """Return a string after filtering out illegal characters.

    filteredFilename(string) -> string
    """
    illegal = [60, 62, 58, 34, 47, 92, 124, 63, 42] 
    outStr=''
    for c in filename:
        if not ord(c) in illegal:
            outStr+=c
    return outStr


def cylinderVol(radius,length):
    """Return the cylinder volume for the given dimensions.

    cylinderVol(float,float) -> float
    """
    return pi*radius**2*length


def timeUnits(timeVal,unitIn,unitOut):
    """Convert the time value between the given units.

    timeUnits(float,string,string) -> float
    preconditions:  unitIn and unitOut are in ['s', 'm', 'h', 'd', 'y']
    """
    unitValue = {'s' : 1,
                  'm' : 60,
                  'h' : 3600,
                  'd' : 86400,
                  'y' : 31557600}
    return timeVal * unitValue[unitIn] *1./unitValue[unitOut]


def progressCurve(progress):
    """Translate the decimal fraction ‘progress’ to a point on the
        quadratic curve, -(x^2)+2x

    progressCurve(float) -> float
    precondition: 0<=progress<=1
    """
    return -(progress**2) + 2*progress


def colorShade(colors,progress):
    """Takes a set of (R,G,B) colour values and decimal fraction ‘progress’.
    Imagine colours are evenly shaded along a line; return the colour value
    at the position indicated by ‘progress’.

    colorShade(list<color>,float) -> color
    preconditions:  0<=progress<=1
                    len(colors)>1
    """
    k = progress
    n = len(colors)-1
    fList=[]
    newCol=(0,0,0)
    
    #Define linear functions for color shading strength around each point
    for i in range(n+1):
        
        if i==0:
            #First point function: downward-sloping line
            fn = lambda x: max(0, 1 - n*x )
            
        elif i==n:
            #Last point function: upward-sloping line
            fn = lambda x: max(0, n*x - 1 )
            
        else:
            #Other points: slopes ending at the adjoining points
            fn = lambda x: max(0, 1 - n * abs(x - (i*1./n) ) )
                ##f(x)=y = 1 - m| x-(i/m) |
            
        fList.append(fn)    
    
    #Generate the combined color: loop over each color value
    for i in range(n+1):
        #Add the value*strength to the output RGB components
        newCol = ( newCol[0] + colors[i][0] * fList[i](k),
                   newCol[1] + colors[i][1] * fList[i](k),
                   newCol[2] + colors[i][2] * fList[i](k) ) 

    return newCol
    

# ----------------------------------------------------------------------------
