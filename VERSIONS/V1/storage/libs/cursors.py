import precore.display as display
import precore.screen as screen

def changeCursor(_screen:screen.Screen, type:str="normal", mode:str="light", size_mode:str="normal"):
    _screen.cursor_pattern = f"cursor_{type}_{mode}_{size_mode}"
    _screen.cursor_changed = True