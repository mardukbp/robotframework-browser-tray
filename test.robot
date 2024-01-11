*** Settings ***
Library       Browser               playwright_process_port=55555
Test Setup    Connect To Browser    http://localhost:1234            chromium     use_cdp=True

*** Test Cases ***
Test web application
    Click    "Alle akzeptieren"
