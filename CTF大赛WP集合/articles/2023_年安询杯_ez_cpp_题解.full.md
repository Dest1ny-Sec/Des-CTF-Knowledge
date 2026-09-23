---
title: 2023 年安询杯 ez_cpp 题解
contest: 安询杯 2023
year: 2023
difficulty: medium
vuln_type: reverse
tags:
- 数组硬编码
- ROT13
- XOR差分
- 半字节交换
- 爆破
attack_chain:
- 'Enc1: ROT13-like 字符偏移 (v3 > 90 时 +13 否则 -13，v3+13 > 122 时回 -13)'
- 'Enc2: 32 字节查 v6 表 ^=4/9/6 或 +=2/5'
- 'Enc3: arr[i] ^= 1; arr[i] = dec3(arr[i])'
- dec3(a1) 是 8-bit reverse 字节反转
- 给定 arr 数组 32 个 uint（含 32-bit 负数）
- 反向 Enc3 → Enc2 → Enc1 还原明文
key_payload: '''arr[] = {0x22, 0x0FFFFFFA2, 0x72, 0x0FFFFFFE6, 0x52, 0x0FFFFFF8C, ...}'''
one_liner: 32 字节 ROT13 + 查表 XOR/ADD + 半字节反转 三层加密逆向。
lesson: 半字节反转 dec3(v) = ((v>>0)&1)<<7 + ... 是经典 8-bit reverse；查表操作要反向回推。
quality: medium
full_path: 2023_年安询杯_ez_cpp_题解.full.md
meta_path: 2023_年安询杯_ez_cpp_题解.meta.md
images_removed: true
images_removed_count: 0
schema_version: v3.0.0-P0
summary: '2023 年安询杯 ez_cpp 题解。32 字节 ROT13 + 查表 XOR/ADD + 半字节反转 三层加密逆向。。关键路径：Enc1: ROT13-like 字符偏移 (v3 > 90 时 +13 否则 -13，v3+13 > 122 时回 -13) → Enc2: 32 字节查 v6 表 ^=4/9/6 或 +=2/5 → Enc3: arr[i] ^= 1; arr[i] = d...'
category: reverse
subcategory: reverse
time_required: medium
difficulty_score: 3
code_blocks_count: 1
images_count: 0
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/119444.html
reasoning_chain:
- 'cpp reverse: arr[] = {0x22, 0x0FFFFFFA2, 0x72, ...} → 触发点：32 字节密文'
- 假设：32 字节 = 加密 flag → 动作：分析加密逻辑
- 观察：dec3(v) = 半字节反转 (v>>0)&1<<7 + (v>>1)&1<<6 + ... → 触发点：8-bit reverse
- 假设：32 字节 → 先反转 8-bit → 再 xor/加减查表 → 动作：dec3(arr[i])
- 观察：v6[] = {0,1,0,1,0,0,1,0,1,0,1,1,1,1,1,1,0,0,0,0,0,0,1,1,0,1,0,0,1,1,1,0} → 假设：查表异或/加法
- 动作：循环 v6[i] 决定 arr[i] ^= 9 / += 2 / ^= 4 / ^= 6 / += 5
- 观察：还原明文 → flag
failed_attempts:
- 试图用 IDA 反编译 → 失败：内联汇编难读
- 试图直接 ROT13 → 失败：还有 XOR/ADD 层
- 试图暴力 256^32 → 失败：组合太大
key_observations:
- 半字节反转 dec3(v) = ((v>>0)&1)<<7 + ... 是经典 8-bit reverse
- 查表操作要反向回推（xor/加减互逆）
- v6[] 数组索引决定加密方式（按位分支）
- 32 字节密文 + 4 步加密是 cpp reverse 常见结构
prerequisites:
- C++ 反汇编基础（IDA / Ghidra）
- 位运算（XOR / AND / SHIFT）
- 加密算法反向推导
- Python 解密脚本
---
# 2023 年安询杯 ez_cpp 题解

