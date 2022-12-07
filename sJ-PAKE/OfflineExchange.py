# This program matches the client and server and initialises the public parameters for them
from Party import * 
import Curve25519 as C
from sage.all import *


class Exchange():
    def __init__(self):
        self.G = C.Curve25519()
    
    def run(self):

        client = Party(self.G, self.G.GetGenerator(), self.G.F(1337), self.G.F(98765432345678))#name, g, q, sigma
        server = Party(self.G, self.G.GetGenerator(), self.G.F(42069), self.G.F(98765432345678), True)

        c_stage1 = client.Stage1()
        s_stage1 = server.Stage1()

        c_stage2 = client.Stage2(s_stage1)
        s_stage2 = server.Stage2(c_stage1)

        c_stage3 = client.Stage3(s_stage2)
        s_stage3 = server.Stage3(c_stage2)

        #print("Key for Client is {0}\nKey for Server is {1}".format(c_stage3, s_stage3))

        if s_stage3 == c_stage3:
            print("\n\n##### !!! PARTY !!! #####\nSERVER KEY: {0}\nClIENT KEY: {1}".format(s_stage3, c_stage3))
            print("WE HAVE EQUAL KEYS!!!")

        return

    def Setup():
        return


foo = Exchange()
foo.run()