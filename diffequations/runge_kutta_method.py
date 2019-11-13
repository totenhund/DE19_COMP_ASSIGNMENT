from diffequations.numeric_method import NumericMethod
from sympy import *
import sympy as sp


class RungeKuttaMethod(NumericMethod):

    def __init__(self):
        super().__init__()

    def plot_numeric(self, x, y, x_max, grid, func):
        super().plot_numeric(x, y, x_max, grid, func)
        self.func = func
        self.y_points = []
        self.x_points = []
        while x < x_max:
            try:
                k1 = grid * self.arg_eval(x, y)
                k2 = grid * self.arg_eval(x + grid/2, y + k1/2)
                k3 = grid * self.arg_eval(x + grid/2, y + k2/2)
                k4 = grid * self.arg_eval(x + grid, y + k3)
                x += grid
                y += (k1 + k2 + k2 + k3 + k3 + k4) / 6
            except ZeroDivisionError or ValueError:
                x += grid
                continue
            self.x_points.append(x)
            self.y_points.append(y)

