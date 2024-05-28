from imports import *

class Screen():
    def __init__(self, master:tk.Tk, _term:term.TerminalReadOnly, _env:env.Env, _display:display.Display) -> None:
        self.screen = tk.Canvas(master, background="black", highlightthickness=0)
        self.term = _term
        self.env = _env
        self.display = _display
        
        self.stop_mouse_loop = False
        self.cursor = self.screen.create_image(0, 0, anchor="nw")
        self.cursor_pattern = f"cursor_normal_light_normal"
        self.cursor_changed = False

    def mouse_loop(self):
        self.screen.itemconfig(self.cursor, image=self.display.images[self.cursor_pattern][1])
        while not self.stop_mouse_loop:
            if self.cursor_changed:
                self.screen.itemconfig(self.cursor, image=self.display.images[self.cursor_pattern][1])
                self.cursor_changed = False
            self.screen.moveto(self.cursor, self.screen.winfo_pointerx() - self.screen.winfo_rootx(), self.screen.winfo_pointery() - self.screen.winfo_rooty())
            self.screen.tag_raise(self.cursor)
        self.stop_mouse_loop = False
    
    def show(self):
        self.screen.pack(fill="both", expand=True)
        self.stop_mouse_loop = False
        self.env.addTask(self.mouse_loop)

    def hide(self):
        self.screen.pack_forget()
        self.stop_mouse_loop = True