import precore.screen as screen
import storage.libs.cursors as cursors
import storage.libs.randid as randid
from PIL import Image, ImageTk

class Text():
    def __init__(self, _screen: screen.Screen, attributes: dict = {}) -> None:
        self.attributes = attributes
        self.screen = _screen
        self.master = self.screen.screen

        self.env = self.screen.env

        self.registered_id = self.env.register_widget(self)
        
        self.chars = []
        self.selected_text = ""

        self.start_point = None
        self.end_point = None

        self.in_select = False

        #self.id = self.master.create_text(0, 0)
        #bbox = self.master.bbox(self.id)
        self.hitbox = self.master.create_rectangle(0, 0, 0, 0, outline="")

    def set_attribute(self, key: str, value: any):
        self.attributes[key] = value

    def get_attribute(self, key: str, default: any) -> any:
        if not key.lower() in self.attributes.keys():
            return default
        return self.attributes[key.lower()]

    def show(self):
        self.update()

    def hide(self):
        for char in self.chars:
            self.master.delete(char[1])
            self.master.delete(char[4])

    def update(self):
        for char in self.chars:
            self.master.delete(char[1])
            self.master.delete(char[4])
        
        self.chars = []

        self.text = self.get_attribute("text", "TextWidget")
        self.color = self.get_attribute("color", "grey")
        self.x = self.get_attribute("x", 0)
        self.y = self.get_attribute("y", 0)
        self.anchor = self.get_attribute("anchor", "nw")
        self.size = self.get_attribute("size", 14)
        self.font = self.get_attribute("font", "Helvetica")
        self.selection = self.get_attribute("selection", True)
        self.selection_color = self.get_attribute("selection_color", "#3399FF")
        self.marge_x = self.get_attribute("marge_x", -1)
        self.marge_y = self.get_attribute("marge_y", 0)

        actual_x = 0
        actual_y = 0
        marge_x = self.marge_x
        marge_y = self.marge_y

        for char in [*self.text]:
            if not char == "\n":
                i = self.master.create_text(self.x + actual_x, self.y + actual_y, text=char, fill=self.color, font=(self.font, self.size), anchor=self.anchor)
                actual_x += self.master.bbox(i)[2] - self.master.bbox(i)[0] + marge_x
                self.chars.append([char, i, False, False])
            else:
                i = self.master.create_text(self.x + actual_x, self.y + actual_y, text=" ", fill=self.color, font=(self.font, self.size), anchor=self.anchor)
                actual_x = 0
                actual_y += self.master.bbox(i)[3] - self.master.bbox(i)[1] + marge_y
                self.chars.append([char, i, False, True])
                #                           ^ SEL  ^ OTHER LINE

        #self.master.moveto(self.id, self.x, self.y)
        #self.master.itemconfig(self.id, text=self.text, fill=self.color, font=(self.font, self.size), anchor=self.anchor)
        if len(self.chars):
            bbox1 = self.master.bbox(self.chars[0][1])
            bbox2 = self.master.bbox(self.chars[-1][1])
            max_x = bbox2[2]
            lines = [[]]
            a_i = 0
            for char in self.chars:
                lines[a_i].append(char)
                if char[3]:
                    lines.append([])
                    a_i += 1
            for line in lines:
                if len(line):
                    _bbox1 = self.master.bbox(line[0][1])
                    _bbox2 = self.master.bbox(line[-1][1])
                    _bbox = (_bbox1[0], _bbox1[1], _bbox2[2], _bbox2[3])
                    max_x = max(max_x, _bbox[2])
            bbox = (bbox1[0], bbox1[1], max_x, bbox2[3])
            self.master.coords(self.hitbox, bbox[0], bbox[1], bbox[2], bbox[3])
            self.master.itemconfig(self.hitbox)

        if len(self.chars):
            for i, char in enumerate(self.chars):
                bbox = self.master.bbox(char[1])
                j = self.master.create_rectangle(bbox[0], bbox[1], bbox[2], bbox[3], outline="")
                self.chars[i].append(j)

        if self.selection:
            self.master.bind("<Motion>", self.on_motion)
            self.master.bind("<ButtonPress-1>", self.start_selection)
            self.master.bind("<B1-Motion>", self.update_selection)
            self.master.bind("<ButtonRelease-1>", self.end_selection)
            self.master.bind("<Double-Button-1>", self.select_all)
            self.master.bind("<Escape>", self.deselect_all)

    def on_motion(self, event):
        x, y = event.x, event.y

        if self.is_over_hitbox(x, y):
            cursors.changeCursor(self.screen, "text", "light", "normal")
        else:
            cursors.changeCursor(self.screen)

    def start_selection(self, event):
        # Commencer la sélection lorsque le bouton de la souris est enfoncé
        self.in_select = True
        self.deselect_all(None)
        self.update_selection(event)

    def update_selection(self, event):
        # Mettre à jour la sélection pendant le mouvement de la souris
        if self.in_select:
            # Effacer la sélection précédente
            """for char in self.selected_chars:
                self.master.itemconfig(char[4], fill="")"""

            # Trouver les caractères sélectionnés sous la souris
            x, y = event.x, event.y
            for i, char in enumerate(self.chars):
                if self.is_over_char(x, y, char):
                    if self.start_point == None:
                        self.start_point = i
                    self.end_point = i
                    if self.end_point < self.start_point:
                        self.end_point -= 1
                    elif self.end_point > self.start_point:
                        self.end_point += 1
                    else:
                        self.end_point += 1
                    step = 1
                    if self.end_point < self.start_point:
                        step = -1
                    #print(self.chars)
                    #print(self.start_point, self.end_point, step, list(range(self.start_point, self.end_point, step)))
                    for i, char in enumerate(self.chars):
                        if self.chars[i][2] and not i in range(self.start_point, self.end_point, step):
                            self.chars[i][2] = False
                            self.master.itemconfig(char[4], fill="")
                    for h in range(self.start_point, self.end_point, step):
                        self.chars[h][2] = True
                        self.master.itemconfig(self.chars[h][4], fill=self.selection_color)
                    #self.chars[i][2] = True
                    #self.master.itemconfig(char[4], fill=self.selection_color)
                    self.updateSelectedText()
        #print(self.selected_text, [self.selected_text,])

    def end_selection(self, event):
        # Terminer la sélection lorsque le bouton de la souris est relâché
        self.in_select = False

    def deselect_all(self, event):
        # Désélectionner tous les caractères
        for i, char in enumerate(self.chars):
            self.chars[i][2] = False
            self.master.itemconfig(char[4], fill="")

        self.start_point = None
        self.end_point = None

        self.updateSelectedText()

    def select_all(self, event):
        for i, char in enumerate(self.chars):
            self.chars[i][2] = True
            self.master.itemconfig(char[4], fill=self.selection_color)

        self.start_point = None
        self.end_point = None

        self.updateSelectedText()

    def updateSelectedText(self):
        t = ""
        for char in self.chars:
            if char[2]:
                t += char[0]
                """if char[3]:
                    t += "\n"""
        self.selected_text = t

    def is_over_char(self, x, y, char):
        # Vérifier si la souris est sur un caractère
        bbox = self.master.bbox(char[1])
        char_x1, char_y1, char_x2, char_y2 = bbox
        return char_x1 <= x <= char_x2 and char_y1 <= y <= char_y2

    def is_over_hitbox(self, x, y):
        bbox = self.master.bbox(self.hitbox)
        hitbox_x1, hitbox_y1, hitbox_x2, hitbox_y2 = bbox

        return hitbox_x1 <= x <= hitbox_x2 and hitbox_y1 <= y <= hitbox_y2

    def zOrderUp(self):
        for char in self.chars:
            self.master.tag_raise(char[4])
            self.master.tag_raise(char[1])

