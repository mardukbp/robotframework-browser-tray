from RobotDebug.RobotDebug import RobotDebug
from robot.libraries.BuiltIn import BuiltIn
import pathlib


class BrowserRepl(RobotDebug):
    def __init__(self, jsextension=None, **kwargs):
        super().__init__(**kwargs)

        jsextension = str(pathlib.Path(__file__).parent.resolve() / jsextension).replace('\\', '\\\\')
        self.Library("Browser", "playwright_process_port=55555", f"jsextension={jsextension}") #  
        BuiltIn().run_keyword("Connect To Browser", "http://localhost:1234", "chromium", "use_cdp=True")
