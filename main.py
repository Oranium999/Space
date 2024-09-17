import numpy as np
import turtle
import random
from scipy.spatial.transform import Rotation as R

class astr():
    def __init__(self, name, mass, xyz, p, e = 0, parent=None, period = None) -> None:
        self.name = name
        self.mass = mass
        self.xyz=xyz
        self.e = e 
        self.p = p
        self.parent = parent
        self.childe = []
        self.period = period
        if self.parent != None:
            self.parent.childe.append(self)
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

        rotMatrix = R.from_euler('xyz', self.xyz, degrees=True).as_matrix()
        
        coord = np.matmul(local_coord, rotMatrix)
        return coord
    
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
        return rep


soleil = astr("soleil", 200, (0,0,0), 0)
terre = astr("terre", 30, (0,0,0), 200, 0.5, soleil)
lune = astr("lune", 6, (0,0,0), 50, 0, terre, period=10)
turtle.colormode(255)
astrs = [soleil, terre, lune]
turtles = []
for i in astrs:
    newTurtles = turtle.Turtle(shape="circle")
    r = random.randrange(0,257,10)
    g = random.randrange(0,257,10)
    b = random.randrange(0,257,10)
    newTurtles.color(r,g,b)
    newTurtles.penup()
    newTurtles.goto((i.get_global_poition(0).item(0), i.get_global_poition(0).item(1)))
    newTurtles.pendown()
    turtles.append(newTurtles)

i = 0 
while True:
    print("#################"+str(i)+"###############")
    for j, a in enumerate(astrs):
        pos = a.get_global_poition(i)
        turtles[j].goto((pos.item(0), pos.item(1)))
    ans = input()
    i += 1