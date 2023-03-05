from connect4.player import Player
from connect4.trainer import train, compete
from jhcompute.task_utils import load_input, write_output

params = load_input()

# example_params = {
#     "train_games": 10,
#     "comp_games": 10,
#     "learning_batch_size": 100,
#     "epsilon_decay": 0.9,
#     "player_one_path": "some/path",
#     "player_two_path": "some/path"
# }

player_one = Player(params["player_one_path"])
player_two = Player(params["player_two_path"])

train(
    params["train_games"],
    player_one, player_two,
    params["learning_batch_size"], params["epsilon_decay"]
)

wins_one, wins_two = compete(params["comp_games"], player_one, player_two)

if wins_one > wins_two:
    player_one.write(params["player_one_path"])
    result = {"winner": 1}

else:
    player_two.write(params["player_two_path"])
    result = {"winner": 2}

write_output(result)
