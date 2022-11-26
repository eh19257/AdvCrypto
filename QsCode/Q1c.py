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

d = F(121665)/F(121666)

Ed_x_1 = (P_1[0]/P_1[1]) * sqrt( F(486664) )
Ed_y_1 = (P_1[0] - 1)/(P_1[0] + 1)

Ed_P_1 = ( (2 * Ed_x_1 * Ed_y_1) / (1 + d * (Ed_x_1**2) * (Ed_y_1**2) ), (Ed_y_1**2 - Ed_x_1**2) / (1 + d * (Ed_x_1**2) * (Ed_y_1**2) ))

print("First option for 2ϕ(P):", Ed_P_1)

Ed_x_2 = (P_2[0]/P_2[1]) * sqrt( F(486664) )
Ed_y_2 = (P_2[0] - 1)/(P_2[0] + 1)

Ed_P_2 = ( (2 * Ed_x_2 * Ed_y_2) / (1 + d * (Ed_x_2**2) * (Ed_y_2**2) ), (Ed_y_2**2 - Ed_x_2**2) / (1 + d * (Ed_x_2**2) * (Ed_y_2**2) ))

print("Second option for 2ϕ(P):", Ed_P_2)
