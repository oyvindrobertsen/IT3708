from __future__ import division, print_function
from beer_tracker import BeerTrackerWorld

from gui import BeerTrackerGUI
from enums import *


if __name__ == "__main__":
    btw = BeerTrackerWorld(30, 15, wrap=True)
    btw.new_falling_object()
    btw.terminal_print()
    BeerTrackerGUI(btw, actions=[
        (LEFT, 4),
        (LEFT, 1),
        (PULL, None)
    ])