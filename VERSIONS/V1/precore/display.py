from imports import *

script_path = os.path.dirname(os.path.abspath(__file__))

class Display():
    def __init__(self, width:int=1200, height:int=800, fullscreen:bool=False) -> None:
        self.root = tk.Tk()
        self.root.config(cursor="none")
        self.width = width
        self.height = height
        if fullscreen:
            self.root.attributes("-fullscreen", True) # FULLSCREEN
        self.images = {}
        self.config_d = read_d.dConfigFile(os.path.join(script_path, "config.d"))
        self.root.title(self.config_d.get_fstring("title"))
        self.canvas = tk.Canvas(self.root, background="black", highlightthickness=0, width=self.width, height=self.height)
        self.resizable = self.config_d.get_value("resize")
        if self.resizable:
            self.resizable = 1
        else:
            self.resizable = False
        self.root.resizable(self.resizable, self.resizable)
        self.canvas.place(x=0, y=0)
        self.changeSize(width, height)
        self.root.bind("<Configure>", self.onWindowResize)
        
    def changeSize(self, width:int=1200, height:int=1200, n:bool=True):
        self.width = width
        self.height = height
        self.updateSize(n)
    
    def updateSize(self, n:bool=True):
        if n: self.root.geometry(f"{self.width}x{self.height}")
        self.canvas.config(width=self.width, height=self.height)

    def onWindowResize(self, event):
        self.changeSize(event.width, event.height, False)

    def runWindow(self):
        self.root.mainloop()

    def addProcedure(self, func, delay:int=0) -> None:
        self.root.after(delay, func)