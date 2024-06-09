from imports import *

class TerminalReadOnly():
    def __init__(self, master:tk.Canvas) -> None:
        self.logs = ""
        self.fill = "white"
        self.font = ("Courier", 16)
        self.columns_chrs_limit = 90
        self.lines_chrs_limit = 34
        self.master = master
        self.text = self.master.create_text(10, 10, fill=self.fill, font=self.font, text="", anchor="nw")

    def hide(self):
        self.master.itemconfig(self.text, text="")

    def show(self):
        new_log = ""
        count = 0
        for char in [*self.logs]:
            count += 1
            new_log += char
            if count >= self.columns_chrs_limit:
                new_log += "\n"
                count = 0
            if char == "\n":
                count = 0
        if len(new_log.splitlines()) >= self.lines_chrs_limit:
            new_log = "\n".join(new_log.splitlines()[len(new_log.splitlines()) - self.lines_chrs_limit:])
        self.master.itemconfig(self.text, text=new_log)

    def update(self):
        self.show()

    def log(self, type:str="LOG", log:str=""):
        type = type.upper()
        log = str(log)
        self.logs += f"[{type}] {log}\n"
        self.update()

    def jump(self, nb:int=1, spec:str="\n"):
        self.logs += spec * nb