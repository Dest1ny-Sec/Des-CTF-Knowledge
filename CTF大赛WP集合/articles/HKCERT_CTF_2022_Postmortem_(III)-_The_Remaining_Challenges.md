# HKCERT CTF 2022 Postmortem (III): The Remaining Challenges

> 原文: https://www.ctfiot.com/87574.html
> ID: 87574


```
nc HOST PORT
? 1 37 37 97
? 33
?
nc HOST PORT
? 1 85 85 97
? 85
? 2 2 26 97
? 24
?
```



```
from pwn import *
from z3 import *
from operator import add, mul
from functools import reduce
from rich.progress import track
import itertools

# TODO: change this to the remote service
r = process('./chall')

for _ in track(range(100)):
 r.recvuntil('? '.encode())

 m, s, p, q = map(int, r.recvline().decode().split())

 _s = Solver()
 xs = [Int(f'x_{i}') for i in range(m)]

 subss = [Int(f'ss_{i}') for i in range(m)]
 subps = [Int(f'ps_{i}') for i in range(m)]

 # The base conditions
 for i in range(1, m):
 _s.add(xs[i-1] <= xs[i])
 for i in range(0, m):
 _s.add(Not(xs[i] <= 0))
 for i in range(0, m):
 _s.add(xs[i] < q)
 for i, j in itertools.product(range(0, m), repeat=2):
 _s.add(Implies(i != j, xs[i] != xs[j]))

 # The "s" and "p" requirements
 _s.add(subss[0] == xs[0])
 _s.add(subps[0] == xs[0])
 for i in range(m-1):
 _s.add(subss[i+1] == subss[i] + (i+2)*xs[i+1])
 _s.add(subps[i+1] == subps[i] * (i+2)*xs[i+1])
 _s.add(subss[m-1] % q == s)
 _s.add(subps[m-1] % q == p)

 assert _s.check() == sat
 md = _s.model()
 x0s = [md.evaluate(xs[i]) for i in range(m)]
 r.sendlineafter('? '.encode(), ' '.join(map(str, x0s)).encode())

print(r.recvline().strip().decode())
```



```
From above, we know (x0+0, y0+0, z0+0) is pointing rightwards and
 (x0+0, y0+0, z0+1) is pointing leftwards and ... and
 (x0+1, y0-2, z0+9) is pointing rightwards
for some (x0, y0, z0).

For each -20000 <= x <= 20000, 0 <= y <= 256, -20000 <= z <= 20000:
 If (x+0, y+0, z+0) is pointing rightwards and
 (x+0, y+0, z+1) is pointing leftwards and ... and
 (x+1, y-2, z+9) is pointing rightwards, then:
 (x, y, z) are the coordinates we want!
```



```
// An Java implementation of the `getRotation`
public static long getRotation(int x, int y, int z) {
 // Math#getSeed
 long l = (long)(x * 3129871) ^ (long)z * 116129781L ^ (long)y;
 l = l * l * 42317861L + l * 11L;
 long seed = l >> 16;

 // ModelBlockRenderer#tesselateWithAO
 Random random = new Random(seed);

 // WeightedBakedModel#getQuads
 return Math.abs(random.nextLong()) % 4;
}
```



```
public long nextLong() {
 return ((long)(next(32)) << 32) + next(32);
}
```



```
func getRotation(x, y, z int) int32 {
	/*
 long l = (long)(x * 3129871) ^ (long)z * 116129781L ^ (long)y;
 l = l * l * 42317861L + l * 11L;
 long seed = l >> 16;
	*/
	x2 := int(int32(x * 3129871))
	z2 := z * 116129781

	l := x2 ^ y ^ z2
	l = l * (l*42317861 + 11) // l = l*l*42317861 + l*11

	seed := l >> 16

	/*
 Random random = new Random(seed);
	*/
	seed ^= 0x5DEECE66D

	/*
 return Math.abs(random.nextLong()) % 4;
	*/
	v := int32((seed*0xBB20B4600A69 + 0x40942DE6BA) >> 16)
	if v < 0 {
 v = -v
	}
	return v & 3
}
```
