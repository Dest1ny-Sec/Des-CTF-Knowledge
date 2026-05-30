# Solving SandboxAQ’s Post-Quantum Crypto CTF

> 原文: https://www.ctfiot.com/169657.html
> ID: 169657


```
"""
 Returns the rotation matrix of poly, i.e.,
 the matrix consisting of the coefficient vectors of
 poly, X * poly, X^2 * poly, ..., X^(deg(poly)-1) * poly
 modulo X^n-1.
 If cyclotomic = True, then reduction mod X^n+1 is applied, instead of X^n-1.
"""
def rotMatrix(poly, cyclotomic=False):
 n = len(poly)
 A = np.array( [[0]*n for _ in range(n)] )

 for i in range(n):
 for j in range(n):
 c = 1
 if cyclotomic and j < i:
 c = -1

 A[i][j] = c * poly[(j-i)%n]

 return A

"""
 Given a list of polynomials poly = [p_1, ...,p_n],
 this function returns a rows*cols matrix,
 consisting of the rotation matrices of p_1, ..., p_n.
"""
def module( polys, rows, cols ):
 if rows*cols != len(polys):
 raise ValueError("len(polys) has to equal rows*cols.")

 n = len(polys[0])
 for poly in polys:
 if len(poly) != n:
 raise ValueError("polys must not contain polynomials of varying degrees.")

 blocks = []

 for i in range(rows):
 row = []
 for j in range(cols):
 row.append( rotMatrix(polys[i*cols+j], cyclotomic=True) )
 blocks.append(row)

 return np.block( blocks )
polys = []
for i in range(k*k):
 polys.append( A[i] )

A = module(polys, 2, 2)
n = 32
sage: m = 32
sage: D_e = {-1:0.33, 0:0.33, 1:0.33}
sage: D_s = {0:0.5, 1:0.5}
sage: D_e = {-1:0.33, 0:0.33, 1:0.34}
sage: A,t, dbdd = initialize_from_LWE_instance(DBDD_predict, n, q, m, D_e, D_s)
 Build DBDD from LWE
 n= 32 m= 32 q=251
sage: beta, delta = dbdd.estimate_attack()
 Attack Estimation
 dim= 65 δ=1.045280 β=2.00
    #include 
    #include <NTL/ZZ_pX.h>
    #include <omp.h>

    #define MODULE 251
    #define DEGREE 16

using namespace std;
using namespace NTL;

bool isSmall(const ZZ_pX& poly) {
 for (int i = 0 ; i < DEGREE ; ++i) {
 if ((coeff(poly, i) != 0) && (coeff(poly, i) != (MODULE - 1)) && (coeff(poly, i) != 1) && (coeff(poly, i) != -1)) {
 return false;
 }
 }
 return true;
}

void numberToPoly(ZZ_pX& poly, long n) {
 for (int i = 0 ; i < DEGREE ; ++i) {
 if ((n>>i) & 1) {
 SetCoeff(poly, i, 1);
 } else {
 SetCoeff(poly, i, 0);
 }
 }
}

int main() {

 // Initialization
 ZZ q_zz(MODULE);
 ZZ_pInfo = new ZZ_pInfoT(q_zz);
 ZZ_pX t, a1, a2;
 long a1_vec[16] = {180, 198, 3, 194, 39, 34, 122, 189, 209, 91, 209, 5, 88, 25, 229, 195};
 long a2_vec[16] = {229, 246, 105, 8, 222, 24, 73, 11, 212, 71, 138, 77, 30, 58, 83, 187};
 long t_vec[16] = {9, 145, 210, 114, 215, 36, 243, 174, 134, 22, 205, 240, 177, 107, 188, 109};

 for (int i = 0 ; i < DEGREE ; ++i) {
 SetCoeff(a1, i, a1_vec[i]);
 SetCoeff(a2, i, a2_vec[i]);
 SetCoeff(t, i, t_vec[i]);
 }

 // Polynomial X^N + 1
 ZZ_pX XNplus1;
 SetCoeff(XNplus1, DEGREE, 1);
 SetCoeff(XNplus1, 0, 1);

 // Bruteforce to test all possible s1 and s2
 #pragma omp parallel for
 for (long s1_n = 1; s1_n < (1 << DEGREE); s1_n++) {
 ZZ_pX s1, s2, temp1, temp2;
 ZZ_pX to_test;
 // segfault protection when using OpenMP
 long q2 = MODULE;
 ZZ q_zz2(q2);
 ZZ_pInfo = new ZZ_pInfoT(q_zz2);
 numberToPoly(s1, s1_n);
 for (long s2_n = 1; s2_n < (1 << DEGREE); s2_n++) {
 // Construction of polynomials s1 and s2 from their integer form
 numberToPoly(s2, s2_n);
 temp1 = MulMod(a1, s1, XNplus1);
 temp2 = MulMod(a2, s2, XNplus1);
 to_test = t - (temp1 + temp2);
 // Verify if the t - A*s yields a small equation (aka solution in [-1,0,1])
 if (isSmall(to_test)) {
 cout << "FOUND s1 = " << s1_n << " and s2 = " << s2_n << endl;
 }
 }
 }
 cout << "Bruteforce over" << endl;
 return 0;
}
K = 2
N = 16
q = 251

R.<x> = Zmod(q)[]
RR = R.quotient(x^N +1)
RR

# Keygen outputs:
A1 = RR(195*x^15+229*x^14+25*x^13+88*x^12+5*x^11+209*x^10+91*x^9+209*x^8+189*x^7+122*x^6+34*x^5+39*x^4+194*x^3+3*x^2+198*x+180)
A2 = RR(187*x^15+83*x^14+58*x^13+30*x^12+77*x^11+138*x^10+71*x^9+212*x^8+11*x^7+73*x^6+24*x^5+222*x^4+8*x^3+105*x^2+246*x+229)
A3 = RR(84*x^15+95*x^14+224*x^13+177*x^12+43*x^11+155*x^10+63*x^9+246*x^8+232*x^7+177*x^6+53*x^5+243*x^4+41*x^3+111*x^2+73*x+234)
A4 = RR(3*x^15+85*x^14+143*x^13+51*x^12+177*x^11+116*x^10+247*x^9+222*x^8+181*x^7+33*x^6+78*x^5+196*x^4+188*x^3+216*x^2+170*x+64)
A = matrix(RR, [[A1,A2], [A3,A4]])

t1 = RR(109*x^15+188*x^14+107*x^13+177*x^12+240*x^11+205*x^10+22*x^9+134*x^8+174*x^7+243*x^6+36*x^5+215*x^4+114*x^3+210*x^2+145*x+9)
t2 = RR(198*x^15+159*x^14+120*x^13+184*x^12+217*x^11+224*x^10+96*x^9+124*x^8+30*x^7+155*x^6+247*x^5+34*x^4+224*x^3+154*x^2+240*x+235)
t = matrix(RR, [t1,t2])

# Encryption outputs:
u1= RR([49, 227, 248, 198, 5, 218, 34, 86, 30, 121, 37, 124, 19, 243, 118, 49])
u2= RR([112, 190, 242, 199, 70, 141, 85, 141, 128, 82, 224, 218, 28, 147, 70, 41])
u = matrix(RR, [u1,u2])
v = RR([29, 156, 77, 121, 232, 189, 96, 34, 16, 86, 80, 165, 81, 72, 206, 78])

# decompress function
def decompress(m_n):
 res = [1]*16
 for i in range(16):
 e = m_n[0][0].list()[i]
 if e in range(-q//4, q//4):
 res[i] = 0
 return res

# results of the bruteforce
s1 = RR([1,1,1,1,1,0,1,1,0,0,0,1,0,0,1,1])
s2 = RR([1,0,0,0,1,0,1,1,1,0,0,1,0,1,1,1])
s = matrix(RR, [s1,s2])

err = t.transpose() - A * s.transpose()

print(err[0][0].list())
print("error in -1,0,1:", all(coeffs in [0,1,250] for coeffs in err[0][0].list()))
m_n = v - s * u.transpose() #decryption
print("flag:", decompress(m_n)) #decompression
[0, 0, 1, 0, 1, 0, 1, 1, 250, 250, 250, 1, 0, 0, 250, 0]
error in -1,0,1: True
flag: [1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1]
dgoudarzi@xxxxx ~/c3> ./ctf_server
Serving on default port 1337
Socket created
Socket bind succeed
Socket listening
Client connected
orig seed = 000000000000000000000000000000000000000000000000010101010001010000000101000100000001010100000001
Shared secret successfully received
Secure AES256 established
[+] Data of each packets:
[+]
[+] Src addr: 127.0.0.1:
47826 (client)
[+] Dst addr: 127.0.0.1:
1337 (server)
[+]
[+] Data size: 16
[+] Data content:
[+] 00000000 4e 53 31 00 00 00 00 00 00 00 00 00 00 00 00 00 |N S 1 . . . . . . . . . . . . .|
[+]
[+] ----------------------------------------------------------------------------------------------------
[+]
[+] Src addr: 127.0.0.1:
1337 (server)
[+] Dst addr: 127.0.0.1:
47826 (client)
[+]
[+] Data size: 800
[+] Data content:
[+] 00000000 4f a6 1e 20 97 84 18 14 c1 3f d3 90 b1 a7 b0 dc |O . . . . . . . ? . . . . . .|
 ......................
[+] 00000310 61 f8 d4 ca eb a1 7c cc db b3 a2 45 98 cb 5b 78 |a . . . . . | . . . . E . . [ x|
[+]
[+] ----------------------------------------------------------------------------------------------------
[+]
[+] Src addr: 127.0.0.1:
47826 (client)
[+] Dst addr: 127.0.0.1:
1337 (server)
[+]
[+] Data size: 768
[+] Data content:
[+] 00000000 af 38 0d 94 fa 86 23 bc ce 15 96 67 52 58 9b cf |. 8 . . . . # . . . . g R X . .|
 ......................
[+] 000002f0 c7 c0 37 75 dc ef 65 b9 8e 83 d0 8f f9 49 65 74 |. . 7 u . . e . . . . . . I e t|
[+]
[+] ----------------------------------------------------------------------------------------------------
[+]
[+] Src addr: 127.0.0.1:
47826 (client)
[+] Dst addr: 127.0.0.1:
1337 (server)
[+]
[+] Data size: 48
[+] Data content:
[+] 00000000 59 13 79 db 74 e2 d5 d6 da 92 59 c8 7d 30 c7 42 |Y . y . t . . . . . Y . } 0 . B|
[+] 00000010 d9 1c 3d 4c 23 ca 9d 28 20 c9 fd db 6a 91 b7 e6 |. . = L # . . ( . . . j . . .|
[+] 00000020 8e 0d 9e 14 7b 07 6f ec 44 25 0a 6b a6 4f 75 9e |. . . . { . o . D % . k . O u .|
[+]
[+] ----------------------------------------------------------------------------------------------------
[+]
[+] Src addr: 127.0.0.1:
1337 (server)
[+] Dst addr: 127.0.0.1:
47826 (client)
[+]
[+] Data size: 16
[+] Data content:
[+] 00000000 32 68 1c 94 ee f7 38 a1 36 ac 49 d4 9f ae 64 38 |2 h . . . . 8 . 6 . I . . . d 8|
[+]
[+] ----------------------------------------------------------------------------------------------------
[+]
[+] Src addr: 127.0.0.1:
1337 (server)
[+] Dst addr: 127.0.0.1:
47826 (client)
[+]
[+] Data size: 368
[+] Data content:
[+] 00000000 5a 18 c7 f5 31 30 50 aa 7c ef 0f 22 d4 64 d7 43 |Z . . . 1 0 P . | . . " . d . C|
[+] 00000010 d9 1c 3d 4c 23 ca 9d 28 20 c9 fd db 6a 91 b7 e6 |. . = L # . . ( . . . j . . .|
[+] 00000020 5a 18 c7 f5 31 30 50 aa 7c ef 0f 22 d4 64 d7 43 |Z . . . 1 0 P . | . . " . d . C|
[+] 00000030 5e 37 60 21 a9 fc 00 dd c2 27 f8 33 43 2e 53 3f |^ 7 ` ! . . . . . ' . 3 C . S ?|
[+] 00000040 5a 18 c7 f5 31 30 50 aa 7c ef 0f 22 d4 64 d7 43 |Z . . . 1 0 P . | . . " . d . C|
[+] 00000050 99 8a 6f 5f 71 1b 17 43 92 90 2d ff 24 0f 2b bf |. . o _ q . . C . . - . $ . + .|
[+] 00000060 5a 18 c7 f5 31 30 50 aa 7c ef 0f 22 d4 64 d7 43 |Z . . . 1 0 P . | . . " . d . C|
[+] 00000070 a7 35 81 2d 11 d1 59 ca 1b d2 86 09 2a 27 d7 98 |. 5 . - . . Y . . . . . * ' . .|
[+] 00000080 5a 18 c7 f5 31 30 50 aa 7c ef 0f 22 d4 64 d7 43 |Z . . . 1 0 P . | . . " . d . C|
[+] 00000090 ee 99 f6 c5 c4 48 17 1f 95 1d 1c 85 2d bd 98 90 |. . . . . H . . . . . . - . . .|
[+] 000000a0 5a 18 c7 f5 31 30 50 aa 7c ef 0f 22 d4 64 d7 43 |Z . . . 1 0 P . | . . " . d . C|
[+] 000000b0 73 57 22 51 18 39 01 92 2c b2 08 c0 ec ff 4e c1 |s W " Q . 9 . . , . . . . . N .|
[+] 000000c0 5a 18 c7 f5 31 30 50 aa 7c ef 0f 22 d4 64 d7 43 |Z . . . 1 0 P . | . . " . d . C|
[+] 000000d0 d4 3c 61 00 67 4f 00 f6 a7 a7 df a6 80 c8 5a 7a |. < a . g O . . . . . . . . Z z|
[+] 000000e0 5a 18 c7 f5 31 30 50 aa 7c ef 0f 22 d4 64 d7 43 |Z . . . 1 0 P . | . . " . d . C|
[+] 000000f0 80 74 8c bf 8a fc 6d 7f 4c 34 f4 36 5c 80 4a 82 |. t . . . . m L 4 . 6 \ . J .|
[+] 00000100 da 34 bd fb 15 6c b7 8c d6 82 3b 60 1e 59 11 4d |. 4 . . . l . . . . ; ` . Y . M|
[+] 00000110 5a 18 c7 f5 31 30 50 aa 7c ef 0f 22 d4 64 d7 43 |Z . . . 1 0 P . | . . " . d . C|
[+] 00000120 bb bf 81 99 04 0f 0c 11 f7 62 be e2 9a 97 77 b7 |. . . . . . . . . b . . . . w .|
[+] 00000130 5a 18 c7 f5 31 30 50 aa 7c ef 0f 22 d4 64 d7 43 |Z . . . 1 0 P . | . . " . d . C|
[+] 00000140 e6 dc 48 d4 97 94 20 04 f5 c8 09 5f 67 89 53 70 |. . H . . . . . . . _ g . S p|
[+] 00000150 5a 18 c7 f5 31 30 50 aa 7c ef 0f 22 d4 64 d7 43 |Z . . . 1 0 P . | . . " . d . C|
[+] 00000160 8e 0d 9e 14 7b 07 6f ec 44 25 0a 6b a6 4f 75 9e |. . . . { . o . D % . k . O u .|
[+]
[+] ----------------------------------------------------------------------------------------------------
orig_seed = local_78;
OQS_randombytes(orig_seed);
local_78 = (undefined [16])0x0;
auVar2._8_8_ = 0;
auVar2._0_8_ = local_68._8_8_ & 0x101010101010101;
local_68 = auVar2 << 0x40;
local_58._8_8_ = local_58._8_8_ & 0x101010101010101;
local_58._0_8_ = local_58._0_8_ & 0x101010101010101;
// brute force part
int rc, res;
struct AES_ctx ctx;
for (size_t i=0; i<16777216; i++) {
 for (size_t j=0; j<24; j++){
 entropy_input[24+j] = (i>>j) & 1;
 }
 OQS_randombytes_nist_kat_init_256bit(entropy_input, NULL);
 rc = OQS_KEM_kyber_1024_keypair(public_key,secret_key);
 res = memcmp(public_key, test_public_key, OQS_KEM_kyber_1024_length_public_key);
 if (res == 0) {
 for (size_t j=0; j<24; j++) {
 printf("%d, ", entropy_input[24+j]);
 }
 return 0;
 }
}
// // recovering pcap communications
OQS_randombytes_nist_kat_init_256bit(entropy_input, NULL);
int rc = OQS_KEM_kyber_1024_keypair(public_key, secret_key);
rc = OQS_KEM_kyber_1024_decaps(shared_secret, ciphertext, secret_key);

for (size_t i=0; i<32; i++) {
 printf("%02X", shared_secret[i]);
}
DIR.ENDb.txt
.
d.txt
c.txt
ctf_server
abc
bfg
..
server_secret.txt
a.txt
abc.txt
ENDPUTclient_secret.txtEND1337h@x0r
ENDDIR.ENDb.txt
.
d.txt
c.txt
ctf_server
client_secret.txt
abc
bfg
..
server_secret.txt
a.txt
abc.txt
ENDGETserver_secret.txtENDMy v0ice is my p@ssport.
END
def _init_key_settings(self):
 ...
 self.defaultCurve = "x25519kyber768draft00"
 self.keyShares = ["x25519kyber768draft00"]
 ...
def calc_shared_key(self, private, peer_share):
 """Calculate the shared key,"""
 if self.group in self._x_groups:
 ...
 elif self.group == GroupName.x25519kyber768draft00:
 x25519_ps = peer_share[:32]
 kyber_ps = peer_share[32:]
 S = x25519(private[:32], x25519_ps)
 self._non_zero_check(S)
 kb = kyber.Kyber(kyber.DEFAULT_PARAMETERS['kyber_768'])
 skb = kb.dec(kyber_ps, private[32:])
 return S+skb
@classmethod
def _genKeyShareEntry(cls, group, version):
 """Generate KeyShareEntry object from randomly selected private value.
 """
 kex = cls._getKEX(group, version)
 private = kex.get_random_private_key()
 share = kex.calc_public_value(private)
 kb = kyber.Kyber(kyber.DEFAULT_PARAMETERS['kyber_768'])
 pub, priv = kb.keygen()
 return KeyShareEntry().create(group, share + pub, private + priv)
Handshake success
Received data: HTTP/1.1 200 OK
Date: Wed, XX Mar 2024 XX:XX:XX GMT
Content-Length: 78
Content-Type: text/plain; charset=utf-8

The flag is: 5443184089537ac26d77f5605e1d0c8271597ca097ef1b40be77c7a7bbd62d90.
```
