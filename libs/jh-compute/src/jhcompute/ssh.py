import subprocess
from typing import List


def run_command(hostname: str, command: List[str], connect_timeout: int = 5):

    result = subprocess.run([
        "ssh",
        "-o",
        f"ConnectTimeout={connect_timeout}",
        hostname
    ] + command, capture_output=True)

    # check errors
    
    if any(b"Connection timed out" in out for out in [result.stdout, result.stderr]):
        raise ConnectionError(f"Connection timed out to f{hostname}")

    elif any(b"closed by remote host." in out for out in [result.stdout, result.stderr]):
        raise ConnectionAbortedError(f"Connection closed by host f{hostname}")

    return result


