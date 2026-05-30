# 【2025春节】解题领红包所有题writeup

> 原文: https://www.ctfiot.com/227568.html
> ID: 227568

作者论坛账号：BMK （通杀榜第一名）

公众号设置“星标”，您不会错过新的消息通知

如开放注册、精华文章和周边活动等公告


```
复制代码 隐藏代码
from struct import *
def shift(z, y, x, k, p, e):
    return ((((z >> 5) ^ (y << 2)) + ((y >> 3) ^ (z << 4))) ^ ((x ^ y) + (k[(p & 3) ^ e] ^ z)))
def encrypt(v, k):
    delta = 0x9E3779B9
    n = len(v)
    rounds = 6 + 52 // n
    x = 0
    z = v[n - 1]
    for i in range(rounds):
        x = (x + delta) & 0xFFFFFFFF
        e = (x >> 2) & 3
        for p in range(n - 1):
            y = v[p + 1]
            v[p] = (v[p] + shift(z, y, x, k, p, e)) & 0xFFFFFFFF
            z = v[p]
        p += 1
        y = v[0]
        v[n - 1] = (v[n - 1] + shift(z, y, x, k, p, e)) & 0xFFFFFFFF
        z = v[n - 1]
    return v
def decrypt(v, k):
    delta = 0x9E3779B9
    n = len(v)
    rounds = 6 + 52 // n
    x = (rounds * delta) & 0xFFFFFFFF
    y = v[0]
    for i in range(rounds):
        e = (x >> 2) & 3
        for p in range(n - 1, 0, -1):
            z = v[p - 1]
            v[p] = (v[p] - shift(z, y, x, k, p, e)) & 0xFFFFFFFF
            y = v[p]
        p -= 1
        z = v[n - 1]
        v[0] = (v[0] - shift(z, y, x, k, p, e)) & 0xFFFFFFFF
        y = v[0]
        x = (x - delta) & 0xFFFFFFFF
    return v
from base64 import *

if __name__ == '__main__':
    key = list(unpack("<4I",b"my-xxtea-secretx00"))
    enc = b64decode(b"hjyaQ8jNSdp+mZic7Kdtyw==")
    print(len(enc))
    enc = list(unpack(f"<{len(enc)//4}I",enc))
    print(enc)
    pt = decrypt(enc,key)
    s = b''
    for i in range(len(pt)):
        s+=pack("> 28 & 15)][(num2 >> 28 & 15)]
            num6 = v12[i][24 * j + 1][(num3 >> 28 & 15)][(num4 >> 28 & 15)]
            num7 = v12[i][24 * j + 2][(num >> 24 & 15)][(num2 >> 24 & 15)]
            num8 = v12[i][24 * j + 3][(num3 >> 24 & 15)][(num4 >> 24 & 15)]
            v16[4 * j] = (v12[i][24 * j + 4][num5][num6] << 4 | v12[i][24 * j + 5][num7][num8])
            num5 = v12[i][24 * j + 6][(num >> 20 & 15)][(num2 >> 20 & 15)]
            num6 = v12[i][24 * j + 7][(num3 >> 20 & 15)][(num4 >> 20 & 15)]
            num7 = v12[i][24 * j + 8][(num >> 16 & 15)][(num2 >> 16 & 15)]
            num8 = v12[i][24 * j + 9][(num3 >> 16 & 15)][(num4 >> 16 & 15)]
            v16[4 * j + 1] = (v12[i][24 * j + 10][num5][num6] << 4 | v12[i][24 * j + 11][num7][num8])
            num5 = v12[i][24 * j + 12][(num >> 12 & 15)][(num2 >> 12 & 15)]
            num6 = v12[i][24 * j + 13][(num3 >> 12 & 15)][(num4 >> 12 & 15)]
            num7 = v12[i][24 * j + 14][(num >> 8 & 15)][(num2 >> 8 & 15)]
            num8 = v12[i][24 * j + 15][(num3 >> 8 & 15)][(num4 >> 8 & 15)]
            v16[4 * j + 2] = (v12[i][24 * j + 16][num5][num6] << 4 | v12[i][24 * j + 17][num7][num8])
            num5 = v12[i][24 * j + 18][(num >> 4 & 15)][(num2 >> 4 & 15)]
            num6 = v12[i][24 * j + 19][(num3 >> 4 & 15)][(num4 >> 4 & 15)]
            num7 = v12[i][24 * j + 20][(num & 15)][(num2 & 15)]
            num8 = v12[i][24 * j + 21][(num3 & 15)][(num4 & 15)]
            v16[4 * j + 3] = (v12[i][24 * j + 22][num5][num6] << 4 | v12[i][24 * j + 23][num7][num8])
            num = v13[i][4 * j][v16[4 * j]]
            num2 = v13[i][4 * j + 1][v16[4 * j + 1]]
            num3 = v13[i][4 * j + 2][v16[4 * j + 2]]
            num4 = v13[i][4 * j + 3][v16[4 * j + 3]]
            num5 = v12[i][24 * j][(num >> 28 & 15)][(num2 >> 28 & 15)]
            num6 = v12[i][24 * j + 1][(num3 >> 28 & 15)][(num4 >> 28 & 15)]
            num7 = v12[i][24 * j + 2][(num >> 24 & 15)][(num2 >> 24 & 15)]
            num8 = v12[i][24 * j + 3][(num3 >> 24 & 15)][(num4 >> 24 & 15)]
            v16[4 * j] = (v12[i][24 * j + 4][num5][num6] << 4 | v12[i][24 * j + 5][num7][num8])
            num5 = v12[i][24 * j + 6][(num >> 20 & 15)][(num2 >> 20 & 15)]
            num6 = v12[i][24 * j + 7][(num3 >> 20 & 15)][(num4 >> 20 & 15)]
            num7 = v12[i][24 * j + 8][(num >> 16 & 15)][(num2 >> 16 & 15)]
            num8 = v12[i][24 * j + 9][(num3 >> 16 & 15)][(num4 >> 16 & 15)]
            v16[4 * j + 1] = (v12[i][24 * j + 10][num5][num6] << 4 | v12[i][24 * j + 11][num7][num8])
            num5 = v12[i][24 * j + 12][(num >> 12 & 15)][(num2 >> 12 & 15)]
            num6 = v12[i][24 * j + 13][(num3 >> 12 & 15)][(num4 >> 12 & 15)]
            num7 = v12[i][24 * j + 14][(num >> 8 & 15)][(num2 >> 8 & 15)]
            num8 = v12[i][24 * j + 15][(num3 >> 8 & 15)][(num4 >> 8 & 15)]
            v16[4 * j + 2] = (v12[i][24 * j + 16][num5][num6] << 4 | v12[i][24 * j + 17][num7][num8])
            num5 = v12[i][24 * j + 18][(num >> 4 & 15)][(num2 >> 4 & 15)]
            num6 = v12[i][24 * j + 19][(num3 >> 4 & 15)][(num4 >> 4 & 15)]
            num7 = v12[i][24 * j + 20][(num & 15)][(num2 & 15)]
            num8 = v12[i][24 * j + 21][(num3 & 15)][(num4 & 15)]
            v16[4 * j + 3] = (v12[i][24 * j + 22][num5][num6] << 4 | v12[i][24 * j + 23][num7][num8])
    change_index()
    for k in range(16):
        v16[k] = table4[k][v16[k]]

    for l in range(16):
        v16[l] = v16[l]

flag = 1

for ss in range(16):
    v16 = [i for i in range(97, 97 + 16)]
    AAA()
    for i in v16:
        print(hex(i)[2:].zfill(2), end='')
    print()

# 3694bf644864b8474a4576bb89c69f14
# 1094bf644864b85e4a4554bb89ac9f14
# 9d94bf644864b8514a45d7bb89299f14
# 0ff94bf644864b8f74a45a7bb8939f14
# 1894bf644864b8eb4a4567bb896a9f14
# 0360bf642c64b8474a4576cb89c62f14
# 3660bf646764b8474a45768e89c6af14
# 3697bf646764b8474a45764289c61b14
# 36d5bf647f64b8474a45763589c64214
# 3694e96448afb847834576bb89c69f54
# 3694fd64486db847814576bb89c69f8d
# 3694ae6448d9b847744576bb89c69fbb
# 3694c1644893b847214576bb89c69f97
# 3694bfc84864ef474ab176bbcac69f14
# 03694bf3f48647474ab576bb23c69f14
# 03694bf84864ef474ad176bb11c69f14
# 3694bf3f4864c2474ad476bbcac69f14
data = b"""
43941d39cd79f798851e0f2928123ad2
24941d39cd79f76a851ebb2928103ad2
84941d39cd79f726851ec42928373ad2
83941d39cd79f7bf851ed12928633ad2
c4941d39cd79f78b851e822928373ad2
43e81d398b79f798851e0f06281246d2
43d01d39c479f798851e0f72281238d2
43d61d39ee79f798851e0fab28128ed2
432f1d399a79f798851e0faa281269d2
43947d39cdcaf798511e0f2928123ae0
43942339cd18f798bd1e0f2928123a27
4394ce39cd26f798bd1e0f2928123ab4
43949f39cd2af7983b1e0f2928123a1c
43941d9ccd79c69885d20f2931123ad2
43941d9bcd794c9885eb0f2930123ad2
43941d2ccd79099885010f2929123ad2
43941d47cd79879885230f2942123ad2"""
with open("E://trace",'wb') as f:
    f.write(data)
import phoenixAES
phoenixAES.crack_file('E://trace',[],True,False,3)
复制代码 隐藏代码
Last round key #N found:
931C3A97F6D1C217E58CF94FC843B226931C3A97F6D1C217E58CF94FC843B226
复制代码 隐藏代码
from Crypto.Cipher.AES import *
a = new(key=bytes.fromhex("7E13141528AED2A6ABF7158809CF4F3C"),mode=MODE_OFB,iv=b'x00'*16)
enc = [0x48, 0x27, 0x8F, 0xAF, 0x9B, 0xF8, 0xEC, 0x72, 0x98, 0x07, 0x72, 0x0C, 0x6B, 0xE2, 0x3A, 0xB6,0x42,0x59,0xf7]
print(a.decrypt(bytes(enc)))
from hashlib import md5
print("flag{"+md5(b"19150922025").hexdigest()+"}")
复制代码 隐藏代码
    #include <stdio.h>
    #include <stdint.h>

//加密函数
void encrypt (uint32_t* v, uint32_t* k) {
    uint32_t v0=v[1], v1=v[0], sum=0, i;           /* set up */
    uint32_t delta=0xB979379E;                     /* a key schedule constant */
    uint32_t k0=k[0], k1=k[1], k2=k[2], k3=k[3];   /* cache key */
    for (i=0; i < 12; i++) {                       /* basic cycle start */
        sum += delta;
        v1 += ((v0<<4) + k0) ^ (v0 + sum) ^ ((v0>>5) + k1);
        v0 += ((v1<<4) + k2) ^ (v1 + sum) ^ ((v1>>5) + k3);
    }                                              /* end cycle */
    v[0]=v0; v[1]=v1;
}

//解密函数
void decrypt (uint32_t* v, uint32_t* k) {
    uint32_t v0=v[0], v1=v[1], sum=0xB1AE9B68, i;  /* set up */
    uint32_t delta=0xB979379E;                     /* a key schedule constant */
    uint32_t k0=k[0], k1=k[1], k2=k[2], k3=k[3];   /* cache key */
    for (i=0; i<12; i++) {                         /* basic cycle start */
        v0 -= ((v1<<4) + k2) ^ (v1 + sum) ^ ((v1>>5) + k3);
        v1 -= ((v0<<4) + k0) ^ (v0 + sum) ^ ((v0>>5) + k1);
        sum -= delta;
    }                                              /* end cycle */
    v[0]=v1; v[1]=v0;
}

int main()
{
    uint32_t v2[2]={0x04040404,0x20375DA2}/*魔改的hash值*/,k1[4]={0x1231F787, 0x9ACD6D9A, 0xD7851B65, 0x473457C1},k2[4]={0xC52D865C, 0x10778A6E, 0xB728E994, 0x1746382E},k3[4]={0x779375B2, 0xEFCB8541, 0x7459F437, 0x090D1E5D};
    uint32_t v0[2]={0,1738762200};/*时间戳*/
    uint32_t v1[2]={0,0x1d38d4};/*uid*/
    // v为要加密的数据是两个32位无符号整数
    // k为加密解密密钥，为4个32位无符号整数，即密钥长度为128位
    printf("加密前原始数据：%x %xn",v2[0],v2[1]);
    encrypt(v2, k3);

    printf("n");
    encrypt(v0, k1);
    encrypt(v1, k2);
    for(int i=0;i<8;i++)
    {
        printf("%02x",*((unsigned char*)v0+i));
    }
    for(int i=0;i<8;i++)
    {
        printf("%02x",*((unsigned char*)v1+i));
    }
    for(int i=0;i<8;i++)
    {
        printf("%02x",*((unsigned char*)v2+i));
    }
    printf("n");
    return 0;
}
# 98cb14e80b42d569ed33224c27a8b943a6695125feffda2d
复制代码 隐藏代码
00000000 vm_s struc ; (sizeof=0x10008, mappedto_33)
00000000 mem dd 16384 dup(?)
00010000 pc dw ?
00010002 top dw ?
00010004 flag dw ?
00010006 field_10006 dw ?
00010008 vm_s ends
复制代码 隐藏代码
opcodes = [0xBF, 0x7F, 0x80, 0xF0, 0xF0, 0xE0, 0xE6, 0xC7, 0x14, 0x41, 0xF7, 0x24, 0xB0, 0xE3, 0xE5, 0xE3, 0xD8, 0xD8, 0xE0, 0xF0, 0xC7, 0x25, 0x68, 0xF8, 0x41, 0xF1, 0x68, 0x7F, 0xE8, 0x19, 0xE0, 0x97, 0x19, 0xF0, 0xC7, 0x1C, 0xF1, 0x68, 0xE5, 0xF7, 0x35, 0xF7, 0xDA, 0x93, 0x94, 0x52, 0x56, 0x28, 0x52, 0x56, 0xF7, 0x41, 0x28, 0xB0, 0xE4, 0xA8, 0x68, 0x98, 0x34, 0x28, 0xF1, 0x28, 0x28, 0x34, 0xF1, 0x28, 0x34, 0xE2, 0xBF, 0x43, 0xF5, 0x7F, 0x0B, 0x41, 0xE4, 0xE2, 0xD8, 0xF7, 0x2D, 0x38, 0x28, 0x41, 0xF1, 0x68, 0xE5, 0xA8, 0xF5, 0xE6, 0xE3, 0x68, 0xE6, 0xBF, 0xA6, 0xE2, 0x28, 0x42, 0x19, 0xE5, 0x97, 0x08, 0x46, 0x19, 0xF5, 0x68, 0xE0, 0xF7, 0x1C, 0xCF, 0xDC, 0x19, 0xF8, 0xF7, 0xFB, 0xF7, 0x53, 0xF7, 0xC1, 0x55, 0x53, 0x28, 0x52, 0x56, 0xF3, 0x28, 0x54, 0x54, 0x28, 0x08, 0x33, 0xE3, 0xBF, 0x32, 0xE3, 0xE3, 0xBF, 0xBB, 0x80, 0xF0, 0xF7, 0x66, 0xE3, 0xF0, 0xD8, 0x08, 0x28, 0xF7, 0x6C, 0xE3, 0xF1, 0xD8, 0x08, 0x28, 0xF7, 0x61, 0xE3, 0xF2, 0xD8, 0x08, 0x28, 0xF7, 0x67, 0xE3, 0xF3, 0xD8, 0x08, 0x28, 0xF7, 0x7B, 0xE3, 0xF4, 0xD8, 0x08, 0x28, 0xF7, 0x7D, 0xE3, 0xF7, 0x1C, 0xD8, 0x08, 0x28, 0x31, 0xF1, 0x53, 0x54, 0xE0, 0x57, 0x10, 0x28, 0xE0, 0x55, 0x53, 0x28, 0xF0, 0xF8, 0xF7, 0x32, 0xBF, 0x61, 0xF7, 0x30, 0xBF, 0x5D, 0xF7, 0x32, 0xBF, 0x59, 0xF7, 0x35, 0xBF, 0x55, 0xE3, 0x95, 0x96, 0x94, 0x95, 0x94, 0xBF, 0x4D, 0xF7, 0x35, 0xBF, 0x49, 0xF7, 0x32, 0xBF, 0x45, 0xF7, 0x70, 0xBF, 0x41, 0xF7, 0x6F, 0xBF, 0x3D, 0xF7, 0x6A, 0xBF, 0x39, 0xF7, 0x69, 0xBF, 0x35, 0xF7, 0x65, 0xBF, 0x31, 0xE3, 0x96, 0x94, 0x96, 0xBF, 0x2B, 0xF7, 0x61, 0xBF, 0x27, 0xF7, 0x66, 0xBF, 0x23, 0xF7, 0x64, 0xBF, 0x1F, 0xF7, 0x6D, 0xBF, 0x1B, 0xE3, 0x92, 0x96, 0xBF, 0x16, 0xF7, 0x32, 0xBF, 0x12, 0xF7, 0x30, 0xBF, 0x0E, 0xF7, 0x32, 0xBF, 0x0A, 0xF7, 0x35, 0xBF, 0x06, 0xE3, 0xBF, 0x03, 0x58, 0x28, 0x31, 0xF7, 0x20, 0xF7, 0x83, 0x57, 0x08, 0x28, 0xF7, 0xB8, 0xF7, 0xED, 0x57, 0x08, 0x28, 0x57, 0x10, 0x28, 0xF4, 0xF3, 0x68, 0xE4, 0xE4, 0xA8, 0x08, 0xE0, 0xF1, 0x48, 0x10, 0xE3, 0x48, 0x41, 0x91, 0x08, 0xE1, 0xF8, 0x42, 0xF0, 0xCF, 0xF1, 0x42, 0x1A, 0x32, 0x36, 0x6D, 0xB4, 0xB5, 0x11, 0x86, 0x2C, 0x24, 0xC0, 0x49, 0xB4, 0xBA, 0x1C, 0x09, 0x94, 0xF2, 0x24, 0x17, 0x17, 0xB9, 0xD3, 0x89, 0x2A, 0x05, 0xA2, 0xD6, 0x08, 0x9F, 0xF3, 0x90, 0xCB, 0xF3, 0x14, 0x4D, 0xA2, 0x9C, 0xFA, 0xB3, 0x0E, 0x9A, 0x82, 0x0F, 0x14, 0x63, 0x38, 0x5C, 0x94, 0xD4, 0x59, 0x0D, 0xB0, 0xCF, 0xC4, 0x8E, 0x23, 0x38, 0xBB, 0xB4, 0x68, 0x53, 0x09, 0xE7, 0x9B, 0x29, 0x8D, 0xD4, 0x36, 0x9D, 0x83, 0xB3, 0x55, 0xDA, 0xB5, 0xAB, 0xF7, 0xD8, 0x6E, 0xD1, 0xD9, 0xB4, 0xA8, 0x18, 0xBF, 0x58, 0xCC, 0x1E, 0x13, 0x38, 0x66, 0xFB, 0x95, 0xD1, 0x37, 0xC1, 0x78, 0x77, 0x59, 0x10, 0xF8, 0x5D, 0x44, 0xA7, 0xA8, 0xCD, 0x85, 0xBF, 0x01, 0xD7, 0xC3, 0xC2, 0x3B, 0x0C, 0x0A, 0x52, 0x15, 0xE2, 0x13, 0xE6, 0xD8, 0x05, 0x5E, 0x0E, 0x3E, 0x1F, 0xC3, 0x0A, 0xA6, 0xA5, 0xCD, 0xD6, 0xAE, 0x45, 0xEF, 0x2C, 0xCB, 0x05, 0x4D, 0xCC, 0xA3, 0x93, 0x91, 0xA7, 0xF0, 0x98, 0xB9, 0x02, 0x65, 0x95, 0xEB, 0x2C, 0x48, 0xC7, 0xFF, 0xF4, 0x6B, 0x2C, 0xA1, 0x5C, 0xB3, 0xDA, 0xE6, 0x99, 0xEB, 0xC7, 0x1E, 0x2A, 0xE9, 0x58, 0x06, 0x2A, 0x71, 0x14, 0xC3, 0xE8]
pc = 0
stack = [0,1915092,0x1000,0x2000]+[0]*0x1000
top = 3
mem = [...]

while True:

    next_pc = pc+1
    op = opcodes[pc]>>3
    imm = opcodes[pc]&7
    print("pc=", hex(pc), hex(op),hex(top*4), end="t")
    if imm == 7:
        imm = opcodes[next_pc]
        next_pc+=1
    if op in [0,12,14,17,20,29]:
        f = 1
        result = stack[top]
        break
    elif op == 1:
        print(f"xor {stack[top]=:x},{stack[top-1]=:x}")
        stack[top-1] = stack[top]^stack[top-1]
        top-=1
    elif op == 2:
        print(f"neg {stack[top]=:x}")
        stack[top] = (-stack[top])&0xffffffff
    elif op == 3:
        print(f"pop {imm=}")
        top-=imm
    elif op == 4 or op == 26:
        print("nop")
    elif op == 5:
        print(f"or {stack[top]=:x},{stack[top - 1]=:x}")
        stack[top - 1] = stack[top] | stack[top - 1]
        top -= 1
    elif op == 6:
        print(f"ret")
        stack[top-1-imm] = stack[top]
        next_pc = stack[top-1]
        top -= imm+1
    elif op == 7:
        print(f"cmpnz {stack[top - 1]=:x},{stack[top]=:x}")
        stack[top - 1] = stack[top] != stack[top - 1]
        top -= 1
    elif op == 8:
        print(f"swap {stack[top - imm]=:x},{stack[top]=:x}")
        stack[top - imm] ,stack[top] = stack[top] ,stack[top - imm]
    elif op == 9:
        print(f"and {stack[top - 1]=:x},{stack[top]=:x}")
        stack[top - 1] = stack[top] & stack[top - 1]
        top -= 1
    elif op == 10:
        print(f"shl {stack[top]=:x},{imm=}")
        stack[top] = (stack[top]<> imm) & 0xffffffff
    elif op == 19:
        print(f"div {stack[top-1]=:x},{stack[top]=:x}")
        stack[top-1] = stack[top-1] // stack[top]
        top -= 1
    elif op == 21:
        print(f"movzx {stack[top]=:x}")
        stack[top] = stack[top]&0xff
    elif op == 22:
        print(f"mul {stack[top-1]=:x},{stack[top]=:x}")
        stack[top-1] = (stack[top-1] * stack[top]) & 0xffffffff
        top -= 1
    elif op == 23:
        if imm&0x80!=0:
            imm = -(0x100-imm)
        print(f"call {next_pc=}+{imm}")
        stack[top + 1] =next_pc
        next_pc+=imm
        top += 1
    elif op == 24 :
        if imm&0x80!=0:
            imm = -(0x100-imm)
        print(f"jz {stack[top-1]=:x},{stack[top]=:x}+{imm=}")
        if stack[top-1] == stack[top]:
            next_pc = next_pc+imm
        top-=2
    elif op == 25:
        if imm&0x80!=0:
            imm = -(0x100-imm)
        print(f"jnz {stack[top - 1]=:x},{stack[top]=:x}+{imm=}")
        if stack[top - 1] != stack[top]:
            next_pc = next_pc + imm
        top -= 2
    elif op == 27:
        print(f"load mem[{stack[top-1]=:x},{stack[top]=:x}]")
        stack[top-1] = mem[(stack[top]+(stack[top-1]&0xffff))]
        top -= 1
    elif op == 28:

        print(f"push stack[{top-imm=}] {stack[top-imm]:x}")
        stack[top+1] = stack[top-imm]
        top += 1
    elif op == 30:
        print(f"push {imm=:x}")
        stack[top + 1] = imm
        top += 1
    elif op == 31:
        print(f"dec {stack[top]=:x}")
        stack[top] = (stack[top]-1) & 0xffffffff

    pc = next_pc
复制代码 隐藏代码
opcodes = [0xBF, 0x7F, 0x80, 0xF0, 0xF0, 0xE0, 0xE6, 0xC7, 0x14, 0x41, 0xF7, 0x24, 0xB0, 0xE3, 0xE5, 0xE3, 0xD8, 0xD8, 0xE0, 0xF0, 0xC7, 0x25, 0x68, 0xF8, 0x41, 0xF1, 0x68, 0x7F, 0xE8, 0x19, 0xE0, 0x97, 0x19, 0xF0, 0xC7, 0x1C, 0xF1, 0x68, 0xE5, 0xF7, 0x35, 0xF7, 0xDA, 0x93, 0x94, 0x52, 0x56, 0x28, 0x52, 0x56, 0xF7, 0x41, 0x28, 0xB0, 0xE4, 0xA8, 0x68, 0x98, 0x34, 0x28, 0xF1, 0x28, 0x28, 0x34, 0xF1, 0x28, 0x34, 0xE2, 0xBF, 0x43, 0xF5, 0x7F, 0x0B, 0x41, 0xE4, 0xE2, 0xD8, 0xF7, 0x2D, 0x38, 0x28, 0x41, 0xF1, 0x68, 0xE5, 0xA8, 0xF5, 0xE6, 0xE3, 0x68, 0xE6, 0xBF, 0xA6, 0xE2, 0x28, 0x42, 0x19, 0xE5, 0x97, 0x08, 0x46, 0x19, 0xF5, 0x68, 0xE0, 0xF7, 0x1C, 0xCF, 0xDC, 0x19, 0xF8, 0xF7, 0xFB, 0xF7, 0x53, 0xF7, 0xC1, 0x55, 0x53, 0x28, 0x52, 0x56, 0xF3, 0x28, 0x54, 0x54, 0x28, 0x08, 0x33, 0xE3, 0xBF, 0x32, 0xE3, 0xE3, 0xBF, 0xBB, 0x80, 0xF0, 0xF7, 0x66, 0xE3, 0xF0, 0xD8, 0x08, 0x28, 0xF7, 0x6C, 0xE3, 0xF1, 0xD8, 0x08, 0x28, 0xF7, 0x61, 0xE3, 0xF2, 0xD8, 0x08, 0x28, 0xF7, 0x67, 0xE3, 0xF3, 0xD8, 0x08, 0x28, 0xF7, 0x7B, 0xE3, 0xF4, 0xD8, 0x08, 0x28, 0xF7, 0x7D, 0xE3, 0xF7, 0x1C, 0xD8, 0x08, 0x28, 0x31, 0xF1, 0x53, 0x54, 0xE0, 0x57, 0x10, 0x28, 0xE0, 0x55, 0x53, 0x28, 0xF0, 0xF8, 0xF7, 0x32, 0xBF, 0x61, 0xF7, 0x30, 0xBF, 0x5D, 0xF7, 0x32, 0xBF, 0x59, 0xF7, 0x35, 0xBF, 0x55, 0xE3, 0x95, 0x96, 0x94, 0x95, 0x94, 0xBF, 0x4D, 0xF7, 0x35, 0xBF, 0x49, 0xF7, 0x32, 0xBF, 0x45, 0xF7, 0x70, 0xBF, 0x41, 0xF7, 0x6F, 0xBF, 0x3D, 0xF7, 0x6A, 0xBF, 0x39, 0xF7, 0x69, 0xBF, 0x35, 0xF7, 0x65, 0xBF, 0x31, 0xE3, 0x96, 0x94, 0x96, 0xBF, 0x2B, 0xF7, 0x61, 0xBF, 0x27, 0xF7, 0x66, 0xBF, 0x23, 0xF7, 0x64, 0xBF, 0x1F, 0xF7, 0x6D, 0xBF, 0x1B, 0xE3, 0x92, 0x96, 0xBF, 0x16, 0xF7, 0x32, 0xBF, 0x12, 0xF7, 0x30, 0xBF, 0x0E, 0xF7, 0x32, 0xBF, 0x0A, 0xF7, 0x35, 0xBF, 0x06, 0xE3, 0xBF, 0x03, 0x58, 0x28, 0x31, 0xF7, 0x20, 0xF7, 0x83, 0x57, 0x08, 0x28, 0xF7, 0xB8, 0xF7, 0xED, 0x57, 0x08, 0x28, 0x57, 0x10, 0x28, 0xF4, 0xF3, 0x68, 0xE4, 0xE4, 0xA8, 0x08, 0xE0, 0xF1, 0x48, 0x10, 0xE3, 0x48, 0x41, 0x91, 0x08, 0xE1, 0xF8, 0x42, 0xF0, 0xCF, 0xF1, 0x42, 0x1A, 0x32, 0x36, 0x6D, 0xB4, 0xB5, 0x11, 0x86, 0x2C, 0x24, 0xC0, 0x49, 0xB4, 0xBA, 0x1C, 0x09, 0x94, 0xF2, 0x24, 0x17, 0x17, 0xB9, 0xD3, 0x89, 0x2A, 0x05, 0xA2, 0xD6, 0x08, 0x9F, 0xF3, 0x90, 0xCB, 0xF3, 0x14, 0x4D, 0xA2, 0x9C, 0xFA, 0xB3, 0x0E, 0x9A, 0x82, 0x0F, 0x14, 0x63, 0x38, 0x5C, 0x94, 0xD4, 0x59, 0x0D, 0xB0, 0xCF, 0xC4, 0x8E, 0x23, 0x38, 0xBB, 0xB4, 0x68, 0x53, 0x09, 0xE7, 0x9B, 0x29, 0x8D, 0xD4, 0x36, 0x9D, 0x83, 0xB3, 0x55, 0xDA, 0xB5, 0xAB, 0xF7, 0xD8, 0x6E, 0xD1, 0xD9, 0xB4, 0xA8, 0x18, 0xBF, 0x58, 0xCC, 0x1E, 0x13, 0x38, 0x66, 0xFB, 0x95, 0xD1, 0x37, 0xC1, 0x78, 0x77, 0x59, 0x10, 0xF8, 0x5D, 0x44, 0xA7, 0xA8, 0xCD, 0x85, 0xBF, 0x01, 0xD7, 0xC3, 0xC2, 0x3B, 0x0C, 0x0A, 0x52, 0x15, 0xE2, 0x13, 0xE6, 0xD8, 0x05, 0x5E, 0x0E, 0x3E, 0x1F, 0xC3, 0x0A, 0xA6, 0xA5, 0xCD, 0xD6, 0xAE, 0x45, 0xEF, 0x2C, 0xCB, 0x05, 0x4D, 0xCC, 0xA3, 0x93, 0x91, 0xA7, 0xF0, 0x98, 0xB9, 0x02, 0x65, 0x95, 0xEB, 0x2C, 0x48, 0xC7, 0xFF, 0xF4, 0x6B, 0x2C, 0xA1, 0x5C, 0xB3, 0xDA, 0xE6, 0x99, 0xEB, 0xC7, 0x1E, 0x2A, 0xE9, 0x58, 0x06, 0x2A, 0x71, 0x14, 0xC3, 0xE8]
pc = 0
stack = [0,0x1E240,0x1000,0x2000]+[0]*0x1000
top = 3
mem = [0]*0x8000
mem[0x400:
0x408] = [0x67616C66, 0x3131317B, 0x322D3131, 0x32323232, 0x3333332D, 0x342D3333, 0x34343434,0x7d]
mem[0x80c:
0x80c+11] = [0x15100A09, 0x040C1321, 0x00001C11, 0x00000000, 0x200F0300, 0x0623020D, 0x010E141B, 0x12081916, 0x0B24171F, 0x051A071E, 0x00221D18]
while True:

    next_pc = pc+1
    op = opcodes[pc]>>3
    imm = opcodes[pc]&7
    print("pc=", hex(pc), hex(op), end="t")
    if imm == 7:
        imm = opcodes[next_pc]
        next_pc+=1
    if op in [0,12,14,17,20,29]:
        print("break 1")
    elif op == 1:
        print("xor stack[-1],stack[-2] -> stack[-2]")
    elif op == 2:
        print("neg stack[-1]")
    elif op == 3:
        print(f"pop top {imm=:x}")
    elif op == 4 or op == 26:
        print("nop")
    elif op == 5:
        print("or stack[-1],stack[-2] -> stack[-2]")
    elif op == 6:
        print(f"ret {imm=:x}")
        print()
    elif op == 7:
        print(f"cmpnz stack[-1],stack[-2] -> stack[-2]")
    elif op == 8:
        print(f"swap stack[top- {imm=:x}],stack[top]")
    elif op == 9:
        print(f"and stack[-1],stack[-2] -> stack[-2]")

    elif op == 10:
        print(f"shl stack[top],{imm=:x}")
    elif op == 11:
        print(f"not stack[top]")
    elif op == 13:
        print(f"add stack[-1],stack[-2] -> stack[-2]")
    elif op == 15:
        if imm&0x80!=0:
            imm = -(0x100-imm)
        print(f"jmp {next_pc+imm:x}")
    elif op == 16:
        print("break 0x101")
    elif op == 18:
        print(f"shr stack[top],{imm=}")
    elif op == 19:
        print(f"div stack[top-1],stack[top] -> stack[top-1]")
    elif op == 21:
        print(f"movzx stack[top]&0xff")
    elif op == 22:
        print(f"mul stack[top-1],stack[top] -> stack[top-1]")
    elif op == 23:
        if imm&0x80!=0:
            imm = -(0x100-imm)
        print(f"call {next_pc+imm:x}")
    elif op == 24 :
        if imm&0x80!=0:
            imm = -(0x100-imm)
        print(f"jz stack[top-1],stack[top] -> $+{imm=:x} {next_pc+imm:x}")
    elif op == 25:
        if imm&0x80!=0:
            imm = -(0x100-imm)
        print(f"jnz stack[top-1],stack[top] -> $+{imm=:x} {next_pc+imm:x}")

    elif op == 27:
        print(f"load mem[stack[top-1],stack[top]]")
    elif op == 28:

        print(f"push stack[top-{imm=}]")

    elif op == 30:
        print(f"push {imm=}")

    elif op == 31:
        print(f"dec stack[top]")

    pc = next_pc
复制代码 隐藏代码
pc= 0x0 0x17    call 81
pc= 0x2 0x10    break 0x101

for i in b"11111":
    sum*=36
    sum+=sbox[i]-1
pc= 0x3 0x1e    push imm=0
pc= 0x4 0x1e    push imm=0
pc= 0x5 0x1c    push stack[top-imm=0]
pc= 0x6 0x1c    push stack[top-imm=6]
pc= 0x7 0x18    jz stack[top-1],stack[top] -> $+imm=14 1d
pc= 0x9 0x8     swap stack[top- imm=1],stack[top]
pc= 0xa 0x1e    push imm=36
pc= 0xc 0x16    mul stack[top-1],stack[top] -> stack[top-1]
pc= 0xd 0x1c    push stack[top-imm=3]
pc= 0xe 0x1c    push stack[top-imm=5]
pc= 0xf 0x1c    push stack[top-imm=3]
pc= 0x10 0x1b   load mem[stack[top-1],stack[top]]
pc= 0x11 0x1b   load mem[stack[top-1],stack[top]] sbox
pc= 0x12 0x1c   push stack[top-imm=0]
pc= 0x13 0x1e   push imm=0
pc= 0x14 0x18   jz stack[top-1],stack[top] -> $+imm=25 3b
pc= 0x16 0xd    add stack[-1],stack[-2] -> stack[-2]
pc= 0x17 0x1f   dec stack[top]
pc= 0x18 0x8    swap stack[top- imm=1],stack[top]
pc= 0x19 0x1e   push imm=1
pc= 0x1a 0xd    add stack[-1],stack[-2] -> stack[-2]
pc= 0x1b 0xf    jmp 5
pc= 0x1d 0x3    pop top imm=1
pc= 0x1e 0x1c   push stack[top-imm=0]
pc= 0x1f 0x12   shr stack[top],imm=25
pc= 0x21 0x1e   push imm=0
pc= 0x22 0x18   jz stack[top-1],stack[top] -> $+imm=1c 40
pc= 0x24 0x1e   push imm=1
pc= 0x25 0xd    add stack[-1],stack[-2] -> stack[-2]
pc= 0x26 0x1c   push stack[top-imm=5]
pc= 0x27 0x1e   push imm=53
pc= 0x29 0x1e   push imm=218
pc= 0x2b 0x12   shr stack[top],imm=3
pc= 0x2c 0x12   shr stack[top],imm=4
pc= 0x2d 0xa    shl stack[top],imm=2
pc= 0x2e 0xa    shl stack[top],imm=6
pc= 0x2f 0x5    or stack[-1],stack[-2] -> stack[-2]
pc= 0x30 0xa    shl stack[top],imm=2
pc= 0x31 0xa    shl stack[top],imm=6
pc= 0x32 0x1e   push imm=65
pc= 0x34 0x5    or stack[-1],stack[-2] -> stack[-2]
pc= 0x35 0x16   mul stack[top-1],stack[top] -> stack[top-1]
pc= 0x36 0x1c   push stack[top-imm=4]
pc= 0x37 0x15   movzx stack[top]&0xff
pc= 0x38 0xd    add stack[-1],stack[-2] -> stack[-2]
pc= 0x39 0x13   div stack[top-1],stack[top] -> stack[top-1]
pc= 0x3a 0x6    ret imm=4

pc= 0x3b 0x5    or stack[-1],stack[-2] -> stack[-2]
pc= 0x3c 0x1e   push imm=1
pc= 0x3d 0x5    or stack[-1],stack[-2] -> stack[-2]
pc= 0x3e 0x5    or stack[-1],stack[-2] -> stack[-2]
pc= 0x3f 0x6    ret imm=4

pc= 0x40 0x1e   push imm=1
pc= 0x41 0x5    or stack[-1],stack[-2] -> stack[-2]
pc= 0x42 0x6    ret imm=4

pc= 0x43 0x1c   push stack[top-imm=2]
pc= 0x44 0x17   call 89
pc= 0x46 0x1e   push imm=5
pc= 0x47 0xf    jmp 54
pc= 0x49 0x8    swap stack[top- imm=1],stack[top]
pc= 0x4a 0x1c   push stack[top-imm=4]
pc= 0x4b 0x1c   push stack[top-imm=2]
pc= 0x4c 0x1b   load mem[stack[top-1],stack[top]]
pc= 0x4d 0x1e   push imm=45
pc= 0x4f 0x7    cmpnz stack[-1],stack[-2] -> stack[-2]
pc= 0x50 0x5    or stack[-1],stack[-2] -> stack[-2]
pc= 0x51 0x8    swap stack[top- imm=1],stack[top]
pc= 0x52 0x1e   push imm=1
pc= 0x53 0xd    add stack[-1],stack[-2] -> stack[-2]
pc= 0x54 0x1c   push stack[top-imm=5]
pc= 0x55 0x15   movzx stack[top]&0xff 8d90c3bd crc32
pc= 0x56 0x1e   push imm=5
pc= 0x57 0x1c   push stack[top-imm=6]
pc= 0x58 0x1c   push stack[top-imm=3]
pc= 0x59 0xd    add stack[-1],stack[-2] -> stack[-2]
pc= 0x5a 0x1c   push stack[top-imm=6]
pc= 0x5b 0x17   call 3
pc= 0x5d 0x1c   push stack[top-imm=2]
pc= 0x5e 0x5    or stack[-1],stack[-2] -> stack[-2]
pc= 0x5f 0x8    swap stack[top- imm=2],stack[top]
pc= 0x60 0x3    pop top imm=1
pc= 0x61 0x1c   push stack[top-imm=5]
pc= 0x62 0x12   shr stack[top],imm=8
pc= 0x64 0x8    swap stack[top- imm=6],stack[top]
pc= 0x65 0x3    pop top imm=1
pc= 0x66 0x1e   push imm=5
pc= 0x67 0xd    add stack[-1],stack[-2] -> stack[-2]
pc= 0x68 0x1c   push stack[top-imm=0]
pc= 0x69 0x1e   push imm=28
pc= 0x6b 0x19   jnz stack[top-1],stack[top] -> $+imm=-24 49
pc= 0x6d 0x3    pop top imm=1
pc= 0x6e 0x1f   dec stack[top]
pc= 0x6f 0x1e   push imm=251
pc= 0x71 0x1e   push imm=83
pc= 0x73 0x1e   push imm=193
pc= 0x75 0xa    shl stack[top],imm=5
pc= 0x76 0xa    shl stack[top],imm=3
pc= 0x77 0x5    or stack[-1],stack[-2] -> stack[-2]
pc= 0x78 0xa    shl stack[top],imm=2
pc= 0x79 0xa    shl stack[top],imm=6
pc= 0x7a 0x1e   push imm=3
pc= 0x7b 0x5    or stack[-1],stack[-2] -> stack[-2]
pc= 0x7c 0xa    shl stack[top],imm=4
pc= 0x7d 0xa    shl stack[top],imm=4
pc= 0x7e 0x5    or stack[-1],stack[-2] -> stack[-2]
pc= 0x7f 0x1    xor stack[-1],stack[-2] -> stack[-2]
pc= 0x80 0x6    ret imm=3

main
pc= 0x81 0x1c   push stack[top-imm=3]
pc= 0x82 0x17   call b6
crc32-> 8d90c3bd
pc= 0x84 0x1c   push stack[top-imm=3]
pc= 0x85 0x1c   push stack[top-imm=3]
pc= 0x86 0x17   call 43
pc= 0x88 0x10   break 0x101

检查flag{}
pc= 0x89 0x1e   push imm=0
pc= 0x8a 0x1e   push imm=102
pc= 0x8c 0x1c   push stack[top-imm=3]
pc= 0x8d 0x1e   push imm=0
pc= 0x8e 0x1b   load mem[stack[top-1],stack[top]]
pc= 0x8f 0x1    xor stack[-1],stack[-2] -> stack[-2]
pc= 0x90 0x5    or stack[-1],stack[-2] -> stack[-2]
pc= 0x91 0x1e   push imm=108
pc= 0x93 0x1c   push stack[top-imm=3]
pc= 0x94 0x1e   push imm=1
pc= 0x95 0x1b   load mem[stack[top-1],stack[top]]
pc= 0x96 0x1    xor stack[-1],stack[-2] -> stack[-2]
pc= 0x97 0x5    or stack[-1],stack[-2] -> stack[-2]
pc= 0x98 0x1e   push imm=97
pc= 0x9a 0x1c   push stack[top-imm=3]
pc= 0x9b 0x1e   push imm=2
pc= 0x9c 0x1b   load mem[stack[top-1],stack[top]]
pc= 0x9d 0x1    xor stack[-1],stack[-2] -> stack[-2]
pc= 0x9e 0x5    or stack[-1],stack[-2] -> stack[-2]
pc= 0x9f 0x1e   push imm=103
pc= 0xa1 0x1c   push stack[top-imm=3]
pc= 0xa2 0x1e   push imm=3
pc= 0xa3 0x1b   load mem[stack[top-1],stack[top]]
pc= 0xa4 0x1    xor stack[-1],stack[-2] -> stack[-2]
pc= 0xa5 0x5    or stack[-1],stack[-2] -> stack[-2]
pc= 0xa6 0x1e   push imm=123
pc= 0xa8 0x1c   push stack[top-imm=3]
pc= 0xa9 0x1e   push imm=4
pc= 0xaa 0x1b   load mem[stack[top-1],stack[top]]
pc= 0xab 0x1    xor stack[-1],stack[-2] -> stack[-2]
pc= 0xac 0x5    or stack[-1],stack[-2] -> stack[-2]
pc= 0xad 0x1e   push imm=125
pc= 0xaf 0x1c   push stack[top-imm=3]
pc= 0xb0 0x1e   push imm=28
pc= 0xb2 0x1b   load mem[stack[top-1],stack[top]]
pc= 0xb3 0x1    xor stack[-1],stack[-2] -> stack[-2]
pc= 0xb4 0x5    or stack[-1],stack[-2] -> stack[-2]
pc= 0xb5 0x6    ret imm=1

serial_crc32
pc= 0xb6 0x1e   push imm=1
pc= 0xb7 0xa    shl stack[top],imm=3
pc= 0xb8 0xa    shl stack[top],imm=4
pc= 0xb9 0x1c   push stack[top-imm=0]
pc= 0xba 0xa    shl stack[top],imm=10
pc= 0xbc 0x5    or stack[-1],stack[-2] -> stack[-2]
pc= 0xbd 0x1c   push stack[top-imm=0]
pc= 0xbe 0xa    shl stack[top],imm=5
pc= 0xbf 0xa    shl stack[top],imm=3
pc= 0xc0 0x5    or stack[-1],stack[-2] -> stack[-2]
pc= 0xc1 0x1e   push imm=0
pc= 0xc2 0x1f   dec stack[top]
pc= 0xc3 0x1e   push imm=50
pc= 0xc5 0x17   call 128
pc= 0xc7 0x1e   push imm=48
pc= 0xc9 0x17   call 128
pc= 0xcb 0x1e   push imm=50
pc= 0xcd 0x17   call 128
pc= 0xcf 0x1e   push imm=53
pc= 0xd1 0x17   call 128
pc= 0xd3 0x1c   push stack[top-imm=3]
pc= 0xd4 0x12   shr stack[top],imm=5
pc= 0xd5 0x12   shr stack[top],imm=6
pc= 0xd6 0x12   shr stack[top],imm=4
pc= 0xd7 0x12   shr stack[top],imm=5
pc= 0xd8 0x12   shr stack[top],imm=4
pc= 0xd9 0x17   call 128
pc= 0xdb 0x1e   push imm=53
pc= 0xdd 0x17   call 128
pc= 0xdf 0x1e   push imm=50
pc= 0xe1 0x17   call 128
pc= 0xe3 0x1e   push imm=112
pc= 0xe5 0x17   call 128
pc= 0xe7 0x1e   push imm=111
pc= 0xe9 0x17   call 128
pc= 0xeb 0x1e   push imm=106
pc= 0xed 0x17   call 128
pc= 0xef 0x1e   push imm=105
pc= 0xf1 0x17   call 128
pc= 0xf3 0x1e   push imm=101
pc= 0xf5 0x17   call 128
pc= 0xf7 0x1c   push stack[top-imm=3]
pc= 0xf8 0x12   shr stack[top],imm=6
pc= 0xf9 0x12   shr stack[top],imm=4
pc= 0xfa 0x12   shr stack[top],imm=6
pc= 0xfb 0x17   call 128
pc= 0xfd 0x1e   push imm=97
pc= 0xff 0x17   call 128
pc= 0x101 0x1e  push imm=102
pc= 0x103 0x17  call 128
pc= 0x105 0x1e  push imm=100
pc= 0x107 0x17  call 128
pc= 0x109 0x1e  push imm=109
pc= 0x10b 0x17  call 128
pc= 0x10d 0x1c  push stack[top-imm=3]
pc= 0x10e 0x12  shr stack[top],imm=2
pc= 0x10f 0x12  shr stack[top],imm=6
pc= 0x110 0x17  call 128
pc= 0x112 0x1e  push imm=50
pc= 0x114 0x17  call 128
pc= 0x116 0x1e  push imm=48
pc= 0x118 0x17  call 128
pc= 0x11a 0x1e  push imm=50
pc= 0x11c 0x17  call 128
pc= 0x11e 0x1e  push imm=53
pc= 0x120 0x17  call 128
pc= 0x122 0x1c  push stack[top-imm=3]
pc= 0x123 0x17  call 128
pc= 0x125 0xb   not stack[top]
pc= 0x126 0x5   or stack[-1],stack[-2] -> stack[-2]
pc= 0x127 0x6   ret imm=1

crc32
pc= 0x128 0x1e  push imm=32
pc= 0x12a 0x1e  push imm=131
pc= 0x12c 0xa   shl stack[top],imm=8
pc= 0x12e 0x5   or stack[-1],stack[-2] -> stack[-2]
pc= 0x12f 0x1e  push imm=184
pc= 0x131 0x1e  push imm=237
pc= 0x133 0xa   shl stack[top],imm=8
pc= 0x135 0x5   or stack[-1],stack[-2] -> stack[-2]
pc= 0x136 0xa   shl stack[top],imm=10
pc= 0x138 0x5   or stack[-1],stack[-2] -> stack[-2]
pc= 0x139 0x1e  push imm=4
pc= 0x13a 0x1e  push imm=3
pc= 0x13b 0xd   add stack[-1],stack[-2] -> stack[-2]
pc= 0x13c 0x1c  push stack[top-imm=4]
pc= 0x13d 0x1c  push stack[top-imm=4]
pc= 0x13e 0x15  movzx stack[top]&0xff
pc= 0x13f 0x1   xor stack[-1],stack[-2] -> stack[-2]
pc= 0x140 0x1c  push stack[top-imm=0]
pc= 0x141 0x1e  push imm=1
pc= 0x142 0x9   and stack[-1],stack[-2] -> stack[-2]
pc= 0x143 0x2   neg stack[-1]
pc= 0x144 0x1c  push stack[top-imm=3]
pc= 0x145 0x9   and stack[-1],stack[-2] -> stack[-2]
pc= 0x146 0x8   swap stack[top- imm=1],stack[top]
pc= 0x147 0x12  shr stack[top],imm=1
pc= 0x148 0x1   xor stack[-1],stack[-2] -> stack[-2]
pc= 0x149 0x1c  push stack[top-imm=1]
pc= 0x14a 0x1f  dec stack[top]
pc= 0x14b 0x8   swap stack[top- imm=2],stack[top]
pc= 0x14c 0x1e  push imm=0
pc= 0x14d 0x19  jnz stack[top-1],stack[top] -> $+imm=-f 140
pc= 0x14f 0x8   swap stack[top- imm=2],stack[top]
pc= 0x150 0x3   pop top imm=2
pc= 0x151 0x6   ret imm=2

pc= 0x152 0x6   ret imm=6

pc= 0x153 0xd   add stack[-1],stack[-2] -> stack[-2]
pc= 0x154 0x16  mul stack[top-1],stack[top] -> stack[top-1]
pc= 0x155 0x16  mul stack[top-1],stack[top] -> stack[top-1]
pc= 0x156 0x2   neg stack[-1]
pc= 0x157 0x10  break 0x101
pc= 0x158 0x5   or stack[-1],stack[-2] -> stack[-2]
pc= 0x159 0x4   nop
pc= 0x15a 0x18  jz stack[top-1],stack[top] -> $+imm=0 15b
pc= 0x15b 0x9   and stack[-1],stack[-2] -> stack[-2]
pc= 0x15c 0x16  mul stack[top-1],stack[top] -> stack[top-1]
pc= 0x15d 0x17  call 160
pc= 0x15e 0x3   pop top imm=4
pc= 0x15f 0x1   xor stack[-1],stack[-2] -> stack[-2]
pc= 0x160 0x12  shr stack[top],imm=4
pc= 0x161 0x1e  push imm=2
pc= 0x162 0x4   nop
pc= 0x163 0x2   neg stack[-1]
pc= 0x165 0x17  call 167
pc= 0x166 0x1a  nop
pc= 0x167 0x11  break 1
pc= 0x168 0x5   or stack[-1],stack[-2] -> stack[-2]
pc= 0x169 0x0   break 1
pc= 0x16a 0x14  break 1
pc= 0x16b 0x1a  nop
pc= 0x16c 0x1   xor stack[-1],stack[-2] -> stack[-2]
pc= 0x16d 0x13  div stack[top-1],stack[top] -> stack[top-1]
pc= 0x16f 0x12  shr stack[top],imm=0
pc= 0x170 0x19  jnz stack[top-1],stack[top] -> $+imm=3 174
pc= 0x171 0x1e  push imm=3
pc= 0x172 0x2   neg stack[-1]
pc= 0x173 0x9   and stack[-1],stack[-2] -> stack[-2]
pc= 0x174 0x14  break 1
pc= 0x175 0x13  div stack[top-1],stack[top] -> stack[top-1]
pc= 0x176 0x1f  dec stack[top]
pc= 0x177 0x16  mul stack[top-1],stack[top] -> stack[top-1]
pc= 0x178 0x1   xor stack[-1],stack[-2] -> stack[-2]
pc= 0x179 0x13  div stack[top-1],stack[top] -> stack[top-1]
pc= 0x17a 0x10  break 0x101
pc= 0x17b 0x1   xor stack[-1],stack[-2] -> stack[-2]
pc= 0x17d 0xc   break 1
pc= 0x17e 0x7   cmpnz stack[-1],stack[-2] -> stack[-2]
pc= 0x17f 0xb   not stack[top]
pc= 0x180 0x12  shr stack[top],imm=4
pc= 0x181 0x1a  nop
pc= 0x182 0xb   not stack[top]
pc= 0x183 0x1   xor stack[-1],stack[-2] -> stack[-2]
pc= 0x184 0x16  mul stack[top-1],stack[top] -> stack[top-1]
pc= 0x185 0x19  jnz stack[top-1],stack[top] -> $+imm=-3c 14b
pc= 0x187 0x11  break 1
pc= 0x188 0x4   nop
pc= 0x189 0x7   cmpnz stack[-1],stack[-2] -> stack[-2]
pc= 0x18a 0x17  call 18e
pc= 0x18b 0x16  mul stack[top-1],stack[top] -> stack[top-1]
pc= 0x18c 0xd   add stack[-1],stack[-2] -> stack[-2]
pc= 0x18d 0xa   shl stack[top],imm=3
pc= 0x18e 0x1   xor stack[-1],stack[-2] -> stack[-2]
pc= 0x18f 0x1c  push stack[top-imm=155]
pc= 0x191 0x5   or stack[-1],stack[-2] -> stack[-2]
pc= 0x192 0x11  break 1
pc= 0x193 0x1a  nop
pc= 0x194 0x6   ret imm=6

pc= 0x195 0x13  div stack[top-1],stack[top] -> stack[top-1]
pc= 0x196 0x10  break 0x101
pc= 0x197 0x16  mul stack[top-1],stack[top] -> stack[top-1]
pc= 0x198 0xa   shl stack[top],imm=5
pc= 0x199 0x1b  load mem[stack[top-1],stack[top]]
pc= 0x19a 0x16  mul stack[top-1],stack[top] -> stack[top-1]
pc= 0x19b 0x15  movzx stack[top]&0xff
pc= 0x19c 0x1e  push imm=216
pc= 0x19e 0xd   add stack[-1],stack[-2] -> stack[-2]
pc= 0x19f 0x1a  nop
pc= 0x1a0 0x1b  load mem[stack[top-1],stack[top]]
pc= 0x1a1 0x16  mul stack[top-1],stack[top] -> stack[top-1]
pc= 0x1a2 0x15  movzx stack[top]&0xff
pc= 0x1a3 0x3   pop top imm=0
pc= 0x1a4 0x17  call 1fe
pc= 0x1a6 0x19  jnz stack[top-1],stack[top] -> $+imm=4 1ab
pc= 0x1a7 0x3   pop top imm=6
pc= 0x1a8 0x2   neg stack[-1]
pc= 0x1a9 0x7   cmpnz stack[-1],stack[-2] -> stack[-2]
pc= 0x1aa 0xc   break 1
pc= 0x1ab 0x1f  dec stack[top]
pc= 0x1ac 0x12  shr stack[top],imm=5
pc= 0x1ad 0x1a  nop
pc= 0x1ae 0x6   ret imm=c1

pc= 0x1b0 0xf   jmp 1b1
pc= 0x1b1 0xe   break 1
pc= 0x1b3 0x2   neg stack[-1]
pc= 0x1b4 0x1f  dec stack[top]
pc= 0x1b5 0xb   not stack[top]
pc= 0x1b6 0x8   swap stack[top- imm=4],stack[top]
pc= 0x1b7 0x14  break 1
pc= 0x1b9 0x19  jnz stack[top-1],stack[top] -> $+imm=5 1bf
pc= 0x1ba 0x10  break 0x101
pc= 0x1bb 0x17  call 1be
pc= 0x1bd 0x1a  nop
pc= 0x1bf 0x18  jz stack[top-1],stack[top] -> $+imm=2 1c2
pc= 0x1c0 0x7   cmpnz stack[-1],stack[-2] -> stack[-2]
pc= 0x1c1 0x1   xor stack[-1],stack[-2] -> stack[-2]
pc= 0x1c2 0x1   xor stack[-1],stack[-2] -> stack[-2]
pc= 0x1c3 0xa   shl stack[top],imm=2
pc= 0x1c4 0x2   neg stack[-1]
pc= 0x1c5 0x1c  push stack[top-imm=2]
pc= 0x1c6 0x2   neg stack[-1]
pc= 0x1c7 0x1c  push stack[top-imm=6]
pc= 0x1c8 0x1b  load mem[stack[top-1],stack[top]]
pc= 0x1c9 0x0   break 1
pc= 0x1ca 0xb   not stack[top]
pc= 0x1cb 0x1   xor stack[-1],stack[-2] -> stack[-2]
pc= 0x1cc 0x7   cmpnz stack[-1],stack[-2] -> stack[-2]
pc= 0x1cd 0x3   pop top imm=c3
pc= 0x1cf 0x1   xor stack[-1],stack[-2] -> stack[-2]
pc= 0x1d0 0x14  break 1
pc= 0x1d1 0x14  break 1
pc= 0x1d2 0x19  jnz stack[top-1],stack[top] -> $+imm=5 1d8
pc= 0x1d3 0x1a  nop
pc= 0x1d4 0x15  movzx stack[top]&0xff
pc= 0x1d5 0x8   swap stack[top- imm=5],stack[top]
pc= 0x1d6 0x1d  break 1
pc= 0x1d8 0x19  jnz stack[top-1],stack[top] -> $+imm=3 1dc
pc= 0x1d9 0x0   break 1
pc= 0x1da 0x9   and stack[-1],stack[-2] -> stack[-2]
pc= 0x1db 0x19  jnz stack[top-1],stack[top] -> $+imm=4 1e0
pc= 0x1dc 0x14  break 1
pc= 0x1dd 0x12  shr stack[top],imm=3
pc= 0x1de 0x12  shr stack[top],imm=1
pc= 0x1df 0x14  break 1
pc= 0x1e1 0x13  div stack[top-1],stack[top] -> stack[top-1]
pc= 0x1e2 0x17  call 1e4
pc= 0x1e3 0x0   break 1
pc= 0x1e4 0xc   break 1
pc= 0x1e5 0x12  shr stack[top],imm=5
pc= 0x1e6 0x1d  break 1
pc= 0x1e7 0x5   or stack[-1],stack[-2] -> stack[-2]
pc= 0x1e8 0x9   and stack[-1],stack[-2] -> stack[-2]
pc= 0x1e9 0x18  jz stack[top-1],stack[top] -> $+imm=-1 1ea
pc= 0x1eb 0x1e  push imm=4
pc= 0x1ec 0xd   add stack[-1],stack[-2] -> stack[-2]
pc= 0x1ed 0x5   or stack[-1],stack[-2] -> stack[-2]
pc= 0x1ee 0x14  break 1
pc= 0x1ef 0xb   not stack[top]
pc= 0x1f0 0x16  mul stack[top-1],stack[top] -> stack[top-1]
pc= 0x1f1 0x1b  load mem[stack[top-1],stack[top]]
pc= 0x1f2 0x1c  push stack[top-imm=6]
pc= 0x1f3 0x13  div stack[top-1],stack[top] -> stack[top-1]
pc= 0x1f4 0x1d  break 1
pc= 0x1f5 0x18  jz stack[top-1],stack[top] -> $+imm=1e 215
pc= 0x1f7 0x5   or stack[-1],stack[-2] -> stack[-2]
pc= 0x1f8 0x1d  break 1
pc= 0x1f9 0xb   not stack[top]
pc= 0x1fa 0x0   break 1
pc= 0x1fb 0x5   or stack[-1],stack[-2] -> stack[-2]
pc= 0x1fc 0xe   break 1
pc= 0x1fd 0x2   neg stack[-1]
pc= 0x1fe 0x18  jz stack[top-1],stack[top] -> $+imm=3 202
pc= 0x1ff 0x1d  break 1
复制代码 隐藏代码
def crc32_2(data):
    crc = 0xFFFFFFFF  # 初始值
    for i in data:
        crc = crc ^ i
        for j in range(8):
            if crc & 0x00000001:
                crc = (crc >> 1) ^ 0xEDB88320  # 逆序后的多项式 0xEDB88320= reverse 0x04C11DB7
            else:
                crc = (crc >> 1)
            # print(hex(crc))
    return (crc ^ 0xFFFFFFFF) | 0x80808080  # 或者写成~crc&0xffffffff   结果异或值

print(bytes([50,48,50,53,53,50,112,111,106,105,101,97,102,100,109,50,48,50,53]))
print(bytes([102,108,97,103]))

sbox = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x09, 0x0A, 0x10, 0x15, 0x21, 0x13, 0x0C, 0x04, 0x11, 0x1C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x0F, 0x20, 0x0D, 0x02, 0x23, 0x06, 0x1B, 0x14, 0x0E, 0x01, 0x16, 0x19, 0x08, 0x12, 0x1F, 0x17, 0x24, 0x0B, 0x1E, 0x07, 0x1A, 0x05, 0x18, 0x1D, 0x22, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
sum = 0
for i in b"11111":
    sum*=36
    sum+=sbox[i]-1
    # print(hex(sum))
print(hex(sum))
sum=0
for i in b"22222":
    sum*=36
    sum+=sbox[i]-1
    # print(hex(sum))
print(hex(sum))

crc32_val = [0xbd,0xc3,0x90,0x8d]
flag_off = [5,11,17,23]
sum = 0
table = b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

for i in range(4):
    print(hex(0x13541*crc32_val[i] + flag_off[i]))
data = [0xe45102,
0xeb908e,
0xadf4a1,
0xaa54e4]
for i in range(4):
    s=chr(sbox.index(data[i]%36+1))+chr(sbox.index(data[i]//36%36+1))+chr(sbox.index(data[i]//36//36%36+1))+chr(sbox.index(data[i]//36//36//36%36+1))+chr(sbox.index(data[i]//36//36//36//36%36+1))
    s=s[::-1]
    print(s,end="-")
print()
for i in b"HHW8A-5JYKV-3JEV6-HLE09":
    print(i,end=",")
print()
for _ in range(4):
    for t1 in table:
        for t2 in table:
            for t3 in table:
                for t4 in table:
                    for t5 in table:
                        t = [t1,t2,t3,t4,t5]

                        sum = 0
                        for i in t:
                            sum*=36
                            sum+=sbox[i]-1
                        if (sum+1) % data[_] == 0 and sum>>25!=0:
                            print(bytes(t),_)
复制代码 隐藏代码
import ida_dbg
import idaapi
p = idaapi.get_qword(0x7FF7A5956AF8)
a = idaapi.get_qword(0x7FF7A5956B08)
ida_dbg.set_reg_val("r14",p)
ida_dbg.set_reg_val("r15",a)
复制代码 隐藏代码
import ida_dbg
import idaapi
py = ida_dbg.get_reg_val("rax")

px = ida_dbg.get_reg_val("rcx")
r12 = ida_dbg.get_reg_val("r12")
print(py,px,r12)
p = idaapi.get_qword(0x7FF7A5956AF8)
a = idaapi.get_qword(0x7FF7A5956B08)
print(f"{a=} {p=}")
import ida_dbg
import idaapi
rbp = ida_dbg.get_reg_val("rbp")
enc = idaapi.get_bytes(rbp+0x30,0x10)
print(enc)
t = 0
for i in range(16):
    for bf in range(1000000):
        temp = ((bf+(-10*py)-t)//px)&0xff
        if temp == enc[i]:
            print(str(bf).zfill(6),end='')
            break
    t+=0x27DA
print(str(a).zfill(6)+str(p).zfill(6))
复制代码 隐藏代码
__int64 __fastcall sub_7A09998454(__int64 a1, unsigned __int64 a2)
{
  __int64 v3; // x0
  __int64 v4; // x0
  __int64 v5; // x0

  v3 = reverse_bit(a2);
  v4 = des_enc(a1, v3);
  v5 = des_dec(a1 + 128, v4);
  return des_enc(a1 + 256, v5);
}
复制代码 隐藏代码
import re

# ========================================
# 一、子密钥生成
# (1) 初始置换 64->56
# 64位的种子密钥经过PC_1置换后，生成56位的密钥
# (2) 划分 56->(28,28)
# 经过初始置换后的56位密钥被均分成C0和D0两部分
# (3) 循环左移
# 第一轮，C0和D0根据移位次数表各自进行循环左移
# 得到C1和D1
# 每一轮的C和D值是由上一轮的C和D值循环左移得到的
# (4) 合并 (28,28)->56->48
# 左移后的两部分再次合并,通过一个选择压缩表(PC_2)
# 得到这一轮的子密钥
# (5)重复3、4操作,最终得到16个子密钥
# ========================================

# 置换选择表1(PC_1) 64->56
PC_1 = [57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4
        ]

# 选择压缩表2(PC_2) 56->48
PC_2 = [14, 17, 11, 24, 1, 5, 3, 28,
        15, 6, 21, 10, 23, 19, 12, 4,
        26, 8, 16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55, 30, 40,
        51, 45, 33, 48, 44, 49, 39, 56,
        34, 53, 46, 42, 50, 36, 29, 32
        ]

# 移位次数表
shift_num = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

def pc_1_change(bin_key):
    """初始置换

    64位的种子密钥经过PC_1置换后，生成56位的密钥
    """
    return [bin_key[i - 1] for i in PC_1]  # 列表形式

def shift_left(bin_key, num):
    """实现C和D的循环左移"""
    return bin_key[num:] + bin_key[:
num]

def pc_2_change(bin_key):
    """选择压缩

    56位的密钥经过PC_2压缩，生成48位子密钥
    """
    return ''.join([bin_key[i - 1] for i in PC_2])  # 列表转字符串

def get_subkey_list(bin_key):
    """生成16轮的加解子密钥"""
    subkey_list = []  # 存储16轮子密钥
    # 1. 初始置换 64->58
    temp = pc_1_change(bin_key)
    # 2. 循环左移
    for i in shift_num:
        temp[:28] = shift_left(temp[:28], i)  # C部分循环左移
        temp[28:] = shift_left(temp[28:], i)  # D部分循环左移
        subkey_list.append(pc_2_change(temp))  # 生成子密钥
    return subkey_list

# ========================================
# 二、DES加解密实现
# ========================================

# 初始置换表IP 64->64
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7
      ]

# 逆置换表_IP 64->64
_IP = [40, 8, 48, 16, 56, 24, 64, 32, 39,
       7, 47, 15, 55, 23, 63, 31, 38, 6,
       46, 14, 54, 22, 62, 30, 37, 5, 45,
       13, 53, 21, 61, 29, 36, 4, 44, 12,
       52, 20, 60, 28, 35, 3, 43, 11, 51,
       19, 59, 27, 34, 2, 42, 10, 50, 18,
       58, 26, 33, 1, 41, 9, 49, 17, 57, 25
       ]

# 扩展置换表E 32->48
E = [32, 1, 2, 3, 4, 5, 4, 5,
     6, 7, 8, 9, 8, 9, 10, 11,
     12, 13, 12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21, 20, 21,
     22, 23, 24, 25, 24, 25, 26, 27,
     28, 29, 28, 29, 30, 31, 32, 1
     ]

# S盒 48->32
S1 = [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
      0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
      4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
      15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13
      ]
S2 = [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
      3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
      0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
      13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9
      ]
S3 = [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
      13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
      13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
      1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12
      ]
S4 = [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
      13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
      10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
      3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14
      ]
S5 = [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
      14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
      4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
      11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3
      ]
S6 = [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
      10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
      9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
      4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13
      ]
S7 = [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
      13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
      1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
      6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12
      ]
S8 = [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
      1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
      7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
      2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11
      ]
S = [S1, S2, S3, S4, S5, S6, S7, S8]

# P盒
P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25
     ]

# encrypt
def ip_change(bin_text):
    """初始置换"""
    return [bin_text[i - 1] for i in IP]

def s_box(bin_result):
    """S盒替换"""
    int_result = []
    result = ''
    for i in range(8):
        # 二进制行号
        bin_row = bin_result[i][0] + bin_result[i][5]
        # 二进制列号
        bin_col = ''.join(bin_result[i][j] for j in range(1, 5))
        # 获取对应的十进制数
        int_result.append(S[i][16 * int(bin_row, base=2) + int(bin_col, base=2)])
        # 十进制转成二进制
        result += bin(int_result[-1])[2:].zfill(4)
    return result

def p_box(result):
    """P盒置换"""
    return ''.join(result[i - 1] for i in P)

def f(R, bin_key):
    """轮函数f()"""
    # 1.将R由32位扩展成48位
    R_ext = [R[i - 1] for i in E]
    # 2.与子密钥进行逐位异或
    bin_temp = [str(int(r) ^ int(k)) for r, k in zip(R_ext, bin_key)]
    # 6个字符为一组，共8组
    bin_result = [''.join(bin_temp[i:i + 6]) for i in range(0, len(bin_temp), 6)]
    # 3.S盒替换 48->32
    result = s_box(bin_result)
    # 4.P盒置换 32->32
    return p_box(result)

def _ip_change(bin_text):
    """进行IP-1逆置换"""
    return ''.join(bin_text[i - 1] for i in _IP)

def des_cipher(bin_text, bin_key, reverse_keys=False):
    """通用DES加密解密函数"""
    # 1. 初始置换IP
    bin_text = ip_change(bin_text)
    # 2. 分成左右两部分L、R
    L, R = bin_text[:32], bin_text[32:]
    # 3. 获得16轮子密钥
    subkey_list= bin_key
    # print(subkey_list)
    if reverse_keys:
        subkey_list = subkey_list[::-1]  # 解密时反转子密钥列表
    # 4. 进行16轮迭代
    for i in subkey_list:
        R_temp = R
        # 轮函数f()结果和L进行异或
        R = ''.join(str(int(r) ^ int(l)) for r, l in zip(f(R, i), L))
        L = R_temp
    # 5. 进行IP-1逆置换 64->64
    return _ip_change(R + L)  # 输出二进制字符串

# 使用示例
def str2bin(text):
    """字符串转二进制字符串"""
    return ''.join(bin(byte)[2:].zfill(8) for byte in text.encode())

def bin2str(bin_text):
    """二进制字符串转字符串"""
    # 1.将二进制字符串按8位分割，并转换为字节数组
    byte_array = bytearray(int(i, 2) for i in re.findall(r'.{8}', bin_text) if int(i, 2) != 0)
    # 2.将字节序列解码为字符串
    return byte_array.decode()

def is_valid_key(key):
    """检查密钥是否有效 64bit"""
    return len(key.encode()) == 8

def des_encrypt(plaintext, subkey):
    """DES加密"""
    subkey = [bin(i)[2:].zfill(48) for i in subkey]
    bin_group_64 = [bin(int(plaintext,16))[2:].zfill(64)]
    bin_ciphertext = ''
    # print(bin_group_64)
    for g in bin_group_64:
        bin_ciphertext += des_cipher(g, subkey)
    # 3.密文转为16进制输出
    bin_group_4 = re.findall(r'.{4}', bin_ciphertext)
    hex_ciphertext = ''
    for g in bin_group_4:
        hex_ciphertext += format(int(g, 2), 'x')
    return hex_ciphertext

def des_decrypt(hex_ciphertext, subkey):
    """DES解密"""
    # 1.16进制密文转为2进制字符串
    subkey = [bin(i)[2:].zfill(48) for i in subkey]
    bin_group_64 = [bin(int(hex_ciphertext,16))[2:].zfill(64)]
    bin_ciphertext = ''
    # print(bin_group_64)
    bin_deciphertext = ''
    for g in bin_group_64:
        bin_deciphertext += des_cipher(g, subkey, reverse_keys=True)
    # 3.将解密密文转为字符串输出
    return hex(int(bin_deciphertext,2))[2:].zfill(16)

if __name__ == '__main__':
    data = [0x7C1A8B2E957A3115, 0x4B43E13562FC5DE6, 0x8346103AE93F945D]
    data = [hex(i)[2:].zfill(16) for i in data]
    for d in data:
        subkey1 = [0x0000CA5903E19093, 0x00001F0223BBA3C8, 0x0000AB109C30D703, 0x00001C02CC5E2426, 0x0000125838EC69C8, 0x00008C296420F25B, 0x0000826E0DF79422, 0x00004937208C0F6A, 0x000073802C5555A0, 0x00008880B2C8086D, 0x0000B40A3EC2FA9C, 0x0000A632003117B9, 0x00000A1E749B1823, 0x0000CC7058466B34, 0x000006C7683129DC, 0x0000B68191C62655]
        subkey2 = [0x00006800535C4C1A, 0x0000197270809D34, 0x00008455C8C90EB0, 0x0000524345594A19, 0x000009D90113501C, 0x00000121EF8131A4, 0x0000B14481A02AA5, 0x0000510BA0720A97, 0x000022A868A2A106, 0x0000886C06A42786, 0x0000602F187C02C3, 0x000044B42156C04B, 0x0000C38C5206B548, 0x00006CE282A8B560, 0x000032950A68CE22, 0x0000821AC102D968]
        t1 = des_decrypt(d,subkey1)

        t1 = des_encrypt(t1,subkey2)

        t1 = des_decrypt(t1, subkey1)
        # print(t1)
        print(bytes.fromhex(hex(int(bin(int(t1,16))[2:].zfill(64)[::-1],2))[2:])[::-1].decode(),end='')
复制代码 隐藏代码
 WebAssembly.instantiateStreaming(fetch('get_verify_code.wasm')).then(({instance}) => {
            window.calc_flag10_uid_timestamp_resultbufptr_resultbuflen_return_resultlen = () => {
                const uid = 1915092;
                const startTime = Date.now();
                const memory = new Uint8Array(instance.exports.memory.buffer);
                const timestamp = Math.floor(Date.now() / 1000);
                const resultBufPtr = 0;
                const resultBufLen = 60;
                let result;
                const resultLen = instance.exports.calc_flag10_uid_timestamp_resultbufptr_resultbuflen_return_resultlen(uid,timestamp,resultBufPtr, resultBufLen,result, resultBufLen);
                const code = (new TextDecoder()).decode(memory.subarray(resultBufPtr, resultBufPtr + resultLen));
                console.log(`solved: ${code} ${(Date.now() - startTime) / 1000}s`);
                return code;
            };
        });
window.calc_flag10_uid_timestamp_resultbufptr_resultbuflen_return_resultlen()
复制代码 隐藏代码
curl -s -H 'Content-type: application/json' --data-raw '{"number":"29382023"}' 'https://api.upowerchain.com/apis/v1alpha1/block/get'
复制代码 隐藏代码
h = 0x2b391e5b80c2491d4a295269a153f02315ce6a50722d6ff4d54de6d50d33a504 #hash_code
for i in range(9981,11000):
    if h%i in range(9980,11000):
        print(i,h%i )
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/5-1739711055.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/6-1739711055.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/0-1739711055.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/3-1739711056.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/9-1739711056.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/1-1739711056.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/5-1739711057.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/6-1739711057.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/0-1739711059.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/02/10-1739711059.png)