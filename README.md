# robotframework-browser-tray

A tray icon for starting the Chromium installed by [Browser Library](https://robotframework-browser.org/)


## Why

Write tests for a web application iteratively.


## How

Add these lines to the top of the .robot file with your tests:

```robotframework
Library       Browser               playwright_process_port=55555
Test Setup    Connect To Browser    http://localhost:1234            chromium    use_cdp=True
```

- Use [irobot](https://pypi.org/project/robotframework-debug/) to interactively test selectors in an open web page

- Incrementally execute tests using e.g. [RobotCode](https://github.com/d-biehl/robotcode)


## Requirements 

- Python >= 3.8.2
- NodeJS >= 18
- Windows


## Installation

```bash
pip install robotframework-browser-tray
```
