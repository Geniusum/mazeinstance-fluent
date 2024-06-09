import precore.term as term
import precore.env as env
import precore.read_d as read_d
import precore.display as display
import precore.screen as screen
import storage.libs.animations as animations
import time
import psutil
import storage.libs.widgets as widgets

psutil.cpu_count()
p = psutil.Process()

class OS():
    def __init__(self, _display:display.Display, _term:term.TerminalReadOnly, _env:env.Env) -> None:
        self.user_selected = "default"
        self.display = _display
        self.term = _term
        self.env = _env

        self.term.log("OS", "OS instancied.")
        self.term.log("OS", "Making screen instance.")
        self.display.screen = screen.Screen(self.display.root, self.term, self.env, self.display)
        self.screen = self.display.screen
        self.cpu_percent = p.cpu_percent()

        self.load_mg_screen_stop = False
        self.bef_ld_mg_screen_stop = False

        self.update_cpu_percent()

    def update_cpu_percent(self):
        def update():
            while True:
                self.cpu_percent = p.cpu_percent()
                time.sleep(0.2)
        self.env.addTask(update, high=True)

    def show_screen(self):
        self.screen.show()

    def hide_screen(self):
        self.screen.hide()

    def load_mg_screen_proc(self):
        frame = 0
        max_frame = 19
        fps = 14
        img = self.screen.screen.create_image(0, 0, anchor="nw")
        cpu_counter = self.screen.screen.create_text(10, 10, font=("Consolas", 12), fill="white", anchor="nw")
        tasks_counter = self.screen.screen.create_text(10, self.screen.screen.bbox(cpu_counter)[3] + 4, font=("Consolas", 12), fill="white", anchor="nw")
        mem_counter = self.screen.screen.create_text(10, self.screen.screen.bbox(tasks_counter)[3] + 4, font=("Consolas", 12), fill="white", anchor="nw")
        logs_counter = self.screen.screen.create_text(10, self.screen.screen.bbox(mem_counter)[3] + 4, font=("Consolas", 12), fill="white", anchor="nw")
        while not self.load_mg_screen_stop:
            frame += 1
            if (frame % 2) == 0:
                self.screen.screen.itemconfig(cpu_counter, text=f"CPU : {p.cpu_percent()}%")
                self.screen.screen.itemconfig(tasks_counter, text=f"Tasks : {len(self.env.tasks_queue)}")
                self.screen.screen.itemconfig(mem_counter, text=f"Memory : {round(p.memory_percent(), 4)}%")
                self.screen.screen.itemconfig(logs_counter, text=f"Logs : Lns : {len(self.term.logs.splitlines())} ; Chrs : {len(self.term.logs)}")
            animations.animate_logo_image("anim_mg_logo_frame_#nb", frame, self.display, self.screen.screen, img)
            if frame >= max_frame:
                frame = 0
            time.sleep((60 / fps) / 100)
        self.screen.screen.delete(cpu_counter)
        self.screen.screen.delete(tasks_counter)
        self.screen.screen.delete(mem_counter)
        self.screen.screen.delete(logs_counter)
        self.screen.screen.delete(img)

    def bef_ld_mg_screen_proc(self):
        def calc(frame, max):
            r = max / 2
            if frame < (max / 2):
                r += max / 2 - frame
            elif frame >= (max / 2):
                r -= max / 2 - frame
            return r * 1 / max
        
        self.screen.screen.config(background="#FFE500")
    
        images_list = self.display.images

        mg_logo_img = images_list["anim_opv_mg_logo"]

        opv_img = images_list["anim_opv_text"]
        
        mg_logo = self.screen.screen.create_image(int(self.display.width / 2 - mg_logo_img[0].size[0] / 2), int(self.display.height / 2 - mg_logo_img[0].size[1] / 2), image=mg_logo_img[1], anchor="nw")

        def anim_1():
            last_x = self.display.width
            center_x = int(self.display.width / 2 - mg_logo_img[0].size[0] / 2)
            fps = 14
            while last_x > center_x:
                ease = calc(last_x, center_x)
                x = last_x - 10
                self.screen.screen.coords(mg_logo, x, int(self.display.height / 2 - mg_logo_img[0].size[1] / 2))
                self.env.root.update()
                last_x = x
                time_to_wait = (60 / fps) / 100 * ease
                self.env.root.after(int(time_to_wait * 100))
        
        self.env.addTask(anim_1)

        """self.env.root.after(3000)

        self."""

    def check_bef_ld_mg_screen_end(self):
        """while not self.bef_ld_mg_screen_stop:
            pass
        self.load_mg_screen_stop = False
        self.env.addTask(self.load_mg_screen_proc)"""

    def load_mg_screen(self):
        self.bef_ld_mg_screen_stop = False
        self.env.addTask(self.bef_ld_mg_screen_proc)
        self.env.addTask(self.check_bef_ld_mg_screen_end)

    def bef_screen(self):
        img = self.screen.screen.create_image(0, 0, anchor="nw")
        fps = 14
        max_frame = 30

        def calc(frame, max):
            r = max / 2
            if frame < (max / 2):
                r += max / 2 - frame
            elif frame >= (max / 2):
                r -= max / 2 - frame
            return r * 1 / max

        for frame in range(max_frame):
            eased = calc(frame, max_frame)
            animations.animate_image(f"wallpaper_{self.user_selected}_effect_1_img_#nb", frame, self.display, self.screen.screen, img)
            time.sleep((60 / fps) / 100 * eased)

        #w = widgets.Text(self.screen, {"color": "white", "x": 30, "y": 30, "text": """Lorem ipsum dolor sit, amet consectetur adipisicing elit. Consequatur architecto 
#cumque dolorum libero necessitatibus, voluptas debitis nulla laboriosam! Laudantium 
#provident hic repellendus id dicta ducimus fugiat. Esse, ut. Architecto, ducimus."""})
        #w.show()
        #w.zOrderUp()

        #h = widgets.Text(self.screen, {"color": "white", "x": 300, "y": 30, "text": "Hello, world !\nI'm a text !"})
        #h.show()
        #h.zOrderUp()

        i = widgets.Button(self.screen, {"x": 80, "y": 80})
        i.show()

    def start(self):
        self.bef_screen()