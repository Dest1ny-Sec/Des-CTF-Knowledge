# 铸网-2025”山东省工业互联网网络安全职业技能竞赛WriteUp（职工组）

> 原文: https://www.ctfiot.com/270057.html
> ID: 270057

点击上方蓝字·关注我们

前言：

比赛题目复现，随便写写wp仅供参考

文章同步CSDN，感谢观看！

csdn主页：https://blog.csdn.net/Aluxian_?type=lately

MISC-安全流量：

Net-A嗦哈解码成功，得到class数据需要反编译

反编译后把数据按顺序拼接得到PK文件头

恢复压缩包打开一眼crc32尝试爆破

得到密码：ICTF_so_Intrest1ng解压得到图片

在使用随波修改高度直接得到flag。

flag{08ca4a8d32bd08b13f260f224a834b75}

Re-寻找序列号：

#!/usr/bin/python
# Write Python 3 code in this online editor and run it.# B64 = "ZYXWVUTSRQPONMLKJIHGFEDCBAzxvtrpnljhfdbywusqomkigeca0123456789#$"# def b64_decode_custom(s):# val = {c:i for i,c in enumerate(B64)}# n=0;bits=0;out=bytearray()
# for ch in s:# n=(n<<6)|val[ch]; bits+=6
# if bits>=8:# bits-=8
# out.append((n>>bits)&0xFF)
# return bytes(out)
# enc = "xGFH5z2#A4VdtPIvlBoX0hFBLXC6h9AdRSrpM8hiXr3RBiLALa9FyiQPtUQHSGhk"# cipher = b64_decode_custom(enc)
# (# print(cipher.hex()))
# import struct
# def to_u32_list_le(b):# n = len(b) // 4
# return list(struct.unpack("<" + "I"*n, b))
# def from_u32_list_le(v):# return struct.pack("<" + "I"*len(v), *v)
# def xxtea_encrypt(v, k):# n = len(v)
# if n < 2:# return v[:]# DELTA = 0x9E3779B9
# z = v[n-1]# y = 0
# s = 0
# rounds = 6 + 52 // n
# while rounds > 0:# s = (s + DELTA) & 0xFFFFFFFF
# e = (s >> 2) & 3
# for p in range(n-1):# y = v[p+1]# mx = (((z>>5) ^ (y<<2)) + ((y>>3) ^ (z<<4))) ^ ((s ^ y) + (k[(p & 3) ^ e] ^ z))
# v[p] = (v[p] + mx) & 0xFFFFFFFF
# z = v[p]# y = v[0]# mx = (((z>>5) ^ (y<<2)) + ((y>>3) ^ (z<<4))) ^ ((s ^ y) + (k[((n-1) & 3) ^ e] ^ z))
# v[n-1] = (v[n-1] + mx) & 0xFFFFFFFF
# z = v[n-1]# rounds -= 1
# return v
# def xxtea_decrypt(v, k):# n = len(v)
# if n < 2:# return v[:]# DELTA = 0x9E3779B9
# rounds = 6 + 52 // n
# s = (rounds * DELTA) & 0xFFFFFFFF
# y = v[0]# while rounds > 0:# e = (s >> 2) & 3
# for p in range(n-1, 0, -1):# z = v[p-1]# mx = (((z>>5) ^ (y<<2)) + ((y>>3) ^ (z<<4))) ^ ((s ^ y) + (k[(p & 3) ^ e] ^ z))
# v[p] = (v[p] - mx) & 0xFFFFFFFF
# y = v[p]# z = v[n-1]# mx = (((z>>5) ^ (y<<2)) + ((y>>3) ^ (z<<4))) ^ ((s ^ y) + (k[(0 & 3) ^ e] ^ z))
# v[0] = (v[0] - mx) & 0xFFFFFFFF
# y = v[0]# s = (s - DELTA) & 0xFFFFFFFF
# rounds -= 1
# return v
# key_bytes = b"abcdef9876543210"# k = list(struct.unpack("<4I", key_bytes))
# cipher = b64_decode_custom(enc)
# v = to_u32_list_le(cipher)
# orig = xxtea_decrypt(v[:], k)
# orig_bytes = from_u32_list_le(orig)
# print(len(orig_bytes), orig_bytes[:16].hex(), orig[-1])
# print(orig_bytes.decode('latin1', errors='ignore')[:48])
# -*- coding: utf-8 -*-# Solve for: everflag{cd00b4953fe9a109148f350427ceddbd}# 同时复刻了题目里的加密管线（XXTEA + 自定义Base64）做校验B64="ZYXWVUTSRQPONMLKJIHGFEDCBAzxvtrpnljhfdbywusqomkigeca0123456789#$"KEY_ASCII= b"abcdef9876543210"TARGET="xGFH5z2#A4VdtPIvlBoX0hFBLXC6h9AdRSrpM8hiXr3RBiLALa9FyiQPtUQHSGhk"FLAG="everflag{cd00b4953fe9a109148f350427ceddbd}"# ---- 下面是题目里 sub_4021F0 的自定义 Base64 编码（索引顺序 v18, v19, i, v21）----defb64_encode_custom_from_function(b: bytes) -> str: out=[] dst= B64 aint=0 n3=0 v22= len(b) idx=0 whilev22: byte= b[idx]; idx +=1; v22 -=1 aint= (aint & ~(0xFF << (8*n3))) | (byte << (8*n3)) n3+=1 ifn3 ==3: v18= (aint &0xFF) >>2 v19= (((aint>>8) &0xFF) >>4) +16*((aint &0xFF) &3) v21= ((aint>>16) &0xFF) &0x3F i_idx= (((aint>>16) &0xFF) >>6) +4*(((aint>>8) &0xFF) &0xF) forval in[v18, v19, i_idx, v21]: out.append(dst[val]) n3 = 0 aint = 0 if n3: v18 = (aint & 0xFF) >> 2 v19 = (((aint>>8)&0xFF) >> 4) + 16*((aint & 0xFF) & 3) v21 = ((aint>>16)&0xFF) & 0x3F i_idx = (((aint>>16)&0xFF) >> 6) + 4*(((aint>>8)&0xFF) & 0xF) order = [v18, v19, i_idx, v21] count= n3 +1 forj in range(count): out.append(dst[order[j]]) for_ in range(4-count): out.append('=') return"".join(out)
# ---- 下面复刻 sub_402AA0 / sub_402980 / sub_402B50 的“正向”加密管线 ----defpack_string_le_with_len(s: bytes): n= len(s) v4= n//4+ (1if n %4else0) words=[0]*v4 for i in range(n): idx = i//4; shift = 8*(i%4) words[idx] = (words[idx] | (s[i] << shift)) & 0xFFFFFFFF words.append(n) # 末尾追加长度（42） return words
def pack_key_le(s: bytes): n = len(s) v4 = n//4 + (1 if n % 4 else 0) words = [0]*v4 for i in range(n): idx = i//4; shift = 8*(i%4) words[idx] = (words[idx] | (s[i] << shift)) & 0xFFFFFFFF return words # 仅打包，不追加长度
def xxtea_encrypt_like_402980(v, key): n = len(v) if n <= 1: return v last = v[n-1] rounds=52//n +6 sumv=0 for_ in range(rounds): sumv= (sumv -0x9E3779B9) &0xFFFFFFFF # 注意：这题是 sum 递减版本 e= (sumv >>2) &3 # p: 0..n-2 forp in range(n-1): y= v[p+1] mx= ((((last <<4) &0xFFFFFFFF) ^ (y >>3)) + ((last >>5) ^ ((y <<2) &0xFFFFFFFF))) mx^= ((sumv ^ y) + (key[(e ^ (p &3))] ^ last)) &0xFFFFFFFF last= (v[p] + mx) &0xFFFFFFFF v[p] = last # 最后一个 y0= v[0] mx= ((((last <<4) &0xFFFFFFFF) ^ (y0 >>3)) + ((last >>5) ^ ((y0 <<2) &0xFFFFFFFF))) mx^= ((sumv ^ y0) + (key[(e ^ ((n-1) &3))] ^ last)) &0xFFFFFFFF last= (v[n-1] + mx) &0xFFFFFFFF v[n-1] = last returnvdefwords_to_bytes_le(words): out= bytearray() forw in words: out+= w.to_bytes(4,"little") returnbytes(out)defencode_pipeline(plain_ascii: str) -> str: v= pack_string_le_with_len(plain_ascii.encode("ascii")) k= pack_key_le(KEY_ASCII) v= xxtea_encrypt_like_402980(v, k) ct_bytes= words_to_bytes_le(v)[:-0] # 跟题里一致，直接4*n 字节 returnb64_encode_custom_from_function(ct_bytes)if__name__ =="__main__": print(FLAG)

