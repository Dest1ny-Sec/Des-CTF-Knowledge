# Automotive CTF 2024 World Final Writeup

> 原文: https://www.ctfiot.com/210738.html
> ID: 210738


```
0x000007e0 05 31 01 40 44 ff 00 00
Time;CH 1 SWCLK;CH 2 SWDIO
0.000000000;1;1
0.594872000;0;1
0.594878000;1;1
0.594884000;0;1
0.594890000;1;1
0.594894000;0;0
0.594900000;1;0
…
1-15 SWD: : W AP4
18-22 SWD: : OK
28-90 SWD: : 0xe000ed00
94-108 SWD: : R APc
111-115 SWD: : OK
117-179 SWD: : 0x00000000
187-201 SWD: : RDBUFF
204-208 SWD: : OK
210-272 SWD: : 0x410fd212
280-294 SWD: : R CTRL/STAT
297-301 SWD: : OK
303-365 SWD: : 0xf0000040
372-386 SWD: : W AP4
389-393 SWD: : OK
399-461 SWD: : 0xe0042000
465-479 SWD: : R APc
482-486 SWD: : OK
488-550 SWD: : 0x00000000
…
res = {}

def rev(s):
 return s[6:] + s[4:6] + s[2:4] + s[:2]

with open("annon.txt") as fp:
 state = 0
 addr = ""
 buf = []
 for _line in fp.readlines():
 line = _line[:-1]
 if line.endswith("SWD: : W AP4"):
 assert state == 0
 state = 1
 elif state == 1 and line.endswith(" SWD: : OK"):
 state = 2
 elif state == 2:
 addr = line.split(':')[2]
 buf = []
 state = 3
 elif state == 3:
 if line.endswith("SWD: : RDBUFF"):
 res[addr] = buf
 state = 0
 elif "SWD: : 0x" in line:
 buf.append(rev(line.split(":")[2][3:]))

for addr,bufs in res.items():
 print(addr, bufs)
SCL -> PB10 ->14
SDA -> PB11 -> 15
I2C> [0x63 0x00 0x00 0x01]
(1729536865.698447) can0 778 [8] 62 68 7B 49 4E 46 41 4D 'bh{INFAM'
 (1729536865.700350) can0 778 [8] 4F 55 53 5F 52 45 4D 41 'OUS_REMA'
 (1729536865.708109) can0 778 [3] 4B 45 7D 'KE}'
```
