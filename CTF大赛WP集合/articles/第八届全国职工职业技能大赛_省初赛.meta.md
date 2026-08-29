---
title: 第八届全国职工职业技能大赛 省初赛
contest: 全国职工职业技能大赛
year: 2024
difficulty: hard
vuln_type: crypto_rsa
tags: [Crypto-RSA,dp/dq泄露,PEM解析,PKCSv1.5,Lattice,LLL,LCG,RSAbits]
attack_chain: crypto1: 不完整PEM私钥→搜索0x8181或0x8180分割→完整e,dp,dq爆破k求p,q→d=inverse(e,(p-1)*(q-1))→long_to_bytes(c^d%p*q)得flag+PKCSv1.5填充|crypto2: p,q 512位+e=65537 RSA→n=670位素数+hint序列(38轮LCG: hint[i]=(p*hint[-2]+q*hint[-1]+r)%n)→格密码(LLL)解p,q
key_payload: e=0x10001 dp=0x00e85194...dq=0x6e2edb1b...|for k in range(1,e): if (e*dp-1)%k==0: if isPrime((e*dp-1)//k+1): p=... break|for k in range(1,e): if (e*dq-1)%k==0: if isPrime((e*dq-1)//k+1): q=... break|with open("flag.enc","rb") as f: c=bytes_to_long(f.read()) d=inverse(e,(p-1)*(q-1)) print(long_to_bytes(pow(c,d,p*q)))|n=2923276556393306465975776608715617918820939733635306287316282928405826711944180807129458880976159847005801863680416075330326850146841550985087091569849369045131250588698063717548052968842737338925409099|flag{622808a53003167cf7c391e9ecfd07cf}
one_liner: 2道密码题:crypto1不完整PEM私钥搜8181/8180分割提完整e+dp+dq爆破k求p,q得flag+PKCSv1.5填充;crypto2标准RSA但n=670位+38轮LCG hint(p*h[-2]+q*h[-1]+r)需格密码LLL解p,q
lesson: 1) 不完整PEM私钥base64解码后搜索0x8181(0x81+长度0x81)或0x8180(0x81+长度0x80)分割ASN.1结构提e/dp/dq; 2) 已知e+dp:爆破k∈[1,e),求p=(e*dp-1)//k+1且isPrime(p)即正确; 3) PKCSv1.5填充格式:\x02+填充+\x00+明文,解后提取\x00后内容; 4) 38轮LCG hint若n比p*q大,可用格密码LLL将hint序列作为近似格基底,解p+q或p-q; 5) hint[i] = (p*h[-2] + q*h[-1] + r) mod n是经典Coppersmith变种
quality: high
---

## 备注

原文(https://www.ctfiot.com/191283.html)作者吐槽"赛后拿到题目简单看了一下两道密码题,不是很难。但是给你们看一下茶茶的小肚腩~"。

### 题目详情

**crypto1** — 不完整PEM私钥还原
- 提供pri.pem但内容不完整
- base64解码后得到DER编码:308204a3 02010002 82010100 ... 0203 010001 02 820100 ... 028181 ... 028180 ...
- 搜索0x8181(=0x81, len≥0x80)或0x8180(=0x81, len<0x80)分割ASN.1结构
- 提取完整e=0x10001, dp=0x00e85194c995..., dq=0x6e2edb1b...
- 爆破k∈[1,e)求p=((e*dp-1)//k+1),q类似,要求isPrime
- d=inverse(e, (p-1)*(q-1))
- pow(c, d, p*q)解flag+PKCSv1.5填充
- flag: `flag{622808a53003167cf7c391e9ecfd07cf}`

**crypto2** — 38轮LCG+格密码
- 标准RSA p,q 512位 + e=65537
- n=670位素数(独立)
- hint = [getPrime(670), getPrime(670)] 初始
- 38轮:r=random.getrandbits(600), hint += [(p*hint[-2] + q*hint[-1] + r) % n]
- 输出hint列表+n+c
- 攻击:格密码LLL(因n>512+512,信息泄露足够)

## 评级

- **quality: high** — 2道密码题,crypto1 PEM分割+dp爆破p完整还原;crypto2 LCG hint链格密码LLL
- **vuln_type: crypto_rsa** — RSA为主
- 实战价值:不完整PEM私钥恢复+已知dp/dq爆破p+格密码解LCG hint链是Crypto高阶套路
