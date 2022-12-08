#AUTHOR = Karl Sachs

import Schnorr
import hashlib
from sage.all import *
import Curve25519

class Party():
    def __init__(self, G, g, label, pw, hash, isServer=False):

        self.G = G        # Group
        self.g = g        # generator
        self.pw = self.G.F(int.from_bytes(pw.encode(), "big"))

        self.hash = hash

        self.isServer = isServer

        # Define the NIZK that's used
        self.NIZK = Schnorr.NonInteractiveSchnorr(self.G, self.g)

        self.x_1 = None
        self.x_2 = None
        
        # My parameters
        self.A = {"l" : self.G.F(int.from_bytes(label.encode(), "big"))}
        # Their parameters
        self.B = {}

        self.key = None
        # Final Key K
        self.K = None
        return 
    
    def Change_pw(self, pw):
        if (not self.isServer):
            raise Exception("This guy aint a server and he trying to do server stuff")
        
        self.pw = pw#self.G.F(int.from_bytes(pw.encode(), "big"))
        
        return

    def Stage1(self):

        self.x_1 = self.G.F.random_element()
        self.x_2 = self.G.F.random_element()
        
        self.A["X_1"] = self.G.DLP(self.x_1, self.g)
        self.A["X_2"] = self.G.DLP(self.x_2, self.g)
        
        self.A["pi_1"], self.A["R_1"] = self.NIZK.Prv((self.A["X_1"], self.g), self.x_1, self.A["l"])
        self.A["pi_2"], self.A["R_2"] = self.NIZK.Prv((self.A["X_2"], self.g), self.x_2, self.A["l"])

        return self.A


    def Stage2(self, B):
        self.B = B

        if (self.B["X_2"] == 1):
            print("Other party's X_2 = 1!!!")
            return b'\x00\x00\x00\x00\x00\x00\x00\x00'
        
        # Check verifications
        if (not ( self.NIZK.Ver((self.B["X_1"], self.g), self.B["pi_1"], self.B["l"], self.B["R_1"]) )):
            print("Other party doesn't actually have their x_1!!!")
            return b'\x00\x00\x00\x00\x00\x00\x00\x01'

        if (not ( self.NIZK.Ver((self.B["X_2"], self.g), self.B["pi_2"], self.B["l"], self.B["R_2"]) )):
            print("Other party doesn't actually have their x_2!!!")

            return b'\x00\x00\x00\x00\x00\x00\x00\x02'


        #### CREATE ALPHA/BETA

        self.A["grk"] = self.G.DLP(self.x_2, self.G.DLP(self.pw, self.G.Op(self.G.Op(self.A["X_1"], self.B["X_1"]), self.B["X_2"])))

        return { "grk" : self.A["grk"]}


    def Stage3(self, grk):

        self.B["grk"] = grk["grk"]

        # prekey
        self.key = self.G.DLP(self.x_2, (self.G.Op(self.B["grk"], self.G.DLP(-self.x_2, self.G.DLP(self.pw, self.B["X_2"]) ) ) ) )

        # Remove x_1 and x_2 so that they act as ephemeral keys
        self.x_1 = None
        self.x_2 = None

        if (self.isServer):
            self.K = int.from_bytes(self.Hash_1( self.B["l"], 
                                    self.A["l"], 
                                    self.B["X_1"], 
                                    self.B["X_2"], 
                                    self.A["X_1"], 
                                    self.A["X_2"], 
                                    self.B["grk"], 
                                    self.A["grk"], 
                                    self.key, 
                                    self.pw), "big")
            return self.K
        
        else:
            self.K = int.from_bytes(self.Hash_1( self.A["l"],
                                    self.B["l"],
                                    self.A["X_1"],
                                    self.A["X_2"], 
                                    self.B["X_1"], 
                                    self.B["X_2"], 
                                    self.A["grk"],
                                    self.B["grk"], 
                                    self.key, 
                                    self.pw), "big")
            return self.K
            



    # Generates hash for multiple args
    def Hash_1(self, *arg):
        digest = self.hash()#hashlib.sha256()
        for a in arg:
            int_a = int(a.lift())
            digest.update(int_a.to_bytes((int_a.bit_length() + 7) // 8, 'big'))
        
        return digest.digest()
    
