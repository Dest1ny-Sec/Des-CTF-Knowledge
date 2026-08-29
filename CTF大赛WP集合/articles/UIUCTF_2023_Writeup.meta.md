---
title: UIUCTF 2023 Writeup
contest: UIUCTF
year: 2023
difficulty: medium
vuln_type: reverse
tags: [custom-vm, vmwhere, stack-vm, byte-swap-reverse, xorshift64, gdb-scripting, sfcta]
attack_chain:
- vmwhere1: 自定义 VM，22 个 opcode (ADD/SUB/AND/OR/XOR/SHL/SHR/READ/PUTCHAR/PUSH/JNEG/JZ/JMP/POP/DUP/REVERSE/SPLIT_BIT/POP_BITS/CALL/UNKNOWN/DEBUG)
- opcode 0xa PUSH imm, 0x8 READ flag byte
- 0x10 REVERSE TOP n 反转栈顶 n 字节
- 0x11 SPLIT BYTE TO 8 BITS, 0x12 POP 8 重组字节
- 24 字节 key XOR 链式: a = k ^ key[i+1]; flag[i] = (a>>4)^a
- key[::-1] 模式找 pattern `\x05\x0f\x0a` 后字节
- ciuctf{ar3_y0u_4_r3al_vm_wh3r3_(gpt_g3n3r4t3d_th1s_f14g)}
- vmwhere2: 更复杂栈机 + 47 字节 key
- 16 进制字符串 hash ('u', 'i', 'u', 'c', 't', 'f', '{') 调 mini-VM
- 每字节 x 计算 SFCTA: result = 0; for bit in 7..0: if (x>>i)&1: result = (result+1)*3; else: result = result*3
- 47 个 key 字符通过 table 反查
- 输入 flag 任意字节返回 PUTCHAR 验证
- gdb python gdb.parse_and_eval("$al") 单字符爆破
key_payload: (a>>4) ^ a  # flag 字符链式 XOR
one_liner: UIUCTF 2023 vmwhere 2 题：自定义字节码 VM + REVERSE TOP N 反转 + 24/47 字节 key 链式 XOR。
lesson: 自研 VM 逆向时先用 Python 写 interpreter 复现 opcode，再分析 flag 校验逻辑。
quality: high
---
# UIUCTF 2023 Writeup

## 1. vmwhere1 - Stack VM Reverse

### 22 个 opcode
```c
case 0: return 0;
case 1: ADD a, b → a+b; sp--;
case 2: SUB a, b → a-b;
case 3: AND a, b;
case 4: OR a, b;
case 5: XOR a, b;
case 6: LSH a, b;
case 7: RSH a, b;
case 8: READ flag byte → push;
case 9: POP + putchar;
case 0xa: PUSH imm; pc += 2;
case 0xb: JNEG (if sp[-1] < 0) pc += offset;
case 0xc: JZ (if sp[-1] == 0) pc += offset;
case 0xd: JMP pc += offset;
case 0xe: POP sp--;
case 0xf: DUP *sp = sp[-1];
case 0x10: REVERSE TOP n (反转栈顶 n);
case 0x11: SPLIT BYTE TO 8 BITS (push 8 个 bit);
case 0x12: POP 8 VALUES, NEW VALUE = LSB of last 8;
case 0x28: DEBUG print state
```

### 攻击
```python
# 找 pattern `\x05\x0f\x0a` 后字节 = key
key = []
with open("program", "rb") as f:
    prog = f.read()
for i in range(3, len(prog)):
    if prog[i-3:i] == b"\x05\x0f\x0a":
        key.append(prog[i])

# 链式 XOR
flag = ""
key = key[::-1]
for i in range(len(key)-1):
    k = key[i]
    a = k ^ key[i+1]
    flag += chr((a>>4)^a)
# ciuctf{ar3_y0u_4_r3al_vm_wh3r3_(gpt_g3n3r4t3d_th1s_f14g)}
```

## 2. vmwhere2 - 复杂 VM + SFCTA hash

### SFCTA 函数
```python
def sfcta(x):
    result = 0
    for i in range(7, -1, -1):
        if (x >> i) & 1:
            result = (result + 1) * 3
        else:
            result = result * 3
        result %= 256
    return result
```

### 解密
```python
key = [0xc6, 0x8b, 0xd9, 0xcf, 0x63, 0x60, 0xd8, 0x7b, ...]  # 47 字节
key = key[::-1]
table = {}
for i in range(0x21, 0xfd):
    cmd = 'echo "{}" | ./a.out | grep 0xb90 | cut -d " " -f 5'.format(chr(i))
    result = subprocess.run(cmd, capture_output=True, shell=True)
    table[result.stdout.decode().replace(",\n", "")] = chr(i)

for k in key:
    print(table[hex(k).replace("0x", "")], end="")
```

### GDB 脚本爆破 (vmwhere1)
```python
import gdb
gdb.execute('file chal')
gdb.execute('b *{}'.format(0x55555555569f))
flag = "uiuctf{" + "A"*150
for i in range(150):
    for j in range(0x21, 0x126):
        flag = flag[:i] + chr(j) + "A"*(30-i)
        with open("in.txt", "w") as f: f.write(flag)
        gdb.execute("run program < in.txt")
        gdb.execute("continue {}".format(51+i))
        res = int(gdb.parse_and_eval("$al"))
        if res == 0:
            print(flag)
            break
```

## 关键洞察
- **REVERSE TOP N** 是关键 opcode，可反转栈内容
- **SPLIT BYTE TO BITS** + **POP 8** 配对使用
- 自定义 VM 逆向时先写 Python interpreter
- 多字节 key 链式 XOR 是常见 flag 校验模式
