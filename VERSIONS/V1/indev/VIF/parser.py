class VIFParser():
    def __init__(self) -> None:
        self.keys = {}
        self.types = {
            "VER", "INT", "ID", "STR", "HEX", "LONG", "CHAR", "EXT", "URL", "PATH", "PERSON", "HASH",
            "LIST", "NAME", "LINK", "URL"
        }

    def parseName(self, name:str):
        chars = [*"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"]
        lower_chars, upper_chars, numbers = chars[0:26], chars[26:26*2], chars[26*2:]
        name = name.strip()
        if not len(name):
            raise "Empty name."
        

    def parse(self, raw:str):
        pass

VIFParser().parseName("")