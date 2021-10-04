#Universidad del Valle de Guatemala
#Laurelinda Gómez 19501


import struct
import collections
import math
from random import randint as random
from random import uniform as randomDec
from obj import ObjReader

def word(w):
  # 2 byte
  return struct.pack('=h', w)
def char(c):
  return struct.pack('=c',c.encode('ascii'))
def dword(d):
  # 4 bytes
  return struct.pack('=l', d)
def color(r, g, b):
  return bytes([b, g, r]) 

#MIS VARIABLES GLOBALES
BLACK = color(3, 3, 3)
WHITE = color(255, 255, 255)
RED = color(255, 0, 0)



class Renderer(object):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.current_color = WHITE
    self.glclear()
    self.light = (0,0,1)
    self.active_texture = None
    self.active_shader  = None
    self.active_vertex_array = []


#(05 puntos) Deben crear una función glInit() que inicialice cualquier objeto interno que requiera su software renderer
  def glInit():
    pass

#05 puntos) Deben crear una función glCreateWindow(width, height) que inicialice su framebuffer con un tamaño (la imagen resultante va a ser de este tamaño
  def glCreateWindow(self,width, height):
    self.width = width
    self.height = height
    self.Clear()
    self.glViewPort(0, 0, width, height)

#(10 puntos)  Deben crear una función glViewPort(x, y, width, height) que defina el área de la imagen sobre la que se va a poder dibujar (hint)
  def glViewPort(self, x, y, width, height):
    self.viewPortX = x
    self.viewPortY = y
    self.viewPortWidth = width
    self.viewPortHeight = height

#(20 puntos) Deben crear una función glClear() que llene el mapa de bits con un solo color
  def clear(self):
    self.buffer = [
      [WHITE for x in range(self.width)] 
      for y in range(self.height)
    ]
    self.zbuffer = [
      [-float('inf') for x in range(self.width)] 
      for y in range(self.height)
    ]

#(10 puntos) Deben crear una función glClearColor(r, g, b) con la que se pueda cambiar el color con el que funciona glClear(). Los parámetros deben ser números en el rango de 0 a 1.
  def glClearColor(self, r, g, b):
    self.clearColor = color(r, g, b)

#(15 puntos) Deben crear una función glColor(r, g, b) con la que se pueda cambiar el color con el que funciona glVertex(). Los parámetros deben ser números en el rango de 0 a 1.
  def glColor(self, r, g, b):
    self.current_color= color(r,g,b)

 
  def render(self):
   
#--Funcion para pintar un pixel
#--Un punto de un color en especidico, coordenadas en x,y y algun color
  def point(self, x, y, color = None):
    self.framebuffer[y][x] = color or self.current_color
  
  #Creación de la función glLine
  def glLine(self, a1, a0, color = None ):
    x0 = a0.x
    x1 = a1.x
    y0 = a0.y
    y1 = a1.y

    #La pendiente de la línea
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    t = dy > dx
    
    if t:
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        

    if x0 > x1:
        x0, y0 = y0, x0
        x1, y1 = y1, x1
    
    dy = abs(y1 - y0)
    dx = abs(y1 - x0)

    offset = 0
    threshold = dx

    y = y0
    for x in range(x0, x1 + 1):
        if t:
            self.point(y, x)
        else:
            self.point(x, y)
        
        offset += dy * 2
        if offset >= threshold:
            y += 1 if y0 < y1 else -1
            threshold += dx * 2

    def glFillTriangle(self, a, b, c):
        #filling triangles

        if a.y > b.y:
            a, b = b, a
        if a.y > c.y:
            a, c = c, a
        if b.y > c.y:
            b, c = c, b
        
        ac_x_slope = c.x - a.x
        ac_y_slope = c.y - a.y

        if ac_y_slope == 0:
            inverse_ac_slope = 0
        else:
            inverse_ac_slope = ac_x_slope / ac_y_slope

        ab_x_slope = b.x - a.x
        ab_y_slope = b.y - a.y

        if ab_y_slope == 0:
            inverse_ab_slope = 0
        else:
            inverse_ab_slope = ab_x_slope / ab_y_slope

        for y in range(a.y, b.y + 1):
            x0 = round(a.x - inverse_ac_slope * (a.y - y))
            xf = round(a.x - inverse_ab_slope * (a.y - y))

            if x0 > xf:
                x0, xf = xf, x0
            
            for x in range(x0, xf + 1):
                self.glPoint((float(x)/(float(self.width)/2))-1,(float(y)/(float(self.height)/2))-1,self.vertex_color)
        
        bc_x_slope = c.x - b.x
        bc_y_slope = c.y - b.y

        if bc_y_slope == 0:
            inverse_bc_slope = 0
        else:
            inverse_bc_slope = bc_x_slope / bc_y_slope
            
        for y in range (b.y, c.y + 1):
            x0 = int(round(a.x - inverse_ac_slope * (a.y - y)))
            xf = int(round(b.x - inverse_bc_slope * (b.y - y)))

            if x0 > xf:
                x0, xf = xf, x0
            
            for x in range(x0, xf + 1):
                self.glPoint((float(x)/(float(self.width)/2))-1,(float(y)/(float(self.height)/2))-1,self.vertex_color)

    #def triangle(self):
    A = next(self.active_vertex_array)
    B = next(self.active_vertex_array)
    C = next(self.active_vertex_array)

    if self.active_texture:
      tA = next(self.active_vertex_array)
      tB = next(self.active_vertex_array)
      tC = next(self.active_vertex_array)

      nA = next(self.active_vertex_array)
      nB = next(self.active_vertex_array)
      nC = next(self.active_vertex_array)

    

    
