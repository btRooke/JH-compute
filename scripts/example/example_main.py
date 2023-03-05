import logging
from threading import Thread
from jhcompute import JHPool

# activating the logging inside the pool

logging.basicConfig(
    format="%(asctime)s %(levelname)-1s %(message)s",
    level=logging.DEBUG
)

pool = JHPool(40, "example_task.py")  # pool of 30 nodes, the task script is "training_task.py"

task_object = {
    "size": 10000000
}

threads = [
    Thread(target=lambda: pool.submit(task_object))
    for i in range(50)
]

[thread.start() for thread in threads]
[thread.join() for thread in threads]



