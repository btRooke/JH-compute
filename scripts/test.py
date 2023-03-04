import logging
from threading import Thread
from jhcompute import JHPool

logging.basicConfig(
    format="%(asctime)s %(levelname)-1s %(message)s",
    level=logging.DEBUG
)

pool = JHPool(5, "bogo.py")

task_object = {
    "size": 10000000
}

threads = [
    Thread(target=lambda: pool.submit(task_object))
    for i in range(5)
]

[thread.start() for thread in threads]
[thread.join() for thread in threads]



