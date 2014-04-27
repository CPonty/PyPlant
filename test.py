# Import
import sys, os
sys.path.append(os.getcwd()+'\lib')#adds lib folder to import directories

from visual import *
from terrain import *
from vectors import *
from seeds import *



# Test Terrain-----------------------------------------------------------------

scene.background = (0,0,0.5)
#scene.stereo='redcyan'

#sphere(radius=0.05)
terrain_feature(scene,24,0.5,hillHeight,8,0.2,(0.6,0.3,0.15),False,True)

arr = arrow(axis=(0,1,0), length=2)
arr2 = arrow(axis=(1,0,0), length=2, width=0.5, color=(1,0,0))
arr3 = arrow(axis=(0,0,1), length=2, width=0.5, color=(0,1,0))

