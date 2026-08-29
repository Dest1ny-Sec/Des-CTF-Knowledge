---
title: 第三届祥云杯-WriteUp by Mini-Venom
contest: 第三届祥云杯
year: 2021
difficulty: medium
vuln_type: deserialize
tags: [祥云杯, CC链CommonsCollections, Java反序列化, base64编码, Mini-Venom]
attack_chain: base64编码CC4链序列化字节→POST发送反序列化payload→RCE
key_payload: "import base64;from weakref import proxy;cc44.txt base64编码;POST Java反序列化"
one_liner: 第三届祥云杯Mini-Venom WP：CC链base64编码+Java反序列化RCE
lesson: CC链Java反序列化需base64编码后通过HTTP传输
quality: low
---

# 第三届祥云杯-WriteUp by Mini-Venom

**赛事**：第三届祥云杯（2021）

**Mini-Venom WP**：

**核心payload**：
```python
import base64
from weakref import proxy
import requests

file = open("/Users/wa1ki0g/webSec/javaUnserizlize/cc44.txt", "rb")
now = file.read()
ba = base64.b64encode(now)
# talk = requests.post("http://127.0.0.1:8080/", data=ba)
```

**攻击链**：
1. CC链CommonsCollections生成序列化字节
2. base64编码
3. POST到Java应用反序列化端点
4. RCE

**质量评估**：低（仅展示部分payload框架）
