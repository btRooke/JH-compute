import connect4, argparse, os
import numpy as np
import tensorflow as tf
from tensorflow import keras

from connect4 import Player


class Memory:
    def __init__(self): 
        self.clear()
        
    def add(self, observation, action): 
        self.observations.append(observation)
        self.actions.append(action)

    def clear(self):
        self.observations = []
        self.actions = []


# Train two players against each other for the given number of games
# learning_batch is the number of moves which should be made before applying learning
# epsilon_decay is how quickly the randomness coefficient decreases after each game (typically > 0.999) 
def train(n_games, player1, player2, learning_batch, epsilon_decay):
    keras.backend.set_floatx('float64')

    memory = [Memory(), Memory()]
    epsilon = 1

    for i in range(n_games):
        print(f"Training game {i}")

        board   = connect4.Board()
        p1_turn = True

        reward = [0, 0]

        # Play the game
        while True:
            player = player1 if p1_turn else player2
            player_n = i % 2 == 0

            action = player.act(board, epsilon)
            memory[player_n].add(board.state, action)

            victory_state = board.check_over(action)

            if victory_state:
                # Encourage winning
                if victory_state == connect4.Result.WIN_P1:
                    reward = [1, -1]

                elif victory_state == connect4.Result.WIN_P2:
                    reward = [-1, 1]

                # Slightly discourage draws
                else:
                    reward = [-0.1, -0.1]

                break

        # Train the models once enough moves have been made
        if len(memory[0].actions) >= learning_batch:
            player1.train(
                np.array(memory[0].observations),
                np.array(memory[0].actions),
                reward[0]
            )
            memory[0].clear()

        if len(memory[1].actions) >= learning_batch:
            player2.train(
                np.array(memory[1].observations),
                np.array(memory[1].actions),
                reward[1]
            )
            memory[1].clear()

        # Update exploration probability
        epsilon *= epsilon_decay
            

# Play n games without training, returning the winner
def compete(n_games, player1, player2):
    wins = [0, 0]

    for _ in range(n_games):
        board   = connect4.Board()
        p1_turn = True

        # Play the game
        while True:
            player = player1 if p1_turn else player2

            # Don't use any randomness - we want to see what the models can do by themselves
            action = player.act(board, 0)

            victory_state = board.check_over(action)

            if victory_state:
                if victory_state == connect4.Result.WIN_P1:
                    print("P1 won")
                    wins[0] += 1

                elif victory_state == connect4.Result.WIN_P2:
                    print("P2 won")
                    wins[1] += 1

                else:
                    print("Draw")
                    
                break

    return wins


if __name__ == "__main__":
    tf.get_logger().setLevel('ERROR')

    player1 = Player()
    player2 = Player()

    print("Training")
    train(1000, player1, player2, 100, 0.9998)

    print("Competing")
    wins = compete(250, player1, player2)

    print(wins)