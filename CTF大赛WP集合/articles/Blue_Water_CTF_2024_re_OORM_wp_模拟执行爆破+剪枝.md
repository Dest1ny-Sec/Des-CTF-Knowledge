# Blue Water CTF 2024 re OORM wp 模拟执行爆破+剪枝

> 原文: https://www.ctfiot.com/213273.html
> ID: 213273

一

re OORM

二

main

times = 0;
 do
 {
 for ( i = 0LL; i != 400; ++i )
 {
 keyA = keyAs_2135E0[i];
 if ( runA )
 {
 ++times;
 funcs_A_211CA0[i](keyA, input_in_bits_A_214EE0[i]);
 keyAs_2135E0[i] = 0LL;
 }
 keyB = keyBs_212960[i];
 if ( keyB )
 {
 ++times;
 funcs_B_211020[i](keyB, input_in_bits_B_214260[i]);
 keyBs_212960[i] = 0LL;
 }
 }
 }
 while ( times <= 799 );

三

800个函数分析

void funcs_A_0(__int64 key, __int64 input_bit) {
 x = input_bit | (key<< 1);
 y = hashA0(x);
 // 48 89 3D B7 C5 mov cs:keyAs_2135E0+0A0h, rdi
 keyAs[20] = y;
}

void funcs_A_1(__int64 key, __int64 input_bit) {
 x = input_bit | (key<< 1);
 y = hashA1(x);
 // 48 89 3D FF BA mov cs:keyAs_2135E0+0A8h, rdi
 keyAs[21] = y;
}

void funcs_A_399(__int64 key, __int64 input_bit) {
 x = input_bit | (key<< 1);
 y = hashA399(x);
 if ( y == 21961 || y == 27098 )
 ++dwCheck_212940;
}

四

模拟执行爆破+剪枝

[0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1] 32766
[0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1] 32766
[0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1] 32766
[0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1] 32766
[0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1] 32766
[0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1] 32766
[0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1] 32766
[0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0] 3090
...
[1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1] 32766
[1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0] 3090
[1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0] 3090
...

from capstone import *
from unicorn import *
from unicorn.x86_const import *
from elftools.elf.elffile import ELFFile

keyAs = [9644, 31494, 15772, ..., 0, 0, 0, ...]

f = open('main', 'rb')
elff = ELFFile(f)

def rva_to_offset(elff, rva):
 for segment in elff.iter_sections():
 if rva >= segment['p_vaddr'] and rva < segment['p_vaddr'] + segment['p_memsz']:
 return rva - segment['p_vaddr'] + segment['p_offset']
 raise ValueError('RVA not within any segment')
 
def read_elf_content_by_rva(elff, rva, size):
 for segment in elff.iter_segments():
 # 检查RVA是否在当前段的范围内
 if rva >= segment['p_vaddr'] and rva < segment['p_vaddr'] + segment['p_memsz']:
 foa = rva - segment['p_vaddr']
 content = segment.data()[foa : foa + size]
 return content

# 收集函数的地址

funcs_A = [int.from_bytes(read_elf_content_by_rva(elff, 0x211CA0 + i * 8, 8), 'little') for i in range(400)]

funcs_A.append(0x106430)

endAs = [ 28866, 31618, 34242, ...]
tyAs = [ 39, 39, 39, ..., (35, 32766, 3090), (35, 6485, 4159), (35, 14535, 24449), ...]

def sim2(uc: Uc, i, j, key, input_bit):
 # func arg
 idx = i + j * 20
 uc.reg_write(UC_X86_REG_RDI, key)
 uc.reg_write(UC_X86_REG_RSI, input_bit)
 uc.emu_start(funcs_A[idx], endAs[idx], 0, 0)
 if j != 19:
 return uc.reg_read(tyAs[idx]), 0, 0
 else:
 return uc.reg_read(tyAs[idx][0]), tyAs[idx][1], tyAs[idx][2]

uc = Uc(UC_ARCH_X86, UC_MODE_64)

