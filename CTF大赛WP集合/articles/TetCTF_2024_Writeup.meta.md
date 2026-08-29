---
title: TetCTF 2024 Writeup
contest: TetCTF
year: 2024
difficulty: hard
vuln_type: reverse
tags: [webassembly, z3-solver, wasm-decompile, wasm-check, fnv1a-hash, xorshift128, linalg-solve]
attack_chain:
- baby-asm: WASM 二进制 + WebAssembly.Module 加载
- processInput 检查 text.length === 27 + 起始 TetCTF{ + 结束 }
- wasm.init(20) 创 20 元素数组
- wasm.array_fill(arr, i, text.charCodeAt(i+7)) 写入 c+83
- wasm.check() 验证 20 个约束
- 每 4 个一组 (add/sub/mul/xor) + 4 个 global 常量
- globals = [115,82,52,149,136,67,76,97,71,90,71,74,124,104,84,67,114,127,52,31]
- next = [1,2,3,0,5,6,7,4,9,10,11,8,...] 交叉排列
- z3 BitVec 求解 20 个 flag[i+7]
- check_key: 0x54 长度字符串 + 白名单 21 字符 !_acdefghilmnoprstuwy
- 每 4 字符一组 (l << 2) hash_64_fnv1a
- xorshift128 (x=0x75bcd15, y=0x159a55e5, z=0x1f123bb5, w=0xdeadbeef)
- mem2[a] += mem1[b] * (xorshift128() % 0x400)
- unk[0..21] 21 个目标值
- Python: 枚举 21^4 哈希表 + xorshift128 矩阵 + np.linalg.solve 解 21 元一次方程
- 还原 mem1 字典
key_payload: np.linalg.solve(X, B)
one_liner: TetCTF 2024 WebAssembly + check_key：WASM 字节码 Z3 求解 + FNV1a + xorshift128 矩阵求逆。
lesson: WASM 反编译为 WAT 后用 z3 BitVec 求解简单运算链；含 xorshift128 的 21 元一次方程可用 numpy.linalg.solve。
quality: high
---
# TetCTF 2024 Writeup

## 1. baby-asm (WebAssembly)
```javascript
const wasmModule = new WebAssembly.Module(byte_code);
const wasmInstance = new WebAssembly.Instance(wasmModule, {});
const wasm = wasmInstance.exports;

function processInput(text) {
    if (text.startsWith('TetCTF{') && text.endsWith('}') && text.length === 27) {
        let array_size = 20;
        let array_obj = wasm.init(array_size);

        for (var i = 0; i < array_size; i++) {
            wasm.array_fill(array_obj, i, text.charCodeAt(i+7));
        }
        if (wasm.check(array_obj)) {
            p.textContent = '> Correct!';
        } else {
            p.textContent = '> Incorrect!';
        }
    }
}
```

### array_fill + check
```python
def array_fill(arr, i, c):
    arr[i] = c + 83
    return arr

# 5 种运算: add/sub/mul/xor + 4 个 global
globals = [115,82,52,149,136,67,76,97,71,90,71,74,124,104,84,67,114,127,52,31]
next = [1,2,3,0,5,6,7,4,9,10,11,8,13,14,15,12,17,18,19,16]

# check 函数 (WASM 反编译)
# 每 4 个一组, type_num = i % 4
# val = arr[i]
# type 0: arr[next[i]] = (val + g) ^ 32
# type 1: arr[next[i]] = (val - g) ^ 36
# type 2: arr[next[i]] = (val * g) ^ 19
# type 3: arr[next[i]] = (val ^ g) ^ 55
```

### z3 求解
```python
from z3 import *
flag = [BitVec(f"flag[{i}]", 8) for i in range(27)]
s = Solver()
s.add(flag[0] == ord("T"))
# ... 26 == ord("}")
for i in range(7, 26):
    s.add(And((flag[i] >= 0x21), (flag[i] <= 0x7e)))

# 代入 globals + ans 数组
ans = [38793,584,738,38594,63809,647,833,63602,...]
for i in range(20):
    s.add(ans[i] == arr[i])
assert s.check() == sat
```

## 2. check_key (Reverse)
```c
// 字符串长度 0x54 (84 字符)
// 白名单 21 字符: !_acdefghilmnoprstuwy
for (k = 0; k < 0x54; k++) {
    for (m = 0; m < 0x15; m++) {
        if (local_38[m] != param_1[k]) break;
    }
    if (m == 0x14) return 0;
}

// 每 4 字符 hash_64_fnv1a
for (l = 0; l < 0x15; l++) {
    mem1[l] = hash_64_fnv1a(param_1 + (l << 2), 4);
}

// xorshift128
x = 0x75bcd15; y = 0x159a55e5; z = 0x1f123bb5; w = 0xdeadbeef;
for (a = 0; a < 0x15; a++) {
    for (b = 0; b < 0x15; b++) {
        mem2[a] += mem1[b] * (xorshift128() % 0x400);
    }
}
// mem2[0..21] == unk[0..21]
```

### 还原
```python
def hash_64_fnv1a(data):
    fnv_prime = 0x100000001b3
    h = 0xcbf29ce484222325
    for byte in data:
        h = c_int32((h ^ byte) * fnv_prime).value
    return h

hashes = {}
words = "!_acdefghilmnoprstuwy"
for chars in product(words, repeat=4):
    A = ''.join(chars)
    hashes[hash_64_fnv1a(A.encode())] = A

# xorshift128 → 21x21 系数矩阵
X = []
for i in range(0x15):
    X.append([int(math.fmod(xorshift128(), 1024)) for n in range(0x15)])

# 21 元一次方程: A * mem1 = B
A = np.array(X)
B = np.array([c_int64(n).value for n in ans])
solution = np.linalg.solve(A, B)
for s in solution:
    v = c_int64(round(s)).value
    print(hashes[v], end="")
```

## xorshift128 实现
```python
def xorshift128():
    global x, y, z, w
    v1 = ((c_uint32(x<<11).value ^ c_uint32(x).value) >> 8)
    v1 ^= c_uint32(x<<11).value ^ x
    x = y; y = z; z = w
    w ^= c_uint32(w).value >> 19
    w ^= v1
    return c_int32(w).value
```
