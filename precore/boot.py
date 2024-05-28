import precore.term as term
import precore.env as env
import precore.read_d as read_d
import precore.display as display
import os

class Boot():
    def __init__(self, _display:display.Display, _term:term.TerminalReadOnly, _env:env.Env) -> None:
        self.script_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.storage = os.path.join(self.script_path, "storage")
        self.display = _display
        self.term = _term
        self.env = _env

    def boot(self):
        exec(read_d.dConfigFile(os.path.join(self.script_path, "booting.d")).get_fstring("boot_import"), globals())
        preboot = osboot.boot(self.display, self.term, self.env)
        preboot.start()

    def preboot(self):
        exec(read_d.dConfigFile(os.path.join(self.script_path, "booting.d")).get_fstring("boot_import"), globals())
        preboot = osboot.preboot(self.display, self.term, self.env)
        preboot.start()

    def proc_(self):
        self.term.log("PRE-BOOT", "Starting pre-boot.")
        self.preboot()
        self.term.log("PRE-BOOT", "Pre-boot call finished.")

    def procedure(self):
        self.env.addTask(self.proc_, prime=True)