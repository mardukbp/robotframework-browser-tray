import argparse
from typing import Tuple


REMOTE_DEBUGGING_PORT = 1234
PLAYWRIGHT_PROCESS_PORT= 4711


def get_ports() -> Tuple[int, int]:
    MAX_PORT = 2**16
    
    arg_parser = argparse.ArgumentParser(add_help=True)
    arg_parser.add_argument("--pw-port", default=PLAYWRIGHT_PROCESS_PORT, type=int, help=f"Playwright process port (default: {PLAYWRIGHT_PROCESS_PORT})")
    arg_parser.add_argument("--cdp-port", default=REMOTE_DEBUGGING_PORT, type=int, help=f"Chromium debugging port (default: {REMOTE_DEBUGGING_PORT})")
    args = arg_parser.parse_args()
    playwright_process_port = args.pw_port
    remote_debugging_port = args.cdp_port

    if playwright_process_port > MAX_PORT or remote_debugging_port > MAX_PORT:
        raise ValueError(f"Port numbers cannot be larger than {MAX_PORT}")

    return (playwright_process_port, remote_debugging_port)
