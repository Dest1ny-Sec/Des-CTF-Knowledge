# NewstarCTF2025-Week1-REVERSE全解wp

> 原文: https://www.ctfiot.com/300688.html
> ID: 300688

NewstarCTF2025也是结束好久了，到现在才发的原因是比较懒，另外就是PicGO抽疯，图片上传不到图床，现在用gitee作图床好多了

最终排名是第三，主方向是逆向，可惜最后有两道没解出来，不然re是全解，后续也会发其他方向的

week1全解

读取输入 Str。

用一个自定义字母表做 Base64 编码：base64_encode(Str, Buf1, strlen(Str))。

把结果和常量串 Buf2 = "T>6uTqOatL39aP!YIqruyv(YBA!8y7ouCa9=" 比较，完全一致就通过。

先对目标串 c 逆向第二步（再 XOR 一次 v5）。

再对结果逆向第一步（根据位置还原原 flag）。


```
Do_Y0u_
```



```
1e_Gam3
```



```
Like_7his_Jig
```



```
part3 = [0xDE, 0xED, 0xDA, 0xF2, 0xDD, 0xD8, 0xD7, 0xD7, 0x00]
v2 = 8
flag_part3 = [x ^ 0xAD for x in part3[:v2]]
print(''.join(map(chr, flag_part3)))
```



```
s@w_puzz
```



```
flag{Do_Y0u_Like_7his_Jigs@w_puzz1e_Gam3}
```



```
aHelloACrqzyB4s db 'HElLo!A=CrQzy-B4S3|is',27h,'waITt1ng&Y0u^{/(>v<)*}GO~256789pPqWXV'
db 'KJNMF',0
```



```
HElLo!A=CrQzy-B4S3|is'waITt1ng&Y0u^{/(>v<)*}GO~256789pPqWXVKJNMF
```



```
def decode_custom_base64(s, alpha):
    idx = {ch: i for i, ch in enumerate(alpha)}
    out = bytearray()
    i = 0
    while i < len(s):
        c0, c1, c2, c3 = s[i:i+4]; i += 4
        a = idx[c0]; b = idx[c1]
        if c2 == '=':
            out.append(((a << 2) | (b >> 4)) & 0xFF)
            break
        c = idx[c2]
        if c3 == '=':
            out += bytes([
                ((a << 2) | (b >> 4)) & 0xFF,
                (((b & 0xF) << 4) | (c >> 2)) & 0xFF,
            ])
            break
        d = idx[c3]
        out += bytes([
            ((a << 2) | (b >> 4)) & 0xFF,
            (((b & 0xF) << 4) | (c >> 2)) & 0xFF,
            (((c & 0x3) << 6) | d) & 0xFF,
        ])
    return bytes(out)

alpha = "HElLo!A=CrQzy-B4S3|is'waITt1ng&Y0u^{/(>v<)*}GO~256789pPqWXVKJNMF"
buf2  = "T>6uTqOatL39aP!YIqruyv(YBA!8y7ouCa9="
print(decode_custom_base64(buf2, alpha).decode())
```



```
flag{Wh4t_a_cra2y_8as3!!!}
```



```
from Crypto.Cipher import AES
import base64
ct = base64.b64decode("cTz2pDhl8fRMfkkJXfqs2t8JBsqLkvQZDLYpWjEtkLE=")
k = b"1145141919810000"
pt = AES.new(k, AES.MODE_ECB).decrypt(ct)
# 去除 PKCS#7 填充
pt = pt[:-pt[-1]]
print(pt.decode())
```



```
flag{@_g00d_st@r7_f0r_ANDROID}
```



```
flag{It3_D3bugG_T11me!_le3_play}
```



```
for ( i = 0; i < v7; ++i )
  if ( i % 3 == 0 )      Str[i] ^= 0x14;
  else if ( i % 3 == 1 ) Str[i] ^= 0x11;
  else                   Str[i] ^= 0x45;
```



```
v5[0]=19; v5[1]=19; v5[2]=81;     // 即 0x13, 0x13, 0x51
for ( j = 0; j < v7; ++j )
  Str[j] ^= v5[j % 3];
```



```
strcpy(Str2, "anu`ym7wKLl$P]v3q%D]lHpi");
if (!strcmp(Str, Str2)) …
```



```
v5 = [19, 19, 81]
c = "anu`ym7wKLl$P]v3q%D]lHpi"
v7 = len(c)

tmp = [ord(c[i]) ^ v5[i % 3] for i in range(v7)]

flag_chars = []
for i in range(v7):
    if i % 3 == 0:
        flag_chars.append(chr(tmp[i] ^ 0x14))
    elif i % 3 == 1:
        flag_chars.append(chr(tmp[i] ^ 0x11))
    else:
        flag_chars.append(chr(tmp[i] ^ 0x45))

flag = "".join(flag_chars)
print(flag)
```



```
flag{y0u_Kn0W_b4s1C_xOr}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1772616992-wxsync-2026-03-463539966b048cfa57066e842904e405.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1772616994-wxsync-2026-03-38730e8b13bd8d6e1ad21295a1a93bb2.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1772616996-wxsync-2026-03-c88f5dee717d16131b1313012b1c120b.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1772616998-wxsync-2026-03-4c7a1e7f857598b1838259c00cfed5af.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1772617000-wxsync-2026-03-00756cc8b1f6d041946bd41c52433f07.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1772617002-wxsync-2026-03-f2ab7192b43fb7b0882981a04428fa20.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1772617003-wxsync-2026-03-ece3f515a87a7098bf9ba7dbb6e84ff6.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1772617005-wxsync-2026-03-8b9ae8d6b74f5def1044e7aa10cda43b.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1772617007-wxsync-2026-03-bb78b3844ee7694c327d26583a4934e0.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2026/03/1772617009-wxsync-2026-03-e8a678e9e4e96b139c4d438835609b40.png)