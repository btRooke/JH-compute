import json
import random
import sys
from jhcompute import JHPool

with open(sys.argv[1], "r") as f:
    parameters = json.load(f)

random_list = [random.randint(0, parameters["size"]) for _ in range(parameters["size"])]
random_list.sort()

with open(sys.argv[1], "w") as f:

    json.dump({
        "result": random_list
    }, f)
