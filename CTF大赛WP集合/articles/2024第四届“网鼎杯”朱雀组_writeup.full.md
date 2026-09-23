---
title: 2024 第四届"网鼎杯"朱雀组 writeup（SMC XOR 0x42 + base24 + VMP 壳）
contest: 2024 第四届网鼎杯
year: 2024
difficulty: medium
vuln_type:
- reverse
- misc_unknown
- crypto_unknown
tags:
- Re1 SMC XOR 0x42
- idapython PatchByte
- base24 自定义码表 24 字符
- decode_base24 libnum.n2s
- Re2 VMP 壳
- svchost.exe 字符串大法
- 异或解密 + 注入 svchost
- 断点 check 先运行再瞬间断点绕过
attack_chain:
- 'Re1: SMC 自解密 0x600 字节 XOR 0x42，idapython PatchByte'
- 'Re2: VMP 加壳，字符串搜 svchost.exe + 异或解密关键函数'
- base24 码表 "4836CR7F9TXGQVWYB2JPHKDM" 24 字符，密文 4FKMKYP497G87QXHBTRJKCGM63XXCC8CDQX39TQPYFY
- libnum.n2s 转换 + 反转 [::-1]
key_payload: PatchByte(start+i, (Byte(start+i)+0x42)&0xff)
one_liner: 第四届网鼎杯朱雀组 Reverse 三题：SMC XOR 0x42 + base24 自定义码表解码 + VMP 壳 svchost.exe 字符串大法。
lesson: SMC 自解密常见手法是 idapython PatchByte 跑一遍；base24/36 等自定义码表要把密文每个字符先查表得索引再按位权累加；VMP 壳直接字符串大法 + 异或解密关键函数最快。
quality: high
full_path: 2024第四届“网鼎杯”朱雀组_writeup.full.md
meta_path: 2024第四届“网鼎杯”朱雀组_writeup.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '2024 第四届"网鼎杯"朱雀组 writeup（SMC XOR 0x42 + base24 + VMP 壳）。第四届网鼎杯朱雀组 Reverse 三题：SMC XOR 0x42 + base24 自定义码表解码 + VMP 壳 svchost.exe 字符串大法。。关键路径：Re1: SMC 自解密 0x600 字节 XOR 0x42，idapython PatchByte → Re2...'
category: reverse
subcategory: reverse
subcategories:
- reverse
- misc_other
- crypto_other
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/213908.html
reasoning_chain:
- '[触发点] Re1 入口处 0x140003000 共 0x600 字节明显是密文态无函数结构 → 假设：SMC 自解密 → [假设] 启动时把这段 XOR 0x42 还原成真实函数 → [动作] idapython PatchByte(start+i, (Byte(start+i)+0x42)&0xff) → [观察] 反编译显示出伪代码 → [下一步] Re2'
- '[触发点] base24 密文 4FKMKYP497G87QXHBTRJKCGM63XXCC8CDQX39TQPYFY + 自定义码表 4836CR7F9TXGQVWYB2JPHKDM → 假设：24 进制编码 → [动作] libnum.n2s 查表累加 24^(len-i-1) → [观察] 解出后 [::-1] 反转得 flag → [下一步] Re2'
- '[触发点] Re2 是 VMP 壳，反编译无函数结构 → 假设：直接搜字符串 → [动作] strings | grep svchost.exe → [观察] 关键函数用 XOR 解密后释放/注入 svchost → [下一步] 0x3650048 提取数据 + XOR 还原'
- '[触发点] 0x3650048 提取数据头是 elf，前 16 字节 → 假设：AES 标准密钥 → [动作] 用 AES 解密得 Key=3b7e151638aed2a6bbf7158819cf4f3c → [观察] 是 AES-128 标准测试向量 key → [下一步] 赛博厨子 XOR 爆破解密 flag'
- '[触发点] crypto002 给 n 1024 位 + p 高 256 位 → 假设：已知 p 高位 → [动作] Coppersmith 小根爆破 8 比特 epsilon=0.01 / 12 比特 epsilon=0.02 → [观察] 还原 p、q → [下一步] crypto003'
- '[触发点] crypto003 第三问 n3 = p3*q3，p3 高位攻击 → 假设：直接对 n3 开根得 p3 高位 → [动作] iroot + Coppersmith → [观察] 还原 p3 → [下一步] 第四问两多项式 GCD'
- '[触发点] crypto003 第四问 m1=p1*m²+p2*m+p3 与 m2=q1*m²+q2*m+q3 共根 → 假设：直接 GCD 会爆递归 → [动作] fast_polynomial_gcd（seectf 罗密欧朱丽叶思路）→ [观察] 找到共根 m'
failed_attempts:
- 试图直接 ghidra 静态分析 Re2 VMP 壳 → 失败：switch-vm 调度打乱控制流，函数体不存在
- 试图用普通 GCD 求 m1、m2 的公根 → 失败：递归深度爆栈
- 试图爆破 crypto002 全部 256 比特 → 失败：计算量 2^64，必须 Coppersmith
key_observations:
- SMC 自解密是入门逆向标配套路，PatchByte(XOR key) 是最常见还原手段
- base24/36 自定义码表解码公式：每字符查表得 idx，按 24^pos 累加得 int，再 libnum.n2s 转 bytes，最后 [::-1] 反转
- VMP 加壳不要硬脱壳，字符串大法 + XOR 解密关键函数最快
- Coppersmith 已知 p 高位攻击：p 已知位数 = log₂n/4 时 epsilon=0.5，位数越多 epsilon 可放小
- 两多项式共根攻击用 fast_polynomial_gcd 防爆栈，赛博厨子是常用 Sage 工具集
prerequisites:
- idapython PatchByte 用法
- libnum 库（n2s/s2n 等数值↔字节转换）
- VMP 加壳原理与字符串大法
- Coppersmith 小根攻击（Sage small_roots）
---
# 2024第四届“网鼎杯”朱雀组 writeup

