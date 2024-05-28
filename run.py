import random as rd
from imports import *

script_path = os.path.dirname(os.path.abspath(__file__))

PRE_DELAY = 2000

ins = display.Display(1200, 800)
term = term.TerminalReadOnly(ins.canvas)
term.logs += ascii_m.Ascii("vm").ascii + "\n" + read_d.dConfigFile(os.path.join(script_path, "precore", "identity.d")).get_fstring("title")
term.jump(2)
term.log("VM", "Virtual Machine was just started.")
term.log("VM VERSION", ins.config_d.get_fstring("title"))
term.log("OS INFO", "Getting OS info...")
os_info = read_d.dConfigFile(os.path.join(script_path, "precore", "os_info.d"))
term.log("OS INFO", f"OS : {os_info.get_fstring("title")}")
term.jump()
term.log("INFO", f"/!\\ Don't turn off the Virtual Machine out of the OS special shutdown function. /!\\")
term.log("DELAY", "Waiting procedure...")
term.log("DELAY", f"Waiting delay of {PRE_DELAY} ms before continue...")

def os():
    os_env = env.Env(ins, term)
    os_env.startTaskChecking()
    checker = check.Checker(term, os_env)
    checker.general_check()
    booter = boot.Boot(ins, term, os_env)
    booter.procedure()

ins.addProcedure(os, PRE_DELAY)
ins.runWindow()