from enum import Enum
import math


class Move(Enum):
    up = -6
    left = -1
    right = 1
    down = 6

    def can_move(self, index):
        row = math.floor(index / 6)

        if index < 0 or index > 29:
            return False

        if self == Move.right and index == 0:
            return True
        if self == Move.left and index % 6 == 0:
            return False
        if self == Move.right and ((index - (0 if index % 6 == 0 else row)) % 5 == 0):
            return False
        if self == Move.up and index <= 5:
            return False
        if self == Move.down and index >= 24:
            return False

        return True
     
    def position(self):

        if self == Move.right:
            return (0, 1)
        if self == Move.left:
            return (0,-1)
        if self == Move.up:
            return (-1, 0)
        if self == Move.down:
            return (1, 0)

        return (0, 0)
    def calc_position(self, index):
        column = index % 6
        row = math.floor(index/6)
        r, c = self.position()
        column += c
        row += r
        index = row*6 + column
        #print(f"c, r: {c}, {r}")
        #print(f"index: {index}")
        #print(f"col: {column}")
        #print(f"row: {row}")
        return index, column, row

def get_available_moves(index):
    moves = []

    for move in Move:
        if move.can_move(index):
            moves.append(move)

    return moves


if __name__ == "__main__":
    print(get_available_moves(0))