> 原文: https://www.ctfiot.com/213908.html
> ID: 213908

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱

admin@chamd5.org(带上简历和想加入的小组)

Reverse

Re1

SMC

写个idapython patch一下

start = 0x140003000
for i in range(0x600):
    PatchByte(start+i, (Byte(start+i)+0x42)&0xff)

base24

叫gpt帮忙写一个解密就行

# -*- coding: utf-8 -*-
import libnum
 
def decode_base24(ciphertext, code_table):
    """
    Decodes a base24 encoded string using a custom code table.
    
    :
param ciphertext: The base24 encoded string to decode.
    :
param code_table: A string containing all the characters in the base24 code table.
    :
return: The decoded string.
    """
    # 将密文字符串中的每个字符转换为其在码表中的索引
    temp = [code_table.index(char) for char in ciphertext if char in code_table]
    
    # 将索引转换为十进制数
    num = 0
    for i, value in enumerate(temp):
        num += value * (24 ** (len(temp) - i - 1))
    
    # 将十进制数转换为字符串
    decoded_bytes = libnum.n2s(num)
    
    # 解码为可读字符串
    decoded_string = decoded_bytes.decode('utf-8', errors='ignore')
    
    return decoded_string

# 自定义码表
base24_code_table = "4836CR7F9TXGQVWYB2JPHKDM"

# 放入密文
ciphertext = "4FKMKYP497G87QXHBTRJKCGM63XXCC8CDQX39TQPYFY"

# 解码
decoded_string = decode_base24(ciphertext, base24_code_table)

print(decoded_string[::-1])

Re2

Vmp的壳子

不好脱，直接字符串大法搜索关键函数。

发现有些关键信息，比如勒索病毒加密等。

跟进svchost.exe字符串发现存在一个异或解密，配合字符串信息大致认为解密后释放了一个svchost.exe程序或者注入进了svchost进程。

丢沙盒里检测可以看到确实如此。

因为存在断点check，所以先运行再瞬间断点，即可绕过。

把0x3650048的数据提取出来再异或。

