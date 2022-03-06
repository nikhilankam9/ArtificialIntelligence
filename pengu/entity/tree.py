from entity.game import Game
from common import constants
import time
from common.common import Cell

class Tree:
    def __init__(self, r: Game) -> None:
        self.root = r
        self.queue = [[]]

    def BFS(self):
        pengu_loc = self.root.pengu_location()

        while len(self.queue) > 0:
            moves = self.queue.pop(0)
            for dir in constants.DIRECTIONS:
                child = self.root.clone()
                # end = time.time()
                # print("Time consumed in working: ",end - start)
                # time.sleep(1)

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
                    # print(dir, "---", moves)
                    # child.print_board()
                    self.queue.append(ll)



                # # revert action
                # self.root.state = constants.BEGIN
                # self.root.score = 0
                # self.root.moves = []
                # self.root.pengu_x = pengu_loc[0]
                # self.root.pengu_y = pengu_loc[1]
                # self.pengu_death_x = -1
                # self.pengu_death_y = -1
                # for fish in self.root.fishs:
                #     self.root.board.update(fish[0], fish[1], Cell.ice_with_fish)             

                # ll = moves.copy()
                # ll.append(dir)


                # # print(dir, ll)
                # # self.root.print_board()

                # for d in ll:
                #     self.root.slide(d)

                # # print(self.root.state)
                # # self.root.print_board()

                # if self.root.score >= 8:
                #     self.queue = []
                #     print("solution: ", self.root.all_moves())
                #     return self.root
                # elif self.root.state == constants.GAME_OVER or self.root.state == constants.INVALID:
                #     pass
                # else:
                #     self.queue.append(ll)
        return self.root