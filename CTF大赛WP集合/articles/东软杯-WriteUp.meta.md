---
title: 东软杯-WriteUp
contest: 东软杯 / ChaMd5 Neusoft NSSCTF
year: 2022
difficulty: medium
vuln_type: misc_unknown
tags: [SSTI, Jinja2, 模板上传, 压缩包密码爆破, DH bsgs, AES-ECB, BigInteger素数, signal驱动VM, sigaction]
attack_chain:
  - 题 1: Python Flask 文件上传 + path 模板路径 + .tpl 含 {{system('cat /flag')}}
  - 题 2: ?user=* 通配 SQL 盲注 + ?pass= 密码校验
  - 题 3: 加密压缩包 yasuobao.zip 数字密码爆破
  - 题 4: DH 离散对数 bsgs(G, A, (0, 2^40)) → a=822690494337
  - key = pow(B, a, p) → AES-ECB key 16 字节
  - 题 5: Java BigInteger 素数测试 (Fermat + Miller-Rabin) + getPrime(1024)
  - 题 6 PWN: exit_got=setvbuf_got-1 改 setvbuf 为 0x4011A9 + ret2system
  - 题 7 PWN: pop_rdi + read@got + ret2libc 0x404020
  - 题 8 PWN: list 双向链表 + overwrite idx+libc 泄 + edit atoi_got=system
  - 题 9 RE: signal 驱动 VM sigaction(34-47) + mmap 0x200 共享内存
  - opcode=[17,52,0,42,...] 自定义指令 push/pop/add/sub/xor/call/ret/jmp/jz
  - sub_40144B 一次性注册 14 个信号 handler
  - dump 0x4019c0 opcode 流 + 模拟器反推
key_payload: 'a=bsgs(G,A,(0,2^40))=822690494337 + setvbuf_got-1+0x4011A9 ret2system'
one_liner: 东软杯 8 题混合栈：SSTI 模板上传 + SQL 盲注 + 压缩包爆破 + DH bsgs + Java 素数 + 3 道 PWN + signal 驱动 VM。
lesson: signal 驱动 VM 是 RE 高级形态，sigaction(34-47) 各绑 handler (push/pop/add/sub/xor/call/ret/jmp/jz) + mmap 共享内存 + 主进程通过 kill 给子进程发信号执行指令。
quality: medium
---

# 东软杯-WriteUp

## 概览
- **来源**: ctfiot 15954
- **赛事**: 东软杯 / ChaMd5 Venom 战队
- **难度**: ⭐⭐⭐ (多题混合)

## 题目列表

### Web
1. **SSTI 模板上传**: Python Flask `path=./templates` + `{{system('cat /flag')}}` 写 .tpl
2. **SQL 通配符盲注**: `?user=*` 模糊 + `?pass=husins` 密码校验，"用户查询不唯一" / "密码错误"
3. **加密压缩包**: yasuobao.zip 数字密码递归解压

### Crypto
4. **DH 离散对数 (bsgs)**:
   ```python
   A = 142989488568573584455487421652639325256968267580899511353325709765313839485530879575182195391847106611058986646758739505820350416810754259522949402428485456431884223161690132385605038767582431070875138678612435983425500273038807582069763455994486365993366499478412783220052753597397455113133312907456163112016
   p = 174807157365465092731323561678522236549173502913317875393564963123330281052524687450754910240009920154525635325209526987433833785499384204819179549544106498491589834195860008906875039418684191252537604123129659746721614402346449135195832955793815709136053198207712511838753919608894095907732099313139446299843
   g = 41899070570517490692126143234857256603477072005476801644745865627893958675820606802876173648371028044404957307185876963051595214534530501331532626624926034521316281025445575243636197258111995884364277423716373007329751928366973332463469104730271236078593527144954324116802080620822212777139186990364810367977
   A = Mod(A, p); G = Mod(g, p)
   a = bsgs(G, A, (0, 2^40))  # = 822690494337
   key = long_to_bytes(pow(B, a, p))[:16]
   AES.new(key, AES.MODE_ECB).decrypt(bytes.fromhex("ed5c..."))
   ```

### Java
5. **BigInteger 素数测试**: Fermat + Miller-Rabin + getPrime(1024)

### PWN
6. **exit_got 改 setvbuf_got-1 → ret2system**
7. **pop_rdi + read@got → ret2libc 0x404020**
8. **双向链表 overwrite(0, 3, 3, 0x3b1) + add(0x100) + libc 泄 + atoi_got → system**:
   - `libc_address = a - 88 - 0x3c4b10 - 0x10`
   - `edit(2, 0, libc_address + 0x0453a0)` → atoi_got=system
   - `menu('/bin/sh\x00')` → system("/bin/sh")

### RE - Signal 驱动 VM
9. **sigaction 14 个信号 + mmap 0x200 共享内存**:
   - `sub_40144B` 一次性注册 sigaction(34-47) 绑 sub_400E1D/sub_400E78/... 14 个 handler
   - `vm` 结构: `stack_ptr/data_ptr/vm_rax/vm_rbx/vm_rcx/vm_esp/vm_eip/vm_eflags` (0x16 字节)
   - 指令: 34=push / 35=pop / 36=add rax,rbx / 37=add / 38=sub / 39=sub / 40=xor / 41=test / 42=call / 43=ret / 44=jmp / 45=jz / 46=push data[rcx] / 47=pop data[rcx]
   - opcode=[17,52,0,42,5,16,20,...] 写反汇编器
