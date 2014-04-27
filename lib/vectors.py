"""
PyPlant 1.0
LIBRARY: Specialised Vector Maths

Copyright(c) 2010 Chris Ponticello
s4234549@student.uq.edu.au

DESCRIPTION:
A series of functions which build on each other to eventually perform the
vector positioning of branches (relative to their parent branches)
in a single call.

LICENSE:
I, Chris Ponticello, hereby grant the rights to copy, redistribute, modify and
otherwise edit any source code file included within PyPlant 1.0, provided that
this license agreement and my ownership of the code is maintained and
acknowledged.

I also grant the right to non-commercial use of the source code without my
express permission. Commercial users must seek the permission of the author.
"""

from visual import *
from math import sqrt,pi,radians,degrees,atan,asin


# -------------------------------------------------------------------------------------
"""
Using vectors in my library: vector input/output uses the Vpython vector class.

Vectors in Vpython: the y-direction (not z) is treated as 'up' in the world.
Therefore mathematics for this library has been modified so that all operations
treat x-z as the 'floor' plane; e.g. 'dir' or 'direction' is the angle on this
plane.

http://www.vpython.org/contents/docs/visual/vector.html

NB: ANGLES IN RADIANS
"""
# ------------------------------------------------------------------------------


def direction(dx,dy,allow_negative=False):
    """Return the direction angle for the given displacement.

    direction(float,float,boolean) -> float
    """
    
    angle=0
    #special case: x==0; avoid division by zero
    if dx==0:
        if dy==0:
            angle=0.
        else:
            angle=pi/2
    #general case: use arctan; keep 0<dir<2pi if needed
    else:
        angle=atan(dy/dx)
        if dx<0 and not allow_negative:
            angle+=pi
        elif (dy<0) and not allow_negative:
            angle+=2*pi
    return angle    


def vec_dir(vec):
    """Return the direction angle of the given vector.     

    vec_dir(vector) -> float
    """

    #find 2d direction for the x-z plane (the 'actual' ground axes)
    return direction(vec.x,vec.z)


def vec_alt(vec):
    """Return the altitude angle of the given vector.

    vec_alt(vector) -> float
    """      

    #the 'actual' x axis for the calculation
    dx = (vec.x**2+vec.z**2)**0.5
    #find the angle for the vector's side-on cross section
    alt = direction(dx,vec.y,True)
    if alt>pi:
        alt=pi-alt
    return alt
    

def vec_yRotate(vec,angle):
    """Return the 3d vector with direction change (y axis rotation) applied.

    vec_yRotate(vector,float) -> vector

    Nonlinear Transformation Matrix:
    T = [ cos(a) 0 -sin(a)
          0      1  0
          sin(a) 0  cos(a) ]
    """
    #Transformed vector values (result of matrix multiplication)
        #x=cos(angle)*vec.x - sin(angle)*vec.z
        #z=sin(angle)*vec.x + cos(angle)*vec.z
        #return vector(x,vec.y,z)
    return rotate(vec, angle, (0,1,0))    


def vec_zRotate(vec,angle):
    """Return the 3d vector with z axis rotation applied.

    vec_zRotate(vector,float) -> vector

    Nonlinear Transformation Matrix:
    T = [ cos(a) -sin(a) 0
          sin(a)  cos(a) 0
          0       0      1 ]
    """
    #Transformed vector values (result of matrix multiplication)
        #x=cos(angle)*vec.x - sin(angle)*vec.y
        #y=sin(angle)*vec.x + cos(angle)*vec.y
        #return vector(x,y,vec.z )
    return rotate(vec, angle, (0,0,1))


def vec_set_len(vec,length):
    """Return a vector with magnitude scaled by the given length.

    vec_set_len(vector,float) -> vector
    """
    #multiply the length by the unit vector
    return vec*(1./vec.mag)*length
    
    
def vec_inc_len(vec,length):
    """Return a vector with magnitude increased by the given length.

    vec_inc_len(vector,float) -> vector
    """
    return vec_set_len(vec,vec.mag+length)


def vec_branch(parent_vec,split,rotation,length):
    """Combine vector functionality: create a vector split/rotated
    from a second (reference) vector.

    vec_branch(float,float,float,vector) -> vector
    Preconditions: mag(parent_vec)>0
                   length>0
    """
    #generate the branch's state of rotation/split about a unit 'i' vector
    x = length*cos(split)
    R = length*sin(split)
    y = R*cos(rotation)
    z = R*sin(rotation)
    vec_ini = vector(x,y,z)
    #rotate about z-axis (vertical orientation)
    vec_ini = vec_zRotate(vec_ini,vec_alt(parent_vec))
    #rotate about xz plane (direction)
    vec_ini = vec_yRotate(vec_ini,vec_dir(parent_vec))
    return vec_ini
    

# ----------------------------------------------------------------------------
