import sympy as sp
from sympy import *


class ExactSolution:

    def __init__(self):
        self.x_points = []
        self.y_points = []
        self.func = ''

    def exact_solution(self, x0, y0, x_max, grid, func):
        # find points for  exact solution
        self.func = func
        self.x_points = []
        self.y_points = []
        x = sp.symbols('x')
        y = sp.Function('y')(x)
        equation = Eq(y.diff(x), eval(self.func))
        sol = dsolve(equation, y).rhs
        constants = solve([sol.subs(x, x0) - y0], dict='True')
        fun = sol.subs(constants[0])
        while x0 < x_max:
            self.x_points.append(x0)
            self.y_points.append(y0)
            x0 += grid
            y0 = fun.subs(x, x0)
