# This program matches the client and server and initialises the public parameters for them
from Party import * 
import Curve25519 as C


class Exchange():
    def __init__(self):
        self.G = C.Curve25519()

        #self.__A = A
        #self.__B = B

        #self.run()
    
    def run(self):

        client = Party("client", self.G, self.G.GetGenerator(), self.G.P, None)#name, g, q, sigma
        server = Party("server", self.G, self.G.GetGenerator(), self.G.P, None)

        return

    def Setup():
        return


foo = Exchange()
foo.run()