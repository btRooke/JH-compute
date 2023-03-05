from player import Player
from connect4 import Board, Result
import trainer

if __name__ == "__main__":
    # Train a model
    player1 = Player()
    player2 = Player()

    print("Training")
    trainer.train(1000, player1, player2, 0.9998)

    print("Competing")
    wins = trainer.compete(100, player1, player2)

    print(wins)
    opponent = player1 if wins[0] > wins[1] else player2
    opp_turn = False

    # Play against it
    board = Board()

    while True:
        if opp_turn:
            # Don't use any randomness - we want to see what the models can do by themselves
            action = opponent.act(board, 0)

        else:
            action = input("Enter a move: ")

            while not board.move(action):
                action = input("Enter a move: ")
                
        victory_state = board.check_over(action)

        if victory_state:
            if victory_state == Result.WIN_P1:
                print("You won!")

            elif victory_state == Result.WIN_P2:
                print("The AI won!")

            else:
                print("Draw")
                
            break
