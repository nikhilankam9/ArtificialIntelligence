from http.client import FOUND
from entity.board import Location
from entity.game import Game
from common import constants
import time
from common.common import Cell

class Tree:
    def __init__(self, r: Game) -> None:
        self.root = r
        self.queue = [[]]
        self.cache = {}

    def BFS(self):
        px = self.root.pengu_x
        py = self.root.pengu_y
        while len(self.queue) > 0:
            moves = self.queue.pop(0)
            child = self.root
            # s = time.time()
            for dir in constants.DIRECTIONS:
                ll = moves.copy()
                ll.append(dir)

                changes = []
                for d in ll:
                    changes += child.slide(d)

                if child.score >= 20:
                    self.queue = []
                    print("solution: ", child.all_moves())
                    return child
                
                if child.state == constants.GAME_OVER or child.state == constants.INVALID:
                    pass
                else:
                    # print(child.score, ll)
                    # if Location(child.pengu_x, child.pengu_y) not in self.cache:
                        # self.cache[Location(child.pengu_x, child.pengu_y)] = True
                        # self.queue.append(ll)
                    self.queue.append(ll)
                
                child.pengu_death_x = -1
                child.pengu_death_y = -1
                child.pengu_x = px
                child.pengu_y = py
                child.score  = 0
                child.moves = []
                child.state = 0
                for c in changes:
                    child.board.grid[c[0]][c[1]] = Cell.ice_with_fish
            # e = time.time()
            # print(e -s)
                    
        return self.root
