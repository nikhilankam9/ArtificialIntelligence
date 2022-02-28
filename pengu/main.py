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
    wall = '#'
    ice = ' '
    ice_with_fish = '*' 
    snow = '0'
    pengu = 'P'
    bear = 'U'
    shark = 'S'
    death = 'X'
    empty = ''

inputTxt = []

if len(sys.argv) != 3:
    sys.exit('ERROR: invalid number of arguments')

if not os.path.exists(sys.argv[1]):
    sys.exit('ERROR: input filedoes not exist')

with open(sys.argv[1]) as file:
    inputTxt = file.readlines()

class Game:
    state = BEGIN
    score = 0
    total_fish = 0
    moves = []

    def __init__(self, r, c) -> None:
        self.row = r
        self.col = c
        self.board = [[Cell.empty for _ in range(c)] for _ in range(r)]
        self.directions = {1: [1, -1], 2: [1,  0], 3: [1,  1], 4: [0, -1], 6: [0,  1], 7: [-1, -1], 8: [-1,  0], 9: [-1,  1]}

    def fillBoard(self, elements: str, row: int) -> None:
        for col, element in enumerate(elements):
            self.board[row][col] = Cell(element)
            if self.board[row][col] == Cell.pengu:
                self.board[row][col] = Cell.ice #pengu always starts on ice
                self.penguX = row
                self.penguY = col
            if Cell(element) == Cell.ice_with_fish:
                self.total_fish += 1

    def play(self):
        iterator = 6
        while iterator > 0:
            move = self.nextValidRandomMove()
            # print("move: ", move)
            self.moves.append(move)
            self.slide(move)

            if self.state == VICTORY or self.state == GAME_OVER:
                break
            iterator -= 1

    def slide(self, direction: int) -> None:
        while True:
            # self.printBoard()
            # time.sleep(1)
            if self.nextCell(direction) == Cell.wall:
                break

            elif self.nextCell(direction) == Cell.ice_with_fish:
                self.score += 1
                if self.score == self.total_fish:
                    self.state = VICTORY
                self.updateNextCell(direction, Cell.ice)
                self.movePengu(direction)

            elif self.nextCell(direction) == Cell.ice:
                self.movePengu(direction)
                
            elif self.nextCell(direction) == Cell.bear or self.nextCell(direction) == Cell.shark:
                self.state = GAME_OVER
                self.movePengu(direction)
                self.recordPenguDeath()
                break

            elif self.nextCell(direction) == Cell.snow:
                self.movePengu(direction)
                break

    def nextValidRandomMove(self) -> int:
        availableDirections = DIRECTIONS.copy()
        c = random.choice(availableDirections)
        while self.nextCell(c) == Cell.wall:
            availableDirections.remove(c)
            c = random.choice(availableDirections)
        return c

    # helper functions
    # return the element in the next cell
    def nextCell(self, direction: int):
        return self.board[self.penguX + self.directions[direction][0]][self.penguY + self.directions[direction][1]]

    def updateNextCell(self, direction: int, toCell: Cell):
        self.board[self.penguX + self.directions[direction][0]][self.penguY + self.directions[direction][1]] = toCell

    def movePengu(self, direction: int):
        self.penguX += self.directions[direction][0]
        self.penguY += self.directions[direction][1]

    def all_moves(self):
        return self.moves

    def recordPenguDeath(self):
        self.penguDeathX = self.penguX
        self.penguDeathY = self.penguY

    def penguLocation(self):
        return self.penguX, self.penguY

    # utility functions
    def info(self) -> None:
        print("Rows:", self.row)
        print("Columns:", self.col)
        self.printBoard()

    def printBoard(self) -> None:
        print("------------")
        for r, row in enumerate(self.board):
            for c, col in enumerate(row):
                if self.state == GAME_OVER:
                    if r == self.penguDeathX and c == self.penguDeathY:
                        print(Cell.death.value, end=",")
                    else:
                        print(col.value, end=",")
                else:
                    if r == self.penguX and c == self.penguY:
                        print(Cell.pengu.value, end=",")
                    else:
                        print(col.value, end=",")
            print()
        print("------------")

def main():
    if len(inputTxt) == 0:
        sys.exit('ERROR: invalid input file')

    game = Game(int(inputTxt[0].split(' ')[0]), int(inputTxt[0].split(' ')[1]))
    for row, elements in enumerate(inputTxt[1:]):
        game.fillBoard(elements=elements[:-1], row= row)

    game.play()
    # print(game.all_moves())
    # game.printBoard()

    with open(sys.argv[2], 'w') as file:
        file.write("".join((map(str, game.all_moves()))) + '\n')
        file.write(str(game.score) + '\n')
        for r, row in enumerate(game.board):
            s = ""
            for c, col in enumerate(row):
                if game.state == GAME_OVER:
                    if r == game.penguDeathX and c == game.penguDeathY:
                        s += Cell.death.value
                    else:
                        s += col.value
                else:
                    if r == game.penguX and c == game.penguY:
                        s += Cell.pengu.value
                    else:
                        s += col.value
            s += '\n'
            file.write(s)

if __name__ == "__main__":
    main()