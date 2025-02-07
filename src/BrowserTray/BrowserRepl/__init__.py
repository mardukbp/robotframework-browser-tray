from RobotDebug.RobotDebug import RobotDebug
from robot.libraries.BuiltIn import BuiltIn


class BrowserRepl(RobotDebug):
    def __init__(self, remote_debugging_port, **kwargs):
        super().__init__(**kwargs)
        
        self.remote_debugging_port = remote_debugging_port
        self.Library("Browser", "enable_presenter_mode=True")
        self.connect()

    def connect(self):
        BuiltIn().run_keyword("Connect To Browser", f"http://localhost:{self.remote_debugging_port}", "chromium", "use_cdp=True")
        BuiltIn().run_keyword("Set Browser Timeout", "2s")
