from diffequations.euler_method import EulerMethod
from diffequations.imp_euler_method import ImpEulerMethod
from diffequations.runge_kutta_method import RungeKuttaMethod
from diffequations.exact_solution import ExactSolution

from sympy import *
import sympy as sp

import numpy as np

import matplotlib.pyplot as plt

from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
from matplotlib.figure import Figure


class PlotGraph:

    def __init__(self):
        # numeric methods
        self.euler = EulerMethod()
        self.improved_euler = ImpEulerMethod()
        self.runge_kutta = RungeKuttaMethod()
        self.exact = ExactSolution()
        # graphs
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.fig_gl_err = Figure(figsize=(5, 4), dpi=100)
        self.fig_global = Figure(figsize=(5, 4), dpi=100)
        self.a = self.fig.add_subplot(1, 1, 1)
        self.a_gl_err = self.fig_gl_err.add_subplot(1, 1, 1)
        self.a_global = self.fig_global.add_subplot(1, 1, 1)
        # plot or not plot
        self.ex_flag = False
        self.eul_flag = False
        self.imp_flag = False
        self.kutta_flag = False

    def init_methods(self, x, y, x_max, grid, func):
        # calculate points for numeric methods
        if self.eul_flag:
            self.euler.plot_numeric(x, y, x_max, grid, func)

        if self.imp_flag:
            self.improved_euler.plot_numeric(x, y, x_max, grid, func)

        if self.kutta_flag:
            self.runge_kutta.plot_numeric(x, y, x_max, grid, func)

        if self.ex_flag:
            self.exact.exact_solution(x, y, x_max, grid, func)

    def init_gl_error(self):
        # calculate global error for numeric method
        if self.eul_flag:
            self.euler.found_glob_error(self.exact.x_points, self.exact.y_points)
            self.euler.found_loc_error()
        if self.imp_flag:
            self.improved_euler.found_glob_error(self.exact.x_points, self.exact.y_points)
            self.improved_euler.found_loc_error()
        if self.kutta_flag:
            self.runge_kutta.found_glob_error(self.exact.x_points, self.exact.y_points)
            self.runge_kutta.found_loc_error()

    def plot_graph(self):
        # plot all numeric methods and exact solution
        self.a.clear()
        #self.a.title = "Numeric methods"
        self.a.axis([0, 10, 0, 1000])
        self.a.set_xlabel("X points")
        self.a.set_ylabel("Y points")
        if self.ex_flag:
            self.a.plot(self.exact.x_points, self.exact.y_points, label="Exact Solution")
        if self.imp_flag:
            self.a.plot(self.improved_euler.x_points, self.improved_euler.y_points, label="Improved Euler Method")
        if self.eul_flag:
            self.a.plot(self.euler.x_points, self.euler.y_points, label="Euler Method")
        if self.kutta_flag:
            self.a.plot(self.runge_kutta.x_points, self.runge_kutta.y_points, label="Runge-Kutta Method")

        self.a.legend()

    def plot_gll_err(self):
        # plot local trunc error of numeric methods
        self.a_gl_err.clear()
        self.a_gl_err.set_xlabel("X points")
        self.a_gl_err.set_ylabel("Y points")
        #self.a_gl_err.axis([0, 10, 0, 1000])

        if self.imp_flag:
            #self.a_gl_err.plot(self.improved_euler.x_points, self.improved_euler.y_gl_err, label="Improved Euler Method GE")
            self.a_gl_err.plot(self.improved_euler.x_points[slice(0, len(self.improved_euler.y_loc_err))], self.improved_euler.y_loc_err, label="Improved Euler Method Local")
        if self.eul_flag:
            #self.a_gl_err.plot(self.euler.x_points, self.euler.y_gl_err, label="Euler Method GE")
            self.a_gl_err.plot(self.euler.x_points[slice(0, len(self.euler.y_loc_err))], self.euler.y_loc_err, label="Euler Method Local")
        if self.kutta_flag:
            #self.a_gl_err.plot(self.runge_kutta.x_points, self.runge_kutta.y_gl_err, label="Runge-Kutta Method GE")
            self.a_gl_err.plot(self.runge_kutta.x_points[slice(0, len(self.runge_kutta.y_loc_err))], self.runge_kutta.y_loc_err, label="Runge-Kutta Method Local")

        self.a_gl_err.legend()

    def init_global(self, x, y, x_max, grid, grid_step, func):
        self.euler.found_global(x, y, x_max, grid, grid_step, func, self.eul_flag)
        self.improved_euler.found_global(x, y, x_max, grid, grid_step, func, self.imp_flag)
        self.runge_kutta.found_global(x, y, x_max, grid, grid_step, func, self.kutta_flag)

    def plot_global(self):
        self.a_global.clear()
        self.a_global.set_xlabel("X points")
        self.a_global.set_ylabel("Y errors")

        if self.eul_flag:
            self.a_global.plot(self.euler.x_dep, self.euler.y_dep, label="Euler Global")
        if self.imp_flag:
            self.a_global.plot(self.improved_euler.x_dep, self.improved_euler.y_dep, label="Imp Euler Global")
        if self.kutta_flag:
            self.a_global.plot(self.runge_kutta.x_dep, self.runge_kutta.y_dep, label="Runge Kutta Global")

        self.a_global.legend()
