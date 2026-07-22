import os
import site
import subprocess
import sys
import tkinter as tk
from glob import iglob
from os.path import join, realpath
from pathlib import Path
from subprocess import Popen
from tkinter import messagebox
from typing import Optional

from PIL import Image
from pystray import Icon, Menu, MenuItem

from BrowserTray import cmdline_args


_, site_packages = site.getsitepackages()
browser_wrapper = Path(site_packages).resolve() / "Browser" / "wrapper"
index_js = browser_wrapper / "index.js"
node_modules = browser_wrapper / "node_modules"
playwright_core = node_modules / "playwright-core"
local_browsers = os.environ.get('PLAYWRIGHT_BROWSERS_PATH', str(playwright_core / ".local-browsers"))


def find_chrome_exe() -> Optional[str]:
    if not Path(local_browsers).is_dir():
       return

    for exe in iglob(join(local_browsers, "**/*.exe"), recursive=True):
        if exe.endswith("chrome.exe"):
            return exe


def start_chromium(remote_debugging_port: int, incognito: bool):
    chrome_exe = find_chrome_exe()

    if not chrome_exe:
        window = tk.Tk()
        window.withdraw()
        messagebox.showerror("Error", "Chromium is not installed. Execute 'rfbrowser init chromium'.", master=window)
    else:
        print(f"Starting {chrome_exe}")
        incognito_flag = ["-incognito"] if incognito else []
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
    remote_debugging_port = cmdline_args.get_remote_debugging_port()
    tray_icon = TrayIcon(remote_debugging_port)
    tray_icon.run()
