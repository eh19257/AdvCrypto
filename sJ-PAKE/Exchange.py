# This program matches the client and server and initialises the public parameters for them
from Party import * 
import Curve25519 as C
from sage.all import *


class Exchange():
    def __init__(self):
        self.G = C.Curve25519()

        #self.__A = A
        #self.__B = B

        #self.run()
        '''
        g = self.G.GetGenerator()

        a = self.G.RandomlyGenerateGroupElement()
        b = self.G.RandomlyGenerateGroupElement()

        

        c = self.G.RandomlyGenerateGroupElement()
        d = self.G.RandomlyGenerateGroupElement()

        A = (a+b)*g
        C_ = (c+d)*g

        if ((c+d)*A == (a+b)*C_):
            print("WORKING")
        '''
    
    def run(self):

        client = Party("client", self.G, self.G.GetGenerator(), self.G.P, None, self.G.F(1337), True)#name, g, q, sigma
        server = Party("server", self.G, self.G.GetGenerator(), self.G.P, None, self.G.F(42069), False)

        c_stage1 = client.Stage1()
        s_stage1 = server.Stage1()

        c_stage2 = client.Stage2(s_stage1)
        s_stage2 = server.Stage2(c_stage1)

        c_stage3 = client.Stage3(s_stage2)
        s_stage3 = server.Stage3(c_stage2)

        print("Key for Client is {0}\nKey for Server is {1}".format(c_stage3, s_stage3))

        if s_stage3 == c_stage3:
            print("WE HAVE EQUAL KEYS!!!")

        return

    def Setup():
        return


foo = Exchange()
foo.run()