from re import X
from common.common import Cell

class Location:
    """Class to define the location i.e position of a game element.
    """
    def __init__(self, x, y) -> None:
        x = x
        y = y

class Board:
    """Class to define the grid structure of the game.
    """
    def __init__(self, r, c) -> None:
        self.row = r
        self.col = c
        self.grid = []

    def update(self, r, c, element):
        self.grid[r][c] = Cell(element)

    def get(self, r, c) -> Cell:
        return self.grid[r][c]

    def layout(self):
        return self.grid

    def clone(self):
        copy = Board(self.row, self.col)
        copy.grid = [row[:] for row in self.grid]
        return copy