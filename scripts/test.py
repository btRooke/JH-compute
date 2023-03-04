import logging
from threading import Thread

logging.basicConfig(level=logging.DEBUG)

from jhcompute import *

pool = Pool(5, "bogo.py")

task_object = {
    "size": 1000000
}

threads = [
    Thread(target=lambda: pool.submit(task_object))
    for i in range(10)
]

[thread.start() for thread in threads]
print("Started.")

[thread.join() for thread in threads]
print("Done.")



