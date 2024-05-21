import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut
from OpenGL.GLUT import glutMouseFunc, glutMotionFunc, glutPassiveMotionFunc
import numpy as np

# add more dots for higher power
control_points = [
    [-0.75, -0.75],
]

selected_point = None

# dots's response range = size / win's size + inaccuracies
selection_radius = 5 / 500 + 0.004

def init():
    gl.glClearColor(0.0, 0.0, 0.0, 1.0)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    glu.gluOrtho2D(-1.0, 1.0, -1.0, 1.0) 

def draw_bezier_curve(points):
    segments = 100

    bezier_points = []
    for i in range(segments + 1):
        t = i / segments
        bezier_points.append(de_casteljau(points, t))

    gl.glBegin(gl.GL_LINE_STRIP)
    for point in bezier_points:
        gl.glVertex2fv(point)
    gl.glEnd()

def de_casteljau(points, t):
    points = np.array(points)
    while len(points) > 1:
        points = (1-t) * points[:-1] + t * points[1:]
    return points[0]

def display():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glColor3f(1.0, 1.0, 1.0)
    draw_bezier_curve(control_points)

    gl.glColor3f(1.0, 0.0, 0.0)
    gl.glPointSize(5.0)
    gl.glBegin(gl.GL_POINTS)
    for point in control_points:
        gl.glVertex2fv(point)
    gl.glEnd()

    gl.glBegin(gl.GL_LINES)
    for i in range(len(control_points)-1):
            gl.glVertex2fv(control_points[i])
            gl.glVertex2fv(control_points[i + 1])
    gl.glEnd()

    glut.glutSwapBuffers()

def mouse(button, state, x, y):
    global selected_point
    if state == glut.GLUT_DOWN:
        window_width = glut.glutGet(glut.GLUT_WINDOW_WIDTH)
        window_height = glut.glutGet(glut.GLUT_WINDOW_HEIGHT)
        opengl_x = (x - window_width / 2) / (window_width / 2)
        opengl_y = -(y - window_height / 2) / (window_height / 2)
        flag=0
        for i, point in enumerate(control_points):
            if np.linalg.norm(point - np.array([opengl_x, opengl_y])) < selection_radius:
                selected_point = i
                flag=1
                break
        if flag==0:
            point=[opengl_x, opengl_y]
            control_points.append(point)
            glut.glutPostRedisplay()
            
    else:
        selected_point = None

def motion(x, y):
    global selected_point
    if selected_point is not None:
        window_width = glut.glutGet(glut.GLUT_WINDOW_WIDTH)
        window_height = glut.glutGet(glut.GLUT_WINDOW_HEIGHT)
        opengl_x = (x - window_width / 2) / (window_width / 2)
        opengl_y = -(y - window_height / 2) / (window_height / 2)

        control_points[selected_point] = [opengl_x, opengl_y]
        glut.glutPostRedisplay()

def main():
    glut.glutInit()
    glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGB)    
    glut.glutInitWindowSize(500,500) 
    glut.glutInitWindowPosition(0,0) 
    glut.glutCreateWindow("Bezier Curve")
    glut.glutDisplayFunc(display)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    init()
    glut.glutMainLoop()

if __name__ == "__main__":
    main()
