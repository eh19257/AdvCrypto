from sage.all import *
from sage.misc.randstate import current_randstate

class Q5b_DH_Party():
    def __init__(self, nickname):
        self.nickname = nickname
        self.P = (2**255 - 19)
        self.A = 486662
        self.F = GF(self.P)

        self.E = EllipticCurve(self.F, [0, self.A, 0, 1, 0])

        self.sk = self.RandomElementFromF_p()
        self.pk = self.sk*self.F(9)
    
        # Ephemeral keys
        self.esk = None
        self.epk = None

    # Create the ephemeral keys for the exchange
    def Stage1(self):
        self.esk = self.RandomElementFromF_p()
        self.epk = self.esk*self.F(9)

        return (self.epk, self.pk)

    # exchange public keys and compute ssk - REMEMBER TO DELETE EPHEMERAL KEYS
    def Stage2(self, other):
        epk_other = other[0]
        pk_other = other[1]
        ssk = epk_other * self.esk + pk_other * self.sk

        # Deleting ephemeral keys
        self.esk = None
        self.epk = None

        return ssk
    
    # When generating multiple random numbers in a row, it is recommended to directly use the current_randstate of sage
    def RandomElementFromF_p(self):
        return current_randstate().python_random().randrange(self.F.order())
        #return self.F.random_element()


class Q5b():
    def __init__(self):
        self.Diffie  = Q5b_DH_Party("Diffie")
        self.Hellman = Q5b_DH_Party("Hellman")

        return

    # runs the exchange between
    def run(self):
        Diffie_pub  = self.Diffie.Stage1()
        Hellman_pub = self.Hellman.Stage1()

        Diffie_ssk  = self.Diffie.Stage2(Hellman_pub)
        Hellman_ssk = self.Hellman.Stage2(Diffie_pub)

        # Verifies the keys are the same 
        if (Diffie_ssk == Hellman_ssk):
            print("THE KEYS ARE THE SAME (this isn't apart of the protocol - it is just for testing purposes)")

        return

Q5b().run()