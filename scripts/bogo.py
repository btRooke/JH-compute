import json
import random
import sys

with open(sys.argv[1], "r") as f:
    parameters = json.load(f)

random_list = [random.randint(0, parameters["size"]) for _ in range(parameters["size"])]
random_list.sort()

