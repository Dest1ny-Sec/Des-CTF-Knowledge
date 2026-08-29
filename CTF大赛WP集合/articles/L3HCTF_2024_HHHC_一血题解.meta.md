---
title: L3HCTF 2024 HHHC 一血题解 (H3C MSR3610 路由器 PPPoE)
contest: L3HCTF
year: 2024
difficulty: hard
vuln_type: misc_unknown
tags: [H3C MSR3610, PPPoE, CHAP, PAP, 路由器配置, 思科命令, 密码恢复]
attack_chain: |
  1. 题目背景: L3HCTF2021 "hillst0ne" 题的延续 — L3HSec 公司有台 MSR3610 路由器，要升级但找不到 PPPoE 密码
  2. show current-configuration 输出含:
     - interface Dialer0: ppp chap password cipher $c$3$TKYJXT4RmMIvPHQX+5Ehf9oD3kjskIur3PGJfR/7fEyqfbx0K0DAokR0pd3rsRbWR5t9Cr3xSbYoPdogCg==
     - ppp chap user hustpppoe114514
     - ppp pap local-user hustpppoe114514 password cipher $c$3$3PbDU2m2/6Neiiz9iO+i641UKjafFMvrfphBc3fmrZ+9Q2TZu3g5l2Hlg1gJWO6ZQLJ4S+r85qU8EQpqQQ==
  3. CHAP 密码已用 $c$3$ 加密，但 PAP 密码用 $c$3$ 同样的格式
  4. 关键洞察: H3C 的 $c$3$ 加密算法在 HCL 模拟器 (H3C Cloud Lab) 上可以模拟解密 (模拟器是 L3HSec 自家产品)
  5. 拓扑重画: 原拓扑 GE0/0 没启用 → 改拓扑让 GE0/0 启用 + 配 pppoe-server 绑定 VT1
  6. 接口绑定 PPPoE 拨号 + 抓包 → 抓到 PPPoE Active Discovery / LCP / PAP/CHAP 握手
  7. CHAP 加密传输 (3 次握手，不传明文)，但 PAP 2 次握手传明文 → 抓明文密码
  8. 作者总结: PPPoE 必须保存明文密码用于认证 (CHAP 和 PAP 中 PAP 是明文)
key_payload: |
  # H3C MSR3610 配置 (Dialer0):
  interface Dialer0
   ppp chap password cipher $c$3$TKYJXT4RmMIvPHQX+5Ehf9oD3kjskIur3PGJfR/7fEyqfbx0K0DAokR0pd3rsRbWR5t9Cr3xSbYoPdogCg==
   ppp chap user hustpppoe114514
   ppp pap local-user hustpppoe114514 password cipher $c$3$3PbDU2m2/6Neiiz9iO+i641UKjafFMvrfphBc3fmrZ+9Q2TZu3g5l2Hlg1gJWO6ZQLJ4S+r85qU8EQpqQQ==
   dialer bundle enable
   dialer-group 2
   ip address ppp-negotiate
   nat outbound
  
  # 重画拓扑: GE0/0 启用 + pppoe-server 绑定 VT1
  
  # PAP vs CHAP 区别:
  # - PAP: 2 次握手，明文传输密码 (RFC 1334)
  # - CHAP: 3 次握手，不传明文密码
  # - PPPoE 必须保存明文密码认证用
one_liner: L3HCTF 2024 HHHC 一血题解 — H3C MSR3610 路由器配置中恢复 PPPoE 密码，靠 H3C 自家模拟器解 $c$3$ cipher + 重画拓扑抓 PAP 明文。
lesson: |
  - H3C $c$3$ cipher 是 H3C 私有加密，可在 HCL 模拟器上复现
  - PPPoE 协议下 PAP 是 2 次握手明文，CHAP 是 3 次握手密文
  - 路由器配置恢复需要在模拟器里重建完整拓扑
  - 抓包工具: Wireshark + PPPoE 过滤器 (pppoed || pppoes || lcp)
  - H3C 模拟器 HCL 是 L3HSec 自家产品，竞赛运维人员熟手
quality: high
---

# L3HCTF 2024 HHHC 一血题解

> 来源: ctfiot.com 161467 - L3HSec 公司 (竞赛运维方向)

## 题目背景

L3HCTF2021 "hillst0ne" 题的延续 — L3HSec 公司有台 H3C MSR3610 路由器，2021 年部署，要升级但找不到 PPPoE 密码。

```
Remember the "hillst0ne" challenge in L3HCTF2021?
L3HSec also has an MSR3610 router deployed since 2021.
Now we have decided to upgrade to a newer model,
but we couldn't find the PPPoE password.
Could you locate it in the existing configuration?
```

## show current-configuration 关键片段

```
[L3HSEC-ROUTER-1]show current-configuration
# version 7.1.064, Release 0821P16
interface Dialer0
 ppp chap password cipher $c$3$TKYJXT4RmMIvPHQX+5Ehf9oD3kjskIur3PGJfR/7fEyqfbx0K0DAokR0pd3rsRbWR5t9Cr3xSbYoPdogCg==
 ppp chap user hustpppoe114514
 ppp pap local-user hustpppoe114514 password cipher $c$3$3PbDU2m2/6Neiiz9iO+i641UKjafFMvrfphBc3fmrZ+9Q2TZu3g5l2Hlg1gJWO6ZQLJ4S+r85qU8EQpqQQ==
 dialer bundle enable
 dialer-group 2
 dialer timer idle 0
 dialer timer autodial 5
 ip address ppp-negotiate
 nat outbound
```

## 攻击链

1. **CHAP 密码已用 `$c$3$` 加密**：H3C 私有加密算法，需要 H3C 自家模拟器 HCL 解密
2. **PAP 密码同样用 `$c$3$` 加密**：L3HSec 公司恰好是 H3C 模拟器开发者
3. **重画拓扑**：原拓扑 GE0/0 没启用 → 改拓扑让 GE0/0 启用 + 配 `pppoe-server` 绑定 `VT1`
4. **接口绑定 PPPoE 拨号 + 抓包**：用 Wireshark 抓 PPPoE Active Discovery / LCP / PAP/CHAP 握手
5. **CHAP vs PAP**：
   - **CHAP (Challenge Handshake Authentication Protocol)**：3 次握手，不传明文密码
   - **PAP (Password Authentication Protocol)**：2 次握手，明文传输密码 (RFC 1334)
6. **PPPoE 必须保存明文密码用于认证** — 作者最终总结

## 作者经验

- 笔者是 L3HSec 公司的运维方向员工，**熟悉 H3C 设备**
- 笔者在 HCL 模拟器里跑完整拓扑复现拨号过程
- 预期解法是 Reverse (H3C $c$3$ 加密算法逆向)，作者走非预期用 HCL 模拟器直接解
- 抓包分析 PAP/CHAP 协议流程的细节，对理解 PPPoE 认证有教学意义

## 评价

特殊的"网络设备 + 模拟器"题，攻击面不在传统 web/pwn 而在国产网络设备的私有协议。

**亮点：**
- H3C `$c$3$` 加密算法的解密是 H3C 自家产品天然优势
- PPPoE CHAP vs PAP 的协议级区别是网络工程师必须掌握
- 重画拓扑 + 抓包分析是网络攻防实战的标准流程

**适用读者：** 网络安全竞赛运维 / H3C 设备管理员 / 网络协议研究者
