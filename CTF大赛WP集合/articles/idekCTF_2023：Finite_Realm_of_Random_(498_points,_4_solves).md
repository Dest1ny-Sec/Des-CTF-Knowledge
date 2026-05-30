# idekCTF 2023：Finite Realm of Random (498 points, 4 solves)

> 原文: https://www.ctfiot.com/92878.html
> ID: 92878

Introduction

Our team Black Bauhinia participated in the idekCTF 2023 which spans two days. Finite Realm of Random was an interesting math / crypto puzzle. In the end, only 3 teams solved it the intended way, and we were the second.

Problem Statement

Description: I took a flag, and shuffled it. I took a part, and randomized it. I took the bits and pieces, and scattered them across the field. Now, only an haphazard mess remains.

Author: A~Z

Binary: finite-realm-of-random.tar.gz

Solution Outline

By observing that the code maps the original flag-encoded polynomial to its Galois conjugates, we try the 32 possibilities and retrieve the flag.

A Bit of Math

Let L=F12732 and g be a fixed generator of L. The flag is splitted into character blocks and the following operation is performed:

The block is encoded by c→=(c0,c1,…,c31)↦f=c0+c1g+c2g2+⋯+c31g31

For at most 5 times:

Two elements r1 and r2 are chosen with the same minimal polynomial in L

Find a polynomial φ(X)∈F127[X] that satisfies deg(φ)≤31 and φ(r1)=f

Replace f↦φ(r2)

We receive the resulting f

Let’s first analyse the curious code in 2(a) by recalling the following fact.

Lemma: Let L/K be a Galois extension. Then, the minimal polynomial of any α∈L∖K is

f(x)=∏σ∈Gal(L/K)(x−σ(α)).

In fancy math terms, we say that the minimal polynomial of α are precisely the Galois conjugates of α. Applying this to our problem, we see that r2=σ(r1) for some σ∈Gal(L/K). Moreover, recall that the Galois group of a finite field is exactly the powers of the Froebnius endomorphism:

Gal(Fpn/Fp)={Frobpi:0≤i<n}≅Z/nZ

Where Frobp is the map x↦xp. Hence, r1 and r2 are Galois conjugates and we can write r2=r1pkfor some 0≤k<32.

Let’s move on to the rest of the algorithm. We now compute a polynomial that maps r1↦f and see where r2 maps to. With our new gained knowledge, this part is easy to figure out. In fact, since the field has characteristics p, we have the following fact:

Claim: We have φ(r2)=φ(r1)pk.

Proof: We apply Freshman’s Dream. Writing φ(X)=∑i=031diXi, we have

φ(r1)pk=(∑i=031dir1i)pk=∑i=031(dir1i)pkFreshman’s dream=∑i=031dir1ipk=φ(r1pk)=φ(r2)

Where the third line uses the fact that di∈F127, so raising di to the pk-th power results in di. By definition, φ(r1)=f, so we get that φ(r2)=fpk. This means that step (2) in the original algorithm simply maps f to one of its conjugates by f↦fpk. Therefore, to recover the original f, we simply look at all 32 conjugates of the resulting f and check if it is valid ASCII with the correct length.

Code

# Curiously, random is not random
L = GF(127)
for i in range(5):
 L = L['x'].irreducible_element(2, algorithm='random').splitting_field(f't{i}')

# Parses resulting f
ct = bytes.fromhex(open('out.txt', 'r').read())
assert len(ct) % L.degree() == 0
blocks = [L(list(map(int, ct[i:i + L.degree()]))) for i in range(0, len(ct), L.degree())]

def convert(poly):
 return bytes(map(int, poly.polynomial().coefficients()))

for c in blocks:
 for i in range(32):
 # Checks conjugates by f -> f^(p^i)
 r = bytes(vector(c^(127^i)))
 if all(32 <= t < 127 or t == 0 for t in r):
 print(r.decode())

Flag: idek{4nd_7hu5_5p0k3_G4!015:_7h3_f1n1t3_r34Lm_sh4ll_n07_h4rb0ur_r4nd0mn355,_0n!y_7h3_fr0b3n1u5__}

Conclusion

Thank you A~Z and all other idekCTF authors for the challenges. It was a lot of fun and I learned quite a lot! Also thank you to my team members, Mystiz and LifeIsHard (new member) for offering their mental support and listening to my nonstop rant for 48 hours. Writeups for other challenges may or may not appear in the future.

Unrelated note: I am now on Mastodon, and you will find me more active there than on Twitter. Check me out over there! There are quite a few exciting things going on.

POV: You are trying to understand the source code of this problem:


```
# Curiously, random is not random
L = GF(127)
for i in range(5):
 L = L['x'].irreducible_element(2, algorithm='random').splitting_field(f't{i}')

# Parses resulting f
ct = bytes.fromhex(open('out.txt', 'r').read())
assert len(ct) % L.degree() == 0
blocks = [L(list(map(int, ct[i:i + L.degree()]))) for i in range(0, len(ct), L.degree())]

def convert(poly):
 return bytes(map(int, poly.polynomial().coefficients()))

for c in blocks:
 for i in range(32):
 # Checks conjugates by f -> f^(p^i)
 r = bytes(vector(c^(127^i)))
 if all(32 <= t < 127 or t == 0 for t in r):
 print(r.decode())
```
