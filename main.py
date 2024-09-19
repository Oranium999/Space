import numpy as np
import turtle
import random
from scipy.spatial.transform import Rotation as R

import tkinter as tk

class astr():
    def __init__(self, name, mass, xyz, p, e = 0, parent=None, period = None) -> None:
        self.name = name
        self.mass = mass
        self.xyz=xyz
        self.e = e 
        self.p = p
        self.parent = parent
        self.childes = []
        self.period = period
        if self.parent != None:
            self.parent.childes.append(self)
        if self.period == None:
            self.period = self.get_period(self.p)

    def get_period(self, p):
        a = (60216.8-87.969)/(4498400000-57909050) # y/x
        b = 60216.8/(4498400000*a)
        return a*p + b
    
    def dist(self, teta):
        return self.p / (1+self.e*np.cos(teta))
    
    def teta(self, t):
        period = self.period
        tR = t/period*2*np.pi
        return tR+(np.sin(tR))
    
    def get_anomalie_moy(self, t):
        period = self.period
        return (2*t*np.pi)/period
    
    def get_anomalie_ex0(self, t):
        m = self.get_anomalie_moy(t)
        return m/(1-self.e)
    
    def get_anomalie_ex(self, t):
        """
        t : temps
        
        Return anomalie_ex. If the series does not converge, return 0.
        """
        m = self.get_anomalie_moy(t)
        un = self.get_anomalie_ex0(t)
        un1 = 0
        u = 0
        for i in range (100):
            un1 = self.e*np.sin(un)+m
            diff = abs(un-un1)
            if diff<0.001:
                u = un1
                break
            un = un1
        return u
    
    def get_anomalie_vrai(self, t):
        u = self.get_anomalie_ex(t)
        v = 2*np.arctan(np.sqrt((1+self.e)/(1-self.e))*np.tan(u/2))
        return v
    
    def get_pos(self, t):
        teta = self.get_anomalie_vrai(t)
        d = self.dist(teta)
        return d*np.cos(teta), d*np.sin(teta)
    
    def get_speed(self,t1,t2):
        pos1 = terre.get_pos(t1)
        pos2 = terre.get_pos(t2)
        speed = np.sqrt(pow(pos1[0]-pos2[0],2)+pow(pos1[1]-pos2[1],2))
        return speed

    def get_pos_3d(self, t):
        local_x, local_y = self.get_pos(t)
        local_z = 0
        local_coord = np.array([local_x, local_y, local_z])

        return local_coord
    
    def get_transforme_matrix(self, t):
        """
        transfome coordonate frome sun referencial to planet referencial
        """
        rotMatrix = R.from_euler('xyz', self.xyz, degrees=True).as_matrix()

        coord = self.get_pos_3d(t)

        rep = np.matrix([[rotMatrix.item((0,0)), rotMatrix.item((0,1)), rotMatrix.item((0,2)), 0],
                         [rotMatrix.item((1,0)), rotMatrix.item((1,1)), rotMatrix.item((1,2)), 0],
                         [rotMatrix.item((2,0)), rotMatrix.item((2,1)), rotMatrix.item((2,2)), 0],
                         [coord[0],coord[1],coord[2],1]])
        
        return rep
    
    def get_invers_transforme_matrix(self, t):
        """
        transfome coordonate frome planet referencial to sun referebcial
        """
        rep = np.linalg.inv(self.get_transforme_matrix(t))
        
        return rep

    def get_global_poition(self, t):
        obj = self
        rep = np.array([0,0,0,1])
        while obj.parent != None:
            rep = np.matmul(rep, obj.get_invers_transforme_matrix(t))
            obj = obj.parent
        rep = np.matmul(rep, obj.get_invers_transforme_matrix(t))
        return rep


soleil = astr("soleil", 200, (0,0,0), 0)
terre = astr("terre", 30, (0,0,0), 200, 0.5, soleil)
lune = astr("lune", 6, (0,0,0), 50, 0.85, terre, period=100)

saturn = astr("saturn", 30, (180,0,0), 400, 0, soleil)
europ = astr("europ", 6, (0,0,0), 50, 0, saturn, period=10)

astrs = [soleil]

