import precore.display as display
import precore.term as term

class RedScreen():
    def __init__(self, _display:display.Display, _term:term.TerminalReadOnly) -> None:
        self.display = _display
        self.term = _term
        
    def show(self):
        self.term.log("CRASH REPORT", "The red screen was called from a fatal error.")
        self.display.canvas.config(background="red")