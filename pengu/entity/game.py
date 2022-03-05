import random
from common import constants, common

class Board:
    def __init__(self, r, c) -> None:
        self.row = r
        self.col = c
        self.grid = [[common.Cell.empty for _ in range(c)] for _ in range(r)]

class Game:
    """Game class: Defines the game pengu and enables playing it.
    """
    state = constants.BEGIN
    score = 0
    total_fish = 0
    moves = []

    def __init__(self, r, c) -> None:
        self.row = r
        self.col = c
        self.board = [[common.Cell.empty for _ in range(c)] for _ in range(r)]
        self.directions = {1: [1, -1], 2: [1,  0], 3: [1,  1], 4: [0, -1], 6: [0,  1], 7: [-1, -1], 8: [-1,  0], 9: [-1,  1]}

    def fill_board(self, elements: str, row: int) -> None:
        """Function to populate the data from the input file

        Args:
            elements (str): text from a single row parsed from input file
            row (int): number of the row
        """
        for col, element in enumerate(elements):
            self.board[row][col] = common.Cell(element)
            if self.board[row][col] == common.Cell.pengu:
                self.board[row][col] = common.Cell.ice #pengu always starts on ice
                self.pengu_x = row
                self.pengu_y = col
            if common.Cell(element) == common.Cell.ice_with_fish:
                self.total_fish += 1

    def play(self):
        iterator = 6
        while iterator > 0:
            move = self.next_valid_random_move()
            self.moves.append(move)
            self.slide(move)

            if self.state == constants.VICTORY or self.state == constants.GAME_OVER:
                break
            iterator -= 1

    def slide(self, direction: int) -> None:
        """Implements the slide action

        Args:
            direction (int): encoded direction
        """
        while True:
            if self.next_cell(direction) == common.Cell.wall:
                break

            elif self.next_cell(direction) == common.Cell.ice_with_fish:
                self.score += 1
                if self.score == self.total_fish:
                    self.state = constants.VICTORY
                self.update_next_cell(direction, common.Cell.ice)
                self.move_pengu(direction)

            elif self.next_cell(direction) == common.Cell.ice:
                self.move_pengu(direction)
                
            elif self.next_cell(direction) == common.Cell.bear or self.next_cell(direction) == common.Cell.shark:
                self.state = constants.GAME_OVER
                self.move_pengu(direction)
                self.record_pengu_death()
                break #no sliding corpses

            elif self.next_cell(direction) == common.Cell.snow:
                self.move_pengu(direction)
                break

    def next_valid_random_move(self) -> int:
        """Generates the next valid random move

        Returns:
            int: encoded direction value
        """
        available_directions = constants.DIRECTIONS.copy()
        c = random.choice(available_directions)
        while self.next_cell(c) == common.Cell.wall:
            available_directions.remove(c)
            c = random.choice(available_directions)
        return c

    # helper functions
    def next_cell(self, direction: int) -> common.Cell:
        """Helper function to check the element if a move is made in the 'direction'

        Args:
            direction (int): encoded direction

        Returns:
            Cell: Human readable representation of the board element
        """
        return self.board[self.pengu_x + self.directions[direction][0]][self.pengu_y + self.directions[direction][1]]

    def update_next_cell(self, direction: int, toCell: common.Cell):
        self.board[self.pengu_x + self.directions[direction][0]][self.pengu_y + self.directions[direction][1]] = toCell

    def move_pengu(self, direction: int):
        self.pengu_x += self.directions[direction][0]
        self.pengu_y += self.directions[direction][1]

    def all_moves(self):
        return self.moves

    def record_pengu_death(self):
        self.pengu_death_x = self.pengu_x
        self.pengu_death_y = self.pengu_y

    def pengu_location(self):
        return self.pengu_x, self.pengu_y

    # utility functions
    def info(self) -> None:
        print("Rows:", self.row)
        print("Columns:", self.col)
        self.print_board()

    def print_board(self) -> None:
        for r, row in enumerate(self.board):
            for c, col in enumerate(row):
                if self.state == constants.GAME_OVER:
                    if r == self.pengu_death_x and c == self.pengu_death_y:
                        print(common.Cell.death.value, end=",")
                    else:
                        print(col.value, end=",")
                else:
                    if r == self.pengu_x and c == self.pengu_y:
                        print(common.Cell.pengu.value, end=",")
                    else:
                        print(col.value, end=",")
            print()
        print()