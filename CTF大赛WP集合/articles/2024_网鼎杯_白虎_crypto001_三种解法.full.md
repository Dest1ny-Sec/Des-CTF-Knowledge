---
title: 网鼎杯 2024 白虎/crypto001
contest: 网鼎杯
year: 2024
difficulty: medium
vuln_type:
- crypto_unknown
- block_cipher
tags:
- S 函数
- MASK
- MT19937
- 线性方程组
- z3
- 自定义分组密码
attack_chain:
- 识别 S 函数结构：IV=7, block_size=64, MASK=64bit
- 简化 S：x2 ^ x3 = x0 ^ MASK（其中 x0 = x<<IV & ((1<<block_size)-1)）
- 推出 enc(x) = S(x) ^ key = x ^ x0 ^ MASK ^ key
- 等效 key 理论：S 复合轮函数可用等效 key 替换
- 解密：先异或 MASK 泄低位，再 unshiftLeft 恢复高位（MT19937 风格）
- 备选 kkp 脚本：enc(x, key^key2^key3) = enc(x, key1) ^ enc(x, key2) ^ enc(x, key3)
- 用线性方程组求 key，再求 msg
key_payload: 'def S(x): x1 = x; x2 = x << IV & MASK; x3 = x << IV & ((1 << block_size) - 1) | MASK; return x1 ^ x2 ^ x3'
one_liner: 自定义 S 函数 + 等效 key 转换 + 线性方程组还原
lesson: 自定义分组密码的 S 函数可通过等价 key 替换和线性方程组分析还原；MASK 异或泄低位 + unshiftLeft 恢复高位是 MT19937 类还原通用思路
quality: medium
full_path: 2024_网鼎杯_白虎_crypto001_三种解法.full.md
meta_path: 2024_网鼎杯_白虎_crypto001_三种解法.meta.md
images_removed: true
images_removed_count: 5
schema_version: v3.0.0-P0
summary: 网鼎杯 2024 白虎/crypto001。自定义 S 函数 + 等效 key 转换 + 线性方程组还原。关键路径：识别 S 函数结构：IV=7, block_size=64, MASK=64bit → 简化 S：x2 ^ x3 = x0 ^ MASK（其中 x0 = x<<IV & ((1<<block_size)-1)） → 推出 enc(x) = S(x) ^ key = x ^ x0...
category: crypto
subcategory: crypto_other
subcategories:
- crypto_other
- symmetric
tools_used:
- Z3
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 5
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/217400.html
reasoning_chain:
- 触发点：custom block cipher S(x) = x1 ^ x2 ^ x3，IV=7 MASK=64bit → 假设：S 是非线性轮函数
- 动作：把 S拆 x2 = x<<IV & MASK, x3 = x<<IV & ((1<<bs)-1) | MASK → 假设：x0 = x<<IV & ((1<<bs)-1) 是整体变量
- 观察：x2^x3 = x0^MASK 异或恒等成立 → 假设：S(x) = x ^ x0 ^ MASK 实质是线性移位 + MASK 异或
- 触发点：enc(x) = S(x) ^ key 多轮复合 → 假设：可等效 key 替换，苏氨酸理论
- 动作：用等效 key + S 逆函数（先异或 MASK 再 unshiftLeft 低位优先恢复高位）→ 观察：解密密文成功
- 触发点：春哥赛后给 kkp 脚本 → 假设：enc(x, k1^k2^k3) = enc(x,k1)^enc(x,k2)^enc(x,k3) 线性可加
- 动作：用线性方程组遍历 enc(x, key_i) 构造奇数项叠加还原 key → 观察：z3 add + linear solver 给出 key
- 下一步：还原 message 出 flag
failed_attempts:
- 试图 z3 一把梭每轮 S → 失败：S 复合 64 轮约束太多 solver 跑不动
- 试图直接对 S 函数 GF(2) 线性化 → 失败：移位 MASK 异或破坏了 GF(2) 线性
- 试图把多轮 S 视为 AES 等价结构 → 失败：完全不同的 S盒与轮密钥
key_observations:
- 异或恒等 (x&MASK)^(x|MASK) = x^MASK 是位运算化简的经典公式
- MT19937 风格的 unshiftLeft 思路可用于任何「低位移位 + MASK 异或」加密
- 自定义分组密码的 S 函数若可化为等效 key，可走 z3 + 线性方程组双解
- kkp 脚本思路 enc(x,k1^k2^k3)=enc1^enc2^enc3 = 线性分组密码通用破解模式
prerequisites:
- Z3 约束求解器使用
- Python 整数位运算基础（移位 / 与 / 异或）
- MT19937 反推 unshift 思路
- 线性方程组求解（numpy.linalg 或 z3 BitVec）
---
# 2024 网鼎杯 白虎 crypto001 三种解法

