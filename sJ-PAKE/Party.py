#AUTHOR = Karl Sachs

import Schnorr
import hashlib
from sage.all import *
import Curve25519

class Party():
    def __init__(self, G, g, label, pw, isServer=False):

        self.G = G        # Group
        self.g = g        # generator
        self.pw = pw

        self.isServer = isServer

        # Define the NIZK that's used
        self.NIZK = Schnorr.NonInteractiveSchnorr(self.G, self.g)

        self.x_1 = None
        self.x_2 = None
        
        # My parameters
        self.A = {"l" : label}
        # Their parameters
        self.B = {}

        return 
    
    
    def Stage1(self):

        self.x_1 = self.G.F.random_element()
        self.x_2 = self.G.F.random_element()
        
        self.A["X_1"] = self.G.DLP(self.x_1, self.g)
        self.A["X_2"] = self.G.DLP(self.x_2, self.g)

        self.A["pi_1"], self.A["R_1"] = self.NIZK.Prv((self.A["X_1"], self.g), self.x_1, self.A["l"])
        self.A["pi_2"], self.A["R_2"] = self.NIZK.Prv((self.A["X_2"], self.g), self.x_2, self.A["l"])

        print("Stage 1 complete! Now sending over (label, X_1, X_2, pi_1, pi_2, R_1, R_2)")
        return self.A

    
    def Stage2(self, B):
        self.B = B

        if (self.B["X_2"] == 1):
            raise Exception("Other party's X_2 = 1!!!")
        
        # Check verifications
        if (not ( self.NIZK.Ver((self.B["X_1"], self.g), self.B["pi_1"], self.B["l"], self.B["R_1"]) )):
            raise Exception("Other party doesn't actually have their x_1!!!")

        if (not ( self.NIZK.Ver((self.B["X_2"], self.g), self.B["pi_2"], self.B["l"], self.B["R_2"]) )):
            raise Exception("Other party doesn't actually have their x_2!!!")


        #### CREATE ALPHA/BETA

        self.A["grk"] = self.G.DLP(self.x_2, self.G.DLP(self.pw, self.G.Op(self.G.Op(self.A["X_1"], self.B["X_1"]), self.B["X_2"])))

        print("Stage 2 complete! Sending over our alpha." )

        return { "grk" : self.A["grk"]}


    # 
    def Stage3(self, grk):
        self.B["grk"] = grk["grk"]

        # prekey
        key = self.G.DLP(self.x_2, (self.G.Op(self.B["grk"], self.G.DLP(-self.x_2, self.G.DLP(self.pw, self.B["X_2"]) ) ) ) )
        print("Stage 3 about to complete...")

        if (self.isServer):
            return self.Hash_1( self.B["l"], 
                                self.A["l"], 
                                self.B["X_1"], 
                                self.B["X_2"], 
                                self.A["X_1"], 
                                self.A["X_2"], 
                                self.B["grk"], 
                                self.A["grk"], 
                                key, 
                                self.pw)
        
        else:
            return self.Hash_1( self.A["l"],
                                self.B["l"],
                                self.A["X_1"],
                                self.A["X_2"], 
                                self.B["X_1"], 
                                self.B["X_2"], 
                                self.A["grk"],
                                self.B["grk"], 
                                key, 
                                self.pw)
            



    # Generates hash for multiple args
    def Hash_1(self, *arg):
        digest = hashlib.sha256()
        for a in arg:
            int_a = int(a.lift())
            digest.update(int_a.to_bytes((int_a.bit_length() + 7) // 8, 'big'))
        
        return digest.digest()
    
