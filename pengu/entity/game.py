import random
from entity.board import Board
from common import constants
from common.common import Cell
import time

class Game:
    """Game class: Defines the game pengu and enables playing it.
    """
    state = constants.BEGIN
    score = 0
    total_fish = 0
    moves = []
    pengu_x = -1
    pengu_y = -1
    pengu_death_x = -1
    pengu_death_y = -1

    def __init__(self, r, c) -> None:
        self.row = r
        self.col = c
        self.board = Board(r, c)

    def clone(self):
        """Clone the game object
        Returns:
            Game: Cloned game object
        """
        copy = Game(self.row, self.col)
        copy.score = self.score
        copy.total_fish = self.total_fish
        copy.moves = self.moves.copy()
        copy.board = self.board.clone()
        copy.state = self.state
        copy.pengu_x = self.pengu_x
        copy.pengu_y = self.pengu_y
        copy.pengu_death = self.pengu_death_x
        copy.pengu_death_y = self.pengu_death_y
        return copy


    def fill_board(self, elements: str, r: int) -> None:
        """Function to populate the data from the input file
        Args:
            elements (str): text from a single row parsed from input file
            r (int): number of the row
        """
        col_cells = []
        for c, element in enumerate(elements):
            col_cells.append(Cell(element))
            if Cell(element) == Cell.pengu:
                col_cells[c] = Cell.ice #pengu always starts on ice
                self.pengu_x = r
                self.pengu_y = c
            if Cell(element) == Cell.ice_with_fish:
                self.total_fish += 1
        
        self.board.grid.append(col_cells)

    def play(self):
        list = [8, 6, 2, 4]
        self.print_board()
        for move in list:
            time.sleep(1)
            self.slide(move)
            self.print_board()

    def slide(self, direction: int):
        """Implements the slide action for the pengu
        Args:
            direction (int): encoded direction
        Returns:
            List: Returns the locations of the fish that the pengu gathered by moving the direction.
        """
        self.moves.append(direction)
        gatheredFishLoc = []
        if not self.valid_move(direction):
            self.state = constants.INVALID
            return gatheredFishLoc

        while True:
            if self.next_cell(direction) == Cell.wall:
                break

            elif self.next_cell(direction) == Cell.ice_with_fish:
                self.score += 1
                if self.score == self.total_fish:
                    self.state = constants.VICTORY
                self.update_next_cell(direction, Cell.ice)
                d = constants.DIRECTION_INDICES[direction]
                gatheredFishLoc.append([self.pengu_x + d[0], self.pengu_y + d[1]])
                self.move_pengu(direction)

            elif self.next_cell(direction) == Cell.ice:
                self.move_pengu(direction)
                
            elif self.next_cell(direction) == Cell.bear or self.next_cell(direction) == Cell.shark:
                self.state = constants.GAME_OVER
                self.move_pengu(direction)
                self.record_pengu_death()
                break #no sliding corpses

            elif self.next_cell(direction) == Cell.snow:
                self.move_pengu(direction)
                break
        
        return gatheredFishLoc

    def next_valid_random_move(self) -> int:
        """Generates the next valid random move
        Returns:
            int: encoded direction value
        """
        available_directions = constants.DIRECTIONS.copy()
        c = random.choice(available_directions)
        while self.valid_move(c) :
            available_directions.remove(c)
            c = random.choice(available_directions)
        return c

    def valid_move(self, dir: int) -> bool:
        if self.next_cell(dir) == Cell.wall:
            return False
        return True

    # helper functions
    def next_cell(self, direction: int) -> Cell:
        """Helper function to check the element if a move is made in the 'direction'
        Args:
            direction (int): encoded direction
        Returns:
            Cell: Human readable representation of the board element
        """
        d = constants.DIRECTION_INDICES[direction]
        return self.board.get(self.pengu_x + d[0], self.pengu_y + d[1])

    def update_next_cell(self, direction: int, toCell: Cell):
        """Updates the next cell of the game board
        Args:
            direction (int): encoded direction
            toCell (Cell): The value that is updated to.
        """
        d = constants.DIRECTION_INDICES[direction]
        self.board.update(self.pengu_x + d[0], self.pengu_y + d[1], toCell)

    def move_pengu(self, direction: int):
        """Make the pengu move one step in the given direction
        Args:
            direction (int): encoded direction
        """
        d = constants.DIRECTION_INDICES[direction]
        self.pengu_x += d[0]
        self.pengu_y += d[1]

    def all_moves(self):
        """All the moves that the pengu made up until now
        Returns:
            List: Moves
        """
        return self.moves

    def record_pengu_death(self):
        self.pengu_death_x = self.pengu_x
        self.pengu_death_y = self.pengu_y

    def pengu_location(self):
        return self.pengu_x, self.pengu_y

    def reset(self, changes, px, py):
        self.pengu_death_x = -1
        self.pengu_death_y = -1
        self.pengu_x = px
        self.pengu_y = py
        self.score  = 0
        self.moves = []
        self.state = constants.BEGIN
        for c in changes:
            self.board.grid[c[0]][c[1]] = Cell.ice_with_fish

    # utility functions
    def info(self) -> None:
        print("Rows:", self.row)
        print("Columns:", self.col)
        self.print_board()

    def print_board(self) -> None:
        for r, row in enumerate(self.board.layout()):
            for c, col in enumerate(row):
                if self.state == constants.GAME_OVER:
                    if r == self.pengu_death_x and c == self.pengu_death_y:
                        print(Cell.death.value, end=",")
                    else:
                        print(col.value, end=",")
                else:
                    if r == self.pengu_x and c == self.pengu_y:
                        print(Cell.pengu.value, end=",")
                    else:
                        print(col.value, end=",")
            print()
        print()