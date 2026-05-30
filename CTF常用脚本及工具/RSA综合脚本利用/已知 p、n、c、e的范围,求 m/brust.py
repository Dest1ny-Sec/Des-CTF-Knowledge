#!/usr/bin/env python
# -*- coding:utf-8 -*-
from base64 import b64encode as b32encode
from base64 import b64decode
from gmpy2 import invert, gcd, iroot
from Crypto.Util.number import *

p = 177077389675257695042507998165006460849
n = 37421829509887796274897162249367329400988647145613325367337968063341372726061
c64 = '==gMzYDNzIjMxUTNyIzNzIjMyYTM4MDM0gTMwEjNzgTM2UTN4cjNwIjN2QzM5ADMwIDNyMTO4UzM2cTM5kDN2MTOyUTO5YDM0czM3MjM'
c = int ( b64decode ( str ( c64)[::-1] ) )
print ( c )
q = n // p
phi = (p - 1) * (q - 1)
for e in range ( 50000, 70000 ):
    if  gcd ( e, phi ) == 1:
        d = invert ( e, phi )
        m = pow ( c, d, n )
        flag=str(long_to_bytes(m))
        if 'flag' in flag or 'CTF' in flag or ("{" in flag and '}'in flag):
            print(flag)