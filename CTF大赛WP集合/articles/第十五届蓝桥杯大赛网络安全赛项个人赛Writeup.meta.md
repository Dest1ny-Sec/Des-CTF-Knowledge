---
title: 第十五届蓝桥杯大赛网络安全赛项个人赛Writeup
contest: 蓝桥杯网络安全
year: 2024
difficulty: medium
vuln_type: web_unknown
tags: [Web-robots.txt,Misc-流量包追踪,Crypto-RSA-yafu分解n,DWT-水印DWT+Arnold,Re-XXTEA,Re-RC4,Pwn-UAF,ECDSA同k攻击]
attack_chain: 爬虫协议: /robots.txt→3个disallow路径→找flag|packet: ctrl+F搜flag+追踪流+base64解码|缺失的数据: 压缩包密码pavilion爆破+DWT水印逆+Arnold逆变换|Theorem: yafu分解n(p,q差206)|欢乐时光: 魔改XXTEA rounds=(415/n)+114 delta=0x61C88647+key='79696755 67346f6c 69231231 5f674231'|rc4: key='gamelab@'+42字节密文RC4解密|ezheap: 0x202405菜单选项触发UAF+tcache满转fastbin+0x430堆叠+free_hook覆盖+system|signature: ECDSA同k攻击(hi., hello.同k)
key_payload: /robots.txt + 追踪流|pavilion (DWT+Arnold)|yafu factor(n=94581028682900113123648734937784634645486813867065294159875516514520556881461611966096883566806571691879115766917833117123695776131443081658364855087575006641022211136751071900710589699171982563753011439999297865781908255529833932820965169382130385236359802696280004495552191520878864368741633686036192501791)|XXTEA rounds=int((415/n)+114); delta=0x61C88647; key=[0x79696755, 0x67346f6c, 0x69231231, 0x674231]|RC4 key='gamelab@' + 42字节密文|sendlineafter("4.exit", str(0x202405)) → delete_item(p, 1) + delete_item(p, 0)|k = ((h1 - h2) * mod_inverse(s1 - s2, n)) % n, dA = (mod_inverse(r1, n) * (k * s1 - h1)) % n
one_liner: 第十五届蓝桥杯网络安全7题:robots.txt+流量包追踪+DWT水印+Arnold逆+yafu分解RSA(差206)+魔改XXTEA(rounds=(415/n)+114)+RC4(gamelab@)+UAF(tcache+fastbin+free_hook)+ECDSA同k攻击
lesson: 1) robots.txt:3个Disallow路径逐个访问找flag; 2) DWT+Arnold水印逆:pywt.wavedec2(db2, level=3) + deArnold; 3) RSA yafu分解:差206的两个P154因子直接被分解; 4) XXTEA rounds魔改:rounds=(415/n)+114; 5) RC4标准实现:KSA+PRGA生成器+XOR; 6) 菜单题UAF:sendlineafter("4.exit", str(0x202405))触发特殊选项; 7) ECDSA同k:k=(h1-h2)/mod_inverse(s1-s2,n); dA=(k*s1-h1)/r1 mod n
quality: high
---

## 备注

原文(https://www.ctfiot.com/176353.html)2024年蓝桥杯网络安全赛项,涵盖Web/Misc/Crypto/Re/Pwn全方向7题。

### 题目清单(7题)

1. **爬虫协议** — /robots.txt
2. **packet** — 流量包追踪
3. **缺失的数据** — DWT+Arnold水印逆
4. **Theorem** — yafu分解RSA
5. **欢乐时光** — 魔改XXTEA
6. **rc4** — 标准RC4
7. **ezheap** — UAF+tcache+free_hook
8. **signature** — ECDSA同k攻击

### 关键细节

**Theorem (RSA-yafu分解)**
- n=94581028682900113123648734937784634645486813867065294159875516514520556881461611966096883566806571691879115766917833117123695776131443081658364855087575006641022211136751071900710589699171982563753011439999297865781908255529833932820965169382130385236359802696280004495552191520878864368741633686036192501791
- P154=9725277820345294029015692786209306694836079927617586357442724339468673996231042839233529246844794558371350733017150605931603344334330882328076640690156923
- P154=9725277820345294029015692786209306694836079927617586357442724339468673996231042839233529246844794558371350733017150605931603344334330882328076640690156717
- 差206,yafu秒出

**欢乐时光 (XXTEA)**
- 魔改rounds=int((415/n)+114)
- delta=0x61C88647(标准XXTEA)
- key=[0x79696755, 0x67346f6c, 0x69231231, 0x5f674231]
- v=[0x480AC20C, 0xCE9037F2, 0x8C212018, 0x0E92A18D, 0xA4035274, 0x2473AAB1, 0xA9EFDB58, 0xA52CC5C8, 0xE432CB51, 0xD04E9223, 0x6FD07093]
- flag{efccf8f0-0c97-12ec-82e0-0c9d9242e335}

**rc4 (RC4)**
- key='gamelab@'
- 42字节密文hex

**ezheap (UAF)**
- sendlineafter("4.exit", str(0x202405)) 特殊菜单选项
- 11次add+特定free顺序触发UAF
- heap_base+0x2a0, libc_base-0x1ecbe0-0x400
- free_hook覆盖+system

**signature (ECDSA同k)**
- 椭圆曲线SECP256k1
- 同一k对b'Hi.'和b'hello.'签名
- k = (h1 - h2) * mod_inverse(s1 - s2, n) % n
- dA = mod_inverse(r1, n) * (k * s1 - h1) % n

## 评级

- **quality: high** — 8+题全方向,yafu分解差206素数+XXTEA魔改rounds+UAF+ECDSA同k全套,典型蓝桥杯高质WP
- **vuln_type: web_unknown** — 主分类Web;涉及sqli、rce、reverse、heap_exploit、crypto_rsa
- 实战价值:差值小的RSA可被yafu/GMP秒分解,ECDSA同k是经典私钥恢复攻击
