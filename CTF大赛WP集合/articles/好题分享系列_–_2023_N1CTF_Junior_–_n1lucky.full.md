---
title: 2023 N1CTF Junior n1lucky - LLL格密码恢复secret
contest: 2023 N1CTF Junior (Nu1L)
year: 2023
difficulty: hard
vuln_type: lattice
tags:
- Nu1L
- N1CTF
- LLL
- 格密码
- CRT中国剩余定理
- multi-prime
- 30-bit_prime
- 888-bit_prime
- 4096-bit_secret
- socketserver
- POW
- hashcash
attack_chain: 解决sha256(XXXX+proof[4:]) POW → 20次交互拿20对(r_i*secret mod p_i) → 因secret 4096-bit远大于p_i 888-bit需5组CRT合并 → 因r_i仅30-bit prime造LLL格(Delta=2^(4096+30)+CRT项+prodp) → LLL规约首行提取r_i → GCD验证r_0∩r_1=r_2*r_3*r_4
key_payload: LLL(6×6) + Delta=2^(4096+30) + CRT合并 + GCD校验
one_liner: Nu1L 30-bit r乘4096-bit secret模888-bit p,20次机会用5组CRT+LLL恢复secret。
lesson: 30-bit与4096-bit数量级悬殊 → 30-bit部分可视为"短向量"通过LLL格密码规约恢复;secret远大于p所以必须多组CRT合并;每组res_i*Pi[i]*Qi[i]填最后一列+Delta=2^(4096+30)在对角+prodp末行末列,LLL后首行除Delta得所有r_i;GCD交叉验证r_0∩r_1=r_2*r_3*...*r_{n-1}。
quality: high
full_path: 好题分享系列_–_2023_N1CTF_Junior_–_n1lucky.full.md
meta_path: 好题分享系列_–_2023_N1CTF_Junior_–_n1lucky.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: 2023 N1CTF Junior n1lucky - LLL格密码恢复secret。Nu1L 30-bit r乘4096-bit secret模888-bit p,20次机会用5组CRT+LLL恢复secret。。经验：30-bit与4096-bit数量级悬殊 → 30-bit部分可视为"短向量"通过LLL格密码规约恢复;secret...
category: crypto
subcategory: lattice
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/147007.html
reasoning_chain:
- 'Nu1L N1CTF 2023 Junior n1lucky, 解决 sha256(XXXX+proof[4:]) POW → 触发点: 4 字符暴力'
- '假设: 20 次交互拿 20 对 (r_i*secret mod p_i) → 动作: 发送 POW 答案 → 观察: 服务端返回 20 对'
- '因 secret 4096-bit 远大于 p_i 888-bit 需 5 组 CRT 合并 → 假设: 中国剩余定理 (CRT) 可恢复 secret mod prod(p_i) → 动作: CRT 合并'
- '因 r_i 仅 30-bit prime 造 LLL 格 (Delta=2^(4096+30)+CRT 项 + prodp) → 假设: LLL 规约可恢复短向量 r_i → 动作: Sage LLL'
- '观察: LLL 后首行除 Delta 得所有 r_i → 假设: GCD 验证 r_0∩r_1 = r_2*r_3*r_4 (交叉验证) → 动作: GCD'
- '动作: 拿到所有 r_i 和 secret mod prod(p_i) → 求 secret → 完成'
failed_attempts:
- '试图不组合 CRT 直接解 secret → 失败: secret 4096-bit 远大于单个 p_i 888-bit'
- '试图不恢复 r_i 直接 LLL → 失败: 矩阵维数不够'
key_observations:
- 30-bit 与 4096-bit 数量级悬殊 → 30-bit 部分可视为'短向量'通过 LLL 格密码规约恢复
- secret 远大于 p 所以必须多组 CRT 合并
- 每组 res_i*Pi[i]*Qi[i] 填最后一列 + Delta=2^(4096+30) 在对角 + prodp 末行末列
- LLL 后首行除 Delta 得所有 r_i
- GCD 交叉验证 r_0∩r_1 = r_2*r_3*...*r_{n-1}
prerequisites:
- LLL 格密码算法 (Sage LLL)
- 中国剩余定理 CRT
- POW 暴力 (sha256 前缀)
- socketserver 编程
---
# 好题分享系列 – 2023 N1CTF Junior – n1lucky

