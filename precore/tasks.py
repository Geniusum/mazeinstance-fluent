import threading as th
import uuid

class Task():
    def __init__(self, preself, func, args:tuple=tuple(), high:bool=False, prime:bool=False):
        self.preself = preself

        self.task = {
            "class": self,
            "high": high,
            "prime": prime,
            "func": func,
            "args": args,
            "waiting": True,
            "id": str(uuid.uuid1()).replace("-", "")
        }

    def addTask(self):
        if not self.preself.block_tasks:
            if self.task["high"]:
                self.preself.tasks_queue.append(self.task)
            else:
                self.preself.tasks_queue.insert(0, self.task)
            self.preself.term.log("TASK", f"The task {self.task["id"]} was been queued. High : {self.task["high"]} ; Prime : {self.task["prime"]}")
        else:
            if self.task["prime"]:
                if self.task["high"]:
                    self.preself.tasks_queue.append(self.task)
                else:
                    self.preself.tasks_queue.insert(0, self.task)
                self.preself.term.log("TASK", f"The task {self.task["id"]} was been queued. High : {self.task["high"]} ; Prime : {self.task["prime"]}")
            else:
                self.preself.term.log("ERROR", f"The task {self.task["id"]} want to enter in the tasks queue but it's blocked.")

    def waitTaskEnd(self):
        self.thread.join()
        for i, task in enumerate(self.preself.tasks_queue):
            if task["id"] == self.task["id"]:
                self.preself.tasks_queue.pop(i)
                break
        self.preself.term.log("TASK", f"The task {self.task["id"]} was been ended.")


    def startTask(self):
        self.task["waiting"] = False
        if not self.preself.block_tasks:
            self.thread = th.Thread(target=self.task["func"], args=self.task["args"])
            self.thread.start()
            self.preself.term.log("TASK", f"The task {self.task["id"]} was been started. High : {self.task["high"]} ; Prime : {self.task["prime"]}")
            th.Thread(target=self.waitTaskEnd).start()
        else:
            if self.task["prime"]:
                self.thread = th.Thread(target=self.task["func"], args=self.task["args"])
                self.thread.start()
                self.preself.term.log("TASK", f"The task {self.task["id"]} was been started. High : {self.task["high"]} ; Prime : {self.task["prime"]}")
                th.Thread(target=self.waitTaskEnd).start()
            else:
                self.preself.term.log("ERROR", f"The task {self.task["id"]} want to be started but the tasks queue blocked.")