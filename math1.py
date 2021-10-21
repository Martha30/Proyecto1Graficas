#Laurelinda Gómez
#19501

import struct
class V3(object):
    def __init__(self, x, y, z =  None):
        self.x = x
        self.y = y
        self.z = z
        
    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        elif i == 2:
            return self.z
    
    def __repr__(self):
        return "V3(%s, %s, %s)" % (self.x, self.y, self.z)

class V2(object):
    def __init__(self, x, y =  None):
        self.x = x
        self.y = y
        
    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
    
    def __repr__(self):
        return "V2(%s, %s)" % (self.x, self.y)
    
def colores(v):
    return max(0, min(255, int(v)))
    
class color(object):
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
    
    def __repr__(self):
        b = colores(self.b)
        g = colores(self.g)
        r = colores(self.r)
        
        return "color(%s, %s, %s)" % (r, g, b)
    
    def toBytes(self):
        b = colores(self.b)
        g = colores(self.g)
        r = colores(self.r)
        
        return bytes([b, g, r])
    
    def sum1(self, other):
        r = colores(self.r + other.r)
        g = colores(self.g + other.g)
        b = colores(self.b + other.b)
        
        return color(r, g, b)
    
    def __mul__(self, k):
        r = colores(self.r * k)
        g = colores(self.g * k)
        b = colores(self.b * k)
        
        return color(r, g, b)

def bbox(A, B, C):
    xs = [A.x, B.x, C.x]
    xs.sort()
    ys = [A.y, B.y, C.y]
    ys.sort()
    return round(xs[0]), round(xs[-1]), round(ys[0]), round(ys[-1])
    
def char(c):
    #1byte
    return struct.pack('=c', c.encode('ascii'))
    
def word(w):
    #2bytes
    return struct.pack('=h', w)

def dword(dw):
     #4bytes
    return struct.pack('=l', dw)

def cross(v0, v1):
    cx = v0.y * v1.z - v0.z * v1.y
    cy = v0.z * v1.x - v0.x * v1.z
    cz = v0.x * v1.y - v0.y * v1.x
    return V3(cx, cy, cz)

def barycentric(A, B, C, P):    
    bary = cross(
        V3(C.x - A.x, B.x - A.x, A.x - P.x),
        V3(C.y - A.y, B.y - A.y, A.y - P.y)
    )

    if abs(bary.z) < 1:
        return -1, -1, -1

    return (
    1 - (bary.x + bary.y) / bary.z,
    bary.y / bary.z,
    bary.x / bary.z
    )

def sub(v0, v1):
    return V3(
        v0.x - v1.x,
        v0.y - v1.y,
        v0.z - v1.z
    )

def length(v0):
    return (v0.x**2 + v0.y**2 + v0.z**2) ** 0.5

def norm(v0):
    l = length(v0)
    
    if l == 0:
        return V3(0, 0, 0)
    
    return V3(
        v0.x / l,
        v0.y / l,
        v0.z / l
    )

def dot(v0, v1):
    return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

def mm(M1, M2):
    result = [[sum(a*b for a,b in zip(X_row,Y_col)) for Y_col in zip(*M2)] for X_row in M1]
    return result

black = color(0, 0, 0)
white = color(255, 255, 255)

