---
title: 2022 第三届网鼎杯 - 玄武组部分 WriteUp
contest: 2022 第三届网鼎杯 玄武组
year: 2022
difficulty: hard
vuln_type: [crypto_oracle, kernel_exploit, web_unknown, pwn_unknown]
tags: [网鼎杯, 玄武, base62, 自定义字符表, Goldwasser-Micali, 二次剩余, kernel-pwn, msg_msg, sk_buff, pipe_buffer, ROP, UAF, slub]
attack_chain: ["misc999 base62 换表: CHARSET='9876543210qwertyuiopasdfghjklzxcvbnmMNBVCXZLKJHGFDSAPOIUYTREWQ'", "decode 7dFRjPItGFkeXAALp6GMKE9Y4R4BuNtIUK1RECFlU4f3PomCzGnfemFvO → flag{cf492422-13cb-4123-8bc5-5495f0349494}", "crypto 二次剩余 (Goldwasser-Micali): x=quadratic_residue 50%, x^r 也是 50%; flag bit=1→x^r (QR), bit=0→r (QR 50%)", "13 组数据, flag 错误概率 1/2^13", "pwn557 内核 UAF: 分配 0x20 opcode 1024 大小, 释放 0x30 不置零, 4 步利用", "Step 1: 堆喷 msg_msg 主从消息队列", "Step 2: 构造 UAF, 堆喷 sk_buff 定位 victim", "Step 3: 堆喷 sk_buff 伪造辅助消息, 泄露 UAF obj 地址", "Step 4: 堆喷 pipe_buffer, 泄露内核基址", "Step 5: 伪造 pipe_buffer, 构造 ROP, 劫持 RIP, 提权"]
key_payload: "base62.decode('7dFRjPItGFkeXAALp6GMKE9Y4R4BuNtIUK1RECFlU4f3PomCzGnfemFvO')"
one_liner: 网鼎杯 2022 玄武：base62 换表 + Goldwasser-Micali 二次剩余 + 内核 pwn UAF
lesson: Goldwasser-Micali 加密是 QR 加密经典；内核 pwn 用 msg_msg/sk_buff/pipe_buffer 是 2022 热点
quality: high
---

# 2022 第三届网鼎杯 玄武组部分 WriteUp

原文 https://www.ctfiot.com/56442.html

## misc999: base62 换表
```python
import base62
CHARSET_DEFAULT = "9876543210qwertyuiopasdfghjklzxcvbnmMNBVCXZLKJHGFDSAPOIUYTREWQ"
CHARSET_INVERTED = "9876543210qwertyuiopasdfghjklzxcvbnmMNBVCXZLKJHGFDSAPOIUYTREWQ"

str1 = "7dFRjPItGFkeXAALp6GMKE9Y4R4BuNtIUK1RECFlU4f3PomCzGnfemFvO"
print(base62.decodebytes(str1))
# flag{cf492422-13cb-4123-8bc5-5495f0349494}
```

## crypto: Goldwasser-Micali 二次剩余
```python
from Crypto.Util.number import *
import random
# 服务器端
for i in range(18):
    p = getPrime(256)
    x = random.randint(2, p-1)
    tmp = bytes_to_long(flag)
    enc = []
    for j in range(tmp.bit_length()):
        r = random.randint(2, p-1)
        if tmp % 2:
            enc += [pow(x, r, p)]  # QR
        else:
            enc += [r]              # 50% QR
        tmp //= 2

# 客户端
# x 有 50% 是二次剩余
# x^r 也是 50% 二次剩余
# flag bit = 1 → enc = x^r (QR)
# flag bit = 0 → enc = r (50% QR)
# 用多组数据排除 false positive
```

## pwn557: 内核 pwn
```c
// 分配 opcode 0x20 → malloc 1024
// 释放 opcode 0x30 → free 但不置零 → UAF
// 释放大小限制 1024 → 用 1024 大小结构体
```

**4 步利用链：**
1. **堆喷 msg_msg** 主从消息队列
2. 构造 UAF，堆喷 **sk_buff** 定位 victim
3. 堆喷 sk_buff 伪造辅助消息泄露 UAF obj 地址
4. 堆喷 **pipe_buffer** 泄露内核基址
5. 伪造 pipe_buffer + ROP 劫持 RIP → 提权

## 教学价值
- **base62 换表** 入门 crypto
- **Goldwasser-Micali** 二次剩余加密（1982）
- **kernel pwn 4 件套**：msg_msg / sk_buff / pipe_buffer / tty_struct
- **UAF + LIFO slub** 是内核堆利用基础
- **ROP 在内核** = modprobe_path / core_pattern 覆盖

## 工具
- pwntools
- base62
- ropper
- SageMath (QR 测试)

## 关联
- 网鼎杯是国内四大顶级赛事（与强网杯、护网杯、长城杯并列）
- 玄武组是分组（青龙/白虎/朱雀/玄武）
- D3CTF2022 d3kheap 同样是 kernel pwn
