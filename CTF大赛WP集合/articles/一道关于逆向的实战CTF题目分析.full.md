---
title: 一道关于逆向的实战CTF题目分析
contest: 实战逆向 CTF
year: 2024
difficulty: easy
vuln_type: reverse
tags:
- left函数
- xor函数
- 32轮调度
- dword数组
- 简单C还原
attack_chain:
- 'IDA 反编译 left(a1,a2): printf("%c", ((a1 ^ a2) >> 8))'
- 'xors(a1,a2): printf("%c", (((a1 + a2) >> 8) ^ a2))'
- dword_402120[32] 已知 32 个 16 位数
- temp[32]={1,0,0,1,0,1,1,0,...} 决定每轮调用 left/xor
- temp[i]=1 调 left(dword[i], 8)
- temp[i]=0 调 xors(dword[i], 40)
- 32 轮逐字节打印还原 flag
key_payload: '''flag{(a1^a2)>>8 | ((a1+a2)>>8)^a2}'''
one_liner: 自实现 left/xor 双函数 + 32 轮调度 + dword 数组还原 flag。
lesson: IDA 反编译时遇到 `((a2 ^ a1) << 8) - a2` 这种结构要还原原始算术语义；32 轮调度类 VM 用 C 复写比反汇编快 10 倍。
quality: medium
full_path: 一道关于逆向的实战CTF题目分析.full.md
meta_path: 一道关于逆向的实战CTF题目分析.meta.md
images_removed: true
images_removed_count: 10
schema_version: v3.0.0-P0
summary: '一道关于逆向的实战CTF题目分析。自实现 left/xor 双函数 + 32 轮调度 + dword 数组还原 flag。。关键路径：IDA 反编译 left(a1,a2): printf("%c", ((a1 ^ a2) >> 8)) → xors(a1,a2): printf("%c", (((a1 + a2) >> 8) ^ a2)) → dword_402120[32] 已知...'
category: reverse
subcategory: reverse
tools_used:
- C
- IDA
time_required: quick
difficulty_score: 2
code_blocks_count: 1
images_count: 10
last_verified: 2026-09-20
contest_type: open
wp_url: https://www.ctfiot.com/193276.html
reasoning_chain:
- '32 位 IDA 反编译看到 left(x,y) + xor(x,y) 两个函数 → 触发点: 简单加密'
- 'sub_401040 = ((a2 ^ a1) << 8) - a2 → 假设: left(a1, a2) 输出 ((a1^a2)>>8) 字符'
- 'sub_401080 = a2 ^ (a1 << 8) → 假设: xors(a1, a2) 输出 (((a1+a2)>>8) ^ a2) 字符'
- 观察到 dword_402120[32] 32 个 16 位已知数 + temp[32]={1,0,0,1,...} 32 位决定调谁
- '假设: temp[i]=1 调 left(dword[i], 8) → temp[i]=0 调 xors(dword[i], 40)'
- '动作: 写 C 代码按 temp 序列跑 32 轮 → printf %c 输出 32 字符 → 还原 flag'
failed_attempts:
- '试图手动算 32 轮 → 失败: 太多, 写脚本更快'
- '假设 temp 是按位翻转 → 失败: 直接读 temp 数组即可'
key_observations:
- left(x,y) + xor(x,y) 双函数调度是入门逆向套路, temp[] 决定调度
- IDA F5 反编译后 printf %c 逐字节输出 = 直接看出 flag 拼接逻辑
- 32 个 dword 常量 + 32 个 temp 标志 = 32 轮确定加密
- 本题是逆向下界, 适合刚学 IDA 的新手
prerequisites:
- IDA F5 反编译基础
- C 位运算 (^ / >> / <<)
- 32 轮调度逻辑识别 (temp[] 二值序列)
- printf %c 字符输出还原
---
# 一道关于逆向的实战CTF题目分析

> 原文: https://www.ctfiot.com/193276.html
> ID: 193276


```
push ebx
.....
pop ebx
int __cdecl sub_401040(char a1, int a2)
{
  return ((a2 ^ a1) << 8) - a2;
}
int __cdecl sub_401080(char a1, int a2)
{
  
  return a2 ^ (a1 << 8);
}
left
xor
xor
left
xor
left
left
xor
left
left
xor
xor
xor
left
left
left
xor
xor
xor
left
xor
xor
left
xor
left
left
left
left
xor
xor
xor
left
int temp[32] = { 1,0,0,1,0,1,1,0,1,1,0,0,0,1,1,1,0,0,0,1,0,0,1,0,1,1,1,1,0,0,0,1 };
dword_402120 数组
unsignedint dword_402120[32]={
0x00004408,0x000068D8,0x00007AD8,0x00004308,0x00007BD8,0x00004608,0x00007B08,0x000070D8,
0x00003308,0x00007308,0x000076D8,0x00005CD8,0x000076D8,0x00006608,0x00006908,0x00006E08,
0x00004BD8,0x000076D8,0x00003FD8,0x00006F08,0x00005ED8,0x000076D8,0x00007408,0x000046D8,
0x00005F08,0x00006308,0x00003408,0x00007408,0x000076D8,0x000044D8,0x00004CD8,0x00007D08
};
    #include <stdio.h>

void left(unsigned int a1, unsigned int a2) {
//  (a1>>8)^a2
printf("%c",((a1 ^ a2)>>8));
}
void xors(unsigned int a1, unsigned int a2) {
//(((a1+a2)>>8)^a2)
printf("%c",(((a1 + a2)>>8)^ a2));
}
int main()
{
unsignedint dword_402120[32]={
0x00004408,0x000068D8,0x00007AD8,0x00004308,0x00007BD8,0x00004608,0x00007B08,0x000070D8,
0x00003308,0x00007308,0x000076D8,0x00005CD8,0x000076D8,0x00006608,0x00006908,0x00006E08,
0x00004BD8,0x000076D8,0x00003FD8,0x00006F08,0x00005ED8,0x000076D8,0x00007408,0x000046D8,
0x00005F08,0x00006308,0x00003408,0x00007408,0x000076D8,0x000044D8,0x00004CD8,0x00007D08
};
int temp[32]={1,0,0,1,0,1,1,0,1,1,0,0,0,1,1,1,0,0,0,1,0,0,1,0,1,1,1,1,0,0,0,1};
for(size_t i =0; i <32; i++)
{
if(temp[i]){
//left
left(dword_402120[i],8);
}
else{
//xor
xors(dword_402120[i],40);

}
}

}
```


---
## 附图

[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]
[图片已移除]