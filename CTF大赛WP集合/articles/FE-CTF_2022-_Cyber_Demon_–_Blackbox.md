# FE-CTF 2022: Cyber Demon – Blackbox

> 原文: https://www.ctfiot.com/82141.html
> ID: 82141


```
$ file file
file: data
```



```
$ hexdump -C file
00000000 80 42 4d 8a 40 38 00 00 28 54 00 8a 29 7c 2a 05 |.BM.@8..(T..)|*.|
00000010 28 d0 82 02 28 01 00 20 00 03 2a 79 01 c3 0e 00 |(...(.. ..*y....|
00000020 e2 0a d4 ff 87 e9 d3 9b 42 47 52 73 17 df bf 77 |........BGRs...w|
00000030 2f 07 01 04 07 04 f0 5e 2a 12 ff e2 c6 87 47 8f |/......^*.....G.|
00000040 07 07 07 01 6b 52 15 e2 ff c6 07 07 07 07 07 a7 |....kR..........|
00000050 67 e3 27 07 6b 52 15 e2 c6 07 7f 06 87 47 07 07 |g.'.kR.......G..|
00000060 07 01 33 fc 12 05 e2 c6 87 47 07 07 ff 07 07 07 |..3......G......|
00000070 07 07 07 07 07 ff 07 07 07 07 07 07 07 07 ff 07 |................|
00000080 07 07 07 07 07 07 07 ff 07 07 07 07 07 07 07 07 |................|
00000090 ff 07 07 07 07 07 07 07 07 ff 07 07 07 07 07 07 |................|
000000a0 07 07 ff 07 07 07 07 07 07 07 07 ff 07 07 07 07 |................|
[...]
```



```
$ nc blackbox.hack.fe-ctf.dk 1337
== proof-of-work: disabled ==
<enter>
<enter>
<enter>
<enter>
<enter>
$
```



```
from pwn import *
sock = remote('blackbox.hack.fe-ctf.dk', 1337)
for i in iters.count(1):
 sock.send(b'\n')
 print(f'sent {i} bytes')
 print('>>>', sock.recv(timeout=1))
```



```
$ python recon0.py
[+] Opening connection to blackbox.hack.fe-ctf.dk on port 1337: Done
sent 1 bytes
>>> b'== proof-of-work: disabled ==\n'
sent 2 bytes
>>> b''
sent 3 bytes
>>> b''
sent 4 bytes
Traceback (most recent call last):
 File "/home/user/recon0.py", line 6, in <module>
 print('>>>', sock.recv(timeout=1))
[...]
EOFError
[*] Closed connection to blackbox.hack.fe-ctf.dk port 1337
```



```
from pwn import *
def test(data):
 sock = remote('blackbox.hack.fe-ctf.dk', 1337)
 print(f'sending {data}')
 for i, b in enumerate(data, start=1):
 sock.send(bytes([b]))
 print(f'sent {i} bytes')
 try:
 print('>>>', sock.recv(timeout=1))
 except EOFError:
 print('connection closed')
 break
 sock.close()

for data in iters.combinations_with_replacement(range(256), 4):
 test(bytes(data))
```



```
$ python recon1.py
[+] Opening connection to blackbox.hack.fe-ctf.dk on port 1337: Done
sending b'\x00\x00\x00\x00'
sent 1 bytes
>>> b'== proof-of-work: disabled ==\n'
sent 2 bytes
>>> b''
sent 3 bytes
>>> b''
sent 4 bytes
connection closed
[*] Closed connection to blackbox.hack.fe-ctf.dk port 1337
[+] Opening connection to blackbox.hack.fe-ctf.dk on port 1337: Done
sending b'\x00\x00\x00\x01'
sent 1 bytes
>>> b'== proof-of-work: disabled ==\n'
sent 2 bytes
>>> b''
sent 3 bytes
>>> b''
sent 4 bytes
connection closed
[*] Closed connection to blackbox.hack.fe-ctf.dk port 1337
[+] Opening connection to blackbox.hack.fe-ctf.dk on port 1337: Done
sending b'\x00\x00\x00\x02'
sent 1 bytes
>>> b'== proof-of-work: disabled ==\n'
sent 2 bytes
>>> b''
sent 3 bytes
>>> b''
sent 4 bytes
connection closed
[...]
```



