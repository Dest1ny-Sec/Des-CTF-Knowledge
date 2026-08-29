---
title: 从TPCTF 2023学习Python逆向
contest: TPCTF 2023
year: 2023
difficulty: medium
vuln_type: reverse
tags: [Python逆向, AES, Cython, IDA重建, PyObject, big num, HITPCTF, pycdc, maze]
attack_chain:
  - nanoPyEnc: enc 列表 48 字节先 XOR 1 再 AES-ECB 解密 key='2033-05-18_03:33'
  - maze: Cython 编译产物 IDA base=0x44960 重建 PyObject*/PyTypeObject* 数组
  - create_qword + SetType + set_name 还原符号 ys, ns
  - 还原 MazeLang 类 (TWF6ZUxhbmc) 含 add_function/cell/step/get_pos/op/__init__/__repr__
  - 还原 check c29sdmU(SvL6VEBRwx) 比对 33 字节
  - 反变换 aW5pdF9zZWNyZXQ 走 EqdU3uQNCi 33 元素排列置换 c2VjcmV0
  - key='HITPCTF' XOR c2VjcmV0[i] 取后 33 字节
key_payload: 'HITPCTF XOR c2VjcmV0[i] 33 字节解'
one_liner: TPCTF 2023 nanoPyEnc AES-ECB + maze Cython 编译产物 IDA 符号重建。
lesson: Python 字节码逆向先识别编译方式 (CPython .pyc, Cython, PyInstaller, Nuitka)，Cython 编译产物的 PyObject 数组可通过 IDA Python 重建；AES-ECB 短密钥直接字典/已知时间戳爆破。
quality: high
---

# 从TPCTF 2023学习Python逆向

## 概览
- **来源**: ctfiot 149063
- **赛事**: TPCTF 2023 (清华 Redbud × 北大 pkucc 联合命题)
- **难度**: ⭐⭐⭐

## nanoPyEnc
```python
enc = [153, 240, 237, ...]  # 48 字节
enc = bytes([x ^ 1 for x in enc])
key = b'2033-05-18_03:33'
aes = AES.new(key, AES.MODE_ECB)
flag = aes.decrypt(enc)
```

## maze (Cython 编译)
- **.pyx → .pyd/.so 编译产物**: IDA 加载 base=0x44960
- **符号重建**:
  - 135 项 PyObject*/PyTypeObject* 数组
  - 用 `create_qword` + `SetType` + `set_name` (SN_CHECK) 还原 `ys` (类型) + `ns` (名字)
- **类/函数识别**:
  - `MazeLang = TWF6ZUxhbmc(base64.b64decode(UJ9mxXxeoS).decode())`
  - `add_function` / `cell` / `step` / `get_pos` / `op` / `__init__` / `__repr__`
- **反推算法**:
  ```python
  def aW5pdF9zZWNyZXQ():
      for i in range(33):
          c2VjcmV0[EqdU3uQNCi[i]], c2VjcmV0[i] = c2VjcmE0[i], c2VjcmV0[EqdU3uQNCi[i]]
  key = b'HITPCTF'
  aW5pdF9zZWNyZXQ()
  for i in range(33):
      flag.append(key[i%7] ^ c2VjcmV0[i])
  ```
- **关键常量**:
  - `EqdU3uQNCi = [18, 17, 15, 0, 27, 31, 10, 19, 14, 21, 25, 22, 6, 3, 30, 8, 24, 5, 7, 4, 13, 29, 9, 26, 1, 2, 28, 16, 20, 32, 12, 23, 11]`
  - `c2VjcmV0 = [7, 47, 60, 28, 39, 11, 23, 5, 49, 49, 26, 11, 63, 4, 9, 2, 25, 61, 36, 112, 25, 15, 62, 25, 3, 16, 102, 38, 14, 7, 37, 4, 40]`

## 工具
- IDA Pro + IDAPython 脚本批量 set_name
- pycdc / uncompyle6 (Cython 字符串可能恢复)
