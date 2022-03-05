from common.common import Cell

class Board:
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
        for r in self.grid:
            copy.grid.append(r.copy())
        # copy.grid = self.grid.copy()
        return copy