import precore.display as display
import tkinter as tk
from PIL import ImageTk

def animate_logo_image(pattern:str, frame:int, _display:display.Display, screen:tk.Canvas, screen_image:int):
    images_list = _display.images
    pattern = pattern.replace("#nb", str(frame))
    if pattern in images_list:
        image = images_list[pattern][0]
        image_tk = images_list[pattern][1]
        screen.moveto(screen_image, int(screen.winfo_width() / 2 - image.size[0] / 2), int(screen.winfo_height() / 2 - image.size[1] / 2))
        screen.itemconfig(screen_image, image=image_tk)

def animate_image(pattern:str, frame:int, _display:display.Display, screen:tk.Canvas, screen_image:int):
    images_list = _display.images
    pattern = pattern.replace("#nb", str(frame))
    if pattern in images_list:
        image_tk = images_list[pattern][1]
        screen.itemconfig(screen_image, image=image_tk)