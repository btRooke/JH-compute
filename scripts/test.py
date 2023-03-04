from threading import Thread

from jhcompute import *

pool = Pool(5, "bogo.py")

task_object = {
    "size": 10
}

threads = [
    Thread(target=lambda: print(pool.submit(task_object)))
    for i in range(10)
]

[thread.start() for thread in threads]
[thread.join() for thread in threads]



