from fixtures import rfbrowser_init
import pytest

from BrowserTray.tray import TrayIcon, PLAYWRIGHT_PROCESS_PORT, REMOTE_DEBUGGING_PORT


def test_start_browser_tray(rfbrowser_init):
    with pytest.raises(expected_exception=SystemExit) as e:
        TrayIcon(PLAYWRIGHT_PROCESS_PORT, REMOTE_DEBUGGING_PORT, 4)

    assert e.value.code is 0, f"browser-tray terminated with return code {e.value.code}"
