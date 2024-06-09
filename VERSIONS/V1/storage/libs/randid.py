import uuid
import random

def RandIDv1():
    j = [*str(uuid.uuid1()).replace("-", "")]
    random.shuffle(j)
    for i in range(random.randint(1, 80)):
        j += hex(random.randint(1, 80)).replace("0x", "")
    random.shuffle(j)
    j = "".join(j)
    return j