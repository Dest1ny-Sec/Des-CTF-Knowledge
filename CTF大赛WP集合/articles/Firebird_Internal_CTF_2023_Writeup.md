# Firebird Internal CTF 2023 Writeup

> 原文: https://www.ctfiot.com/95037.html
> ID: 95037

Gabrielle de Micheli, Nadia Heninger (2020) “Recovering cryptographic keys from partial information, by example”

https://hal.science/hal-03045663/document ↩︎

Juliano Rizzo, Thai Duong (2010) “Practical Padding Oracle Attacks”

https://www.usenix.org/legacy/event/woot10/tech/full_papers/Rizzo.pdf ↩︎


```
from Crypto.PublicKey import RSA
import random

random.seed(1337)

key = RSA.generate(2048)

t = [(key.p>>random.getrandbits(10))&1 if random.getrandbits(1) else (key.q>>random.getrandbits(10))&1 for i in range(2048)]
t = sum(t[i]<<i for i in range(2048))

with open('flag.txt', 'rb') as f:
 m = int.from_bytes(f.read(), 'big')

n, e = key.n, key.e
c = pow(m, e, n)

print(f'{n = }')
print(f'{e = }')
print(f'{t = }')
print(f'{c = }')

# n = 23972924803656725645946104612288180239254366533835447570211958435888835149024704127730216635918366064642338427956144263722073485986182242950506562077115261972266819566896991605805331175926336936623727858956342095970617971414648408199255433214266089182676417304576439449775708611349397255997892478936263800821533938404508818638694040349742659681140030800595271768949111564030020912493782604042297523251856213731597666043107228963973074577037344345426025975807448211052650699923918471883180836394144595630503970610793789138051476548955355193194759840128264687246565426588680843522246453634852078525991710060236523993541
# e = 65537
# t = 14000066433047292246448752794201977165563733655047203575867121262166187560566711892325594792129845153282249633931642143973215540568376319171334159461972160877466256238242152503653373908684017280676080125004854850332445723153614845802146395899581463896936557611606222767193353523987995818833578861773617167644193038121558267674251210114195760011821306729346761634659759967871454608623374306270379642305886119902085577927092579512468263725679201030921437666386689058685094677660425920780030296995254804923997961573399239884517270135267952236745232513979074599714453057660939074051865674834210296195715452442772175320306
# c = 6629119219609628910262885521069144816410786299451464969111007624958603576922839074850618464009859754669933262329186876226112761547177882680972685257697161919090897947135355903504454390331332951864051787079151186147963687429869735814443602986151345233136170388603746969296411646714158233418888611277576374237710204734229716394950713361265013458346462648487382316305877942127752214474859094795859454295294490880154326380500685914654596927550241665243599892940472157748432105831205326132442653659482947911799058715375236555903827420335782334212566356002880715361572706447898027515949713485430213701388248011598192532689
```



```
import random
import sys

MASKS = [(2<<i)-1 for i in range(1024)]

def guess(n, _ps, _qs, p0=0, q0=0, bits=0):
 n0 = p0 * q0
 if n == n0: return p0
 if n < n0: return

 for pb in _ps[bits]:
 p1 = p0 | (pb<<bits)
 for qb in _qs[bits]:
 q1 = q0 | (qb<<bits)
 if p1*q1 & MASKS[bits] != n & MASKS[bits]: continue
 res = guess(n, _ps, _qs, p1, q1, bits+1)
 if res is not None: return res

sys.setrecursionlimit(1027)
n = 23972924803656725645946104612288180239254366533835447570211958435888835149024704127730216635918366064642338427956144263722073485986182242950506562077115261972266819566896991605805331175926336936623727858956342095970617971414648408199255433214266089182676417304576439449775708611349397255997892478936263800821533938404508818638694040349742659681140030800595271768949111564030020912493782604042297523251856213731597666043107228963973074577037344345426025975807448211052650699923918471883180836394144595630503970610793789138051476548955355193194759840128264687246565426588680843522246453634852078525991710060236523993541
e = 65537
t = 14000066433047292246448752794201977165563733655047203575867121262166187560566711892325594792129845153282249633931642143973215540568376319171334159461972160877466256238242152503653373908684017280676080125004854850332445723153614845802146395899581463896936557611606222767193353523987995818833578861773617167644193038121558267674251210114195760011821306729346761634659759967871454608623374306270379642305886119902085577927092579512468263725679201030921437666386689058685094677660425920780030296995254804923997961573399239884517270135267952236745232513979074599714453057660939074051865674834210296195715452442772175320306
c = 6629119219609628910262885521069144816410786299451464969111007624958603576922839074850618464009859754669933262329186876226112761547177882680972685257697161919090897947135355903504454390331332951864051787079151186147963687429869735814443602986151345233136170388603746969296411646714158233418888611277576374237710204734229716394950713361265013458346462648487382316305877942127752214474859094795859454295294490880154326380500685914654596927550241665243599892940472157748432105831205326132442653659482947911799058715375236555903827420335782334212566356002880715361572706447898027515949713485430213701388248011598192532689

# Known bits
random.seed(1337)
bs = [(0, random.getrandbits(10)) if random.getrandbits(1) else (1, random.getrandbits(10)) for i in range(2048)]

_ps = [[0, 1] for _ in range(1024)]
_qs = [[0, 1] for _ in range(1024)]

for i, (id, b) in enumerate(bs):
 v = (t>>i) & 1
 if id == 0:
 assert _ps[b] in [[v], [0, 1]]
 _ps[b] = [v]
 else:
 assert _qs[b] in [[v], [0, 1]]
 _qs[b] = [v]

p = guess(n, _ps, _qs)
assert n % p == 0
q = n // p

phi_n = (p-1) * (q-1)
d = pow(e, -1, phi_n)

m = pow(c, d, n)
flag = int(m).to_bytes(2048//8, 'big').lstrip(b'\0')
print(f'{flag = }')
```



