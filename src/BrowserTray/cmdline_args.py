import argparse


REMOTE_DEBUGGING_PORT = 1234


def get_remote_debugging_port() -> int:
    arg_parser = argparse.ArgumentParser(add_help=True)
    arg_parser.add_argument(
        "--cdp-port", 
        default=REMOTE_DEBUGGING_PORT, 
        type=int, 
        help=f"Chromium debugging port (default: {REMOTE_DEBUGGING_PORT})"
    )
    args = arg_parser.parse_args()

    return args.cdp_port
