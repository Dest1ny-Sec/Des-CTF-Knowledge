# 解析2025强网杯ezran

> 原文: https://www.ctfiot.com/275603.html
> ID: 275603

ezran – MT19937随机数生成器状态恢复攻击

一、题目概述

本题是一道经典的密码学题目，涉及到MT19937伪随机数生成器（PRNG）的状态恢复攻击。题目通过Python的random模块生成随机数，并使用这些随机数对flag进行了加密和混淆。我们的目标是通过分析题目给出的输出数据，逆向还原随机数生成器的内部状态，从而解密出原始的flag。

涉及知识点：

MT19937伪随机数生成器原理

线性方程组求解（GF(2)域）

逆向随机数状态恢复

Python shuffle算法逆向

循环3108次，每次生成两个随机数：

r1: 8位随机数

r2: 16位随机数

计算 x = (pow(r1, 2*i, 257) & 0xff) ^ r2

pow(r1, 2*i, 257) 是计算 r1^(2i) mod 257

& 0xff 取结果的低8位

^ r2 与16位随机数r2进行异或

将结果x转换为2字节并追加到gift

每次循环产生2个字节的输出

总共产生 3108 × 2 = 6216 字节

这些数据包含了随机数生成器的输出信息

将flag转换为字符列表

使用Python的shuffle()函数打乱2025次

shuffle()内部使用同一个随机数生成器

x 的值是通过 (pow(r1, 2*i, 257) & 0xff) ^ r2 计算得到的

pow(r1, 2*i, 257) & 0xff 只保留低8位，结果范围是 0-255

r2 是16位随机数，范围是 0-65535

两者异或后，x 的值范围是 0-65535（16位）

但是 long_to_bytes(x, 2) 会将 x 转换为2字节的大端序表示

内部状态： 624个32位整数（共19968位）

确定性： 相同的内部状态会产生相同的随机数序列

可逆性： 如果知道足够多的输出，可以反推内部状态

提取约束信息：从gift中提取出能够约束MT19937状态的信息

恢复随机数状态：使用线性代数方法求解MT19937的内部状态

逆向还原flag：使用恢复的状态重新生成随机数序列，逆向shuffle操作

维护一个624个32位整数的状态数组

每次生成随机数时，对状态进行线性变换

输出经过”tempering”（调质）变换后的值

创建线性系统：

lin = LinearSystem([32] * 624)
mt = lin.gens()

创建624个32位的符号变量，代表MT19937的内部状态。

构建约束条件：

for o in out:
    rng.getrandbits(8)
    zeros.append(rng.getrandbits(bs) >> 8 ^ int(o))

由于我们观测到的是 r2 >> 8 的值，这个约束条件表达的是：

(r2 >> 8) ^ observed = (pow(r1, 2*i, 257) & 0xff)

但实际上由于 pow(r1, 2*i, 257) & 0xff 的不确定性，这里建立的约束是：

(r2 >> 8) ^ observed = 某个0-255的值

rng.getrandbits(8) 模拟题目中的 r1 = getrandbits(8)

rng.getrandbits(bs) 模拟题目中的 r2 = getrandbits(16)

>> 8 取高8位

^ int(o) 与观测值异或

添加初始状态约束：

zeros.append(mt[0] ^ int(0x80000000))

MT19937的第一个状态值的最高位通常为1，这是一个额外的约束。

求解线性方程组：

for sol in lin.solve_all(zeros):

使用高斯消元法求解GF(2)上的线性方程组，可能有多个解。

从后向前遍历数组

每次随机选择一个位置j（0 ≤ j ≤ i）

交换位置i和位置j的元素

第一次交换位置2和0：[C, B, A, D]

第二次交换位置3和1：[C, D, A, B]

先撤销第二次交换（位置3和1）：[C, B, A, D]

再撤销第一次交换（位置2和0）：[A, B, C, D]

MT19937伪随机数生成器

内部状态：624个32位整数

线性运算特性：在GF(2)域上是线性的

可预测性：知道足够输出可以恢复状态

信息泄露漏洞

x 和 r2 的高8位相同

通过 long_to_bytes(x, 2) 可以提取这个信息

3108个样本提供了足够的约束条件

线性代数攻击

将MT19937状态恢复转化为GF(2)上的线性方程组

使用高斯消元法求解

gf2bv库自动化了这个过程

