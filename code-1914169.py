from cmath import *
from sage.all import *
from sage.misc.randstate import current_randstate
from operator import truediv

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

        print("Diffie's  ssk: {0}".format(Diffie_ssk))
        print("Hellman's ssk: {0}".format(Hellman_ssk))
        
        # Verifies the keys are the same 
        if (Diffie_ssk == Hellman_ssk):
            print("THE KEYS ARE THE SAME")

        return


def Q1a():
    A = 486662
    P = 2**255 - 19

    F = GF(P)

    E = EllipticCurve(F, [0, A, 0, 1, 0])     # Curve25519

    #E_t = EllipticCurve([0, A, 0, 1, 0])  # test curve
    # X(Q)  = 4 = x/z = 8/2
    # X(2Q) = x_2/z_2
    x = 8
    z = 2

    x_2 = F((x**2 - z**2)**2)
    z_2 = F(4*x*z*(x**2 + A*x*z + z**2))

    Q_2 = x_2/z_2

    print("X coordinate of 2P is:", Q_2, "\n")

    print("We don't care about the y value but here they are anyway:", E.lift_x(Q_2, all=True))

    #print("\n\n", E.lift_x(F(4), all=True))



    ###### Verify ######

    #P = E.lift_x(4)
    #X = P+P
    #print(X)

    ####################

def Q1b():
    A = 486662
    P = 2**255 - 19

    F = GF(P)

    E = EllipticCurve(F, [0, A, 0, 1, 0])     # Curve25519

    Q = F(4)
    Points = E.lift_x(Q, all=True)

    P_1 = E(4, 10396089888167458996693606908380331970145732977558722329349539962582616845133)
    P_2 = P_1#Points[0]

    x_1 = (P_1[0]/P_1[1]) * sqrt( F(486664) )
    y_1 = (P_1[0] - 1)/(P_1[0] + 1)

    print("Image of P: (", x_1, ", ", y_1, ")")

    x_2 = (P_2[0]/P_2[1]) * -sqrt( F(486664) )
    y_2 = (P_2[0] - 1)/(P_2[0] + 1)

    print("- Image of P: (", x_2, ", ", y_2, ")")


def Q1c():
    A = 486662
    P = 2**255 - 19

    F = GF(P)

    E = EllipticCurve(F, [0, A, 0, 1, 0])     # Curve25519

    Q = F(4)
    Points = E.lift_x(Q, all=True)

    P_1 = E(4, 10396089888167458996693606908380331970145732977558722329349539962582616845133)#Points[0]
    P_2 = P_1#Points[1]

    d = F(121665)/F(121666)

    Ed_x_1 = (P_1[0]/P_1[1]) * sqrt( F(486664) )
    Ed_y_1 = (P_1[0] - 1)/(P_1[0] + 1)

    Ed_P_1 = ( (2 * Ed_x_1 * Ed_y_1) / (1 + d * (Ed_x_1**2) * (Ed_y_1**2) ), (Ed_y_1**2 - Ed_x_1**2) / (1 - d * (Ed_x_1**2) * (Ed_y_1**2) ))

    print("Option for 2ϕ(P):", Ed_P_1)


    Ed_x_2 = (P_2[0]/P_2[1]) * -sqrt( F(486664) )
    Ed_y_2 = (P_2[0] - 1)/(P_2[0] + 1)

    Ed_P_2 = ( (2 * Ed_x_2 * Ed_y_2) / (1 + d * (Ed_x_2**2) * (Ed_y_2**2) ), (Ed_y_2**2 - Ed_x_2**2) / (1 - d * (Ed_x_2**2) * (Ed_y_2**2) ))

    print("Option for -2ϕ(P):", Ed_P_2)


Q1a()
#Q1b()
#Q1c()
#Q5b().run()

print("Open up the program and comment/uncommment the lines above me")