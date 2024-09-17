import numpy as np
import turtle

from scipy.spatial.transform import Rotation as R

class astr():
    def __init__(self, _mass, _xyz, _p, _e = 0, _parent=None) -> None:
        self.mass = _mass
        self.xyz=_xyz
        self.e = _e 
        self.p = _p
        self.parent = _parent

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
    
    def get_pos_2d(self, t):
        teta = self.teta(t)
        d = self.dist(teta)
        return d*np.cos(teta), d*np.sin(teta)
    
    def get_pos_3d(self, t):
        local_x, local_y = self.get_pos_2d(t)
        local_z = 0

        rotMatrix = R.from_euler('xyz', self.xyz, degrees=True).as_matrix()
        local_coord = np.array([local_x, local_y, local_z])
        coord = np.matmul(local_coord, rotMatrix)
        return coord


terre = astr(10, (0,0,0), 100, 0.7)
for i in range(10000):
    turtle.goto(terre.get_pos_2d(i))
    