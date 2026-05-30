# HackerGame 2022 出题记

> 原文: https://www.ctfiot.com/76391.html
> ID: 76391


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
40
41
42
43
44
45
46
47
```



```
from Crypto.Util.number import *
from Crypto.Cipher import AES
import os

block_size=16
key_size=16

def pad(msg:bytes,block_size = 16):
 n = AES.block_size - len(msg) % AES.block_size
 return msg + bytes([n]) * n

def unpad(msg, block_size = 16):
 return msg[: -msg[-1]]

def xor(b1:bytes, b2:bytes):
 return bytes([x ^^ y for x, y in zip(b1, b2)])

def split_block(text:bytes):
 assert len(text)%block_size==0,'Invalid length'
 return [text[i*block_size:(i+1)*block_size] for i in range(len(text)//block_size)]

def AES_CBC_chosen_ciphertext(AES_key:bytes,plaintext:bytes,chosen_ciphertext:bytes,pos=None):
 # pos = None the iv will be set as chosen ciphertext
 # pos = -1 : the last block will be set as ciphertext
 # pos = i : the ith (from 0) block will be set as ciphertext 
 if pos==None:
 iv=chosen_ciphertext
 aes_cbc=AES.new(AES_key,AES.MODE_CBC,iv)
 return iv,aes_cbc.encrypt(msg)
 
 iv=os.urandom(block_size)
 aes_cbc=AES.new(AES_key,AES.MODE_CBC,iv)
 aes_ecb=AES.new(AES_key,AES.MODE_ECB)
 cipher=aes_cbc.encrypt(msg)
 msg_blocks=split_block(msg)
 cipher_blocks=split_block(cipher)
 cipher_blocks[pos]=chosen_ciphertext
 
 for i in range(pos-1,-1,-1):
 cipher_blocks[i]=xor(aes_ecb.decrypt(cipher_blocks[i+1]),msg_blocks[i+1])
 
 iv=xor(aes_ecb.decrypt(cipher_blocks[0]),msg_blocks[0])
 
 for i in range(pos+1,len(cipher_blocks)):
 cipher_blocks[i]=aes_ecb.encrypt(xor(cipher_blocks[i-1],msg_blocks[i]))
 
 return iv, b"".join(cipher_blocks)
```



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
```



```
def crc128(data, poly=0x883ddfe55bba9af41f47bd6e0b0d8f8f):
 crc = (1 << 128) - 1
 for b in data:
 crc ^^= b
 for _ in range(8):
 crc = (crc >> 1) ^^ (poly & -(crc & 1))
 return crc ^^ ((1 << 128) - 1)

def equivalent_affine_crc(crc = crc128, crc_bits = 128, target_bytes = 16):
 zero_crc = crc(target_bytes*b"\x00")
 target_bits = 8 * target_bytes
 v2n = lambda v: int(''.join(map(str, v)), 2)
 n2v = lambda n: vector(GF(2), bin(n)[2:].zfill(crc_bits))
 # n2v_t = lambda n: vector(GF(2), bin(n)[2:].zfill(target_bits))
 Affine_Matrix = []
 for i in range(target_bits):
 v = vector(GF(2), (j == i for j in range(target_bits)))
 value = crc(long_to_bytes(v2n(v),target_bytes)) ^^ zero_crc
 Affine_Matrix.append(n2v(value))
 # crc affine function: crc_128(x) = M*x+ C
 return matrix(GF(2),Affine_Matrix).transpose(), n2v(zero_crc)

def crc_128_reverse(crc_value):
 M , C = equivalent_affine_crc()
 # crc affine function: crc_128(x) = M*x+ C
 v2n = lambda v: int(''.join(map(str, v)), 2)
 n2v = lambda n: vector(GF(2), bin(n)[2:].zfill(128))
 res = M.solve_right(n2v(crc_value)+C)
 return long_to_bytes(v2n(res),16)
```



```
1
```



```
[(e, sub_element**e) for sub_element in g.standard_tuple for e in range(len(sub_element))]
```



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
```



```
def aupton(N): # compute terms a(0)..a(N)
 V = [1 for j in range(N+1)]
 for i in primerange(2, N+1):
 for j in range(N, i-1, -1):
 hi = V[j]
 pp = i
 while pp <= j:
 hi = max((pp if j==pp else V[j-pp]*pp), hi)
 pp *= i
 V[j] = hi
 return V
```



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
```



```
# sage 9.5
# For python you can use the `factorint` from sympy instead of `factor`
# from sympy import factorint
# factor = lambda x: list(factorint(x).items())
from math import sqrt,gcd
from Crypto.Util.number import *
from sympy import nextprime

def PrimeN(n):
 a = [0]*(n+1)
 a[0] = a[1] = 0
 for i in range(2,n+1):
 a[i] = 1
 for i in range(2,int(sqrt(n)+1)):
 mul = 2
 if (a[i] == 0):
 continue
 while (i * mul <= n):
 a[i * mul] = 0
 mul+=1
 return a

def max_order_element_combine(n,nums=1):
 #MX = [1]*(n+1)
 prime = PrimeN(n)
 prime_pows = {}
 # init item values
 for i in range(n,-1,-1):
 if not prime[i]:continue
 k = i*i
 prime_pows.setdefault(i,i)
 while (k <= n):
 prime[i]+=1
 prime_pows.setdefault(k,k)
 k *= i
 res = [] # store the results
 for _ in range(nums):
 MX = [1]*(n+1)
 for i in range(2,n+1):
 if not prime[i]:continue
 for j in range(n,1,-1):
 temp = i
 for k in range(1,prime[i]+1):
 if (j - temp >= 0 and MX[j] < MX[j - temp] * prime_pows[temp]):
 MX[j] = MX[j - temp] * prime_pows[temp]
 temp *= i
 
 res.append(MX[-1])
 res_facts = factor(res[-1])
 # renew the item weights
 for f in res_facts:
 p_f =f[0]**f[1]
 j = f[0]
 while j < n:
 if j <= p_f:
 prime_pows[j] = 1
 else:
 prime_pows[j] = min(j//p_f,prime_pows[j])
 j*=f[0]
 return res
```



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
```



```
# sage 9.5
# python version in python exp
def aupton_2(N): # compute terms a(0)..a(N)
 V = [1 for j in range(2*N+1)]
 for i in primerange(2, N+1):
 for j in range(2*N, i-1, -1):
 hi = V[j]
 pp = i
 while pp <= j:
 hi = max((pp if j==pp else V[j-pp]*pp), hi)
 pp *= i
 V[j] = hi
 return V
'''
Wikipedia subset sum approximation algorithm
http://en.wikipedia.org/wiki/Subset_sum_problem#Polynomial_time_approximate_algorithm
from https://github.com/saltycrane/subset-sum/blob/master/subsetsum/wikipedia.py
'''

import operator
def approx_with_accounting_and_duplicates(x_list,s):
 c = .01 # fraction error (constant)
 N = len(x_list) # number of values

 S = [(0, [])]
 for x in sorted(x_list):
 T = []
 for y, y_list in S:
 T.append((x + y, y_list + [x]))
 U = T + S
 U = sorted(U, key=operator.itemgetter(0))
 y, y_list = U[0]
 S = [(y, y_list)]

 for z, z_list in U:
 lower_bound = (float(y) + c * float(s) / float(N))
 if lower_bound < z <= s:
 y = z
 S.append((z, z_list))

 return sort_by_col(S, 0)[-1]

def split_2n(n,order):
 num_set = set([p^e for p,e in factor(order)])
 target_sum = n
 sum1,prime_list1 = approx_with_accounting_and_duplicates(num_set,target_sum)
 prime_list2 = num_set - set(prime_list1)
 sum2 = sum(prime_list2)
 if sum1 <= target_sum and sum2 <= target_sum:
 return prod(prime_list1),prod(prime_list2)
 
def Landu_expand(n):
 order = aupton_2(n)[-1]
 return split_2n(n,order)
```
