# 好题分享系列 – 2023 香山杯 – strange_hash

> 原文: https://www.ctfiot.com/140286.html
> ID: 140286

首先声明，这个系列所分享的“好题” 仅代表我个人在解这道题时可能觉得这道题某一个知识点很有趣；或是很新颖；或是出题人对这道题各个知识点的衔接处理的很好，而不是单纯套娃；或是看了出题人的题解觉得特别优雅，或是觉得自己的解法很妙…… 但并不保证这道题目的实时性、原创性，可能我看到这道题的时候它已经是被抄袭过的，但我并没有遇到过原题。 （题好，但不对比赛给予评价）另外为了避免纯粹的拿来主义，以给读者一定的思考、操作空间，这个系列也不会直接给出完整的解题 exp，大家自己也多试试叭！

今天这道题目来自 2023 香山杯 – strange_hash

是一道交互型题目，用的 socketserver 写法，所以代码显得很长，实际题目关键函数在于 Rescue_Prime

理论上我们需要输入一个三元数组 input，并且满足最后一个元素是 0，然后在经过 Rescue_Prime 函数一通操作后得到输出 output，且最后一个元素也是 0。

题目的原型来自于今年 第八届（2023年）全国高校密码数学挑战赛 赛道一：有限域密码原语CICO问题

可以在 github 找到相关题目介绍和附件：https://github.com/ismdeep/cmsecc-problems/tree/main/2023/problem-01

挑战的难度系数在于解决不同轮次
 下的

 问题，这道题目是取得是最简单的

 的情况。

最开始的想法是，把输入用两个变量

 和一个常量 0  进行表示，然后带入 Rescue_Prime 后会输出一个关于

 的多项式向量，然后我找到结果中第三个元素（多项式）的解就行了。自己解当然是不会解的了，想的是 sagemath 自带的 root 函数能够给出我一个解，但是经过一顿操作后，发现最后得到的式子奇长无比，sagemath表示自己也无能为力。然后就剩我懵逼在那了。

后来再看看他具体的操作，无非就是向量加法，矩阵乘法，对向量进行的幂次运算，由于模数是素数，也可以求逆弄回来。所以我们可以直接定死一个输出，然后从尾巴往上逆回去看看输入就行了。原来是加的，就减；原来是乘的，就除（乘以逆）；原来是幂次的，也幂次，不是幂的是原来次数在

 下的逆，这里题目直接给了。

最终大概代码长这样（非常的粗鄙）

这样能搞到一个输入 [1340156074189456211, 16362045171765893968, 18169133141834315644]

但是，输入的第三个元素不是 0 啊？这咋操作呢？继续懵逼。

赛后 @沛公 一语惊醒梦中人，输入检查的不是第三个元素，而是最后一个元素。。所以直接再加一个元素 0 就可以通过输入的 check 了，而这个 0 在第一次向量加法的时候就会被抛掉，不会影响后面的运算。

可是，，这应该是非预期叭，那么预期解该怎么做呢？希望有参加了今年 全国高校密码数学挑战赛赛道一 的大佬能指教一下子 Orz。