> 原文: https://www.ctfiot.com/147007.html
> ID: 147007

首先声明，这个系列所分享的“好题” 仅代表我个人在解这道题时可能觉得这道题某一个知识点很有趣；或是很新颖；或是出题人对这道题各个知识点的衔接处理的很好，而不是单纯套娃；或是看了出题人的题解觉得特别优雅，或是觉得自己的解法很妙…… 但并不保证这道题目的实时性、原创性，可能我看到这道题的时候它已经是被抄袭过的，但我并没有遇到过原题。 （题好，但不对比赛给予评价）另外为了避免纯粹的拿来主义，以给读者一定的思考、操作空间，这个系列也不会直接给出完整的解题 exp，大家自己也多试试叭！

今天这道题目来自 2023 N1CTF Junior – n1lucky

# !/usr/bin/env python3
import socketserver
import os
import signal
import string
import random
from hashlib import sha256
from Crypto.Util.number import *
from secret import flag

BANNER = br"""                                                                                                
::::    :::   :::  :::    :::  ::::::::  :::    ::: :::   ::: 
:+:+:   :+: :+:+:  :+:    :+: :+:    :+: :+:   :+:  :+:   :+: 
:+:+:+  +:+   +:+  +:+    +:+ +:+        +:+  +:+    +:+ +:+  
+#+ +:+ +#+   +#+  +#+    +:+ +#+        +#++:++      +#++:   
+#+  +#+#+#   +#+  +#+    +#+ +#+        +#+  +#+      +#+    
#+#   #+#+#   #+#  #+#    #+# #+#    #+# #+#   #+#     #+#    
###    #### ####### ########   ########  ###    ###    ###         
"""

MENU = br"""
1. guess
2. exit
"""

class Task(socketserver.BaseRequestHandler):
    def _recvall(self):
        BUFF_SIZE = 2048
        data = b''
        while True:
            part = self.request.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data.strip()

    def send(self, msg, newline=True):
        try:
            if newline:
                msg += b'n'
            self.request.sendall(msg)
        
except:
            pass

    def recv(self, prompt=b'[+] '):
        self.send(prompt, newline=False)
        return self._recvall()

    def recvint(self, prompt=b'> '):
        self.send(prompt, newline=False)
        try:
            data = int(self._recvall().decode('latin-1'))
        
except ValueError:
            self.send(b"Wrong type")
            self.close()
            return None
        return data

    def close(self):
        self.send(b"Bye~")
        self.request.close()

    def proof_of_work(self):
        random.seed(os.urandom(8))
        proof = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(20)])
        _hexdigest = sha256(proof.encode()).hexdigest()
        self.send(f"sha256(XXXX+{proof[4:]}) == {_hexdigest}".encode())
        x = self.recv(prompt=b'Give me XXXX: ')
        if len(x) != 4 or sha256(x + proof[4:].encode()).hexdigest() != _hexdigest:
            return False
        return True

    def handle(self):
        signal.alarm(120)

        if not self.proof_of_work():
            return

        self.send(BANNER)
        secret = random.getrandbits(4096)

        time = 0
        self.send("Nu1L's 🚩 are only for the lucky people~".encode())
        self.send("😊 Try to prove you're lucky enough!".encode())

        while time < 20:
            self.send(MENU, newline=False)
            choice = self.recv()
            time += 1

            if choice == b"1":
                p = getPrime(888)
                r = getPrime(30)
                res = r * secret % p
                self.send("n🎁 here : {}, {}n".format(res, p).encode())
                guess = self.recvint(prompt=b"Your guess > ")
                if guess == secret:
                    self.send("🎉 So lucky!!! Here is your flag: ".encode() + flag)
                    self.close()
                    break
                else:
                    self.send("👻 A little hapless".encode())
                continue

            self.close()
            break

        self.send("nn💀 No Chance!".encode())
        self.close()