> 原文: https://www.ctfiot.com/119444.html
> ID: 119444


```
// Enc1
 int tmp_result;
 for (int i = 0; i < 32; i++) {
 bool find_v3 = false;
 for (int v3 = 0; v3 < 128; v3++) {
 int result;
 if ((v3 - 61) <= 0x3Eu) {
 result = v3;
 int v7 = v3 + 13;
 if (v3 > 90) {
 if (v7 <= 122)
 tmp_result = v3 + 13;
 else
 tmp_result = v3 - 13;
 } else {
 result = -13;
 if (v7 <= 90)
 result = 13;
 result = v3 + result;
 tmp_result = result;
 }
 }

 if (tmp_result == arr[i] && check(v3)) {
 find_v3 = true;
 cout << (char)v3;
 }
 }
 if (!find_v3) {
 cout << (char)arr[i];
 }
 cout << " ";
 }
    #include 
using namespace std;

unsigned int dec3(unsigned int a1) {
 unsigned int a2 = 8;
 a1--;

 unsigned int v2; // edx
 unsigned int v3; // edi
 unsigned int v4; // ebx

 v2 = 0;
 v3 = 0;
 if (a2 > 0) {
 v4 = a2 - 1;
 do
 v2 |= ((a1 >> v3++) & 1) << v4--;
 while (v3 < a2);
 }
 return v2;
}

unsigned int arr[] = {0x22, 0x0FFFFFFA2, 0x72, 0x0FFFFFFE6,
 0x52, 0x0FFFFFF8C, 0x0FFFFFFF2, 0x0FFFFFFD4,
 0x0FFFFFFA6, 0x0A, 0x3C, 0x24,
 0x0FFFFFFA6, 0x0FFFFFF9C, 0x0FFFFFF86, 0x24,
 0x42, 0x0FFFFFFD4, 0x22, 0x0FFFFFFB6,
 0x14, 0x42, 0x0FFFFFFCE, 0x0FFFFFFAC,
 0x14, 0x6A, 0x2C, 0x7C,
 0x0FFFFFFE4, 0x0FFFFFFE4, 0x0FFFFFFE4, 0x1E};

void dec2(unsigned int *arr) {
 int v6[] = {0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1,
 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0};

 int index = 0;
 unsigned int result;
 do {
 if (index <= 16) {
 if (index >= 16) {
 arr[index] ^= 4;
 } else {
 result = v6[index];
 if (result) {
 if (!--result)
 arr[index] ^= 9;
 } else {
 arr[index] += 2;
 }
 }
 } else {
 result = v6[index];
 if (result) {
 if (!--result)
 arr[index] ^= 6;
 } else {
 arr[index] += 5;
 }
 }
 ++index;
 } while (arr[index]);
}

int check(int c) {
 if ((c >= 'a' && c <= 'z') (c >= 'A' && c <= 'Z')
 (c >= '0' && c <= '9') c == '{' c == '}' || c == '_') {
 return true;
 }
 return false;
}

int main() {
 // Enc3
 for (int i = 0; i < 32; i++) {
 arr[i] ^= 1;
 arr[i] = dec3(arr[i]);
 }

 // Enc2
 dec2(arr);

 // Enc1
 int tmp_result;
 for (int i = 0; i < 32; i++) {
 bool find_v3 = false;
 for (int v3 = 0; v3 < 128; v3++) {
 int result;
 if ((v3 - 61) <= 0x3Eu) {
 result = v3;
 int v7 = v3 + 13;
 if (v3 > 90) {
 if (v7 <= 122)
 tmp_result = v3 + 13;
 else
 tmp_result = v3 - 13;
 } else {
 result = -13;
 if (v7 <= 90)
 result = 13;
 result = v3 + result;
 tmp_result = result;
 }
 }

 if (tmp_result == arr[i] && check(v3)) {
 find_v3 = true;
 cout << (char)v3;
 }
 }
 if (!find_v3) {
 cout << (char)arr[i];
 }
 cout << " ";
 }

 return 0;
}
```