```
from os import urandom
import socketserver
from Crypto.Util.number import *
import random
from hashlib import sha256
import string
from secret import flag

p = 18446744073709551557
M = [[8, 56, 280], [18446744073709551543, 18446744073709551467, 18446744073709551123], [7, 35, 155]]
ConInv = [0x39a3f978106bac2d,0x2940e055f4a33725,0xfda9a7a293fb5bc9]
Con = [[0x9c52c2de7a9373c4,0xf2135cb886d0fa21,0x957df7f3cd4879e9], [0xd54f837d2738d717,0x400ddf1ffaae436d,0xc2abb601d9a26b07], [0x1904359f1deb3495,0xc21aa09ba52b157b,0x3d45525db1b19a0c], [0xed66cf26a65afc73,0x1cee569b29ffa476,0x3da45abf4304849], [0x1c1a642fa0f3d96d,0x59a1c4fbb96aec86,0xa18e9ca93163f63d], [0x9621ec9fbcb402be,0xd69468353c31bee0,0x50655b3f20fee3b8], [0x109cde7a61c2c195,0x5ebbd9e98be60c59,0x334d2d15f6e43190], [0x47af2b0d63901977,0x67ace097bf8c6f34,0xb87da3296b70d64b], [0x52d6344b38f49899,0xad5773add31420e1,0xecd0b7480f8c8095], [0xe2afb6d20f5decda,0xb1767d8be7d1371,0x902fd6806a0ef4db]]
assert len(Con) == 10
Inv = inverse(3, p-1)
Round = 2

def add(x, y):
    return [(a + b)%p for a, b in zip(x, y)]

def multiply(x, M):
    result = []
    for i in range(len(M[0])):
        temp = 0
        for j in range(len(x)):
            temp += x[j] * M[j][i]
        result.append(temp%p)
    return result

def Rescue_Prime(R, P):
    X = add(P, ConInv)
    Y = [0, 0, 0]
    Z = [0, 0, 0]
    U = [0, 0, 0]
    for r in range(R):
        for i in range(3):
            Y[i] = pow(X[i], 3, p)
            
        Z = add(Con[2*r%10], multiply(Y, M))
        
        for i in range(3):
            U[i] = pow(Z[i], Inv, p)

        X = add(Con[(2*r+1)%10], multiply(U, M))
    return X

class Task(socketserver.BaseRequestHandler):
    encrypt_history = []

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    def proof_of_work(self):
        random.seed(urandom(8))
        proof = ''.join([
            random.choice(string.ascii_letters + string.digits)
            for _ in range(20)
        ])
        digest = sha256(proof.encode()).hexdigest()
        self.send_line(
            str.encode(("sha256(XXXX + %s) == %s" % (proof[4:], digest))))
        self.send_line(str.encode('Give me XXXX:'))
        x = self.request.recv(10)
        x = (x.strip()).decode("utf-8")
        if len(x) != 4 or sha256(
                (x + proof[4:]).encode()).hexdigest() != digest:
            return False
        return True

    def send_line(self, msg):
        try:
            self.request.sendall(msg + b'n')
        
except:
            pass

    def read_line(self):
        body = b""
        while True:
            ch = self.request.recv(1)
            if ch == b"n":
                break
            body = body + ch
        return body

    def timeout_handler(self, signum, frame):
        raise TimeoutError

    def handle(self):
        try:
            if not self.proof_of_work():
                self.dosend(b'You must pass the PoW!')
                self.request.close()
            self.send_line(b'Send your input:')
            input_str = self.read_line().decode()
            num_tuple = tuple(map(int, input_str.strip('()').split(',')))  
            if num_tuple[-1] != 0:
                self.send_line(b'The third number is not zero!')
                self.request.close()
            output = Rescue_Prime(Round, num_tuple)
            if output[-1] == 0:
                self.send_line(b'congratulate! Here is the flag:')
                self.send_line(flag)
            else:
                self.send_line(b'Oops! Find collision failed.')
                self.request.close()
        
except:
            self.send_line(b'What's wrong???')
            self.request.close()

class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

HOST, PORT = '0.0.0.0', 9999
server = ThreadedServer((HOST, PORT), Task)
server.allow_reuse_address = True
server.serve_forever()
ConInv = matrix(Zmod(p),ConInv)
Con = matrix(Zmod(p),Con)
M = matrix(Zmod(p),M)
output = vector(Zmod(p),[1, 1, 0])

tmp = output - Con[3]
tmp = tmp * M^-1
tmp = tmp * diagonal_matrix(tmp)^2
tmp = tmp - Con[2]
tmp = tmp * M^-1
tmp = tmp * diagonal_matrix(tmp)^(Inv-1)
tmp = tmp - Con[1]
tmp = tmp * M^-1
tmp = tmp * diagonal_matrix(tmp)^2
tmp = tmp - Con[0]
tmp = tmp * M^-1
tmp = tmp * diagonal_matrix(tmp)^(Inv-1)
input = tmp - ConInv[0]
```
