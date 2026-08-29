---
title: 由SUCTF一血题SU_Harmony初探鸿蒙应用安全分析
contest: SUCTF 2024
year: 2024
difficulty: medium
vuln_type: reverse
tags: [鸿蒙HAP, ArkTS, modules.abc, abc-decompiler, libentry.so, 大整数运算, z3求解]
attack_chain: HAP包unzip解压→abc-decompiler反编译modules.abc→找TextInput onSubmit事件→check函数入口→IDA分析libentry.so垃圾代码→sub_57B0大整数运算链sub_62F0/6D20/8270/9890/A8F0/C160→z3解(input^2+2*input-3)//2=array
key_payload: "abc-decompiler;modules.abc;libentry.so;sub_62F0/6D20/8270/9890/A8F0/C160大整数加/减/乘/除2;z3 ToInt;array=[b'999272289930604998',...,b'2213954953857181622']"
one_liner: SUCTF 2024 SU_Harmony：鸿蒙HAP包逆向+abc-decompiler+大整数运算链+z3解
lesson: 鸿蒙HAP = Zip结构，逆向modules.abc (ArkTS) + libentry.so (NAPI)；大整数反转+加减乘除2混合运算
quality: high
---

# 由SUCTF一血题SU_Harmony初探鸿蒙应用安全分析

**赛事**：SUCTF 2024 SU_Harmony（一血）

**HAP包结构**：
- HAP（Harmony Ability Package）：应用安装运行基本单元
- 类型：entry（主模块）/ feature（动态特性模块）
- 本题：`entry-default-unsigned.hap`（default模式编译）
- 实际为Zip格式，unzip解压
- 关键路径：`./ets/modules.abc`（ArkTS源码编译结果）+ `./libs/`（动态库）

**modules.abc逆向**：
- 工具：abc-decompiler（基于jadx开发，GitHub: ohos-decompiler/abc-decompiler）
- 关注 main包/pages目录
- 找TextInput onSubmit事件 → handleInput → 调 libentry.so check

**libentry.so逆向**：
- NAPI函数：napi_get_value_string_utf8（必须返回napi_ok=0）
- 输入长度校验：32字符
- 32字符 → 8个uint（每4字符合并为uint）
- 对每uint调 sub_57B0 进行大整数运算

**sub_57B0大整数运算链**：
- sub_62F0：uint转大整数字符串
- sub_CC10：大整数字符串反转
- sub_6D20：大整数乘法 a1*a2
- sub_8270：大整数*整数 a1*a2 (a2<10)
- sub_9890：大整数加法 a1+a2
- sub_A8F0：大整数减法 a1-a2
- sub_C160：大整数整除2 a1//2

**检查逻辑**：
```python
# (input_uint ** 2 + input_uint * 2 - 3) // 2 == array
rslt0 = str(input_uint)
rslt1 = rslt0 * rslt0
rslt2 = rslt0 * 2
rslt3 = rslt1 + rslt2
rslt4 = rslt3 - 3
rslt5 = rslt4 // 2
```

**z3求解**：
```python
from z3 import *
array = [b'999272289930604998', b'1332475531266467542', ..., b'2213954953857181622']
s = Solver()
v = [Int(f"v{i}") for i in range(8)]
for i in range(8):
    get = ToInt(v[i]**2 + 2*v[i] - 3)
    s.add(v[i] > 0)
    s.add(Or(
        And(get % 2 == 1, (get - 1) / 2 == int(array[i])),
        And(get % 2 == 0, get / 2 == int(array[i]))
    ))
flag = b''
if s.check() == sat:
    m = s.model()
    for i in range(8):
        flag += m[v[i]].as_long().to_bytes(4, 'little')
print(flag)
# b'SUCTF{Ma7h_WorldIs_S0_B3aut1ful}'
```

**质量评估**：高（完整大整数运算链 + z3脚本 + flag）
