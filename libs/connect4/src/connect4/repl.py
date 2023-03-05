from player import Player
from connect4 import Board, Result
import trainer

if __name__ == "__main__":
    opponent = Player("opponent")
    opp_turn = False

    board = Board()

    while True:
        print(board.state)

        if opp_turn:
            # Don't use any randomness - we want to see what the models can do by themselves
            action = opponent.act(board, 0)

        else:
            action = int(input("Enter a move: "))

            while not board.move(action):
                action = int(input("Enter a move: "))
                
        opp_turn = not opp_turn
        victory_state = board.check_over(action)

        if victory_state:
            if victory_state == Result.WIN_P1:
                print("You won!")

            elif victory_state == Result.WIN_P2:
                print("The AI won!")

            else:
                print("Draw")
                
            break
