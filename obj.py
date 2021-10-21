#Laurelinda Gómez
#19501

import struct
def color(r, g, b):
    return bytes([ int(b * 255), int(g* 255), int(r* 255)])

#En relación a lo que vimos en la clase
class Obj(object):
    def __init__(self, filename):
        with open(filename) as f:
            self.lineas = f.read().splitlines()
        self.verts = []
        self.tverts = []
        self.normales = []
        self.faces = []
        self.read()

    def read(self):
        m1 = 0
        m2 = 0
        m3 = 0
        for linea in self.lineas:
            if linea:
                try:
                    prefix, val = linea.split(' ', 1)
                except:
                    prefix =''
                if prefix =='v':
                    vert = list(map(float, val.split(' ')))
                    self.verts.append(vert)
                    if vert[0]>m2:
                        m2 = vert[0]
                    if vert[1]>m1:
                        m1 = vert[1]
                    if vert[2]>m3:
                        m3 = vert[2]
                elif prefix =='vt':
                    self.tverts.append(
                        list(map(float, val.split(' ')))
                    )
                elif prefix == 'vn':
                    self.normales.append(
                        list(map(float, val.split(' ')))
                  )
                elif prefix == 'f':
                    faces = val.split(' ')
                    if(len(faces)==3):

                        self.faces.append(
                            [list(map(int, face.split('/'))) for face in faces if len(face)>2]
                        )
                    else:
                        faces1 = [faces[0], faces[1], faces[2]]
                        faces2 = [faces[0], faces[2], faces[3]]

                        self.faces.append(
                            [list(map(int, face.split('/'))) for face in faces1 if len(face)>2]
                        )

                        self.faces.append(
                            [list(map(int, face.split('/'))) for face in faces2 if len(face)>2]
                        )

        self.vertexN = [[i[0]/m2, i[1]/m1, i[2]/m3]for i in self.verts]
        self.verts = self.vertexN

class Texture(object):
    def __init__(self, path):
        self.path = path
        self.read()
    
    def read(self):
        image = open(self.path, 'rb')
        image.seek(2 + 4 + 4)
        #header
        headerSize = struct.unpack('=l', image.read(4))[0]

        image.seek(2 + 4 + 4 + 4 + 4)
        #el ancho
        self.width = struct.unpack('=l', image.read(4))[0]
        #altura
        self.height = struct.unpack('=l', image.read(4))[0]
        image.seek(headerSize)
        self.pixels = []
        
        for y in range(self.height):
            self.pixels.append([])
            for x in range(self.width):
                b = ord(image.read(1))
                g = ord(image.read(1))
                r = ord(image.read(1))
                self.pixels[y].append(color(r, g, b))
        image.close()
        
    def get_color(self, tx, ty):
        x = int(tx * self.width)
        y = int(ty * self.height)
        try:
            return self.pixels[y][x]
        except:
            return color(0, 0, 0)
        