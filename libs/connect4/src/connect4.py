from enum import Enum
import numpy as np

WIDTH = 7
HEIGHT = 6

class Result(Enum):
    WIN_P1 = 1
    WIN_P2 = 2
    DRAW   = 3


class Board:
    def __init__(self):
        self.state = np.zeros((HEIGHT, WIDTH))
        self.p1_turn = True


    # Add a piece to the given column
    def move(self, move: int) -> bool:
        if not self.check_legal(move):
            return False

        for i in range(1, HEIGHT + 1):
            if self.state[HEIGHT - i, move] == 0:
                self.state[HEIGHT - i, move] = 1 if self.p1_turn else -1
                self.p1_turn = not self.p1_turn
                return True


    # Check if a given move is legal on the current board
    def check_legal(self, move: int) -> bool:
        return move >= 0 and move < WIDTH and self.state[0, move] == 0


    # Check if the game is over due to the previous move, and report the result if it is
    def check_over(self, last_move: int) -> Result:
        # Find the coordinate of the last move and the value of the piece
        y = 0
        player = 0

        for i in range(HEIGHT):
            if self.state[i, last_move] != 0:
                y = i
                player = self.state[i, last_move]

        won = False
        # Scan horizontal
        if check_slice(self.state[y, :], player):
            won = True

        # Scan vertical
        elif check_slice(self.state[:, last_move], player):
            won = True

        # Scan diagonals
        elif check_slice(np.diagonal(self.state, last_move - y), player):
            won = True

        elif check_slice(np.diagonal(self.state, last_move + y), player):
            won = True
            
        if won:
            return Result.WIN_P1 if player == 1 else Result.WIN_P2
        else:
            return False if 0 in self.state else Result.DRAW


# Given a slice of the game state (a row, column, or diagonal)
# Check if there are 4 pieces in a row for the given player
def check_slice(slice, player) -> bool:
    if len(slice) < 4:
        return False
    
    cons = 0

    for piece in slice:
        if piece == player:
            cons += 1

            if cons == 4:
                return True

    return False