---
title: 强网拟态 WriteUp by Mini-Venom (ChaMd5 Venom)
contest: 强网拟态(强网杯)
year: 2022
difficulty: hard
vuln_type: misc_unknown
tags: [PHP反序列化, 全角字符替换, Jinja2 SSTI, Node原型链, 区块链, ethereumjs-tx, 自定义VM, 二分搜索, 沙箱逃逸, ChaMd5_Venom, __proto__, 全角, fullwidth, 招新]
attack_chain: Web1:PHP反序列化order类f=trypass+hint=mochu7://prankhub/../../../../../../var/www/html/hint.php读hint → 全角a-z替换dict:request.application.__globals__.__builtins__.__import__ → Node原型链{"__proto__":{"command":["-c","cat /flag"]},"command":["-c","-i"]} → 区块链ethereumjs-tx签名+rawTx.data:0xa0f1d69c(_Cal(uint256,uint256)) → 二分搜索(15次log2(900000)=20)猜数字 → Pwn自定义VM\x2e\x3e\x2c\x3c指令构造+ORW
key_payload: 全角字符替换 + __proto__+command数组 + ethereumjs-tx _Cal+rawTx + 二分搜索15次+VM指令
one_liner: ChaMd5 Venom强网拟态全方向8+题:PHP反序列化+全角绕/Jinja2/Node原型链/区块链签名/二分搜索/自定义VM。
lesson: PHP反序列化用全角字符替换a-z绕SSTI黑名单;Node原型链__proto__.command数组注入;区块链用ethereumjs-tx签rawTx.data=_Cal(uint256,uint256)交互;二分搜索15次log2精度;自定义VM用\x2e\x3e\x2c\x3c字节码表示ADD/SUB/IF/PRINT指令。
quality: high
---
