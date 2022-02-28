import os.path
import sys
import enum
import random
import time

# constants
DIRECTIONS = [1, 2, 3, 4, 6, 7, 8, 9]
BEGIN = "begin"
GAME_OVER = "game_over"
VICTORY = "victory"

class Cell(enum.Enum):
    """Encapsulates the elements in the game to human readable format.
    """
    wall = '#'
    ice = ' '
    ice_with_fish = '*' 
    snow = '0'
    pengu = 'P'
    bear = 'U'
    shark = 'S'
    death = 'X'
    empty = ''

input_text = []

if len(sys.argv) != 3:
    sys.exit('ERROR: invalid number of arguments')

if not os.path.exists(sys.argv[1]):
    sys.exit('ERROR: input filedoes not exist')

with open(sys.argv[1]) as file:
    input_text = file.readlines()

class Game:
    """Game class: Defines the game pengu and enables playing it.
    """
    state = BEGIN
    score = 0
    total_fish = 0
    moves = []

    def __init__(self, r, c) -> None:
        self.row = r
        self.col = c
        self.board = [[Cell.empty for _ in range(c)] for _ in range(r)]
        self.directions = {1: [1, -1], 2: [1,  0], 3: [1,  1], 4: [0, -1], 6: [0,  1], 7: [-1, -1], 8: [-1,  0], 9: [-1,  1]}

    def fill_board(self, elements: str, row: int) -> None:
        """Function to populate the data from the input file

        Args:
            elements (str): text from a single row parsed from input file
            row (int): number of the row
        """
        for col, element in enumerate(elements):
            self.board[row][col] = Cell(element)
            if self.board[row][col] == Cell.pengu:
                self.board[row][col] = Cell.ice #pengu always starts on ice
                self.pengu_x = row
                self.pengu_y = col
            if Cell(element) == Cell.ice_with_fish:
                self.total_fish += 1

    def play(self):
        iterator = 6
        while iterator > 0:
            move = self.next_valid_random_move()
            self.moves.append(move)
            self.slide(move)

            if self.state == VICTORY or self.state == GAME_OVER:
                break
            iterator -= 1

    def slide(self, direction: int) -> None:
        """Implements the slide action

        Args:
            direction (int): encoded direction
        """
        while True:
            if self.next_cell(direction) == Cell.wall:
                break

            elif self.next_cell(direction) == Cell.ice_with_fish:
                self.score += 1
                if self.score == self.total_fish:
                    self.state = VICTORY
                self.update_next_cell(direction, Cell.ice)
                self.move_pengu(direction)

            elif self.next_cell(direction) == Cell.ice:
                self.move_pengu(direction)
                
            elif self.next_cell(direction) == Cell.bear or self.next_cell(direction) == Cell.shark:
                self.state = GAME_OVER
                self.move_pengu(direction)
                self.record_pengu_death()
                break

            elif self.next_cell(direction) == Cell.snow:
                self.move_pengu(direction)
                break

    def next_valid_random_move(self) -> int:
        """Generates the next valid random move

        Returns:
            int: encoded direction value
        """
        available_directions = DIRECTIONS.copy()
        c = random.choice(available_directions)
        while self.next_cell(c) == Cell.wall:
            available_directions.remove(c)
            c = random.choice(available_directions)
        return c

    # helper functions
    def next_cell(self, direction: int) -> Cell:
        """Helper function to check the element if a move is made in the 'direction'

        Args:
            direction (int): encoded direction

        Returns:
            Cell: Human readable representation of the board element
        """
        return self.board[self.pengu_x + self.directions[direction][0]][self.pengu_y + self.directions[direction][1]]

    def update_next_cell(self, direction: int, toCell: Cell):
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
        print("------------")
        for r, row in enumerate(self.board):
            for c, col in enumerate(row):
                if self.state == GAME_OVER:
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
        print("------------")

def main():
    if len(input_text) == 0:
        sys.exit('ERROR: invalid input file')

    game = Game(int(input_text[0].split(' ')[0]), int(input_text[0].split(' ')[1]))
    for row, elements in enumerate(input_text[1:]):
        game.fill_board(elements=elements[:-1], row=row)

    game.play()

    with open(sys.argv[2], 'w') as file:
        file.write("".join((map(str, game.all_moves()))) + '\n')
        file.write(str(game.score) + '\n')
        for r, row in enumerate(game.board):
            s = ""
            for c, col in enumerate(row):
                if game.state == GAME_OVER:
                    if r == game.pengu_death_x and c == game.pengu_death_y:
                        s += Cell.death.value
                    else:
                        s += col.value
                else:
                    if r == game.pengu_x and c == game.pengu_y:
                        s += Cell.pengu.value
                    else:
                        s += col.value
            s += '\n'
            file.write(s)

if __name__ == "__main__":
    main()