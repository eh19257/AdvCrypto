from cmath import sqrt
from operator import truediv
from sage.all import *

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