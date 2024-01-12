import argparse
import os
import site
import subprocess
import sys
from os.path import realpath
from pathlib import Path
from subprocess import Popen
from PIL import Image
from pystray import Icon, Menu, MenuItem


_, site_packages = site.getsitepackages()
browser_wrapper = Path(site_packages) / "Browser" / "wrapper"
index_js = browser_wrapper / "index.js"
node_modules = browser_wrapper / "node_modules"
local_browsers = node_modules / "playwright-core" / ".local-browsers"


def find_chromium(path: Path) -> list[Path]:
    return [
        Path(file.path)
        for file in os.scandir(path)
        if file.is_dir() and file.name.startswith("chromium")
    ]


def assert_playwright_initialized():
    if not (node_modules.is_dir() and local_browsers.is_dir() and find_chromium(local_browsers)):
       raise FileNotFoundError("Playwright has not been initialized. Execute 'rfbrowser init chromium'.")


def start_playwright(playwright_process_port: int) -> Popen:
    return Popen(f"node {index_js} {playwright_process_port}")


def start_chromium(remote_debugging_port: int, incognito=False) -> Popen:
    incognito_flag = "-incognito" if incognito else ""
    chromium_dir = find_chromium(local_browsers)[0]
    chrome_exe = chromium_dir / "chrome-win" / "chrome.exe"
    return Popen(f"{chrome_exe} --remote-debugging-port={remote_debugging_port} --test-type {incognito_flag}")


def new_tray_icon(processes: list[Popen], remote_debugging_port: int) -> Icon:
    def exit():
        for proc in processes:
            proc.terminate()

        icon.stop()

    def open_chromium():
        chromium = start_chromium(remote_debugging_port)
        processes.append(chromium)

    def open_chromium_incognito():
        chromium = start_chromium(remote_debugging_port, True)
        processes.append(chromium)

    chromium_icon = Image.open(Path(realpath(__file__)).parent / "chromium.png")

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

    return icon


def is_running(cmd: str) -> bool:
    process_list = subprocess.check_output(
        ["TASKLIST", "/FI", f'imagename eq {cmd}'],
        encoding="utf-8"
    ).splitlines()
    instances = [
        process 
        for process in process_list 
        if process.startswith(cmd)
    ]
    return len(instances) > 1


def get_ports() -> tuple[int, int]:
    MAX_PORT = 2**16
    REMOTE_DEBUGGING_PORT = 1234
    PLAYWRIGHT_PROCESS_PORT= 55555
    
    arg_parser = argparse.ArgumentParser(add_help=True)
    arg_parser.add_argument("--pw-port", default=PLAYWRIGHT_PROCESS_PORT, type=int, help=f"Playwright process port (default: {PLAYWRIGHT_PROCESS_PORT})")
    arg_parser.add_argument("--cdp-port", default=REMOTE_DEBUGGING_PORT, type=int, help=f"Chromium debugging port (default: {REMOTE_DEBUGGING_PORT})")
    args = arg_parser.parse_args()
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

    assert_playwright_initialized()
    playwright_process = start_playwright(playwright_process_port)
    tray_icon = new_tray_icon([playwright_process], remote_debugging_port)
    tray_icon.run()
