---
title: 香港網安奪旗賽HKCERT CTF 2024 Write up（下）
contest: HKCERT CTF 2024
year: 2024
difficulty: hard
vuln_type: misc_unknown
tags: [RSA-LCG, multiprime-rsa, pty-disassembly, Proxy-handler, XOR-stream, jsc-pyc, z3-constraint, pyc-decompile, SMT, weak-encryption]
attack_chain:
- 多线程爆破RSA-LCG seed: bits=128 LCG (a,c已知) 生成4个1024位素数p0-p3做multiprime RSA
- 第二阶段用nth_root(4, all=True)求S0初始种子+反推LCG恢复p0
- ISA 101 PTY空白字符IFS Proxy隐写通过Proxy has trap触发eval
- 数组映射XOR: array+array2置换+array3^num→去除x01→还原字节
- 未知加密算法用z3约束3个未知数(s0+s1+s2=300, 2s0+s1+2s2=496, s0+3s1+s2=508)
- sser.pyc反编译识别AES-CFB + sha256(nonce+pw)做key+IV
key_payload: hkcert24{c0mpu71n9_subs3qu3nc3s_0f_g30m3tr1c_s3qu3nc3s_1s_fun}
one_liner: HKCERT 2024下篇涵盖RSA-LCG多线程爆破+几何序列求根+Proxy隐写+数组置换+未知加密z3约束+pyc反编译,密码学综合难度顶级。
lesson: LCG生成RSA素数时,若bits小且seed少,可用nth_root或暴力搜索重建;未知加密不要硬逆,先列方程组用SMT求解;pyc反编译在CTF中是必备技能(使用pycdc/pylingual)。
quality: high
---

## 题目列表

Crypto(2): RSA LCG (0)(1)
Reverse(7): 虛空 / 再一個破解挑戰 / 嬰兒梳打餅 / Cyp.ress / 旗幟檢查機 / ISA 101 / 炒埋一碟 / bashed!
Pwn(2): 旗幟雜湊 / ChatGGT (1)

## 关键考点

### RSA LCG (0) 多线程seed爆破
- LCG bits=128, a=181525535962623036141846439269075744717, c=115518761677956575882056543847720910703
- 每次调用next()生成128位,4次拼接成1024位p,要求bit_length()==1024 + is_prime
- n=p0*p1*p2*p3是multiprime RSA
- 多进程pool.map(func, pars)按seed范围(0-65536)分16片爆破
- 命中seed=58727后重放LCG生成全部p

### RSA LCG (1) nth_root反推seed
- LCG bits=256, c=0, a=102197201962123846389438942955101245465045811321520032783251514372432272871077
- 已知n和a,反推S0;因c=0,S4 = a^4 * S0 (mod 2^bits)
- S0^4 = S4 (mod 2^256), 用Zmod(2^256)(S4).nth_root(4, all=True)求所有4次根
- 对每个候选S0重建LCG,生成p0,验证n%p0==0
- 命中后p0已知,因c=0且a公开,c^e mod p0 = c mod p0直接得m
- flag: `hkcert24{c0mpu71n9_subs3qu3nc3s_0f_g30m3tr1c_s3qu3nc3s_1s_fun}`

### ISA 101 PTY 空白字符 Proxy隐写
- flag藏在with (ㅤ``) (一片空白)块里
- function u3164()用Proxy has trap:`{has:(t,n)=>(p.push(n.length-1),2==p.length&&(p[0]||p[1]||eval(f),f+=String.fromCharCode(p[0]<<4|p[1]),p=[]),!0)}`
- Proxy的has trap读取属性名长度编码,2次属性访问凑出1字节
- 输入array3[i] ^= num + 长度拼接 + dict置换得明文

### Cyp.ress jsc字节码反编译
- .cpython-312.pyc文件,用pylingual在线反编译
- 识别AES-CFB + sha256(b'pow/'+nonce)做key/IV+pow工作量证明
- 客户端AES-encrypt后POST回服务端验证

### 旗幟檢查机 z3约束未知加密
- 三个未知数s0/s1/s2范围32-127 (排除特定字符)
- 三个线性方程:s0+s1+s2=300, 2s0+s1+2s2=496, s0+3s1+s2=508
- z3 solver.check()==sat,model()解出三个数+补1}闭合
- Solver迭代找到全部解

### ChatGGT (1) Pwn
- (未给出细节,见同源WP)

## 实战价值
- LCG+RSA攻击矩阵:已知a反推S0用nth_root,已知c暴力seed
- Proxy has trap是JS隐写高阶技术
- pyc反编译在2024-2025 CTF出现频率增加,推荐工具:pylingual web / pycdc
- z3对未知加密是首选