> 原文: https://www.ctfiot.com/217400.html
> ID: 217400

解法1

前面一篇文章提到的 z3 一把梭

解法2（来自苏氨酸）

IV = 7
block_size = 64
MASK = 0b1110001001111001000110010000100010101111101100101110100001001001

def S(x):
    x1 = x
    x2 = x << IV & MASK
    x3 = x << IV & ((1 << block_size) - 1) | MASK
    return x1 ^ x2 ^ x3

注意到 x2 和 x3 的定义，由于 MASK 是 64 比特的，所以其实也可以写成这样

x2 = x << IV & ((1 << block_size) - 1) & MASK
x3 = x << IV & ((1 << block_size) - 1) | MASK

其中 x << IV & ((1 << block_size) - 1) 先运算，可以看作一个整体设为 x0，

于是 x2 ^ x3 = (x0 & MASK) ^ (x0 | MASK)

鄙人 离散对数 学的也不是很好，所以蛮力了一下

x0 = 1,MASK = 1 -> 1 ^ 1 = 0
x0 = 0,MASK = 1 -> 0 ^ 1 = 1
x0 = 1,MASK = 0 -> 0 ^ 1 = 1
X0 = 0,MASK = 0 -> 0 ^ 0 = 0

于是粗鄙地得出结论，x2 ^ x3 = x0 ^ MASK

那么 S(x) = x ^ x0 ^ MASK，enc(x) = S(x) ^ key = x ^ x0 ^ MASK ^ key

虽然这样子看着挺不错的，但是由于 x0 的存在，多轮复合起来似乎也不太那么好处理。 苏氨酸提出了一个等效 key 的理论。就是先不用 key 进行加密，最后一轮的时候用一个等效 key 异或补掉。一图以蔽之，就是

不过这样在解密的时候就需要写一个 S 函数的逆函数了。这也不难写，先把MASK异或掉，然后由于 x0 的低位是 0，就能把 x 的低位泄露，然后再去恢复 x 的高位。就跟 MT19937 crack 的那个  unshiftLeft 差不多。

解法3 （来自春哥）

赛后春哥也在 1997 分享了他的 kkp 脚本，

发现 enc(x,key^key2^key3) = enc(x,key1) ^ enc(x,key2) ^ enc(x,key3)

只有奇数项才会满足，不足奇数项就用 0 补齐。

上图表示，在明文确定的情况下，密钥 7 的密文 等价于  1 的密文 异或 2 的密文 异或 4 的密文

上图表示，在明文确定的情况下，密钥 15 的密文 等价于  1 的密文 异或 2 的密文 异或 4的密文 异或 8 的密文 异或 0 的密文

所以用 msg 和

 建一个

 表，然后求解一个线性方程组，找到
 是由哪些

 加起来的就可以了。确定了 key 后，解 msg 也是同理

上图表示，在密钥固定的情况下，明文 15 的密文 等价于  1的密文 异或 2的密文 异或 4的密文 异或 8 的密文 异或 0 的密文


```
IV = 7
block_size = 64
MASK = 0b1110001001111001000110010000100010101111101100101110100001001001

def S(x):
    x1 = x
    x2 = x << IV & MASK
    x3 = x << IV & ((1 << block_size) - 1) | MASK
    return x1 ^ x2 ^ x3
x2 = x << IV & ((1 << block_size) - 1) & MASK
x3 = x << IV & ((1 << block_size) - 1) | MASK
x0 = 1,MASK = 1 -> 1 ^ 1 = 0
x0 = 0,MASK = 1 -> 0 ^ 1 = 1
x0 = 1,MASK = 0 -> 0 ^ 1 = 1
X0 = 0,MASK = 0 -> 0 ^ 0 = 0
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]