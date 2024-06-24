from RobotDebug.RobotDebug import RobotDebug
from robot.libraries.BuiltIn import BuiltIn


class Repl(RobotDebug):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.Library("Browser", "enable_presenter_mode=True", "playwright_process_port=4711", "timeout=2s")
        self.connect()

    def connect(self):
        BuiltIn().run_keyword("Connect To Browser", "http://localhost:1234", "chromium", "use_cdp=True")
