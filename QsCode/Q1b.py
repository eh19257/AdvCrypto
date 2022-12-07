from cmath import sqrt
from operator import truediv
from sage.all import *

A = 486662
P = 2**255 - 19

F = GF(P)

E = EllipticCurve(F, [0, A, 0, 1, 0])     # Curve25519

Q = F(4)
Points = E.lift_x(Q, all=True)

P_1 = E(4, 10396089888167458996693606908380331970145732977558722329349539962582616845133)
P_2 = P_1#Points[0]

#print("Point 1:", P_1)
#print("Point 1 + Point 1:", P_1 + P_1, "\n")


#print("Point 2:", P_2)
#print("Point 2 + Point 2:", P_2 + P_2, "\n")

#print("Points:", E.lift_x((P_1+P_1)[0], all=True))

x_1 = (P_1[0]/P_1[1]) * sqrt( F(486664) )
y_1 = (P_1[0] - 1)/(P_1[0] + 1)

print("Image of P: (", x_1, ", ", y_1, ")")

x_2 = (P_2[0]/P_2[1]) * -sqrt( F(486664) )
y_2 = (P_2[0] - 1)/(P_2[0] + 1)

print("- Image of P: (", x_2, ", ", y_2, ")")
