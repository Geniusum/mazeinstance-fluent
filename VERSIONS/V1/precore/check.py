import os
import precore.term as term
import precore.env as env
import precore.read_d as read_d

class Checker():
    def __init__(self, _term:term.TerminalReadOnly, _env:env.Env) -> None:
        self.script_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.storage = os.path.join(self.script_path, "storage")
        self.term = _term
        self.env = _env

        self.term.log("CHECKER", "Checker initialized.")
        self.finished = False
        self.result = True

    def check_storage(self):
        try:
            booting_d = read_d.dConfigFile(os.path.join(self.script_path, "booting.d"))
        except:
            return False
        self.storage = booting_d.get_fstring("storage").replace("~", self.script_path)
        self.term.log("CHECKER", "Checking storage folder.")
        return os.path.exists(self.storage)

    def check_boot(self):
        self.term.log("CHECKER", "Checking boot file(s).")
        try:
            booting_d = read_d.dConfigFile(os.path.join(self.script_path, "booting.d"))
        except:
            return False
        boot_path = booting_d.get_fstring("boot").replace("~", self.script_path)
        return os.path.exists(boot_path)

    def general_check_main(self):
        self.term.log("CHECKER", "Starting checking : general checking procedure.")

        is_storage_valid = self.check_storage()
        self.term.log("CHECKER RESULT", f"Checking storage result : {is_storage_valid}")
        if is_storage_valid:
            pass
        else:
            self.term.log("CHECKER ERROR", "Checking finished with an error.")
            return
        
        is_boot_valid = self.check_boot()
        self.term.log("CHECKER RESULT", f"Checking boot result : {is_boot_valid}")
        if is_boot_valid:
            pass
        else:
            self.term.log("CHECKER ERROR", "Checking finished with an error.")
            return
        
        self.term.log("CHECKER", "Checking finished : general checking procedure.")

    def general_check(self):
        self.finished = False
        self.result = True
        self.env.addTask(self.general_check_main, prime=True)