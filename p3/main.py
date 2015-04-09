from __future__ import print_function, division
from flatland import EvoFlatland
from gui import flatland_gui

if __name__ == "__main__":
    layers = [6, 4, 3]
    bias = {}
    evo_flatland = EvoFlatland(8, layers, bias)
