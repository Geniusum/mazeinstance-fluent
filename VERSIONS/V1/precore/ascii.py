import os

class Ascii():
    def __init__(self, name:str) -> None:
        self.ascii = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ascii", f"{name}.txt"), encoding="utf-8").read()