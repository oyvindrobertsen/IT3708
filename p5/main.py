from __future__ import print_function, division

import sys

from flatland import Flatland, FlatlandQLearn
from gui import FlatlandGUI

SCENARIOS = (
    '1-simple.txt',
    '2-still-simple.txt',
    '3-dont-be-greedy.txt',
    '4-big-one.txt',
    '5-even-bigger.txt'
)


def parse_flatland_scenario(filename):
    with open('scenarios/' + filename) as f:
        w, h, x, y, n = map(int, f.readline().split(' '))
        grid = []
        for line in f:
            grid.append(list(map(int, line.split(' '))))
        return Flatland((w, h), x, y, n, grid)

if __name__ == "__main__":
    filename = SCENARIOS[2]
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    flatland = parse_flatland_scenario(filename)

    flq = FlatlandQLearn(
        k=1000,
        scenario=flatland,
        learning_rate=0.5,
        discount_rate=0.8,
        temp=1,
        # x=3
    )

    actions, states = flq.learn()
    #FlatlandGUI(flatland, actions, states, flq.q)
    #flq.plot_steps()