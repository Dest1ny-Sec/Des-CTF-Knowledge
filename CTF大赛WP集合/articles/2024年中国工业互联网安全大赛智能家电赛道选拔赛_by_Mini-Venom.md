# 2024年中国工业互联网安全大赛智能家电赛道选拔赛 by Mini-Venom

> 原文: https://www.ctfiot.com/193342.html
> ID: 193342

招新小广告CTF组诚招re、crypto、pwn、misc、合约方向的师傅,长期招新IOT+Car+工控+样本分析多个组招人有意向的师傅请联系邮箱

admin@chamd5.org(带上简历和想加入的小组)

结束

招新小广告

ChaMd5 Venom 招收大佬入圈

新成立组IOT+工控+样本分析 长期招新

欢迎联系admin@chamd5.org


```
import rsa

def rsaencode(m):
    # 生成RSA密钥对
    (pubkey, privkey) = rsa.newkeys(256)
    # 获取公钥和私钥参数
    n = pubkey.n
    print(n)
    e = pubkey.e
    print(e)
    c = rsa.encrypt(m, pubkey)
    return c

def add_one_to_ascii(data):
    result = bytearray()
    for byte in data:
        result.append(byte + 1)
    return bytes(result)

def xor_bytes(data, key):
    result = bytearray()
    for byte in data:
        result.append(byte ^ key)
    return bytes(result)

if __name__ == '__main__':
    # 使用公钥进行加密
    m=xor_bytes(add_one_to_ascii(x),12)
    c=rsaencode(m)
    print("加密后的密文:", c.hex())

#output
71484438965393396388835335667806052411397994375702758854090697767967524655627
65537
加密后的密文:0x515b50d7407f4f321ddea14d0d99e4134c285ee6b7b92b77f3ed65f32212a529
```



```
import rsa

def rsa_decode(c, pubkey):
    # 从公钥生成对应的私钥
    privkey = rsa.PrivateKey(pubkey.n, pubkey.e, pubkey.d, pubkey.p, pubkey.q)
    m = rsa.decrypt(c, privkey)
    return m

def subtract_one_from_ascii(data):
    result = bytearray()
    for byte in data:
        result.append(byte - 1)
    return bytes(result)

def xor_bytes(data, key):
    result = bytearray()
    for byte in data:
        result.append(byte ^ key)
    return bytes(result)

# RSA 公钥参数
n = 71484438965393396388835335667806052411397994375702758854090697767967524655627
e = 65537

# 加密后的密文 (已转换为字节)
ciphertext = bytes.fromhex('515b50d7407f4f321ddea14d0d99e4134c285ee6b7b92b77f3ed65f32212a529')

# 创建公钥对象
pubkey = rsa.PublicKey(n, e)

p = 895534711824738922785094048763390663
q = 79823191688166851259736970548355545692829
d = 19619308233067290551077729872542647104506154812668367156272584280826183049209
privkey = rsa.PrivateKey(n, e, d, p, q)

# 解密得到加密前的数据
decoded_data = rsa.decrypt(ciphertext, privkey)

# 逆向处理数据
decoded_data = xor_bytes(decoded_data, 12)
original_data = subtract_one_from_ascii(decoded_data)

print("解密后的原始明文:", original_data)
```



```
cd "/var/www/html";echo ZmxhZ3szOTA4NEVFRjJEMjhFOTQxRjUzRTRBMUFBMUZBNjc2Nn0K|base64 -d > ./flag.txt;echo cc6288cd;pwd;echo 2ddc1cfd81
```



```
504b0304140001000000fb81e158591948f02000000014000000080000006d7174742e7478741b14fe05d941726530b707cce78a2bd8639d2ce0fdb7ce63270fe005a5f130ed504b01023f00140001000000fb81e158591948f020000000140000000800240000000000000020000000000000006d7174742e7478740a0020000000000001001800604005e48ecbda0100000000000000000000000000000000504b050600000000010001005a000000460000000000
```



```
modbus.reference_num >= 212
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/4-1721002529.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/9-1721002530.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/1-1721002530.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/7-1721002532.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/1-1721002533.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/5-1721002534.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/8-1721002535.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/3-1721002536.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/2-1721002536.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2024/07/7-1721002537.png)