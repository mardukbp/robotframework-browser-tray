import argparse
import http.client
import os
import site
import socket
import subprocess
import sys
import time
import tkinter as tk
from os.path import realpath
from pathlib import Path
from subprocess import Popen
from tkinter import messagebox
from typing import List, Tuple

from PIL import Image
from pystray import Icon, Menu, MenuItem


REMOTE_DEBUGGING_PORT = 1234
PLAYWRIGHT_PROCESS_PORT= 4711


_, site_packages = site.getsitepackages()
browser_wrapper = Path(site_packages) / "Browser" / "wrapper"
index_js = browser_wrapper / "index.js"
node_modules = browser_wrapper / "node_modules"
playwright_core = node_modules / "playwright-core"


def find_chromium(path: Path) -> List[Path]:
    return [
        Path(file.path)
        for file in os.scandir(path)
        if file.is_dir() and file.name.startswith("chromium")
    ]


def playwright_is_initialized():
    return node_modules.is_dir() and playwright_core.is_dir()


def get_chromium_dir(node_modules: Path):
    local_browsers = playwright_core / ".local-browsers"

    if not (node_modules.is_dir() and local_browsers.is_dir() and find_chromium(local_browsers)):
       return None

    return find_chromium(local_browsers)[0]


def start_playwright(playwright_process_port: int) -> Popen:
    return Popen(['node', index_js, str(playwright_process_port)])


class TrayIcon:
    def __init__(self, playwright_process_port: int, remote_debugging_port: int, timeout=0):
        chromium_icon = Image.open(Path(realpath(__file__)).parent / "chromium.png")

        playwright_process = start_playwright(playwright_process_port)
        time.sleep(2)
        return_code = playwright_process.poll()

        if return_code:
            sys.exit(return_code)

        if timeout:
            time.sleep(timeout)
            playwright_process.kill()
            sys.exit(0)

        self.processes = [playwright_process]
        self.remote_debugging_port = remote_debugging_port
        self.icon = Icon(
        name='Browser Tray',
        icon=chromium_icon,
        menu=Menu(
            MenuItem(
                'Open Chromium',
                self.open_chromium,
                default=True
            ),
            MenuItem(
                'Open Chromium Incognito',
                self.open_chromium_incognito,
            ),
            MenuItem(
                'Exit',
                self.exit
            )
        )
    )

    def exit(self):
        for proc in self.processes:
            proc.terminate()

        self.icon.stop()

    def open_chromium(self):
        self.start_chromium(self.remote_debugging_port, False)

    def open_chromium_incognito(self):
        self.start_chromium(self.remote_debugging_port, True)

    def run(self):
        self.icon.run()

    def start_chromium(self, remote_debugging_port: int, incognito: bool):
        chromium_dir = get_chromium_dir(node_modules)

        if not chromium_dir:
            window = tk.Tk()
            window.withdraw()
            messagebox.showerror("Error", "Chromium is not installed. Execute 'rfbrowser init chromium'.", master=window)
        else:
            incognito_flag = ["-incognito"] if incognito else []
            chrome_exe = chromium_dir / "chrome-win" / "chrome.exe"
            chromium = Popen([chrome_exe, f"--remote-debugging-port={remote_debugging_port}", "--test-type"] + incognito_flag)
            time.sleep(2)
            self.processes.append(chromium)


def is_running(cmd: str) -> bool:
    process_list = subprocess.check_output(
        # Set the character page to 65001 = UTF-8
        f'chcp 65001 | TASKLIST /FI "IMAGENAME eq {cmd}"', shell=True
    ).decode('utf-8').splitlines()
    instances = [
        process 
        for process in process_list 
        if process.startswith(cmd) and os.getlogin().lower() in process.lower()
    ]
    return len(instances) > 1


def get_ports(cmdline_args=None) -> Tuple[int, int]:
    MAX_PORT = 2**16
    
    arg_parser = argparse.ArgumentParser(add_help=True)
    arg_parser.add_argument("--pw-port", default=PLAYWRIGHT_PROCESS_PORT, type=int, help=f"Playwright process port (default: {PLAYWRIGHT_PROCESS_PORT})")
    arg_parser.add_argument("--cdp-port", default=REMOTE_DEBUGGING_PORT, type=int, help=f"Chromium debugging port (default: {REMOTE_DEBUGGING_PORT})")
    args = arg_parser.parse_args(cmdline_args)
    playwright_process_port = args.pw_port
    remote_debugging_port = args.cdp_port

    if playwright_process_port > MAX_PORT or remote_debugging_port > MAX_PORT:
        raise ValueError(f"Port numbers cannot be larger than {MAX_PORT}")

    return (playwright_process_port, remote_debugging_port)


def run():
    cmd = "browser-tray.exe"
    if is_running(cmd):
        print(f"{cmd} is already running")
        sys.exit(1)

    playwright_process_port, remote_debugging_port = get_ports()

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
        tray_icon = TrayIcon(playwright_process_port, remote_debugging_port)
        tray_icon.run()