class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class ForkedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 10000
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()

是用 socketserver 写的交互题，核心部分我们看到 handle 函数就好

def handle():
    secret = random.getrandbits(4096)
    time = 0
    #self.send("Nu1L's 🚩 are only for the lucky people~".encode())
    #self.send("😊 Try to prove you're lucky enough!".encode())

    while time < 20:
        #self.send(MENU, newline=False)
        choice = b"1"
        time += 1

        if choice == b"1":
            p = getPrime(888)
            r = getPrime(30)
            res = r * secret % p
            print("n🎁 here : {}, {}n".format(res, p).encode())
            guess = input(b"Your guess > ")
            if guess == secret:
                print("🎉 So lucky!!! Here is your flag: ".encode() + flag)
                #self.close()
                break
            else:
                print("👻 A little hapless".encode())
            continue

生成了一个 4096 比特的随机数 Secret ，随后最多能给出 20 对 ，需要我们恢复这个 Secret。其中
 是 888 比特的素数，而
 是一个只有 30 比特的素数。大小差异这么明显，造个格子是跑不了得到了。但是具体怎么造呢？思索了好久也没整出来，最终群友 @Tover. 给出了解决方案。

注意到这里的 Secret 是 4096 比特的，而模数

 只有 888 比特，那么显然中国剩余定理是跑不掉的，大概需要五组数据。假设我们已知

 ，于是我们有


