import pytest
import subprocess


@pytest.fixture(scope="session", autouse=True)
def rfbrowser_init():
    subprocess.run("rfbrowser init chromium")
