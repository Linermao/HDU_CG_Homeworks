from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

WHITE = (1.0, 1.0, 1.0, 1.0)
BLACK = (0.0, 0.0, 0.0, 0.0)
RED = (1.0, 0.0, 0.0, 1.0)
GREEN = (0.0, 1.0, 0.0, 1.0)
BLUE = (0.0, 0.0, 1.0, 1.0)

def draw_wire(vertices: np.ndarray, edges: list, color: tuple) -> None:

    glColor4f(*color)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex4fv(vertices[vertex])
    glEnd()

def draw_hard(vertices: np.ndarray, edges: list, color: tuple) -> None:

    glColor4f(*color)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex4fv(vertices[vertex])
    glEnd()

def sphere_points():
    u = np.linspace(0, 2*np.pi, 30)
    v = np.linspace(0, np.pi, 30)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))
    return np.vstack((x.flatten(), y.flatten(), z.flatten(), np.ones(np.size(x.flatten()))))

POINTS = sphere_points()

class Pyramid:

    def __init__ (self):
        self.vertices = np.array([
            [-1, 0, 1, 1],
            [-1, 0,-1, 1],
            [ 1, 0,-1, 1],
            [ 1, 0, 1, 1],
            [ 0, 1, 0, 1]
        ])

        self.edges = [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),
            (0, 4),
            (1, 4),
            (2, 4),
            (3, 4)
        ]

        self.color = WHITE
        
    def draw(self) -> None:
        draw_wire(self.vertices, self.edges, self.color)

    def transfer(self, matrix: np.ndarray) -> None:
        self.vertices = np.dot(matrix, self.vertices.T).T

    def restore(self) -> None:
        self.vertices = np.array([
            [-1, 0, 1, 1],
            [-1, 0,-1, 1],
            [ 1, 0,-1, 1],
            [ 1, 0, 1, 1],
            [ 0, 1, 0, 1]
        ])

class Cube:

    def __init__(self):
        self.vertices = np.array([
            [-1, -1, 1, 1],
            [-1, -1,-1, 1],
            [ 1, -1,-1, 1],
            [ 1, -1, 1, 1],
            [-1,  1, 1, 1],
            [-1,  1,-1, 1],
            [ 1,  1,-1, 1],
            [ 1,  1, 1, 1]
        ])

        self.edges = [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),
            (0, 4),
            (1, 5),
            (2, 6),
            (3, 7),
            (4, 5),
            (5, 6),
            (6, 7),
            (7, 4)
        ]

        self.color = WHITE

    def draw(self) -> None:
        draw_wire(self.vertices, self.edges, self.color)

    def transfer(self, matrix: np.ndarray) -> None:
        self.vertices = np.dot(matrix, self.vertices.T).T

    def restore(self) -> None:
        self.vertices = np.array([
            [-1, -1, 1, 1],
            [-1, -1,-1, 1],
            [ 1, -1,-1, 1],
            [ 1, -1, 1, 1],
            [-1,  1, 1, 1],
            [-1,  1,-1, 1],
            [ 1,  1,-1, 1],
            [ 1,  1, 1, 1]
        ])

class Sphere:
    '''
    此处球体使用遍历点法作图，开销大，还可以进一步优化
    直接对所有点进行仿射变换开销大，还需要进一步优化
    '''
    def __init__(self):

        # center point
        self.vertices = np.array([
            [0, 0, 0, 1]
        ])
        self.vertices = np.concatenate((self.vertices, POINTS.T), axis=0)

        self.color = WHITE

    def draw(self):
        glColor4f(*self.color)
        for vertice in self.vertices:
            glBegin(GL_POINTS)
            glVertex4fv(vertice)
            glEnd()

    def transfer(self, matrix: np.ndarray) -> None:
        self.vertices = np.dot(matrix, self.vertices.T).T

    def restore(self) -> None:
        self.vertices = np.array([
            [0, 0, 0, 1]
        ])
        self.vertices = np.concatenate((self.vertices, POINTS.T), axis=0)