```
# !/usr/bin/env python3
import socketserver
import os
import signal
import string
import random
from hashlib import sha256
from Crypto.Util.number import *
from secret import flag

BANNER = br"""                                                                                                
::::    :::   :::  :::    :::  ::::::::  :::    ::: :::   ::: 
:+:+:   :+: :+:+:  :+:    :+: :+:    :+: :+:   :+:  :+:   :+: 
:+:+:+  +:+   +:+  +:+    +:+ +:+        +:+  +:+    +:+ +:+  
+#+ +:+ +#+   +#+  +#+    +:+ +#+        +#++:++      +#++:   
+#+  +#+#+#   +#+  +#+    +#+ +#+        +#+  +#+      +#+    
#+#   #+#+#   #+#  #+#    #+# #+#    #+# #+#   #+#     #+#    
###    #### ####### ########   ########  ###    ###    ###         
"""

MENU = br"""
1. guess
2. exit
"""

class Task(socketserver.BaseRequestHandler):
    def _recvall(self):
        BUFF_SIZE = 2048
        data = b''
        while True:
            part = self.request.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data.strip()

    def send(self, msg, newline=True):
        try:
            if newline:
                msg += b'n'
            self.request.sendall(msg)
        
except:
            pass

    def recv(self, prompt=b'[+] '):
        self.send(prompt, newline=False)
        return self._recvall()

    def recvint(self, prompt=b'> '):
        self.send(prompt, newline=False)
        try:
            data = int(self._recvall().decode('latin-1'))
        
except ValueError:
            self.send(b"Wrong type")
            self.close()
            return None
        return data

    def close(self):
        self.send(b"Bye~")
        self.request.close()

    def proof_of_work(self):
        random.seed(os.urandom(8))
        proof = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(20)])
        _hexdigest = sha256(proof.encode()).hexdigest()
        self.send(f"sha256(XXXX+{proof[4:]}) == {_hexdigest}".encode())
        x = self.recv(prompt=b'Give me XXXX: ')
        if len(x) != 4 or sha256(x + proof[4:].encode()).hexdigest() != _hexdigest:
            return False
        return True

    def handle(self):
        signal.alarm(120)

        if not self.proof_of_work():
            return

        self.send(BANNER)
        secret = random.getrandbits(4096)

        time = 0
        self.send("Nu1L's 🚩 are only for the lucky people~".encode())
        self.send("😊 Try to prove you're lucky enough!".encode())

        while time < 20:
            self.send(MENU, newline=False)
            choice = self.recv()
            time += 1

            if choice == b"1":
                p = getPrime(888)
                r = getPrime(30)
                res = r * secret % p
                self.send("n🎁 here : {}, {}n".format(res, p).encode())
                guess = self.recvint(prompt=b"Your guess > ")
                if guess == secret:
                    self.send("🎉 So lucky!!! Here is your flag: ".encode() + flag)
                    self.close()
                    break
                else:
                    self.send("👻 A little hapless".encode())
                continue

            self.close()
            break

        self.send("nn💀 No Chance!".encode())
        self.close()

class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class ForkedServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = '0.0.0.0', 10000
    server = ForkedServer((HOST, PORT), Task)
    server.allow_reuse_address = True
    server.serve_forever()
def handle():
    secret = random.getrandbits(4096)
    time = 0
    #self.send("Nu1L's 🚩 are only for the lucky people~".encode())
    #self.send("😊 Try to prove you're lucky enough!".encode())

    while time < 20:
        #self.send(MENU, newline=False)
        choice = b"1"
        time += 1

        if choice == b"1":
            p = getPrime(888)
            r = getPrime(30)
            res = r * secret % p
            print("n🎁 here : {}, {}n".format(res, p).encode())
            guess = input(b"Your guess > ")
            if guess == secret:
                print("🎉 So lucky!!! Here is your flag: ".encode() + flag)
                #self.close()
                break
            else:
                print("👻 A little hapless".encode())
            continue
from Crypto.Util.number import *
import random
# 生成数据
R = []
P = []
Res = []

secret = random.getrandbits(4096)
for i in range(5):
    r = getPrime(30)
    p = getPrime(888)
    res = r * secret % p
    R.append(r)
    P.append(p)
    Res.append(res)

# poc

prodp = 1
for i in P:
    prodp *= i

Pi = []
for i in P:
    Pi.append(prodp//i)

Qi = []
for i in range(5):
    Qi.append(inverse(Pi[i],P[i]))

Delta = 2^(4096+30)
M = matrix(ZZ,[[Delta,0,0,0,0,Res[0]*Pi[0]*Qi[0]],
               [0,Delta,0,0,0,Res[1]*Pi[1]*Qi[1]],
               [0,0,Delta,0,0,Res[2]*Pi[2]*Qi[2]],
               [0,0,0,Delta,0,Res[3]*Pi[3]*Qi[3]],
               [0,0,0,0,Delta,Res[4]*Pi[4]*Qi[4]],
               [0,0,0,0,0,                 prodp]])
L = M.LLL()

Ri = list((L[0]/Delta)[:5])

Ri = [abs(i) for i in Ri]

assert GCD(Ri[0],Ri[1]) == R[2]*R[3]*R[4]
from Crypto.Util.number import *
import random
# 生成数据
R = []
P = []
Res = []
rounds = 10
secret = random.getrandbits(4096)
for i in range(rounds):
    r = getPrime(30)
    p = getPrime(888)
    res = r * secret % p
    R.append(r)
    P.append(p)
    Res.append(res)

# poc

prodp = 1
for i in P:
    prodp *= i

Pi = []
for i in P:
    Pi.append(prodp//i)

Qi = []
for i in range(rounds):
    Qi.append(inverse(Pi[i],P[i]))

Delta = 2^(4096+30*(rounds-1))

ML = []
for i in range(rounds):
    T = [0] * (rounds+1)
    T[i] = Delta
    T[-1] = Res[i]*Pi[i]*Qi[i]
    ML.append(T)

T = [0] * (rounds+1)
T[-1] = prodp
ML.append(T)

M = matrix(ZZ,ML)

L = M.LLL()

Ri = list((L[0]/Delta)[:
rounds])

Ri = [abs(i) for i in Ri]

#  R0 和 R1 的最大公因子是 r2*r3*r3*....

check = 1

for i in range(2,rounds):
    check*=R[i]

assert GCD(Ri[0],Ri[1]) == check
```
