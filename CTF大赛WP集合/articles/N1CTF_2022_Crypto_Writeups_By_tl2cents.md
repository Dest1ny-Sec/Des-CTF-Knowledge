# N1CTF 2022 Crypto Writeups By tl2cents

> 原文: https://www.ctfiot.com/76390.html
> ID: 76390


```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
from Crypto.Util.number import *
from random import getrandbits
from secret import flag

def keygen():
 p = getPrime(512)
 q = getPrime(512)
 n = p * q
 phi = (p-1)*(q-1)
 while True:
 a = getrandbits(1024)
 b = phi + 1 - a
 s = getrandbits(1024)
 t = -s*a * inverse(b, phi) % phi
 if GCD(b, phi) == 1:
 break
 return (s, t, n), (a, b, n)

def enc(m, k):
 s, t, n = k
 r = getrandbits(1024)
 return m * pow(r, s, n) % n, m * pow(r, t, n) % n

pubkey, privkey = keygen()
flag = pow(bytes_to_long(flag), 0x10001, pubkey[2])
c = []
for m in long_to_bytes(flag):
 c1, c2 = enc(m, pubkey)
 c.append((c1, c2))
print(pubkey)
print(c)
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
from ast import literal_eval
from Crypto.Util.number import *
from tqdm import tqdm

lines = open("./output.txt","r").readlines()
s,t,n = literal_eval(lines[0].strip())
enc = literal_eval(lines[1])

def xgcd(a: int, b: int):
 x0, y0, x1, y1 = 0, 1, 1, 0
 while a != 0:
 q, a, b = b // a, b % a, a
 x0, x1 = x1, x0 - x1 * q
 y0, y1 = y1, y0 - y1 * q
 return b, x0, y0

encflag = b""
r_list = []

for c1, c2 in tqdm(enc):
 if c1 == 0 and c2 == 0:
 # m is zero , r unknown, set -1
 encflag += bytes([0])
 r_list.append(-1)
 continue
 for m in range(256):
 g, x, y = xgcd(s, t)
 z = pow(c1, x, n)
 w = pow(c2, y, n)
 mm = pow(m, -(x+y), n)
 r_ = mm * z * w % n
 c1_ = (m * pow(r_, s // g, n)) % n
 c2_ = (m * pow(r_, t // g, n)) % n
 if c1_ == c1 and c2_ == c2:
 encflag += bytes([m])
 r_list.append(r_)
 break
print(encflag)
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
# Initialise rng (random.getrandbits)
import random
import time
import copy
from sympy import prod
from Crypto.Util.number import *
from ast import literal_eval
from tqdm import tqdm
from mt19937predictor import MT19937Predictor

off = 48
lines = open("./output.txt","r").readlines()
s,t,n = literal_eval(lines[0].strip())
enc = literal_eval(lines[1])

r = r_list # above r_list

data = r[off:20+off]
multi_r_list = []

def split32bit(d):
 temp = []
 for _ in range(1024//32):
 temp.append(d%2**32)
 d = d>>32
 assert d==0
 return temp

for d in data[:20]:
 assert d < n
 multi_ls = [split32bit(d)]
 while d + n < 2**1024:
 d = d + n
 multi_ls.append(split32bit(d))
 multi_r_list.append(multi_ls)

from itertools import product
brute_length = prod([len(i) for i in multi_r_list])
print(f"[+] Brute forcing space {brute_length} {brute_length.bit_length()}")

# split the brute-forcing space
expand_part = product(*(multi_r_list[-3:]))
brute_list = [product(*(multi_r_list[:-3]+[[f[0]],[f[1]],[f[2]]])) for f in expand_part]
n_cores = len(brute_list)
slice_length = brute_length//n_cores
datas = [[b] for b in brute_list]
print(f"[+] cores {n_cores}")

def verify_func(brute_list):
 for i in tqdm(brute_list,total=slice_length):
 MT_data = []
 for ls in i:
 MT_data.extend(ls)
 predictor = MT19937Predictor()
 for _ in range(624):
 predictor.setrandbits(MT_data[_], 32)

 mflag = True
 for _ in range(640-624):
 if predictor.getrandbits(32)!= MT_data[624 + _]:
 mflag = False
 break
 if mflag == False:
 continue
 # print(f"[+] possible result : {MT_data}")
 for _ in range(20):
 if predictor.getrandbits(1024)%n != r[20+off+_]:
 mflag = False
 break
 if mflag == False:
 continue
 print(f"[+] GOOD MT STATE")
 return (True,MT_data[:])
 return (False,[])

from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing
import os

def parallel_process(array, function, use_kwargs=False):
 """
 A parallel version of the map function with a progress bar.

 Args:
 array (array-like): An array to iterate over.
 function (function): A python function to apply to the elements of array
 n_jobs (int, default=16): The number of cores to use
 use_kwargs (boolean, default=False): Whether to consider the elements of array as dictionaries of
 keyword arguments to function
 front_num (int, default=3): The number of iterations to run serially before kicking off the parallel job.
 Useful for catching bugs
 Returns:
 [function(array[0]), function(array[1]), ...]
 """
 front = []
 n_jobs = n_cores
 with ProcessPoolExecutor(max_workers=n_jobs) as pool:
 if use_kwargs:
 futures = [pool.submit(function, **a) for a in array]
 else:
 futures = [pool.submit(function, *a) for a in array]
 kwargs = {
 'total': len(futures),
 'unit': 'it',
 'unit_scale': True,
 'leave': True
 }
 #Print out the progress as tasks complete
 for f in tqdm(as_completed(futures), **kwargs):
 res = f.result()
 if res[0] == True:
 print("[+] find!")
 print(res)
 pool.shutdown(wait=True, cancel_futures=True)
 break
 return res

res_list = parallel_process(datas,verify_func)
1
2
3
4
[+] Brute forcing space 7962624 23
[+] cores 12
 69%|██████████████████████████████████████████████████▍ | 458676/663552 [07:08<02:57, 1153.05it/s]
[+] GOOD MT STATE
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
data = res_list # results from above MT state
import random
from Crypto.Util.number import *
from ast import literal_eval
from tqdm import tqdm

lines = open("./output.txt","r").readlines()
s,t,n = literal_eval(lines[0].strip())
enc = literal_eval(lines[1])

# https://github.com/JuliaPoo/MT19937-Symbolic-Execution-and-Solver
import sys
sys.path.append('./source')
# Import symbolic execution
from MT19937 import MT19937, MT19937_symbolic
# Import XorSolver
from XorSolver import XorSolver
rng = lambda: random.getrandbits(1024)

rng_clone = MT19937(state_from_data = (data, 32))
shift = 64*(1024//32)
rng_clone.reverse_states(shift)

def get1024():
 res = 0
 temps = []
 for i in range(32):
 temps.append(rng_clone())
 for num in temps[::-1]:
 res = (res<<32) + num
 return res

res_ls = []
for _ in range(64):
 rnd_num = get1024()
 res_ls.append(rnd_num)
 if rnd_num%n == s%n:
 print("[+] cracked")
 a = res_ls[-2]
 break

kphi = s*a+(1-a)*t
print(f"[+] kphi found , verify {pow(2,kphi,n) == 1} ")
encflag = b'\x08EZg\xbf\xa0\xeb\x9d\x81\x01\xa8\x96m\x97\x08I(\xed\xb5iQE\xdb\xf5\x8c\xbdcr!\xe6\xc9\xac\x0c\x16K\xa0\x0fr\xecM\x04\xe6\x87\x0f}9\x94\xcfa\x16\x87\x8f4\xcd\xcb\xa4\x0eq\xc3Q\x16\x928&\xe2\x18C\xafN\x87\xcc\x18\xc2D\x9d\x06\xbd"\xe7\xe8\xb7\x12\xb0\xb8CC\x9aM\xff\x12\x00\x05,\xeeopYC)mI\xb7\x81\xb6\x13\x0e\x8a\xc0\xd7\xd3\xd2\xa9\xe5vg.\xa4\xf3\xaa\x10f\x9c\xa4nS=O\xe9'
encnum = bytes_to_long(encflag)
d = inverse(0x10001,kphi)
m = long_to_bytes(pow(encnum,d,n))
print(m)
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
from Crypto.Util.number import *
from math import prod
from secret import flag

def keygen(pbits,kbits,k):
 p = getPrime(pbits)
 x = [getPrime(kbits + 1) for i in range(k)]
 y = prod(x)
 while 1:
 r = getPrime(pbits - kbits * k)
 q = 2 * y * r + 1
 if isPrime(q):
 return p*q, (p, q, r, x)

def encrypt(key, message):
 return pow(0x10001, message, key)

key = keygen(512, 24, 20)
flag = bytes_to_long(flag)
messages = [getPrime(flag.bit_length()) for i in range(47)] + [flag]
enc = [encrypt(key[0], message) for message in messages]

print(messages[:-1])
print(enc)
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
C:\yafu-1.34>yafu-x64.exe -B1pm1 33554432 -B2pm1 4294967296

11/07/22 14:55:23 v1.34.5 @ TL2CENTS, System/Build Info:
Using GMP-ECM 6.3, Powered by GMP 5.1.1
detected 12th Gen Intel(R) Core(TM) i7-12700H
detected L1 = 49152 bytes, L2 = 25165824 bytes, CL = 64 bytes
measured cpu frequency ~= 2692.260400
using 20 random witnesses for Rabin-Miller PRP checks

===============================================================
======= Welcome to YAFU (Yet Another Factoring Utility) =======
======= bbuhrow@gmail.com =======
======= Type help at any time, or quit to quit =======
===============================================================
cached 78498 primes. pmax = 999983

>> pm1(131158523227880830085100826212925738665356578827561846263073537503153187073136528966506785633847097997799377037969243883439723340886038624250936927221630287086602285835045356221763554989140952262353930420392663280482277832613695689454662506372252641564106136178637816827646124189347219273164844809807934422046441)

pm1: starting B1 = 33554432, B2 = 4294967296 on C312

***factors found***

P158 = 12980311456459934558628309999285260982188754011593109633858685687007370476504059552729490523256867881534711749584157463076269599380216374688443704196597025947

***co-factor***
P155 = 10104420349837363561278745998119091841853342383118385156657416134976061697027571349895988817770681767227605656666215380267313369652920490697343475330713803

ans = 10104420349837363561278745998119091841853342383118385156657416134976061697027571349895988817770681767227605656666215380267313369652920490697343475330713803
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
from ast import literal_eval

lines = open("./output.txt","r").readlines()
messages = literal_eval(lines[0].strip())
enc = literal_eval(lines[1].strip())

M1 = matrix.identity(ZZ,47)
B1 = matrix(ZZ,47,1)
for i,message in enumerate(messages):
 B1[i,0] = message

M = block_matrix(ZZ,[B1,M1],ncols = 2)
L = M.LLL()

def coompute_kn(coff):
 # \sum mi*ki = coff[0]
 if coff[0]>0:
 res_right = 1
 res_left = pow(0x10001, coff[0])
 else:
 res_right = pow(0x10001, -coff[0])
 res_left = 1
 for i ,cof in enumerate(coff[1:]):
 if cof > 0:
 res_right = res_right * enc[i]**cof
 else:
 res_left = res_left * enc[i]**(-cof)
 return res_left - res_right

n0 = coompute_kn(L[0])
for i in range(1,47):
 kn = coompute_kn(L[i])
 n0 = gcd(kn,n0)
 print("[+] nbits ",n0.nbits())
 if n0.nbits()<=1024:
 print(n0)
 break
print(n0)
# filter small factors
n0 = factor(n0,limit=2^20)
n_ = n0[-1][0]
print(f"[+] find n : {n_}")
print(f"[+] n bits : {n_.nbits()}")
1
2
3
4
5
6
7
8
9
from Crypto.Util.number import *
encm = enc[-1]
discrete_log
p = 12980311456459934558628309999285260982188754011593109633858685687007370476504059552729490523256867881534711749584157463076269599380216374688443704196597025947
q = 10104420349837363561278745998119091841853342383118385156657416134976061697027571349895988817770681767227605656666215380267313369652920490697343475330713803
assert p*q==n_
GN = GF(p)
flag = discrete_log(GN(encm),GN(0x10001))
print(long_to_bytes(int(flag)))
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
from Crypto.Util.number import *
from secret import flag

m = Integer(int.from_bytes(flag, 'big'))

for _ in range(7):
 p = getPrime(512)
 q = getPrime(512)
 n = p * q
 while 1:
 try:
 a = randint(0,n)
 b = randint(0,n)
 Ep = EllipticCurve(GF(p), [a,b])
 Gp = Ep.lift_x(m) * 2
 Eq = EllipticCurve(GF(q), [a,b])
 Gq = Eq.lift_x(m) * 2
 y = crt([int(Gp[1]),int(Gq[1])],[p,q])
 break
 
except Exception as err:
 pass
 print(n, a, b, y)
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
from ast import literal_eval
lines = open("./output.txt","r").readlines()
fs = []
ns = []
para_s = []

def fun(n,a,b,y):
 Pn.<x> = PolynomialRing(Zmod(n))
 k = 4*(x^3+a*x+b)
 c = (3*x^2+a)^2
 f = k^3*y^2 - (c-2*x*k)^3 - a*(k^2*c-2*x*k^3) - b*k^3
 return f

for line in lines:
 n,a,b,y = [ZZ(i) for i in line.strip().split(" ")]
 f = fun(n,a,b,y).monic().change_ring(ZZ)
 fs.append(f)
 ns.append(n)
 para_s.append([n, a, b, y])

F = crt(fs,ns)
M = prod(ns)
FF = F.change_ring(Zmod(M))
roots = FF.small_roots(X = 2**400,epsilon = 1/40,beta = 4/7)
# m = FF.small_roots(X=2**256,beta=1.0)
print(roots)

from Crypto.Util.number import *
m = 15425251357776807541227287240467548867067510789583043568768907891381811730130189461693802496389917454461
print(m.nbits())
print(long_to_bytes(int(m)))
```