```
class Hacker:
 def __init__(self, srv):
 # The function to check if the padding is correct
 self.srv = srv

 def __oracle(self, token):
 try:
 self.srv.authenticate(token.hex())
 return True
 except Exception as err:
 return str(err) not in [
 'Padding is incorrect.',
 'PKCS#7 padding is incorrect.'
 ]

 def __recover_block(self, ciphertext_block):
 iv = bytearray(16)

 for k in range(16):
 for i in range(256):
 iv[15-k] = i
 crafted_iv = xor(iv, bytes([k+1 for _ in range(16)]))
 if self.__oracle(crafted_iv + ciphertext_block): break
 return iv

 def __recover(self, ciphertext):
 return b''.join([
 xor(ciphertext[i-16:i],
 self.__recover_block(ciphertext[i:i+16]))
 for i in range(16, len(ciphertext), 16)
 ])
 
 def crack(self, token):
 token = bytes.fromhex(token)
 m = self.__recover(token)
 m = unpad(m, 16)
 m = parse_qs(m.decode())

 username, = m.get('username')
 password, = m.get('password')

 return username, password
```



```
000102030405060708090a0b0c0d0e0f 1d53a4e415b0893fc386fbea776b7198
```



```
> auth 204094b9bec1ea6b9473d345130699d2de1c31278bda8b9f4695bc8fac7116735f78bb7509cd5add82abcdca9bf7989d 
?️ The token is correct for foo!
> auth 204094b9bec1ea6b9473d345130699d2de1c31278bda8b9f4695bc8fac7116735f78bb7509cd5add82abcdca9bf7989e 
?️ Invalid token: Padding is incorrect..
```



```
from pwn import *

r = remote('carbon-chal.firebird.sh', 36013)

r.sendline(b'register foo xxxxxxxx\x02')
# username=foo&password=xxxxxxxx\x02

tokens = []
while len(tokens) == 0:
 # Create 1024 tokens at once to save time
 for _ in range(1024):
 r.sendline(b'signin foo xxxxxxxx\x02')

 for _ in range(1024):
 r.recvuntil(b'Signed in as foo with token ')
 token = bytes.fromhex(r.recvuntil(b'.')[:-1].decode())
 
 if token[30] != 1: continue
 if token[31]^0x1^0x2 > token[31]: continue
 tokens.append(token.hex())

token = tokens[0]
print(f'{token = }')
r.sendline(f'hack {token}'.encode())
r.recvuntil(b'WHY? ')

r.interactive()
```



```
f84bf7049cb55a0e1457d977e6cfbc0cc49ee1102da505e10aa3c32e619180446617ae2270cba3629b0851ae627236f19bb9cbfcadcd010eb923d170cbc2a7
```



```
import random
import re
from Crypto.Cipher import AES
from Crypto.Util import Counter
from operator import mul
from functools import reduce

# f i r e b i r d { }
known = bytes.fromhex('ffffffffffffffffff8080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080ff')
m = bytes.fromhex('66697265626972647b00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007d')
c = bytes.fromhex('f84bf7049cb55a0e1457d977e6cfbc0cc49ee1102da505e10aa3c32e619180446617ae2270cba3629b0851ae627236f19bb9cbfcadcd010eb923d170cbc2a7')

def xor(a, b):
 return bytes([u^^v for u, v in zip(a, b)])

keystreams = []
for k in range(256):
 cipher = AES.new(bytes([k]) + b'\0'*15, AES.MODE_CTR, counter=Counter.new(128, initial_value=int(0)))
 keystreams.append(
 cipher.encrypt(b'\0'*len(c))
 )

A = []
b = []

# The number of entries I guessed that they are zeroes
# Suggested: sampled_zeroes + number_of_equations >= 256 (or add some more to avoid less false positives...)

number_of_equations = bin(int.from_bytes(known, 'big')).count('1')
sampled_zeroes = 256 - number_of_equations
assert sampled_zeroes <= 256-16
print(f'{sampled_zeroes + number_of_equations = }')

for i, (rc, mc, cc) in enumerate(zip(known, m, c)):
 for j in range(8):
 if (rc>>j) & 1 == 0: continue
 mb = (mc>>j) & 1
 cb = (cc>>j) & 1

 row = [(k[i]>>j) & 1 for k in keystreams]

 A.append(row)
 b.append(mb^^cb)

F = GF(2)
A = Matrix(F, A)
b = vector(F, b)

hit_frequency = reduce(mul, [(256-16-k)/(256-k) for k in range(sampled_zeroes)])
print(f'{number_of_equations = }')
print(f'{sampled_zeroes = }')
print(f'Expecting a hit every {int(1/hit_frequency)} times')

attempt = 0
while True:
 attempt += 1

 # The 128 entries "I" guessed it is non-zero
 v = sorted(random.sample(range(256), k=256-sampled_zeroes))
 
 _A = A[:, v]
 try:
 x0 = _A.solve_right(b)
 for dx in _A.right_kernel():
 flag = c
 set_bits_count = 0
 for i in range(256-sampled_zeroes):
 if x0[i] == dx[i]: continue
 set_bits_count += 1
 flag = xor(flag, keystreams[v[i]])

 flag = flag.decode()
 if not re.match(r'firebird\{\w+\}', flag): continue
 if set_bits_count > 16: continue

 print(f'[*] Flag recovered at attempt #{attempt}: {flag}')
 assert False, 'done!'

 except KeyboardInterrupt:
 raise KeyboardInterrupt
 except AssertionError as err:
 raise err
 except:
 pass
```
