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

3. Click on the tray icon with the Chromium logo

4. Open a Terminal and execute `ibrowser`

**Hint**: In case your environment does not allow executing ibrowser, call the Python module directly:

```bash
python -m BrowserTray.BrowserRepl
```

### ibrowser

ibrowser allows testing selectors in an open web page interactively. In addition to the selectors supported by Browser library,
it adds the selector `role` for selecting elements using their ARIA role.

The role of an element can be easily obtained from the Accessibility Tree. To open the tree follow these steps:

1. Press F12 to open the DevTools
2. Select the Elements tab
3. In the right panel click on the Accessibility tab
4. In the section "Accessibility Tree" check "Enable full-page accessibility tree"
5. Click the button "Reload DevTools"
6. In the left panel click on the person icon to toggle the Accessibility Tree view


### Usage in a Robot Framework Test Suite

Add these lines to the top of the .robot file:

```robotframework
Library       Browser               playwright_process_port=55555
Test Setup    Connect To Browser    http://localhost:1234            chromium    use_cdp=True
```

In order to use other ports execute:

```bash
browser-tray --pw-port=XXXX --cdp-port=XXXX
``` 


### Using Microsoft Edge

If Microsoft Edge is installed on your machine:

1. Close all instances of Microsoft Edge

```powershell
taskkill /F /IM msedge.exe
```

2. Start Microsoft Edge with `Windows + R`

```powershell
msedge.exe --remote-debugging-port=1234
```


## How it works

On start up it checks whether `rfbrowser init chromium` has been executed in the current environment.

If this requirement is met the Playwright wrapper is started with `node site-packages/Browser/wrapper/index.js 55555`.

Selecting "Open Chromium" in the tray icon executes `site-packages/Browser/wrapper/node_modules/playwright-core/.local-browsers/chromium-XX/chrome-win/chrome.exe --remote-debugging-port=1234 --test-type`.

`ibrowser` is a batteries-included irobot that imports Browser library, connects to Chromium (if it is running) and adds some convenient selectors.