Fisher-Yates洗牌算法

确定性算法：相同随机数序列产生相同结果

可逆性：知道随机数序列可以逆向还原

数据提取

g = [gift[2 * i:2 * i + 2][0] for i in range(len(gift) // 2)]

准确提取每个 x 的高8位。

状态验证

if gg == gift:
    flag = ins(c, rng)

由于可能有多个解，需要验证哪个是正确的。

逆向交换

for i, j in reversed(sw):
    a[i], a[j] = a[j], a[i]

逆序应用交换操作还原原始序列。

PRNG Cracking: 经典的MT19937状态恢复题目

PRNG Prediction: 预测下一个随机数

Shuffle Cryptanalysis: 基于shuffle的密码分析

MT19937算法详解

论文：Makoto Matsumoto and Takuji Nishimura (1998). “Mersenne Twister: A 623-Dimensionally Equidistributed Uniform Pseudo-Random Number Generator”

gf2bv库文档

GitHub: https://github.com/orisano/gf2bv

Fisher-Yates洗牌算法

时间复杂度：O(n)

空间复杂度：O(1)

保证每个排列的概率相等

尝试修改题目参数（如循环次数、shuffle次数）

实现其他PRNG的状态恢复攻击

研究真随机数生成器（TRNG）和PRNG的区别


```
from Crypto.Util.number import *
from random import *

f = open('flag.txt', 'r')
flag = f.read().encode()

# 第一部分：生成 gift 序列
gift = b''
for i in range(3108):
    r1 = getrandbits(8)   # 生成8位随机数
    r2 = getrandbits(16)  # 生成16位随机数
    x = (pow(r1, 2*i, 257) & 0xff) ^ r2
    c = long_to_bytes(x, 2)
    gift += c

# 第二部分：对 flag 进行 shuffle 混淆
m = list(flag)
for i in range(2025):
    shuffle(m)

c = "".join(list(map(chr, m)))

# 输出结果
f = open('output.txt', 'w')
f.write(f"gift = {bytes_to_long(gift)}n")
f.write(f"c = {c}n")
for i in range(3108):
    r1 = getrandbits(8)   # 8位随机数（0-255）
    r2 = getrandbits(16)  # 16位随机数（0-65535）
    x = (pow(r1, 2*i, 257) & 0xff) ^ r2
    c = long_to_bytes(x, 2)
    gift += c
m = list(flag)
for i in range(2025):
    shuffle(m)
c = "".join(list(map(chr, m)))
x = (pow(r1, 2*i, 257) & 0xff) ^ r2
c = long_to_bytes(x, 2)  # 转换为2字节
如果 x < 256（即 x 的高8位为0），则：
  long_to_bytes(x, 2) = b'x00' + bytes([x])

如果 x >= 256（即 x 的高8位不为0），则：
  long_to_bytes(x, 2) = bytes([x >> 8]) + bytes([x & 0xff])
x = (pow(r1, 2*i, 257) & 0xff) ^ r2

设 pow(r1, 2*i, 257) & 0xff = y （y 是0-255的一个值）

则：x = y ^ r2
x = y ^ r2
  = y ^ (r2_high * 256 + r2_low)
  = (r2_high * 256) ^ (y ^ r2_low)

x 的高8位 = r2_high
x 的低8位 = y ^ r2_low
gift = long_to_bytes(gift)
g = [gift[2 * i:2 * i + 2][0] for i in range(len(gift) // 2)]
from gf2bv import LinearSystem
from gf2bv.crypto.mt import MT19937

def mt19937(bs, out):
    # 创建一个线性系统，624个32位变量
    lin = LinearSystem([32] * 624)
    mt = lin.gens()  # 获取符号变量（代表MT19937的624个状态）

    rng = MT19937(mt)  # 创建符号MT19937
    zeros = []

    for o in out:
        rng.getrandbits(8)   # 模拟调用 r1 = getrandbits(8)
        # 模拟调用 r2 = getrandbits(16)，然后右移8位
        # 右移8位相当于取高8位
        # 我们知道 r2 >> 8 的结果，与观察值 o 异或应该为某个8位值
        zeros.append(rng.getrandbits(bs) >> 8 ^ int(o))

    # 添加额外约束：MT19937状态的第一个元素的最高位必须为1
    zeros.append(mt[0] ^ int(0x80000000))

    # 求解所有可能的状态
    for sol in lin.solve_all(zeros):
        rng = MT19937(sol)
        pyrand = rng.to_python_random()
        yield pyrand
lin = LinearSystem([32] * 624)
mt = lin.gens()
for o in out:
    rng.getrandbits(8)
    zeros.append(rng.getrandbits(bs) >> 8 ^ int(o))
(r2 >> 8) ^ observed = (pow(r1, 2*i, 257) & 0xff)
(r2 >> 8) ^ observed = 某个0-255的值
zeros.append(mt[0] ^ int(0x80000000))
for sol in lin.solve_all(zeros):
def shuffle(x):
    for i in range(len(x)-1, 0, -1):
        j = randrange(i+1)
        x[i], x[j] = x[j], x[i]
def ins(s, rng, rounds=2025):
    a = list(s)
    n = len(a)
    sw = []

    # 步骤1：重新生成所有的随机数，记录所有交换操作
    for _ in range(rounds):
        for i in range(n - 1, 0, -1):
            j = rng.randrange(i + 1)
            sw.append((i, j))

    # 步骤2：逆序应用交换操作
    for i, j in reversed(sw):
        a[i], a[j] = a[j], a[i]

    if isinstance(s, (bytes, bytearray)):
        return bytes(a)
    return''.join(a)
from sage.all import *
from Crypto.Util.number import *
from gf2bv import LinearSystem
from gf2bv.crypto.mt import MT19937
from output import gift, c

def mt19937(bs, out):
    """
    使用 gf2bv 库恢复 MT19937 随机数生成器的内部状态

    参数:
    bs: 随机数位数
    out: 观测到的输出序列

    返回:
    可能的随机数生成器状态
    """
    lin = LinearSystem([32] * 624)
    mt = lin.gens()

    rng = MT19937(mt)
    zeros = []
    for o in out:
        rng.getrandbits(8)  # 跳过一个8位随机数
        zeros.append(rng.getrandbits(bs) >> 8 ^ int(o))  # 添加约束条件
    zeros.append(mt[0] ^ int(0x80000000))  # MSB 必须为1

    # 求解所有可能的状态
    for sol in lin.solve_all(zeros):
        rng = MT19937(sol)
        pyrand = rng.to_python_random()
        yield pyrand

def ins(s, rng, rounds=2025):
    """
    逆向 shuffle 操作

    参数:
    s: 被打乱的序列
    rng: 随机数生成器（需要与加密时使用的相同状态）
    rounds: shuffle 轮数

    返回:
    还原后的原始序列
    """
    a = list(s)
    n = len(a)
    sw = []

    # 记录所有的交换操作
    for _ in range(rounds):
        for i in range(n - 1, 0, -1):
            j = rng.randrange(i + 1)
            sw.append((i, j))

    # 逆序应用交换操作
    for i, j in reversed(sw):
        a[i], a[j] = a[j], a[i]

    if isinstance(s, (bytes, bytearray)):
        return bytes(a)
    return''.join(a)

# 将 gift 转换为字节
gift = long_to_bytes(gift)

# 提取每两个字节的第一个字节作为观测输出
g = [gift[2 * i:2 * i + 2][0] for i in range(len(gift) // 2)]

print("[*] 开始恢复 MT19937 随机数生成器状态...")
print(f"[*] 观测到的输出数量: {len(g)}")

# 尝试所有可能的随机数生成器状态
for rng in mt19937(16, g):
    print("[*] 找到一个可能的状态，正在验证...")

    # 重新生成 gift 序列
    gg = b''
    for i in range(3108):
        r1 = rng.getrandbits(8)
        r2 = rng.getrandbits(16)
        x = (pow(r1, 2*i, 257) & 0xff) ^ r2
        cc = long_to_bytes(x, 2)
        gg += cc

    # 验证生成的序列是否与原始 gift 匹配
    if gg == gift:
        print("[+] 状态验证成功！")
        print("[*] 正在还原 flag...")
        flag = ins(c, rng)
        print(f"n[+] Flag: {flag}n")
        break
else:
    print("[-] 未找到正确的状态")
g = [gift[2 * i:2 * i + 2][0] for i in range(len(gift) // 2)]
if gg == gift:
    flag = ins(c, rng)
for i, j in reversed(sw):
    a[i], a[j] = a[j], a[i]
```
