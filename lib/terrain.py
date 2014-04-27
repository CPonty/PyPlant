"""
PyPlant 1.0
LIBRARY: Terrain Generator

Copyright(c) 2010 Chris Ponticello
s4234549@student.uq.edu.au

DESCRIPTION:
A series of inheriting classes, building up functionality from a simple polygon
to model converter, to a parameter-based 3d terrain generator.

LICENSE:
I, Chris Ponticello, hereby grant the rights to copy, redistribute, modify and
otherwise edit any source code file included within PyPlant 1.0, provided that
this license agreement and my ownership of the code is maintained and
acknowledged.

I also grant the right to non-commercial use of the source code without my
express permission. Commercial users must seek the permission of the author.
"""

from visual import *
from random import random

# -------------------------------------------------------------------------------------
"""
About the features used in vpython:
http://www.vpython.org/contents/docs/visual/faces.html
http://www.vpython.org/contents/docs/visual/frame.html
http://www.vpython.org/contents/docs/visual/display.html
"""
# ------------------------------------------------------------------------------


class model:
    """The base class for creating a custom 3D model in Vpython.

    Constructor: model(display, color, boolean)
    """
    
    def __init__(self, window, color=(1,1,1), clipping=False):
        """Initialise an empty model in the given display."""
        
        self._window = window
        self._frame = frame(display=self._window)
        self._poly = faces(frame=self._frame, display=self._window)
        self._col = color
        self._clipping = clipping #single-sided 3d render

    def triNorm(self, vertices): 
        """Get a unit normal vector for the given pointlist triangle.

        triNorm(tuple<vector,vector,vector> -> vector
        Precondition:   vertices[0]<>vertices[1]<>vertices[2]                        
        """
        
        v1 = vertices[1]-vertices[0]
        v2 = vertices[2]-vertices[0]
        normal = cross(v1,v2)
        return normal*(1./mag(normal))

    def addTriangle(self, vertices):
        """Append a trangular face to the model.

        addTriangle(tuple<vector,vector,vector> -> void
        Precondition:   vertices[0]<>vertices[1]<>vertices[2]                        
        """
        
        norm=self.triNorm(vertices)
        
        #add the triangle to the model
        for vertex in vertices:
            self._poly.append( pos=vertex,color=self._col,normal=norm )
            
        #for two-sided drawing, add reversed vertices/normals
        if self._clipping==False:
            for vertex in (vertices[0],vertices[2],vertices[1]):                
                self._poly.append( pos=vertex,color=self._col,normal=-norm )

    def addPolygon(self, vertices):
        """Add an n-sided polygon to the model.

        addPolygon(list<tuple<float,float,float>> -> void
        Preconditions:  len(vertices)>2
                        vertices[0]<>vertices[1]<>...<>vertices[n]                        
        """
        
        #create a fan pattern of triangles around the polygon
        for x in range(len(vertices)-2):
            self.addTriangle( (vector(vertices[0]),vector(vertices[x+1]),
                               vector(vertices[x+2])) )

        
class gridMesh(model):
    """Specialisation of model: a 3d grid-coordinate mesh generator.

    Constructor: gridMesh(display, color, list<float>, list<float>,
                            list<list<float>>, color, boolean, boolean)

    Class invariant:
        len(xlist)>1
        and
        len(zlist)>1
        and
        len(xlist)==len(ygrid)
        and
        len(zlist)==len(ygrid[n]), for all 0<=n<=len(ygrid)       
    """    
    
    def __init__(self, window, xlist, zlist, ygrid, color=(1,1,1),
                 shading=False, clipping=False):
        """Create empty model; fill with polygons constructed from coordinate
            lists.
        """
        
        model.__init__(self, window, color, clipping)
        
        #for each x-z point pair (excluding the end row/column)
        for i in range(len(xlist)-2):
            for j in range(len(zlist)-2):
                #create a four-vertex polygon- the terrain square for this point
                self.addPolygon(( (xlist[i],  ygrid[i][j],    zlist[j]),
                                  (xlist[i],  ygrid[i][j+1],  zlist[j+1]),
                                  (xlist[i+1],ygrid[i+1][j+1],zlist[j+1]),
                                  (xlist[i+1],ygrid[i+1][j],  zlist[j])  ))
        #smooth texture shading
        if shading:
            self._poly.smooth()
            #NB: smoothing time  <2ms for a 5000-point model
            #    only need to run once (after finishing model)
            #    i.e. very fast - always use it if it looks better


class terrain_feature(gridMesh):
    """Specialisation of gridMesh: generates a terrain grid-coordinate map and
        builds the 3d model

    Constructor: terrain_hill(display,float,float,function,float,float,color,
                                boolean,boolean)

    Class invariant:
        gridcount>2
        gridsize>0
        Yfunction takes 4 float arguments
    """  
    
    def __init__(self,window,gridcount,gridsize,Yfunction,arg1=0,arg2=0,
                 color=(1,1,1),shading=False,clipping=True):
        """Generates the terrain's coordinate lists, based on input paramters
            and an external height-finding function.
        """

        #setup grid of evenly spaced x-y values around origin
        xlist = arange(-gridcount*gridsize*0.5,gridcount*gridsize*0.5,gridsize)
        zlist = xlist

        #generate height values
        ygrid = []
        for i in xlist:
            tempList = []
            for j in zlist:
                tempList.append(Yfunction(i,j,arg1,arg2))
            ygrid.append(tempList)

        #pass point lists to the meshGrid-Model initialiser
        gridMesh.__init__(self,window,xlist,zlist,ygrid,color,shading,clipping)


def hillHeight(x,z,hillsize, slope):
    """A height calculation for generating hilly terrain.
    Returns the y-value (height) of the point on the given hill.

    hillHeight(float,float,float,float) -> float
    Precondition: hillsize>0
    """
    dist = (x**2+z**2)**(slope*4)
    if dist>hillsize:
        dist=hillsize
    return -dist*slope *(1-(1-2*random())*0.075)

# ------------------------------------------------------------------------------
