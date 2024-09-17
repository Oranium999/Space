import numpy as np
import turtle

class astr():
    def __init__(self, _mass, _vectRotation, _p, _e = 0.0001) -> None:
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
        teta = self.get_anomalie_vrai(t)
        d = self.dist(teta)
        return d*np.cos(teta), d*np.sin(teta)
    
    def get_anomalie_moy(self, t):
        period = self.period(self.p)
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
            # print("diff= ",diff,"un= ",un,"un1= ",un1)
            if diff<0.001:
                u = un1
                # print("break")
                break
            un = un1
        return u
    
    def get_anomalie_vrai(self, t):
        u = self.get_anomalie_ex(t)
        v = 2*np.arctan(np.sqrt((1+self.e)/(1-self.e))*np.tan(u/2))
        # print ("v= ",v)
        return v
    
    def get_speed(self,t1,t2):
        pos1 = terre.get_pos(t1)
        pos2 = terre.get_pos(t2)
        speed = np.sqrt(pow(pos1[0]-pos2[0],2)+pow(pos1[1]-pos2[1],2))
        return speed

        


terre = astr(10, (0,0,1), 100, 0.0009)
for i in range(1000):
    speed = terre.get_speed(i,i+1)
    print("speed = ",speed)
    turtle.goto(terre.get_pos(i))
    