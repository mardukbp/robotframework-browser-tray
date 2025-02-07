import os
import site
import subprocess
import sys
import tkinter as tk
from os.path import realpath
from pathlib import Path
from subprocess import Popen
from tkinter import messagebox
from typing import List

from PIL import Image
from pystray import Icon, Menu, MenuItem

from BrowserTray import cmdline_args


_, site_packages = site.getsitepackages()
browser_wrapper = Path(site_packages).resolve() / "Browser" / "wrapper"
index_js = browser_wrapper / "index.js"
node_modules = browser_wrapper / "node_modules"
playwright_core = node_modules / "playwright-core"


def find_chromium(path: Path) -> List[Path]:
    return [
        Path(file.path)
        for file in os.scandir(path)
        if file.is_dir() and file.name.startswith("chromium")
    ]


def get_chromium_dir(node_modules: Path):
    local_browsers = playwright_core / ".local-browsers"

    if not (node_modules.is_dir() and local_browsers.is_dir() and find_chromium(local_browsers)):
       return None

    return find_chromium(local_browsers)[0]


def start_chromium(remote_debugging_port: int, incognito: bool):
    chromium_dir = get_chromium_dir(node_modules)

    if not chromium_dir:
        window = tk.Tk()
        window.withdraw()
        messagebox.showerror("Error", "Chromium is not installed. Execute 'rfbrowser init chromium'.", master=window)
    else:
        incognito_flag = ["-incognito"] if incognito else []
        chrome_exe = chromium_dir / "chrome-win" / "chrome.exe"
        Popen([chrome_exe, f"--remote-debugging-port={remote_debugging_port}", "--test-type"] + incognito_flag)


class TrayIcon:
    def __init__(self, remote_debugging_port: int):
        chromium_icon = Image.open(Path(realpath(__file__)).parent / "chromium.png")

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
        self.icon.stop()

    def open_chromium(self):
        start_chromium(self.remote_debugging_port, False)

    def open_chromium_incognito(self):
        start_chromium(self.remote_debugging_port, True)

    def run(self):
        cmd = "browser-tray.exe"
        if is_running(cmd):
            print(f"{cmd} is already running")
            sys.exit(1)
            
        self.icon.run()


def is_running(cmd: str) -> bool:
    process_list = subprocess.check_output(
        # Set the character page to 65001 = UTF-8
        f'chcp 65001 | TASKLIST /FI "IMAGENAME eq {cmd}"', shell=True
    ).decode('utf-8').splitlines()
    instances = [
        process 
        for process in process_list 
        if process.startswith(cmd)
    ]
    return len(instances) > 1


def run():
    playwright_process_port, remote_debugging_port = cmdline_args.get_ports()
    tray_icon = TrayIcon(remote_debugging_port)
    tray_icon.run()
