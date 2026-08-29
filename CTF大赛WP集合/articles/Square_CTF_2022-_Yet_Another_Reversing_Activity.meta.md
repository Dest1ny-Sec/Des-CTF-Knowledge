---
title: Square CTF 2022: Yet Another Reversing Activity
contest: Square CTF
year: 2022
difficulty: medium
vuln_type: reverse
tags: [yara-rules, yara-vm-debug, opcode-trace, op_bitwise_xor, brute-char]
attack_chain:
- yara-4.2.3 源码 ./bootstrap.sh + ./configure --with-debug-verbose=8 + make
- 写 flag.yarc 测试规则匹配 banker pattern
- 跑 ./yara-4.2.3/yara -C flag.yarc test.txt 触发 OP_PUSH_8
- 提取 yr_execute_code 调试日志中所有 PUSH_8 + BITWISE_XOR 对
- chr(95^57)='f' chr(51^95)='l' chr(248^153)='a' chr(83^52)='g' chr(248^131)='{' chr(154^247)='m'
- 写 bruteforce.sh 自动化每次取最后 3 行
- flag{m33t_me_1n_7h3_ar3n4} 渐进输出
key_payload: yara-4.2.3/yara -C flag.yarc test.txt 2>&1 | grep -B2 OP_BITWISE_XOR
one_liner: Square CTF 2022 YARA：自编译 yara --with-debug-verbose=8 跑规则，提取 OP_PUSH_8 + BITWISE_XOR trace 还原 flag。
lesson: 给开源工具加 --with-debug-verbose 选项是 CTF 题目常用的"半源码"逆向入口。
quality: high
---
# Square CTF 2022: Yet Another Reversing Activity

## 思路
- 题目给了一段 YARA 规则 `silent_banker : banker`
- YARA 自身有一个内置 bytecode VM (`yr_execute_code`)

## 自编译带 verbose 调试
```bash
git clone https://github.com/VirusTotal/yara
cd yara-4.2.3
./bootstrap.sh
./build.sh
./configure --with-debug-verbose=8
make
```

## 跑测试
```bash
echo "flag{test}" > test.txt
./yara-4.2.3/yara -C flag.yarc test.txt
```

## 提取 trace
OP_PUSH_8 r1.i=95, r1.i=57, OP_BITWISE_XOR
→ `chr(95^57) = 'f'`

按顺序逐字符爆破：
```bash
get_next() {
    ./yara-4.2.3/yara -C flag.yarc test.txt 2>&1 \
    | grep -B2 OP_BITWISE_XOR: | tail -3 \
    | sed -n 's/.*r1.i=\([0-9]*\).*$/\1/p' | xargs \
    | python -c "x,y=[int(_) for _ in input().split()]; print(chr(x^y), end='')" 2>/dev/null
}
```

## 输出
```
f
fl
fla
flag
flag{
flag{m
flag{m3
...
flag{m33t_me_1n_7h3_ar3n4}
```

## flag
```
flag{m33t_me_1n_7h3_ar3n4}
```

## 关键 insight
- YARA 规则条件编译为字节码执行 (`OP_PUSH_8` / `OP_INT_EQ` / `OP_BITWISE_XOR` / `OP_AND` / `OP_JFALSE` / `OP_MATCH_RULE` / `OP_HALT`)
- `--with-debug-verbose=8` 打印所有 VM opcode 执行
- 字符级可爆破（每次改 test.txt 后重跑）