# code
for segment in elff.iter_segments():
 if segment['p_vaddr'] == 0x6000:
 uc.mem_map(segment['p_vaddr'], segment['p_memsz']//0x1000*0x1000 + 0x1000)
 uc.mem_write(segment['p_vaddr'], segment.data())

# 执行funcA[i + j * 20](key, 0) 和 funcA[i + j * 20](key, 1)
def dfsA(i, j, key) -> bool:
 global path, uc

 if j == 3: # unicron的bug，得隔一定次数重新创建一个Uc
 uc = Uc(UC_ARCH_X86, UC_MODE_64)
 for segment in elff.iter_segments():
 if segment['p_vaddr'] == 0x6000:
 uc.mem_map(segment['p_vaddr'], segment['p_memsz']//0x1000*0x1000 + 0x1000)
 uc.mem_write(segment['p_vaddr'], segment.data())

 if j == 6:
 print(path)

 if j == 19:
 new_key, t0, t1 = sim2(uc, i, j, key, 0)
 if new_key == t0 or new_key == t1:
 print('path', path + [0], new_key)
 
 new_key, t0, t1 = sim2(uc, i, j, key, 1)
 if new_key == t0 or new_key == t1:
 print('path', path + [1], new_key)
 else:
 new_key, _, _ = sim2(uc, i, j, key, 0)
 path.append(0)
 dfsA(i, j + 1, new_key)
 path.pop()
 
 new_key, _, _ = sim2(uc, i, j, key, 1)
 path.append(1)
 dfsA(i, j + 1, new_key)
 path.pop()

path = []
dfsA(0, 0, keyAs[0])

f.close()

_, _, _, _, _, _, _, _, _, _, _, _, _, 1, _, 1, 1, _, _, _
_, 1, _, 1, 1, _, _, _, _, _, 1, _, _, 1, _, 1, 1, _, _, _
_, _, _, 1, _, _, 1, 1, _, _, 1, _, _, 0, _, 0, 1, _, _, _
_, _, _, 1, _, 1, _, 1, _, _, 1, _, _, 1, _, 1, 0, _, _, _
_, 1, _, _, 1, 1, _, _, 1, _, 1, _, _, 1, _, 1, 1, _, _, 1
_, _, 1, _, 1, 1, _, _, _, _, 1, _, 1, 0, _, 1, 0, _, _, _
_, _, _, 1, 1, 1, _, _, _, _, 1, _, 1, 1, _, 0, 1, _, _, _
_, 1, _, 1, 1, 1, _, 1, _, _, 1, _, 1, 1, 1, 1, 1, _, 1, _
1, 1, _, 1, 1, 1, 1, 1, _, _, 1, _, _, 1, 1, 1, 1, _, _, 1
_, 1, 1, _, 1, 1, 1, 1, _, _, 1, _, _, 1, 1, 1, 1, _, _, 1
_, 1, 1, _, _, 1, 1, 1, _, 1, _, 1, _, 1, 1, 1, 1, _, _, 1
_, _, 1, 1, _, _, 1, _, _, 1, _, 1, _, 1, _, 1, 1, _, _, 1
_, _, 1, 1, 1, _, 1, _, _, 1, 1, 1, _, 0, _, 0, 1, _, 1, 1
_, 1, 1, 1, 1, _, 1, _, _, 1, _, _, _, 1, _, 1, 0, _, 1, 1
_, 1, 1, 1, 1, _, 1, _, _, 1, _, _, _, 1, _, 1, 1, _, _, 1
1, 1, 1, 1, _, _, _, _, _, _, 1, _, _, 1, _, 1, 1, _, _, 1
_, 1, 1, 1, _, _, _, _, 1, _, 1, _, _, 1, _, 0, 1, _, _, 1
_, 1, 1, _, 1, _, _, 1, 1, _, _, _, _, 1, 1, 1, 1, _, _, 1
_, 1, _, _, 1, _, _, _, _, _, _, _, _, 1, _, 1, 1, _, _, _
_, _, _, _, _, _, _, _, _, _, _, _, _, 1, _, 1, 1, _, _, _

看雪ID：wx_御史神风

https://bbs.kanxue.com/user-home-1000123.htm

*本文为看雪论坛优秀文章，由 wx_御史神风 原创，转载请注明来自看雪社区

# 往期推荐

1、PWN入门-SROP拜师

2、一种apc注入型的Gamarue病毒的变种

3、野蛮fuzz：提升性能

4、关于安卓注入几种方式的讨论，开源注入模块实现

5、2024年KCTF水泊梁山-反混淆

球分享

球点赞

球在看

点击阅读原文查看更多


```
一
re OORM
```



```
二
main
```



```
times = 0;
 do
 {
 for ( i = 0LL; i != 400; ++i )
 {
 keyA = keyAs_2135E0[i];
 if ( runA )
 {
 ++times;
 funcs_A_211CA0[i](keyA, input_in_bits_A_214EE0[i]);
 keyAs_2135E0[i] = 0LL;
 }
 keyB = keyBs_212960[i];
 if ( keyB )
 {
 ++times;
 funcs_B_211020[i](keyB, input_in_bits_B_214260[i]);
 keyBs_212960[i] = 0LL;
 }
 }
 }
 while ( times <= 799 );
```



```
三
800个函数分析
```



```
void funcs_A_0(__int64 key, __int64 input_bit) {
 x = input_bit | (key<< 1);
 y = hashA0(x);
 // 48 89 3D B7 C5 mov cs:keyAs_2135E0+0A0h, rdi
 keyAs[20] = y;
}
```



```
void funcs_A_1(__int64 key, __int64 input_bit) {
 x = input_bit | (key<< 1);
 y = hashA1(x);
 // 48 89 3D FF BA mov cs:keyAs_2135E0+0A8h, rdi
 keyAs[21] = y;
}
```



```
void funcs_A_399(__int64 key, __int64 input_bit) {
 x = input_bit | (key<< 1);
 y = hashA399(x);
 if ( y == 21961 || y == 27098 )
 ++dwCheck_212940;
}
```



```
四
模拟执行爆破+剪枝
```



```
[0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1] 32766
[0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1] 32766
[0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1] 32766
[0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1] 32766
[0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1] 32766
[0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1] 32766
[0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1] 32766
[0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0] 3090
...
[1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1] 32766
[1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0] 3090
[1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0] 3090
...
```



```
from capstone import *
from unicorn import *
from unicorn.x86_const import *
from elftools.elf.elffile import ELFFile

keyAs = [9644, 31494, 15772, ..., 0, 0, 0, ...]

f = open('main', 'rb')
elff = ELFFile(f)

def rva_to_offset(elff, rva):
 for segment in elff.iter_sections():
 if rva >= segment['p_vaddr'] and rva < segment['p_vaddr'] + segment['p_memsz']:
 return rva - segment['p_vaddr'] + segment['p_offset']
 raise ValueError('RVA not within any segment')
 
def read_elf_content_by_rva(elff, rva, size):
 for segment in elff.iter_segments():
 # 检查RVA是否在当前段的范围内
 if rva >= segment['p_vaddr'] and rva < segment['p_vaddr'] + segment['p_memsz']:
 foa = rva - segment['p_vaddr']
 content = segment.data()[foa : foa + size]
 return content

# 收集函数的地址

funcs_A = [int.from_bytes(read_elf_content_by_rva(elff, 0x211CA0 + i * 8, 8), 'little') for i in range(400)]

funcs_A.append(0x106430)

endAs = [ 28866, 31618, 34242, ...]
tyAs = [ 39, 39, 39, ..., (35, 32766, 3090), (35, 6485, 4159), (35, 14535, 24449), ...]

def sim2(uc: Uc, i, j, key, input_bit):
 # func arg
 idx = i + j * 20
 uc.reg_write(UC_X86_REG_RDI, key)
 uc.reg_write(UC_X86_REG_RSI, input_bit)
 uc.emu_start(funcs_A[idx], endAs[idx], 0, 0)
 if j != 19:
 return uc.reg_read(tyAs[idx]), 0, 0
 else:
 return uc.reg_read(tyAs[idx][0]), tyAs[idx][1], tyAs[idx][2]

uc = Uc(UC_ARCH_X86, UC_MODE_64)

# code
for segment in elff.iter_segments():
 if segment['p_vaddr'] == 0x6000:
 uc.mem_map(segment['p_vaddr'], segment['p_memsz']//0x1000*0x1000 + 0x1000)
 uc.mem_write(segment['p_vaddr'], segment.data())

# 执行funcA[i + j * 20](key, 0) 和 funcA[i + j * 20](key, 1)
def dfsA(i, j, key) -> bool:
 global path, uc

 if j == 3: # unicron的bug，得隔一定次数重新创建一个Uc
 uc = Uc(UC_ARCH_X86, UC_MODE_64)
 for segment in elff.iter_segments():
 if segment['p_vaddr'] == 0x6000:
 uc.mem_map(segment['p_vaddr'], segment['p_memsz']//0x1000*0x1000 + 0x1000)
 uc.mem_write(segment['p_vaddr'], segment.data())

 if j == 6:
 print(path)

 if j == 19:
 new_key, t0, t1 = sim2(uc, i, j, key, 0)
 if new_key == t0 or new_key == t1:
 print('path', path + [0], new_key)
 
 new_key, t0, t1 = sim2(uc, i, j, key, 1)
 if new_key == t0 or new_key == t1:
 print('path', path + [1], new_key)
 else:
 new_key, _, _ = sim2(uc, i, j, key, 0)
 path.append(0)
 dfsA(i, j + 1, new_key)
 path.pop()
 
 new_key, _, _ = sim2(uc, i, j, key, 1)
 path.append(1)
 dfsA(i, j + 1, new_key)
 path.pop()

path = []
dfsA(0, 0, keyAs[0])

f.close()
```



```
_, _, _, _, _, _, _, _, _, _, _, _, _, 1, _, 1, 1, _, _, _
_, 1, _, 1, 1, _, _, _, _, _, 1, _, _, 1, _, 1, 1, _, _, _
_, _, _, 1, _, _, 1, 1, _, _, 1, _, _, 0, _, 0, 1, _, _, _
_, _, _, 1, _, 1, _, 1, _, _, 1, _, _, 1, _, 1, 0, _, _, _
_, 1, _, _, 1, 1, _, _, 1, _, 1, _, _, 1, _, 1, 1, _, _, 1
_, _, 1, _, 1, 1, _, _, _, _, 1, _, 1, 0, _, 1, 0, _, _, _
_, _, _, 1, 1, 1, _, _, _, _, 1, _, 1, 1, _, 0, 1, _, _, _
_, 1, _, 1, 1, 1, _, 1, _, _, 1, _, 1, 1, 1, 1, 1, _, 1, _
1, 1, _, 1, 1, 1, 1, 1, _, _, 1, _, _, 1, 1, 1, 1, _, _, 1
_, 1, 1, _, 1, 1, 1, 1, _, _, 1, _, _, 1, 1, 1, 1, _, _, 1
_, 1, 1, _, _, 1, 1, 1, _, 1, _, 1, _, 1, 1, 1, 1, _, _, 1
_, _, 1, 1, _, _, 1, _, _, 1, _, 1, _, 1, _, 1, 1, _, _, 1
_, _, 1, 1, 1, _, 1, _, _, 1, 1, 1, _, 0, _, 0, 1, _, 1, 1
_, 1, 1, 1, 1, _, 1, _, _, 1, _, _, _, 1, _, 1, 0, _, 1, 1
_, 1, 1, 1, 1, _, 1, _, _, 1, _, _, _, 1, _, 1, 1, _, _, 1
1, 1, 1, 1, _, _, _, _, _, _, 1, _, _, 1, _, 1, 1, _, _, 1
_, 1, 1, 1, _, _, _, _, 1, _, 1, _, _, 1, _, 0, 1, _, _, 1
_, 1, 1, _, 1, _, _, 1, 1, _, _, _, _, 1, 1, 1, 1, _, _, 1
_, 1, _, _, 1, _, _, _, _, _, _, _, _, 1, _, 1, 1, _, _, _
_, _, _, _, _, _, _, _, _, _, _, _, _, 1, _, 1, 1, _, _, _
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/5-1730546467.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/0-1730546468.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/8-1730546468.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/6-1730546469.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/4-1730546470.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/11/9-1730546470.gif)