import os.path
import sys
import time
from entity.tree import Tree
from common import constants, common
from entity.game import Game

input_text = []

if len(sys.argv) != 3:
    sys.exit('ERROR: invalid number of arguments')

if not os.path.exists(sys.argv[1]):
    sys.exit('ERROR: input filedoes not exist')

with open(sys.argv[1]) as file:
    input_text = file.readlines()

def main():
    if len(input_text) == 0:
        sys.exit('ERROR: invalid input file')

    game = Game(int(input_text[0].split(' ')[0]), int(input_text[0].split(' ')[1]))
    for row, elements in enumerate(input_text[1:]):
        game.fill_board(elements=elements[:-1], r=row)

    tree = Tree(game)
    game = tree.BFS_best_first()

    with open(sys.argv[2], 'w') as file:
        file.write("".join((map(str, game.all_moves()))) + '\n')
        file.write(str(game.score) + '\n')
        for r, row in enumerate(game.board.layout()):
            s = ""
            for c, col in enumerate(row):
                if game.state == constants.GAME_OVER:
                    if r == game.pengu_death_x and c == game.pengu_death_y:
                        s += common.Cell.death.value
                    else:
                        s += col.value
                else:
                    if r == game.pengu_x and c == game.pengu_y:
                        s += common.Cell.pengu.value
                    else:
                        s += col.value
            s += '\n'
            file.write(s)

if __name__ == "__main__":
    main()