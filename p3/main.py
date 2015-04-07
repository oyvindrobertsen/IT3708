from __future__ import print_function, division
from flatland import FlatlandProblem
from gui import flatland_gui

if __name__ == "__main__":
    W, H = (10, 10)
    F, P = 0.25, 0.25

    flatland = FlatlandProblem(W, H, F, P)

    flatland_gui(flatland)
