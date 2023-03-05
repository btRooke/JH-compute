import logging
import os
import shutil
from threading import Thread

from connect4.player import Player
from jhcompute import JHPool

# activating the logging inside the pool

logging.basicConfig(
    format="%(asctime)s %(levelname)-1s %(message)s",
    level=logging.DEBUG
)

# create the pool

pool = JHPool(16, "training_task.py")

# training round


class Competition(Thread):
    
    def __init__(self, pool : JHPool, one, two):
        self.winning_model = None
        self.pool = pool
        self.one = one if one else Player()
        self.two = two if two else Player()
        super().__init__()

    def run(self):

        one_path = self.pool.get_tempfile_path()
        self.one.write(one_path)

        two_path = self.pool.get_tempfile_path()
        self.two.write(two_path)

        result = self.pool.submit({
            "train_games": 10,
            "comp_games": 10,
            "learning_batch_size": 5,
            "epsilon_decay": 0.9998,
            "player_one_path": one_path,
            "player_two_path": two_path
        })

        self.winning_model = Player(one_path if result["winner"] == 1 else two_path)

        shutil.rmtree(one_path)
        shutil.rmtree(two_path)


winning_models = [Player() for _ in range(pool.node_count * 2)]

while winning_models != 1:

    competitions = []

    while winning_models:

        one = winning_models.pop()
        two = winning_models.pop()

        competitions.append(Competition(pool, one, two))

    [thread.start() for thread in competitions]
    [thread.join() for thread in competitions]
    [winning_models.append(c.winning_model) for c in competitions]

winning_models[0].write("winner.txt")






