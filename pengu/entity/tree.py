from entity.board import Location
from entity.game import Game
from common import constants
from common.common import Cell

class Tree:
    """Class to define the game tree i.e the possible states of the game 
    """
    def __init__(self, r: Game) -> None:
        """Initialize the tree object, a game object is required to init.

        Args:
            r (Game): The initial state of the game is considered as the root.
        """
        self.root = r
        self.queue = [[]] # FIFO queue for BFS implementation

    def BFS(self):
        """BFS implementation where each queue element is the sequence of moves. 

        Returns:
            Game: Game state that acheived the desired result.
        """
        px = self.root.pengu_x
        py = self.root.pengu_y
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
                child.pengu_x = px
                child.pengu_y = py
                child.score  = 0
                child.moves = []
                child.state = constants.BEGIN
                for c in changes:
                    child.board.grid[c[0]][c[1]] = Cell.ice_with_fish
                    
        return self.root
