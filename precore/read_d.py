import os

class dConfigFile():
    def __init__(self, path:str) -> None:
        self.path = path

    def read(self) -> str:
        return open(self.path).read()
    
    def get(self) -> dict:
        return dict(eval(self.read()))
    
    def get_value(self, key:str) -> any:
        return self.get()[key]
    
    def key_exists(self, key:str):
        c = self.get()
        if key in c.keys():
            return True
        return False
    
    def key_value_exists(self, key:str):
        c = self.get()
        if key in c.keys():
            if c[key]:
                return True
        return False
    
    def write(self, new:str) -> None:
        f = open(self.path, "w")
        f.write(new)
        f.close()
    
    def edit(self, key:str, value:any) -> None:
        c = self.get()
        c[key] = value
        self.write(str(c))

    def get_fstring(self, key__:str) -> str:
        c = self.get()
        ref = {}
        if self.key_exists(key__):
            for key, value in c.items():
                if not key in ref.keys():
                    ref[f"#{key}"] = value
            for key, value in c.items():
                if type(c[key]) == str:
                    for key_, value_ in ref.items():
                        c[key] = c[key].replace(key_, str(value_))
            return c[key__]
        else:
            return None
        
def dPath(*args):
    script_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_path, *args)