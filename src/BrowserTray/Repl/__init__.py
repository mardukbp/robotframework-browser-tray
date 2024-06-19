import pathlib

from RobotDebug.RobotDebug import RobotDebug
from robot.libraries.BuiltIn import BuiltIn


class Repl(RobotDebug):
    def __init__(self, jsextension=None, **kwargs):
        super().__init__(**kwargs)

        jsextension = str(pathlib.Path(__file__).parent.resolve() / jsextension).replace('\\', '\\\\')
        self.Library("Browser", "enable_presenter_mode=True", "playwright_process_port=55555", f"jsextension={jsextension}") #  
        BuiltIn().run_keyword("Connect To Browser", "http://localhost:1234", "chromium", "use_cdp=True")