def add_children_to_astrs(planet):
    if len(planet.childes) == 0:
        return
    for p in planet.childes:
        astrs.append(p)
        add_children_to_astrs(p)

add_children_to_astrs(astrs[0])

turtles = []

def find_planet_by_name(name):
    for planet in astrs:
        if planet.name == name:
            return planet
    raise NameError("noucle not find planet")

finished_pass_time = True

def display_next_day(_):
    global t, finished_pass_time, sim_is_runing
    if not finished_pass_time:
        return
    finished_pass_time =  False
    for j, a in enumerate(astrs):
        pos = a.get_global_poition(t)
        turtles[j].goto((pos.item(0), pos.item(1)))
    
    t += 1
    window.title(str(t))
    finished_pass_time = True
    if sim_is_runing:
        display_next_day(_)

    

import tkinter as tk


def keypress(event):
    global xx, yy, canvas, speed
    ev = event.keysym
    if ev == 'Left':
        xx += speed
        canvas.place(x=xx, y=yy)
    elif ev == 'Right':
        xx -= speed
        canvas.place(x=xx, y=yy)
    if ev == 'Up':
        yy += speed
        canvas.place(x=xx, y=yy)
    elif ev == 'Down':
        yy -= speed
        canvas.place(x=xx, y=yy)

    
    return None

Hight, Width = 1000, 1000

# Set the main window
window = tk.Tk()
window.geometry(f'{Width}x{Hight}')
#window.resizable(False, False)

# Create the canvas. Width is larger than window
canvas = turtle.Canvas(window, width=Width*2, height=Hight*2)
xx, yy = -Hight/2, -Width/2
canvas.place(x=xx, y=yy)

def get_a_2digit_randome_hex():
    rep = hex(random.randrange(0,257,10))[2:]
    if len(rep) == 1:
        rep = "0"+rep
    return rep

t = 0
for i in astrs:
    newTurtles = turtle.RawTurtle(canvas=canvas, shape="circle")

    r = get_a_2digit_randome_hex() 
    g = get_a_2digit_randome_hex()
    b = get_a_2digit_randome_hex()
    
    newTurtles.color("#"+r+g+b)
    newTurtles.speed(0)
    newTurtles.penup()
    pos = i.get_global_poition(t)
    newTurtles.goto((pos.item(0), pos.item(1)))
    newTurtles.pendown()
    turtles.append(newTurtles)

initX, initY = 0, 0
def motion(event):
    global initX, initY
    x, y = event.x, event.y
    if initX==0 and initY == 0:
        initX, initY = xx, yy
    
    canvas.place(x=initX+x, y=initY+(y))
    
def ButtonRelease(_):
    global initX, initY
    initX, initY = 0, 0

sim_is_runing = False
is_space_presed = False
def spacePresed(_):
    global is_space_presed, sim_is_runing
    if is_space_presed == True:
        return
    
    is_space_presed = True
    sim_is_runing = not(sim_is_runing)
     
def spaceRelease(_):
    global is_space_presed
    if is_space_presed == False:
        return
    is_space_presed = False
    display_next_day("")

# key binding
window.bind('<KeyPress-Left>', keypress)
window.bind('<KeyPress-Right>', keypress)
window.bind('<KeyPress-Up>', keypress)
window.bind('<KeyPress-Down>', keypress)

window.bind('<KeyPress-space>', spacePresed)
window.bind('<KeyRelease-space>', spaceRelease)

window.bind('<ButtonRelease-2>', ButtonRelease)
window.bind('<ButtonRelease-1>', ButtonRelease)
window.bind('<ButtonRelease-3>', ButtonRelease)

window.bind('<B2-Motion>', motion)
window.bind('<B1-Motion>', motion)
window.bind('<B3-Motion>', motion)

def do_zoom(event):
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    factor = 1.001 ** event.delta
    canvas.scale(ALL, x, y, factor, factor)
    
from tkinter import ALL, EventType

canvas.bind("<MouseWheel>", do_zoom) # WINDOWS ONLY
canvas.bind('<ButtonPress-1>', lambda event: canvas.scan_mark(event.x, event.y))
canvas.bind("<B1-Motion>", lambda event: canvas.scan_dragto(event.x, event.y, gain=1))

speed = 10  # scrolling speed


window.mainloop()