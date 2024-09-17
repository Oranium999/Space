import numpy as np
import turtle

class astr():
    def __init__(self, _mass, _vectRotation, _p, _e = 0) -> None:
        self.mass = _mass
        self.vect=_vectRotation
        self.e = _e 
        self.p = _p

    def period(self, p):
        a = (60216.8-87.969)/(4498400000-57909050) # y/x
        b = 60216.8/(4498400000*a)
        return a*p + b
    
    def dist(self, teta):
        return self.p / (1+self.e*np.cos(teta))
    
    def teta(self, t):
        period = self.period(self.p)
        tR = t/period*2*np.pi
        return tR+(np.sin(tR))

    def get_pos(self, t):
        teta = self.teta(t)
        d = self.dist(teta)
        return d*np.cos(teta), d*np.sin(teta)


terre = astr(10, (0,0,1), 100, 0.7)
for i in range(10000):
    turtle.goto(terre.get_pos(i))
    