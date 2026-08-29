---
title: 华为杯第一届中国研究生网络安全创新大赛实网对抗赛初赛(一)官方WP
contest: "华为杯第一届中国研究生网络安全创新大赛实网对抗赛初赛"
year: 2022
difficulty: hard
vuln_type: misc_unknown
tags: [hashCode绕过, QLExpressRCE, nashorn, ScriptEngineManager, CSP_Report_Only, CSP_bypass, eval, PHP_bypass_REMOTE_ADDR, 50x50_动态规划, 花指令_patch, LZSS解码, R/DFS路径]
attack_chain: babyql:hashCode=s[0]*31+s[1]逆推绕过黑名单 → QLExpress第一参数表达式执行 → 走Nashorn ScriptEngineManager绕黑名单(URL编码java.lang.Runtime.getInputStream反弹shell) → bbzl_shell:CSP-Report-Only report-uri=shell.php?+&bbzl's shell=system触发eval → 50x50:动态规划最大路径和DP[i][j]=max(DP[i][j-1],DP[i-1][j])+arr[i][j]求max_val → 验证:遍历input[i] R/D坐标移动累加和与max_val比对 → 迷宫:花指令75 03 74 01 e8 nop掉 → LZSS解码(bPreBufSizeBits=8,bWindowBufSizeBits=8,bThreshold=3)解"out"文件
key_payload: hashCode绕过串"guanzhujiarandundunjiechbO" + QLExpress+nashorn+java.lang.Runtime.getInputStream反弹shell + CSP-Report-Only绕过REMOTE_ADDR + 50x50 DP+RRDDRR路径 + 花指令0x75 0x03 0x74 0x01 0xe8 nop
one_liner: 华为杯研网赛初赛官方WP(一):hashCode+QLExpress+CSP+50x50DP+迷宫花指令+LZSS六题综合。
lesson: hashCode=s[0]*31+s[1]可逆推;QLExpress第一参数是表达式但有黑名单,绕Nashorn ScriptEngineManager;PHP eval需REMOTE_ADDR=127.0.0.1但CSP-Report-Only的report-uri可触发shell.php?内代码执行;50x50最大路径DP[i][j]=max(DP[i][j-1],DP[i-1][j])+arr;花指令识别0x75 03 74 01 e8模式;LZSS参数:bThreshold=3,bPreBufSizeBits=8。
quality: high
---
