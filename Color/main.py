from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

IS_PERSPECTIVE = True  # 透视投影
VIEW = np.array([-0.8, 0.8, -0.8, 0.8, 1.0, 20.0])  # 视景体的left/right/bottom/top/near/far六个面
EYE = np.array([0.0, 12.0, 0.0])  # 眼睛的位置（默认z轴的正方向）
LOOK_AT = np.array([0.0, 0.0, 0.0])  # 瞄准方向的参考点（默认在坐标原点）
EYE_UP = np.array([0.0, 1.0, 0.0])  # 定义对观察者而言的上方（默认y轴的正方向）
WIN_W, WIN_H = 640, 480  # 保存窗口宽度和高度的变量
LEFT_IS_DOWNED = False  # 鼠标左键被按下
MOUSE_X, MOUSE_Y = 0, 0  # 考察鼠标位移量时保存的起始位置
angle = 0

def getposture():
    global EYE, LOOK_AT
    dist = np.sqrt(np.power((EYE-LOOK_AT), 2).sum())
    if dist > 0:
        phi = np.arcsin((EYE[1]-LOOK_AT[1])/dist)
        theta = np.arcsin((EYE[0]-LOOK_AT[0])/(dist*np.cos(phi)))
    else:
        phi = 0.0
        theta = 0.0
    return dist, phi, theta

DIST, PHI, THETA = getposture()  # 眼睛与观察目标之间的距离、仰角、方位角

def display():
    global IS_PERSPECTIVE, VIEW
    global EYE, LOOK_AT, EYE_UP
    global WIN_W, WIN_H
    global angle
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    if WIN_W > WIN_H:
        if IS_PERSPECTIVE:
            glFrustum(VIEW[0]*WIN_W/WIN_H, VIEW[1]*WIN_W/WIN_H, VIEW[2], VIEW[3], VIEW[4], VIEW[5])
        else:
            glOrtho(VIEW[0]*WIN_W/WIN_H, VIEW[1]*WIN_W/WIN_H, VIEW[2], VIEW[3], VIEW[4], VIEW[5])
    else:
        if IS_PERSPECTIVE:
            glFrustum(VIEW[0], VIEW[1], VIEW[2]*WIN_H/WIN_W, VIEW[3]*WIN_H/WIN_W, VIEW[4], VIEW[5])
        else:
            glOrtho(VIEW[0], VIEW[1], VIEW[2]*WIN_H/WIN_W, VIEW[3]*WIN_H/WIN_W, VIEW[4], VIEW[5])
        
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(
        EYE[0], EYE[1], EYE[2], 
        LOOK_AT[0], LOOK_AT[1], LOOK_AT[2],
        EYE_UP[0], EYE_UP[1], EYE_UP[2]
    )

    glViewport(0, 0, WIN_W, WIN_H)

    glutPostRedisplay()

    #定义环境光源0，它是一种白色的光源
    glLightfv(GL_LIGHT0, GL_POSITION,(10.0*np.cos(np.radians(angle)),0.0,10.0*np.sin(np.radians(angle)),1.0) )
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.0,0.0,0.0,1.0) )
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0,1.0,0.0,1.0) )
    glLightfv(GL_LIGHT0, GL_SPECULAR,(1.0,1.0,0.0,1.0) )
    #开启灯光
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)

    #定义环境光源1，它是一种白色的光源
    glLightfv(GL_LIGHT1, GL_POSITION,(-10.0*np.cos(np.radians(angle)),0.0,-10.0*np.sin(np.radians(angle)),1.0) )
    glLightfv(GL_LIGHT1, GL_AMBIENT, (0.0,0.0,0.0,1.0) )
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (0.0,1.0,1.0,1.0) )
    glLightfv(GL_LIGHT1, GL_SPECULAR,(0.0,1.0,1.0,1.0) )
    #开启灯光
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHTING)
    glEnable(GL_DEPTH_TEST)
 
    
    glMaterialfv(GL_FRONT, GL_AMBIENT, (0.0, 0.0, 0.0, 1.0))
    glMaterialfv(GL_FRONT, GL_DIFFUSE, (0.0, 0.0, 0.0, 0.0))
    glMaterialfv(GL_FRONT, GL_SPECULAR, (0.0, 0.0, 0.0, 0.0))
    glMaterialfv(GL_FRONT, GL_EMISSION, (1.0, 1.0, 0.0, 1.0))
    glMaterialf(GL_FRONT, GL_SHININESS, 0.0)
    glTranslatef(10.0*np.cos(np.radians(angle)), 0.0, 10.0*np.sin(np.radians(angle)))
    glutSolidSphere(1.0, 40, 32)
    glTranslatef(-10.0*np.cos(np.radians(angle)), 0.0, -10.0*np.sin(np.radians(angle)))

    glMaterialfv(GL_FRONT, GL_AMBIENT, (0.0, 0.0, 0.0, 1.0))
    glMaterialfv(GL_FRONT, GL_DIFFUSE, (0.0, 0.0, 0.0, 0.0))
    glMaterialfv(GL_FRONT, GL_SPECULAR, (0.0, 0.0, 0.0, 0.0))
    glMaterialfv(GL_FRONT, GL_EMISSION, (0.0, 1.0, 1.0, 1.0))
    glMaterialf(GL_FRONT, GL_SHININESS, 0.0)
    glTranslatef(-10.0*np.cos(np.radians(angle)), 0.0, -10.0*np.sin(np.radians(angle)))
    glutSolidSphere(1.0, 40, 32)
    glTranslatef(10.0*np.cos(np.radians(angle)), 0.0, 10.0*np.sin(np.radians(angle)))

    #环境光蓝灰色
    glMaterialfv(GL_FRONT, GL_AMBIENT, (0.0, 0.0, 0.0, 1.0))
    #漫射光红色
    glMaterialfv(GL_FRONT, GL_DIFFUSE, (0.5, 0.3, 0.1, 1.0))
    #镜面光白色
    glMaterialfv(GL_FRONT, GL_SPECULAR,(1.0, 1.0, 1.0, 1.0))
    #发光体蓝色
    glMaterialfv(GL_FRONT, GL_EMISSION, (0.0, 0.0, 0.0, 1.0))
    glMaterialf(GL_FRONT, GL_SHININESS,  30.0)
    glutSolidTeapot(3.0)

    #OpenGL缓冲区   
    glutSwapBuffers()

    angle += 0.5
    while angle > 360:
        angle = 0
    glFlush()

