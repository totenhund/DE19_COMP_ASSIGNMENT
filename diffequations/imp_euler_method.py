from diffequations.numeric_method import NumericMethod
from sympy import *
import sympy as sp


class ImpEulerMethod(NumericMethod):

    def __init__(self):
        super().__init__()

    def plot_numeric(self, x, y, x_max, grid, func):
        super().plot_numeric(x, y, x_max, grid, func)
        self.func = func
        self.x_points = []
        self.y_points = []
        y_prev = x
        x_prev = y
        while x < x_max:
            try:
                f1 = y_prev + grid * self.arg_eval(x_prev, y_prev)
                x += grid
                y += grid * ((self.arg_eval(x_prev, y_prev) + self.arg_eval(x, f1)) / 2)
                x_prev = x
                y_prev = y
            except ZeroDivisionError or ValueError:
                x += grid
                continue
            self.x_points.append(x)
            self.y_points.append(y)

