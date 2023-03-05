from connect4.trainer import train, compete
from jhcompute.task_utils import load_input, write_output

params = load_input()

example_params = {
    "train_games": 10,
    "comp_games": 10,
    "learning_batch_size": 100,
    "epsilon_decay": 0.9,
    "player_one_path": "some/path",
    "player_two_path": "some/path"
}

player_one = load_player(params["player_one_path"])
player_two = load_player(params["player_two_path"])

train(
    params["train_games"],
    player_one, player_two,
    params["learning_batch_size"], params["epsilon_decay"]
)

wins_one, wins_two = compete(params["comp_games"], player_one, player_two)

if wins_one > wins_two:
    write_player(player_one, params["player_one_path"])

else:
    write_player(player_two, params["player_two_path"])

write_output({
    "winning_player": 1
})
