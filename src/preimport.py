import random;
import re
from math import *

rint = random.randint
r = rint

def rdouble(a, b):
    return (b - a) * random.random()+a

def expand(matched):
    st = ord(matched.group(1))
    ed = ord(matched.group(2))
    str = ""
    for c in range(st,ed+1):
        str+=chr(c)
    return str

def rstr(chars,len):
    chars = re.sub("(.)-(.)",expand,chars)
    str = ""
    for i in range(len):
        str+=random.choice(chars)

    return str

