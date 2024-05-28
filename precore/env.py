import precore.term as term
import precore.display as display
import precore.tasks as tasks
import uuid

class Env():
    def __init__(self, display:display.Display, term:term.TerminalReadOnly) -> None:
        self.display = display
        self.root = self.display.root
        self.canvas = self.display.canvas
        self.term = term
        self.block_tasks = False
        self.tasks_queue = []

        self.selected_text = ""
        self.selected_theme = "light"

        self.active_widgets = {}

        self.term.log("ENV", "Environnement initialized.")

    def register_widget(self, class_):
        id = str(uuid.uuid1()).replace("-", "")
        self.active_widgets[id] = {
            "class": class_
        }
        return id
    
    def check_loop(self):
        n = []
        for d in self.tasks_queue:
            if d["waiting"]:
                n.append(d)
        if len(n):
            if n[-1]["waiting"]:
                n[-1]["class"].startTask()
        self.root.after(10, self.check_loop)

    def startTaskChecking(self):
        self.term.log("ENV", "Tasks checking loop started.")
        self.root.after(0, self.check_loop)
    
    def addTask(self, func, args:tuple=tuple(), high:bool=False, prime:bool=False):
        task = tasks.Task(self, func, args, high, prime)
        task.addTask()