---
title: 安徽大学生攻防赛 WriteUp - EDI安全
contest: 安徽大学生攻防赛 (EDI安全)
year: 2022
difficulty: medium
vuln_type: misc_unknown
tags: [RSA, dp_dq, CRT解密, 共模攻击, gcd, LCG, 线性同余, 迷宫DFS, EDI安全, debug, 招新]
attack_chain: Misc三题(直接给flag) → Re1调试得flag → Re2迷宫66x66 DFS路径 → Cr1 RSA dp/dq + CRT解密 → Cr2 n1 n2 gcd得p → Cr3 LCG逆推seed0
key_payload: RSA(CRT+dpdq) + gcd(n1,n2) + LCG(s3-s2=a(s2-s1) mod p) + DFS迷宫
one_liner: EDI安全2022安大攻防赛Misc 3题+Re 2题+Cr 3题,RSA三种解法全覆盖。
lesson: RSA三类解法:已知dp/dq用CRT求m;两n共享p用gcd;多seed题用LCG逆推(s3-s2=a(s2-s1) mod p);66x66迷宫用DFS+回溯(wasd路径);Re1调试技能题(flag{i_has_debugger_skill})。
quality: high
---
