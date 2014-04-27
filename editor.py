"""
PyPlant 1.0
GUI: Seed File Editor

Copyright(c) 2010 Chris Ponticello
s4234549@student.uq.edu.au

DESCRIPTION:
A small GUI application used for creating and editing seed properties.
The 21 parameters are changed through command-line input, buttons and sliders.
Seed files can be created and edited for later use by the grower application.
2 windows/displays: 'Controls' and 'Data'

LICENSE:
I, Chris Ponticello, hereby grant the rights to copy, redistribute, modify and
otherwise edit any source code file included within PyPlant 1.0, provided that
this license agreement and my ownership of the code is maintained and
acknowledged.

I also grant the right to non-commercial use of the source code without my
express permission. Commercial users must seek the permission of the author.
"""

# Get Directories
import sys, os
sys.path.append(os.getcwd()+'\lib')#adds lib folder to import directories

# PyPlant Libraries
from visual import *
from visual.controls import *
from seeds import *
#from common import *

# Standard Libraries
from random import random


# -------------------------------------------------------------------------------------
#CONSTANTS & EXTERNAL FUNCTIONS
"""
Using the Controls window:
http://www.vpython.org/contents/docs/visual/controls.html
"""

#Constants
s=0.9

ctrlWinW=650
ctrlWinH=350
ctrlWinAspect=0.7857#0.7857#1.*ctrlWinW/ctrlWinH

dataWinW=650
dataWinH=350
dataWinAspect=dataWinW/dataWinH

sliderLen=125*s
sliderW=15*s
slider_txtbuf=22*s

labelW=145*s
labelH=20*s

vspacing=52

red=(1,0,0)
green=(0,1,0)
blue=(0,0,1)
ltgrey=(0.7,0.7,0.7)
white=(1,1,1)
sliderCol=(0.6,0.6,1)

def testReturn(x):
    pass

def cWinPos(x,y):
    """Convert regular screen-pixel coordinates to a control window position."""
    return (-ctrlWinW/2+75 + x*ctrlWinAspect, ctrlWinH/2 - y)

def dWinPos(x,y):
    """Convert regular screen-pixel coordinate to a display window position."""
    return (-dataWinW/2 + x*dataWinAspect, dataWinH/2 - y)

# ------------------------------------------------------------------------------
#WIDGET ABSTRACTION


class text(menu):
    """A simple wrapper for the menu class, to create a static label on Control
        windows.
    """
    def __init__(self,x,y,text,color=ltgrey):
        menu.__init__(self, pos=cWinPos(x,y), text=text, width=labelW,
                      height=labelH, color=color)    


class dragbar:
    """A widget combining a label, a slider and associated formatting.

    Constructor: dragbar(tuple<float,float,float>,string,float,float,float,function,
                         color)
    Class invariant: action_change takes a float as input
    """
    
    def _move(self):
        """Send slider value to be processed"""

        self._sendValue(self.sliderObj.value)

    def getValue(self):
        """Return the slider reading."""

        return self.sliderObj.value

    def setValue(self,val):
        """Change the slider position"""

        self.sliderObj.value=val
        self._move()
    
    def __init__(self, x, y, title, minval, maxval, action_change,
                 color=sliderCol):
        """Create GUI elements"""

        self._sendValue = action_change
        self._title=title
        self.x,self.y=cWinPos(x,y)

        #Create the components
        self._title=title
        self.sliderObj = slider(pos=( self.x-sliderLen/2+5, self.y ),
                                width = sliderW,
                                length = sliderLen,
                                axis = (1,0,0),
                                color = color,
                                min = minval, max = maxval,
                                action = self._move)
        if self._title<>'':
            self.titleLbl = text(x,y-slider_txtbuf,title)



class colorSlider:
    """A widget combining three dragbars, a title and color display.

    Constructor: colorSlider(float,float,function,color)
    Class invariant: action_change takes a color as input
    """

    def getColor(self):
        """Return the combined color from slider values"""

        return (self.s1.getValue(),self.s2.getValue(),self.s3.getValue())

    def update(self):
        """Fill the color box; pass the value to the change action"""

        val=self.getColor()
        self._updateColor(val)

    def sliderMove(self, sliderValue):
        """Slider change event"""

        self.update()

    def setColor(self,color):
        """Overwrite color represented by sliders"""

        self.s1.setValue(color[0])
        self.s2.setValue(color[1])
        self.s3.setValue(color[2])
        self.update()

    def __init__(self,x,y,action_change):
        """Initialise and update GUI elements"""
        
        self._updateColor=action_change

        #Create the components
        self.s1=dragbar(x,y-15,'',0,1,self.sliderMove,color=red)
        self.s2=dragbar(x,y   ,'',0,1,self.sliderMove,color=green)
        self.s3=dragbar(x,y+15,'',0,1,self.sliderMove,color=blue)
        self.update()


