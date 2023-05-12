# JH Compute

Built in under 24 hours for STACSHack 2023 (STACSHack 9), JH compute comprises:

- JHCompute - A framework for distributed computing in the John Honey (JH) computer lab in the School of Computer Science at the University of St Andrews
- An adversairal CNN to play connect 4 whose training can be parallelised
- A website to on which one can play against the AI

## JHCompute Framework

The interface that JHCompute provides is a workpool, the workpool is configured with a _job script_ and the job script can be executed with different parameters in parallel, a simple example is as follows (full versions at `scripts/example`):

Main:

```python
from threading import Thread
from jhcompute import JHPool

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
```

Job script:

```python
import random
from jhcompute.task_utils import load_input, write_output

parameters = load_input()

random_list = [random.randint(0, parameters["size"]) for _ in range(parameters["size"])]
random_list.sort()

write_output({
    "result": random_list
})
```

This example code parallelises sorting a list of 10,000,000 elements over 40 notes in the JH lab.

For this demo, the parameters of each task are the same (`task_object`) but in real training the task objects change and contain paths to temporary files holding stored CNN models which are then trained on separate nodes.

The framework hinges heavily on the shared networked drive all machines have as well as easy key-based SSH access to the machines.

## Adversairal CNN

Tensorflow was used to create a mostly from-scratch adversairal CNN to play connect 4. These models were then pitted against each other over a large tournament bracket on 50 nodes in the JH lab to train a model.

## Website

React was used to create a simple website where the model (imported by [a cool JS library](https://www.npmjs.com/package/@tensorflow/tfjs-converter)) will play against you.

Admittedly after doing all of this we could only train the model for about 40 minutes, so it's not very good.

Regardless the principle of the project is solid and extensible.

Play against the model at [btrooke.github.io/JH-compute](https://btrooke.github.io/JH-compute/)!
