from silence_tensorflow import silence_tensorflow
silence_tensorflow()

import connect4
import numpy as np
from tensorflow import keras
from player import Player


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
# epsilon_decay is how quickly the randomness coefficient decreases after each game (typically > 0.999) 
def train(n_games, player1, player2, epsilon_decay):
    keras.backend.set_floatx('float64')
    print(f"Training for {n_games} games")

    memory = [Memory(), Memory()]
    epsilon = 1

    for i in range(n_games):
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

        # Update exploration probability after each game
        epsilon *= epsilon_decay

        # Train the models every 10 games
        if i % 10 == 9:

            player1.train(np.array(memory[0].observations), np.array(memory[0].actions), reward[0])
            player2.train(np.array(memory[1].observations), np.array(memory[1].actions), reward[1])

            memory[0].clear()
            memory[1].clear()
            

# Play n games without training, returning the winner
def compete(n_games, player1, player2):
    print(f"Competing for {n_games} games")
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
                    wins[0] += 1

                elif victory_state == connect4.Result.WIN_P2:
                    wins[1] += 1
                    
                break

    return wins


if __name__ == "__main__":
    player1 = Player()
    player2 = Player()

    train(1000, player1, player2, 0.9998)
    wins = compete(100, player1, player2)

    print(wins)