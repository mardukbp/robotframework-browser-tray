import http.client
import re
import socket
import sys
import tempfile
import time
from functools import wraps
from pathlib import Path

import RobotDebug.styles
from Browser.base.librarycomponent import LibraryComponent
from robot.run import run_cli
from robot.api import logger


def escape_ansi(line):
    ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)


print_output = RobotDebug.styles.print_output

@wraps(print_output)
def wrap_print_output(head, message, style=RobotDebug.styles.NORMAL_STYLE):
    print_output(head, escape_ansi(message), style)

RobotDebug.styles.print_output = wrap_print_output


presenter_mode = LibraryComponent.presenter_mode

@wraps(presenter_mode)
def wrap_presenter_mode(self, selector, strict):
    selector = self.resolve_selector(selector)
    if self.library.presenter_mode:
        mode = self.get_presenter_mode
        try:
            self.library.scroll_to_element(selector)
            self.library.highlight_elements(
                selector,
                duration=mode["duration"],
                width=mode["width"],
                style=mode["style"],
                color=mode["color"],
            )
        except Exception as error:
            # selector = self.library.record_selector(f'"{selector}" failure')
            logger.debug(f"On presenter more supress {error}")
        else:
            time.sleep(mode["duration"].seconds)
    return selector

LibraryComponent.presenter_mode = wrap_presenter_mode


TEST_SUITE = b"""
*** Settings ***
Library    BrowserTray.Repl   repl=${True}

*** Test Cases ***
Robot Framework Debug REPL
    Debug
"""


def shell():
    """A standalone robotframework shell."""

    default_no_logs = [
        "-l",
        "None",
        "-x",
        "None",
        "-o",
        "None",
        "-L",
        "None",
        "-r",
        "None",
        "--quiet",
    ]

    with tempfile.NamedTemporaryFile(
        prefix="robot-debug-", suffix=".robot", delete=False
    ) as test_file:
        test_file.write(TEST_SUITE)
        test_file.flush()

        if len(sys.argv) > 1:
            args = sys.argv[1:] + [test_file.name]
        else:
            args = [*default_no_logs, test_file.name]

        try:
            sys.exit(run_cli(args))
        finally:
            test_file.close()
            # pybot will raise PermissionError on Windows NT or later
            # if NamedTemporaryFile called with `delete=True`,
            # deleting test file seperated will be OK.
            file_path = Path(test_file.name)
            if file_path.exists():
                file_path.unlink()


def run(timeout=0):
    try:
        http.client.HTTPConnection('127.0.0.1', 1234, timeout=1).connect()
        if timeout:
            time.sleep(timeout)
            sys.exit(0)
        shell()
    except socket.timeout:
        print("ibrowser needs either:\n" +
              "  - a running Chromium, started using the tray icon or\n" + 
              "  - a running Microsoft Edge started as explained in the documentation: https://pypi.org/project/robotframework-browser-tray/"
        )
        sys.exit(1)
