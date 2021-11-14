#Laurelinda Gómez
#19501

#main
from gl3 import *

pi = 3.14

def gourad(render, **kwargs):
    #barycentric
    w, v, u = kwargs['bar']
    #textura
    tx, ty = kwargs['texture_coords']
    #normals
    nA, nB, nC = kwargs['varying_normals']
    diver = render.current_texture.get_color(tx, ty)
     # intensidad de luz
    iA, iB, iC = [dot(n, render.light) for n in (nA, nB, nC)]
    intensity = w*iA + v*iB + u*iC
    return diver * intensity


def shader1(render, **kwargs):
    #mesa
    w, v, u = kwargs['bar']
    nA, nB, nC = kwargs['varying_normals']
    A, B, C = kwargs['triangle']
    diver = color(241, 180, 109)
    iA, iB, iC = [dot(n, render.light) for n in (nA, nB, nC)]
    intensity = w*iA + v*iB + u*iC
    return diver * intensity

def shader2(render, **kwargs):
    # lata
    w, v, u = kwargs['bar']
    nA, nB, nC = kwargs['varying_normals']
    A, B, C = kwargs['triangle']
    diver = color(249, 219, 227)
    iA, iB, iC = [dot(n, render.light) for n in (nA, nB, nC)]
    intensity = w*iA + v*iB + u*iC
    return diver * intensity

def shader3(render, **kwargs):
    #Lentes
    w, v, u = kwargs['bar']
    nA, nB, nC = kwargs['varying_normals']
    A, B, C = kwargs['triangle']
    diver = color(242, 208, 102)
    iA, iB, iC = [dot(n, render.light) for n in (nA, nB, nC)]
    intensity = w*iA + v*iB + u*iC
    return diver * intensity

def shader4(render, **kwargs):
    #succulent
    w, v, u = kwargs['bar']
    nA, nB, nC = kwargs['varying_normals']
    A, B, C = kwargs['triangle']
    diver = color(0,0,255)
    iA, iB, iC = [dot(n, render.light) for n in (nA, nB, nC)]
    intensity = w*iA + v*iB + u*iC
    return diver * intensity

def shader5(render, **kwargs):
    #quran
    w, v, u = kwargs['bar']
    nA, nB, nC = kwargs['varying_normals']
    A, B, C = kwargs['triangle']
    diver = color(255,255,0)
    iA, iB, iC = [dot(n, render.light) for n in (nA, nB, nC)]
    intensity = w*iA + v*iB + u*iC
    return diver * intensity


r = Renderer(900,900)
r.lookAt(V3(0,0,5), V3(0, 0, 0), V3(0, 1, 0))
r.current_texture = gourad
r.light = V3(-0.3, -0.3, 0.4)
#Mesa 
r.load('./models/table.obj', (-0.3, -0.6, 0), (0.8, 0.6, 0.1), (0, pi/3, 0))
r.active_shader = shader1
r.draw_arrays('TRIANGLES')

r.current_texture = gourad
r.light = V3(-0.3, -0.3, 0.4)
#Lentes
r.load('./models/Glasses.obj', (-0.3, 0.15, 0), (0.08, 0.2, 0.05), (0, pi/3, 0))
r.active_shader = shader2
r.draw_arrays('TRIANGLES')

r.current_texture = gourad
r.light = V3(-0.3, -0.3, 0.4)
#Lata 
r.load('./models/Can.obj', (-0.6, 0.01, 0), (0.08, 0.2, 0.05), (0, pi/3, 0))
r.active_shader = shader3
r.draw_arrays('TRIANGLES')

r.current_texture = gourad
r.light = V3(-0.3, -0.3, 0.4)
#plantita
r.load('./models/SUCCULENT.obj', (-0.4, -0.5, 0), (0.09, 0.2, 0.05), (0, pi/3, 0))
r.active_shader = shader4
r.draw_arrays('TRIANGLES')

r.current_texture = gourad
r.light = V3(-0.3, -0.3, 0.4)
#Libro
r.load('./models/Quran.obj', (-0.2, -0.5, 0), (0.09, 0.2, 0.05), (0, pi/4, 0))
r.active_shader = shader5
r.draw_arrays('TRIANGLES')
r.render()

