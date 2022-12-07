# Author = Karl Sachs

#from cmath import sqrt
#from operator import truediv
from sage.all import *

#class Group():
#    def __init__():



class Curve25519():

    def __init__(self):
        self.P = (2**255 - 19)
        self.A = 486662

        self.F = GF(self.P)

        self.E = EllipticCurve(self.F, [0, self.A, 0, 1, 0])


    # Used to abstract out the group operation
    def Op(self, A, B):
        return A + B
    
    # DLP for group [n]g
    def DLP(self, g, n):      
        return n*g#self.E(n)*self.E(g)#self.F_p_2(n)*self.F_p_2(g)

    # Gets generator. In the case of Curve25519 we use 9 as our base point
    def GetGenerator(self):
        return self.F(9)#self.E.lift_x(self.F(9))

    # Randomly pick 
    def RandomlyGenerateGroupElement(self):
        return self.F.random_element()