def reshape(width, height):
    global WIN_W, WIN_H
    WIN_W, WIN_H = width, height
    glutPostRedisplay()

def mouseclick(button, state, x, y):
    global LEFT_IS_DOWNED
    global MOUSE_X, MOUSE_Y
    MOUSE_X, MOUSE_Y = x, y
    if button == GLUT_LEFT_BUTTON:
        LEFT_IS_DOWNED = state == GLUT_DOWN

def mousemotion(x, y):
    global LEFT_IS_DOWNED
    global EYE, EYE_UP
    global MOUSE_X, MOUSE_Y
    global DIST, PHI, THETA
    global WIN_W, WIN_H
    
    if LEFT_IS_DOWNED:
        dx = MOUSE_X - x
        dy = y - MOUSE_Y
        MOUSE_X, MOUSE_Y = x, y
        PHI += 2 * np.pi * dy / WIN_H
        PHI %= 2 * np.pi
        THETA += 2 * np.pi * dx / WIN_W
        THETA %= 2 * np.pi
        r = DIST * np.cos(PHI)
        EYE[1] = DIST * np.sin(PHI)
        EYE[0] = r * np.sin(THETA)
        EYE[2] = r * np.cos(THETA)
        if 0.5 * np.pi < PHI < 1.5 * np.pi:
            EYE_UP[1] = -1.0
        else:
            EYE_UP[1] = 1.0
        glutPostRedisplay()

def keydown(key, x, y):
    global DIST, PHI, THETA
    global EYE, LOOK_AT, EYE_UP
    global IS_PERSPECTIVE, VIEW
    match key:
        # movement
        case b'w':
            EYE = LOOK_AT + (EYE - LOOK_AT) * 0.9
            DIST, PHI, THETA = getposture()
        case b's':
            EYE = LOOK_AT + (EYE - LOOK_AT) * 1.1
            DIST, PHI, THETA = getposture()

        # change perspective
        case b' ':
            IS_PERSPECTIVE = not IS_PERSPECTIVE

    glutPostRedisplay()

if __name__ == "__main__":
    glutInit()  # 使用glut库初始化OpenGL
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    # glEnable(GL_DEPTH_TEST)  # 开启深度测试，实现遮挡关系
    # glDepthFunc(GL_LEQUAL)
    glutInitWindowSize(WIN_W, WIN_H)  # 初始化窗口大小
    glutCreateWindow("OpenGL Window")  # 创建窗口
    glClearColor(0.8, 0.8, 0.8, 1.0)  # 背景颜色
    glutDisplayFunc(display)  # 注册回调函数display
    glutKeyboardFunc(keydown)
    glutReshapeFunc(reshape)  # 注册响应窗口改变的函数reshape
    glutMouseFunc(mouseclick)  # 注册响应鼠标点击的函数mouseclick
    glutMotionFunc(mousemotion)  # 注册响应鼠标拖拽的函数mousemotion
    glutMainLoop()  # 进入glut主循环