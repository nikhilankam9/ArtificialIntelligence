from entity.board import Location
from entity.game import Game
from common import constants
from common.common import Cell
import time

class Tree:
    """Class to define the game tree i.e the possible states of the game 
    """
    def __init__(self, r: Game) -> None:
        """Initialize the tree object, a game object is required to init.

        Args:
            r (Game): The initial state of the game is considered as the root.
        """
        self.root = r
        self.px = r.pengu_x
        self.py = r.pengu_y
        self.queue = [[]] # FIFO queue for BFS implementation
        self.stack = [[]] # FILO stack for DFS implementation

    def DFS_bounded(self, depth: int):
        """DFS implementation with a bound(depth) limit where each stack element is a 
        sequence of moves.

        Args:
            depth (int): Maximum depth of the tree that can be traversed

        Returns:
            Game: Game state that acheived the desired result or None if desired state is
            not reached
        """
        if len(self.stack) == 0:
            self.stack = [[]]

        while len(self.stack) > 0:
            moves = self.stack.pop(-1)
            child = self.root
            changes = []
            for do_move in moves:
                changes += child.slide(do_move)

            if len(moves) == depth:
                if child.score >= 16:
                    self.stack = []
                    print("solution: ", child.all_moves())
                    return child

            if len(moves) <= depth:
                if child.state == constants.GAME_OVER or child.state == constants.INVALID:
                    pass
                else:
                    for dir in constants.DIRECTIONS:
                        if child.valid_move(dir):
                            ll = child.moves.copy()
                            ll.append(dir)
                            # print(depth, len(ll), ll)
                            self.stack.append(ll)

            # revert action
            child.pengu_death_x = -1
            child.pengu_death_y = -1
            child.pengu_x = self.px
            child.pengu_y = self.py
            child.score  = 0
            child.moves = []
            child.state = constants.BEGIN
            for c in changes:
                child.board.grid[c[0]][c[1]] = Cell.ice_with_fish     
        
    def ID_search(self):
        """Iterative deepening search implemention.
        Applies DFS to the game tree with an incremental bound in each iteration

        Returns:
            Game: Game state that acheived the desired result
        """
        bound = 0
        while bound >= 0:
            result_state = self.DFS_bounded(bound)
            if result_state:
                return result_state
            bound += 1
            if bound > 100: # fail safe to avoid infinite loop
                break


    def BFS(self):
        """BFS implementation where each queue element is the sequence of moves. 

        Returns:
            Game: Game state that acheived the desired result.
        """
        while len(self.queue) > 0:
            moves = self.queue.pop(0)
            child = self.root
            for dir in constants.DIRECTIONS:
                ll = moves.copy()
                ll.append(dir)

                changes = []
                for d in ll:
                    changes += child.slide(d)

                if child.score >= 8:
                    self.queue = []
                    print("solution: ", child.all_moves())
                    return child
                
                if child.state == constants.GAME_OVER or child.state == constants.INVALID:
                    pass
                else:
                    self.queue.append(ll)
                
                # revert action
                child.pengu_death_x = -1
                child.pengu_death_y = -1
                child.pengu_x = self.px
                child.pengu_y = self.py
                child.score  = 0
                child.moves = []
                child.state = constants.BEGIN
                for c in changes:
                    child.board.grid[c[0]][c[1]] = Cell.ice_with_fish
                    
        return self.root
