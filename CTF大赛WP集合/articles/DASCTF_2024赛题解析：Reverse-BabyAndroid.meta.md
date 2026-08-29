---
title: DASCTF 2024 赛题解析：Reverse - BabyAndroid
contest: DASCTF
year: 2024
difficulty: medium
vuln_type: reverse
tags: [android, jni, rc4, custom-hash, aes-ecb, in-memory-dex, dct]
attack_chain:
  - loadData 读 assets/Sex.jpg (RC4 key="DASCTF")
  - InMemoryDexClassLoader 加载 dex
  - 反射 site.qifen.note.ui.Encrypto.encrypt
  - 自定义 hash 派生 AES 16 字节 key
  - AES/ECB/PKCS5Padding 加密
  - native JNI encrypt 走 IDCT
  - DCT 浮点 29 维
  - 逆 IDCT 还原
key_payload: RC4 解 dex + 自定义 hash 派生 AES + IDCT 浮点变换
one_liner: DASCTF 2024 BabyAndroid：Android JNI + RC4 + InMemoryDexClassLoader + AES/ECB + DCT 浮点加密。
lesson: Android 逆向链：assets RC4 → InMemoryDexClassLoader → 反射调用 → 自定义 hash 派生 → AES → native JNI 二次变换。
quality: high
---

DASCTF 2024 逆向题 BabyAndroid 完整 WP，作者 sffool（看雪论坛）。

**第一层：RC4 解 dex**

`loadData(str)` 读 `assets/Sex.jpg` 字节流，用 `rc4Decrypt(key="DASCTF", data)` 还原出 dex 字节。`to_unsigned_bytes(byte_list)` 把有符号字节转无符号，导出 `dump.dex` 用 jadx 看。

**第二层：dex 类 Encrypto**

`customHash(KEY)` 派生 16 字节 AES key：
```java
int[] temp = new int[16];
for (int i = 0; i < input.length(); i++) {
    int charVal = input.charAt(i);
    for (int j = 0; j < 16; j++) {
        temp[j] = ((temp[j] * 31) + charVal) % 251;
    }
}
for (int i2 = 0; i2 < 16; i2++) {
    keyBytes[i2] = (byte) (temp[i2] % 256);
}
```
KEY="DSACTF" → temp[0..15] 派生 16 字节 → SecretKeySpec → AES/ECB/PKCS5Padding 加密 sendInit 文本。

**第三层：NoteActivity$EncryptAndSendTask**

`doInBackground(String...)` 流程：
1. `loadData("Sex.jpg")` RC4 解
2. `InMemoryDexClassLoader(ByteBuffer.wrap(dexData))` 动态加载
3. `classLoader.loadClass("site.qifen.note.ui.Encrypto")` 反射获取类
4. `getMethod("encrypt", String.class)` 反射获取方法
5. `checkMethod.invoke(...)` 触发加密
6. `sendRequest.sendPost("http://yuanshen.com/", "data=" + cipher)`

**第四层：native JNI encrypt**

`sub_15548` 取字符串长度；DCT 变换 `cos((j + 0.5) * (i * π) / N) * v[j]`；`sqrt(1.0/N)` 首项 + `sqrt(2.0/N)` 后续项系数；最后 `to_string(v, "%.f")` 拼接逗号返回。

**还原**

29 维 IDCT 公式：
```python
def idct(dct_data):
    N = len(dct_data)
    result = np.zeros(N)
    for n in range(N):
        sum_value = 0.0
        for k in range(N):
            cos_term = np.cos((k * π * (n + 0.5)) / N)
            if k == 0:
                sum_value += dct_data[k] * np.sqrt(1.0/N) * cos_term
            else:
                sum_value += dct_data[k] * np.sqrt(2.0/N) * cos_term
        result[n] = sum_value
    return result
```

29 个 DCT 系数输入 → IDCT 还原 → `np.rint(...).astype(int)` → chr → flag。
