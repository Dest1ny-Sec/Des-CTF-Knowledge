---
title: 科来杯第十届山东省大学生网络安全技能大赛wp
contest: 科来杯第十届山东省大学生网络安全技能大赛
year: 2023
difficulty: medium
vuln_type: misc_unknown
tags: [科来杯, 山东大学生网安赛, Misc/Web/Crypto/RE, 简单编码, base换表爆破, 取证, 二进制八进制混合, 数独]
attack_chain: 简单编码(2/8进制混合)→神秘的base(换表base64爆破)→签到→Stego→取证金刚大战哥斯拉→啊吧啊吧的数据包→小刘的硬盘→Web uns→Crypto小试牛刀/easyrsa→RE人生模拟
key_payload: "2/8进制混合解码;换表base64爆破;stego;forensic;uns web;easyrsa"
one_liner: 科来杯第十届山东省大学生网络安全技能大赛：Misc/Web/Crypto/RE综合WP
lesson: 综合性高校CTF赛常考：编码混合、换表base64、stego、forensic、web反序列化、RSA
quality: medium
---

# 科来杯第十届山东省大学生网络安全技能大赛wp

**赛事**：科来杯第十届山东省大学生网络安全技能大赛

**团队**：挽歌 / sp4c1ous / Charshark / Mu.Chen

**题目分类**：

**Misc**：
- 简单编码（二进制八进制混合）
- 神秘的base（换表base64爆破）
- 签到
- Stego（我应该去爱你）
- 数独
- 莫生气
- 取证：金刚大战哥斯拉、啊吧啊吧的数据包、小刘的硬盘
- Web: uns
- Crypto: 小试牛刀、easyrsa
- RE: 人生模拟

**简单编码题解**：
```python
import re
flag = ''
a = ['1010010','110001','1101011','0172','1010010','1000101','061','0132', ...]
for i in range(len(a)):
    if len(a[i]) == 4 or len(a[i]) == 3:
        flag += chr(int(a[i], 8))  # 8进制
    else:
        flag += chr(int(a[i], 2))  # 2进制
print(flag)
```

**神秘的base题解**：
```python
import base64
import string
import itertools
# 换表base64爆破
```

**质量评估**：中（综合性高校CTF题解集，难度中等）