```
for data in iters.combinations_with_replacement(
 reversed(range(256)), 4):
```



```
test(bytes(reversed(data)))
```



```
$ python recon2.py
[+] Opening connection to blackbox.hack.fe-ctf.dk on port 1337: Done
sending b'\x00\x00\x00\x00'
sent 1 bytes
>>> b'== proof-of-work: disabled ==\n'
sent 2 bytes
>>> b''
sent 3 bytes
>>> b''
sent 4 bytes
connection closed
[*] Closed connection to blackbox.hack.fe-ctf.dk port 1337
[+] Opening connection to blackbox.hack.fe-ctf.dk on port 1337: Done
sending b'\x01\x00\x00\x00'
sent 1 bytes
>>> b'== proof-of-work: disabled ==\n'
sent 2 bytes
>>> b''
sent 3 bytes
>>> b''
sent 4 bytes
>>> b''
[*] Closed connection to blackbox.hack.fe-ctf.dk port 1337
[+] Opening connection to blackbox.hack.fe-ctf.dk on port 1337: Done
sending b'\x02\x00\x00\x00'
sent 1 bytes
>>> b'== proof-of-work: disabled ==\n'
sent 2 bytes
>>> b''
sent 3 bytes
>>> b''
sent 4 bytes
>>> b''
[*] Closed connection to blackbox.hack.fe-ctf.dk port 1337
```



```
from pwn import *
def test(numb):
 sock = remote('blackbox.hack.fe-ctf.dk', 1337)
 # Read "proof-of-work" line
 sock.recvline()
 print(f'length = {numb} bytes')
 sock.send(p32(numb))
 for realnumb in iters.count():
 print(f'sent {realnumb} bytes')
 try:
 print('>>>', sock.recv(timeout=1))
 except EOFError:
 print('connection closed')
 print(f'successfully sent {realnumb} bytes')
 break
 sock.send(b'A')
 sock.close()
for numb in iters.count():
 test(numb)
```



```
$ python recon3.py
[+] Opening connection to blackbox.hack.fe-ctf.dk on port 1337: Done
length = 0 bytes
sent 0 bytes
connection closed
successfully sent 0 bytes
[*] Closed connection to blackbox.hack.fe-ctf.dk port 1337
[+] Opening connection to blackbox.hack.fe-ctf.dk on port 1337: Done
length = 1 bytes
sent 0 bytes
>>> b''
sent 1 bytes
>>> b'\x00A'
sent 2 bytes
connection closed
successfully sent 2 bytes
[*] Closed connection to blackbox.hack.fe-ctf.dk port 1337
[+] Opening connection to blackbox.hack.fe-ctf.dk on port 1337: Done
length = 2 bytes
sent 0 bytes
>>> b''
sent 1 bytes
>>> b''
sent 2 bytes
>>> b'\x00AA'
sent 3 bytes
connection closed
successfully sent 3 bytes
[*] Closed connection to blackbox.hack.fe-ctf.dk port 1337
[+] Opening connection to blackbox.hack.fe-ctf.dk on port 1337: Done
length = 3 bytes
sent 0 bytes
>>> b''
sent 1 bytes
>>> b''
sent 2 bytes
>>> b''
sent 3 bytes
>>> b'\x00AAA'
sent 4 bytes
connection closed
successfully sent 4 bytes
[*] Closed connection to blackbox.hack.fe-ctf.dk port 1337
[+] Opening connection to blackbox.hack.fe-ctf.dk on port 1337: Done
length = 4 bytes
sent 0 bytes
>>> b''
sent 1 bytes
>>> b''
sent 2 bytes
>>> b''
sent 3 bytes
>>> b''
sent 4 bytes
>>> b'\x04AA\x00'
sent 5 bytes
connection closed
successfully sent 5 bytes
[*] Closed connection to blackbox.hack.fe-ctf.dk port 1337
[...]
```



