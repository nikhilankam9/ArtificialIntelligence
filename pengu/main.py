import os.path
import sys

WALL = '#'
ICE = ' '
ICE_WITH_FISH = '*'
SNOW = '0'
PENGU = 'P'
BEAR = 'U'
SHARK = 'S'

inputTxt = []

if len(sys.argv) != 3:
    sys.exit('ERROR: invalid number of arguments')

if not os.path.exists(sys.argv[1]):
    sys.exit('ERROR: input filedoes not exist')

with open(sys.argv[1]) as file:
    inputTxt = file.readlines()

class Game:
    def __init__(self, r, c) -> None:
        self.row = r
        self.col = c
        self.board = [[' ' for c1 in range(c)] for r1 in range(r)]

    def fillBoard(self, elements: str, row: int) -> None:
        for col, element in enumerate(elements):
            self.board[row][col] = element

    def info(self) -> None:
        print("Rows:", self.row)
        print("Columns:", self.col)
        for row in self.board:
            print(row)

def main():
    if len(inputTxt) == 0:
        sys.exit('ERROR: invalid input file data')

    game = Game(int(inputTxt[0].split(' ')[0]), int(inputTxt[0].split(' ')[1]))
    for row, elements in enumerate(inputTxt[1:]):
        game.fillBoard(elements=elements[:-1], row= row)

    game.info()

#test add 


if __name__ == "__main__":
    main()