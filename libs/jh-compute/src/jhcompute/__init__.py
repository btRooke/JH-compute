import os

# exposed methods

from .pool import JHPool

# resources

dir_path = os.path.dirname(os.path.realpath(__file__))

def resource(path: str):
    return f"{dir_path}/resources/{path}"
