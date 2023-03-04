import connect4
import numpy as np
import tensorflow as tf
from tensorflow import keras

class Player:
    def __init__(self) -> None:
        # Create a CNN model
        self.model = keras.models.Sequential()
        # 64 4x4 kernels
        self.model.add(keras.layers.Conv2D(64, (4, 4), activation='relu', input_shape=(6, 7)))
        # 64 2x2 kernels
        self.model.add(keras.layers.Conv2D(64, (2, 2), activation='relu'))
        # Flattener to reduce dimensions from 2 to 1 for dense layers
        self.model.add(keras.layers.Flatten())
        # Two 64-node dense layers
        self.model.add(keras.layers.Dense(64, activation='relu'))
        self.model.add(keras.layers.Dense(64, activation='relu'))
        # Output layer with one node per column
        self.model.add(keras.layers.Dense(connect4.WIDTH, activation='softmax'))


    # Given a Connect 4 board state and a randomness coefficient, choose a move
    def act(self, board: connect4.Board, epsilon: float):
        assert(epsilon >= 0 and epsilon <= 1)

        action, prob_weights = self.decide_move(board, epsilon)

        if board.move(action):
            return action
        
        # If an illegal move was made, choose the next-most probable move until a legal move is found
        else:
            while True:
                # Find the largest weight smaller than the previous weight
                previous_weight = prob_weights[action]
                new_weight = min(prob_weights)
                
                for prob in prob_weights:
                    if prob < previous_weight and prob > new_weight:
                        new_weight = prob
                        action = list(prob_weights).index(new_weight)
                
                if board.move(action):
                    return action


    # Choose the next move
    # Use a small randomness coefficient epsilon to occasionally choose new moves
    # This promotes exploration in the model, which could help it find new winning strategies
    def decide_move(model, board, epsilon: int) -> tuple(int, float):
        observation = np.array(board).reshape(1, connect4.HEIGHT, connect4.WIDTH, 1)
        logits = model.predict(observation)
        prob_weights = tf.nn.softmax(logits).numpy()
        
        # Choose a random float between 0 and 1
        # If leq epsilon, choose a random action
        # Otherwise, use the model
        if np.random.random() > epsilon:
            action = list(prob_weights[0]).index(max(prob_weights[0]))
        else:
            action = np.random.choice(connect4.WIDTH)
            
        return action, prob_weights[0]


    # Compute the loss of the decisions made over a complete game
    def compute_loss(self, logits, actions, rewards): 
        entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=actions)
        loss = tf.reduce_mean(entropy * rewards)
        return loss

    
    # Apply forward propagation to train the model
    def train_step(self, model, optimizer, observations, actions, rewards):
        with tf.GradientTape() as tape:
            logits = model(observations)
            loss = self.compute_loss(logits, actions, rewards)
            
            grads = tape.gradient(loss, model.trainable_variables)
            optimizer.apply_gradients(zip(grads, model.trainable_variables))