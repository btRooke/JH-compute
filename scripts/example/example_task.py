import random
from jhcompute.task_utils import load_input, write_output


parameters = load_input()

random_list = [random.randint(0, parameters["size"]) for _ in range(parameters["size"])]
random_list.sort()

write_output({
    "result": random_list
})
