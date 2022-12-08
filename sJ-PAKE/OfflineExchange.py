# This program matches the client and server and initialises the public parameters for them
from Party import * 
import Curve25519 as C
from sage.all import *


class Exchange():
    def __init__(self):
        self.G = C.Curve25519()

        self.client = Party(self.G, self.G.GetGenerator(), "example_client", "SuperSecretSharedPassword", hashlib.sha256)
        self.server = Party(self.G, self.G.GetGenerator(), "example_server", "SuperSecretSharedPassword", hashlib.sha256, True)
    
    def run(self):

        c_stage1 = self.client.Stage1()
        s_stage1 = self.server.Stage1()

        c_stage2 = self.client.Stage2(s_stage1)
        s_stage2 = self.server.Stage2(c_stage1)

        c_stage3 = self.client.Stage3(s_stage2)
        s_stage3 = self.server.Stage3(c_stage2)

        #print("Key for Client is {0}\nKey for Server is {1}".format(c_stage3, s_stage3))

        if s_stage3 == c_stage3:
            print("\n\nSERVER KEY: {0}\nClIENT KEY: {1}".format(s_stage3, c_stage3))
            print("Both parties have EQUAL keys!!!")

        return

    def Setup():
        return


foo = Exchange()
foo.run()