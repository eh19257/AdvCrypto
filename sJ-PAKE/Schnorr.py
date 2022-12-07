# Implementation of Schnorr's Identification protocol for NIZK proof

import Curve25519 as C
import hashlib


class NonInteractiveSchnorr:
    def __init__(self, G, g):
        self.G = G
        #self.g = g

        return
    
    def Setup(self, seed=0):
        return 
    
    # Create a Non Interactive Commitment. We also return R here as it is needed for 
    def Prv(self, sigma, x, l):

        k = self.G.F.random_element()
        R = self.G.DLP(sigma[1], k)
        
        e = self.G.F(int.from_bytes(self.Hash(R, sigma[0], sigma[1], l), "big"))

        pi = k + x*e
        return pi, R


    # Verifies the incoming Non-interactive commitment
    def Ver(self, sigma, pi, l ,R):
        e = self.G.F(int.from_bytes(self.Hash(R, sigma[0], sigma[1], l), "big"))

        rhs = self.G.Op(self.G.DLP(sigma[1], pi), self.G.DLP(sigma[0], (-e)))

        return R == rhs

    
    # Generates hash for multiple args
    def Hash(self, *arg):
        digest = hashlib.sha256()

        for a in arg:
            int_a = int(a.lift())
            digest.update(int_a.to_bytes((int_a.bit_length() + 7) // 8, 'big'))
        
        return digest.digest()