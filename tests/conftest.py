import pytest
import subprocess


@pytest.fixture(scope="session", autouse=True)
def rfbrowser_init():
    subprocess.run("npm.cmd config set cache C:\\tmp\\nodejs\\npm-cache --global")
    subprocess.run("rfbrowser clean-node")
    subprocess.run("rfbrowser init chromium")
