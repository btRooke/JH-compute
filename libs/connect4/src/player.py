import connect4
import numpy as np
import tensorflow as tf
from tensorflow import keras

class Player:
    def __init__(self) -> None:
        # Rate of decrease for rewarding moves further from the end state
        self.discount_factor = 0.9

        # Create a CNN model
        self.model = keras.models.Sequential()
        # 64 4x4 kernels
        self.model.add(keras.layers.Conv2D(64, (4, 4), activation='relu', input_shape=(6, 7, 1)))
        # 64 2x2 kernels
        self.model.add(keras.layers.Conv2D(64, (2, 2), activation='relu'))
        # Flattener to reduce dimensions from 2 to 1 for dense layers
        self.model.add(keras.layers.Flatten())
        # Two 64-node dense layers
        self.model.add(keras.layers.Dense(64, activation='relu'))
        self.model.add(keras.layers.Dense(64, activation='relu'))
        # Output layer with one node per column
        self.model.add(keras.layers.Dense(connect4.WIDTH, activation='softmax'))

        self.model.compile(
            loss='mean_squared_error',
            optimizer=keras.optimizers.Adam(),
            metrics=['accuracy']
        )


    # Given a Connect 4 board state and a randomness coefficient, choose a move
    def act(self, board: connect4.Board, epsilon: float) -> int:
        assert(epsilon >= 0 and epsilon <= 1)

        action, prob_weights = self.decide_move(board, epsilon)

        if board.move(action):
            return action
        
        # If an illegal move was made, choose a random move instead
        else:
            while True:
                action = np.random.choice(connect4.WIDTH)

                if board.move(action):
                    return action


    # Choose the next move
    # Use a small randomness coefficient epsilon to occasionally choose new moves
    # This promotes exploration in the model, which could help it find new winning strategies
    def decide_move(self, board: connect4.Board, epsilon: float) -> tuple[int, float]:
        observation = np.array(board.state).reshape(1, connect4.HEIGHT, connect4.WIDTH, 1)
        logits = self.model.predict(observation, verbose=0)
        prob_weights = tf.nn.softmax(logits).numpy()
        
        # Choose a random float between 0 and 1
        # If leq epsilon, choose a random action
        # Otherwise, use the model
        if np.random.random() > epsilon:
            action = list(prob_weights[0]).index(max(prob_weights[0]))
        else:
            action = np.random.choice(connect4.WIDTH)
            
        return action, prob_weights[0]

    
    # After a game has been played, give the model a reward and train its weights
    def train(self, observations, actions, reward: float) -> None:
        # Give each move a reward based on the final result of the game
        # Moves closer to the end of the game are given bigger rewards
        rewards = np.zeros_like(actions)

        for i in range(len(actions)):
            rewards[len(actions) - (1 + i)] = reward
            reward *= self.discount_factor

        # Train the model on the played states and associated rewards
        observations = observations.reshape(len(actions), connect4.HEIGHT, connect4.WIDTH, 1)
        self.model.train_on_batch(observations, rewards)