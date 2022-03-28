from entity.board import Location
from entity.game import Game
from common import constants
from common.common import Cell
import heapq as pq
import time

# References: https://stackoverflow.com/a/8875823/7434711

class TreePQNode:
    """Class to hold moves and score as the tree node.
    """
    def __init__(self, moves, score) -> None:
        """Initialize class with moves and score

        Args:
            moves (list): list of moves
            score (int): score obtained from the moves
        """
        self.moves = moves.copy()
        self.score = score

class Tree:
    """Class to define the game tree i.e the possible states of the game 
    """
    def __init__(self, r: Game, heuristic=lambda x: -x) -> None:
        """Initialize the tree object, a game object is required to init.

        Args:
            r (Game): The initial state of the game is considered as the root.
            heuristic=lambda x: -x: Heuristic to return the largest priority element.

            priority_queue is used to leverage the heapq python library.

        """
        self.root = r

        self.heuristic = heuristic
        self.index = 0 #To avoid clashes when the evaluated key value is a draw and the stored value is not directly comparable
        self.priority_queue = []
        self.pq_push(TreePQNode([], 0))

        self.px = r.pengu_x
        self.py = r.pengu_y
        self.queue = [[]] # FIFO queue for BFS implementation
        self.stack = [[]] # FILO stack for DFS implementation

    def pq_push(self, tree_node: TreePQNode):
        """Wrapper function to abstract heappush operation.
        It pushes an tree node to the priority_queue using the current achieved score as the priority
        i.e the path that leads to highest score is given highest score.

        self.index: Autoincrement integer to value to avoid clashes when the heap element is not comparable.

        Args:
            tree_node (TreePQNode): Tree node that holds the current sequence of moves along with the score achieved.
        """
        pq.heappush(self.priority_queue, (self.heuristic(tree_node.score), self.index, tree_node))
        self.index += 1 # auto-increment index

    def pq_pop(self):
        """Wrapper function to abstract heappop operation.
        It pops the tree node with highest priority(score) and returns the equivalent tree node.

        Returns:
            TreePQNode: Tree node with the highest priority.
        """
        return pq.heappop(self.priority_queue)[2]

    def BFS_best_first(self):
        """Greedy best first search
        The greedy property in this algorithm is that the highest score achieved by doing the possible 8 moves
        yeilds the better solution.

        Pruning: Only valid(pengu state changes) moves and moves that already did not end in a GAME_OVER state are considered.

        Returns:
            Game: Returns the game state that achieved the desired result.
        """
        while len(self.priority_queue) > 0:
            curr = self.pq_pop()
            child = self.root
            for dir in constants.DIRECTIONS:
                ll = curr.moves.copy()
                ll.append(dir)

                changes = []
                for d in ll:
                    changes += child.slide(d)

                if child.score >= 20:
                    print("solution: ", child.all_moves(), child.score)
                    return child
                
                if child.state == constants.GAME_OVER or child.state == constants.INVALID:
                    pass
                else:
                    # print(child.all_moves(), child.score)
                    self.pq_push(TreePQNode(child.all_moves(), child.score))
                
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
                self.root


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
