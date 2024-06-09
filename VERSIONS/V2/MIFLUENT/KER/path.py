import os

try:
    class PATHs:
        OS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        KER = os.path.join(OS, "KER")
        VM = os.path.join(OS, "VM")
        LIBS = os.path.join(OS, "LIBS")
        RUNNER = os.path.join(OS, "RUNNER")
except:
    raise "Directories missing."