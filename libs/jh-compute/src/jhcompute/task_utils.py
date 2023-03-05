import json
import sys


def load_input() -> dict:
    with open(sys.argv[1], "r") as f:
        return json.load(f)


def write_output(output_object: dict) -> None:
    with open(sys.argv[1], "w") as f:
        json.dump(output_object, f)