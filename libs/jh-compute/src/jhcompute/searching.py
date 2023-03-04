from threading import Thread
from typing import List, Tuple

import jhcompute
from jhcompute.ssh import run_command


def all_nodes() -> List[str]:

    with open(jhcompute.resource("list.csv"), "r") as file:
        raw = file.read()

    # split by newline and remove empty lines

    return [line for line in raw.split("\n") if line]


def user_count(hostname: str) -> int:

    result = run_command(hostname, ["w", "-h"])

    if result.returncode != 0:
        return -1

    else:
        return result.stdout.count(b"\n")


class UserCountFinder(Thread):

    count = -2

    def __init__(self, hostname):
        super().__init__()
        self.hostname = hostname

    def run(self) -> None:
        self.count = user_count(self.hostname)


def active_nodes_user_count() -> List[Tuple[str, int]]:

    """
    Get tuples of (hostname, user_count) for all active nodes in JH.

    Blocks until complete.

    :return: A sorted (lowest to highest user count) list of tuples of
             (hostname, user_count) for active nodes.
    """

    nodes = all_nodes()

    threads = [UserCountFinder(node) for node in nodes]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

    return [("pc7-072-l", 0)] + sorted(
        [(t.hostname, t.count) for t in threads if t.count >= 0],
        key=lambda p: p[1]
    )


if __name__ == "__main__":
    print(active_nodes_user_count())
