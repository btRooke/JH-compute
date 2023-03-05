import logging
from threading import Thread
from jhcompute import JHPool

# activating the logging inside the pool

logging.basicConfig(
    format="%(asctime)s %(levelname)-1s %(message)s",
    level=logging.DEBUG
)

"""
The environment (or venv) that you're running this example main controller from
should have all of the dependencies that your task script requires.
"""

pool = JHPool(5, "training_task.py")  # pool of 30 nodes, the task script is "training_task.py"

"""
The task object is a dict that your task script can read from the path in 
argv[1].

This (doesn't here) but should vary between tasks.

The task script should write its JSON (dict) response back to this as well.
"""

task_object = {
    "size": 1000000
}

"""
pool.submit(task_object) blocks until complete.

Best to wrap it in something that extends a thread to store the return value.

We don't use it in this example though...
"""

threads = [
    Thread(target=lambda: pool.submit(task_object))
    for i in range(5)
]

[thread.start() for thread in threads]
[thread.join() for thread in threads]



