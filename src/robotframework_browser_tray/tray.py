import os
import site
import sys
from os.path import realpath
from pathlib import Path
from subprocess import Popen
from tkinter import messagebox
from PIL import Image
from pystray import Icon, Menu, MenuItem


REMOTE_DEBUGGING_PORT = 1234
PLAYWRIGHT_PROCESS_PORT= 55555

chromium_icon = Image.open(Path(realpath(__file__)).parent / "chromium.png")

_, site_packages = site.getsitepackages()
browser_wrapper = Path(site_packages) / "Browser" / "wrapper"
index_js = browser_wrapper / "index.js"
node_modules = browser_wrapper / "node_modules"
local_browsers = node_modules / "playwright-core" / ".local-browsers"

processes: list[Popen] = []


def find_chromium(path: Path) -> Path:
    chromium = [
        file.path
        for file in os.scandir(path)
        if file.is_dir() and file.name.startswith("chromium")
    ]

    if chromium:
        return Path(chromium[0])
    
    return None


def assert_playwright_initialized():
    if not (node_modules.is_dir() and local_browsers.is_dir() and find_chromium(local_browsers)):
        messagebox.showerror("Playwright wrapper error", "\n\n".join([
            "Playwright has not been initialized.",
            "Execute 'rfbrowser init chromium'."
        ]))
        sys.exit(1)


def start_playwright():
    try:
        node_process = Popen(f"node {index_js} {PLAYWRIGHT_PROCESS_PORT}")
        processes.append(node_process)
    except FileNotFoundError as error:
        messagebox.showerror("Playwright wrapper could not be started", error)


def start_chromium(incognito=False):
    incognito_flag = "-incognito" if incognito else ""

    try:
        chrome_exe = find_chromium(local_browsers) / "chrome-win" / "chrome.exe"
        chrome_process = Popen(f"{chrome_exe} --remote-debugging-port={REMOTE_DEBUGGING_PORT} --test-type {incognito_flag}")
        processes.append(chrome_process)
    except FileNotFoundError as error:
        messagebox.showerror("Chromium could not be started", error)


def open_chromium():
    start_chromium()


def open_chromium_incognito():
    start_chromium(True)


def exit():
    for proc in processes:
        proc.terminate()

    icon.stop()


icon = Icon(
    name='Browser Tray',
    icon=chromium_icon,
    menu=Menu(
        MenuItem(
            'Open Chromium',
            open_chromium,
            default=True
        ),        
        MenuItem(
            'Open Chromium Incognito',
            open_chromium_incognito,
        ),
        MenuItem(
            'Exit',
            exit
        )
    )
)


def run():
    assert_playwright_initialized()
    start_playwright()
    icon.run()
