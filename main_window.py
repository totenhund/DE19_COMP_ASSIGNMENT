import sys
from plot_graph.plot_graph import PlotGraph

from sympy import *
import sympy as sp

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk

from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
from matplotlib.figure import Figure

from matplotlib.backends.backend_gtk3 import (
    NavigationToolbar2GTK3 as NavigationToolbar)
import numpy as np


class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Numeric methods")
        self.set_border_width(10)
        self.set_size_request(872, 657)
        #self.set_resizable(resizable=False)
        self.pl = PlotGraph()

        # Layout grid
        self.grid = Gtk.Grid(column_homogeneous=True, column_spacing=10, row_spacing=10)
        self.add(self.grid)

        # All entries (equation, x0, y0, step, bound)
        # equation
        self.equation = Gtk.Entry(placeholder_text="write your equation")
        self.equation.set_size_request(357, 47)

        # x0
        self.x_entry = Gtk.Entry(placeholder_text="initial point x")
        self.x_entry.set_size_request(134, 37)

        # y0
        self.y_entry = Gtk.Entry(placeholder_text="initial point y")
        self.y_entry.set_size_request(134, 37)

        # grid
        self.step = Gtk.Entry(placeholder_text="step")
        self.step.set_size_request(134, 37)

        # grid bound
        self.grid_bound = Gtk.Entry(placeholder_text="step bound")
        self.grid_bound.set_size_request(134, 37)

        # bound
        self.bound = Gtk.Entry(placeholder_text="x bound")
        self.bound.set_size_request(134, 37)

        # flag to check which error should be plotted(local or global)
        self.error_flag = False  # when False it means local, when True it means global

        # creating button
        self.button = Gtk.Button(label="PLOT GRAPH")
        self.button.connect("clicked", self.draw)
        self.button.set_size_request(115, 47)

        self.canvas = FigureCanvas(self.pl.fig)
        self.canvas.set_size_request(800, 600)

        # check buttons (for choice of methods that would be plotted)
        ex_box = Gtk.Box()
        label_ex = Gtk.Label("Exact")
        self.exact_check = Gtk.CheckButton()
        self.exact_check.connect("toggled", self.toggled)
        ex_box.pack_start(label_ex, True, True, 0)
        ex_box.pack_start(self.exact_check, True, True, 0)

        label_eul = Gtk.Label("Euler")
        eul_box = Gtk.Box()
        self.eul_check = Gtk.CheckButton()
        self.eul_check.connect("toggled", self.toggled)
        eul_box.pack_start(label_eul, True, True, 0)
        eul_box.pack_start(self.eul_check, True, True, 0)

        label_imp = Gtk.Label("Improved Eul")
        imp_box = Gtk.Box()
        self.imp_check = Gtk.CheckButton()
        self.imp_check.connect("toggled", self.toggled)
        imp_box.pack_start(label_imp, True, True, 0)
        imp_box.pack_start(self.imp_check, True, True, 0)

        label_kutta = Gtk.Label("Runge-Kutta  ")
        kutta_box = Gtk.Box()
        self.kutta_check = Gtk.CheckButton()
        self.kutta_check.connect("toggled", self.toggled)
        kutta_box.pack_start(label_kutta, True, True, 0)
        kutta_box.pack_start(self.kutta_check, True, True, 0)

        # global error canvas
        self.gl_canvas = FigureCanvas(self.pl.fig_gl_err)
        self.gl_canvas.set_size_request(800, 600)

        self.toolbar = NavigationToolbar(self.canvas, Gtk)
        self.toolbox = Gtk.Box()
        self.toolbox.add(self.toolbar)

        radio_box = Gtk.Box()
        loc_button = Gtk.RadioButton.new_with_label_from_widget(None, "Local")
        loc_button.connect("toggled", self.radio_toggled, "local", self)
        radio_box.pack_start(loc_button, False, False, 10)

        glob_button = Gtk.RadioButton.new_from_widget(loc_button)
        glob_button.set_label("Global")
        glob_button.connect("toggled", self.radio_toggled, "global", self)
        radio_box.pack_start(glob_button, False, False, 10)

        # Adding entries and buttons to grid
        self.grid.attach(self.equation, 2, 0, 3, 1)
        self.grid.attach(self.button, 4, 2, 1, 1)
        self.grid.attach(self.x_entry, 2, 1, 1, 1)
        self.grid.attach(self.y_entry, 3, 1, 1, 1)
        self.grid.attach(self.step, 2, 2, 1, 1)
        self.grid.attach(self.bound, 4, 1, 1, 1)
        self.grid.attach(self.toolbox, 2, 3, 1, 1)
        self.grid.attach(self.canvas, 2, 4, 3, 4)
        self.grid.attach(self.gl_canvas, 5, 4, 3, 4)
        self.grid.attach(ex_box, 5, 0, 1, 1)
        self.grid.attach(eul_box, 5, 1, 1, 1)
        self.grid.attach(imp_box, 7, 0, 1, 1)
        self.grid.attach(kutta_box, 7, 1, 1, 1)
        self.grid.attach(self.grid_bound, 3, 2, 1, 1)
        self.grid.attach(radio_box, 6, 2, 1, 1)

    @staticmethod
    def toggled(check_butt):
        if check_butt.get_active():
            print("Active")

    @staticmethod
    def radio_toggled(button, name, activity):
        if button.get_active() and name == "global":
            activity.error_flag = True
        else:
            activity.error_flag = False

    def draw(self, wid):
        # draw the graph on ui, click listener on button 'plot graph'
        self.grid.remove_row(5)

        if self.exact_check.get_active():
            self.pl.ex_flag = True
        else:
            self.pl.ex_flag = False

        if self.kutta_check.get_active():
            self.pl.kutta_flag = True
        else:
            self.pl.kutta_flag = False

        if self.eul_check.get_active():
            self.pl.eul_flag = True
        else:
            self.pl.eul_flag = False

        if self.imp_check.get_active():
            self.pl.imp_flag = True
        else:
            self.pl.imp_flag = False

        # check if method is chosen
        if not self.pl.imp_flag and not self.pl.kutta_flag and not self.pl.eul_flag:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                       Gtk.ButtonsType.OK, "You should choose at least one method")
            dialog.format_secondary_text(
                "No methods are chosen")
            dialog.run()
            dialog.destroy()
            return

        # user input (some bad code style, need to create function for checking)
        try:
            x0 = float(self.x_entry.get_text())
        except ValueError:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                       Gtk.ButtonsType.OK, "Wrong initial x")
            dialog.format_secondary_text(
                "Your initial x is not a number")
            dialog.run()
            dialog.destroy()
            return

        try:
            y0 = float(self.y_entry.get_text())
        except ValueError:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                       Gtk.ButtonsType.OK, "Wrong initial y")
            dialog.format_secondary_text(
                "Your initial y is not a number")
            dialog.run()
            dialog.destroy()
            return

        try:
            bound = float(self.bound.get_text())
        except ValueError:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                       Gtk.ButtonsType.OK, "Wrong x bound")
            dialog.format_secondary_text(
                "Your x bound is not a number")
            dialog.run()
            dialog.destroy()
            return

        try:
            step = float(self.step.get_text())
        except ValueError:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                       Gtk.ButtonsType.OK, "Wrong step")
            dialog.format_secondary_text(
                "Your step is not a number")
            dialog.run()
            dialog.destroy()
            return

        try:
            step_bound = float(self.grid_bound.get_text())
        except ValueError:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                       Gtk.ButtonsType.OK, "Wrong step bound")
            dialog.format_secondary_text(
                "Your step bound is not a number")
            dialog.run()
            dialog.destroy()
            return

        equation = str(self.equation.get_text())

        self.pl.init_methods(x0, y0, bound, step, equation)
        self.pl.plot_graph()
        self.canvas = FigureCanvas(self.pl.fig)
        self.canvas.show()

        self.toolbar.canvas = self.canvas
        self.toolbar.show()

        if self.error_flag:
            self.pl.init_global(x0, y0, bound, step, step_bound, equation)
            self.pl.plot_global()
            self.gl_canvas = FigureCanvas(self.pl.fig_global)
            self.gl_canvas.show()
        else:
            self.pl.init_gl_error()
            self.pl.plot_gll_err()
            self.gl_canvas = FigureCanvas(self.pl.fig_gl_err)
            self.gl_canvas.show()

        self.grid.attach(self.canvas, 2, 4, 3, 4)
        self.grid.attach(self.gl_canvas, 5, 4, 3, 4)
        self.show_all()


window = MainWindow()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()
