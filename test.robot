*** Settings ***
Library       Browser
Library       RobotDebug
Test Setup    Connect To Browser    http://localhost:1234    chromium    use_cdp=True


*** Keywords ***
Start Edge with Remote Debugging
    New Browser    chromium    channel=msedge    args=["--remote-debugging-port=1234"]


*** Test Cases ***
Test web application
    Debug