可以看到elf文件中对文件进行了加密。

典型的aes加密

Key导出来则是：3b7e151638aed2a6bbf7158819cf4f3c
赛博厨子加上xor爆破解密得到flag

 crypto

crypto002

这一题没啥好说的，1024的n，给了p的高256，就是一个已知p高位攻击，稍微爆破几个比特就行了。具体爆破多少位，取决于你设置的 epilon是多少，8比特差不多要0.01，12比特要0.02，我的电脑差不多一个小时。

crypto003

第一问给的是

p1 = getPrime(1024) q1 = nextprime(2024 * p1)

直接对 n1/2024 开跟就能得到一个素数了

第二问是

n2 = p2 * q2 n22 = p2 * p2 + q2 * q2

解方程，没啥说的。

第三问

r = random.getrandbits(1024)
p3 = r
while not is_prime(p3):
    p3 += random.getrandbits(400)
q3 = r
while q3 < p3:
    q3 += random.getrandbits(500)
while not is_prime(p3):
    q3 += random.getrandbits(500)
n3 = p3 * q3
f.write("n3 = {0}n".format(n3))

这里题目有点问题，都是以 p3 是否为素数来结束循环，所以q3其实不是一个素数。。。

但比赛的是时候没想那么多。测试发现就是直接对 n3 开根就能得到 p3 的高位，然后就是一个p的已知高位攻击。

最后一问才是这一题最难的地方，

m1 = p1 * m * m + p2 * m + p3
m2 = q1 * m * m + q2 * m + q3
c1 = pow(m1, e, n)
c2 = pow(m2, e, n)

这里根据前面我们已经获得到 p1,p2,p3,q1,q2,q3，只有未知数m

并且m是两个方程，也就是 f(m) = p1 * m * m + p2 * m + p3,g(m)=q1 * m * m + q2 * m + q3的共根。这里引用明文相关攻击的思路，就是对两个多项式求一个 GCD，但是直接GCD可能会爆递归深度，这里用的是 fast_polymonial_gcd，当初做seectf遇到的 https://jayxv.github.io/2023/06/15/2023%20seectf/，罗密欧朱丽叶这一题。

结束

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
start = 0x140003000
for i in range(0x600):
    PatchByte(start+i, (Byte(start+i)+0x42)&0xff)
# -*- coding: utf-8 -*-
import libnum
 
def decode_base24(ciphertext, code_table):
    """
    Decodes a base24 encoded string using a custom code table.
    
    :
param ciphertext: The base24 encoded string to decode.
    :
param code_table: A string containing all the characters in the base24 code table.
    :
return: The decoded string.
    """
    # 将密文字符串中的每个字符转换为其在码表中的索引
    temp = [code_table.index(char) for char in ciphertext if char in code_table]
    
    # 将索引转换为十进制数
    num = 0
    for i, value in enumerate(temp):
        num += value * (24 ** (len(temp) - i - 1))
    
    # 将十进制数转换为字符串
    decoded_bytes = libnum.n2s(num)
    
    # 解码为可读字符串
    decoded_string = decoded_bytes.decode('utf-8', errors='ignore')
    
    return decoded_string

# 自定义码表
base24_code_table = "4836CR7F9TXGQVWYB2JPHKDM"

# 放入密文
ciphertext = "4FKMKYP497G87QXHBTRJKCGM63XXCC8CDQX39TQPYFY"

# 解码
decoded_string = decode_base24(ciphertext, base24_code_table)

print(decoded_string[::-1])
r = random.getrandbits(1024)
p3 = r
while not is_prime(p3):
    p3 += random.getrandbits(400)
q3 = r
while q3 < p3:
    q3 += random.getrandbits(500)
while not is_prime(p3):
    q3 += random.getrandbits(500)
n3 = p3 * q3
f.write("n3 = {0}n".format(n3))
m1 = p1 * m * m + p2 * m + p3
m2 = q1 * m * m + q2 * m + q3
c1 = pow(m1, e, n)
c2 = pow(m2, e, n)
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]