def glLoadObjModel(self, file_name, mtl=None, texture=None, translate=(0,0, 0), scale=(1,1, 1), rotate =(0,0,0), shader = None, mapping = None):
    
        #Reads .obj file
        self.loadModelMatrix(translate, scale, rotate)
        self.glPipelineMatrix()
        
        if not mtl:
            model = ObjReader(file_name)
            model.readLines()
        else:
            model = ObjReader(file_name, mtl)
            model.readLines()

        light = V3(0, 0.5, 1)
        
        
def loadModelMatrix(self, translate=(0,0,0),scale=(1,1,1),rotate=(0,0,0)):
        translate_matrix = [
            [1,0,0,translate[0]],
            [0,1,0,translate[1]],
            [0,0,1,translate[2]],
            [0,0,0,1]
        ]
        
        scale_matrix = [
            [scale[0],0,0,0],
            [0,scale[1],0,0],
            [0,0,scale[2],0],
            [0,0,0,1]
        ]
        
        a = rotate[0]
        rotation_matrix_x = [
            [1,0,0,0],
            [0,math.cos(a),-1*(math.sin(a)),0],
            [0,math.sin(a),math.cos(a),0],
            [0,0,0,1]
        ]
        
        a = rotate[1]
        rotation_matrix_y = [
            [math.cos(a),0,math.sin(a),0],
            [0,1,0,0],
            [-1*(math.sin(a)),0,math.cos(a),0],
            [0,0,0,1]
        ]

        a = rotate[2]
        rotation_matrix_z = [
            [math.cos(a),-1*(math.sin(a)),0,0],
            [math.sin(a),math.cos(a),0,0],
            [0,0,1,0],
            [0,0,0,1]
        ]

        primera = multMatrices(rotation_matrix_z,rotation_matrix_y)
        rotation_matrix = multMatrices(primera,rotation_matrix_x)
        
        segunda = multMatrices(rotation_matrix,scale_matrix)
        self.Model = multMatrices(translate_matrix,segunda)

def lookAt(self, eye, center, up):
     z = norm(sub(eye, center))
     x = norm(cross(up,z))
     y = norm(cross(z,x))
     self.loadViewMatrix(x, y, z, center)
     self.loadProyectionMatrix(1/magnitud(sub(eye,center)))

def loadViewMatrix(self, x, y, z, center):
        M = [
            [x.x,x.y,x.z,0],
            [y.x,y.y,y.z,0],
            [z.x,z.y,z.z,0],
            [0,0,0,1]
        ]
        O = [
            [1,0,0,-1*center.x],
            [0,1,0,-1*center.y],
            [0,0,1,-1*center.z],
            [0,0,0,1]
        ]
        self.View = (M,O)
    
def loadProyectionMatrix(self, coeff):
        self.Proyection = [
            [1,0,0,0],
            [0,1,0,0],
            [0,0,1,0],
            [0,0,coeff,1]
        ]
    
def loadViewportMatrix(self, x, y):
        self.Viewport = [
            [self.width/2,0,0,x+self.width/2],
            [0,self.height/2,0,y+self.height/2],
            [0,0,128,128],
            [0,0,0,1]
        ]
    
def glLoadTexture(self, file_name, translate=(0, 0), scale=(1, 1)):

        model = ObjReader(file_name)
        model.readLines()

        for face in model.faces:
            vertices_ctr = len(face)
            if vertices_ctr == 3:

                tv1 = face[0][1] - 1
                tv2 = face[1][1] - 1
                tv3 = face[2][1] - 1
                
                tvAx, tvAy = tvA.x,tvA.y
                tvBx, tvBy = tvB.x,tvB.y
                tvCx, tvCy = tvC.x,tvC.y
                
                tvAx = (tvAx * 2) - 1
                tvAy = (tvAy * 2) - 1
                tvBx = (tvBx * 2) - 1
                tvBy = (tvBy * 2) - 1
                tvCx = (tvCx * 2) - 1
                tvCy = (tvCy * 2) - 1
                
                self.glLine(tvAx, tvAy,tvBx, tvBy)
                self.glLine(tvBx, tvBy,tvCx, tvCy)
                self.glLine(tvCx, tvCy,tvAx, tvAy)

#(05 puntos) Deben crear una función glFinish() que escriba el archivo de imagen
def glWrite(self, file_name):
      bmp_file = open(file_name, 'wb')
      #file header 14 bytes
      bmp_file.write(char('B'))
      bmp_file.write(char('M'))
      bmp_file.write(dword(14 + 40 + 3 *(self.width * self.height)))
      bmp_file.write(dword(0))
      bmp_file.write(dword(14 + 40))

      #info header 40 bytes
      bmp_file.write(dword(40))
      bmp_file.write(dword(self.width))
      bmp_file.write(dword(self.height))
      bmp_file.write(word(1))
      bmp_file.write(word(24))
      bmp_file.write(dword(0))
      bmp_file.write(dword( 3 *(self.width * self.height)))
      bmp_file.write(dword(0))
      bmp_file.write(dword(0))
      bmp_file.write(dword(0))
      bmp_file.write(dword(0))
      #bitmap
      for y in range(self.height):
        for x in range(self.width):
            self.framebuffer[x][y]
            bmp_file.write(self.framebuffer[y][x])

        bmp_file.close()
        
