from entity.game import Game
from common import constants
import time
from common.common import Cell

class Tree:
    def __init__(self, r: Game) -> None:
        self.root = r
        self.queue = [[]]

    def BFS(self):
        while len(self.queue) > 0:
            moves = self.queue.pop(0)
            for dir in constants.DIRECTIONS:
                child = self.root.clone()

                ll = moves.copy()
                ll.append(dir)

                for d in ll:
                    child.slide(d)

                if child.score >= 8:
                    self.queue = []
                    print("solution: ", child.all_moves())
                    return child
                elif child.state == constants.GAME_OVER or child.state == constants.INVALID:
                    pass
                else:
                    self.queue.append(ll)
        return self.root