#Universidad del Valle de Guatemala
#Laurelinda Gómez 19501
#Ejercicio 1
#26/07/2021

import struct 
from obj import Obj, Texture
from math1 import *
from math import sin, cos, tan



class Renderer(object):
    #Constructor
    def __init__(self, width, height):
        # Renderer de color negro
        self.width = width
        self.height = height
        self.currentColores = white
        self.current_texture = None
        self.current_texture_2 = None
        self.light = None
        self.clear()

    #def glCreateWindow(self, width, height):
      #  self.width = width
     #   self.height = height
    #    self.glClear()
    #    self.glViewport(0,0, width, height)

    # Crea el viewport
    #def glViewport(self, x, y, width, height):
     #   self.viewportX = int(x)
      #  self.viewportY = int(y)
       # self.viewportWidth = int(width)
        #self.viewportHeight = int(height)

    # color fondo
    #def glClearColor(self, r, g, b):
     #   self.clear_color = color(r, g, b)
    
    # Crea una lista 2D de pixeles y a cada valor le asigna 3 bytes de color
    # Recorre todo el ancho y altura asigna colores 
    def clear(self):
        self.framebuffer = [
            [black for x in range(self.width)]
            for y in range(self.height)
        ]
        
        self.zbuffer = [
            [-float('inf') for x in range(self.width)]
            for y in range(self.height)
        ]    

    # Creación del Bitmap
    def write(self, filename):
    #Crea un archivo BMP 
        f = open(filename, 'bw')
        #Header
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + 3*(self.width * self.height)))
        f.write(dword(0))
        f.write(dword(14 + 40))        
        # InfoHeader
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword((self.width * self.height) * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        
        #Mapa Bits
        # Color Table
        for y in range(self.height):
            for x in range(self.width):
                try:
                    f.write(self.framebuffer[y][x].toBytes())
                except:
                    pass
        f.close()

    def render(self):
        self.write('a.bmp')

    def point(self, x, y, color = None):
        self.framebuffer[y][x] = color or self.currentColores

#Basado en lo que se realizó en clase
    def line(self, A, B):
        x0 = A.x
        y0 = A.y
        x1 = B.x
        y1 = B.y
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        steep = dy > dx
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
            
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        
        offset = 0 * 2 * dx
        threshold = 0.5
        y = y0
        
        # y = mx + b
        points = []
        for x in range(x0, x1 + 1):
            if steep:
                points.append((y, x))
            else:
                points.append((x, y))
                
            offset += dy * 2 
            if offset >= threshold:
                y += 1 if y0 < y1 else -1
                threshold += 1 * 2 * dx
            
        for point in points:        
            point(*point)
    
    # se calcula la matriz 4x4 
    def transform(self, vertex):
        augmented_vertex = [
                [vertex[0]],
                [vertex[1]],
                [vertex[2]],
                [1]                
        ]        
        
        transformed_vertex = mm(self.ViewPort, mm(self.Projection, mm(self.View, mm(self.Model, augmented_vertex))))
        
        transformed_vertex = [
                (transformed_vertex[0][0]/transformed_vertex[3][0]), 
                (transformed_vertex[1][0]/transformed_vertex[3][0]), 
                (transformed_vertex[2][0]/transformed_vertex[3][0]) 
        ]
        
        return V3(*transformed_vertex)

    def load(self, filename, translate, scale, rotate):
        self.loadModelMatrix(translate, scale, rotate)
        model = Obj(filename)        
        vertex_buffer_object = []
        
        #forma de la figura triangulo o cuadrado
        for face in model.faces:
            for v in range(len(face)):
                vertex = self.transform(model.verts[face[v][0] - 1])
                vertex_buffer_object.append(vertex)
                
            if self.current_texture:
                for v in range(len(face)):
                    tvertex = V3(*model.tverts[face[v][1] - 1])
                    vertex_buffer_object.append(tvertex)
                    
            for v in range(len(face)):
                normal = V3(*model.normales[face[v][2] - 1])
                vertex_buffer_object.append(normal)
        
        self.active_vertex_array = iter(vertex_buffer_object)

    def draw_arrays(self, polygon):
        
        if polygon == 'TRIANGLES':
            try:
                while True:
                    self.triangle()
            except StopIteration:
                print('Cargando...')

    def triangle(self):
        A = next(self.active_vertex_array)
        B = next(self.active_vertex_array)
        C = next(self.active_vertex_array)
        if self.current_texture:
            tA = next(self.active_vertex_array)
            tB = next(self.active_vertex_array)
            tC = next(self.active_vertex_array)
        nA = next(self.active_vertex_array)
        nB = next(self.active_vertex_array)
        nC = next(self.active_vertex_array)
        xmin, xmax, ymin, ymax = bbox(A, B, C)
        #profunidad en z
        for x in range(xmin, xmax + 1):
            for y in range(ymin, ymax + 1):
                P = V2(x, y)
                w, v, u = barycentric(A, B, C, P)
                if w < 0 or v < 0 or u < 0:
                    continue
                if self.current_texture:
                    tx = tA.x * w + tB.x * v + tC.x * u
                    ty = tA.y * w + tB.y * v + tC.y * u
                    col = self.active_shader(
                        self,
                        triangle=(A, B, C),
                        bar=(w, v, u),
                        tex_coords=(tx, ty),
                        varying_normals=(nA, nB, nC)
                    )
                else:
                    col = self.active_shader(
                        self,
                        triangle=(A, B, C),
                        bar=(w, v, u),
                        varying_normales=(nA, nB, nC)
                    )
                z = A.z * w + B.z * v + C.z * u
                    
                if x < len(self.zbuffer) and y < len(self.zbuffer[x]) and z > self.zbuffer[x][y]:
                    self.point(x, y, col)
                    self.zbuffer[x][y] = z     
    
    def loadModelMatrix(self, translate, scale, rotate):
        translate = V3(*translate)
        scale = V3(*scale)
        rotate = V3(*rotate)
        
        translation_matrix = [
                [1, 0, 0, translate.x],
                [0, 1, 0, translate.y],
                [0, 0, 1, translate.z],
                [0, 0, 0, 1]
            ]
        
        a = rotate.x
        rotation_matrix_x = [
                [1, 0, 0, 0],
                [0, cos(a), -sin(a), 0],
                [0, sin(a), cos(a), 0],
                [0, 0, 0, 1]
            ]
        
        a = rotate.y
        rotation_matrix_y = [
                [cos(a), 0, sin(a), 0],
                [0, 1, 0, 0],
                [-sin(a), 0, cos(a), 0],
                [0, 0, 0, 1]
            ]
        
        a = rotate.z
        rotation_matrix_z = [
                [cos(a), -sin(a), 0, 0],
                [sin(a), cos(a), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ]
        
        rotation_matrix = mm(rotation_matrix_x, mm(rotation_matrix_y, rotation_matrix_z))
        
        scale_matrix = [
                [scale.x, 0, 0, 0],
                [0, scale.y, 0, 0],
                [0, 0, scale.z, 0],
                [0, 0, 0, 1]
            ]
        
        self.Model = mm(translation_matrix, mm(rotation_matrix, scale_matrix))
    

    def loadViewMatrix(self, x, y, z, center):
        M = [
                [x.x, x.y, x.z, 0],
                [y.x, y.y, y.z, 0],
                [z.x, z.y, z.z, 0],
                [0, 0, 0, 1]
            ]
        
        O = [
                [1, 0, 0, -center.x],
                [0, 1, 0, -center.y],
                [0, 0, 1, -center.z],
                [0, 0, 0, 1]
            ]
        
        self.View = mm(M, O)


    def loadProjectionMatrix(self, coeff):
        self.Projection = [
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, coeff, 1]
            ]
    
    def loadViewportMatrix(self, x = 0, y = 0):
        self.ViewPort = [
                [self.width/2, 0, 0, x + self.width/2],
                [0, self.height/2, 0, y + self.height/2],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ]

    def lookAt(self, eye, center, up):
        z = norm(sub(eye, center))
        x = norm(cross(up, z))
        y = norm(cross(z, x))
        self.loadViewMatrix(x, y, z, center)
        self.loadProjectionMatrix(-1/length(sub(eye, center)))
        self.loadViewportMatrix()

    