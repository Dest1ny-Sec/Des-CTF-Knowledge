---
title: 看雪2022 KCTF 春季赛 | 第八题设计思路及解析
contest: 看雪2022 KCTF春季赛
year: 2022
difficulty: hard
vuln_type: reverse
tags: [ArmVMP, ARM指令虚拟化, ELF保护, ptrace反调试, Frida hook, DES, scanmem, ghidra]
attack_chain: ArmVMP（反汇编器+vmachine+解释器）保护ARM ELF→push/pop/ldr/str/bl/add/mov指令模拟→重定位处理PC相对寻址→dump内存找"顺利通关"→frida hook DES加密→找返回地址0xe409→ghidra强制识别arm代码
key_payload: "ArmVMP vmdata; 44 f0 0d e5指令搜索;frida Interceptor.attach(baseAddr.add(0x4d15));ghidra强制识别arm;DES Enc"
one_liner: KCTF2022春Q8《迷雾散去》ArmVMP保护：ARM指令虚拟化+重定位+ptrace反调试+Frida hook DES
lesson: ArmVMP原理：反汇编+vmachine+解释器；指令模拟需重定位处理PC相对寻址；Frida可绕ptrace
quality: high
---

# 看雪2022 KCTF 春季赛 | 第八题设计思路及解析

**赛事**：看雪2022 KCTF春季赛 Q8《迷雾散去》

**难度**：围观1387人，4支战队成功破解，持续4天

**题目设计（ArmVMP战队）**：
- 安卓平台CrackMe
- 公开序列号示例：
  - name: KCTF, serial: 3432356538383237303738386163323436323438663964343063393831366663
  - name: C8EB85C90E69EDC8, serial: 3638386461396366623135623535353361323862656630656561326334303931
- APK SHA-256: `c8eb85c90e69edc8ee85e7233c6cb91aa633f6ff5dc4882ca3fc3ba45225d8c1`

**ArmVMP保护原理**（类vmprotect技术）：
- 三部分组成：**反汇编器** + **vmachine解释器** + **链接器**
- 反汇编器取汇编指令列表，根据指令类型生成模拟代码
- 模拟指令：push/pop, ldr/str, bl, add, mov 等
- 原始代码替换为 `b 指令` 跳转到模拟代码
- 关键：**重定位**处理PC相对寻址
  - 移动代码后 `R4 = data + (PC+4)` 不等于原值
  - 必须修改data以保证访问正确

**重定位示例**：
```asm
.text:
000016C2 19 4C  LDR R4, =(__stack_chk_guard_ptr - 0x16CC)
000016C4 C3 B0  SUB SP, SP, #0x10C
...
00001728 A0 38 00 00 off_1728 DCD __stack_chk_guard_ptr - 0x16CC
```
- 0x16C2指令读0x1728得0x38A0 → R4
- 0x16C8处 R4 + (PC+4) = 0x38A0 + 0x16CC = 0x4F6C
- 移动到0x6000后：0x38A0 + 0x600A = 0x98AA ≠ 0x4F6C
- 需将0x606C的0x38A0修改为0x4F6C-0x600A = 0x213C

**破解步骤**：
1. 程序用ptrace防止调试（IDA/CE无法用）
2. 用 **scanmem** 读取内存（需自行编译+改部分代码）
3. dump出"顺利通关"附近内存作对比
4. IDA查算法特征发现DES
5. **Frida hook**（输出到文件）：
   ```javascript
   var mylogfile = new File("/data/data/a.b.c/d1.txt", "wb");
   Interceptor.attach(baseAddr.add(0x4d15), {
       onEnter: function(args) {
           var mylog = "DES Enc:" + (this.context).lr.sub(baseAddr) + "\n";
           mylogfile.write(mylog); mylogfile.flush();
       },
       onLeave: function(ret) {
           var mylog = "After DES Enc:" + (this.context).lr.sub(baseAddr) + "\n";
           mylogfile.write(mylog); mylogfile.flush();
       }
   });
   ```
6. 找返回地址0xe409
7. 搜索特征 `44 f0 0d e5`（VMP代码结构）
8. ghidra强制识别arm代码

**质量评估**：高（ArmVMP原理详尽 + Frida hook完整代码 + 重定位算法）