需要交流或者培训可以联系小编加群交流！

排版创作不宜如果对你有帮助，可以支持一下小编！

关注我们

欢迎关注鱼影安全社区,专注CTF,职业技能大赛中高职技能培训,金砖企业赛,世界技能大赛省选拔赛,企业赛,行业赛,电子取证和CTF系列培训。

鱼影安全团队招人啦,有感兴趣的师傅可以私信我

需要学习数据安全管理员和CTF安全培训,可以联系小编


```
flag{08ca4a8d32bd08b13f260f224a834b75}
#!/usr/bin/python
# Write Python 3 code in this online editor and run it.# B64 = "ZYXWVUTSRQPONMLKJIHGFEDCBAzxvtrpnljhfdbywusqomkigeca0123456789#$"# def b64_decode_custom(s):# val = {c:i for i,c in enumerate(B64)}# n=0;bits=0;out=bytearray()
# for ch in s:# n=(n<<6)|val[ch]; bits+=6
# if bits>=8:# bits-=8
# out.append((n>>bits)&0xFF)
# return bytes(out)
# enc = "xGFH5z2#A4VdtPIvlBoX0hFBLXC6h9AdRSrpM8hiXr3RBiLALa9FyiQPtUQHSGhk"# cipher = b64_decode_custom(enc)
# (# print(cipher.hex()))
# import struct
# def to_u32_list_le(b):# n = len(b) // 4
# return list(struct.unpack("<" + "I"*n, b))
# def from_u32_list_le(v):# return struct.pack("<" + "I"*len(v), *v)
# def xxtea_encrypt(v, k):# n = len(v)
# if n < 2:# return v[:]# DELTA = 0x9E3779B9
# z = v[n-1]# y = 0
# s = 0
# rounds = 6 + 52 // n
# while rounds > 0:# s = (s + DELTA) & 0xFFFFFFFF
# e = (s >> 2) & 3
# for p in range(n-1):# y = v[p+1]# mx = (((z>>5) ^ (y<<2)) + ((y>>3) ^ (z<<4))) ^ ((s ^ y) + (k[(p & 3) ^ e] ^ z))
# v[p] = (v[p] + mx) & 0xFFFFFFFF
# z = v[p]# y = v[0]# mx = (((z>>5) ^ (y<<2)) + ((y>>3) ^ (z<<4))) ^ ((s ^ y) + (k[((n-1) & 3) ^ e] ^ z))
# v[n-1] = (v[n-1] + mx) & 0xFFFFFFFF
# z = v[n-1]# rounds -= 1
# return v
# def xxtea_decrypt(v, k):# n = len(v)
# if n < 2:# return v[:]# DELTA = 0x9E3779B9
# rounds = 6 + 52 // n
# s = (rounds * DELTA) & 0xFFFFFFFF
# y = v[0]# while rounds > 0:# e = (s >> 2) & 3
# for p in range(n-1, 0, -1):# z = v[p-1]# mx = (((z>>5) ^ (y<<2)) + ((y>>3) ^ (z<<4))) ^ ((s ^ y) + (k[(p & 3) ^ e] ^ z))
# v[p] = (v[p] - mx) & 0xFFFFFFFF
# y = v[p]# z = v[n-1]# mx = (((z>>5) ^ (y<<2)) + ((y>>3) ^ (z<<4))) ^ ((s ^ y) + (k[(0 & 3) ^ e] ^ z))
# v[0] = (v[0] - mx) & 0xFFFFFFFF
# y = v[0]# s = (s - DELTA) & 0xFFFFFFFF
# rounds -= 1
# return v
# key_bytes = b"abcdef9876543210"# k = list(struct.unpack("<4I", key_bytes))
# cipher = b64_decode_custom(enc)
# v = to_u32_list_le(cipher)
# orig = xxtea_decrypt(v[:], k)
# orig_bytes = from_u32_list_le(orig)
# print(len(orig_bytes), orig_bytes[:16].hex(), orig[-1])
# print(orig_bytes.decode('latin1', errors='ignore')[:48])
# -*- coding: utf-8 -*-# Solve for: everflag{cd00b4953fe9a109148f350427ceddbd}# 同时复刻了题目里的加密管线（XXTEA + 自定义Base64）做校验B64="ZYXWVUTSRQPONMLKJIHGFEDCBAzxvtrpnljhfdbywusqomkigeca0123456789#$"KEY_ASCII= b"abcdef9876543210"TARGET="xGFH5z2#A4VdtPIvlBoX0hFBLXC6h9AdRSrpM8hiXr3RBiLALa9FyiQPtUQHSGhk"FLAG="everflag{cd00b4953fe9a109148f350427ceddbd}"# ---- 下面是题目里 sub_4021F0 的自定义 Base64 编码（索引顺序 v18, v19, i, v21）----defb64_encode_custom_from_function(b: bytes) -> str: out=[] dst= B64 aint=0 n3=0 v22= len(b) idx=0 whilev22: byte= b[idx]; idx +=1; v22 -=1 aint= (aint & ~(0xFF << (8*n3))) | (byte << (8*n3)) n3+=1 ifn3 ==3: v18= (aint &0xFF) >>2 v19= (((aint>>8) &0xFF) >>4) +16*((aint &0xFF) &3) v21= ((aint>>16) &0xFF) &0x3F i_idx= (((aint>>16) &0xFF) >>6) +4*(((aint>>8) &0xFF) &0xF) forval in[v18, v19, i_idx, v21]: out.append(dst[val]) n3 = 0 aint = 0 if n3: v18 = (aint & 0xFF) >> 2 v19 = (((aint>>8)&0xFF) >> 4) + 16*((aint & 0xFF) & 3) v21 = ((aint>>16)&0xFF) & 0x3F i_idx = (((aint>>16)&0xFF) >> 6) + 4*(((aint>>8)&0xFF) & 0xF) order = [v18, v19, i_idx, v21] count= n3 +1 forj in range(count): out.append(dst[order[j]]) for_ in range(4-count): out.append('=') return"".join(out)
# ---- 下面复刻 sub_402AA0 / sub_402980 / sub_402B50 的“正向”加密管线 ----defpack_string_le_with_len(s: bytes): n= len(s) v4= n//4+ (1if n %4else0) words=[0]*v4 for i in range(n): idx = i//4; shift = 8*(i%4) words[idx] = (words[idx] | (s[i] << shift)) & 0xFFFFFFFF words.append(n) # 末尾追加长度（42） return words
def pack_key_le(s: bytes): n = len(s) v4 = n//4 + (1 if n % 4 else 0) words = [0]*v4 for i in range(n): idx = i//4; shift = 8*(i%4) words[idx] = (words[idx] | (s[i] << shift)) & 0xFFFFFFFF return words # 仅打包，不追加长度
def xxtea_encrypt_like_402980(v, key): n = len(v) if n <= 1: return v last = v[n-1] rounds=52//n +6 sumv=0 for_ in range(rounds): sumv= (sumv -0x9E3779B9) &0xFFFFFFFF # 注意：这题是 sum 递减版本 e= (sumv >>2) &3 # p: 0..n-2 forp in range(n-1): y= v[p+1] mx= ((((last <<4) &0xFFFFFFFF) ^ (y >>3)) + ((last >>5) ^ ((y <<2) &0xFFFFFFFF))) mx^= ((sumv ^ y) + (key[(e ^ (p &3))] ^ last)) &0xFFFFFFFF last= (v[p] + mx) &0xFFFFFFFF v[p] = last # 最后一个 y0= v[0] mx= ((((last <<4) &0xFFFFFFFF) ^ (y0 >>3)) + ((last >>5) ^ ((y0 <<2) &0xFFFFFFFF))) mx^= ((sumv ^ y0) + (key[(e ^ ((n-1) &3))] ^ last)) &0xFFFFFFFF last= (v[n-1] + mx) &0xFFFFFFFF v[n-1] = last returnvdefwords_to_bytes_le(words): out= bytearray() forw in words: out+= w.to_bytes(4,"little") returnbytes(out)defencode_pipeline(plain_ascii: str) -> str: v= pack_string_le_with_len(plain_ascii.encode("ascii")) k= pack_key_le(KEY_ASCII) v= xxtea_encrypt_like_402980(v, k) ct_bytes= words_to_bytes_le(v)[:-0] # 跟题里一致，直接4*n 字节 returnb64_encode_custom_from_function(ct_bytes)if__name__ =="__main__": print(FLAG)
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757570066-wxsync-2025-09-f4dd000cea4bf9f74ed932731079694c.gif)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757570067-wxsync-2025-09-a8f45598cf1a3d1d063fee7dc3b7301b.webp)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757570069-wxsync-2025-09-146d24bf47861641d0e042f41d247583.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757570071-wxsync-2025-09-2033ba071daabab3011556f6d490afaa.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757570073-wxsync-2025-09-f472ac91342bc69d7d687a3cb78b8189.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757570075-wxsync-2025-09-4f93782a6a82f695ce9a7b939872032e.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757570076-wxsync-2025-09-b9ecca3642851f9b7f456c2d0bd122e5.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757570078-wxsync-2025-09-6a0a62f8b32e487aa261a615c5dd8418.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757570080-wxsync-2025-09-b49528d1ebbb3312ee29f07c9987ca00.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/09/1757570082-wxsync-2025-09-9cc51a4c8c2c3d225dbdb2663b964cd1.png)