```
while True:
 s = sock.recv(timeout=1)
 print('>>>', s)
 if not s:
 break
```



```
$ python recon4.py
[+] Opening connection to blackbox.hack.fe-ctf.dk on port 1337: Done
length = 0 bytes
sent 0 bytes
connection closed
successfully sent 0 bytes
[*] Closed connection to blackbox.hack.fe-ctf.dk port 1337
[+] Opening connection to blackbox.hack.fe-ctf.dk on port 1337: Done
length = 1 bytes
sent 0 bytes
>>> b''
sent 1 bytes
>>> b'\x00A'
connection closed
successfully sent 1 bytes
[*] Closed connection to blackbox.hack.fe-ctf.dk port 1337
[+] Opening connection to blackbox.hack.fe-ctf.dk on port 1337: Done
length = 2 bytes
sent 0 bytes
>>> b''
sent 1 bytes
>>> b''
sent 2 bytes
>>> b'\x00AA'
connection closed
successfully sent 2 bytes
[*] Closed connection to blackbox.hack.fe-ctf.dk port 1337
[...]
```



```
from pwn import *
def encode(data):
 with context.silent:
 sock = remote('blackbox.hack.fe-ctf.dk', 1337)
 # Read "proof-of-work" line
 sock.recvline()
 sock.send(p32(len(data)))
 sock.send(data)
 return sock.recvall()
```



```
$ python send-As.py
Input : 41 length 1
Output: 0041
Input : 4141 length 2
Output: 004141
Input : 414141 length 3
Output: 00414141
Input : 41414141 length 4
Output: 04414100
Input : 4141414141 length 5
Output: 0441410041
Input : 414141414141 length 6
Output: 0c41410000
Input : 41414141414141 length 7
Output: 0c41410001
Input : 4141414141414141 length 8
Output: 0c41410002
Input : 414141414141414141 length 9
Output: 0c4141000241
Input : 41414141414141414141 length 10
Output: 1c4141000200
Input : 4141414141414141414141 length 11
Output: 1c4141000201
[...]
```



```
$ python send-As.py
[...]
Input : 41[...] length 43
Output: fc4141000206070707
Input : 41[...] length 44
Output: fc41410002060707070041
Input : 41[...] length 45
Output: fc41410002060707070100
[...]
```



```
$ python send-Bs.py
[...]
Input : 42[...] length 44
Output: fc42420002060707070042
Input : 42[...] length 45
Output: fc42420002060707070100
```



```
from encode import encode
while True:
 idat = input('> ').strip().encode()
 odat = encode(idat)
 print('Input :', idat.hex(), 'length', len(idat))
 print('Output:', odat.hex())
```



```
$ python encode-interactive.py
> AAABAB
Input : 414141424142 length 6
Output: 104141414210
```



```
> AAABAA
Input : 414141424141 length 6
Output: 104141414200
> AAABAAA
Input : 41414142414141 length 7
Output: 104141414201
> AAABAAB
Input : 41414142414142 length 7
Output: 104141414209
> AAABAAAB
Input : 4141414241414142 length 8
Output: 104141414202
```



```
(AAAB)AA -> (0, 0) # 0x00 = 0b00000_000
(AAAB)AAA -> (1, 0) # 0x01 = 0b00000_001
(AAAB)AAAB -> (2, 0) # 0x02 = 0b00000_010
(AAAB)AAB -> (1, 1) # 0x09 = 0b00001_001
(AAAB)AB -> (0, 2) # 0x10 = 0b00010_000
```



```
$ python encode-interactive.py
> B[...]AAAA
Input : 42[...]41414141 length 33
Output: 7c42420002060702410241e8
> B[...]BAAAA
Input : 42[...]4241414141 length 34
Output: 7c42420002060703410241f0
> B[...]BBAAAA
Input : 42[...]424241414141 length 35
Output: 7c42420002060704410241f0
```



