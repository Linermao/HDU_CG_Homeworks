from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

RED = (1.0, 0.0, 0.0, 1.0)
GREEN = (0.0, 1.0, 0.0, 1.0)
BLUE = (0.0, 0.0, 1.0, 1.0)

def draw_axis() -> None:
    # draw XYZ axis
    glBegin(GL_LINES)            
    
    # X axis in red
    glColor4f(*RED)
    glVertex3f(-2, 0.0, 0.0)
    glVertex3f(2, 0.0, 0.0)
    
    # Y axis in green
    glColor4f(*GREEN)
    glVertex3f(0.0, -2, 0.0)
    glVertex3f(0.0, 2, 0.0)
    
    # Z axis in blue
    glColor4f(*BLUE)
    glVertex3f(0.0, 0.0, -2)
    glVertex3f(0.0, 0.0, 2)
    
    glEnd()      

