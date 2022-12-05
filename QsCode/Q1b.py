from cmath import sqrt
from operator import truediv
from sage.all import *

A = 486662
P = 2**255 - 19

F = GF(P)

E = EllipticCurve(F, [0, A, 0, 1, 0])     # Curve25519

Q = F(4)
Points = E.lift_x(Q, all=True)

P_1 = Points[0]
P_2 = Points[1]

print(P_1)

x_1 = (P_1[0]/P_1[1]) * sqrt( F(486664) )
y_1 = (P_1[0] - 1)/(P_1[0] + 1)

print("Point: (", x_1, ", ", y_1, ")")

x_2 = (P_2[0]/P_2[1]) * sqrt( F(486664) )
y_2 = (P_2[0] - 1)/(P_2[0] + 1)

print("Point: (", x_2, ", ", y_2, ")")
