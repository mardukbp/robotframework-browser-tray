# robotframework-browser-tray

A tray icon for starting the Chromium installed by [Browser Library](https://robotframework-browser.org/)

**Requirements**

- NodeJS >= 18
- Windows


## Use Cases

- Execute tests incrementally using e.g. [RobotCode](https://github.com/d-biehl/robotcode)

- Test selectors in an open web page interactively using [irobot](https://pypi.org/project/robotframework-debug/)


## How to use it

1. Install the package

```bash
pip install robotframework-browser-tray
```

2. Execute `browser-tray`

**Hint**: In case your environment does not allow executing browser-tray, call the Python module directly:

```bash
python -m BrowserTray
```

3a. Click on the tray icon with the Chromium logo and select `Open Chromium`

3b. If Microsoft Edge is installed on your machine:

1. Close all instances of Microsoft Edge

```powershell
taskkill /F /IM msedge.exe
```

2. Start Microsoft Edge with `Windows + R`

```powershell
msedge.exe --remote-debugging-port=1234
```

4. Add these lines to the top of the .robot file with your tests:

```robotframework
Library       Browser               playwright_process_port=55555
Test Setup    Connect To Browser    http://localhost:1234            chromium    use_cdp=True
```

In order to use other ports execute:

```bash
browser-tray --pw-port=XXXX --cdp-port=XXXX
``` 

## How it works

On start up it checks whether `rfbrowser init chromium` has been executed in the current environment.

If this requirement is met the Playwright wrapper is started with `node site-packages/Browser/wrapper/index.js 55555`.

Selecting "Open Chromium" in the tray icon executes `site-packages/Browser/wrapper/node_modules/playwright-core/.local-browsers/chromium-XX/chrome-win/chrome.exe --remote-debugging-port=1234 --test-type`.
