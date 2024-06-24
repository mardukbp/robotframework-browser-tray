import pytest

from BrowserTray.tray import TrayIcon, PLAYWRIGHT_PROCESS_PORT, REMOTE_DEBUGGING_PORT
from BrowserTray.Repl import repl


@pytest.fixture(scope="function", autouse=True)
def tray_icon():
    icon = TrayIcon(PLAYWRIGHT_PROCESS_PORT, REMOTE_DEBUGGING_PORT)
    yield icon
    icon.exit()


def test_start_ibrowser_with_running_browser(tray_icon):
    with pytest.raises(SystemExit) as e:
        tray_icon.open_chromium()
        repl.run(4)

    assert e.value.code is 0, f"ibrowser terminated with return code {e.value.code}"


def test_start_ibrowser_with_no_running_browser(tray_icon):
    with pytest.raises(SystemExit) as e:
        repl.run(4)

    assert e.value.code is 1, f"ibrowser terminated with return code {e.value.code}"
