import http.client
import site
import socket
import subprocess
import sys
from pathlib import Path
from subprocess import Popen


_, site_packages = site.getsitepackages()
browser_wrapper = Path(site_packages) / "Browser" / "wrapper"
index_js = browser_wrapper / "index.js"
node_modules = browser_wrapper / "node_modules"
playwright_core = node_modules / "playwright-core"


def playwright_is_initialized():
    return node_modules.is_dir() and playwright_core.is_dir()


def start_playwright(playwright_process_port: int) -> Popen:
    return Popen(
        ['node', index_js, str(playwright_process_port)],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE
    )


def run(playwright_process_port: int) -> Popen:
    if not playwright_is_initialized():
        print(
            "Playwright has not been initialized.\n" + 
            "In order to use Chromium execute 'rfbrowser init chromium'.\n" + 
            "If you want to use the Microsoft Edge installed on your system execute 'rfbrowser init --skip-browsers'"
        )
        sys.exit(1)

    try:
        http.client.HTTPConnection('127.0.0.1', playwright_process_port, timeout=1).connect()
        print(f"The port {playwright_process_port} is already in use. Either browser-tray is already running or another process is using the port.\n" + 
              "To start the Playwright wrapper on another port execute `browser-tray --pw-port PORT`")
        sys.exit(1)
    except socket.timeout:
        return start_playwright(playwright_process_port)
