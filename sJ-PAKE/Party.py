#AUTHOR = Karl Sachs

import Schnorr
import hashlib
from sage.all import *

class Party():
    def __init__(self, name, G, g, q, sigma, label, isclient=False):
        self.name = name

        self.G = G        # Group
        self.g = g        # generator
        #self.q = q        # Prime

        # Long term keys
        self.sk = self.G.RandomlyGenerateGroupElement()
        self.pk = self.G.DLP(g, self.sk)

        self.NIZK = Schnorr.NonInteractiveSchnorr(self.G, self.g)

        self.label = label
        self.pw = self.G.F(1234)

        self.inParams = None
        self.alpha = None
        self.K = None

        #self.sigma = sigma

        self.isclient = isclient

        print(name)
        return 
    
    def Stage1(self):
        self.x_1 = self.G.RandomlyGenerateGroupElement()
        self.x_2 = self.G.RandomlyGenerateGroupElement()

        out = { "label" : self.pk }

        self.X_1 = self.G.DLP(self.g, self.x_1)
        self.X_2 = self.G.DLP(self.g, self.x_2)

        out["X_1"] = self.X_1
        out["X_2"] = self.X_2

        # This is based on a non-interactive zero knowledge proof
        out["pi_1"], out["R_1"] = self.NIZK.Prv((self.X_1, self.g), self.x_1, self.pk, self.sk)
        out["pi_2"], out["R_2"] = self.NIZK.Prv((self.X_2, self.g), self.x_2, self.pk, self.sk)
    
        return out


    # Parameters in the form (label, X_3, X_4, pi_3, pi_4, R_3, R_4)
    def Stage2(self, inParams):
        self.inParams = inParams

        if (inParams["X_2"] == 1):
            raise Exception("Other party's X_2 should NOT equal 1!")
        else:
            if (not self.NIZK.Ver((inParams["X_1"], self.g), inParams["pi_1"], inParams["label"], inParams["R_1"])):
                raise Exception("Bad verification, the other party does not have their private key x_1!")

            if (not self.NIZK.Ver((inParams["X_2"], self.g), inParams["pi_2"], inParams["label"], inParams["R_2"])):
                raise Exception("Bad verification, the other party does not have their private key x_2!")

        if (self.isclient):
            #self.alpha = self.G.DLP(self.G.Op(self.G.Op(self.X_1, inParams["X_1"]), inParams["X_2"]), self.G.Op(self.x_2, self.pw))
            self.alpha = self.G.DLP(self.G.DLP(self.G.Op(self.G.Op(self.X_1, inParams["X_1"]), inParams["X_2"]), self.x_2), self.pw)
        else:
            #self.alpha = self.G.DLP(self.G.Op(self.G.Op(inParams["X_1"], inParams["X_2"]), self.X_1), self.G.Op(self.x_2, self.pw))
            self.alpha = self.G.DLP(self.G.DLP(self.G.Op(self.G.Op(inParams["X_1"], inParams["X_2"]), self.X_1), self.x_2), self.pw)
        
        #self.alpha = self.G.DLP(base, exponent)
        return self.alpha


    # Stage 3 of sJ-PAKE. Here both parties have the information they need and now they can generate some shared key from this information
    def Stage3(self, beta):
        #self.inParams["beta"] = beta

        Key = None#self.G.DLP(self.G.DLP(base, expo_1), self.x_2)
        '''
        if (self.isclient):
            print("AM CLIENT")
            Key = self.G.DLP(self.G.Op(beta, self.G.DLP(self.inParams["X_2"], self.G.Op(-self.x_2, self.pw))), self.x_2)
        else:
            print("AM server")
            Key = self.G.DLP(self.G.Op(beta, self.G.DLP(self.inParams["X_2"], self.G.Op(-self.x_2, self.pw))), self.x_2)
        '''
        # (foo * bar^baz)

        #Key = self.G.DLP(self.G.Op(beta, self.G.DLP(self.inParams["X_2"], self.G.Op(-self.x_2, self.pw))), self.x_2)
        #Key = self.G.DLP(self.G.DLP(self.G.Op(beta, self.inParams["X_2"]), self.G.Op(-self.x_2, self.pw)), self.x_2)
        #####

        #return self.G.DLP(self.G.Op(beta, self.G.DLP(self.inParams["X_2"], self.G.Op(-self.x_2, self.pw))), self.x_2)
        
        return (beta + self.inParams["X_2"] * (-self.x_2 + self.pw))* self.x_2
        
        if (self.isclient):
            return self.G.F(self.G.DLP(self.G.Op(beta, self.G.DLP(self.inParams["X_2"], self.G.Op(-self.x_2, self.pw))), self.x_2))
            #print("THIS IS A CLIENT:", self.label, self.inParams["label"], self.X_1, self.X_2, self.inParams["X_1"], self.inParams["X_2"], self.alpha, beta, Key, self.pw)
            print("This is the client Key:", Key)
            self.K = self.Hash_1(self.label,
                                 self.inParams["label"],
                                 self.X_1,
                                 self.X_2, 
                                 self.inParams["X_1"], 
                                 self.inParams["X_2"], 
                                 self.alpha,
                                 beta, 
                                 Key, 
                                 self.pw)
        else:
            return self.G.F(self.G.DLP(self.G.Op(beta, self.G.DLP(self.inParams["X_2"], self.G.Op(-self.x_2, self.pw))), self.x_2))
            #print("THIS IS A SERVER:", self.inParams["label"], self.label, self.inParams["X_1"], self.inParams["X_2"], self.X_1, self.X_2, beta, self.alpha, Key, self.pw)
            print("This is the server Key:", Key)
            self.K = self.Hash_1(self.inParams["label"], 
                                 self.label, 
                                 self.inParams["X_1"], 
                                 self.inParams["X_2"], 
                                 self.X_1, 
                                 self.X_2, 
                                 beta, 
                                 self.alpha, 
                                 Key, 
                                 self.pw)
        
        return self.K
        

    # Generates hash for multiple args
    def Hash_1(self, *arg):
        digest = hashlib.sha256()
        for a in arg:
            int_a = int(a.lift())
            digest.update(int_a.to_bytes((int_a.bit_length() + 7) // 8, 'big'))
        
        return digest.digest()
    