```
OFFSET_BITS = 5
LENGTH_BITS = 3
WINDOW_SIZE = 2**OFFSET_BITS
MIN_LENGTH = 2
MAX_LENGTH = MIN_LENGTH + 2**LENGTH_BITS - 1
def encode_model(idat):
 odat = bytearray()
 i = 0
 while i < len(idat):
 if len(odat) % 9 == 0:
 # Record index of header, which is constructed below
 hdridx = len(odat)
 odat.append(0)
 # Start of window
 window = max(0, i - WINDOW_SIZE)
 best_length = 0
 best_offset = offset = 0
 # Iterate over offsets into window
 while window + offset < i:
 # Iterate over lengths
 length = 0
 while True:
 k = i + length
 l = window + offset + length
 if length >= MAX_LENGTH:
 break
 if k >= len(idat):
 break
 if l >= i:
 break
 if idat[l] != idat[k]:
 break
 length += 1
 if length > best_length:
 best_length = length
 best_offset = offset
 offset += 1
 length = best_length
 offset = best_offset
 if length >= MIN_LENGTH:
 # Patch a 1-bit into header
 odat[hdridx] |= 1 << (len(odat) % 9 - 1)
 # Encode this chunk as a reference
 hdr = (offset << LENGTH_BITS) | (length - MIN_LENGTH)
 odat.append(hdr)
 i += length
 else:
 # Encode raw byte
 odat.append(idat[i])
 i += 1
 return odat

def test():
 import os
 import sys
 import random
 from itertools import count
 from encode import encode as encode_pukka
 for n in count(1):
 ilen = random.randrange(0, 0x1000)
 idat = os.urandom(ilen)
 odat_model = encode_model(idat)
 odat_pukka = encode_pukka(idat)
 if odat_pukka != odat_model:
 print('Found counter example')
 print('Input:', idat.hex())
 print('Pukka output:', odat_pukka.hex())
 print('Model output:', odat_model.hex())
 sys.exit(1)
 else:
 print(f'OK ({n})')

if __name__ == '__main__':
 test()
```



```
$ python model.py
OK (1)
[...]
OK (9001)
```



```
OFFSET_BITS = 5
LENGTH_BITS = 3
WINDOW_SIZE = 2**OFFSET_BITS
MIN_LENGTH = 2
MAX_LENGTH = MIN_LENGTH + 2**LENGTH_BITS - 1
def decode_model(idat):
 odat = bytearray()
 i = 0
 while i < len(idat):
 hdr = idat[i]
 i += 1
 for _ in range(8):
 if hdr & 1:
 # Decode referenced chunk
 pair = idat[i]
 length = (pair & (2**LENGTH_BITS - 1)) + MIN_LENGTH
 offset = pair >> LENGTH_BITS
 window = max(0, len(odat) - WINDOW_SIZE)
 chunk = odat[window + offset : window + offset + length]
 odat.extend(chunk)
 else:
 # Raw byte
 odat.append(idat[i])
 i += 1
 # End of data?
 if i >= len(idat):
 break
 # Next header bit
 hdr >>= 1
 return odat

def test():
 import os
 import sys
 import random
 from itertools import count
 from model import encode_model
 for n in count(1):
 ilen = random.randrange(0, 0x1000)
 idat = os.urandom(ilen)
 odat = encode_model(idat)
 idat2 = decode_model(odat)
 if idat != idat2:
 print('Found counter example')
 print('Input :', idat.hex())
 print('Output :', odat.hex())
 print('Decoded:', idat2.hex())
 sys.exit(1)
 else:
 print(f'OK ({n})')

if __name__ == '__main__':
 test()
```



```
$ python decode.py
OK (1)
OK (2)
[...]
```



```
$ python -c "import decode ; open('file.bmp', 'wb')"\
".write(decode.decode_model(open('file', 'rb').read()))"
```
