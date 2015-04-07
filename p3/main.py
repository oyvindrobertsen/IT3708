from __future__ import print_function, division
from flatland import gen_flatland
from gui import flatland_gui

if __name__ == "__main__":
    W, H = (10, 10)
    F, P = 0.25, 0.25

    flatland = gen_flatland(W, H, F, P)

    print(*flatland, sep='\n')

    flatland_gui(flatland)