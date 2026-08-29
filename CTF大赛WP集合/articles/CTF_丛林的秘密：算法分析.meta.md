---
title: CTF 丛林的秘密：算法分析
contest: 移动安全
year: 2024
difficulty: hard
vuln_type: reverse
tags: [WebAssembly, wasm2c, libgogogo.so mm0导出, Frida hook gogogoJNI.check_key, WebAssembly.instantiate, set_input_flag_len, set_input_flag, check_key, 32x32 矩阵, numpy.linalg.solve, linear algebra]
attack_chain:
  - 安卓 APK 装 WebAssembly, 验证逻辑在 wasm 内
  - libgogogo.so 导出 mm0 函数 (readByteArray 拿 wasm 字节)
  - WebAssembly.instantiate + check_key
  - 32 字符 flag, 32x32 矩阵验证
  - wasm2c /root/Desktop/hex.wasm -o web.c 转 c
  - gcc -c web.c → web.o
  - numpy.array 32x32 矩阵
  - scipy.linalg.solve 解线性方程组
  - 还原 flag
key_payload: 'WebAssembly / wasm2c 转 c / libgogogo.so mm0 35000 字节 / gogogoJNI.check_key 32 字符 / 32x32 矩阵 / numpy.linalg.solve'
one_liner: CTF 丛林的秘密 — 安卓 + WebAssembly 算法分析 + libgogogo.so mm0 导出 wasm 字节 + wasm2c 转 c + 32x32 矩阵 numpy.linalg.solve 还原 flag。
lesson: WebAssembly 是 Android 算法保护新趋势;Frida hook 导出函数 + readByteArray 拿 wasm 字节是标准流程;wasm2c 转 c 后用 numpy 解线性方程组。
quality: high
---

# CTF 丛林的秘密：算法分析

## 速读
安卓 + WebAssembly 算法分析 — wasm2c 转 c + numpy 解线性方程组。

## 步骤

### 1. Frida hook 拿 wasm 字节
```javascript
var module_addr = Module.findBaseAddress("libgogogo.so");
var mm0__addr = Module.findExportByName("libgogogo.so", "mm0");
var get_html = mm0__addr.readByteArray(35000);
```

### 2. wasm2c 转换
```bash
./wasm2c /root/Desktop/hex.wasm -o web.c
gcc -c web.c -o web.o
```

### 3. 矩阵求解
```python
import numpy as np
from scipy.linalg import solve

a = np.array([
    [108, 111, 92, 194, 124, 240, ...],  # 32x32 系数矩阵
    [...],
])  # 32 行 32 列

b = np.array([...])  # 32 个常数项
flag_chars = solve(a, b)  # 解 32 个 ASCII 字符
```

## WebAssembly
```javascript
WebAssembly.compile(new Uint8Array(`00 61 73 6D ...`.trim().split(/[\s\r\n]+/g).map(s => parseInt(s, 16))))
.then(module => new WebAssembly.instantiate(module).then(results => { instance = results; }))
```

## 校验
```javascript
function check_flag() {
    var value = document.getElementById("key_value").value;
    if (value.length != 32) return;
    instance.exports.set_input_flag_len(value.length);
    for (var ii = 0; ii < value.length; ii++) {
        instance.exports.set_input_flag(value[ii].charCodeAt(), ii);
    }
    var ret = instance.exports.check_key();
    if (ret == 1) tips = "Congratulations!";
}
```