class Button():
    def __init__(self, _screen: screen.Screen, attributes: dict = {}) -> None:
        self.attributes = attributes
        self.screen = _screen
        self.master = self.screen.screen

        self.env = self.screen.env
        self.display = self.screen.display

        self.registered_id = self.env.register_widget(self)

        self.text_widget = None
        self.button_box = None

    def check_attributes(self):
        self.text = self.get_attribute("text", "ButtonWidget")
        self.color = self.get_attribute("color", "black")
        self.selection = self.get_attribute("selection", False)
        self.x = self.get_attribute("x", 0)
        self.y = self.get_attribute("y", 0)
        self.b_marge_x = self.get_attribute("b_marge_x", 10)
        self.b_marge_y = self.get_attribute("b_marge_y", 10)

    def show(self):
        self.update()

    def hide(self):
        self.text_widget.hide()
        self.button_box.hide()

    def update(self):
        self.check_attributes()
        t_attr = self.attributes.copy()
        t_attr["text"] = self.text
        t_attr["color"] = self.color
        t_attr["selection"] = self.selection
        t_attr["x"] = self.x + self.b_marge_x
        t_attr["y"] = self.y + self.b_marge_y
        print(t_attr, self.x, self.y)
        self.text_widget = Text(self.screen, t_attr)
        self.text_widget.show()
        t_bbox = self.screen.screen.bbox(self.text_widget.hitbox)
        b_attr = self.attributes
        b_attr["width"] = t_bbox[2] - self.x + self.b_marge_x * 2
        b_attr["height"] = t_bbox[3] - self.y + self.b_marge_y * 2
        self.button_box = plan3x3(self.screen, b_attr)
        self.button_box.show()
        self.text_widget.zOrderUp()

    def set_attribute(self, key: str, value: any):
        self.attributes[key] = value

    def get_attribute(self, key: str, default: any) -> any:
        if not key.lower() in self.attributes.keys():
            return default
        return self.attributes[key.lower()]

