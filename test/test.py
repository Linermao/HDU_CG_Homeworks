from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy
import sys

def init(): 
    glClearColor(1.0, 1.0, 1.0, 1.0) 
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0) 

def plotpoints(): 
    glClear(GL_COLOR_BUFFER_BIT) 
    glColor3f(0.0, 0.0, 0.0) 
    glPointSize(3.0) 
    for x in numpy.arange(-0.5, 0.5, 0.001): 
        y = numpy.sin(x*5*numpy.pi)
        glBegin(GL_POINTS) 

        glVertex2f(x, y)

        glEnd()
        glFlush()

    glBegin(GL_LINES)

    glVertex2f(-1.0, 0.0)
    glVertex2f(1.0, 0.0)
    glVertex2f(0.0, -1.0)
    glVertex2f(0.0, 1.0)

    glEnd()
    glFlush()

def run(): 
    glutInit(sys.argv) 
    glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB) 
    glutInitWindowSize(500,500) 
    glutInitWindowPosition(50,50) 
    glutCreateWindow("My OpenGL task") 
    glutDisplayFunc(plotpoints) 

    init() 
    glutMainLoop()

if __name__ == "__main__":
    run()