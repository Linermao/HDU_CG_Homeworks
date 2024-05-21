import numpy as np
from math import *

theta = radians(5)

class Transformer:
    def __init__ (self):
        self.matrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    def sym_axis_x(self) -> None:
        self.matrix = np.array([
            [-1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    def sym_axis_y(self) -> None:
        self.matrix = np.array([
            [1, 0, 0, 0],
            [0, -1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    def sym_axis_z(self) -> None:
        self.matrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, -1, 0],
            [0, 0, 0, 1]
        ])

    def sym_o(self) -> None:
        self.matrix = np.array([
            [-1, 0, 0, 0],
            [0, -1, 0, 0],
            [0, 0, -1, 0],
            [0, 0, 0, 1]
        ])

    def sym_give(self) -> None:
        self.matrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    def panning(self, tx, ty, tz) -> None:
        self.matrix = np.array([
            [1, 0, 0, tx],
            [0, 1, 0, ty],
            [0, 0, 1, tz],
            [0, 0, 0, 1],
        ])

    def rotate_axis_x(self) -> None:
        self.matrix = np.array([
            [1, 0,           0,          0],
            [0, cos(theta), -sin(theta), 0],
            [0, sin(theta),  cos(theta), 0],
            [0, 0,           0,          1],
        ])
    
    def rotate_axis_y(self) -> None:
        self.matrix = np.array([
            [cos(theta), 0, -sin(theta), 0],
            [0,          1,  0,          0],
            [sin(theta), 0,  cos(theta), 0],
            [0,          0,  0,          1],
        ])

    def rotate_axis_z(self) -> None:
        self.matrix = np.array([
            [cos(theta), -sin(theta), 0, 0],
            [sin(theta),  cos(theta), 0, 0],
            [0,           0,          1, 0],
            [0,           0,          0, 1],
        ])

    def shear_axis_x(self, x_y=0.5, x_z=0.5) -> None:
        self.matrix = np.array([
            [1,   0, 0, 0],
            [x_y, 1, 0, 0],
            [x_z, 0, 1, 0],
            [0,   0, 0, 1],
        ])

    def shear_axis_y(self, y_x=0.5, y_z=0.5) -> None:
        self.matrix = np.array([
            [y_x, 0, 0, 0],
            [0,   1, 0, 0],
            [y_z, 0, 1, 0],
            [0,   0, 0, 1],
        ])

    def shear_axis_z(self, x_y=0.5, x_z=0.5) -> None:
        self.matrix = np.array([
            [1,   0, 0, 0],
            [x_y, 1, 0, 0],
            [x_z, 0, 1, 0],
            [0,   0, 0, 1],
        ])