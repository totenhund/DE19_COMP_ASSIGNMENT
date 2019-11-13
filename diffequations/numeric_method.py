from diffequations.exact_solution import ExactSolution
from sympy import *
import sympy as sp
import math
import numpy as np

class NumericMethod:

    def __init__(self):
        self.func = ''
        self.arg_eval = lambda x, y: eval(self.func)
        self.max = 0
        # points of numerical method
        self.x_points = []
        self.y_points = []
        # points of global and local errors
        self.y_gl_err = []
        self.y_loc_err = []
        # points of global errors in dependence of step
        self.x_dep = []
        self.y_dep = []

    def plot_numeric(self, x, y, x_max, grid, func):
        pass

    def found_glob_error(self, x_exact, y_exact):

        # find gl error
        self.y_gl_err = []
        for i in range(0, min(len(self.x_points), len(self.y_points), len(x_exact), len(y_exact))):
            self.y_gl_err.append(y_exact[i] - self.y_points[i])

        self.max = max(self.y_gl_err)

    def found_loc_error(self):

        self.y_loc_err = []
        for i in range(1, len(self.y_gl_err)):
            self.y_loc_err.append(math.fabs(self.y_gl_err[i] - self.y_gl_err[i-1]))

    def found_global(self, x, y, x_max, grid, grid_step, func, flag:bool):
        if flag:
            self.x_dep = []
            self.y_dep = []
            exact = ExactSolution()
            while grid < grid_step:
                self.plot_numeric(x, y, x_max, grid, func)
                exact.exact_solution(x, y, x_max, grid, func)
                self.found_glob_error(exact.x_points, exact.y_points)
                self.y_dep.append(self.max)
                self.x_dep.append(grid)
                grid += 0.1
        else:
            return
