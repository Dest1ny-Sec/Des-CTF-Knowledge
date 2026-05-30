# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 12:44:52 2018
@author: Baron
"""

import numpy as np
from numpy.linalg import *


def my_int_inv(mat, n=26):
    x = np.zeros(mat.shape, dtype=np.int16)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            x[i, j] = int(round(mat[i, j])) % n
    return x


def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b


def exgcd(a, m):
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (
            u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


a = np.mat([[2, 19],[0,4]])
b = np.mat([[0], [0]])
m = np.mat([[24, 17, 13, 8, 14], [14, 15, 13, 18, 20], [20, 8, 14, 5, 17]])

c = a * m + b
c = my_int_inv(c)

a_inv = a.I
a_det = det(a)
a_adju = my_int_inv(a_det * a_inv)
a_det_inv = exgcd(int(round((det(a) % 26))), 26)
aa_inv = my_int_inv(a_det_inv * a_adju)
m = (aa_inv * (c - b)) % 26
print(m)
