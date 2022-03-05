from entity.game import Game
from common import constants
import time

class Node:
    def __init__(self, game: Game) -> None:
        self.game = game
        self.parent = None
        self.children = []

    def set_parent(self, p):
        self.parent = p
    
    def add_child(self, c):
        self.children.append(c)

class Tree:
    def __init__(self, r: Node) -> None:
        self.root = r
        self.queue = [r]

    def BFS(self):
        while len(self.queue) > 0:
            current = self.queue.pop(0)
            # print("curr:")
            # current.game.print_board()
            for dir in constants.DIRECTIONS:
                if not current.game.valid_move(dir):
                    continue
                # time.sleep(1)
                
                child = Node(current.game.clone())
                child.set_parent(current)
                child.game.slide(dir)
                current.add_child(child)

                # print(dir, "---")
                # child.game.print_board()

                if child.game.score >= 8:
                    self.queue = []
                    print("solution: ", child.game.all_moves())
                    return child.game
                elif child.game.state == constants.GAME_OVER:
                    pass
                else:
                    self.queue.append(child)

        return self.root.game
