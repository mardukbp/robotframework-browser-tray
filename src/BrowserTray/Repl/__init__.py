from RobotDebug.RobotDebug import RobotDebug
from robot.libraries.BuiltIn import BuiltIn


class Repl(RobotDebug):
    def __init__(self, playwright_process_port, remote_debugging_port, **kwargs):
        super().__init__(**kwargs)
        
        self.Library("Browser", "enable_presenter_mode=True", f"playwright_process_port={playwright_process_port}")
        self.connect(remote_debugging_port)

    def connect(self, remote_debugging_port):
        BuiltIn().run_keyword("Connect To Browser", f"http://localhost:{remote_debugging_port}", "chromium", "use_cdp=True")
        BuiltIn().run_keyword("Set Browser Timeout", "2s")