class colorTribar:
    """A widget using a Curve object to show 3 color values.

    Constructor: colorTribar(float,float,float,float,color,color,color)
    """

    def update(self):
        """Update the color values on the model from memory"""

        self._model.color[0]=self._col1
        self._model.color[1]=self._col1
        self._model.color[2]=self._col2
        self._model.color[3]=self._col2
        self._model.color[4]=self._col3
        self._model.color[5]=self._col3

    def setColor(self,col1=None,col2=None,col3=None):
        """Change the color values.

        setColor(color,color,color) -> void
        """
        if col1: self._col1=col1
        if col2: self._col2=col2
        if col3: self._col3=col3
        self.update()

    def __init__(self,x,y,w,h,col1,col2,col3):
        """Initialise and update GUI elements"""

        #Store colors
        self._col1=col1
        self._col2=col2
        self._col3=col3

        #Create component
        pos=dWinPos(x,y)
        ylist=[pos[1]-h,
               pos[1]-0.33*h, pos[1]-0.33*h,
               pos[1]+0.33*h, pos[1]+0.33*h,
               pos[1]+h]
        self._model=curve(radius=w,x=pos[0],y=ylist)
        self.update()
        

# ------------------------------------------------------------------------------
#GUI BUILDING/OPERATION


class GUI:
    """The user interaction handler and main application GUI. """    

    #functions:    initialisation; all buttons; all sliders
    #do return statements where needed: load/changename button; colorsliders

    def color1Change(self,value):
        """Call the general color changer"""
        self._colorChange(1,value)

    def color2Change(self,value):
        """Call the general color changer"""
        self._colorChange(2,value)

    def color3Change(self,value):
        """Call the general color changer"""
        self._colorChange(3,value)

    def _colorChange(self,colorNum,value):
        """Update seed data and display with the new color"""
        if colorNum==1: self.colorBar.setColor(col1=value)
        if colorNum==2: self.colorBar.setColor(col2=value)     
        if colorNum==3: self.colorBar.setColor(col3=value)
        #self.mainseed.color[colorNum] = value

    def globalUpdate(self):
        """Update all display widgets from the current seed settings"""
        
        pass
        #self.colorSlider1.setColor(ltgrey)
        
        #update all widgets. after loading a new seed
            #(Override control settings with seed data; automatically triggers)


    def __init__(self):
        """Create all GUI components"""
    
        #Initialiser: get file/keep data

        #Add widgets for the Data display
            ##self.xx=box(pos=dWinPos(dataWinW*0.25,dataWinH*0.3), width=10, height=10, length=10,
                        ##color=color.red)
        self.colorBar=colorTribar(dataWinW*0.5,dataWinH*0.5,10,100,red,green,blue)

        #Add widgets for the Controls display
        text(0,100,'COLORS',white)
        self.colorSlider1 = colorSlider(-8,100+vspacing*1,self.color1Change)
        self.colorSlider2 = colorSlider(-8,100+vspacing*2,self.color2Change)
        self.colorSlider3 = colorSlider(-8,100+vspacing*3,self.color3Change)

        x=220
        text(x,100,'FIRST STEM',blue)
        self.iniLenBar = dragbar(x,110+vspacing*1,'Length:',0,1,testReturn)
        self.iniWidthBar = dragbar(x,110+vspacing*2,'Width:',0,1,testReturn)
        self.iniAngleBar = dragbar(x,110+vspacing*3,'Branch Angle:',0,1,testReturn)
        self.iniSplitsBar = dragbar(x,110+vspacing*4,'Branches/Split:',0,1,testReturn)

        x=435
        text(x,100,'CHANGE RATES',red)
        self.changeLenBar = dragbar(x,110+vspacing*1,'Length:',0,1,testReturn)
        self.changeWidthBar = dragbar(x,110+vspacing*2,'Width:',0,1,testReturn)
        self.changeAngleBar = dragbar(x,110+vspacing*3,'Branch Angle:',0,1,testReturn)
        self.changeSplitsBar = dragbar(x,110+vspacing*4,'Branches/Split',0,1,testReturn)

        x=650
        text(x,100,'GROW CYCLE',green)
        self.cycleTimeBar = dragbar(x,110+vspacing*1,'Time:',0,1,testReturn)
        self.cycleMutationBar = dragbar(x,110+vspacing*2,'Mutation:',0,1,testReturn)
        self.cycleIterationsBar = dragbar(x,110+vspacing*3,'Iterations:',0,1,testReturn)
        
        #Update state
        self.globalUpdate()


# --------------------------------------------------------------------------
#MAIN APPLICATION

class runtime:
    """The main application """
    
    def __init__(self):
        """Set up the controls window and process input."""    

        #Make controls window
        self.ctrlWin = controls(x=25, y=25, width=ctrlWinW,
                                title='==PyPlant Seed Editor==        Controls',
                                height=ctrlWinH, range=ctrlWinH)
        slider(pos=(-999,-999))

        #Make data window        
        self.dataWin = display(height=dataWinH, width=dataWinW,
                               range=dataWinH,
                               title='==PyPlant Seed Editor==        Data',
                               x = self.ctrlWin.x,
                               y=self.ctrlWin.y+self.ctrlWin.height)
        
        self.g = GUI()

        #Main loop
        while True:
            rate(100)
            self.ctrlWin.interact()
            

r=runtime()

# ----------------------------------------------------------------------------
