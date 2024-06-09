import precore.term as term
import precore.env as env
import precore.read_d as read_d
import precore.display as display
import precore.screen as screen
import storage.system.core.os as os_
import os
import copy
import time
from PIL import Image, ImageTk, ImageFilter
import storage.libs.imgs as imgs
import storage.libs.temp as temp

class preboot():
    def __init__(self, _display:display.Display, _term:term.TerminalReadOnly, _env:env.Env) -> None:
        self.display = _display
        self.term = _term
        self.env = _env
        self.d_os_info = read_d.dConfigFile(read_d.dPath("os_info.d"))
        self.script_path = os.path.dirname(os.path.abspath(__file__))

    def instance_os(self):
        self.env.os = os_.OS(self.display, self.term, self.env)
        self.os = self.env.os
    
    def gen_wallpaper_effects(self):
        images = 30
        actual_opacity = 100
        actual_blur = 0
        wallpaper_path = read_d.dConfigFile(os.path.join(os.path.dirname(os.path.dirname(self.script_path)), "data", "users", "users.d")).get_fstring(self.os.user_selected)["wallpaper"].replace("~", os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(self.script_path)))))
        temp_path = os.path.join(os.path.dirname(os.path.dirname(self.script_path)), "temp")
        for image in range(images):
            image += 1
            def mk(image:int, actual_blur:int, actual_opacity:int):
                if self.os.cpu_percent >= 200.0:
                    time.sleep(0.2)
                wallpaper_img = Image.open(wallpaper_path)
                actual_img = wallpaper_img.convert("RGB")
                if self.os.cpu_percent >= 200.0:
                    time.sleep(0.1)
                actual_img = actual_img.filter(ImageFilter.GaussianBlur(actual_blur))
                actual_img = actual_img.resize((self.display.root.winfo_width(), self.display.root.winfo_height()))
                #actual_img = imgs.change_opacity(actual_img, actual_opacity * 100)
                if self.os.cpu_percent >= 200.0:
                    time.sleep(0.2)
                actual_img.save(os.path.join(temp_path, f"wallpaper_{self.os.user_selected}_effect_1_img_{image}.png"), format="PNG")
                if self.os.cpu_percent >= 200.0:
                    time.sleep(0.1)
                self.display.images[f"wallpaper_{self.os.user_selected}_effect_1_img_{image}"] = [actual_img, ImageTk.PhotoImage(actual_img)]
            self.env.addTask(mk, (image, actual_blur, actual_opacity))
            time.sleep(0.6)
            actual_blur += 1
            actual_opacity -= 1

    def gen_buttons_corners(self):
        def absoluteFilePaths(directory):
            g = []
            for dirpath,_,filenames in os.walk(directory):
                for f in filenames:
                    g.append(os.path.abspath(os.path.join(dirpath, f)))
            return g
        buttons_path = os.path.join(os.path.dirname(os.path.dirname(self.script_path)), "assets", "plans", "buttons")
        buttons_paths = []
        types = ["light/normal"]
        for type in types:
            path = os.path.join(buttons_path, type)
            buttons_paths.append([path, type])
        for button_path in buttons_paths:
            type = button_path[1]
            button_path = button_path[0]
            abs = absoluteFilePaths(button_path)
            for path in abs:
                img = Image.open(path)
                name = os.path.splitext(os.path.basename(path))[0]
                self.display.images[f"plan_button_{type.replace("/", "_")}_{name}"] = [img, ImageTk.PhotoImage(img)]

    def gen_cursors(self):
        def absoluteFilePaths(directory):
            g = []
            for dirpath,_,filenames in os.walk(directory):
                for f in filenames:
                    g.append(os.path.abspath(os.path.join(dirpath, f)))
            return g
        cursors_path = os.path.join(os.path.dirname(os.path.dirname(self.script_path)), "assets", "cursors")
        cursors_paths = absoluteFilePaths(cursors_path)
        formats = {
            "normal": (28, 28)
        }
        for cursor in cursors_paths:
            img = Image.open(cursor)
            name = os.path.splitext(os.path.basename(cursor))[0]
            
            for format_name, format in formats.items():
                _ = img.resize(format)
                self.display.images[f"cursor_{name}_{format_name}"] = [_, ImageTk.PhotoImage(_)]

    def load_images_anim(self, path_pattern:str, max:int, resize_divider:int=1):
        for nb in range(max):
            nb += 1
            def mk(nb:int):
                path = path_pattern.replace("#nb", str(nb))
                name = os.path.splitext(os.path.basename(path))[0]
                img = Image.open(path)
                if resize_divider != 1:
                    img = img.resize((int(img.size[0] / resize_divider), int(img.size[1] / resize_divider)))
                anim_name = os.path.basename(os.path.dirname(path))
                name = name.replace(" ", "_")
                self.display.images["anim_" + anim_name + "_" + name] = [img, ImageTk.PhotoImage(img)]
            self.env.addTask(mk, (nb,))
        for mpath in ["mg_logo.png", "text.png"]:
            def mk(mpath:str):
                path = os.path.join(os.path.dirname(os.path.dirname(self.script_path)), "assets", "anims", "opv", mpath)
                name = os.path.splitext(os.path.basename(path))[0]
                img = Image.open(path)
                if resize_divider != 1:
                    img = img.resize((int(img.size[0] / resize_divider), int(img.size[1] / resize_divider)))
                anim_name = os.path.basename(os.path.dirname(path))
                name = name.replace(" ", "_")
                self.display.images["anim_" + anim_name + "_" + name] = [img, ImageTk.PhotoImage(img)]
            self.env.addTask(mk, (mpath,))

    def proc_(self):
        self.term.log("PRE-BOOT", f"{self.d_os_info.get_fstring("prename")} {self.d_os_info.get_fstring("name")} pre-boot called.")
        self.term.log("PRE-BOOT", "Instancing OS class on environnement.")
        self.instance_os()
        self.term.log("PRE-BOOT", "Generating cursors in formats.")
        self.gen_cursors()
        self.term.log("PRE-BOOT", "Loading load screen assets.")
        self.load_images_anim(os.path.join(os.path.dirname(os.path.dirname(self.script_path)), "assets", "anims", "mg_logo", "frame #nb.png"), 19, 2)
        self.term.log("PRE-BOOT", "Showing load screen.")
        self.os.show_screen()
        self.os.load_mg_screen()
        self.term.log("PRE-BOOT", "Cleaning temp folder.")
        temp.clear_temp()
        self.term.log("PRE-BOOT", "Generating wallpaper effects in temp folder.")
        self.gen_wallpaper_effects()
        self.term.log("PRE-BOOT", "Generating buttons plan textures in temp folder.")
        self.gen_buttons_corners()
        self.os.load_mg_screen_stop = True
        self.os.screen.hide()
        self.term.log("PRE-BOOT", "Pre-boot was finished. Starting booting...")
        time.sleep(1)
        self.os.screen.show()
        self.term.log("BOOT", "Starting boot.")
        boot(self.display, self.term, self.env).start()
        self.term.log("BOOT", "Boot call finished.")

    def start(self):
        self.env.addTask(self.proc_, prime=True)

class boot():
    def __init__(self, _display:display.Display, _term:term.TerminalReadOnly, _env:env.Env) -> None:
        self.display = _display
        self.term = _term
        self.env = _env
        self.os = self.env.os
        self.d_os_info = read_d.dConfigFile(read_d.dPath("os_info.d"))
        self.script_path = os.path.dirname(os.path.abspath(__file__))

    def start(self):
        self.env.addTask(self.os.start, high=True)