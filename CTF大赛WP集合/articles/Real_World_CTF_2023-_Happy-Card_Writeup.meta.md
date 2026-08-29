---
title: Real World CTF 2023 - Happy-Card Writeup
contest: Real World CTF 2023
year: 2023
difficulty: high
vuln_type: misc_unknown
tags: [java-card, smartcard, apdu, cref-simulator, cap-file, offcardverifier, type-confusion, phi-attack, array-handle]
attack_chain:
  - JavaCard (智能卡) 模拟挑战 - hello.cap 文件 + cref_t1.exe wine 模拟器
  - 入口脚本 entrypoint.sh 跑 verifycap + scriptgen + apdutool
  - safe Applet: process(APDU) 处理 3 类指令
  - 0x00A4 SELECT FILE / 0x8888 SET secret / 0x8866 GET secret
  - secret = new byte[48] + isInit 标志
  - APDU[5:5+48] 复制到 secret + 二次 SET 覆盖
  - 攻击: 上传 恶意 exploit.exp 包绕过 verifycap
  - 1) verifycap 读 hello.cap 生成 .digest + 校验签名
  - 2) scriptgen 生成 APDU 脚本 (.script)
  - 3) apdutool 跑脚本触发 SELECT 0xA00000006203010801 + SET secret (攻击者可控) + GET
  - 4) 攻击者 APDU 覆盖 secret 为 0xAA*48
  - 5) 但 secret 写后只能 read 同样位置 → 经典 Oracle
  - 类型混淆攻击 (Phi Attack): Array 0x8000 标签 + 0x22 上下文 + 0x1C magic
  - ObjectHeader 6 字节头: objectTag + securityContext + classDef + package
  - 数组头: 0x8000 + 0x22 + 0x0 + 0x1C + length(2)
  - ExploitApplet: 0xda 引用 (Object ref) + 0xdb (byte[] ref) + 0x1234/0x5678 short
  - 关键: fromShort(short) 返回 null + fromShort(byte[]) 返回 this
  - 真实攻击: PhiProxy 拿 toShort + fromShort 链
  - 1) toShort(meMySelfAndI) → 短引用
  - 2) fromShort(meMySelfAndIHandle) → 同一对象但类型变为 byte[]
  - 3) 数组 read 偏移 0x2b5 拿到 secret 起始位置
  - 4) Util.arrayCopyNonAtomic(longarr, 0x2b5, buffer, 0, 0x85) 读 0x85 字节
  - 5) apdu.setOutgoingAndSend 0, 0x85 泄出 0x72 0x77 0x63 0x74 0x66 0x7b... = "rwctf{H4ppyCa3d...}"
key_payload: Util.arrayCopyNonAtomic(longarr, (short)0x2b5, buffer, (short)0, (short)0x85) + apdu.setOutgoingAndSend(0, 0x85)
one_liner: Real World CTF 2023 Happy-Card: JavaCard 智能卡 + cref 模拟器 + 类型混淆攻击 (Phi Attack) + toShort/fromShort 链 + arrayCopyNonAtomic 越界读 0x2b5 偏移泄 secret。
lesson: JavaCard 智能卡 APDU 协议 + 类型混淆是 CTF 高阶题；Phi 攻击 (PhiProxy/Phi.fromShort) 是 JavaCard 类型系统漏洞核心；arrayCopyNonAtomic 偏移 0x2b5 跳过 secret 头读 user data 是绕过 secret 存储保护的关键。
quality: high
---
