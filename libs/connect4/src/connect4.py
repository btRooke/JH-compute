import numpy as np

WIDTH = 7
HEIGHT = 6

class Board:
    def __init__(self):
        self.state = np.zeros((HEIGHT, WIDTH))
        self.p1_turn = True


    def move(self, move: int) -> bool:
        if not self.check_legal(move):
            return False

        for i in range(HEIGHT):
            if self.state[HEIGHT - i, move] == 0:
                self.state[HEIGHT - i, move] = 1 if self.p1_turn else -1
                self.p1_turn = not self.p1_turn
                return True


    def check_legal(self, move: int):
        return move >= 0 and move < WIDTH and self.state[0, move]


    def check_over(self, last_move: int):
        # Find the coordinate of the last move and the value of the piece
        y = 0
        player = 0

        for i in range(HEIGHT):
            if self.state[i, last_move] != 0:
                y = i
                player = self.state[i, last_move]

        # Scan left-right
        row = self.state[y, max(0, last_move - 3):min(WIDTH, last_move + 4)]

        if check_slice(row, player):
            return True

        # Scan top-bottom
        # This can only be an end state when the y-coordinate of the last piece was > 2
        if y > 2:
            col = self.state[(y - 3):(y + 1), last_move]

            if check_slice(col, player):
                return True

        # Scan topleft-bottomright
        diag = [
            self.state[y + i, last_move + i] for i in range(-3, 4) 
            if (y + i) >= 0 and (y + i) < HEIGHT and (last_move + i) >= 0 and (last_move + i) < WIDTH
        ]

        if check_slice(diag, player):
            return True

        # Scan bottomleft-topright
        diag = [
            self.state[y - i, last_move + i] for i in range(-3, 4) 
            if (y + i) >= 0 and (y + i) < HEIGHT and (last_move + i) >= 0 and (last_move + i) < WIDTH
        ]

        if check_slice(diag, player):
            return True

        return False

# Given a slice of the game state (a row, column, or diagonal)
# Check if there are 4 pieces in a row for the given player
def check_slice(slice, player):
    cons = 0
    for piece in slice:
        if piece == player:
            cons += 1

            if cons == 4:
                return True

    return False