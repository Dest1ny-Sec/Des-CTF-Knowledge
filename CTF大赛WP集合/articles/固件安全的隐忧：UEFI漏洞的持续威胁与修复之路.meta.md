---
title: 固件安全的隐忧：UEFI漏洞的持续威胁与修复之路
contest: Binarly UEFI 漏洞研究
year: 2025
difficulty: hard
vuln_type: misc_unknown
tags: [Binarly, UEFI固件, AMI UsbRt, SMM漏洞, CVE-2022-24419, CVE-2022-24420, CVE-2022-24421, SMM_Code_Chk_En, ROP链, FwHunt]
attack_chain:
  - Binarly 团队 1 年披露 42 个高严重性 UEFI 漏洞
  - AMI UsbRt (INTEL-SA-00057) 7 年漏洞仍未修复
  - gUsbData 结构 30+ 字段，代码复杂难维护
  - CVE-2017-5721 → CVE-2020-12301 CRC32 欺骗绕过
  - ValidateUsbData() CRC32 校验可被 CRC32 强制攻击绕过
  - CVE-2020-12301 利用：控制 struct_ptr + gUsbData
  - SMM_Code_Chk_En 缓解 (Intel Kabylake+)
  - SMM 公开 ROP 链: SetJump 抓寄存器 + CopyMem 链
  - 戴尔 3 个新 UsbRt 变种 (BRLY-2021-043/045, BRLY-2022-004)
  - 戴尔 DSA-2022-053 三个月响应
  - Binarly FwHunt + LVFS 协作大规模检测
key_payload: 'AMI UsbRt gUsbData 30+ 字段 + CRC32 欺骗 + SMM ROP 链 + FwHunt 检测'
one_liner: Binarly UEFI 固件安全研究：AMI UsbRt 7 年漏洞未修复 + CRC32 欺骗 + SMM ROP 链 + FwHunt 大规模检测。
lesson: AMI UsbRt 是 7 年老漏洞 (gUsbData 30+ 字段), CRC32 验证可被欺骗绕过, SMM_Code_Chk_En 仅 Kabylake+ 支持, ROP 链利用 SMM 是核心攻击面。
quality: high
---

# 固件安全的隐忧：UEFI漏洞的持续威胁与修复之路

## 概览
- **来源**: ctfiot 237369
- **类型**: Binarly UEFI 漏洞研究
- **难度**: ⭐⭐⭐⭐

## Binarly 团队成果
- 1 年披露 42 个高严重性 UEFI 漏洞
- 全部可导致 SMM 任意代码执行
- 戴尔 DSA-2022-053 三个月响应

## AMI UsbRt 漏洞 (INTEL-SA-00057)
- **年龄**: 7 年 (2016 Aptiocalypsis)
- **状态**: 至今未修复，影响联想/戴尔/Star Labs
- **根因**: gUsbData 结构 30+ 字段，代码复杂难维护
- **变异链**:
  - CVE-2017-5721: UsbRt API 复杂
  - CVE-2020-12301: CRC32 欺骗绕过 ValidateUsbData()
  - CVE-2022-24419/20/21: 戴尔 3 个新变种 (BRLY-2021-043/045, BRLY-2022-004)

## 攻击步骤 (CVE-2020-12301)
1. 控制 struct_ptr 指针
2. 控制 gUsbData (绕过 CRC32 验证)
3. 调用任意函数 + 传参

## SMM_Code_Chk_En 缓解
- Intel Kabylake+ 支持
- 阻止 SMRAM 外代码执行
- chipsec 工具检查 MSR_SMM_FEATURE_CONTROL

## 公开 ROP 利用 (Synactiv BrunoPujos)
- SetJump gadget: 抓寄存器值
- `mov ecx, 0xe8; mov rax, rdx; jmp qword ptr [rcx+0x48]`
- ROP 链: R8 长度 + RCX/RDX 源/目标 + CopyMem 调用
- ropper 找 gadget: `ropper -a x86_64 -f UsbRtSmm –search "mov rdx" –detail`
- Intel Chipsec PoC 代码开源于 Binarly GitHub

## 戴尔 BRLY-2022-004 利用
- Struct 指针被攻击者控制
- 无 SMRAM 重叠检查 → 任意写
- FuncIndex==15 调用偏移 0x30D8 函数
- gCoreProcTable[9]=[10]=[11]=0 → 任意代码执行

## 工具链
- FwHunt: https://github.com/binarly-io/FwHunt
- LVFS: https://fwupd.org/
- Chipsec: https://github.com/chipsec/chipsec
- Ropper: https://github.com/sashs/Ropper

## 教学
- UEFI 固件 30+ 字段的复杂结构 = 漏洞温床
- CRC32 验证可被强制攻击绕过
- SMM 任意代码执行是终极攻击面
- Binarly FwHunt + LVFS 是行业协作检测机制