class plan3x3():
    def __init__(self, _screen: screen.Screen, attributes: dict = {}) -> None:
        self.attributes = attributes
        self.screen = _screen
        self.master = self.screen.screen
        self.display = self.screen.display

        self.env = self.screen.env

        self.wg = []

        self.registered_id = self.env.register_widget(self)

    def check_attributes(self):
        self.x = self.get_attribute("x", 0)
        self.y = self.get_attribute("y", 0)
        self.theme = self.get_attribute("theme", self.env.selected_theme)
        self.type = self.get_attribute("type", "normal")
        self.left_top = self.get_attribute("left_top", self.display.images[f"plan_button_{self.env.selected_theme}_{self.type}_left_top"])
        self.left = self.get_attribute("left", self.display.images[f"plan_button_{self.env.selected_theme}_{self.type}_left"])
        self.left_bottom = self.get_attribute("left_bottom", self.display.images[f"plan_button_{self.env.selected_theme}_{self.type}_left_bottom"])
        self.bottom = self.get_attribute("bottom", self.display.images[f"plan_button_{self.env.selected_theme}_{self.type}_bottom"])
        self.right_bottom = self.get_attribute("right_bottom", self.display.images[f"plan_button_{self.env.selected_theme}_{self.type}_right_bottom"])
        self.right = self.get_attribute("right", self.display.images[f"plan_button_{self.env.selected_theme}_{self.type}_right"])
        self.right_top = self.get_attribute("right_top", self.display.images[f"plan_button_{self.env.selected_theme}_{self.type}_right_top"])
        self.top = self.get_attribute("top", self.display.images[f"plan_button_{self.env.selected_theme}_{self.type}_top"])
        self.middle = self.get_attribute("middle", self.display.images[f"plan_button_{self.env.selected_theme}_{self.type}_middle"])
        self.width = self.get_attribute("width", 30)
        self.height = self.get_attribute("height", 30)
        self.corners_var = {
            "left_top": self.left_top,
            "left": self.left,
            "left_bottom": self.left_bottom,
            "bottom": self.bottom,
            "right_bottom": self.right_bottom,
            "right": self.right,
            "right_top": self.right_top,
            "top": self.top,
            "middle": self.middle
        }

    def show(self):
        self.update()

    def hide(self):
        for wg in self.wg:
            self.screen.screen.delete(wg)

    def update(self):
        self.hide()
        self.check_attributes()
        self.wg = []
        im = {}
        for type, var in self.corners_var.items():
            if type in ["left", "right"]:
                d = self.corners_var[type][0].resize((self.corners_var[type][0].size[0], self.height - self.corners_var[type][0].size[0] * 3 + 1))
                e = ImageTk.PhotoImage(d)
                im[type] = [d, e]
                self.display.images[randid.RandIDv1()] = [d, e]
            elif type in ["top", "bottom"]:
                d = self.corners_var[type][0].resize((self.width, self.corners_var[type][0].size[1]))
                e = ImageTk.PhotoImage(d)
                im[type] = [d, e]
                self.display.images[randid.RandIDv1()] = [d, e]
            elif type == "middle":
                d = self.corners_var[type][0].resize((self.width, self.height - self.corners_var[type][0].size[0] * 3 + 1))
                e = ImageTk.PhotoImage(d)
                im[type] = [d, e]
                self.display.images[randid.RandIDv1()] = [d, e]
            else:
                im[type] = var
        for type, var in im.items():
            if type == "left_top":
                wg_act = self.screen.screen.create_image(self.x, self.y, image=var[1], anchor="nw")
            elif type == "left":
                wg_act = self.screen.screen.create_image(self.x, self.y + im["left_top"][0].size[0], image=var[1], anchor="nw")
            elif type == "left_bottom":
                wg_act = self.screen.screen.create_image(self.x, self.y + im["left_top"][0].size[0] + im["left"][0].size[0], image=var[1], anchor="nw")
            elif type == "bottom":
                wg_act = self.screen.screen.create_image(self.x + im["left_bottom"][0].size[0], self.y + im["left_top"][0].size[0] + im["left"][0].size[0], image=var[1], anchor="nw")
            elif type == "right_bottom":
                wg_act = self.screen.screen.create_image(self.x + im["left_bottom"][0].size[0] + im["bottom"][0].size[0], self.y + im["left_top"][0].size[0] + im["left"][0].size[0], image=var[1], anchor="nw")
            elif type == "right":
                wg_act = self.screen.screen.create_image(self.x + im["left_bottom"][0].size[0] + im["bottom"][0].size[0], self.y + im["left_top"][0].size[0], image=var[1], anchor="nw")
            elif type == "right_top":
                wg_act = self.screen.screen.create_image(self.x + im["left_bottom"][0].size[0] + im["bottom"][0].size[0], self.y, image=var[1], anchor="nw")
            elif type == "top":
                wg_act = self.screen.screen.create_image(self.x + im["left_bottom"][0].size[0], self.y, image=var[1], anchor="nw")
            elif type == "middle":
                wg_act = self.screen.screen.create_image(self.x + im["left_top"][0].size[0], self.y + im["left_top"][0].size[0], image=var[1], anchor="nw")
            self.wg.append(wg_act)

    def set_attribute(self, key: str, value: any):
        self.attributes[key] = value

    def get_attribute(self, key: str, default: any) -> any:
        if not key.lower() in self.attributes.keys():
            return default
        return self.attributes[key.lower()]