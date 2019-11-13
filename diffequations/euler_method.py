from diffequations.numeric_method import NumericMethod
from sympy import *
import sympy as sp


class EulerMethod(NumericMethod):

    def __init__(self):
        super().__init__()

    def plot_numeric(self, x, y, x_max, grid, func):
        super().plot_numeric(x, y, x_max, grid, func)
        # find points for euler method
        self.func = func
        self.y_points = []
        self.x_points = []
        while x < x_max:
            try:
                k = eval(self.func)
                x += grid
                y += grid * k
            except ZeroDivisionError or ValueError:
                x += grid
                continue
            self.x_points.append(x)
            self.y_points.append(y)
