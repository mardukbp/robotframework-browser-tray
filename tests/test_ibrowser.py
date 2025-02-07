import pytest

from BrowserTray.ibrowser import repl


def test_start_ibrowser_with_no_running_browser():
    with pytest.raises(SystemExit) as e:
        repl.run()

    assert e.value.code is 1, f"ibrowser terminated with return code {e.value.code}"
