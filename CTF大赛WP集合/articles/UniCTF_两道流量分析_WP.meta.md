---
title: UniCTF 两道流量分析 WP
contest: UniCTF (YunSee团队)
year: 2025
difficulty: medium
vuln_type: forensic_traffic
tags: [modbus, opc_ua, dns, http, icmp, snmp, bkcrack, xor_key_recover, gzip_known_plaintext, tcp_reassemble, webshell_decrypt, scada_forensic]
attack_chain: 工厂应急响应 (7 任务):Modbus 0x05/ff00 → OPC UA ReadRequest → DNS 解析 → TCP 首连时间 → HTTP Host/URI → ICMP seq=0x0123 → SNMP OID → BlueBreath:TCP 8000 端口 bkcrack PNG 头明文攻击 → POST /uploads/shell.php → gzip 1f8b08 已知头推 XOR key → 解密 webshell 流量
key_payload: modbus.func_code==5 && modbus.data==ff:00 / bkcrack -C hint.zip -c hint.png -p png.header / KEY=b"dc3ef5ff0c670152" (16-byte XOR)
one_liner: YunSee 团队招新流量分析题，工厂应急响应 7 个 flag + BlueBreath XOR 加密 webshell 完整解密，HTTP+Modbus+OPC UA+SNMP 协议全接触。
lesson: Webshell 加密流量特征：gzip 头 1f 8b 08 是常见的"先压缩再异或"模板，可用已知明文反推 XOR key 头 9 字节再爆破。
quality: high
---
