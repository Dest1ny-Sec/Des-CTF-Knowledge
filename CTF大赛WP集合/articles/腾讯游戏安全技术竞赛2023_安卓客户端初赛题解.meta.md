---
title: 腾讯游戏安全技术竞赛2023 安卓客户端初赛题解
contest: 腾讯游戏安全技术竞赛 2023 安卓客户端初赛
year: 2023
difficulty: hard
vuln_type: reverse
tags: [frida-bypass, libsec2023, libil2cpp-dump, IL2CPPDumper, BlackObfuscator, XTEA-encrypt, VM-decompile, Unicorn-emulate, smali-analysis, frida-dlopen-hook]
attack_chain:
- 修改frida源码:re.frida_server字符串+port 27042→其他+so特征字符串
- 用修改版frida hook dlopen(避开libsec2023.so检测)
- 加载libil2cpp.so后从内存dump解密版
- 010editor比对apk中的so和dump的so,补全重定位表
- IL2CPPDumper恢复符号和结构体
- patch CollectCoin函数0x465674自增逻辑为每次+1000金币
- 第一处加密:XTEA key={0x7B777C63, 0xC56F6BF2, 0x2B670130, 0x76ABD7FE}
- 第二处加密:VM实现(21个方法,栈/操作码/handler)
- 去除libsec2023.so混淆(寄存器跳转+常数+偏移)
- 第三处加密+第四处加密:Sec2023.Encrypt(BlackObfuscator dex)
- frida-dump运行时dump libsec2023.so
- 输出VM指令为C代码,用register关键字优化
key_payload: XTEA key + BlackObfuscator dex + VM decompile
one_liner: 腾讯游戏安全技术竞赛2023安卓客户端初赛题解,frida源码bypass+IL2CPPDumper恢复符号+patch金币自增+四层加密(XTEA+VM+混淆去除+BlackObfuscator dex)注册机。
lesson: 安卓游戏安全三大挑战:frida bypass(改re.frida_server字符串)+il2cpp符号恢复(IL2CPPDumper)+多层加密(XTEA+VM+混淆壳+dex BlackObfuscator)。
quality: high
---

## 题目列表

1道安卓客户端:四层加密注册机

## 关键考点

### Frida Bypass
- 修改frida源码:
  - /server/server.vala 中 re.frida_server 改其他字符串
  - src/linux/linux-host-session.vala 中 so文件特征字符串更改
- 用27042之外的端口启动
- 仍然检测到hook libsec2023.so,但hook其他库没问题
- 选择hook dlopen加载libil2cpp.so时dump

### dump libil2cpp.so
- 写Memory到/data/data/com.com.sec2023.../files/
- mkdir + chmod 0x1FF + fopen wb + fwrite + fclose
- 通过dlopen onLeave触发DumpIL2CPP
- 010editor比对apk中的so和dump的so,补全重定位表

### IL2CPPDumper
- 恢复符号和结构体
- dump.cs搜索金币相关方法+字段
- CollectCoin函数自增逻辑

### patch金币
- frida patch 0x465674汇编改为增加1000
- `Memory.protect(insn, 4, 'rwx')` + `insn.writeByteArray([0x01, 0xA0, 0x0F, 0x11])`
- 重新启动游戏,吃几粒金币即可获取flag

### 第一处加密:XTEA
```c
uint32_t key[4] = {0x7B777C63, 0xC56F6BF2, 0x2B670130, 0x76ABD7FE};
void EncryptXTEA(uint32_t *msg, uint32_t *key, ssize_t round) {
    uint32_t v0 = msg[0], v1 = msg[1];
    uint32_t delta = DELTA, sum = 0xBEEFBEEF;
    for (ssize_t idx = 0; idx < round; idx++) {
        v0 += (((v1 << 7) ^ (v1 >> 8)) + v1) ^ (sum - key[sum & 3]);
        sum += delta;
        v1 += (((v0 << 8) ^ (v0 >> 7)) - v0) ^ (sum + key[(sum >> 13) & 3]);
    }
}
```
- delta = DELTA, sum起始=0xBEEFBEEF(非标准0)
- v0/v1:((v1<<7)^(v1>>8))+v1) ^ (sum - key[sum&3])
- v1:((v0<<8)^(v0>>7))-v0) ^ (sum + key[(sum>>13)&3])

### 第二处加密:VM
- 21个方法,除构造方法外均为VM handler
- hook所有handler输出执行的指令
- 输出为C代码,用register关键字把栈处理为寄存器变量
- 通过opcode取出的值处理为常量
- 重新编译得到精简的加密算法

### libsec2023.so混淆
- 分支跳转指令用寄存器寻址
- 寄存器跳转地址 = 常数 + 偏移
- 常数和取偏移的基址在函数内固定
- 跳转前用条件选择指令获取偏移
- 用Unicorn模拟执行+IDAPython修改汇编+手动改
- 去除混淆后可找到第三、四处加密

### 第三、四处加密
- 第三处:直接分析
- 第四处:Sec2023.Encrypt方法(由壳加载,JADX/JEB无法直接分析)
- frida-dump运行时dump libsec2023.so
- BlackObfuscator dex中找到该方法
- 复制所有真实指令+结合第三处加密+frida观察加密结果

## 实战价值
- 安卓游戏安全三大挑战:frida bypass+il2cpp符号恢复+多层加密
- 修改frida源码字符串是bypass基本功
- IL2CPPDumper是Unity游戏逆向必备工具
- XTEA魔改(sum起始值+位移量)是密码学逆向常见考点
- VM加密可通过frida hook所有handler输出指令再编译
- BlackObfuscator是高级dex混淆,需要frida-dump+真指令分析
