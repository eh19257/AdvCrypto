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
        #self.F_p_2 = GF(self.P**2)

        self.E = EllipticCurve(self.F, [0, self.A, 0, 1, 0])

    # Used to abstract out the group operation
    def Op(self, A, B):
        '''
        # X(A + B) = x_3/z_3
        # Where A = x/z
        # Where B = x_/z_

        x = A*2
        z = self.F(2)

        x_ = B*2
        z_ = self.F(2)


        x_3 = 4 * (x * x_ - z * z_) ** 2
        z_3 = 4 * (x * z_ - z * x_) ** 2

        out = (1/z_3) * x_3
        '''
        return A + B
        #return A  + B#self.E(A) + self.E(B)#self.F_p_2(A) + self.F_p_2(B)

    '''
    # A - B
    def NegOp(self, A, B):
        # X(A - B) = x_1/z_1
        # Where A = x/z
        # Where B = x_/z_

        x = A*2
        z = self.F(2)

        x_ = B*2
        z_ = self.F(2)

        x_1 = ((x - z) * (x_ + z_) + (x + z) * (x_ - z_)) ** 2
        z_1 = 
    '''

    
    # DLP for group [n]g
    def DLP(self, g, n):      
        return n*g#self.E(n)*self.E(g)#self.F_p_2(n)*self.F_p_2(g)

    # Gets generator. In the case of Curve25519 we use 9 as our base point
    def GetGenerator(self):
        return self.F(9)#self.E.lift_x(self.F(9))

    # Randomly pick 
    def RandomlyGenerateGroupElement(self):
        return self.F.random_element()