*** Settings ***
Library       Browser               playwright_process_port=4711
Test Setup    Connect To Browser    http://localhost:1234            chromium     use_cdp=True

*** Test Cases ***
Test web application
    Click    "Alle akzeptieren"
