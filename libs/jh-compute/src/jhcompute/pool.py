import json
import logging
import os
import queue
import random
import string
import sys
from pathlib import Path
from threading import Thread, Lock

from jhcompute import ssh
from jhcompute.searching import active_nodes_user_count


class JHPool:

    def __init__(self, node_count: int, job_file: str) -> None:

        """
        Create a pool of workers which can concurrently run a job script in the JH labs.

        The task script can read a JSON object (the task object) of parameters
        from the path to a temporary file provided at argv[1].

        A response should be written to this same file once complete.

        :param node_count: The amount of nodes (lab machines) to use.
        :param job_file: A path (relative to the CWD) for a task script.
        """

        self.task_id_lock = Lock()
        self.task_id = 0

        self.python_path = sys.executable
        self.node_count = node_count
        self.temp_dir = os.path.dirname(os.getcwd()) + "/temp/"

        logging.info(f"Using {self.python_path} as python")
        logging.info(f"Using {self.temp_dir} as temp directory")

        # make temp directory

        try:
            os.mkdir(self.temp_dir)

        except FileExistsError as e:
            if Path(self.temp_dir).is_file():
                raise e

        # validate job file

        self.job_file = Path(job_file).resolve()

        if not self.job_file.is_file():
            raise FileNotFoundError(f"Can't find job file \"{job_file}\"...")

        logging.info(f"Loaded {self.job_file} as job file!")

        # find nodes

        potential_nodes = active_nodes_user_count()

        logging.info(
            f"Found {len(potential_nodes)} potential active nodes -- require {self.node_count} -- {len([n for n in potential_nodes if n[1] == 0])} have no users"
        )

        if len(potential_nodes) < self.node_count:
            raise RuntimeError(f"Too few nodes active -- found only {len(potential_nodes)}")

        chosen_nodes = potential_nodes[:self.node_count]

        for node in filter(lambda n: n[1] > 0, chosen_nodes):
            logging.warning(f"{node[0]} already have {node[1]} user(s)...")

        self.nodes = [Node(self, node[0]) for node in chosen_nodes]
        self.free_nodes = queue.Queue()
        [self.free_nodes.put(node) for node in self.nodes]

        logging.info(f"Using initial nodes: {chosen_nodes}")

        # initialise queues

        self.job_queue = queue.Queue()

        self.potential_nodes = queue.Queue()
        [self.potential_nodes.put(node[0]) for node in potential_nodes[self.node_count:]]

    def submit(self, task_object: dict) -> dict:

        """
        Submit a task object to be processed by the pool task script.

        Blocks until complete.

        Handles node failure by replacing the node -- fails if all nodes in JH
        are used up (this is very unlikely).

        Throws a RuntimeException if the script being run on some worker node
        fails.

        :param task_object: A JSON object (python dict) of parameters for the task script to process.
        :return: A python dict -- the response of the task script.
        """

        task_id = self._get_next_task_id()

        logging.info(f"Task {task_id} submitted -- {task_object}")
        node = self.free_nodes.get()

        complete = False

        while not complete:

            try:
                result = node.run_task(task_id, task_object)
                complete = True

            except NodeDiedException:
                logging.warning(f"Node died during {task_id} - {node.hostname}")
                node = self._new_node()
                logging.info(f"Selected {node.hostname} as new node!")

        self.free_nodes.put(node)

        logging.info(f"Task {task_id} complete from {node.hostname}")

        return result

    def _get_next_task_id(self):

        with self.task_id_lock:
            to_return = self.task_id
            self.task_id += 1
            return to_return

    def write_to_temp(self, json_object: dict):

        filename = self.temp_dir + f"{''.join(random.choices(string.ascii_letters, k=32))}.json"

        while Path(filename).is_file():
            filename = self.temp_dir + f"{''.join(random.choices(string.ascii_letters, k=32))}.json"

        with open(filename, "w") as file:
            json.dump(json_object, file)

        return filename

    def _new_node(self):
        return Node(self, self.potential_nodes.get())


class NodeDiedException(Exception):
    pass


class Node:

    def __init__(self, pool: JHPool, hostname: str):
        self.hostname = hostname
        self.pool = pool

    def run_task(self, task_id: int, task_object: dict) -> dict:

        logging.info(f"Task {task_id} started on {self.hostname}")

        object_file = self.pool.write_to_temp(task_object)

        try:
            result = ssh.run_command(self.hostname, [
                self.pool.python_path,
                self.pool.job_file,
                object_file
            ])

        except (ConnectionAbortedError, ConnectionError):
            raise NodeDiedException(f"Node {self.hostname} died during {task_id}!")

        if result.returncode == 0:

            with open(object_file, "r") as file:
                return_object = json.load(file)

            os.remove(object_file)
            return return_object

        else:

            raise RuntimeError(
                f"Node {self.hostname} execution failed during {task_id}\n"
                f"stdout:\n{result.stdout.decode()}\n"
                f"stderr:\n{result.stderr.decode()}\n"
            )
