# 强网杯2024 solve2-apk-赛题解析

> 原文: https://www.ctfiot.com/222465.html
> ID: 222465

#include 
#include <cstdio>
#include <stdint.h> // For uint32_t
using namespace std;

void tea_decrypt(uint32_t* v) {
 uint32_t v0 = v[0], v1 = v[1], sum = 0xC6EF3720, i;
 uint32_t delta = 0x9e3779b9;
 uint32_t k[5] = { 598323648, 1213115916, 970832168, 274853062};

 for (i = 0; i < 32; i++) {

 v1 -= (((v0 << 4) + k[2] ^ v0) + (sum ^ (v0 >> 5)) + k[3]);
 v0 -= (((v1 << 4) + k[0] ^ v1) + (sum ^ (v1 >> 5)) + k[1]);
 sum -= delta;
 }
 v[0] = v0;
 v[1] = v1;
}

uint32_t switchEndian(uint32_t num) {
 return ((num >> 24) & 0x000000FF) | // 取最高字节
 ((num >> 8) & 0x0000FF00) | // 取第二字节
 ((num << 8) & 0x00FF0000) | // 取第三字节
 ((num << 24) & 0xFF000000); // 取最低字节
}

int main() {
 uint32_t key[] = { 598323648, 1213115916, 970832168, 274853062 };

 uint32_t data[] = {
 0x5E5440B0, 2057046228, 0x4A1ED228, 0x233FE7C, 0x96461450, 0x88A670ED, 0xF79BFC89, 0x20C3D75F,0
 };

 for (int i = 0; i < 8; i += 2) {
 tea_decrypt(&data[i]);
 }

 for (int i = 0; i < 8; ++i) {
 data[i] = switchEndian(data[i]);
 }
 printf("%s",data);

 return 0;
}
// Come on you are about to get it>

/**
 * Use (12, 8) Reed-Solomon code over GF(256) to produce a key S-box
 * 32-bit entity from two key material 32-bit entities.
 *
 * @param k0 1st 32-bit entity.
 * @param k1 2nd 32-bit entity.
 * @return Remainder polynomial generated using RS code
 */
 private static final int RS_MDS_Encode( int k0, int k1) {
 int r = k1;
 for (int i = 0; i < 4; i++) // shift 1 byte at a time
 r = RS_rem( r );
 r ^= k0;
 for (int i = 0; i < 4; i++)
 r = RS_rem( r );
 return r;
 }

import twofish

key = bytes.fromhex("000102030405060708090a0b0c0d0e0f") # key
tf = twofish.Twofish(key)
data1 = bytes([159, 46, 128, 211, 56, 34, 22, 223, 236, 150, 252, 143, 26, 34, 136, 115])
decrypted1 = tf.decrypt(data1)
print(decrypted1)
#flag{iT3N0t7H@tH

data2 = [169, 217, 118, 189, 119, 187, 86, 154, 49, 179, 222, 168, 101, 142, 26, 50]
enc1 = bytes([0xD8, 0xAD, 0x71, 0xC8, 0x76, 0xD3, 0x28, 0xFD, 0x37, 0xEA, 0xA6, 0xF7, 0x3F, 0xEC, 0x1B, 0x32])
enc2 = b'111111111111111}'
dec2 = ''.join(chr(data2[i] ^ enc1[i] ^ enc2[i]) for i in range(len(data2)))
print(dec2)
#@E6D0YOV7hInkS0}

看雪ID：Aar0n

https://bbs.kanxue.com/user-home-985355.htm

*本文为看雪论坛优秀文章，由 Aar0n 原创，转载请注明来自看雪社区

# 往期推荐

1、PWN入门-SROP拜师

2、一种apc注入型的Gamarue病毒的变种

3、野蛮fuzz：提升性能

4、关于安卓注入几种方式的讨论，开源注入模块实现

5、2024年KCTF水泊梁山-反混淆

球分享

球点赞

球在看

点击阅读原文查看更多


```
    #include 
    #include <cstdio>
    #include <stdint.h> // For uint32_t
using namespace std;

void tea_decrypt(uint32_t* v) {
 uint32_t v0 = v[0], v1 = v[1], sum = 0xC6EF3720, i;
 uint32_t delta = 0x9e3779b9;
 uint32_t k[5] = { 598323648, 1213115916, 970832168, 274853062};

 for (i = 0; i < 32; i++) {

 v1 -= (((v0 << 4) + k[2] ^ v0) + (sum ^ (v0 >> 5)) + k[3]);
 v0 -= (((v1 << 4) + k[0] ^ v1) + (sum ^ (v1 >> 5)) + k[1]);
 sum -= delta;
 }
 v[0] = v0;
 v[1] = v1;
}

uint32_t switchEndian(uint32_t num) {
 return ((num >> 24) & 0x000000FF) | // 取最高字节
 ((num >> 8) & 0x0000FF00) | // 取第二字节
 ((num << 8) & 0x00FF0000) | // 取第三字节
 ((num << 24) & 0xFF000000); // 取最低字节
}

int main() {
 uint32_t key[] = { 598323648, 1213115916, 970832168, 274853062 };

 uint32_t data[] = {
 0x5E5440B0, 2057046228, 0x4A1ED228, 0x233FE7C, 0x96461450, 0x88A670ED, 0xF79BFC89, 0x20C3D75F,0
 };

 for (int i = 0; i < 8; i += 2) {
 tea_decrypt(&data[i]);
 }

 for (int i = 0; i < 8; ++i) {
 data[i] = switchEndian(data[i]);
 }
 printf("%s",data);

 return 0;
}
// Come on you are about to get it>
/**
 * Use (12, 8) Reed-Solomon code over GF(256) to produce a key S-box
 * 32-bit entity from two key material 32-bit entities.
 *
 * @param k0 1st 32-bit entity.
 * @param k1 2nd 32-bit entity.
 * @return Remainder polynomial generated using RS code
 */
 private static final int RS_MDS_Encode( int k0, int k1) {
 int r = k1;
 for (int i = 0; i < 4; i++) // shift 1 byte at a time
 r = RS_rem( r );
 r ^= k0;
 for (int i = 0; i < 4; i++)
 r = RS_rem( r );
 return r;
 }
import twofish

key = bytes.fromhex("000102030405060708090a0b0c0d0e0f") # key
tf = twofish.Twofish(key)
data1 = bytes([159, 46, 128, 211, 56, 34, 22, 223, 236, 150, 252, 143, 26, 34, 136, 115])
decrypted1 = tf.decrypt(data1)
print(decrypted1)
    #flag{iT3N0t7H@tH
data2 = [169, 217, 118, 189, 119, 187, 86, 154, 49, 179, 222, 168, 101, 142, 26, 50]
enc1 = bytes([0xD8, 0xAD, 0x71, 0xC8, 0x76, 0xD3, 0x28, 0xFD, 0x37, 0xEA, 0xA6, 0xF7, 0x3F, 0xEC, 0x1B, 0x32])
enc2 = b'111111111111111}'
dec2 = ''.join(chr(data2[i] ^ enc1[i] ^ enc2[i]) for i in range(len(data2)))
print(dec2)
#@E6D0YOV7hInkS0}
```


---
## 附图

![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/1-1736080911.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/4-1736080912.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/2-1736080912.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/10-1736080912.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/2-1736080913.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/1-1736080914.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/1-1736080915.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/0-1736080916.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/8-1736080917.png)
![](https://ctfiot.oss-cn-beijing.aliyuncs.com/uploads/2025/01/0-1736080917.png)